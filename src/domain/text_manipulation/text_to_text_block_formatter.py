import re
from typing import List

from src.config import config
from src.models.TextBlock import TextBlock, SimpleTextBlock

"""Splits the Markdown text into lines."""


def multiline_text_to_single_line_array(markdown_text: SimpleTextBlock) -> List[SimpleTextBlock]:
    # only an empty line is a separator
    lines = markdown_text.text.split('\n\n')
    result = []

    # Add an empty line after each line except the last one to have a separator in the final text
    for i in range(len(lines)):
        result.append(SimpleTextBlock(text=lines[i].strip(), skip=False, indentations_count=markdown_text.indentations_count))
        if i < len(lines) - 1:
            result.append(SimpleTextBlock(text='', skip=True, indentations_count=0))
    return result


def extract_math_code_blocks(text_block: SimpleTextBlock):
    blocks = process_text_block(text_block, '```math', '```')
    for block in blocks:
        block.at_start = True
        block.at_end = True
        if block.is_enclosed:
            block.skip = True

    return blocks


def extract_code_blocks(text_block: SimpleTextBlock):
    blocks = process_text_block(text_block, '```', '```', '```')
    for block in blocks:
        block.at_start = True
        block.at_end = True
        if block.is_enclosed:
            block.is_enclosed = False
            block.skip = True

    return blocks


def process_text_block(text_block: SimpleTextBlock, start_separator: str, end_separator: str, replace_text="") -> List[
    TextBlock]:
    """Processes a text block and creates a list of objects."""
    text_block_text = text_block.text.strip()  # Remove leading and trailing whitespace

    # Use the patterns from the config
    # Check for square bracket enclosed text first
    regex = re.compile(re.escape(start_separator) + r'(.*?)' + re.escape(end_separator), re.DOTALL)

    # Process round bracket enclosed text
    matches = list(regex.finditer(text_block_text))
    if not matches:
        # No match found, create a direct object
        return [TextBlock(text=text_block_text, at_start=True, is_enclosed=False, at_end=True, skip=False, indentations_count=text_block.indentations_count)]

    parts: List[TextBlock] = []
    last_end = 0

    for match in matches:
        start, end = match.span()
        enclosed_text = match.group(0)

        # Text before the bracket
        if start > last_end:
            parts.append(
                TextBlock(text=text_block_text[last_end:start], at_start=last_end == 0, is_enclosed=False, at_end=False,
                          skip=False))

        new_text = enclosed_text.replace(start_separator, replace_text).replace(end_separator, replace_text)
        # Text within the bracket
        parts.append(TextBlock(text=new_text,
                               at_start=False, is_enclosed=True, at_end=False, skip=False))

        last_end = end

    # Text after the last bracket
    if last_end < len(text_block_text):
        parts.append(
            TextBlock(text=text_block_text[last_end:], at_start=False, is_enclosed=False, at_end=True, skip=False))
    else:
        # Mark the last part as at_end if no text follows
        parts[-1].at_end = True

    parts[0].indentations_count = text_block.indentations_count
    return insert_empty_elements(parts)


def insert_empty_elements(parts: List[TextBlock]) -> List[TextBlock]:
    if len(parts) == 1:
        return parts
    """Inserts empty elements before and after enclosed text if needed."""
    result: List[TextBlock] = []
    for i, part in enumerate(parts):
        if part.is_enclosed:
            # Insert empty element before if not at the start
            if i == 0 or not parts[i - 1].at_end:
                result.append(TextBlock(text="", at_start=False, is_enclosed=False, at_end=False, skip=False))
            result.append(part)
            # Insert empty element after if not at the end
            if i == len(parts) - 1 or not parts[i + 1].at_start:
                result.append(TextBlock(text="", at_start=False, is_enclosed=False, at_end=False, skip=False))

        # Insert empty element if the text is a single dash, otherwise notion will completely ignore it.
        # Happens for lists which will start with a math equation.
        elif part.at_start and part.text.strip() == "-":
            if i == 0 or not parts[i - 1].at_end:
                result.append(TextBlock(text="", at_start=False, is_enclosed=False, at_end=False, skip=False))
            result.append(part)
        else:
            result.append(part)
    return result


def map_string_list_to_text_blocks(string_list: List[SimpleTextBlock]) -> List[TextBlock]:
    return [
        TextBlock(text=text.text,
                  at_start=True,
                  is_enclosed=False,
                  at_end=True,
                  skip=False,
                  indentations_count=text.indentations_count
                  ) for text in string_list]


def process_markdown_text_to_text_blocks(markdown_blocks: List[SimpleTextBlock]) -> List[TextBlock]:
    text_blocks = map_string_list_to_text_blocks(markdown_blocks)
    # text_blocks = insert_empty_elements(text_blocks)
    blocks_with_math_code_blocks: List[TextBlock] = []
    for block in text_blocks:
        blocks_with_math_code_blocks.extend(extract_math_code_blocks(block))
    # Math Code Blocks

    blocks_with_code: List[TextBlock] = []
    for block in blocks_with_math_code_blocks:
        if block.skip:
            blocks_with_code.append(block)
            continue
        blocks_with_code.extend(extract_code_blocks(block))

    # Block equations
    blocks_with_block_equations: List[TextBlock] = []
    for block in blocks_with_code:
        if block.skip:
            blocks_with_block_equations.append(block)
            continue
        text_blocks_with_block_equations = process_text_block(block,
                                                              config.BLOCK_MATHE_EQUATION_SEPARATOR_START,
                                                              config.BLOCK_MATHE_EQUATION_SEPARATOR_END)

        for block in text_blocks_with_block_equations:
            block.at_start = True
            block.at_end = True
        blocks_with_block_equations.extend(text_blocks_with_block_equations)

    # Inline Equations
    processed_blocks: List[TextBlock] = []

    for block in blocks_with_block_equations:
        if block.is_enclosed or block.skip:
            processed_blocks.append(block)
            continue
        for newBlock in multiline_text_to_single_line_array(block):
            processed_blocks.extend(process_text_block(newBlock, config.INLINE_MATHE_EQUATION_SEPARATOR_START,
                                                       config.INLINE_MATHE_EQUATION_SEPARATOR_END))

    return processed_blocks
