from datetime import datetime
from ..exceptions.config import HeaderException

class Header:
    Scheme_Name: str
    Scheme_Description: str
    Scheme_Author: str
    Scheme_Owner: str
    Creation_Date: str

    def __init__(self, name: str, description: str, author: str, owner: str, creation_date: str):
        self.Scheme_Name = name
        self.Scheme_Description = description
        self.Scheme_Author = author
        self.Scheme_Owner = owner
        self.Creation_Date = creation_date

    @staticmethod
    def new(name: str) -> "Header":
        """
        Creates a new config header, with default attributes

        Args:
            name (str): The name of the feedscheme

        Returns:
            ConfigHeader: The new header
        """
        description = "Enter a description for your feed scheme"
        author = "Enter the author of your feed scheme"
        owner = "Enter the owner for your feed scheme"
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return Header(name, description, author, owner, creation_date)

    @staticmethod
    def load(data: dict) -> "Header":
        if "Scheme_Name" not in data:
            raise HeaderException("No Scheme_Name defined")
        if "Scheme_Description" not in data:
            raise HeaderException("No Scheme_Description defined")
        if "Scheme_Author" not in data:
            raise HeaderException("No Scheme_Author defined")
        if "Scheme_Owner" not in data:
            raise HeaderException("No Scheme_Owner defined")
        if "Creation_Date" not in data:
            raise HeaderException("No Creation_Data defined")
        return Header(
            data["Scheme_Name"],
            data["Scheme_Description"],
            data["Scheme_Author"],
            data["Scheme_Owner"],
            data["Creation_Date"]
        )

    def dump(self) -> dict:
        return {
            "Scheme_Name": self.Scheme_Name,
            "Scheme_Description": self.Scheme_Description,
            "Scheme_Author": self.Scheme_Author,
            "Scheme_Owner": self.Scheme_Owner,
            "Creation_Date": self.Creation_Date
        }