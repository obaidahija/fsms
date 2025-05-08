import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.state import State
from core.transition_table import TransitionTable

def test_transition_table_add_and_get():
    """Test that a transition can be added and retrieved for a state."""
    s1 = State("A")
    s2 = State("B")
    transitions = TransitionTable().add(s1, "x", s2)
    assert transitions.get_rules(s1)[0].to_state == s2

def test_transition_table_multiple_adds():
    """Test that multiple transitions can be added and retrieved for different states."""
    s1 = State("A")
    s2 = State("B")
    s3 = State("C")
    transitions = (
        TransitionTable()
        .add(s1, "x", s2)
        .add(s2, "y", s3)
    )
    assert transitions.get_rules(s1)[0].to_state == s2
    assert transitions.get_rules(s2)[0].to_state == s3

def test_transition_table_str():
    """Test the string representation of the TransitionTable includes states and symbols."""
    s1 = State("A")
    s2 = State("B")
    transitions = TransitionTable().add(s1, "x", s2).add(s2, "y", s1)
    s = str(transitions)
    assert "A" in s and "B" in s and "x" in s

def test_transition_table_self_loop():
    """Test that a state can have a transition to itself (self-loop)."""
    s = State("A")
    transitions = TransitionTable().add(s, "x", s)
    assert transitions.get_rules(s)[0].to_state == s

def test_transition_table_empty_symbol():
    """Test that a transition can be added with an empty string as the symbol."""
    s1 = State("A")
    s2 = State("B")
    transitions = TransitionTable().add(s1, "", s2)
    assert transitions.get_rules(s1)[0].input_matcher == ""

def test_transition_table_special_symbol():
    """Test that a transition can be added with a special symbol as the input."""
    s1 = State("A")
    s2 = State("B")
    transitions = TransitionTable().add(s1, "@", s2)
    assert transitions.get_rules(s1)[0].input_matcher == "@"

def test_transition_table_no_rules_for_state():
    """Test that querying for rules for a state with no transitions returns an empty list."""
    s1 = State("A")
    s2 = State("B")
    transitions = TransitionTable().add(s1, "x", s2)
    assert transitions.get_rules(State("C")) == []
