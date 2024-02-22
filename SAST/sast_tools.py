from importlib import import_module
from sast.utils import load_sast_specific_config
from typing import Dict, Callable
from sast.sast_interface import SAST


def get_class_from_str(class_str: str) -> Callable[[], SAST]:
    try:
        module_path, class_name = class_str.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(class_str)


def get_sast_tool(tool_name: str, tool_version) -> SAST:
    sast_config: Dict = load_sast_specific_config(tool_name, tool_version)
    sast_interface_class: str = sast_config["tool_interface"]
    sast_class = get_class_from_str(sast_interface_class)
    sast: SAST = sast_class()
    return sast
