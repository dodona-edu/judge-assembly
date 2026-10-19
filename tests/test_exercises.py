"""Runs the judge on every submission in tests/exercises and compares its
feedback with the expected output.

Meant to run as root inside the judge image. Set UPDATE_EXPECTED=1 to
(re)write the expected output instead of comparing against it.
"""

import contextlib
import difflib
import fnmatch
import glob
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(TESTS_DIR)
EXERCISES_DIR = os.path.join(TESTS_DIR, "exercises")

UPDATE_EXPECTED = os.environ.get("UPDATE_EXPECTED") == "1"
JUDGE_TIMEOUT = 120
LANGUAGES = ("en", "nl")

# gcc names its intermediate object files randomly.
COMPILER_DETAILS = [
    (re.compile(r"/tmp/cc[0-9A-Za-z]{6}\.o\b"), "/tmp/cc<random>.o"),
]


def judge_ignore():
    """A shutil.copytree ignore function that leaves out what Dodona's sync
    of the judge leaves out."""
    with open(os.path.join(REPO_DIR, ".dodonaignore")) as f:
        lines = [line.strip() for line in f]
    patterns = [line for line in lines if line and not line.startswith("#")]

    def ignore(directory, names):
        # Not tracked, so Dodona never syncs them.
        ignored = {".git", ".claude", "__pycache__"}
        for name in names:
            path = "/" + os.path.relpath(os.path.join(directory, name), REPO_DIR)
            if os.path.isdir(os.path.join(directory, name)):
                path += "/"
            # Only anchored patterns; a trailing slash matches directories only.
            if any(fnmatch.fnmatchcase(path, p) or fnmatch.fnmatchcase(path, p + "/") for p in patterns):
                ignored.add(name)
        return ignored

    return ignore


def make_sandbox_root():
    # Dodona mounts everything under /mnt/<random>/.
    if not os.access("/mnt", os.W_OK):
        raise RuntimeError("/mnt is not writable: run the suite as root, like CI")
    return tempfile.mkdtemp(dir="/mnt")


@contextlib.contextmanager
def sandbox(root, exercise_dir, submission):
    """Lays out the resources, submission and workdir for one run, and removes
    them afterwards."""
    resources = os.path.join(root, "resources")
    source = os.path.join(root, "submission", "source")
    workdir = os.path.join(tempfile.gettempdir(), "workdir")
    try:
        shutil.copytree(os.path.join(exercise_dir, "evaluation"), resources)
        os.makedirs(os.path.dirname(source))
        shutil.copyfile(submission, source)
        os.mkdir(workdir)
        yield {"resources": resources, "source": source, "workdir": workdir}
    finally:
        for path in (resources, os.path.dirname(source), workdir):
            shutil.rmtree(path, ignore_errors=True)


def parse_commands(output):
    """The judge writes partial feedback: a stream of JSON commands."""
    decoder = json.JSONDecoder()
    commands = []
    position = 0
    while True:
        while position < len(output) and output[position].isspace():
            position += 1
        if position == len(output):
            return commands
        command, position = decoder.raw_decode(output, position)
        commands.append(command)


def normalise(value):
    if isinstance(value, str):
        for pattern, replacement in COMPILER_DETAILS:
            value = pattern.sub(replacement, value)
        return value
    if isinstance(value, list):
        return [normalise(v) for v in value]
    if isinstance(value, dict):
        return {k: normalise(v) for k, v in value.items()}
    return value


def dump(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def diff(a, b, a_name, b_name):
    return "".join(difflib.unified_diff(a.splitlines(True), b.splitlines(True), a_name, b_name))


def binutils_version():
    output = subprocess.run(["as", "--version"], capture_output=True, text=True, check=True).stdout
    return re.search(r"([0-9]+\.[0-9]+)(\.[0-9]+)*$", output.splitlines()[0]).group(1)


def cases():
    for exercise in sorted(os.listdir(EXERCISES_DIR)):
        exercise_dir = os.path.join(EXERCISES_DIR, exercise)
        for submission in sorted(glob.glob(os.path.join(exercise_dir, "submissions", "*.s"))):
            yield exercise, os.path.basename(submission)[: -len(".s")]


class ExerciseTest(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.root = make_sandbox_root()
        cls.addClassCleanup(shutil.rmtree, cls.root)
        cls.judge = os.path.join(cls.root, "judge")
        shutil.copytree(REPO_DIR, cls.judge, ignore=judge_ignore())
        cls.binutils_version = binutils_version()

    def run_judge(self, exercise_dir, submission, language):
        config = {
            "time_limit": 10,
            "memory_limit": 536870912,
        }
        with open(os.path.join(exercise_dir, "config.json")) as f:
            config.update(json.load(f))
        config.update(
            {
                "programming_language": "assembly",
                "natural_language": language,
                "judge": self.judge,
            }
        )
        with sandbox(self.root, exercise_dir, submission) as paths:
            config.update(paths)
            return subprocess.run(
                ["/main.sh", os.path.join(self.judge, "run")],
                input=json.dumps(config),
                capture_output=True,
                text=True,
                cwd=paths["workdir"],
                timeout=JUDGE_TIMEOUT,
            )

    def feedback(self, exercise_dir, submission, language):
        """The normalised feedback of one judge run, as JSON text."""
        process = self.run_judge(exercise_dir, submission, language)
        self.assertEqual(
            process.returncode, 0, "judge exited with {}\nstderr:\n{}".format(process.returncode, process.stderr)
        )
        self.assertEqual(process.stderr, "", "judge wrote to stderr")
        try:
            feedback = parse_commands(process.stdout)
        except json.JSONDecodeError as e:
            self.fail("judge output is not JSON ({})\nstdout:\n{}".format(e, process.stdout))
        if not feedback:
            self.fail("judge wrote no feedback")
        return dump(normalise(feedback))

    def expected_file(self, exercise_dir, case):
        """<case>.binutils<major>.<minor>.json when it exists for the running
        binutils version, else <case>.json."""
        expected_dir = os.path.join(exercise_dir, "expected")
        versioned = os.path.join(expected_dir, "{}.binutils{}.json".format(case, self.binutils_version))
        if os.path.exists(versioned):
            return versioned
        return os.path.join(expected_dir, case + ".json")

    def compare(self, expected_file, output):
        if not os.path.exists(expected_file):
            self.fail(
                "no expected output, run with UPDATE_EXPECTED=1 to create " + os.path.relpath(expected_file, REPO_DIR)
            )
        with open(expected_file) as f:
            expected = dump(json.load(f))
        if output != expected:
            self.fail("output differs from the expected output:\n" + diff(expected, output, "expected", "actual"))

    def check_case(self, exercise, case):
        exercise_dir = os.path.join(EXERCISES_DIR, exercise)
        submission = os.path.join(exercise_dir, "submissions", case + ".s")
        expected_file = self.expected_file(exercise_dir, case)
        suffix = os.path.splitext(case)[1].lstrip(".")
        language = suffix if suffix in LANGUAGES else "en"

        output = self.feedback(exercise_dir, submission, language)
        if UPDATE_EXPECTED:
            os.makedirs(os.path.dirname(expected_file), exist_ok=True)
            with open(expected_file, "w") as f:
                f.write(output)
        else:
            self.compare(expected_file, output)


for exercise, case in cases():
    setattr(
        ExerciseTest,
        re.sub(r"\W", "_", "test_{}_{}".format(exercise, case)),
        lambda self, exercise=exercise, case=case: self.check_case(exercise, case),
    )


if __name__ == "__main__":
    unittest.main()
