import json
from python_homework_nlp.renderers.base_renderer import BaseRenderer


class JsonRenderer(BaseRenderer):
    """Renders the input dictionary as a JSON dict."""

    def render(self) -> None:
        self._rendered_output = json.loads(json.dumps(self.input_dict))
