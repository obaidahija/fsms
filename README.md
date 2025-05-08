# FSMS

FSMS is a Python framework for building finite state machines (FSMs) in a modular and extensible way. It allows you to define states, transitions, outputs, and how input is split into tokens using pluggable splitter classes.

---

## Table of Contents

- [Design Overview](#design-overview)
- [Approach](#approach)
- [Splitter Concept](#splitter-concept)
- [AbstractFiniteStateMachine](#abstractfinitestatemachine)
- [Example: Modulo-3 FSM](#example-modulo-3-fsm)
- [Usage](#usage)
- [Files and Structure](#files-and-structure)
- [Types](#types)
- [What I Would Add or Improve](#what-i-would-add-or-improve)
- [Testing](#testing)
- [License](#license)
- [Summary](#summary)

---

## Design Overview

FSMS is designed around the following components:

- **State**: Represents a state in the FSM.
- **TransitionTable**: Defines transitions between states based on input tokens.
- **OutputMapping**: Maps states to output values.
- **Splitter**: Defines how input is split into tokens for the FSM to process.
- **FiniteStateMachine**: The base class that ties together states, transitions, outputs, and the splitter.
- **Custom Machines**: You create your own FSMs by subclassing `FiniteStateMachine` and configuring the above components.

---

## Approach

The framework is object-oriented and highly composable:

- You define states using the `State` class.
- You define transitions using the `TransitionTable` class, mapping (state, input) pairs to next states.
- You define outputs using the `OutputMapping` class, mapping states to output values.
- You select or implement a `Splitter` class to control how input is tokenized.
- You subclass `FiniteStateMachine` to assemble your FSM, passing in the states, transitions, output mapping, and splitter.

---

## Splitter Concept

A **Splitter** is a class that defines how to break input into tokens for the FSM. This allows you to control whether your FSM processes input character-by-character, word-by-word, by regex, or any custom logic.

**Built-in splitters include:**
- `StringSplitter`: Yields each character of a string.
- `ListSplitter`: Yields each element of a list.
- `CommaStringSplitter`: Splits a string by commas.
- `WhitespaceSplitter`: Splits a string by whitespace.
- `RegexSplitter`: Splits a string using a regular expression.
- `WholeStringSplitter`: Treats the entire input as a single token.

**Example: Using a splitter**
```python
from core.splitter import StringSplitter, CommaStringSplitter

splitter = StringSplitter()  # Will yield each character
tokens = splitter.split("1011")  # yields '1', '0', '1', '1'

splitter = CommaStringSplitter()
tokens = splitter.split("a,b,c")  # yields 'a', 'b', 'c'
```

You pass the splitter instance to your FSM when you construct it.

---

## AbstractFiniteStateMachine

The `AbstractFiniteStateMachine` is an abstract base class that defines the interface for all FSMs in this framework. Every FSM you implement should inherit from this class (directly or via `FiniteStateMachine`) and **must implement the `calculate` method**.

- The `calculate` method is where you define how your FSM processes input and what it returns.
- The return type of `calculate` is up to you: it can return an integer, string, boolean, or any object, depending on your FSM's purpose.
- This design gives you flexibility to decide what the output of your FSM should be.
- **FSM Validation:**  
  When implementing a new FSM, you can use the `validate` method (available on `FiniteStateMachine`) to check for common issues such as unreachable states, missing transitions, or ambiguous transitions. This helps ensure your FSM is correctly defined before using it.

**Example:**
```python
from core.abstract_finite_state_machine import AbstractFiniteStateMachine

class MyFSM(AbstractFiniteStateMachine):
    def calculate(self, input_data):
        # process input_data and return any type you want
        return ...
```

---

## Example: Modulo-3 FSM

This FSM computes the remainder when a binary string is interpreted as a number and divided by 3.

```python
from core.state import State
from core.transition_table import TransitionTable
from core.output_mapping import OutputMapping
from core.splitter import StringSplitter
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
        self.process(binary_string)
        return self.get_output()
```

**How it works:**
- Each state represents a possible remainder (0, 1, or 2).
- Transitions are defined for each input ('0' or '1') from each state.
- The output mapping assigns the remainder value to each state.
- The `StringSplitter` is used so the FSM processes the input one character at a time.

---

## Usage

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Create or use a machine:**
    ```python
    from machines.mod_three_machine import ModThreeMachine

    fsm = ModThreeMachine()
    result = fsm.calculate("1011")  # result will be 0, 1, or 2
    ```

3. **Change the splitter if needed:**
    - Use a different splitter by passing it to your FSM's constructor.

---

## Files and Structure

- **core/abstract_finite_state_machine.py**:  
  Defines the `AbstractFiniteStateMachine` base class. All FSMs should inherit from this and implement the `calculate` method.

- **core/state.py**:  
  Contains the `State` class, representing a state in the FSM.

- **core/transition_rule.py**:  
  Contains the `TransitionRule` class, which encapsulates a single transition: from a state, on a given input, to a next state.

- **core/transition_table.py**:  
  Contains the `TransitionTable` class, which manages a collection of `TransitionRule` objects and provides lookup for transitions.

- **core/output_mapping.py**:  
  Maps states to output values.

- **core/splitter.py**:  
  Contains all splitter classes, which define how input is tokenized for the FSM.

- **core/types.py**:  
  Defines type aliases and helper types used throughout the framework for clarity and type safety.

- **core/finite_state_machine.py**:  
  Implements the main FSM logic, typically subclassed by user-defined FSMs.

- **machines/**:  
  Contains concrete FSM implementations (e.g., `mod_three_machine.py`).

---

## Types

The `core/types` folder contains type definitions and helpers to make FSMs robust and type-safe.

- **output_type.py**:  
  Defines the `OutputType` type alias, which is a union of standard output types for FSMs: `int`, `str`, `float`, `list`, `dict`, `bool`, `None`, and `Exception`.

- **input_type.py**:  
  Defines allowed input types for FSM transitions and input matching.  
  - `ALLOWED_TYPES` includes `str`, `int`, `bool`, and `re.Pattern`.
  - `InputMatcher` is a type alias for values or patterns that can be used to match input tokens in transitions.

> **Notes:** If you do not define an output for a state in your output mapping, the FSM will return `None` as the result for that state.
> 
> When using custom splitter classes, ensure that the `split` method yields tokens compatible with your transition table's expected input types.

These types help ensure that your FSMs are consistent and can be checked with static analysis tools.

---

## What I Would Add or Improve

If I were to extend or improve this project, here are some ideas:


- **Serialization/Deserialization:**  
  Allow FSMs to be saved to and loaded from JSON/YAML for easier sharing and reuse.
  
- **More Built-in Splitters:**  
  Include additional splitters for common data formats (e.g., CSV, JSON paths).

- **Extensive Documentation and Tutorials:**  
  Expand documentation with more real-world examples and step-by-step guides.

---

## Testing

Run tests using `pytest`:

```bash
pytest
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Summary

FSMS lets you build FSMs by composing states, transitions, outputs, and input splitters. The splitter concept gives you full control over how input is tokenized, making the framework flexible for many parsing and processing tasks.

See the `machines/` directory for more FSM examples.
