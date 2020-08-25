import SeeThru_Feeds.Model.Properties.Properties
from SeeThru_Feeds.Model.Properties.Properties import PropertyBase


class PropertyManager:
    def __init__(self):
        self.Properties = None
        self.initialise()

    def initialise(self):
        """
        Ensures that the Properties attribute is set
        """
        # Initialises the properties dictionary for the manager
        # This stores new instances of every property defined
        if self.Properties is None or type(self.Properties) is not dict:
            self.Properties = {}
            # --Fills the properties dict with the the subclass' properties
            # Loops through every variable in the class, getting the
            # variable name and it's associated value
            for attr in self.__dir__():
                prop = getattr(self, attr)
                # If the attribute is a property, then it is added to the properties dict
                if isinstance(prop, SeeThru_Feeds.Model.Properties.Properties.PropertyBase):
                    # Uses either a name defined in the property or the variable's name
                    name = prop.name if prop.name is not None else attr

                    # Creates a new instance of the property
                    # This is used to store the property value
                    instanceProp = prop.new_instance(prop)
                    instanceProp._value = instanceProp.default  # Assigns the default value, ! This bypasses validation
                    # Stores the instance property in the Properties dictionary
                    self.Properties[name] = instanceProp

                    # Sets the properties internal name to the name obtained
                    instanceProp.name = name

                    # Makes the property instance available 
                    # by both the variable name and internal name
                    self.__setattr__(attr, instanceProp)
                    self.__setattr__(name, instanceProp)

    def set_property(self, prop, value):
        """
        Sets a value to the given property
        Note: The value isn't stored in the property instance

        Arguments:
            prop (PropertyBase): The value to associate with the property
            value (any): The value to give the property

        Raises:
            TypeError: Prop argument must be either of type Property or string
            TypeError: Modifier argument must be a function pointer

        Returns:
            PropertyManager: The property manager
        """
        self.initialise()
        # Data validation
        if not isinstance(prop, SeeThru_Feeds.Model.Properties.Properties.PropertyBase) and type(prop) != str:
            raise TypeError("Prop argument must be either of type Property or string")
        # Gets the index name of the property
        # it is either the value passed in as a string or the prop's internal name
        indexName = prop if type(prop) == str else prop.name
        # Assigns the new value to the property
        self.Properties[indexName].value = value
        return self

    def get_property(self, prop):
        """
        Gets the value associated with a property in the manager

        Arguments:
            prop (PropertyBase, str): The property reference (e.g. HTTPGet.URL) or the property name

        Raises:
            TypeError: Prop argument must be either of type Property or string

        Returns:
            any: The value
        """
        self.initialise()
        # Data validation
        if not isinstance(prop, SeeThru_Feeds.Model.Properties.Properties.PropertyBase) and type(prop) != str:
            raise TypeError(
                "Prop argument must be either of type Property or string")
        # Gets the index name of the property
        # it is either the value passed in as a string or the prop's internal name
        indexName = prop if type(prop) == str else prop.name
        # Returns the value of the property
        return self.Properties[indexName].value

    def modify_property(self, prop, modifier):
        """
        Modifies the value of a given property

        Arguments:
            prop (PropertyBase, str): The property reference (e.g. HTTPGet.URL) or the property name
            modifier (lambda): A function which takes the value as an argument and modifies it in some way

        Raises:
            TypeError: Prop argument must be either of type Property or string
            TypeError: Modifier argument must be a function pointer

        Returns:
            PropertyManager: The property manager
        """
        self.initialise()
        # Data validation
        if not isinstance(prop, SeeThru_Feeds.Model.Properties.Properties.PropertyBase) and type(prop) != str:
            raise TypeError(
                "Prop argument must be either of type Property or string")
        if not callable(modifier):
            raise TypeError("modifier argument must be a function pointer")
        # Gets the index name of the property
        # it is either the value passed in as a string or the prop's internal name
        indexName = prop if type(prop) == str else prop.name
        # Assigns the new value to the property
        self.Properties[indexName].value = modifier(
            self.Properties[indexName].value)
        return self

    @property
    def FillableProperties(self):
        """Returns a list of the fillable properties for the manager

        Returns:
            list: A list of fillable result properties
        """
        self.initialise()
        # Loops through all of the properties and returns the names of the fillable
        fillable = [prop for prop in self.Properties.values() if isinstance(prop, SeeThru_Feeds.Model.Properties.Properties.FillableProperty)]
        return fillable

    @property
    def ResultProperties(self):
        """Returns a list of the result properties for the manager

        Returns:
            list: A list of result property instances
        """
        self.initialise()
        # Loops through all of the properties and returns the names of the result properties
        results = [prop for prop in self.Properties.values() if isinstance(prop, SeeThru_Feeds.Model.Properties.Properties.ResultProperty)]
        return results

    def check_fillables(self):
        """
        Parses all of the fillable properties to make sure that they are valid

        Raises:
            Exception: Did not pass a property pass

        Returns:
            bool: Whether the fillables are valid, effectively it is always true as exceptions are made
        """
        self.initialise()
        # Parses all of the fillable properties of the manager to make sure that they are met
        for prop in self.FillableProperties:
            if not prop.parse_value(prop.value):
                raise Exception("[Property: {}] Did not pass a property parse".format(prop.name))
        return True
