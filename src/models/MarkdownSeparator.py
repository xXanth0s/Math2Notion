from typing import TypedDict, List
from typing_extensions import NotRequired


class MarkdownSeparator(TypedDict):
    is_multiline: bool
    separator: str
    end_separator: NotRequired[str]
    no_math_equations_included: bool


all_markdown_separators: List[MarkdownSeparator] = [
    MarkdownSeparator(is_multiline=True, separator='```', end_separator='```', no_math_equations_included=True),
    MarkdownSeparator(is_multiline=False, separator='#', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=False, separator='##', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=False, separator='###', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=False, separator='####', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=False, separator='#####', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=False, separator='######', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='-', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='*', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='[ ]', no_math_equations_included=False),

    # Numbered Lists. Temporarily only 20, should be solved with regex.
    MarkdownSeparator(is_multiline=True, separator='1.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='2.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='3.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='4.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='5.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='6.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='7.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='8.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='9.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='10.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='11.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='12.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='13.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='14.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='15.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='16.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='17.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='18.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='19.', no_math_equations_included=False),
    MarkdownSeparator(is_multiline=True, separator='20.', no_math_equations_included=False),
]
