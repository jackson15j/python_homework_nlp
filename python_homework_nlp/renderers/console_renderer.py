from python_homework_nlp.renderers.base_renderer import BaseRenderer


class ConsoleRenderer(BaseRenderer):
    """Renders the input dictionary to the console."""

    def render(self) -> None:
        _sentence_indent = " | ".join([" " * len(x) for x in self.field_names])
        ret_val = []
        for word, sub_dict in self.input_dict.items():
            _word_count = f"{word} ({sub_dict['count']})"
            _docs = ",".join(sub_dict["files"])
            _sentences = f"\n{_sentence_indent}".join(sub_dict["matches"])
            ret_val.append([_word_count, _docs, _sentences])
        self._rendered_output = ret_val

    def write_to_file(self, *args, **kwargs) -> None:
        print(" | ".join(self.field_names))
        print(" | ".join(["-" * len(x) for x in self.field_names]))
        for row in self.rendered_output:
            print(" | ".join(row))
