from typing import Any, Iterable
import re

class Splitter:
    def split(self, input_data: Any) -> Iterable:
        raise NotImplementedError

class StringSplitter(Splitter):
    def split(self, input_data: Any) -> Iterable:
        if not isinstance(input_data, str):
            raise TypeError("Input must be a string")
        return input_data

class ListSplitter(Splitter):
    def split(self, input_data: Any) -> Iterable:
        if not isinstance(input_data, list):
            raise TypeError("Input must be a list")
        return input_data

class CommaStringSplitter(Splitter):
    def split(self, input_data: Any) -> Iterable:
        if not isinstance(input_data, str):
            raise TypeError("Input must be a string")
        return input_data.split(',')
    
class WhitespaceSplitter(Splitter):
    def split(self, input_data: Any) -> Iterable:
        if not isinstance(input_data, str):
            raise TypeError("Input must be a string")
        return input_data.split()
    
class RegexSplitter(Splitter):
    def __init__(self, pattern: str):
        self.pattern = pattern

    def split(self, input_data: Any) -> Iterable:
        if not isinstance(input_data, str):
            raise TypeError("Input must be a string")
        return re.split(self.pattern, input_data)

class WholeStringSplitter(Splitter):
    def split(self, input_data: Any) -> Iterable:
        if not isinstance(input_data, str):
            raise TypeError("Input must be a string")
        return [input_data]