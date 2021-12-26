from python_homework_nlp.renderers.json_renderer import JsonRenderer


class TestJsonRenderer:
    def test_json_renderer(self):
        input_dict = {"a": 1}
        exp = {"a": 1}
        renderer = JsonRenderer(input_dict)
        renderer.render()
        assert renderer.rendered_output == exp
