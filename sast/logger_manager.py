from sast.config import ROOT_LOGGER_NAME


def logger_name(name: str) -> str:
    return ROOT_LOGGER_NAME + "." + name
