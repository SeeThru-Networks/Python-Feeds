class Attribution:
    # region Title
    # The Script_Title attribute should be set in your implementation
    Attr_Title = None

    @classmethod
    def get_title(cls):
        """
        Returns a set title

        Raises:
            NotImplementedError: There is no title defined, please define it as 'Attr_Title='

        Returns:
            str: The title
        """
        if cls.Attr_Title is None:
            raise NotImplementedError("There is no title defined, please define it as 'Attr_Title='")
        return cls.Attr_Title
    # endregion

    # region Description
    # The Attr_Description attribute should be set in your implementation
    Attr_Description = None

    @classmethod
    def get_description(cls):
        """
        Returns a description

        Raises:
            NotImplementedError: There is no description defined, please define it as 'Attr_Description='

        Returns:
            str: The description
        """
        if cls.Attr_Description is None:
            raise NotImplementedError("There is no description defined, please define it as 'Attr_Description='")
        return cls.Attr_Description
    # endregion

    # region Author
    # The Attr_Author attribute should be set in your implementation
    Attr_Author = None

    @classmethod
    def get_author(cls):
        """
        Returns the author

        Raises:
            NotImplementedError: There is no author defined, please define it as 'Attr_Author='

        Returns:
            str: The author
        """
        if cls.Attr_Author is None:
            raise NotImplementedError("There is no author defined, please define it as 'Attr_Author='")
        return cls.Attr_Author
    # endregion

    # region Owner
    # The Attr_Owner attribute should be set in your implementation
    Attr_Owner = None

    @classmethod
    def get_owner(cls):
        """
        Returns a owner

        Raises:
            NotImplementedError: There is no owner defined, please define it as 'Attr_Owner='

        Returns:
            str: The owner
        """
        if cls.Attr_Owner is None:
            raise NotImplementedError("There is no owner defined, please define it as 'Attr_Owner='")
        return cls.Attr_Owner
    # endregion

    # region Support_Link
    # The Attr_SupportLink attribute should be set in your implementation
    Attr_SupportLink = None

    @classmethod
    def get_support_link(cls):
        """
        Returns a support link

        Raises:
            NotImplementedError: There is no supportLink defined, please define it as 'Attr_SupportLink='

        Returns:
            str: The support link
        """
        if cls.Attr_SupportLink is None:
            raise NotImplementedError("There is no supportLink defined, please define it as 'Attr_SupportLink='")
        return cls.Attr_SupportLink
    # endregion

    # region Docs_Link
    # The Attr_DocLink attribute should be set in your implementation
    Attr_DocLink = None

    @classmethod
    def get_docs_link(cls):
        """
        Returns a doc link

        Raises:
            NotImplementedError: There is no DocLink defined, please define it as 'Attr_DocLink='

        Returns:
            str: The doc link
        """
        if cls.Attr_DocLink is None:
            raise NotImplementedError("There is no DocLink defined, please define it as 'Attr_DocLink='")
        return cls.Attr_DocLink
    # endregion

    # region LicenseLink
    # The Attr_LicenseLink attribute should be set in your implementation
    Attr_LicenseLink = None

    @classmethod
    def get_license_link(cls):
        """
        Returns a license link

        Raises:
            NotImplementedError: There is no LicenseLink defined, please define it as 'Attr_LicenseLink='

        Returns:
            str: The license link
        """
        if cls.Attr_LicenseLink is None:
            raise NotImplementedError("There is no LicenseLink defined, please define it as 'Attr_LicenseLink='")
        return cls.Attr_LicenseLink
    # endregion
