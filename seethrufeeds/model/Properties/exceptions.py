class InvalidPropertyType(Exception):
    def __init__(self, name, value, typeSet):
        self.name = name
        self.value = value
        self.typeSet = typeSet

    def __str__(self):
        return f"[Property: {self.name}] Type of {self.value} not in {self.typeSet}"


class InvalidPropertyValue(Exception):
    def __init__(self, name, value, valueSet):
        self.name = name
        self.value = value
        self.valueSet = valueSet

    def __str__(self):
        return f"[Property: {self.name}] {self.value} not in {self.valueSet}"


class PropertyValidatorError(Exception):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"[Property: {self.name}] {self.value} does not pass custom validator"


class PropertyRequired(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"[Property: {self.name}] Value not provided"
