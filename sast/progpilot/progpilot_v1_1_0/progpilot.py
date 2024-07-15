from pathlib import Path
import yaml
from typing import Dict
import sys

DIR: Path = Path(__file__).parent.resolve()
SAST_DIR: Path = DIR.parent.parent.resolve()
sys.path.append(str(SAST_DIR))

from sast.progpilot.core.progpilot import Progpilot


class Progpilot_v_1_1_0(Progpilot):

    def __init__(self):
        self.tool = "progpilot_1_1_0"
        self.PROGPILOT_SCRIPT_DIR: Path = Path(__file__).parent.resolve()
        self.PROGPILOT_CONFIG_FILE: Path = self.PROGPILOT_SCRIPT_DIR / "config.yaml"
        with open(self.PROGPILOT_CONFIG_FILE) as sast_config_file:
            self.PROGPILOT_CONFIG: Dict = yaml.load(sast_config_file, Loader=yaml.Loader)
