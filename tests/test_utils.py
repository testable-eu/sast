import os
from sast.utils import is_windows, get_exception_message, build_timestamp_language_name, zipdir, \
    load_sast_specific_config, filter_sast_tools, get_class_from_str
from datetime import datetime
import zipfile
from unittest.mock import patch, call
import pytest
from sast.exceptions import InvalidSastTool, InvalidSastTools
import sast.config


@pytest.fixture
def sast_tools():
    return [
        {"name": "dummyTool1", "version": "1.0.0"},
        {"name": "dummyTool2", "version": "2.0.0"}
    ]


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

    @patch('sast.utils.load_yaml')
    def test_load_sast_specific_config(self, mock_load_yaml, sast_tools):
        tool_name = sast_tools[0]['name']
        tool_version = sast_tools[0]['version']

        mock_load_yaml.side_effect = [
            {"tools": {tool_name: {"version": {tool_version: {"config": "dummyTool/config.yaml"}}}}},
            {"name": tool_name,
             "version": tool_version,
             "tool_interface": "sast.dummyTool1.dummyTool1",
             "supported_languages": ["JAVA", "PHP", "JS"]
             }
        ]

        result = load_sast_specific_config(tool_name, tool_version)

        assert result == {"name": tool_name,
                          "version": tool_version,
                          "tool_interface": "sast.dummyTool1.dummyTool1",
                          "supported_languages": ["JAVA", "PHP", "JS"]
                          }
        mock_load_yaml.assert_has_calls(
            [call(sast.config.SAST_CONFIG_FILE), call(sast.config.ROOT / "dummyTool/config.yaml")])

    @patch('sast.utils.load_yaml')
    def test_load_sast_specific_config_fail_when_tool_not_found(self, mock_load_yaml):
        tool_name = "dummyTool"
        tool_version = "1.0.0"
        mock_load_yaml.side_effect = InvalidSastTool("Invalid SAST Tool")
        with pytest.raises(InvalidSastTool):
            load_sast_specific_config(tool_name, tool_version)

    @patch('sast.utils.load_sast_specific_config')
    def test_filter_sast_tools_success(self, mock_load_sast_config, sast_tools):
        # Arrange
        input_tools = sast_tools
        language = 'JAVA'
        mock_load_sast_config.return_value = {'supported_languages': ['JAVA', 'PHP']}

        # Act
        result = filter_sast_tools(input_tools, language)

        # Assert
        assert result == input_tools
        mock_load_sast_config.assert_called_with('dummyTool2', '2.0.0')

    @patch('sast.utils.load_sast_specific_config')
    def test_filter_sast_tools_no_tools_found(self, mock_load_sast_config, sast_tools):
        # Arrange
        input_tools = sast_tools
        language = 'Ruby'
        mock_load_sast_config.return_value = {'supported_languages': ['JAVA', 'PHP']}

        # Act and Assert
        InvalidSastTool("Invalid SAST Tool")
        with pytest.raises(InvalidSastTools):
            filter_sast_tools(input_tools, language)

    def test_get_class_from_str_failure(self):
        class_str = "non.existing.module.ClassName"

        with pytest.raises(ImportError):
            get_class_from_str(class_str)

    def test_get_class_from_str_success(self):
        class_str = "os.path.abspath"

        result = get_class_from_str(class_str)

        assert result == os.path.abspath
