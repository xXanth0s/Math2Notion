import os
import sys
import threading
import time

from config import config
from src.domain.text_manipulation.markdown_splitter import split_text_by_markdown_separators
from src.models.MarkdownSeparator import all_markdown_separators
from src.domain.text_manipulation.text_to_text_block_formatter import process_markdown_text_to_text_blocks
from src.domain.notion.notion_gui_utils import MathEquationInserter
from src.domain.notion.notion_window_observer import NotionWindowObserver
from src.domain.cli.markdown_input_reader import read_markdown_input_from_console

project_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.join(project_dir, '')

sys.path.append(project_dir)
sys.path.append(src_dir)

if __name__ == '__main__':
    stop_event = threading.Event()
    math_equation_inserter = MathEquationInserter(stop_event)
    markdown_input = read_markdown_input_from_console()
    markdown_blocks = split_text_by_markdown_separators(markdown_input, all_markdown_separators)
    input_text = process_markdown_text_to_text_blocks(markdown_blocks)

    notion_app_watcher = NotionWindowObserver(poll_interval=0.1)

    first_run = True

    def on_next(is_notion_in_foreground):
        global first_run
        if is_notion_in_foreground:
            print("Notion got selected. Starting with text insertion in 5 Seconds. When switching the app, "
                  "the programm will shut down.")

            for i in range(config.COUNTDOWN_LENGTH, 0, -1):
                if stop_event.is_set():
                    break
                print(f"{i}...")
                time.sleep(1)
            if not stop_event.is_set():
                thread = threading.Thread(
                    target=math_equation_inserter.insert_text_blocks_and_convert_to_math_equations,
                    args=(input_text,))
                thread.start()


        elif not first_run:
            print("Notion is not in focus anymore. The app will not continue with inserting the text.")
            notion_app_watcher.stop_polling()
            stop_event.set()
            sys.exit(0)
        first_run = False


    notion_app_watcher.get_observable().subscribe(
        on_next=on_next,
        on_error=lambda e: print(f"Error: {e}"),
    )

    try:
        notion_app_watcher.start_polling()
        print("Please select the Notion app, so the insertion can start.")
    except KeyboardInterrupt:
        notion_app_watcher.stop_polling()