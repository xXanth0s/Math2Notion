import re
from typing import List
from config import config  # Import the config instance from the config module
from models import TextBlock

"""Splits the Markdown text into lines."""


def multiline_text_to_single_line_array(markdown_text: str) -> List[str]:
    # only an empty line is a separator
    lines = markdown_text.split('\n\n')
    result = []

    # Add an empty line after each line except the last one to have a separator in the final text
    for i in range(len(lines)):
        result.append(lines[i])
        if i < len(lines) - 1:
            result.append('')
    return result


def extract_math_code_blocks(text_block: str):
    blocks = process_text_block(text_block, '```math', '```')
    for block in blocks:
        block["at_start"] = True
        block["at_end"] = True
        if block["is_enclosed"]:
            block["skip"] = True

    return blocks

def extract_code_blocks(text_block: str):
    blocks = process_text_block(text_block, '```', '```', '```')
    for block in blocks:
        block["at_start"] = True
        block["at_end"] = True
        if block["is_enclosed"]:
            block["is_enclosed"] = False
            block["skip"] = True

    return blocks


def process_text_block(text_block: str, start_separator: str, end_separator: str, replace_text="") -> List[TextBlock]:
    """Processes a text block and creates a list of objects."""
    text_block = text_block.strip()  # Remove leading and trailing whitespace

    # Use the patterns from the config
    # Check for square bracket enclosed text first
    regex = re.compile(re.escape(start_separator) + r'(.*?)' + re.escape(end_separator), re.DOTALL)

    # Process round bracket enclosed text
    matches = list(regex.finditer(text_block))
    if not matches:
        # No match found, create a direct object
        return [{"text": text_block, "at_start": True, "is_enclosed": False, "at_end": True, "skip": False}]

    parts: List[TextBlock] = []
    last_end = 0

    for match in matches:
        start, end = match.span()
        enclosed_text = match.group(0)

        # Text before the bracket
        if start > last_end:
            parts.append(
                {"text": text_block[last_end:start], "at_start": last_end == 0, "is_enclosed": False, "at_end": False,
                 "skip": False})

        new_text = enclosed_text.replace(start_separator, replace_text).replace(end_separator, replace_text)
        # Text within the bracket
        parts.append({"text": new_text,
                      "at_start": False, "is_enclosed": True, "at_end": False, "skip": False})

        last_end = end

    # Text after the last bracket
    if last_end < len(text_block):
        parts.append(
            {"text": text_block[last_end:], "at_start": False, "is_enclosed": False, "at_end": True, "skip": False})
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
                result.append({"text": "", "at_start": False, "is_enclosed": False, "at_end": False, "skip": False})
            result.append(part)
            # Insert empty element after if not at the end
            if i == len(parts) - 1 or not parts[i + 1]['at_start']:
                result.append({"text": "", "at_start": False, "is_enclosed": False, "at_end": False, "skip": False})

        # Insert empty element if the text is a single dash, otherwise notion will completely ignore it.
        # Happens for lists which will start with a math equation.
        elif part['at_start'] and part['text'].strip() == "-":
            if i == 0 or not parts[i - 1]['at_end']:
                result.append({"text": "", "at_start": False, "is_enclosed": False, "at_end": False, "skip": False})
            result.append(part)
        else:
            result.append(part)
    return result


def get_text_from_user() -> str:
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

    return "\n".join(markdown_text)


def process_markdown_input() -> List[TextBlock]:
    markdown_text_str = get_text_from_user()

    # Math Code Blocks
    blocks_with_math_code_blocks = extract_math_code_blocks(markdown_text_str)
    # Code Blocks

    blocks_with_code: List[TextBlock] = []
    for block in blocks_with_math_code_blocks:
        if block["skip"]:
            blocks_with_code.append(block)
            continue
        blocks_with_code.extend(extract_code_blocks(block["text"]))

    # Block equations
    blocks_with_block_equations: List[TextBlock] = []
    for block in blocks_with_code:
        if block["skip"]:
            blocks_with_block_equations.append(block)
            continue
        text_blocks_with_block_equations = process_text_block(block["text"],
                                                              config.BLOCK_MATHE_EQUATION_SEPARATOR_START,
                                                              config.BLOCK_MATHE_EQUATION_SEPARATOR_END)

        for block in text_blocks_with_block_equations:
            block["at_start"] = True
            block["at_end"] = True
        blocks_with_block_equations.extend(text_blocks_with_block_equations)

    # Inline Equations
    processed_blocks: List[TextBlock] = []

    for block in blocks_with_block_equations:
        if block["is_enclosed"] or block["skip"]:
            processed_blocks.append(block)
            continue
        for newBlock in multiline_text_to_single_line_array(block["text"]):
            processed_blocks.extend(process_text_block(newBlock, config.INLINE_MATHE_EQUATION_SEPARATOR_START,
                                                       config.INLINE_MATHE_EQUATION_SEPARATOR_END))

    return processed_blocks


if __name__ == "__main__":
    processed_blocks = process_markdown_input()
    # Output the results
    print("\nProcessed Text Blocks:")
    for block in processed_blocks:
        print(block)
    # text = get_text_from_user()
    # text_blocks_with_block_equations = process_text_block(text, '```math', '```')
    #
    # print(text_blocks_with_block_equations)
