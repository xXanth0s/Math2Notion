from format_text import process_markdown_input
from src.notion_gui_utils import paste_text, insert_text_blocks_and_convert_to_math_equations
from switch_to_notion import prompt_user_to_switch_to_notion


if __name__ == '__main__':
    input_text = process_markdown_input()
    print(input_text)
    prompt_user_to_switch_to_notion("After 5 seconds the text will be pasted and processed in Notion.")
    insert_text_blocks_and_convert_to_math_equations(input_text)
