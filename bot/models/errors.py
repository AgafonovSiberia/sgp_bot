from typing import NamedTuple


class ValidInputError(NamedTuple):
    is_valid: bool
    error_text: str = ""