import unittest
from typing import List
from domain.text_manipulation.markdown_splitter import split_text_by_markdown_separators
from models.MarkdownSeparator import all_markdown_separators
from domain.text_manipulation.text_to_text_block_formatter import process_markdown_text_to_text_blocks
from models.TextBlock import TextBlock, SimpleTextBlock


def remove_empty_strings_from_array(arr: List[SimpleTextBlock]) -> List[SimpleTextBlock]:
    return [element for element in arr if element.text != '']


def remove_empty_textblocks_from_array(arr: List[TextBlock]) -> List[TextBlock]:
    return [element for element in arr if element.text != '']


class TestTextBlockProcessing(unittest.TestCase):

    def test_simple_list_with_equations_at_start(self):
        input_text = """
        Ein Markov-Entscheidungsprozess (MDP) \(D\) ist ein Tupel \(D = (S, A, P, R, s_0, S_t)\) mit:
        - \(S\): Menge der Zustände (Zustandsraum)
        - \(A\): Menge der Aktionen (Aktionsraum)
        line in the list 

        - \(P: (S \setminus S_t) \times A \times S [0,1]\): Transitionswahrscheinlichkeitsfunktion, wobei \(\sum_{s' \in S} P(s, a, s') = 1\) für alle \(s \in S, a \in A\)
        - \(R: (S \setminus S_t) \times A \times S \mathbb{R}\): Belohnungsfunktion
        - \(s_0 \in S\): Startzustand
        - \(S_t \subseteq S\): Menge der Zielzustände
        """

        text_blocks = split_text_by_markdown_separators(input_text, all_markdown_separators)
        result = process_markdown_text_to_text_blocks(text_blocks)

        text_blocks_count_without_whitespace = remove_empty_strings_from_array(text_blocks)
        result_without_empty_elements = remove_empty_textblocks_from_array(result)

        self.assertEqual(len(text_blocks_count_without_whitespace), 7)
        self.assertEqual(len(result_without_empty_elements), 26)

    def test_simple_list_with_header_and_numbered_list(self):
        input_text = """
        ### Iterative Bellman Update

        To compute the optimal utility, we use an iterative method.
        Including a second line of text
        1. Start with \( u_0(s) = 0 \) for all states \( s \).
        2. Calculate \( u_1(s) \) based on the Bellman equation.
        3. Repeat this process \( i \) times until the values no longer change significantly.
        This is also part of the third bullet point.
        """

        text_blocks = split_text_by_markdown_separators(input_text, all_markdown_separators)
        result = process_markdown_text_to_text_blocks(text_blocks)

        text_blocks_count_without_whitespace = remove_empty_strings_from_array(text_blocks)
        result_without_empty_elements = remove_empty_textblocks_from_array(result)

        self.assertEqual(len(text_blocks_count_without_whitespace), 5)
        self.assertEqual(len(result_without_empty_elements), 13)

        self.assertEqual(result_without_empty_elements[3].text, ' u_0(s) = 0 ')
        self.assertFalse(result_without_empty_elements[3].at_end)
        self.assertFalse(result_without_empty_elements[3].at_start)
        self.assertTrue(result_without_empty_elements[3].is_enclosed)

    def test_simple_list_with_header_and_minus_list(self):
        input_text = """
        ### Iterative Bellman Update

        To compute the optimal utility, we use an iterative method.
        Including a second line of text
        - Start with \( u_0(s) = 0 \) for all states \( s \).
          - Calculate \( u_1(s) \) based on the Bellman equation.
        - Repeat this process \( i \) times until the values no longer change significantly.
        This is part of the third bullet point.
        """

        text_blocks = split_text_by_markdown_separators(input_text, all_markdown_separators)
        result = process_markdown_text_to_text_blocks(text_blocks)

        text_blocks_count_without_whitespace = remove_empty_strings_from_array(text_blocks)
        result_without_empty_elements = remove_empty_textblocks_from_array(result)

        self.assertEqual(len(text_blocks_count_without_whitespace), 5)
        self.assertEqual(len(result_without_empty_elements), 13)

    def test_list_with_block_equation_following(self):
        input_text = """
        - \( \gamma \in [0, 1] \): Diskontierungsfaktor, der zukünftige Belohnungen abwertet.

        Die Bellmann-Gleichung wird durch iteratives Bellmann-Update approximiert:

        \[ u_{i+1}(s) := \max_{a \in A} \sum_{s' \in S} P(s, a, s') \left[ R(s, a, s') + \gamma u_i(s') \right] \]

        Mit der Initialisierung \( u_0(s) = 0 \) für alle \( s \in S \).
        """

        text_blocks = split_text_by_markdown_separators(input_text, all_markdown_separators)
        result = process_markdown_text_to_text_blocks(text_blocks)

        text_blocks_count_without_whitespace = remove_empty_strings_from_array(text_blocks)
        result_without_empty_elements = remove_empty_textblocks_from_array(result)

        self.assertEqual(len(text_blocks_count_without_whitespace), 2)
        self.assertEqual(len(result_without_empty_elements), 10)

    def test_list_with_sub_list(self):
        input_text = """
    Beispiel:
    - **Zustandsraum \( S \)**: \[ S_{vc} = \{s_{1,1}^{1}, s_{1,1}^{2}, s_{0,1}^{1}, s_{0,1}^{2}, s_{1,0}^{1}, s_{1,0}^{2}, s_{0,0}^{1}, s_{0,0}^{2}, s_t\} \]
    - **Aktionsraum \( A \)**: \[ A_{vc} = \{move, clean, charge\} \]
    - **Transitionswahrscheinlichkeiten \( P_{vc} \)**:
      - \( P(s, move, s') = 0.9 \) (90% erfolgreich)
      - \( P(s, clean, s') = 0.8 \) (80% erfolgreich)           
    
        """
        text_blocks = split_text_by_markdown_separators(input_text, all_markdown_separators)
        result = process_markdown_text_to_text_blocks(text_blocks)

        text_blocks_count_without_whitespace = remove_empty_strings_from_array(text_blocks)
        result_without_empty_elements = remove_empty_textblocks_from_array(result)

        self.assertEqual(len(text_blocks_count_without_whitespace), 6)
        self.assertEqual(len(result_without_empty_elements), 18)

    def test_with_math_code_block_and_normal_code_block(self):

        input_text = """
        In the vast realm of programming, we often encounter scenarios where we need to calculate certain values precisely. 
        For instance, the area of a circle is a common mathematical problem. The formula to calculate the area of a circle is given by:
        ```math
        A = \pi r^2
        ```
        where \( A \) represents the area, \( r \) is the radius of the circle, and \( \pi \) is a constant approximately equal to 3.14159.

        Now, let's consider a simple program in Python to compute the area of a circle given its radius:

        ```python
        import math

        def calculate_circle_area(radius):
            return math.pi * (radius ** 2)

        radius = 5
        area = calculate_circle_area(radius)
        print(f"The area of a circle with radius {radius} is {area}")
        ```

        This was a nice demonstration of \( \pi \).
        """
        text_blocks = split_text_by_markdown_separators(input_text, all_markdown_separators)
        result = process_markdown_text_to_text_blocks(text_blocks)

        text_blocks_count_without_whitespace = remove_empty_strings_from_array(text_blocks)
        result_without_empty_elements = remove_empty_textblocks_from_array(result)


        # Math Code Block
        math_code_block = result_without_empty_elements[1]
        self.assertTrue(math_code_block.is_enclosed)
        self.assertTrue(math_code_block.at_start)
        self.assertTrue(math_code_block.at_end)

        # Python Code Block
        python_code_block = result_without_empty_elements[10]
        self.assertIn('```python', python_code_block.text)

        self.assertFalse(python_code_block.is_enclosed)
        self.assertTrue(python_code_block.at_start)
        self.assertTrue(python_code_block.at_end)


    def test_wild_mix_with_markdown_separators(self):
        input_text = """
            Das ist ein Beispieltext.
    
            - This is some list element.
            - This is a sublist
     This is anew line
            # Heading 1 
            - Weitere Informationen,
            die nützlich sind.
    
            Block which should be separated
            [ ] Checkbox 1
            [ ] Checkbox 2
            extra text for second checkbox
    
            [ ] Checkbox 3
    
            - list 1
            - list 2
            extra list text
    
            New block with random text
    
    
            ```
            - list in code block
    
            - list in code block 2
            [ ] Checkbox in code block 
            def actual_code_block():
                return True
            ```
            Random Text 2 
            text with a minus - inside
            * new list 
            - list with other starter 
            * list with random text
            extra line
    
            last single block of text
    
                """

        text_blocks = split_text_by_markdown_separators(input_text, all_markdown_separators)
        text_blocks_without_whitespace = remove_empty_strings_from_array(text_blocks)

        self.assertEqual(len(text_blocks_without_whitespace), 15)


if __name__ == "__main__":
    unittest.main()
