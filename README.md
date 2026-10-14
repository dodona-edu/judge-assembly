# Assembly judge for [Dodona](https://dodona.ugent.be/)

## Recommended exercise directory structure

> [More info about repository directory structure](https://docs.dodona.be/en/references/repository-directory-structure/#example-of-a-valid-repository-structure)

```text
+-- README.md                           # Optional: Describes the repository
+-- dirconfig.json                      # Shared config for all exercises in subdirs
+-- 📂public                            # Optional: Contains files that belong to the course or series
|   +-- my_picture.png                  # Optional: An image to reuse throughout the course
+-- 📂exercises                         # We could group exercises in a folder
|   +-- 📂first_html_exercise           # Folder name for the exercise
|   |   +-- config.json                 # ▶ Configuration of the exercise
|   |   +-- 📂evaluation                # -- 🔽️ ADD YOUR FILES HERE 🔽 --
|   |   |   +-- plan.json               # A JSON file describing what tests to run
|   |   +-- 📂solution                  # Optional: This will be visible in Dodona for teaching staff
|   |   |   +-- solution.s              # Optional: The model solution file
|   |   +-- 📂description               #
|   |       +-- description.nl.md       # ▶ The description in Dutch
|   |       +-- description.en.md       # Optional: The description in English
|   |       +-- 📂media                 # Optional folder
|   |       |   +-- some_image.png      # Optional: An image used in the description and/or exercise
|   |       +-- 📂boilerplate           # Optional folder
|   |           +-- boilerplate         # Optional: loaded automatically in submission text area
|   :
:
```

## Recommended `dirconfig.json`

> [More info about exercise directory structure](https://docs.dodona.be/en/references/exercise-directory-structure/)

````json
{
  "type": "exercise",
  "programming_language": "assembly",
  "access": "public",
  "evaluation": {
    "time_limit": 10,
    "memory_limit": 50000000
  },
  "labels": [
    "assembly",
    "calling convention",
    "loops"
  ],
  "author": "Firstname Lastname <firstname_lastname@ugent.be>",
  "contact": "firstname_lastname@ugent.be"
}
````

## Sample exercises

See https://github.com/nielsdos/dodona-assembly-exercises/tree/main/exercises/narayana-x86-32-at%26t for a full sample exercise setup.

## Tests

The judge image is built from
[`dodona-assembly.dockerfile`](https://github.com/dodona-edu/docker-images/blob/master/dodona-assembly.dockerfile)
in docker-images and published as `ghcr.io/dodona-edu/dodona-assembly`.

`tests/` runs the judge on the submissions in `tests/exercises/*/submissions`
and compares its feedback with `tests/exercises/*/expected`. The suite runs as
root inside the judge image: `devel/run-tests.sh` runs it there, as CI does,
and `devel/run-tests-in-image.sh` starts the image and runs it locally:

```
devel/run-tests-in-image.sh                                # ghcr.io/dodona-edu/dodona-assembly:latest
IMAGE=my-image devel/run-tests-in-image.sh -v -k narayana  # another image, unittest arguments
UPDATE_EXPECTED=1 devel/run-tests-in-image.sh              # rewrite the expected output
```

Each exercise has an `evaluation/` directory with its plan and a `config.json`
with the `evaluation` keys Dodona merges into the run configuration. A
submission named `<case>.nl.s` runs with Dutch as natural language.

## Acknowledgements

This judge was based on the work of four students of Ghent University for the cross-course project (vakoverschrijdend project ingenieurswetenschappen computerwetenschappen, 2022-2023):

* Gilles De Praetere
* Wout De Saegher
* Joris Pockelé
* Stijn Verbeken

Based on the HTML judge (https://github.com/dodona-edu/judge-html) made by:

* **S. De Clercq**
* **Q. Vervynck**
* T. Ramlot
* B. Willems
