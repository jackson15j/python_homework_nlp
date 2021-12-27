import json
from pathlib import Path
from python_homework_nlp.renderers.base_renderer import BaseRenderer


class JsonRenderer(BaseRenderer):
    """Renders the input dictionary as a JSON dict."""

    def render(self) -> None:
        self._rendered_output = json.loads(json.dumps(self.input_dict))

    def write_to_file(self, filepath: Path) -> None:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(json.dumps(self.rendered_output))
