import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from machines.mod_three_machine import ModThreeMachine
# Happy path test cases (from the examples)
@pytest.mark.parametrize("binary_string, expected", [
    ("110", 0),  # 6 % 3 = 0
    ("1010", 1), # 10 % 3 = 1
    ("1101", 1), # 13 % 3 = 1
    ("1110", 2), # 14 % 3 = 2
    ("1111", 0), # 15 % 3 = 0
])
def test_mod_three_basic(binary_string, expected):
    fsm = ModThreeMachine()
    assert fsm.calculate(binary_string) == expected # 0, 1, 2, 0, 1

# Test empty string input (edge case)
def test_mod_three_empty_input():
    fsm = ModThreeMachine()
    assert fsm.calculate("") == 0  # stays at initial state S0

# Test empty string input (edge case)
def test_mod_three_empty_input_state_name():
    fsm = ModThreeMachine()
    fsm.calculate("")
    fsm.get_current_state()
    assert fsm.get_current_state().name == "S0"  # stays at initial state S0

# Test empty input by calling calculate() with no arguments (should raise TypeError)
def test_mod_three_empty_input_state_name_no_arg():
    fsm = ModThreeMachine()
    with pytest.raises(TypeError) as excinfo:
        fsm.calculate()
    assert "calculate() missing 1 required positional" in str(excinfo.value)

# Test empty string input (edge case)
def test_mod_three_input_state_name():
    fsm = ModThreeMachine()
    fsm.calculate("1")
    fsm.get_current_state()
    assert fsm.get_current_state().name == "S1"  # stays at initial state S0

# Test single characters (edge cases)
@pytest.mark.parametrize("binary_string, expected", [
    ("0", 0),  # S0 -> S0
    ("1", 1),  # S0 -> S1
])
def test_mod_three_single_char(binary_string, expected):
    fsm = ModThreeMachine()
    assert fsm.calculate(binary_string) == expected

# Test invalid input (should raise ValueError)
@pytest.mark.parametrize("binary_string", [
    "2",    # Invalid symbol
    "11001a01",  # Contains non-binary
])
def test_mod_three_invalid_input(binary_string):
    fsm = ModThreeMachine()
    with pytest.raises(ValueError) as excinfo:
        fsm.calculate(binary_string)
    assert "No transition" in str(excinfo.value)

# Test long input (edge case)
def test_mod_three_long_input():
    fsm = ModThreeMachine()
    # Just the mod-3 of decimal 2**40
    binary_string = bin(2**40)[2:]
    expected = int(binary_string, 2) % 3
    assert fsm.calculate(binary_string) == expected

def test_mod_three_input_with_whitespace():
    fsm = ModThreeMachine()
    with pytest.raises(ValueError):
        fsm.calculate(" 1010 ")

def test_mod_three_leading_zeros():
    fsm = ModThreeMachine()
    assert fsm.calculate("000110") == 0  # 6 % 3 = 0

def test_mod_three_all_zeros():
    fsm = ModThreeMachine()
    assert fsm.calculate("00000") == 0

def test_mod_three_all_ones():
    fsm = ModThreeMachine()
    assert fsm.calculate("11111") == int("11111", 2) % 3

def test_mod_three_alternating():
    fsm = ModThreeMachine()
    assert fsm.calculate("101010") == int("101010", 2) % 3

def test_mod_three_many_zeros():
    fsm = ModThreeMachine()
    assert fsm.calculate("0" * 1000) == 0

def test_mod_three_many_ones():
    fsm = ModThreeMachine()
    assert fsm.calculate("1" * 1000) == int("1" * 1000, 2) % 3

# Test input with spaces only (edge case)
def test_mod_three_spaces_only():
    fsm = ModThreeMachine()
    with pytest.raises(ValueError) as excinfo:
        fsm.calculate("     ")
    assert "No transition" in str(excinfo.value)

# Test input with mixed valid and invalid characters
def test_mod_three_mixed_valid_invalid():
    fsm = ModThreeMachine()
    with pytest.raises(ValueError) as excinfo:
        fsm.calculate("1010a101")
    assert "No transition" in str(excinfo.value)

# Test very large invalid input
def test_mod_three_large_invalid_input():
    fsm = ModThreeMachine()
    invalid_input = "1" * 1000 + "a"  # Valid binary followed by an invalid character
    with pytest.raises(ValueError) as excinfo:
        fsm.calculate(invalid_input)
    assert "No transition" in str(excinfo.value)

# Test input with special characters
def test_mod_three_special_characters():
    fsm = ModThreeMachine()
    with pytest.raises(ValueError) as excinfo:
        fsm.calculate("1010!@#")
    assert "No transition" in str(excinfo.value)
