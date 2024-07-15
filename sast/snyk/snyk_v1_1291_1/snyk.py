from pathlib import Path
import yaml
from typing import Dict
import sys

DIR: Path = Path(__file__).parent.resolve()
SAST_DIR: Path = DIR.parent.parent.resolve()
sys.path.append(str(SAST_DIR))

from sast.snyk.core.snyk import Snyk


class Snyk_v_1_1291_1(Snyk):

    def __init__(self):
        self.tool = "snyk_1_1291_1"
        self.SNYK_SCRIPT_DIR: Path = Path(__file__).parent.resolve()
        self.SNYK_CONFIG_FILE: Path = self.SNYK_SCRIPT_DIR / "config.yaml"
        with open(self.SNYK_CONFIG_FILE) as sast_config_file:
            self.SNYK_CONFIG: Dict = yaml.load(sast_config_file, Loader=yaml.Loader)
