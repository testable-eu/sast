def invalidSastTool(tool):
    return f"sast tool not found in the sast yaml configuration: {tool}"


def invalidSastTools():
    return "Invalid sast tools or none of them could be selected for the task."
