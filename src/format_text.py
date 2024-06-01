import re
from typing import List

from src.models import TextBlock


def markdown_to_array(markdown_text: str) -> List[str]:
    """Splits the Markdown text into lines."""
    lines = markdown_text.split('\n')
    return lines


def process_text_block(text_block: str) -> List[TextBlock]:
    """Processes a text block and creates a list of objects."""
    text_block = text_block.strip()  # Remove leading and trailing whitespace

    round_pattern = re.compile(r'\\\((.*?)\\\)')
    square_pattern = re.compile(r'\\\[(.*?)\\\]')

    # Check for square bracket enclosed text first
    square_matches = list(square_pattern.finditer(text_block))
    if square_matches:
        # We found text enclosed by \[ \], replace the brackets with $ and mark it as enclosed
        return [{"text": text_block.replace("\\[", "$").replace("\\]", "$"), "at_start": True, "is_enclosed": True,
                 "at_end": True}]

    # Process round bracket enclosed text
    matches = list(round_pattern.finditer(text_block))
    if not matches:
        # No match found, create a direct object
        return [{"text": text_block, "at_start": True, "is_enclosed": False, "at_end": True}]

    parts: List[TextBlock] = []
    last_end = 0

    for match in matches:
        start, end = match.span()
        enclosed_text = match.group(0)

        # Text before the bracket
        if start > last_end:
            parts.append(
                {"text": text_block[last_end:start], "at_start": last_end == 0, "is_enclosed": False, "at_end": False})

        # Text within the bracket
        parts.append(
            {"text": enclosed_text.replace("\\(", "$").replace("\\)", "$"), "at_start": False, "is_enclosed": True,
             "at_end": False})

        last_end = end

    # Text after the last bracket
    if last_end < len(text_block):
        parts.append({"text": text_block[last_end:], "at_start": False, "is_enclosed": False, "at_end": True})
    else:
        # Mark the last part as at_end if no text follows
        parts[-1]["at_end"] = True

    return insert_empty_elements(parts)


def insert_empty_elements(parts: List[TextBlock]) -> List[TextBlock]:
    """Inserts empty elements before and after enclosed text if needed."""
    result: List[TextBlock] = []
    for i, part in enumerate(parts):
        if part['is_enclosed']:
            # Insert empty element before if not at the start
            if i == 0 or not parts[i - 1]['at_end']:
                result.append({"text": "", "at_start": False, "is_enclosed": False, "at_end": False})
            result.append(part)
            # Insert empty element after if not at the end
            if i == len(parts) - 1 or not parts[i + 1]['at_start']:
                result.append({"text": "", "at_start": False, "is_enclosed": False, "at_end": False})
        else:
            result.append(part)
    return result


def process_markdown_input() -> List[TextBlock]:
    """Reads the Markdown text input and returns the processed text blocks."""
    print("Please enter the Markdown text (finish with a line containing 'END'):")
    markdown_text: List[str] = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            markdown_text.append(line)
        except EOFError:
            break

    markdown_text_str = "\n".join(markdown_text)
    text_blocks = markdown_to_array(markdown_text_str)

    # Process the text blocks
    processed_blocks: List[TextBlock] = []
    for block in text_blocks:
        processed_blocks.extend(process_text_block(block))

    return processed_blocks
