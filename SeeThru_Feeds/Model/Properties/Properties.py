class PropertyBase():
    # Checks that the value given has met the conditions of the property
    # Arguments:    -A value    -Any
    def ParseValue(self, value):
        """
        Checks that the value given has met the conditions of the property

        Arguments:
            value {Any} -- The value associated with this property

        Raises:
            NotImplementedError: The function hasn't been implemented yet for the subclass
            Exception: The property is None but it is required

        Returns:
            [boolean] -- Whether the value given is valid for the property
        """
        raise NotImplementedError(
            "ParseValue function not implemented yet for property")


class FillableProperty(PropertyBase):
    def __init__(self, name=None, default=None, required=True, ofType=None, valueSet=None, custom=None):
        """
        Defines the fillable property with the parameters that the property should take,
        the property is a static member of a component class and should not be instance
        dependent

        Keyword Arguments:
            name {string} -- The internal name of the property (default: {None})
            defailt {Any} -- A default value
            required {bool} -- Whether a value of the property has to be given, i.e. not None (default: {True})
            ofType {Type, [Type]} -- A type or set of types that a value of the property must be (default: {None})
            valueSet {Set, list, range} -- A set of values that the property must be (default: {None})
            func {function pointer} -- A custom function to run to check the value that must return a boolean (default: {None})
        """
        if type(name) != str and name != None:
            raise TypeError("Invalid type for 'name'")
        self.name = name

        self.default = default

        if type(required) != bool:
            raise TypeError("Invalid type for 'required'")
        self.required = required

        self.ofType = ofType

        if type(valueSet) == set or type(valueSet) == list or type(valueSet) == range:
            self.valueSet = set(valueSet)
        elif valueSet == None:
            self.valueSet = valueSet
        else:
            raise TypeError("Invalid type for 'valueSet'")

        if not callable(custom) and custom != None:
            raise TypeError("Invald type for 'func'")
        self.custom = custom

    def ParseValue(self, value):
        # --Required check
        if self.required and value == None:
            raise Exception(
                "[Property: {}] This property is required".format(self.name))
        # --Type check, ensures that the value is of a type in ofType
        if self.ofType != None:
            if type(self.ofType) == list:
                if type(value) not in self.ofType:
                    raise Exception(
                        "[Property: {}] Value given is not of a valid type".format(self.name))
            else:
                if value != None and type(value) != self.ofType:
                    raise Exception(
                        "[Property: {}] Value given is not of a valid type".format(self.name))
        # --Value check, checks that the value is in the set given
        if self.valueSet != None and value not in self.valueSet:
            raise ValueError(
                "[Property: {}] Value given is not a valid value".format(self.name))
        # --Runs the custom function to check the value
        if self.custom != None and not self.custom(value):
            raise Exception(
                "[Property: {}] Value given does not pass custom check".format(self.name))
        return True


class ResultProperty(PropertyBase):
    # Defines what the property is
    # Arguments:    -The property name, defaults to variable name   -String
    def __init__(self, name=None, default=None):
        self.name = name
        self.default = default
