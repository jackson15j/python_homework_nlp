from pathlib import Path


def get_folder_contents(dir_path: Path) -> dict:
    """Scrape the root-level of a folder for `*.txt` files and return a
    dictionary of file content against file names.

    :param pathlib.Path dir_path: Path of directory to glob for `*.txt` files.
    :returns: dict of: `{<file_name>: <file_content>, ...}`.
    """
    ret_val = {}
    for f in dir_path.glob("*.txt"):
        if not f.is_file():
            continue
        ret_val[f.name] = f.read_text()
    return ret_val
