from pathlib import Path
from typing import Generator, Union
from python_homework_nlp.common import Content


def get_folder_contents(dir_path: Path, sort_files: bool = True) -> list[Content]:
    """Scrape the root-level of a folder for `*.txt` files and return a
    dictionary of file content against file names.

    :param pathlib.Path dir_path: Path of directory to glob for `*.txt` files.
    :param bool sort_files: Sorts the files discovered.
    :returns: list of: Content.
    """
    ret_val = []
    files: Union[list[Path], Generator[Path, None, None]] = dir_path.glob("*.txt")
    if sort_files:
        # Test helper for deterministic results without additional test code to
        # discover arbitrary order from the glob generator.
        files = list(files)
        files.sort()

    for f in files:
        if not f.is_file():
            continue
        _content = Content()
        _content.file_name = f.name
        _content.original_content = f.read_text()
        ret_val.append(_content)
    return ret_val
