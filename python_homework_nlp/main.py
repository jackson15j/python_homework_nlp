from argparse import ArgumentParser, Namespace
from pathlib import Path
from python_homework_nlp.common import Content
from python_homework_nlp.counter import Counter
from python_homework_nlp.file_reader import get_folder_contents
from python_homework_nlp.normaliser import Normaliser
from python_homework_nlp.renderers import CsvRenderer, JsonRenderer

OUTPUT_DIR = Path("build/output/")
OUTPUT_CSV = OUTPUT_DIR / "output.csv"
OUTPUT_JSON = OUTPUT_DIR / "output.json"
FILEPATH_LOOKUP = {
    CsvRenderer: OUTPUT_CSV,
    JsonRenderer: OUTPUT_JSON,
}

# TODO: Sanitise all TODO's!
# TODO: Test + time Normaliser + Counter!! ie. Core logic time.
# TODO: Write Retrospective section in `README.md`.
# TODO: `typeddict` typehints.
# TODO: Improve efficiency around `original_sentence` lookup to sentence
# matching. Aim: single loop.


def cli_parser() -> Namespace:
    """Parse CLI flags.

    :returns: `argparse.Namesapce` of parsed CLI arguments.
    """
    parser = ArgumentParser(description="Python Homework NLP")

    parser.add_argument(
        "-n",
        "--num_most_common_words",
        type=int,
        help=(
            "Reduce the rendered output to the <int> most common words. If "
            "absent, then all words (non-Stopwords/punction) are returned."
        ),
        default=None,
    )
    parser.add_argument(
        "-d",
        "--docs_dir",
        type=Path,
        help=(
            "Directory of `*.txt` files for the application to render results "
            "from. Default: `test_docs/`."
        ),
        default=Path("test_docs/"),
    )

    parsed_args = parser.parse_args()
    return parsed_args


def workflow(content_objs: list[Content], parsed_args: Namespace) -> dict:
    """High-level Workflow to run through all of the NLP parsing of the
    supplied text, as well as doing the word counts against files/sentences.

    :param list[Content] content_objs` Content instances for each file to process.
    :param argparse.Namespace: Parsed CLI args.
    :returns: dict of output to be rendered.
    """
    print("-- Parsing file contents...")
    for content in content_objs:
        _normaliser = Normaliser(content)
        _normaliser.normalise()

    print("-- Counting words against files & sentences...")
    counter = Counter(content_objs)
    ret_dict = counter.counter(parsed_args.num_most_common_words)
    # TODO: Should counter change to populate `Context` with word counts ??
    return ret_dict


# FIXME: re-investigate the correct way to type hint an ABC class explicitly.
def render_output(workflow_output: dict, renderer) -> None:
    """Renders the output from the `Counter` to a more human readable form and
    then writes it to a file in: `build/output/`.

    :param dict workflow_output: Dict of `Counter` results to render. Expect:
    {<word>: {"count": <int>, "matches": [<str>,], "files": [<str>,]}}
    :param BaseRenderer renderer: Render to use.
    """
    print(f"-- Rendering output via: {renderer.__name__}...")
    _renderer = renderer(workflow_output)
    _renderer.render()
    _ = _renderer.rendered_output
    _filepath = FILEPATH_LOOKUP[renderer]
    print(f"-- Writing Rendered output to: {_filepath} ...")
    _renderer.write_to_file(_filepath)


def main():
    args = cli_parser()
    print(
        f"Gathering `*.txt` file contents from the root of: {args.docs_dir} ..."
    )
    content_objs = get_folder_contents(args.docs_dir)

    print("Calling main workflow.")
    workflow_output = workflow(content_objs, args)
    print("Render results.")
    # TODO: Update Renderers to use Content ??
    render_output(workflow_output, JsonRenderer)
    render_output(workflow_output, CsvRenderer)
    print("done.")


if __name__ == "__main__":
    main()
