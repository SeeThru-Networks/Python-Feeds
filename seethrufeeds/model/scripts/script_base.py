from seethrufeeds.feeds import FeedResult
from seethrufeeds.model.attribution import Attribution

from seethrufeeds.model.scripts.script_state import StatesEnum, State


class ScriptBase(Attribution):
    state: StatesEnum

    def run(self):
        """
        Override this to implement logic for running of the script
        """
        raise NotImplementedError("run method not implemented for script")

    def get_result(self) -> FeedResult:
        """
        Evaluates the script result using the state system, for custom logic, override this

        Returns:
            FeedResult: The result
        """
        if not isinstance(self.state, StatesEnum):
            raise TypeError("state not of type StatesEnum")

        if not isinstance(self.state.value, State):
            raise TypeError("chosen script state not of type State")

        # TODO: Optional override

        # Constructs a new result
        return FeedResult(status=self.state.value.status, message=self.state.value.message)
