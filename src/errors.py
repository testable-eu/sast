def invalidSastTool(tool):
    return f"SAST tool not found in the SAST yaml configuration: {tool}"


def invalidSastTools():
    return "Invalid SAST tools or none of them could be selected for the task."
