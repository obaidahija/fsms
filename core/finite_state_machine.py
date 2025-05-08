from typing import Dict, Any

from core.transition_table import TransitionTable
from core.output_mapping import OutputMapping
from .state import State
from .abstract_finite_state_machine import AbstractFiniteStateMachine
from core.splitter import Splitter, StringSplitter

class FiniteStateMachine(AbstractFiniteStateMachine):
    def __init__(self, 
                 initial_state: State, 
                 transitions: TransitionTable,
                 output_mapping: OutputMapping,
                 splitter: Splitter = None):
        super().__init__(output_mapping)
        self.current_state = self.initial_state = initial_state
        self.transitions = transitions
        self.splitter = splitter or StringSplitter()

    def reset(self) -> None:
        self.current_state = self.initial_state


    def process(self, input_data: Any):
        self.reset()
        for symbol in self.splitter.split(input_data):
            rules = self.transitions.get_rules(self.current_state)
            for rule in rules:
                if rule.matches(symbol):
                    self.current_state = rule.to_state
                    break
            else:
                raise ValueError(f"No transition for {self.current_state} on '{symbol}'")
            
    def get_current_state(self) -> State:
        return self.current_state

    def validate(self):
        """Run all FSM validation checks."""
        errors = []
        errors.extend(self._check_unreachable_states())
        errors.extend(self._check_missing_transitions())
        errors.extend(self._check_ambiguous_transitions())
        return errors

    def _check_unreachable_states(self):
        """Return a list of unreachable states."""
        reachable = set()
        to_visit = {self.initial_state}
        while to_visit:
            state = to_visit.pop()
            if state in reachable:
                continue
            reachable.add(state)
            for input_token in self.transitions.inputs_for_state(state):
                next_state = self.transitions.get(state, input_token)
                if next_state and next_state not in reachable:
                    to_visit.add(next_state)
        unreachable = set(self.transitions.states()) - reachable
        return [f"Unreachable state: {s}" for s in unreachable]

    def _check_missing_transitions(self):
        """Return a list of missing transitions for each state/input."""
        errors = []
        for state in self.transitions.states():
            for input_token in self.transitions.all_inputs():
                if not self.transitions.has(state, input_token):
                    errors.append(f"Missing transition: state={state}, input={input_token}")
        return errors

    def _check_ambiguous_transitions(self):
        """Return a list of ambiguous transitions (multiple for same state/input)."""
        errors = []
        for state in self.transitions.states():
            for input_token in self.transitions.all_inputs():
                if self.transitions.count(state, input_token) > 1:
                    errors.append(f"Ambiguous transition: state={state}, input={input_token}")
        return errors