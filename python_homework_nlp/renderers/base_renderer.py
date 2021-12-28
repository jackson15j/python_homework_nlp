from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseRenderer(ABC):
    _rendered_output: Any = None
    field_names = (
        "Word (Total Occurrences)",
        "Documents",
        "Sentences containing the word",
    )

    def __init__(self, input_dict: dict):
        self.input_dict = input_dict

    @abstractmethod
    def render(self):
        """Method to render the supplied data into the required representation.

        .. note::
            Writes rendered output to the `rendered_output` property for
            downstrream usage.
        """

    @abstractmethod
    def write_to_file(self, filepath: Path) -> None:
        """Writes the `rendered_output` to a file.

        .. note::
            Handles creation of missing directories.

        :param pathlib.Path filepath: filepath to write to.
        """

    @property
    def rendered_output(self):
        return self._rendered_output
