import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.splitter import WholeStringSplitter
import pytest
from core.output_mapping import OutputMapping

from core.state import State
from core.finite_state_machine import FiniteStateMachine
from core.transition_table import TransitionTable

class MyFSM(FiniteStateMachine):
    def calculate(self, input_symbol):
        pass

def test_fsm_add_states_and_transitions():
    """FSM can add states and transitions and process input."""

    s0 = State("S0")
    s1 = State("S1")
    transitions = TransitionTable().add(s0, "a", s1)
    output_mapping = OutputMapping().add(s0, 0).add(s1, 1)
    fsm = MyFSM(initial_state=s0, transitions=transitions, output_mapping=output_mapping)
    assert fsm.get_current_state() == s0
    fsm.process("a")
    assert fsm.get_current_state() == s1

def test_fsm_invalid_transition_raises():
    """FSM raises ValueError on invalid transition."""

    s0 = State("S0")
    transitions = TransitionTable()  # no transitions
    output_mapping = OutputMapping()

    fsm = MyFSM(initial_state=s0, transitions=transitions, output_mapping=output_mapping)
    with pytest.raises(ValueError) as excinfo:
        fsm.process("x")
    assert "No transition" in str(excinfo.value)

def test_fsm_reset():
    """FSM can reset to initial state."""

    s0 = State("S0")
    s1 = State("S1")
    transitions = TransitionTable().add(s0, "a", s1)
    output_mapping = OutputMapping().add(s0, 0).add(s1, 1)

    fsm = MyFSM(initial_state=s0, transitions=transitions, output_mapping=output_mapping)
    fsm.process("a")
    assert fsm.get_current_state() == s1
    fsm.reset()
    assert fsm.get_current_state() == s0

def test_fsm_multiple_transitions():
    """FSM handles multiple transitions and states."""

    s0 = State("S0")
    s1 = State("S1")
    s2 = State("S2")
    transitions = (
        TransitionTable()
        .add(s0, "a", s1)
        .add(s1, "b", s2)
        .add(s2, "c", s0)
    )
    output_mapping = OutputMapping().add(s0, 0).add(s1, 1).add(s2, 2)
    fsm = MyFSM(initial_state=s0, transitions=transitions, output_mapping=output_mapping)
    assert fsm.get_current_state() == s0
    fsm.process("a")
    assert fsm.get_current_state() == s1
    fsm.process("ab")
    assert fsm.get_current_state() == s2
    fsm.process("abc")
    assert fsm.get_current_state() == s0

def test_fsm_output_mapping():
    """FSM output mapping returns correct output for each state."""

    s0 = State("S0")
    s1 = State("S1")
    transitions = TransitionTable().add(s0, "a", s1)
    output_mapping = OutputMapping().add(s0, "zero").add(s1, "one")
    fsm = MyFSM(initial_state=s0, transitions=transitions, output_mapping=output_mapping)
    assert fsm.get_output() == "zero"
    fsm.process("a")
    assert fsm.get_output() == "one"

def test_fsm_loop_transition():
    """FSM supports loop transitions and correct output."""

    s0 = State("S0")
    transitions = TransitionTable().add(s0, "loop", s0)
    output_mapping = OutputMapping().add(s0, 42)
    fsm = MyFSM(initial_state=s0, transitions=transitions, output_mapping=output_mapping, splitter= WholeStringSplitter())
    for _ in range(5):
        fsm.process("loop")
        assert fsm.get_current_state() == s0
        assert fsm.get_output() == 42

def test_fsm_empty_input():
    """FSM processes empty input string (should stay in initial state)."""
    s0 = State("S0")
    transitions = TransitionTable()
    output_mapping = OutputMapping().add(s0, 0)
    fsm = MyFSM(initial_state=s0, transitions=transitions, output_mapping=output_mapping)
    fsm.process("")
    assert fsm.get_current_state() == s0
    assert fsm.get_output() == 0

def test_fsm_all_invalid_symbols():
    """FSM raises ValueError for input with only invalid symbols."""
    s0 = State("S0")
    transitions = TransitionTable()
    output_mapping = OutputMapping().add(s0, 0)
    fsm = MyFSM(initial_state=s0, transitions=transitions, output_mapping=output_mapping)
    with pytest.raises(ValueError) as excinfo:
        fsm.process("xyz")
    assert "No transition" in str(excinfo.value)

def test_fsm_output_mapping_missing_state():
    """FSM returns None if output mapping missing for current state."""
    s0 = State("S0")
    s1 = State("S1")
    transitions = TransitionTable().add(s0, "a", s1)
    output_mapping = OutputMapping().add(s0, 0)  # s1 missing
    fsm = MyFSM(initial_state=s0, transitions=transitions, output_mapping=output_mapping)
    fsm.process("a")
    assert fsm.get_output() is None



def test_fsm_output_mapping_callable():
    """FSM supports callable as output mapping value."""
    s0 = State("S0")
    s1 = State("S1")
    transitions = TransitionTable().add(s0, "a", s1)
    output_mapping = OutputMapping().add(s0, lambda: "zero").add(s1, lambda: "one")
    fsm = MyFSM(initial_state=s0, transitions=transitions, output_mapping=output_mapping)
    assert callable(fsm.get_output())
    fsm.process("a")
    assert callable(fsm.get_output())




def test_fsm_validate_reports_errors():
    """FSM validate reports unreachable, missing, and ambiguous transitions."""

    s0 = State("S0")
    s1 = State("S1")
    s2 = State("S2")
    transitions = (
        TransitionTable()
        .add(s0, "a", s1)
        .add(s1, "b", s0)
        .add(s2, "b", s0)
        .add(s1, "b", s0)  # Ambiguous: two transitions for s1, "b"
        # s2 is unreachable from s0
    )
    output_mapping = OutputMapping().add(s0, 0).add(s1, 1).add(s2, 2)
    fsm = MyFSM(initial_state=s0, transitions=transitions, output_mapping=output_mapping)
    errors = fsm.validate()
    assert any("Unreachable state" in e for e in errors)
    assert any("Ambiguous transition" in e for e in errors)
    # s2 has no outgoing transitions, so for all inputs except those defined, missing transitions will be reported
    assert any("Missing transition" in e for e in errors)
