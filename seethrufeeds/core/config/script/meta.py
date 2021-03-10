import seethrufeeds.core.exceptions.config as ConfigExceptions


class Meta:
    Script_Name: str
    Script_Output_Path: str
    Script_Object_Path: str

    def __init__(self, name: str, output_path: str, object_path: str):
        self.Script_Name = name
        self.Script_Output_Path = output_path
        self.Script_Object_Path = object_path

    @staticmethod
    def new(name: str) -> "Meta":
        """
        Creates a new script meta, with attributes derived from the name

        Args:
            name (str): The name of the script

        Returns:
            ScriptMeta: The new script meta
        """
        output_path = f"Outputs/{name}"
        object_path = f"Scripts.{name}@{name}"
        return Meta(name, output_path, object_path)

    @staticmethod
    def load(data: dict, script_name: str) -> "Meta":
        """
        Parses the given data into a script meta

        Args:
            data: The data to parse
            script_name: The name of the script ot which this belongs

        Returns:
            Meta: The new script meta
        """
        if "Script_Name" not in data:
            raise ConfigExceptions.ScriptMetaException("A script meta has no name", script_name)
        if "Script_Output_Path" not in data:
            raise ConfigExceptions.ScriptMetaException("A script meta has no output path", script_name)
        if "Script_Object_Path" not in data:
            raise ConfigExceptions.ScriptMetaException("A script meta has no script module", script_name)
        return Meta(
            data["Script_Name"],
            data["Script_Output_Path"],
            data["Script_Object_Path"]
        )

    def dump(self) -> dict:
        """
        Dumps the meta into a dictionary

        Returns:
            dict: The dumped data
        """
        return {
            "Script_Name": self.Script_Name,
            "Script_Output_Path": self.Script_Output_Path,
            "Script_Object_Path": self.Script_Object_Path
        }
