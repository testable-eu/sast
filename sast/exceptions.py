import sast.errors as errors


class SastScanFailed(Exception):
    pass


class InvalidSastTool(Exception):
    def __init__(self, tool, message=None):
        if message:
            self.message = message
        else:
            self.message = errors.invalidSastTool(tool)
        super().__init__(self.message)


class InvalidSastTools(Exception):
    def __init__(self, message=None, tool=None):
        if message:
            self.message = message
        else:
            self.message = errors.invalidSastTools()
        super().__init__(self.message)
