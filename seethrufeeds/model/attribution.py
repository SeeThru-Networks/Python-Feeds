class Attribution:
    # region Title
    # The Script_Title attribute should be set in your implementation
    attribute_title = None

    @classmethod
    def get_title(cls):
        """
        Returns a set title

        Raises:
            NotImplementedError: There is no title defined, please define it as 'attribute_title='

        Returns:
            str: The title
        """
        if cls.attribute_title is None:
            raise NotImplementedError("There is no title defined, please define it as 'attribute_title='")
        return cls.attribute_title
    # endregion

    # region Description
    # The attribute_description attribute should be set in your implementation
    attribute_description = None

    @classmethod
    def get_description(cls):
        """
        Returns a description

        Raises:
            NotImplementedError: There is no description defined, please define it as 'attribute_description='

        Returns:
            str: The description
        """
        if cls.attribute_description is None:
            raise NotImplementedError("There is no description defined, please define it as 'attribute_description='")
        return cls.attribute_description
    # endregion

    # region Author
    # The attribute_author attribute should be set in your implementation
    attribute_author = None

    @classmethod
    def get_author(cls):
        """
        Returns the author

        Raises:
            NotImplementedError: There is no author defined, please define it as 'attribute_author='

        Returns:
            str: The author
        """
        if cls.attribute_author is None:
            raise NotImplementedError("There is no author defined, please define it as 'attribute_author='")
        return cls.attribute_author
    # endregion

    # region Owner
    # The attribute_owner attribute should be set in your implementation
    attribute_owner = None

    @classmethod
    def get_owner(cls):
        """
        Returns a owner

        Raises:
            NotImplementedError: There is no owner defined, please define it as 'attribute_owner='

        Returns:
            str: The owner
        """
        if cls.attribute_owner is None:
            raise NotImplementedError("There is no owner defined, please define it as 'attribute_owner='")
        return cls.attribute_owner
    # endregion

    # region Support_Link
    # The attribute_supportLink attribute should be set in your implementation
    attribute_supportLink = None

    @classmethod
    def get_support_link(cls):
        """
        Returns a support link

        Raises:
            NotImplementedError: There is no supportLink defined, please define it as 'attribute_supportLink='

        Returns:
            str: The support link
        """
        if cls.attribute_supportLink is None:
            raise NotImplementedError("There is no supportLink defined, please define it as 'attribute_supportLink='")
        return cls.attribute_supportLink
    # endregion

    # region Docs_Link
    # The attribute_docs_link attribute should be set in your implementation
    attribute_docs_link = None

    @classmethod
    def get_docs_link(cls):
        """
        Returns a doc link

        Raises:
            NotImplementedError: There is no DocLink defined, please define it as 'attribute_docs_link='

        Returns:
            str: The doc link
        """
        if cls.attribute_docs_link is None:
            raise NotImplementedError("There is no DocLink defined, please define it as 'attribute_docs_link='")
        return cls.attribute_docs_link
    # endregion

    # region LicenseLink
    # The attribute_license_link attribute should be set in your implementation
    attribute_license_link = None

    @classmethod
    def get_license_link(cls):
        """
        Returns a license link

        Raises:
            NotImplementedError: There is no LicenseLink defined, please define it as 'attribute_license_link='

        Returns:
            str: The license link
        """
        if cls.attribute_license_link is None:
            raise NotImplementedError("There is no LicenseLink defined, please define it as 'attribute_license_link='")
        return cls.attribute_license_link
    # endregion
