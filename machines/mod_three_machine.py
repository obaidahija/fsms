from core.output_mapping import OutputMapping
from core.splitter import StringSplitter
from core.transition_table import TransitionTable
from core.state import State
from core.transition_rule import TransitionRule
from core.finite_state_machine import FiniteStateMachine


class ModThreeMachine(FiniteStateMachine):
    def __init__(self):
        s0 = State('S0')
        s1 = State('S1')
        s2 = State('S2')

        transitions = (
                    TransitionTable()
                    .add(s0, '0', s0)
                    .add(s0, '1', s1)
                    .add(s1, '0', s2)
                    .add(s1, '1', s0)
                    .add(s2, '0', s1)
                    .add(s2, '1', s2)
                )

        output_mapping = (
            OutputMapping()
            .add(s0, 0)
            .add(s1, 1)
            .add(s2, 2)
        )

        super().__init__(
            initial_state=s0,
            transitions=transitions,
            output_mapping=output_mapping,
            splitter=StringSplitter()
        )

    def calculate(self, binary_string: str) -> int:
        """
        Processes the binary string and returns the output based on the FSM's current state.
        """
        self.process(binary_string)
        return self.get_output()