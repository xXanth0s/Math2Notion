# This is a sample Python script.
from format_text import process_markdown_input
from switch_to_notion import prompt_user_to_switch_to_notion

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_text = process_markdown_input()
    input_text_str = "\n".join([block["text"] for block in input_text])
    print("The processed text blocks are:")
    print(input_text_str)
    prompt_user_to_switch_to_notion()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
