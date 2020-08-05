from copy import copy
from SeeThru_Feeds.Model.Properties.Exceptions import InvalidPropertyType, PropertyRequired, InvalidPropertyValue, \
    PropertyValidatorError


class PropertyBase:
    def __init__(self, name):
        if type(name) != str and name is not None:
            raise TypeError("Invalid type for 'name'")
        self.name = name
        self._value = None

    def parse_value(self, value):
        """
        Checks that the value given has met the conditions of the property

        Arguments:
            value (any): The value associated with this property

        Raises:
            NotImplementedError: The function hasn't been implemented yet for the subclass
            Exception: The property is None but it is required

        Returns:
            bool: Whether the value given is valid for the property
        """
        raise NotImplementedError("parse_value function not implemented yet for property")

    @staticmethod
    def new_instance(self):
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
            value (any): The value to assign to the property

        """
        # Validates that the value given is valid
        if self.parse_value(value):
            self._value = value


class FillableProperty(PropertyBase):
    def __init__(self, name=None, default=None, required=False, of_type=None, value_set=None, custom=None):
        """
        Defines the fillable property with the parameters that the property should take

        Args:
            name (str): The internal name of the property
            default (any): A default value
            required (bool): Whether this property is required
            of_type (type, [type]): A type or a set of types that the property can be
            value_set (set, list, range]): A set of values that the property can be
            custom (lambda): A lambda function to check the value against
        """
        super().__init__(name)

        self.default = default

        if type(required) != bool:
            raise TypeError("Invalid type for 'required'")
        self.required = required

        self.ofType = of_type

        if type(value_set) == set or type(value_set) == list or type(value_set) == range:
            self.valueSet = set(value_set)
        elif value_set is None:
            self.valueSet = value_set
        else:
            raise TypeError("Invalid type for 'value_set'")

        if not callable(custom) and custom is not None:
            raise TypeError("Invalid type for 'func'")
        self.custom = custom

    def parse_value(self, value):
        """
        Ensures that the value provided is valid

        Args:
            value (any): The value to check against

        Returns:
            bool: Whether the value is valid

        """
        # --Required check
        if self.required and value is None:
            raise PropertyRequired(self.name)
        # --Type check, ensures that the value is of a type in of_type
        if self.ofType is not None:
            if type(self.ofType) == list:
                if type(value) not in self.ofType:
                    raise InvalidPropertyType(self.name, value, self.ofType)
            else:
                if value is not None and type(value) != self.ofType:
                    raise InvalidPropertyType(self.name, value, self.ofType)
        # --Value check, checks that the value is in the set given
        if self.valueSet is not None and value not in self.valueSet:
            raise InvalidPropertyValue(self.name, value, self.valueSet)
        # --Runs the custom function to check the value
        if self.custom is not None and not self.custom(value):
            raise PropertyValidatorError(self.name, value)
        return True


class ResultProperty(PropertyBase):
    def __init__(self, name=None, default=None, of_type=None, value_set=None, custom=None):
        """
        Defines the result property with the parameters that the property should take

        Args:
            name (str): The internal name of the property
            default (any): A default value
            of_type (type, [type]): A type or a set of types that the property can be
            value_set (set, list, range): A set of values that the property can be
            custom (lambda): A lambda function to check the value against
        """
        super().__init__(name)

        self.default = default

        self.ofType = of_type

        if type(value_set) == set or type(value_set) == list or type(value_set) == range:
            self.valueSet = set(value_set)
        elif value_set is None:
            self.valueSet = value_set
        else:
            raise TypeError("Invalid type for 'value_set'")

        if not callable(custom) and custom is not None:
            raise TypeError("Invalid type for 'func'")
        self.custom = custom

    def parse_value(self, value):
        # --Type check, ensures that the value is of a type in of_type
        if self.ofType is not None:
            if type(self.ofType) == list:
                if type(value) not in self.ofType:
                    raise InvalidPropertyType(self.name, value, self.ofType)
            else:
                if value is not None and type(value) != self.ofType:
                    raise InvalidPropertyType(self.name, value, self.ofType)
        # --Value check, checks that the value is in the set given
        if self.valueSet is not None and value not in self.valueSet:
            raise InvalidPropertyValue(self.name, value, self.valueSet)
        # --Runs the custom function to check the value
        if self.custom is not None and not self.custom(value):
            raise PropertyValidatorError(self.name, value)
        return True
