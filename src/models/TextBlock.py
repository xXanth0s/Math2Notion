from typing import TypedDict


class TextBlock(TypedDict):
    text: str
    at_start: bool
    is_enclosed: bool
    skip: bool
    at_end: bool

class SimpleTextBlock(TypedDict):
    text: str
    skip: bool