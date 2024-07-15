import asyncio
import json
import shutil
import logging
import os

from pathlib import Path
from typing import Dict

import sast.config
from sast.logger_manager import logger_name
from sast.sast_interface import SAST
import config

logger = logging.getLogger(logger_name(__name__))

class Semgrep(SAST):
    tool = "semgrep"

    SEMGREP_SCRIPT_DIR: Path = None
    SEMGREP_CONFIG_FILE: Path = None
    SEMGREP_CONFIG: Dict = None

    async def launcher(self, src_dir: Path, language: str, output_dir: Path, **kwargs) -> Path:
        self.logging(what="launcher", status="started...")
        # project_name: str = f"TPF_{language}_{src_dir.name}_{uuid.uuid4()}"
        project_name: str = SAST.build_project_name(src_dir.name, self.tool, language, timestamp=True)
        proj_dir_tmp: Path = output_dir / project_name
        proj_dir_tmp.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src_dir, proj_dir_tmp / "src")
        print(f"AOOOOOOOOOOOOOOOOOOOOOOOO {self.SEMGREP_CONFIG['installation_path']}")
        logger.info(f"DIO BESTIA {self.SEMGREP_CONFIG['installation_path']}")  
        src_root: Path = (proj_dir_tmp / "src").resolve()  
        semgrep_analyze_cmd = f"{self.SEMGREP_CONFIG['installation_path']}/semgrep-1.79.0/cli/bin/semgrep scan -q --config 'p/xss' --config 'p/sql-injection' --config 'p/phpcs-security-audit' --json {src_root} > {proj_dir_tmp}/{project_name}.txt"
        semgrep_analyze = await asyncio.create_subprocess_shell(semgrep_analyze_cmd)
        await semgrep_analyze.wait()
        self.logging(what="launcher", message=f"scanning", status="done.")

        res = proj_dir_tmp / f"{project_name}.txt"
        self.logging(what="launcher", message=f"result {res}", status="done.")
        return res

    def inspector(self, sast_res_file: Path, language: str) -> list[Dict]:
        self.logging(what="inspector", status="started...")
        with open(sast_res_file) as res_file:
            semgrep_report: Dict = json.load(res_file)

        findings: list[Dict] = []
        for result in semgrep_report["results"]:
            finding: Dict = {
                "type": result["extra"]["metadata"]["vulnerability_class"],
                "type_orig": result["check_id"],
                "file": result["path"],
                "line": result["end"]["line"]
            }
            findings.append(finding)
            #self.logging(what="inspector", message=f"{findings}")#manudebug
        self.logging(what="inspector", status="done.")
        return findings

    async def get_tool_version(self) -> str:
        return self.SEMGREP_CONFIG["version"]
