from pathlib import Path
import yaml
from typing import Dict
import sys

DIR: Path = Path(__file__).parent.resolve()
SAST_DIR: Path = DIR.parent.parent.resolve()
sys.path.append(str(SAST_DIR))

from sast.semgrep.core.semgrep import Semgrep


class Semgrep_v_1_79_0(Semgrep):

    def __init__(self):
        self.tool = "semgrep_1_79_0"
        self.SEMGREP_SCRIPT_DIR: Path = Path(__file__).parent.resolve()
        self.SEMGREP_CONFIG_FILE: Path = self.SEMGREP_SCRIPT_DIR / "config.yaml"
        with open(self.SEMGREP_CONFIG_FILE) as sast_config_file:
            self.SEMGREP_CONFIG: Dict = yaml.load(sast_config_file, Loader=yaml.Loader)
