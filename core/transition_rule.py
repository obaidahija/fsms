from typing import Union
import re
from .state import State
from .types.input_type import InputMatcher, ALLOWED_TYPES  # Import allowed types

class TransitionRule:
    @property
    def to_state(self):
        return self._to_state

    def __init__(self, from_state: State, input_matcher: InputMatcher, to_state: State):
        # Validate input_matcher type at construction using ALLOWED_TYPES
        if not (
            isinstance(input_matcher, ALLOWED_TYPES + (list,))
            and (not isinstance(input_matcher, list) or all(isinstance(m, ALLOWED_TYPES) for m in input_matcher))
        ):
            raise TypeError(f"Unsupported input matcher type: {type(input_matcher)}")
        self.from_state = from_state
        self.input_matcher = input_matcher
        self._to_state = to_state

    def matches(self, input_symbol: InputMatcher) -> bool:
        if isinstance(self.input_matcher, list):
            return any(
                TransitionRule(self.from_state, matcher, self.to_state).matches(input_symbol)
                for matcher in self.input_matcher
            )
        elif isinstance(self.input_matcher, re.Pattern):
            return bool(self.input_matcher.match(str(input_symbol)))
        elif isinstance(self.input_matcher, tuple(t for t in ALLOWED_TYPES if t is not re.Pattern)):
            return self.input_matcher == input_symbol
        else:
            raise TypeError(f"Unsupported input matcher type: {type(self.input_matcher)}")
        

    def __repr__(self):
        return f"Transition({self.from_state} -> {self.to_state} on '{self.input_matcher}')"