import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import re
import pytest
from core.state import State
from core.transition_rule import TransitionRule

def test_match_str():
    """Test that TransitionRule matches string input correctly."""
    rule = TransitionRule(State("A"), "x", State("B"))
    assert rule.matches("x")
    assert not rule.matches("y")

def test_match_int():
    """Test that TransitionRule matches integer input correctly."""
    rule = TransitionRule(State("A"), 1, State("B"))
    assert rule.matches(1)
    assert not rule.matches(2)

def test_match_bool():
    """Test that TransitionRule matches boolean input correctly."""
    rule = TransitionRule(State("A"), True, State("B"))
    assert rule.matches(True)
    assert not rule.matches(False)

def test_match_regex():
    """Test that TransitionRule matches input using a regex pattern."""
    pattern = re.compile(r"\d+")
    rule = TransitionRule(State("A"), pattern, State("B"))
    assert rule.matches("123")
    assert not rule.matches("abc")

def test_match_list():
    """Test that TransitionRule matches input from a list of matchers."""
    rule = TransitionRule(State("A"), ["x", "y", 1], State("B"))
    assert rule.matches("x")
    assert rule.matches("y")
    assert rule.matches(1)
    assert not rule.matches("z")

def test_match_none_raises():
    """Test that TransitionRule does not match None input."""
    rule = TransitionRule(State("A"), "x", State("B"))
    assert not rule.matches(None)

def test_invalid_matcher_type_raises():
    """Test that TransitionRule raises TypeError for unsupported matcher types."""
    with pytest.raises(TypeError) as excinfo:
        TransitionRule(State("A"), object(), State("B"))
    assert "Unsupported input matcher type" in str(excinfo.value)

def test_matcher_list_with_invalid_type():
    """Test that TransitionRule raises TypeError for invalid matcher in list."""
    with pytest.raises(TypeError) as excinfo:
        TransitionRule(State("A"), ["x", None], State("B"))
    assert "Unsupported input matcher type" in str(excinfo.value)

def test_match_empty_string():
    """Test that TransitionRule matches empty string input."""
    rule = TransitionRule(State("A"), "", State("B"))
    assert rule.matches("")
    assert not rule.matches("x")

def test_match_empty_list():
    """Test that TransitionRule with an empty matcher list matches nothing."""
    rule = TransitionRule(State("A"), [], State("B"))
    assert not rule.matches("anything")

def test_match_regex_matches_nothing():
    """Test that TransitionRule with a regex that matches nothing behaves correctly."""
    pattern = re.compile(r"^$")
    rule = TransitionRule(State("A"), pattern, State("B"))
    assert rule.matches("")
    assert not rule.matches("x")

def test_match_bool_false():
    """Test that TransitionRule matches boolean False input correctly."""
    rule = TransitionRule(State("A"), False, State("B"))
    assert rule.matches(False)
    assert not rule.matches(True)

def test_match_list_mixed_types():
    """Test that TransitionRule matches input from a list of mixed types."""
    rule = TransitionRule(State("A"), ["x", 1, True], State("B"))
    assert rule.matches("x")
    assert rule.matches(1)
    assert rule.matches(True)
    assert not rule.matches("y")

def test_match_regex_special_chars():
    """Test that TransitionRule matches input with regex for special characters."""
    pattern = re.compile(r"\W+")
    rule = TransitionRule(State("A"), pattern, State("B"))
    assert rule.matches("!!!")
    assert not rule.matches("abc")
