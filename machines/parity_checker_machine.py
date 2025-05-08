from core.transition_table import TransitionTable
from core.state import State
from core.finite_state_machine import FiniteStateMachine

class ParityCheckerMachine(FiniteStateMachine):
    """
    FSM that checks the parity (even or odd number of 1s) in a binary string.
    Output: 0 for even parity, 1 for odd parity.
    """
    def __init__(self):
        even = State('EVEN')
        odd = State('ODD')

        transitions = (
            TransitionTable()
            .add(even, '0', even)
            .add(even, '1', odd)
            .add(odd, '0', odd)
            .add(odd, '1', even)
        )

        output_mapping = {
            even: False,  # Even number of 1s
            odd: True    # Odd number of 1s
        }

        super().__init__(
            initial_state=even,
            transitions=transitions,
            output_mapping=output_mapping
        )

    def calculate(self, binary_string: str) -> int:
        """
        Returns 0 if the number of 1s is even, 1 if odd.
        """
        self.process(binary_string)
        return self.get_output()