from pathlib import Path
from typing import Any
from python_homework_nlp.common import Content
from python_homework_nlp.counter import Counter
from python_homework_nlp.file_reader import get_folder_contents
from python_homework_nlp.normaliser import Normaliser
from python_homework_nlp.renderers import CsvRenderer, JsonRenderer

OUTPUT_DIR = Path("build/output/")
OUTPUT_CSV = OUTPUT_DIR / "output.csv"
OUTPUT_JSON = OUTPUT_DIR / "output.json"


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
def get_rendered_output(workflow_output: dict, renderer) -> tuple[Any, Any]:
    print("Rendering output via: %r...", renderer)
    _renderer = renderer(workflow_output)
    _renderer.render()
    rendered_output = _renderer.rendered_output
    return rendered_output, _renderer


def main():
    # TODO: argparse
    parsed_args = cli_parser()
    # TODO: get folder path from `parsed_args`.
    content_objs = get_folder_contents(Path("test_docs"))

    # call main workflow.
    workflow_output = workflow(content_objs)
    # TODO: Render results
    json_rendered_output, json_renderer = get_rendered_output(
        workflow_output, JsonRenderer
    )
    csv_rendered_output, csv_renderer = get_rendered_output(
        workflow_output, CsvRenderer
    )
    csv_renderer.write_to_file(OUTPUT_CSV)
    # TODO: Update Renderers to use Content!!


if __name__ == "__main__":
    main()
