from typing import List

from src.models.TextBlock import SimpleTextBlock


def count_leading_spaces(string: str) -> int:
    leading_spaces = 0
    for char in string:
        if char == ' ':
            leading_spaces += 1
        else:
            break
    return leading_spaces


def strip_all_line_breaks(text: List[SimpleTextBlock]) -> List[SimpleTextBlock]:
    for line in text:
        line.text = line.text.strip('\n')
    return text

def remove_empty_lines(text: List[SimpleTextBlock]) -> List[SimpleTextBlock]:
    return [line for line in text if line.text.strip() != '']
