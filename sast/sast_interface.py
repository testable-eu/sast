from __future__ import annotations
import abc
import logging
import sast.utils as utils

from pathlib import Path
from typing import Dict, Tuple, Optional, List
from datetime import datetime
from sast.logger_manager import logger_name


logger = logging.getLogger(logger_name(__name__))


class SAST(metaclass=abc.ABCMeta):
    tool = None

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "launcher") and callable(subclass.launcher) and
                hasattr(subclass, "inspector") and callable(subclass.inspector) and
                hasattr(subclass, "get_tool_version") and callable(subclass.get_tool_version) or
                NotImplemented)

    @abc.abstractmethod
    async def launcher(self, src_dir: Path, language: str, output_dir: Path, **kwargs) -> Path:
        raise NotImplementedError

    @abc.abstractmethod
    def inspector(self, sast_res_file: Path, language: str) -> list[Dict]:
        """
        Shall return a list of Dict s.t. :
        [{
            type: "",
            file: "",
            line: ""
        }, ...]
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def get_tool_version(self) -> str:
        raise NotImplementedError
    

    @abc.abstractmethod
    async def populate_dataflow(self, sast_findings: List[SastFinding]) -> List[SastFinding]:
        raise NotImplementedError
    

    @staticmethod
    def build_project_name(name: str, tool: str | None, language: str, timestamp: bool = True):
        now = None
        if timestamp:
            now = datetime.now()
        if tool:
            comp = f"{tool}_{name}"
        else:
            comp = name
        return utils.build_timestamp_language_name(comp, language, now, extra="TPF")

    def logging(self, what="launcher", message=None, status=None):
        message_str = ""
        if message:
            message_str = f" - {message}"
        status_str = ""
        if status:
            status_str = f": {status}"
        logger.info(f"SAST tool {self.tool} - {what}{message_str}{status_str}")

    @staticmethod
    def get_norm_vuln(vuln: str, d_supported_vuln_map: Dict):
        for norm_vuln in d_supported_vuln_map:
            if SAST.vuln_match(d_supported_vuln_map[norm_vuln], vuln):
                return norm_vuln
        return None

    @staticmethod
    # simple sub-string but it could be elaborated more
    def vuln_match(vcand, vtarget):
        return vcand in vtarget


class SastFinding(metaclass=abc.ABCMeta):
    def __init__(self, sast_tool: SAST,  src_filename: str, src_line: str, dest_filename: str, dest_line: str, vuln_type: str,  dataflow: Optional[Tuple[int]] = None):
        self.sast_tool = sast_tool
        self.src_filename = src_filename
        self.src_line = src_line
        self.dest_filename = dest_filename
        self.dest_line = dest_line
        self.dataflow = dataflow
        self.vuln_type = vuln_type


    def get_all_attributes_as_tuple(self) -> Tuple:
        return (self.src_filename, self.src_line, self.dest_filename, self.dest_line, self.dataflow, self.vuln_type)

    def get_attributes_without_dataflow_as_tuple(self) -> Tuple:
        return (self.src_filename, self.src_line, self.dest_filename, self.dest_line, self.vuln_type)


    def get_alert(self) -> Dict:
        return {
                'sast_tool': self.sast_tool.tool,
                'file': self.dest_filename,
                'file_row': self.dest_line,
                'vuln_type': self.vuln_type,
            }
    
    def get_summary(self) -> Dict:
        return {
            'sast_tool': self.sast_tool.tool,
            'src_filename': self.src_filename,
            'src_line': self.src_line,
            'dest_filename': self.dest_filename,
            'dest_line': self.dest_line,
            'vuln_type': self.vuln_type,
        }
    