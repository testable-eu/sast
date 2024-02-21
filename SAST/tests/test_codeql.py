import pytest
from pathlib import Path
from SAST.codeql import CodeQL_v_2_9_2

test_resources_path = Path(__file__).resolve() / 'resources'


@pytest.mark.asyncio
class TestCodeQL:

    def test_inspector(self):
        sarif_file = test_resources_path / "TPF_JS_codeql_2_9_2_1_instance_1_unset_element_array.sarif"
        language: str = "JS"
        inspection = CodeQL_v_2_9_2().inspector(sarif_file, language)
        assert inspection[0]["type"] == "xss"
        assert inspection[0]["line"] == 33

    async def test_launcher(self, tmp_path):
        # TODO
        pass
