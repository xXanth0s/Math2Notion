import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    TIME_TO_SLEEP: float
    COUNTDOWN_LENGTH: int
    INLINE_MATHE_EQUATION_SEPARATOR_START: str
    INLINE_MATHE_EQUATION_SEPARATOR_END: str
    BLOCK_MATHE_EQUATION_SEPARATOR_START: str
    BLOCK_MATHE_EQUATION_SEPARATOR_END: str

    def __init__(self):
        self.TIME_TO_SLEEP = float(os.getenv('TIME_TO_SLEEP', 0.02))
        self.COUNTDOWN_LENGTH = int(os.getenv('COUNTDOWN_LENGTH', 5))
        self.INLINE_MATHE_EQUATION_SEPARATOR_START = os.getenv('INLINE_MATHE_EQUATION_SEPARATOR_START', '\\(')
        self.INLINE_MATHE_EQUATION_SEPARATOR_END = os.getenv('INLINE_MATHE_EQUATION_SEPARATOR_END', '\\)')
        self.BLOCK_MATHE_EQUATION_SEPARATOR_START = os.getenv('BLOCK_MATHE_EQUATION_SEPARATOR_START', '\\[')
        self.BLOCK_MATHE_EQUATION_SEPARATOR_END = os.getenv('BLOCK_MATHE_EQUATION_SEPARATOR_END', '\\]')

# Create an instance of the Config class to use across the project
config = Config()
