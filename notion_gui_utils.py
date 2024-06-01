from typing import List

import os
import pyautogui
import pyperclip
import time

time_to_sleep = 0.02


def copy_text():

    time.sleep(time_to_sleep)
    print('Kopiere den Text mit Cmd+C')

    os.system("""
    osascript -e 'tell application "System Events" to keystroke "c" using {command down}'
    """)

    time.sleep(time_to_sleep)
    clipboard_content = pyperclip.paste()
    print('Clipboard Inhalt:', clipboard_content)
    return pyperclip.paste()


def press_hotkeys(keys: List[str]):
    print('pressing hot keys:', keys)
    pyautogui.hotkey(*keys, interval=0.02)
    time.sleep(time_to_sleep)


def press_key(key: str):
    print('pressing keys:', key)
    pyautogui.press(key)
    time.sleep(time_to_sleep)

def move_to_end_of_cell():
    press_hotkeys(['command', 'a'])
    press_key('right')

def insert_math_equation(text: str):
    had_new_line_beginning = text.startswith('$$')
    had_new_line_end = text.endswith('$$')
    if had_new_line_beginning:
        press_hotkeys(['command', 'a'])
        press_key('left')
        press_key('delete')

    if had_new_line_end:
        press_hotkeys(['command', 'a'])
        press_key('right')
        press_key('backspace')


    print('Markiere den gesamten Text mit Cmd+A')
    press_hotkeys(['command', 'a'])

    print('Führe Cmd+Shift+E aus')
    press_hotkeys(['command', 'shift', 'e'])

    print('Drücke Enter')
    press_key('enter')

    if not had_new_line_beginning:
        print('Wechsle zur oberen Zelle mit Pfeiltaste nach oben')
        press_key('up')

        print('Wechsle zum Ende der Zelle')
        move_to_end_of_cell()

        print('Entferne den Zeilenumbruch mit Entf')
        press_key('delete')

        print('Füge ein Leerzeichen ein')
        press_key('space')

    if not had_new_line_end:
        print('Wechsle erneut zum Ende der Zelle mit Cmd+Pfeil nach rechts')
        press_hotkeys(['command', 'right'])

        print('Füge erneut ein Leerzeichen ein')
        press_key('space')

        print('Entferne erneut den Zeilenumbruch mit Entf')
        press_key('delete')


def go_to_next_block():
    print('Wechsle zum nächsten block')
    # press_hotkeys(['command', 'a'])
    press_key('down')


def test():
    print('Warte 5 Sekunden, um Zeit zu geben, zu Notion zu wechseln')
    time.sleep(5)
    print('Hole den kopierten Text aus der Zwischenablage')
    copied_text = copy_text()

    go_to_next_block()

    print('Hole den kopierten Text aus der Zwischenablage')
    copied_text2 = copy_text()

    print('Der kopierte Text lautet:', copied_text)
    print('Der 2. kopierte Text lautet:', copied_text2)


def main():
    print('Warte 5 Sekunden, um Zeit zu geben, zu Notion zu wechseln')
    time.sleep(5)

    seen_texts = set()
    previous_text = ""

    while True:
        print('Hole den kopierten Text aus der Zwischenablage')
        copied_text = copy_text()

        print('Der kopierte Text lautet:', copied_text)

        print('Überprüfe, ob der Text bereits der vorherige Text war ')
        if copied_text == previous_text:
            break
        seen_texts.add(copied_text)

        print('Überprüfe, ob de Text mit $$ oder $ anfängt und aufhört')
        if copied_text and copied_text.startswith('$') and copied_text.endswith('$'):
            print('Der Text ist eine Mathematik-Gleichung')
            insert_math_equation(copied_text)


        print('Wechsle zum nächsten block')
        press_hotkeys(['command', 'a'])
        press_key('down')

        previous_text = copied_text


if __name__ == "__main__":
    main()
    # test()
    # press_hotkeys(['command', 'a'])
    # press_hotkeys(['command', 'a'])
