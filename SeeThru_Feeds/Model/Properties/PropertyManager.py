from SeeThru_Feeds.Model.Properties.Properties import *


class PropertyManager:
    def Initialise(self):
        """
        Ensures that the properties attribute is set
        """
        # Initialises the properties dictionary for the manager
        if "Properties" not in dir(self) or type(self.Properties) != dict:
            self.Properties = {}
            # --Fills the properties dict with the the subclass' properties
            # Loops through every variable in the class, getting the
            # variable name and it's associated value
            for attr in self.__dir__():
                prop = getattr(self, attr)
                # If the attribute is a property, then it is added to the properties dict
                if isinstance(prop, PropertyBase):
                    # Uses either a name defined in the property or the variable's name
                    name = prop.name if prop.name != None else attr
                    self.Properties[name] = {
                        "definition": prop,
                        "fillable": isinstance(prop, FillableProperty),
                        "result": isinstance(prop, ResultProperty),
                        "value": prop.default
                    }
                    # Sets the properties internal name to the name obtained
                    # This sets the name for the property across all instances
                    # of the component, as the property is a static variable
                    prop.name = name

    def SetProperty(self, prop, value):
        """
        Sets a value to the given property
        Note: The value isn't stored in the property instance

        Arguments:
            prop {Property or String} -- The property reference (e.g. HTTPGet.URL) or the property name
            value {Any} -- The value to associate with the property

        Raises:
            TypeError: Prop argument must be either of type Property or string
            TypeError: Modifier argument must be a function pointer

        Returns:
            PropertyManager -- The property manager
        """
        self.Initialise()
        # Data validation
        if not isinstance(prop, PropertyBase) and type(prop) != str:
            raise TypeError(
                "Prop argument must be either of type Property or string")
        # Gets the indexable name of the property
        # it is either the value passed in as a string or the prop's internal name
        indexName = prop if type(prop) == str else prop.name
        # Assigns the new value to the property
        self.Properties[indexName]["value"] = value
        return self

    def GetProperty(self, prop):
        """
        Gets the value associated with a property in the manager

        Arguments:
            prop {Property or String} -- The property reference (e.g. HTTPGet.URL) or the property name

        Raises:
            TypeError: Prop argument must be either of type Property or string

        Returns:
            Any -- The value
        """
        self.Initialise()
        # Data validation
        if not isinstance(prop, PropertyBase) and type(prop) != str:
            raise TypeError(
                "Prop argument must be either of type Property or string")
        # Gets the indexable name of the property
        # it is either the value passed in as a string or the prop's internal name
        indexName = prop if type(prop) == str else prop.name
        # Assigns the new value to the property
        return self.Properties[indexName]["value"]

    def modifyProperty(self, prop, modifier):
        """
        Modifies the value of a given property

        Arguments:
            prop {Property or String} -- The property reference (e.g. HTTPGet.URL) or the property name
            modifier {function pointer} -- A function which takes the value as an argument and modifies it in some way

        Raises:
            TypeError: Prop argument must be either of type Property or string
            TypeError: Modifier argument must be a function pointer

        Returns:
            PropertyManager -- The property manager
        """
        self.Initialise()
        # Data validation
        if not isinstance(prop, PropertyBase) and type(prop) != str:
            raise TypeError(
                "Prop argument must be either of type Property or string")
        if not callable(modifier):
            raise TypeError("modifier argument must be a function pointer")
        # Gets the indexable name of the property
        # it is either the value passed in as a string or the prop's internal name
        indexName = prop if type(prop) == str else prop.name
        # Assigns the new value to the property
        self.Properties[indexName]["value"] = modifier(
            self.Properties[indexName]["value"])
        return self

    @property
    def FillableProperties(self):
        """Returns a list of the fillable properties for the manager

        Returns:
            list -- A list of names of the fillable properties in the manager
        """
        self.Initialise()
        # Loops through all of the properties and returns the names of the fillable
        fillable = [
            prop["definition"].name for prop in self.Properties.values() if prop["fillable"]]
        return fillable

    @property
    def ResultProperties(self):
        """Returns a list of the result properties for the manager

        Returns:
            list -- A list of names of the result properties in the manager
        """
        self.Initialise()
        # Loops through all of the properties and returns the names of the result properties
        results = [
            prop["definition"].name for prop in self.Properties.values() if prop["result"]]
        return results

    def CheckFillables(self):
        """
        Parses all of the fillable properties to make sure that they are valid

        Raises:
            Exception: Did not pass a property pass

        Returns:
            boolean -- Whether the fillables are valid, effictively it is always true as excptions are made
        """
        self.Initialise()
        # Parses all of the fillable properties of the manager to make sure that they are met
        for prop in self.Properties.values():
            if prop["fillable"] and not prop["definition"].ParseValue(prop["value"]):
                raise Exception("[Property: {}] Did not pass a property parse".format(
                    prop["definition"].name))
        return True
