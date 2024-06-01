from typing import TypedDict
class TextBlock(TypedDict):
    text: str
    at_start: bool
    is_enclosed: bool
    at_end: bool

