import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from core.state import State
from core.output_mapping import OutputMapping

def test_output_mapper_add_and_get():
    """Test that OutputMapping.add and get work for a single state-output pair."""
    s1 = State("A")
    mapper = OutputMapping().add(s1, "output1")
    assert mapper.get(s1) == "output1"

def test_output_mapper_overwrite():
    """Test that adding the same state twice overwrites the output."""
    s1 = State("A")
    mapper = OutputMapping().add(s1, "output1").add(s1, "output2")
    assert mapper.get(s1) == "output2"

def test_output_mapper_multiple_states():
    """Test that OutputMapping can handle multiple states with different outputs."""
    s1 = State("A")
    s2 = State("B")
    mapper = OutputMapping().add(s1, "out1").add(s2, "out2")
    assert mapper.get(s1) == "out1"
    assert mapper.get(s2) == "out2"

def test_output_mapper_missing_state():
    """Test that OutputMapping.get returns None for a missing state."""
    s1 = State("A")
    mapper = OutputMapping()
    assert mapper.get(s1) is None

def test_output_mapper_non_state_key():
    """Test that OutputMapping.add raises TypeError if key is not a State."""
    mapper = OutputMapping()
    with pytest.raises(TypeError) as excinfo:
        mapper.add("not_a_state", "output")
    assert "to be of type 'State'" in str(excinfo.value)

def test_output_mapper_none_output():
    """Test that OutputMapping can store None as an output."""
    s1 = State("A")
    mapper = OutputMapping().add(s1, None)
    assert mapper.get(s1) is None

def test_output_mapper_str():
    """Test the string representation of OutputMapping includes states and outputs."""
    s1 = State("A")
    s2 = State("B")
    mapper = OutputMapping().add(s1, "out1").add(s2, "out2")
    s = str(mapper)
    assert "A" in s and "out1" in s and "B" in s and "out2" in s

def test_output_mapper_get_non_state():
    """Test that OutputMapping.get raises TypeError if key is not a State."""
    mapper = OutputMapping()
    with pytest.raises(TypeError) as excinfo:
        mapper.get("1") is None
    assert "to be of type 'State'" in str(excinfo.value)