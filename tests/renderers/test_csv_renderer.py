from python_homework_nlp.renderers.csv_renderer import CsvRenderer


class TestCsvRenderer:
    input_dict = {
        "final": {
            "count": 1,
            "matches": ["Final SENTENCE!"],
            "files": [
                "file1",
            ],
        },
        "sentence": {
            "count": 3,
            "matches": [
                "First sentence.",
                "Second is sentences.",
                "Final SENTENCE!",
            ],
            "files": [
                "file1",
                "file2",
            ],
        },
    }

    def test_csv_renderer(self):
        exp = [
            ["final (1)", "file1", "Final SENTENCE!"],
            [
                "sentence (3)",
                "file1,file2",
                "First sentence.;;Second is sentences.;;Final SENTENCE!",
            ],
        ]
        renderer = CsvRenderer(self.input_dict)
        renderer.render()
        assert renderer.rendered_output == exp

    def test_write_to_file(self, tmp_path):
        # NOTE: the escaped list of files when there are more than one!
        exp = """
final (1),file1,Final SENTENCE!
sentence (3),"file1,file2",First sentence.;;Second is sentences.;;Final SENTENCE!
"""
        tmp_csv = tmp_path / "tmp.csv"
        renderer = CsvRenderer(self.input_dict)
        renderer.render()
        assert not tmp_csv.exists()

        renderer.write_to_file(tmp_csv)
        assert tmp_csv.exists()
        print(renderer._rendered_output)
        print(tmp_csv.read_text())
        assert exp in tmp_csv.read_text()
