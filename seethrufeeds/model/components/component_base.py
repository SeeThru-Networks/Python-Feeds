from seethrufeeds.model.attribution import Attribution
from seethrufeeds.model.Properties.properties import *
from seethrufeeds.model.Properties.property_manager import PropertyManager


class ComponentBase(PropertyManager, Attribution):
    def component_execute(self):
        """
        This function should be overridden by a subclass
        This is where your component should start executing

        Raises:
            NotImplementedError: There is no execution method defined, please define it with 'component_execute'
        """
        raise NotImplementedError("There is no execution method defined, please define it with 'component_execute'")

    def run(self):
        """
        This method will call the sub class' component_execute method
        This is the only way a component should be executed as it 
        ensures that the properties of the component are valid

        Returns:
            ComponentBase: The component
        """
        self.check_fillables()
        # The fillable properties passed their parsing, therefore the component can be executed
        self.component_execute()
        return self
