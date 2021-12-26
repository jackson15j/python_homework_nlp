import csv
from pathlib import Path
from python_homework_nlp.renderers.base_renderer import BaseRenderer


class CsvRenderer(BaseRenderer):
    """Renders the input dictionary as a CSV object."""

    def render(self) -> None:
        ret_val = []
        for word, sub_dict in self.input_dict.items():
            _word_count = f"{word} ({sub_dict['count']})"
            _docs = ",".join(sub_dict["files"])
            # FIXME: multiline field support seems to be messy in excel,
            # however, it is in the example requested table in the
            # `README.md`. eg.
            # https://stackoverflow.com/questions/10546933/inserting-multiline-text-in-a-csv-field
            _sentences = ";;".join(sub_dict["matches"])
            ret_val.append([_word_count, _docs, _sentences])
        self._rendered_output = ret_val

    def write_to_file(self, filepath: Path) -> None:
        # TODO: Create directories if doesn't exist.
        #
        fieldnames = [
            "Word (Total Occurrences)",
            "Documents",
            "Sentences containing the word",
        ]
        with open(str(filepath), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(fieldnames)
            writer.writerows(self._rendered_output)
