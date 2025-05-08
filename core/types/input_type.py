from typing import Dict, List, Union
import re

ALLOWED_TYPES = (str, int, bool, re.Pattern)
InputMatcher = Union[str, int, bool, re.Pattern, list]