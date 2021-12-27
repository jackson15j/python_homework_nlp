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


def cli_parser():
    pass


def workflow(content_objs: list[Content]) -> dict:
    print("Parsing file contents...")
    for content in content_objs:
        _normaliser = Normaliser(content)
        _normaliser.normalise()
    counter = Counter(content_objs)
    ret_dict = counter.counter()
    # TODO: Should counter change to populate `Context` with word counts ??
    return ret_dict


# FIXME: re-investigate the correct way to type hint an ABC class explicitly.
def render_output(workflow_output: dict, renderer) -> None:
    print(f"Rendering output via: {renderer!r} ...")
    _renderer = renderer(workflow_output)
    _renderer.render()
    _ = _renderer.rendered_output
    _filepath = FILEPATH_LOOKUP[renderer]
    print(f"Writing Rendered output to: {_filepath} ...")
    _renderer.write_to_file(_filepath)


def main():
    # TODO: argparse
    _ = cli_parser()
    # TODO: get folder path from `parsed_args`.
    _input_path = Path("test_docs/")
    print(f"Gathering `*.txt` file contents from the root of: {_input_path} ...")
    content_objs = get_folder_contents(_input_path)

    # call main workflow.
    workflow_output = workflow(content_objs)
    # Render results
    # TODO: Update Renderers to use Content ??
    render_output(workflow_output, JsonRenderer)
    render_output(workflow_output, CsvRenderer)
    print("...done.")


if __name__ == "__main__":
    main()
