from sast.utils import load_sast_specific_config, get_class_from_str
from typing import Dict
from sast.sast_interface import SAST


def get_sast_tool(tool_name: str, tool_version) -> SAST:
    sast_config: Dict = load_sast_specific_config(tool_name, tool_version)
    sast_interface_class: str = sast_config["tool_interface"]
    sast_class = get_class_from_str(sast_interface_class)
    sast: SAST = sast_class()
    return sast
