from copy import copy
from SeeThru_Feeds.Model.Properties.Exceptions import InvalidPropertyType, PropertyRequired, InvalidPropertyValue, PropertyValidatorError

class PropertyBase():
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

    @staticmethod
    def NewInstance(self):
        """Returns a new instance of the property, this is used by the property manager

        Returns:
            PropertyBase: The property copy
        """
        return copy(self)

    @property
    def value(self):
        """Provides a getter for the value of an instance of the property
        Parses the instance's value

        Returns:
            Any: The parsed value of the property
        """
        # The value should be provided by the PropertyManager
        if not hasattr(self, "_value"):
            raise Exception("Value attribute has not been set for property")

        return self._value
    @value.setter
    def value(self, value):
        """Sets the value to the property

        Args:
            value ([type]): [description]
        """
        # Validates that the value given is valid
        if self.ParseValue(value):
            self._value = value

class FillableProperty(PropertyBase):
    def __init__(self, name=None, default=None, required=True, ofType=None, valueSet=None, custom=None):
        """
        Defines the fillable property with the parameters that the property should take

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
            raise PropertyRequired(self.name)
        # --Type check, ensures that the value is of a type in ofType
        if self.ofType != None:
            if type(self.ofType) == list:
                if type(value) not in self.ofType:
                    raise InvalidPropertyType(self.name, value, self.ofType)
            else:
                if value != None and type(value) != self.ofType:
                    raise InvalidPropertyType(self.name, value, self.ofType)
        # --Value check, checks that the value is in the set given
        if self.valueSet != None and value not in self.valueSet:
            raise InvalidPropertyValue(self.name, value, self.valueSet)
        # --Runs the custom function to check the value
        if self.custom != None and not self.custom(value):
            raise PropertyValidatorError(self.name, value)
        return True


class ResultProperty(PropertyBase):
    def __init__(self, name=None, default=None, ofType=None, valueSet=None, custom=None):
        """
        Defines the result property with the parameters that the property should take

        Keyword Arguments:
            name {string} -- The internal name of the property (default: {None})
            defailt {Any} -- A default value
            ofType {Type, [Type]} -- A type or set of types that a value of the property must be (default: {None})
            valueSet {Set, list, range} -- A set of values that the property must be (default: {None})
            func {function pointer} -- A custom function to run to check the value that must return a boolean (default: {None})
        """
        if type(name) != str and name != None:
            raise TypeError("Invalid type for 'name'")
        self.name = name

        self.default = default

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
        # --Type check, ensures that the value is of a type in ofType
        if self.ofType != None:
            if type(self.ofType) == list:
                if type(value) not in self.ofType:
                    raise InvalidPropertyType(self.name, value, self.ofType)
            else:
                if value != None and type(value) != self.ofType:
                    raise InvalidPropertyType(self.name, value, self.ofType)
        # --Value check, checks that the value is in the set given
        if self.valueSet != None and value not in self.valueSet:
            raise InvalidPropertyValue(self.name, value, self.valueSet)
        # --Runs the custom function to check the value
        if self.custom != None and not self.custom(value):
            raise PropertyValidatorError(self.name, value)
        return True