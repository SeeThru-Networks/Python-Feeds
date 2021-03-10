class ConfigException(Exception):
    pass


class NoConfigException(ConfigException):
    pass


class HeaderException(ConfigException):
    pass


class ScriptException(ConfigException):
    script_name: str

    def __init__(self, message, script_name):
        super().__init__(message)

        self.script_name = script_name


class ScriptMetaException(ScriptException):
    pass


class ScriptStateException(ScriptException):
    pass


class ScriptFillableException(ScriptException):
    name: str

    def __init__(self, message, script_name, fillable_name):
        super().__init__(message, script_name)

        self.name = fillable_name


class FeedException(ConfigException):
    name: str

    def __init__(self, message, feed_name):
        super().__init__(message)

        self.name = feed_name


class ApiKeyException(ConfigException):
    name: str

    def __init__(self, message, api_key_name):
        super().__init__(message)

        self.name = api_key_name


if __name__ == "__main__":
    raise ScriptStateException("", "", "")
