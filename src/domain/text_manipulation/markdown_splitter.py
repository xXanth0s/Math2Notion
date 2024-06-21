import re
from typing import List

from src.models.MarkdownSeparator import MarkdownSeparator
from src.models.TextBlock import SimpleTextBlock
from src.utils.array_utils import insert_between_elements_to_array


def strip_lines(text):
    stripped_lines = [line.strip() for line in text.splitlines()]
    return '\n'.join(stripped_lines)


def separate_text_by_separators(text: str, separators: List[str], skip_separated_text: bool) -> List[SimpleTextBlock]:
    result: List[SimpleTextBlock] = []
    last_end = 0

    for separator in separators:
        start = text.find(separator, last_end)
        if start > last_end:
            text_before = text[last_end:start].strip()
            result.append(SimpleTextBlock(text=text_before, skip=False))
        result.append(SimpleTextBlock(text=separator, skip=skip_separated_text))
        last_end = start + len(separator)

    if last_end < len(text):
        text_at_end = text[last_end:].strip()
        result.append(SimpleTextBlock(text=text_at_end, skip=False))

    return result


def split_multiline_markdown_text(text: str, separator: MarkdownSeparator) -> List[SimpleTextBlock]:
    escaped_char = separator['separator']
    try:
        seperator_string = re.escape(escaped_char)
        pattern = fr'^{seperator_string}(?:.*(?:\n(?!{seperator_string}|$).*)*)*'
        # pattern = rf'^{seperator_string}.*?(?:\n(?!{seperator_string}|$|\n).*)*(?=\n\n|$)'
        # pattern = fr'^{seperator_string}.*?(?=(?<!\n)\n{seperator_string}|\n\n|$)'
        matches: List[str] = re.findall(pattern, text, re.DOTALL | re.MULTILINE)
        return separate_text_by_separators(text, matches, False)
    except re.error as e:
        print(f"Regex-Fehler: {e}")
        return []


def split_multiline_markdown_text_with_end_separator(text: str, separator: MarkdownSeparator) -> List[SimpleTextBlock]:
    try:
        start_separator = re.escape(separator['separator'])
        end_separator = re.escape(separator['end_separator'])
        pattern = fr"^{start_separator}{r'.*?'}{end_separator}"
        matches: List[str] = re.findall(pattern, text, re.DOTALL | re.MULTILINE)
        return separate_text_by_separators(text, matches, True)
    except re.error as e:
        print(f"Regex-Fehler: {e}")
        return []


def split_singleline_markdown_text(markdown_text: str, separator: MarkdownSeparator) -> List[SimpleTextBlock]:
    try:
        escaped_string = re.escape(separator['separator'])
        pattern = fr"^{escaped_string}.*?$"
        matches = re.findall(pattern, markdown_text, re.MULTILINE)
        return separate_text_by_separators(markdown_text, matches, True)
    except re.error as e:
        print(f"Regex-Fehler: {e}")
        return []


def split_markdown_text_by_markdown_separator(text: str, separator: MarkdownSeparator) -> List[SimpleTextBlock]:
    if separator['is_multiline']:
        if 'end_separator' in separator:
            return split_multiline_markdown_text_with_end_separator(text, separator)
        return split_multiline_markdown_text(text, separator)
    else:
        return split_singleline_markdown_text(text, separator)


def split_text_by_markdown_separators(text: str, separators: List[MarkdownSeparator]) -> List[str]:
    separators = sorted(separators, key=lambda x: 'end_separator' not in x)
    stripped_text = strip_lines(text)
    parts = [SimpleTextBlock(text=stripped_text, skip=False)]
    for separator in separators:
        new_parts: [SimpleTextBlock] = []
        for current_part in parts:
            if current_part['skip']:
                new_parts.append(current_part)
                continue
            new_parts.extend(split_markdown_text_by_markdown_separator(current_part['text'], separator))
        parts = new_parts
    final_parts = [text_part['text'] for text_part in parts]
    return insert_between_elements_to_array(final_parts, '')
