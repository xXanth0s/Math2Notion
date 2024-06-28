import os
import sys
import time
from typing import List
import pyautogui
import pyperclip
from threading import Event

from src.config import config
from src.models.TextBlock import TextBlock
from src.utils.markdown_utils import is_text_simple_markdown_separator
from src.utils.text_block_utils import is_block_equation


class MathEquationInserter:
    def __init__(self, stop_event: Event):
        self.time_to_sleep = config.TIME_TO_SLEEP
        self.stop_event = stop_event

    def _copy_text(self):
        time.sleep(self.time_to_sleep)
        os.system("""
        osascript -e 'tell application "System Events" to keystroke "c" using {command down}'
        """)
        time.sleep(self.time_to_sleep)
        return pyperclip.paste()

    def _press_hotkeys(self, keys: List[str]):
        pyautogui.hotkey(*keys, interval=0.02)
        time.sleep(self.time_to_sleep)

    def _press_key(self, key: str):
        pyautogui.press(key)
        time.sleep(self.time_to_sleep)

    def _move_to_end_of_cell(self):
        self._press_hotkeys(['command', 'a'])
        self._press_key('right')

    def _insert_block_equations(self, text: TextBlock, previous_block: TextBlock):
        if is_block_equation(previous_block):
            os.system("""
                    osascript -e 'tell application "System Events" to keystroke "d" using {command down}'
                    """)
            time.sleep(self.time_to_sleep)
            self._press_key('enter')
        else:
            self._press_key('enter')
            self._press_key('space')
            time.sleep(self.time_to_sleep)
            os.system("""
                osascript -e 'tell application "System Events" to keystroke "/"'
            """)
            os.system("""
                osascript -e 'tell application "System Events" to keystroke "e"'
            """)
            os.system("""
                osascript -e 'tell application "System Events" to keystroke "q"'
            """)
            time.sleep(self.time_to_sleep)

            self._press_key('enter')
            time.sleep(self.time_to_sleep)
        self.paste_text(text['text'])
        time.sleep(0.2)
        self._press_key('esc')

    def _insert_inline_equations(self, text: TextBlock, previous_block: TextBlock):
        self._press_key('enter')
        # only add whitespace to previous text, if there is already text. Otherwise, the notion AI input will open
        if not is_text_simple_markdown_separator(previous_block['text']):
            self._press_key('space')

        self.paste_text(f"$${text['text'].strip()}$$")
        time.sleep(self.time_to_sleep)

        if not text['at_end']:
            # Inserting space to have separation to the next content
            self._press_key('space')

            # Removing the line break again with Delete
            self._press_key('delete')

        self._press_key('esc')

    def _insert_math_equation(self, text: TextBlock, previous_block: TextBlock = None):
        if is_block_equation(text):
            self._insert_block_equations(text, previous_block)
        else:
            self._insert_inline_equations(text, previous_block)

    def _go_to_next_block(self):
        # Switching to the next block
        self._press_key('down')

    def paste_text(self, text: str):
        pyperclip.copy(text)
        time.sleep(self.time_to_sleep)
        os.system("""
        osascript -e 'tell application "System Events" to keystroke "v" using {command down}'
        """)

    def get_text_to_insert(self, text_blocks: List[TextBlock]) -> str:
        # inserting dummy q for block equations, so notion will recognize it as its own block
        adjusted_text_blocks = [
            "" if block['is_enclosed'] else block['text']
            for block in text_blocks
        ]

        return "\n".join(adjusted_text_blocks)

    def insert_text_blocks_and_convert_to_math_equations(self, text_blocks: List[TextBlock]):
        input_text_str = self.get_text_to_insert(text_blocks)
        self.paste_text(input_text_str)

        time.sleep(1)
        text_blocks_to_process = [block for block in text_blocks if block['text'] != ""]

        # Moving to first cell of the inserted text
        self._press_key('enter')
        time.sleep(1)

        # Switch from text focus to block focus
        self._press_key('esc')
        skip_next = False
        previous_block = None
        is_first = True
        for text_block in text_blocks_to_process:
            if self.stop_event.is_set():
                return
            if skip_next:
                skip_next = False
                continue
            if text_block['is_enclosed']:
                self._insert_math_equation(text_block, previous_block)
                skip_next = not text_block['at_end']
            elif not is_first:
                self._press_key('down')
            previous_block = text_block
            is_first = False

        print("Inserting text has been completed.")
        print("Switching the app will close the tool.")
        self.stop_event.set()
        sys.exit(0)
