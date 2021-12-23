# python_homework_nlp

[![Python application](https://github.com/jackson15j/python_homework_nlp/actions/workflows/python_app.yml/badge.svg)](https://github.com/jackson15j/python_homework_nlp/actions/workflows/python_app.yml)
[![Release](https://github.com/jackson15j/python_homework_nlp/actions/workflows/release.yml/badge.svg)](https://github.com/jackson15j/python_homework_nlp/actions/workflows/release.yml)

Python homework exercise to pull out words of interest from text files via NLP.

## Exercise

From the [documents] provided:

* Produce a list of the most frequent interesting words.
* Summary table showing where those words appear (sentences and documents) eg.

  Word (Total Occurrences)|Documents|Sentences containing the word
  ------------------------|---------|-----------------------------
  Philosophy (42) | x,y,z | I don't have time for **philosophy**<br /><br />**Surely this was a touch of fine philosophy;** though no doubt he had never heard there was such a thing as that.<br /><br />Still, her pay-as-you-go **philosophy** implies it.
  ... | ... | ...

## Personal Aims

* To show-off the type of developer I am:
    * Solution design & planning.
    * List assumptions & reasoning for my choices.
    * Documentation (docs, code comments, commit messages).
    * Workflow (CI, tests, concise commits).
* To learn new packages:
    * [NLTK] - I've only worked on rule-based NLP products built in C++ ([Boost
      Spirit]). Recently found out that [NLTK] is a great python alternative.
    * [Poetry] - I've heard great things about [Poetry] from @mikeymo for
      years, but not had a chance to experiment (and potentially) migrate
      Current Production code away from [PEP-517] style packaging
      (`setup.cfg`/`pyproject.toml`) to [Poetry].
        * Had also found that [PDM] seems to be a good alternative, but feels
          like there is an upfront education cost for it to be smooth sailing
          to use in Production.
        * Previously used [Pipenv] but my opinions have soured after the mix of
          issues; Pypa distancing themselves from [Pipenv] usage in Production
          vs using [PEP-517] config, non-OS-agnostic lock files and dependency
          graphs breaking easily.

## Design

[PlantUml] design to solve the above problem (See: [initial design sketch] in
[docs/] for my pre-[NLTK] investigation):

![PlantUml Design][PlantUml Design]

## Usage

Either:

* `pip install <package.whl>` into a local virtualenv (See _"Releases"_ section
  for published wheels) and then run the entrypoint: `<TODO: add entrypoint>`.
* Follow the steps in: [Contribute](#contribute) section.

## Contribute

* Pre-req.: `curl -sSL https://install.python-poetry.org | python3 -` [Poetry:
  install].
* Install dependencies: `poetry install`.
* Run tests: `poetry run pytest`.
* Build Wheel: `poetry build`.
* Run app: `<TODO: add entrypoint>`.

**NOTE:** Explicitly not publishing this package to PyPI!! I don't want to
bloat the PyPI namespace with a point-in-time homework piece that wont have
on-going maintenance/support (beyond the initial learning/puzzle-solving
stage).


[documents]: test_docs/

[NLTK]: https://www.nltk.org/
[Boost Spirit]: https://www.boost.org/doc/libs/1_78_0/libs/spirit/doc/html/index.html
[Poetry]: https://python-poetry.org
[Poetry: install]: https://python-poetry.org/docs/master/#installation
[PDM]: https://pdm.fming.dev
[PEP-517]: https://www.python.org/dev/peps/pep-0517/
[Pipenv]: https://pipenv.pypa.io/en/latest/

[PlantUml]: https://plantuml.com
[PlantUml Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_nlp/main/docs/design.plantuml
[docs/]: docs/
[initial design sketch]: docs/initial_design_sketch_before_investigating_nltk.jpg
