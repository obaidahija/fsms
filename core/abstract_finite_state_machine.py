from abc import ABC, abstractmethod
from typing import List, Any
from core.output_mapping import OutputMapping
from core.types.output_type import OutputType
from .state import State


class AbstractFiniteStateMachine(ABC):
    def __init__(self, output_mapping: OutputMapping):
        self.output_mapping = output_mapping

    @abstractmethod
    def reset(self) -> None:
        """Resets the FSM to its initial state."""
        pass

    @abstractmethod
    def process(self, inputs: List[str]) -> bool:
        """Processes a list of input symbols and determines if the FSM ends in an accept state."""
        pass

    @abstractmethod
    def get_current_state(self) -> State:
        """Returns the current state of the FSM."""
        pass

    @abstractmethod
    def calculate(self, inputs: Any) -> Any:
        """
        Processes the inputs and returns a result based on the FSM's logic.
        The return type can vary depending on the FSM's implementation.
        """
        pass

    
    def get_output(self) -> OutputType: 
        """Returns the output associated with the current state."""
        if self.output_mapping is None:
            raise NotImplementedError("Output mapping is not defined for this FSM.")
        output = self.output_mapping.get(self.current_state)
        if isinstance(output, type) and issubclass(output, Exception):
            raise output("FSM ended in TRAP state!")
        return output