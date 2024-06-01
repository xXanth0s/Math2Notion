import os
import time
from typing import List

import pyautogui
import pyperclip

from config import config
from models import TextBlock

time_to_sleep = config.TIME_TO_SLEEP

def copy_text():
    time.sleep(time_to_sleep)

    os.system("""
    osascript -e 'tell application "System Events" to keystroke "c" using {command down}'
    """)

    time.sleep(time_to_sleep)

    return pyperclip.paste()

def paste_text(text: str):
    pyperclip.copy(text)
    time.sleep(time_to_sleep)
    os.system("""
    osascript -e 'tell application "System Events" to keystroke "v" using {command down}'
    """)

def press_hotkeys(keys: List[str]):
    pyautogui.hotkey(*keys, interval=0.02)
    time.sleep(time_to_sleep)

def press_key(key: str):
    pyautogui.press(key)
    time.sleep(time_to_sleep)

def move_to_end_of_cell():
    press_hotkeys(['command', 'a'])
    press_key('right')

def insert_math_equation(text: TextBlock):
    press_key('enter')

    # Selecting all text with Cmd+A
    press_hotkeys(['command', 'a'])

    # Transforming selection to mathe equations
    press_hotkeys(['command', 'shift', 'e'])

    # Approve math equation
    press_key('enter')

    if not text['at_start']:
        # Switching to the upper cell with Up Arrow key
        press_key('up')

        # Moving to the end of the cell
        move_to_end_of_cell()

        # Removing the line break with Delete
        press_key('delete')

        # Inserting a space to have sepeartion to math equation
        press_key('space')

    if not text['at_end']:
        # Moving to the end of the cell
        move_to_end_of_cell()

        # Inserting space to have separation to the next content
        press_key('space')

        # Removing the line break again with Delete
        press_key('delete')

    # Switch from text focus to block focus
    press_key('esc')

def go_to_next_block():
    # Switching to the next block
    press_key('down')

def insert_text_blocks_and_convert_to_math_equations(text_blocks: List[TextBlock]):
    input_text_str = "\n".join([block["text"] for block in text_blocks])
    paste_text(input_text_str)

    text_blocks_to_process = [block for block in text_blocks if block['text'] != ""]

    # Moving to first cell of the inserted text
    press_key('enter')

    # Switch from text focus to block focus
    press_key('esc')
    skip_next = False
    for text_block in text_blocks_to_process:
        if skip_next:
            skip_next = False
            continue
        if text_block['is_enclosed']:
            insert_math_equation(text_block)
            skip_next = not text_block['at_end']
        press_key('down')
