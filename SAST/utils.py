import os
import zipfile
from typing import NoReturn
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import yaml
from sast.exceptions import InvalidSastTool, InvalidSastTools
from sast.config import ROOT


def zipdir(path, zip_file: zipfile.ZipFile) -> NoReturn:
    for root, dirs, files in os.walk(str(path)):
        for file in files:
            zip_file.write(os.path.join(str(root), str(file)),
                           os.path.relpath(os.path.join(str(root), str(file)),
                                           os.path.join(str(path), '..')))


def is_windows() -> bool:
    return os.name == 'nt'


def get_exception_message(e: Exception) -> str:
    if hasattr(e, 'message'):
        return e.message
    elif hasattr(e, 'msg'):
        return e.msg
    else:
        return str(e)


def build_timestamp_language_name(name: Path | str, language: str, now: datetime, extra: str = None) -> str:
    res = f"{language}_{name}"
    if extra:
        res = f"{extra}_{res}"
    if now:
        now_str = now.strftime("%Y-%m-%d-%H-%M-%S")
        res = f"{now_str}_{res}"
    return res


def sast_tool_version_match(v1, v2, nv_max=3, ignore_saas=True) -> bool:
    if ignore_saas and (v1 == "saas" or v2 == "saas"):
        return True
    sv1 = v1.split(".")
    sv2 = v2.split(".")
    nv = max(len(sv1), len(sv2))
    for i in range(0, min(nv, nv_max)):
        try:
            if sv1[i] != sv2[i]:
                return False
        except IndexError:
            return False
    return True


def load_yaml(fpath) -> Dict:
    with open(fpath) as f:
        fdict: Dict = yaml.load(f, Loader=yaml.Loader)
    return fdict


def load_sast_specific_config(tool_name: str, tool_version: str) -> Dict:
    try:
        tool_config_path: Path = load_yaml(ROOT / 'sast-config.yaml')["tools"][tool_name]["version"][tool_version][
            "config"]
    except KeyError:
        e = InvalidSastTool(f"{tool_name}:{tool_version}")
        raise e
    return load_yaml(ROOT / tool_config_path)


def filter_sast_tools(itools: list[Dict], language: str, exception_raised=True) -> List[Dict]:
    for t in itools:
        t["supported_languages"] = load_sast_specific_config(t["name"], t["version"])["supported_languages"]
    tools = list(filter(lambda x: language in x["supported_languages"], itools))
    if exception_raised and not tools:
        e = InvalidSastTools()
        raise e
    return tools
