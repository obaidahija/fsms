import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.state import State

def test_state_equality():
    """Test that State objects with the same name are equal, and different names are not equal."""
    s1 = State("A")
    s2 = State("A")
    s3 = State("B")
    assert s1 == s2
    assert s1 != s3

def test_state_str():
    """Test the string representation of a State object."""
    s = State("X")
    assert str(s) == "X"

def test_state_empty_name():
    """Test that a State with an empty name returns an empty string."""
    s = State("")
    assert str(s) == ""

def test_state_long_name():
    """Test that a State with a long name returns the correct string."""
    name = "A" * 1000
    s = State(name)
    assert str(s) == name
