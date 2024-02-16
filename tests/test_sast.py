from pathlib import Path
import pytest
from unittest.mock import Mock, patch
from src.sast import SAST


class SASTTestSubclass(SAST):
    async def launcher(self, src_dir: Path, language: str, output_dir: Path, **kwargs) -> Path: pass

    def inspector(self, sast_res_file: Path, language: str) -> list: pass

    async def get_tool_version(self) -> str: pass


# Test for launcher method
@patch.object(SASTTestSubclass, 'launcher')
@pytest.mark.asyncio
async def test_launcher(mock_launcher):
    sast = SASTTestSubclass()
    src_dir = Mock(spec=Path)
    language = 'Python'
    output_dir = Mock(spec=Path)
    mock_launcher.return_value = output_dir
    result = await sast.launcher(src_dir, language, output_dir)
    assert result == output_dir


@patch.object(SASTTestSubclass, 'inspector')
def test_inspector(mock_inspector):
    sast = SASTTestSubclass()
    sast_res_file = Mock(spec=Path)
    language = 'Python'
    mock_inspector.return_value = []
    result = sast.inspector(sast_res_file, language)
    assert result == []


@patch.object(SASTTestSubclass, 'get_tool_version')
@pytest.mark.asyncio
async def test_get_tool_version(mock_get_tool_version):
    sast = SASTTestSubclass()
    mock_get_tool_version.return_value = '1.0.0'
    result = await sast.get_tool_version()
    assert result == '1.0.0'
