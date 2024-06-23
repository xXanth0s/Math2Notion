from src.models.MarkdownSeparator import all_markdown_separators


def is_text_simple_markdown_separator(text: str) -> bool:
    stripped_text = text.strip()
    return any(stripped_text == separator['separator'] for separator in all_markdown_separators)