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

## Acknowledgements

Based on the HTML judge (https://github.com/dodona-edu/judge-html) made by:

* **S. De Clercq**
* **Q. Vervynck**
* T. Ramlot
* B. Willems
