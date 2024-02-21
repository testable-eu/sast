import os
from SAST.src import is_windows, get_exception_message, build_timestamp_language_name, zipdir
from datetime import datetime
import zipfile


class TestUtils:
    def test_is_windows(self):
        assert is_windows() == (os.name == 'nt')

    def test_get_exception_message(self):
        e = Exception('Test Exception')
        assert get_exception_message(e) == "Test Exception"

    def test_build_timestamp_language_name(self):
        now = datetime(2022, 1, 1, 0, 0, 0)
        name = "PythonCode"
        language = "python"
        extra = "extra"
        assert build_timestamp_language_name(name, language, now,
                                             extra) == "2022-01-01-00-00-00_extra_python_PythonCode"
        assert build_timestamp_language_name(name, language, now) == "2022-01-01-00-00-00_python_PythonCode"

    def test_zipdir(self, tmp_path):
        zip_file = zipfile.ZipFile(tmp_path / 'test.zip', 'w')
        zipdir('TestDir', zip_file)
        assert (tmp_path / 'test.zip').is_file()

    def test_load_sast_specific_config(self, monkeypatch):
        pass
