# Math2Notion

This application allows you to insert Markdown text containing mathematical formulas into Notion so that they are displayed correctly in Notion.
The text is formatted accordingly, pasted into Notion and then automatically adapted in Notion itself using a shortcut. 
This tool is particularly useful when copying output from ChatGPT to Notion.

## Usage
### Mac
Go to the [latest release](https://github.com/xXanth0s/Math2Notion/releases/tag/v0.0.1) and download the executable for normal Markdown or ChatGPT output.
Start the executable, a console window will open and ask for the markdown text containing the mathematical formulas.
Add `END` at the end of the text to indicate that the text is complete and approve with `enter`.
After the text was passed, the programm waits, till the user switches to the notion app.
When the user has switched to the notion app, the programm will start a countdown.
After the countdown, the programm will insert a preformatted text and manipulate the text in notion to display the mathematical formulas correctly.
The user should not interact with the computer till the programm has finished.

### Windows
No support for Windows yet.

# Development

## Installation

Ensure that you have Python 3.9 and pip installed on your system.

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install the required packages with pipenv:

```bash
pip install pipenv
pipenv install
```

## Configuration

To customize the behavior of the application, you can set various environment variables in a `.env` file. Below is a list of the available variables and their descriptions.

### Environment Variables

- `TIME_TO_SLEEP` (float): The time in seconds to wait between keyboard inputs. Default is `0.02`.
- `COUNTDOWN_LENGTH` (int): The length of countdown in seconds, after the user has switched to notion and the programm will insert and manipulate the text. Default is `5`.

### Markdown 

These variables define the separators for inline and block mathematical equations:

- `INLINE_MATHE_EQUATION_SEPARATOR_START` (string): The starting delimiter for inline math equations. Default is `\(` for ChatGPT output. Markdown uses `$`.
- `INLINE_MATHE_EQUATION_SEPARATOR_END` (string): The ending delimiter for inline math equations. Default is `\)` for ChatGPT output. Markdown uses `$`.
- `BLOCK_MATHE_EQUATION_SEPARATOR_START` (string): The starting delimiter for block math equations. Default is `\[` for ChatGPT output. Markdown uses `$$`.
- `BLOCK_MATHE_EQUATION_SEPARATOR_END` (string): The ending delimiter for block math equations. Default is `\]` for ChatGPT output. Markdown uses `$`.

### Example

```bash
TIME_TO_SLEEP=0.02
COUNTDOWN_LENGTH=5

## ChatGPT
# INLINE_MATHE_EQUATION_SEPARATOR_START=\(
# INLINE_MATHE_EQUATION_SEPARATOR_END=\)
# BLOCK_MATHE_EQUATION_SEPARATOR_START=\[
# BLOCK_MATHE_EQUATION_SEPARATOR_END=\]

## Markdown
INLINE_MATHE_EQUATION_SEPARATOR_START=$
INLINE_MATHE_EQUATION_SEPARATOR_END=$
BLOCK_MATHE_EQUATION_SEPARATOR_START=$$
BLOCK_MATHE_EQUATION_SEPARATOR_END=$$
```



## Build

To make a new build, execute the following commands in the project directory:

```bash
cd src
pyinstaller --onefile main.py
```