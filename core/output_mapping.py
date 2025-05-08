from typing import Dict, Any
from core.state import State
from core.types.output_type import OutputType

class OutputMapping:
    def __init__(self):
        """
        Initializes an empty mapping of states to outputs.
        """
        self._mapping: Dict[State, OutputType] = {}

    def add(self, state: State, output: OutputType):
        """
        Adds a state and its corresponding output to the mapping.
        If the state already exists, it updates the output.
        """
        if not isinstance(state, State):
            raise TypeError("Expected state to be of type 'State'")
        self._mapping[state] = output
        return self

    def get(self, state: State) -> OutputType:
        """
        Retrieves the output for a given state. If the state is not found, returns None.
        """
        if not isinstance(state, State):
            raise TypeError("Expected state to be of type 'State'")
        return self._mapping.get(state)

    def __str__(self):
        """
        Returns a string representation of the output mapping.
        """
        return ", ".join(f"{str(state)}: {repr(output)}" for state, output in self._mapping.items())