from pathlib import Path
import yaml
from typing import Dict
import sys

DIR: Path = Path(__file__).parent.resolve()
SAST_DIR: Path = DIR.parent.parent.resolve()
sys.path.append(str(SAST_DIR))

from sast.bearer.core.bearer import Bearer


class Bearer_v_1_45_0(Bearer):

    def __init__(self):
        self.tool = "bearer_1_45_0"
        self.BEARER_SCRIPT_DIR: Path = Path(__file__).parent.resolve()
        self.BEARER_CONFIG_FILE: Path = self.BEARER_SCRIPT_DIR / "config.yaml"
        with open(self.BEARER_CONFIG_FILE) as sast_config_file:
            self.BEARER_CONFIG: Dict = yaml.load(sast_config_file, Loader=yaml.Loader)
