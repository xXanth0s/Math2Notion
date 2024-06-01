from format_text import process_markdown_input
from notion_gui_utils import insert_text_blocks_and_convert_to_math_equations
from switch_to_notion import prompt_user_to_switch_to_notion
import sys
import os

# Add the project directory and src directory to sys.path
project_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.join(project_dir, 'src')

sys.path.append(project_dir)
sys.path.append(src_dir)



if __name__ == '__main__':
    input_text = process_markdown_input()
    prompt_user_to_switch_to_notion("After 5 seconds the text will be pasted and processed in Notion.")
    insert_text_blocks_and_convert_to_math_equations(input_text)
