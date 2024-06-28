import unittest

from src.utils.text_utils import count_leading_spaces


class TestCountLeadingSpaces(unittest.TestCase):
    def test_leading_spaces(self):
        input_text = "    Example text"
        result = count_leading_spaces(input_text)
        self.assertEqual(result, 4)

    def test_no_leading_spaces(self):
        input_text = "Example text"
        result = count_leading_spaces(input_text)
        self.assertEqual(result, 0)

    def test_all_spaces(self):
        input_text = "    "
        result = count_leading_spaces(input_text)
        self.assertEqual(result, 4)

    def test_spaces_and_tabs(self):
        input_text = "    \tExample text"
        result = count_leading_spaces(input_text)
        self.assertEqual(result, 4)

    def test_no_spaces(self):
        input_text = "NoLeadingSpaces"
        result = count_leading_spaces(input_text)
        self.assertEqual(result, 0)

    def test_empty_string(self):
        input_text = ""
        result = count_leading_spaces(input_text)
        self.assertEqual(result, 0)

    def test_spaces_before_newline(self):
        input_text = "    \nExample text"
        result = count_leading_spaces(input_text)
        self.assertEqual(result, 4)