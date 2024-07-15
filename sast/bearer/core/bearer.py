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

class Bearer(SAST):
    tool = "bearer"

    BEARER_SCRIPT_DIR: Path = None
    BEARER_CONFIG_FILE: Path = None
    BEARER_CONFIG: Dict = None

    async def launcher(self, src_dir: Path, language: str, output_dir: Path, **kwargs) -> Path:
        self.logging(what="launcher", status="started...")
        project_name: str = SAST.build_project_name(src_dir.name, self.tool, language, timestamp=True)
        proj_dir_tmp: Path = output_dir / project_name
        proj_dir_tmp.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src_dir, proj_dir_tmp / "src")
        src_root: Path = (proj_dir_tmp / "src").resolve()
        
        bearer_analyze_cmd = f"{self.BEARER_CONFIG['installation_path']}/bearer scan {src_root} --scanner=sast,secrets --report dataflow --quiet > {proj_dir_tmp}/{project_name}.txt"
        bearer_analyze = await asyncio.create_subprocess_shell(bearer_analyze_cmd)
        await bearer_analyze.wait()
        self.logging(what="launcher", message=f"scanning", status="done.")

        res = proj_dir_tmp / f"{project_name}.txt"
        self.logging(what="launcher", message=f"result {res}", status="done.")
        return res

    def inspector(self, sast_res_file: Path, language: str) -> list[Dict]:
        self.logging(what="inspector", status="started...")
        with open(sast_res_file) as res_file:
            bearer_report: Dict = json.load(res_file)

        findings: list[Dict] = []
        for risk in bearer_report["risks"]:
            for elem in risk["locations"]:
                finding: Dict = {
                    "type": risk["detector_id"],
                    "type_orig": risk["detector_id"],
                    "file": elem["filename"],
                    "line": elem["end_line_number"]
                }
                findings.append(finding)
        self.logging(what="inspector", status="done.")
        return findings

    async def get_tool_version(self) -> str:
        return self.BEARER_CONFIG["version"]
    
    async def populate_dataflow(self, sast_findings):
        return super().populate_dataflow(sast_findings)