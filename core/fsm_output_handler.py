from typing import Dict, Any

from core.types.output_type import OutputType
from .state import State

class FSMOutputHandler:
    def __init__(self, state_outputs: Dict[State, Any]):
        self.state_outputs = state_outputs

    def get_output(self, state: State) -> Any:
        return self.state_outputs[state]