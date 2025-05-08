from typing import Dict, List, Union
from .state import State
from .transition_rule import TransitionRule
from .types.input_type import InputMatcher

class TransitionTable:
    def __init__(self):
        """
        Initializes an empty transition table.
        The table is a dictionary where the keys are states and the values are lists of TransitionRule objects.
        """
        self._table: Dict[State, List[TransitionRule]] = {}

    def add(self, from_state: State, input_matcher: InputMatcher , to_state: State):
        """
        Adds a transition rule to the table.
        If the input_matcher is a list, it adds multiple rules for each symbol in the list.
        """
        if not isinstance(from_state, State):
            raise TypeError("Expected from_state to be of type 'State'")
        if not isinstance(to_state, State):
            raise TypeError("Expected to_state to be of type 'State'")
        if isinstance(input_matcher, list):
            for symbol in input_matcher:
                self._add_rule(from_state, symbol, to_state)
        else:
            self._add_rule(from_state, input_matcher, to_state)
        return self  # For chaining

    def _add_rule(self, from_state: State, input_matcher: InputMatcher, to_state: State):
        rule = TransitionRule(from_state, input_matcher, to_state)
        if from_state not in self._table:
            self._table[from_state] = []
        self._table[from_state].append(rule)

    def get_rules(self, state: State) -> List[TransitionRule]:
        return self._table.get(state, [])

    def states(self):
        """Return a set of all states in the transition table."""
        states = set(self._table.keys())
        for rules in self._table.values():
            for rule in rules:
                states.add(rule.to_state)
        return states
    
    def all_inputs(self):
        """Return a set of all unique input matchers used in the table."""
        inputs = set()
        for rules in self._table.values():
            for rule in rules:
                inputs.add(rule.input_matcher)
        return inputs
    
    def inputs_for_state(self, state: State):
        """Return a set of input matchers for a given state."""
        return {rule.input_matcher for rule in self.get_rules(state)}

    def has(self, state: State, input_matcher: InputMatcher):
        """Return True if a transition exists for the given state and input."""
        return any(rule.input_matcher == input_matcher for rule in self.get_rules(state))

    def count(self, state: State, input_matcher: InputMatcher):
        """Return the number of transitions for the given state and input."""
        return sum(1 for rule in self.get_rules(state) if rule.input_matcher == input_matcher)

    def get(self, state: State, input_matcher: InputMatcher):
        """Return the to_state for a given state and input_matcher, or None if not found."""
        for rule in self.get_rules(state):
            if rule.input_matcher == input_matcher:
                return rule.to_state
        return None
    def __str__(self):
        """
        Returns a string representation of the transition table.
        """
        lines = []
        for from_state, rules in self._table.items():
            for rule in rules:
                lines.append(f"{rule.from_state} --[{rule.input_matcher}]--> {rule.to_state}")
        return "\n".join(lines)