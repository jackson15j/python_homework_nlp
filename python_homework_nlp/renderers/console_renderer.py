from python_homework_nlp.renderers.base_renderer import BaseRenderer


class ConsoleRenderer(BaseRenderer):
    """Renders the input dictionary to the console."""

    def render(self) -> None:
        _sentence_indent = " | ".join([" " * len(x) for x in self.field_names])
        ret_val = f"""
Python Homework NLP Output
==========================

Below is the output from this application based off the originally supplied
files:

{" | ".join(self.field_names)}
{" | ".join(["-" * len(x) for x in self.field_names])}
"""
        for word, sub_dict in self.input_dict.items():
            _word_count = f"{word} ({sub_dict['count']})"
            _docs = ",".join(sub_dict["files"])
            _sentences = f"\n{_sentence_indent}".join(sub_dict["matches"])
            ret_val += " | ".join([_word_count, _docs, _sentences])
        self._rendered_output = ret_val

    def write_to_file(self, *args, **kwargs) -> None:
        print(self.rendered_output)
