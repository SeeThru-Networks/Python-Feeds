from SeeThru_Feeds.Model.Properties.Properties import *
from SeeThru_Feeds.Model.Properties.PropertyManager import PropertyManager

class ComponentBase(PropertyManager):
    def Component_Execute(self): 
        """
        This function should be overridden by a subclass
        This is where your component should start executing

        Raises:
            NotImplementedError: There is no execution method defined, please define it with 'Component_Execute'
        """
        raise NotImplementedError("There is no execution method defined, please define it with 'Component_Execute'")

    def Run(self): 
        """
        This method will call the sub class' Component_Execute method
        This is the only way a component should be executed as it 
        ensures that the properties of the component are valid

        Returns:
            Component -- The component
        """
        self.CheckFillables()
        # The fillable properties passed their parsing, therefore the component can be executed
        self.Component_Execute()
        return self

    # The Component_Title attribute should be set in your component
    Component_Title = None
    @classmethod
    def GetTitle(cls):
        """
        Returns a titile of the component

        Raises:
            NotImplementedError: There is no title defined, please define it as 'Component_Title='

        Returns:
            string -- The component's title
        """
        if cls.Component_Title == None: raise NotImplementedError("There is no name defined, please define it as 'Component_Title='")
        return cls.Component_Title
    # The Component_Description attribute should be set in your component
    Component_Description = None
    @classmethod
    def GetDescription(cls):
        """
        Returns a description of the component

        Raises:
            NotImplementedError: There is no description defined, please define it as 'Component_Description='

        Returns:
            string -- The component's description
        """
        if cls.Component_Description == None: raise NotImplementedError("There is no description defined, please define it as 'Component_Description='")
        return cls.Component_Description
    # The Component_Author attribute should be set in your component
    Component_Author = None
    @classmethod
    def GetAuthor(cls):
        """
        Returns the author of the component

        Raises:
            NotImplementedError: There is no author defined, please define it as 'Component_Author='

        Returns:
            string -- The component's author
        """
        if cls.Component_Author == None: raise NotImplementedError("There is no author defined, please define it as 'Component_Author='")
        return cls.Component_Author
    # The Component_Owner attribute should be set in your component
    Component_Owner = None
    @classmethod
    def GetOwner(cls):
        """
        Returns a owner of the component

        Raises:
            NotImplementedError: There is no owner defined, please define it as 'Component_Owner='

        Returns:
            string -- The component's owner
        """
        if cls.Component_Owner == None: raise NotImplementedError("There is no owner defined, please define it as 'Component_Owner='")
        return cls.Component_Owner
    # The Component_SupportLink attribute should be set in your component
    Component_SupportLink = None
    @classmethod
    def GetSupportLink(cls):
        """
        Returns a support link of the component

        Raises:
            NotImplementedError: There is no supportLink defined, please define it as 'Component_SupportLink='

        Returns:
            string -- The component's support link
        """
        if cls.Component_SupportLink == None: raise NotImplementedError("There is no supportLink defined, please define it as 'Component_SupportLink='")
        return cls.Component_SupportLink
    # The Component_DocLink attribute should be set in your component
    Component_DocLink = None
    @classmethod
    def GetDocLink(cls):
        """
        Returns a doc link of the component

        Raises:
            NotImplementedError: There is no DocLink defined, please define it as 'Component_DocLink='

        Returns:
            string -- The component's doc link
        """
        if cls.Component_DocLink == None: raise NotImplementedError("There is no DocLink defined, please define it as 'Component_DocLink='")
        return cls.Component_DocLink
    # The Component_LicenseLink attribute should be set in your component
    Component_LicenseLink = None
    @classmethod
    def GetLicenseLink(cls):
        """
        Returns a license link of the component

        Raises:
            NotImplementedError: There is no LicenseLink defined, please define it as 'Component_LicenseLink='

        Returns:
            string -- The component's license link
        """
        if cls.Component_LicenseLink == None: raise NotImplementedError("There is no LicenseLink defined, please define it as 'Component_LicenseLink='")
        return cls.Component_LicenseLink
