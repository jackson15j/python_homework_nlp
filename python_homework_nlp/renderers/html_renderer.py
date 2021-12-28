from pathlib import Path
from python_homework_nlp.renderers.base_renderer import BaseRenderer


class HtmlRenderer(BaseRenderer):
    """Renders the input dictionary to the a HTML file."""

    def render(self) -> None:
        ret_val = f"""
<title>Python Homework NLP Output</title>
<h1>Python Homework NLP Output</h1>

<p>Below is the output from this application based off the originally supplied
files:</p>

<table border="1">
  <tr>
    <th>{"</th><th>".join(self.field_names)}</th>
  </tr>
"""
        for word, sub_dict in self.input_dict.items():
            _word_count = f"{word} ({sub_dict['count']})"
            _docs = ",".join(sub_dict["files"])
            _sentences = "<br>".join(sub_dict["matches"])
            ret_val += f"""
  <tr>
    <td>{_word_count}</td>
    <td>{_docs}</td>
    <td>{_sentences}</td>
  </tr>
"""
        ret_val += "\n</table>"
        self._rendered_output = ret_val

    def write_to_file(self, filepath: Path) -> None:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(self.rendered_output)
