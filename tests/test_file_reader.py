from python_homework_nlp.file_reader import get_folder_contents


class TestFileReader:
    def test_get_folder_contents(self, tmp_path):
        exp1 = "One line."
        exp2 = "First Sentence.\nSecond line."
        not_exp1 = (
            "NOTE: Should not hit a file in a sub-folder! Not mentioned in "
            "current requirements."
        )
        not_exp2 = (
            "NOTE: Should not read non-`*.txt` files! Not mentioned in "
            "current requirements"
        )
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        _subfolder = tmp_path / "subfolder"
        _subfolder.mkdir()
        file3 = _subfolder / "file3.txt"
        file4 = tmp_path / "file4.md"
        file1.write_text(exp1)
        file2.write_text(exp2)
        file3.write_text(not_exp1)
        file4.write_text(not_exp2)

        ret_val = get_folder_contents(tmp_path)
        assert len(ret_val) == 2
        assert ret_val[0].file_name == file1.name
        assert ret_val[0].original_content == exp1
        assert ret_val[1].file_name == file2.name
        assert ret_val[1].original_content == exp2
