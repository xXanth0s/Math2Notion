import os
import time
from typing import List
import pyautogui
import pyperclip
from threading import Event
from config import config
from models import TextBlock


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

    def _paste_text(self, text: str):
        pyperclip.copy(text)
        time.sleep(self.time_to_sleep)
        os.system("""
        osascript -e 'tell application "System Events" to keystroke "v" using {command down}'
        """)

    def _press_hotkeys(self, keys: List[str]):
        pyautogui.hotkey(*keys, interval=0.02)
        time.sleep(self.time_to_sleep)

    def _press_key(self, key: str):
        pyautogui.press(key)
        time.sleep(self.time_to_sleep)

    def _move_to_end_of_cell(self):
        self._press_hotkeys(['command', 'a'])
        self._press_key('right')

    def _insert_math_equation(self, text: TextBlock, previous_Block: TextBlock = None):
        self._press_key('enter')

        # Selecting all text with Cmd+A
        self._press_hotkeys(['command', 'a'])

        # Transforming selection to math equations
        self._press_hotkeys(['command', 'shift', 'e'])

        # Approve math equation
        self._press_key('enter')

        add_space = False
        if not text['at_start'] and previous_Block:
            # Switching to the upper cell with Up Arrow key
            self._press_key('up')

            if previous_Block['at_start'] and len(previous_Block['text']) <= 20:
                # Moving to the end of the cell with shortcut for small cells, which are not just a new list
                if previous_Block['text'].strip() != '-':
                    self._press_key('right')
                    add_space = True
            else:
                # Moving to the end of the cell
                self._move_to_end_of_cell()
                add_space = True
            # Removing the line break with Delete
            self._press_key('delete')

            if add_space:
                # Inserting a space to have separation to math equation
                self._press_key('space')

        if not text['at_end']:
            # Moving to the end of the cell
            self._move_to_end_of_cell()

            # Inserting space to have separation to the next content
            self._press_key('space')

            # Removing the line break again with Delete
            self._press_key('delete')

        # Switch from text focus to block focus
        self._press_key('esc')

    def _go_to_next_block(self):
        # Switching to the next block
        self._press_key('down')

    def insert_text_blocks_and_convert_to_math_equations(self, text_blocks: List[TextBlock]):
        input_text_str = "\n".join([block["text"] for block in text_blocks])
        print(f"Inserting text: {input_text_str}")
        self._paste_text(input_text_str)

        time.sleep(1)
        text_blocks_to_process = [block for block in text_blocks if block['text'] != ""]

        # Moving to first cell of the inserted text
        self._press_key('enter')
        time.sleep(1)

        # Switch from text focus to block focus
        self._press_key('esc')
        skip_next = False
        previous_block = None
        for text_block in text_blocks_to_process:
            if self.stop_event.is_set():
                return
            if skip_next:
                skip_next = False
                continue
            if text_block['is_enclosed']:
                self._insert_math_equation(text_block, previous_block)
                skip_next = not text_block['at_end']
            self._press_key('down')
            previous_block = text_block
