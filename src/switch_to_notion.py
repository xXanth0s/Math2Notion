import os
import time
import pygetwindow as gw
from dotenv import load_dotenv

load_dotenv()
countdownLength = int(os.getenv('COUNTDOWN_LENGTH', '5'))


def prompt_user_to_switch_to_notion(text_to_show_after_switch: str = 'Countdown starting...'):
    print("Please switch to the 'Notion' application.")

    # Wait for the user to switch to Notion
    notion_found = False
    while not notion_found:
        # Check the active window title
        active_window_title = gw.getActiveWindow()
        if active_window_title and "Notion" in active_window_title:
            notion_found = True
        else:
            print("Waiting for the user to switch to Notion...")
            time.sleep(1)

    print(text_to_show_after_switch)
    for i in range(countdownLength, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    print("Countdown complete.")
