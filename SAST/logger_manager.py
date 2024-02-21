import config


def logger_name(name: str) -> str:
    return config.rootLoggerName + "." + name
