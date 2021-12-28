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

[PlantUml] design to solve the above problem (See: [PlantUml Design (original)]
& [initial design sketch] in [docs/] for my pre-[NLTK] investigation):

![PlantUml Design (current)][PlantUml Design (current)]

### Normaliser

Current implementation is using Stemming. This is documented as being typically
faster than Lemmatization at the cost of accuracy/quality.

### Counter

Current design uses _"2-passes"_ to go from filtered tokens to counts +
file/sentence mappings:

* Pass 0: tokenize/filter/stem words from content (`Normaliser`).
* Pass 1: Use [collections.Counter] to get a set of words+counts.
    * Currently counts are done per-sentence, then amalgamated together
      per-file and then all files.
* Pass 2: Loop through `Content` instances to discover file/sentence mappings
  for each word.
* [`python_homework_nlp/test_main.py::TestMain::test_workflow_with_real_docs`] takes ~0.7s to run `main.workflow` (`Normaliser` + `Counter`) on my Linux
  PC with an i7-8700 CPU.

Pros:

* Fast to get the `Word (Total Occurences)` column in the [Exercise]
  section's table.
* Could horizontally scale _"Pass 2"_ by using a task queue system and then
  amalgamating the results at the end.
* Can specify the a number for the top/most-common words as output from -"Pass
  1"_. ie. Save time in _"Pass 2"_.
* **Efficiency:** _"Pass 1"_ is _O(n)_ for the [collections.Counter] with a
  quick _O(n^3)_ to get a singular [collections.Counter] total.

Cons:

* _"Pass 2"_ is inefficient to get the `Documents`/`Sentences containing the
  word` columns in the [Exercise] section's table, due to doing a full pass of
  all sentences for each word.
* **Efficiency:** _"Pass 2"_ is: _O(n^3)_. For each word, for each file, for
  each sentence find a match.

#### Alternative Design Ideas

* Modifications to the above _"2-Pass"_ design:
    * juggle the _O(n^3)_ ordering. eg: For each file, for each sentence, for
      each word find a match.
    * Restructure code to benefit from caching. eg. [functools.lru_cache].
* _"Single-pass"_ where file/sentence mapping is recorded at point of
  normalising each sentence + increment a counter for each word when seen
  again.
    * Would need to flatten the files/sentences structure to avoid _O(n^3)_

## Usage

Either:

* `pip install <package.whl>` into a local virtualenv (See _"Releases"_ section
  for published wheels).
* Follow the steps in: [Contribute](#contribute) section.

You can then run the application via the entrypoint:

* `app`.
* `app --help` returns the usage.

Example:

```bash
$ app
[nltk_data] Downloading package punkt to /path/to/nltk_data...
[nltk_data]   Package punkt is already up-to-date!
[nltk_data] Downloading package stopwords to /path/to/nltk_data...
[nltk_data]   Package stopwords is already up-to-date!
Gathering `*.txt` file contents from the root of: test_docs ...
Calling main workflow.
-- Parsing file contents...
-- Counting words against files & sentences...
Render results.
-- Rendering output via: JsonRenderer...
-- Writing Rendered output to: build/output/output.json ...
-- Rendering output via: CsvRenderer...
-- Writing Rendered output to: build/output/output.csv ...
done.
$
```

**NOTE:** See `Releases` section for the rendered output for each tagged
release (generated by the `release` Github Action).

## Contribute

* Pre-req.: `curl -sSL https://install.python-poetry.org | python3 -` [Poetry
  Docs: install].
* Install dependencies: `poetry install`.
* Run tests: `poetry run pytest`.
* Build Wheel: `poetry build`.
* Run app: `poetry run app`.

**NOTE:** Explicitly not publishing this package to PyPI!! I don't want to
bloat the PyPI namespace with a point-in-time homework piece that wont have
on-going maintenance/support (beyond the initial learning/puzzle-solving
stage).

---

## Retrospective

### Things I've learnt?

* [Poetry]: never used it before, but so far seems to be what [Pipenv] should
  have been. No major pain (outside of the py3.10/pytest version bug) so far
  and very smooth.
* [NLTK]: never used it before. Interesting package with adequate reference
  examples. Had to do a general refresher on NLP terminology (and changes) from
  what terms were used in the rule-based NLP that I've interacted with in the
  past. Only scratched the surface so far.
* [mypy]: I've been pushing type hints usage on past work projects as we came
  to support those python versions in Production (We didn't us [mypy] in anger,
  due to the tech debt of warnings). Definitely benefited from the mypy
  warnings catching mistakes around single/double nested lists in function
  calls.
* [PlantUml] Proxy: Use the proxy to generate UML on page loads, instead of
  committing generated images into git.

### What would I improve (with additional time)?

**NOTE:** Follow is in addition to, or summary of, the `TODO` comments
intentionally left in the code.

* Additional Renderer's. eg. Markdown table, HTML, console.
* Fix bugs:
   * Multiline strings in single CSV field syntax.
   * TypeHint an ABC class correctly.
   * [NLTK] Data download singleton + remove `normaliser.py` import
     side-effect.
* Add [tox] for matrix building/testing of the application against python
  versions locally. **NOTE:** negated by the matrix building in CI
  (`python_app` Github Action).

### What would I change?

* [Poetry Docs: version]: I prefer discovering versions git tags, instead of
  forcing a commit/PR to bump. I've been using [PyPA: setuptools_scm] to do
  this in current projects. Need to investigate how other uses of [Poetry]
  handle versioning.
* Try out and profile [Alternative Design Ideas].
* [NLTK]: Try out different Stemming/Lemmatizing calls in [NLTK] to compare
  speed vs quality of results.
* [NLTK]: investigate best practices for managing [NLTK] Data in Production
  code. eg. gathering data dependencies at build-time vs run-time. Packing data
  into built wheel or not?
[documents]: test_docs/

[NLTK]: https://www.nltk.org/
[Boost Spirit]: https://www.boost.org/doc/libs/1_78_0/libs/spirit/doc/html/index.html
[Poetry]: https://python-poetry.org
[Poetry Docs: install]: https://python-poetry.org/docs/master/#installation
[Poetry Docs: version]: https://python-poetry.org/docs/master/cli/#version
[PDM]: https://pdm.fming.dev
[PEP-517]: https://www.python.org/dev/peps/pep-0517/
[Pipenv]: https://pipenv.pypa.io/en/latest/

[PlantUml]: https://plantuml.com
[PlantUml Design (original)]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_nlp/e1d67c16eba3cdf9b9c03dffbdcda4a77919dc6d/docs/design.plantuml
[PlantUml Design (current)]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_nlp/main/docs/design.plantuml
[docs/]: docs/
[initial design sketch]: docs/initial_design_sketch_before_investigating_nltk.jpg
[collections.Counter]: https://docs.python.org/3/library/collections.html#collections.Counter
[Exercise]: #exercise
[`python_homework_nlp/test_main.py::TestMain::test_workflow_with_real_docs`]: tests/test_main.py
[functools.lru_cache]: https://docs.python.org/3/library/functools.html#functools.lru_cache

[PyPA: setuptools_scm]: https://github.com/pypa/setuptools_scm/
[mypy]: mypy-lang.org
[Alternative Design Ideas]: #alternative-design-ideas
[tox]: https://tox.wiki/en/latest/index.html
