from core.transition_table import TransitionTable
from core.state import State
from core.finite_state_machine import FiniteStateMachine


class TrapStateMachine(FiniteStateMachine):
    def __init__(self):
        s0 = State('S0')
        s1 = State('S1')
        trap = State('TRAP')

        transitions = (
            TransitionTable()
            .add(s0, '0', s1)
            .add(s0, '1', s0)
            .add(s1, '0', trap)
            .add(s1, '1', s0)
            .add(trap, '0', trap)
            .add(trap, '1', trap)
        )

        output_mapping = {
            s0: 0,
            s1: 1,
            trap: Exception  # Assign the exception type directly
        }

        super().__init__(
            initial_state=s0,
            transitions=transitions,
            output_mapping=output_mapping
        )


    def calculate(self, binary_string: str) -> int:
        """
        Processes the binary string. Raises TrapStateException if ending in TRAP state.
        """
        self.process(binary_string)
        return self.get_output()