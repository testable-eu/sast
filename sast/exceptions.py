import sast.errors as errors


class SastScanFailed(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
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
