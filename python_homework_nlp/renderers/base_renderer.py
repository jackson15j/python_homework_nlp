from abc import ABC


class BaseRenderer(ABC):
    _rendered_output = None

    def __init__(self, input_dict: dict):
        self.input_dict = input_dict

    def render(self):
        raise NotImplementedError()

    @property
    def rendered_output(self):
        return self._rendered_output
