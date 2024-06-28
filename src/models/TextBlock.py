
class SimpleTextBlock:
    def __init__(self, text: str, skip: bool, indentations_count: int = 0) -> None:
        self.text = text
        self.skip = skip
        self.indentations_count = indentations_count
    def __str__(self) -> str:
        return f"text='{self.text}', skip={self.skip}, indentations_count={self.indentations_count}"


class TextBlock(SimpleTextBlock):
    def __init__(self, text: str, at_start: bool, is_enclosed: bool, skip: bool, at_end: bool,
                 indentations_count: int = 0) -> None:
        super().__init__(text, skip, indentations_count)
        self.at_start = at_start
        self.is_enclosed = is_enclosed
        self.at_end = at_end

    def __str__(self) -> str:
        return (f"text='{self.text}', at_start={self.at_start}, is_enclosed={self.is_enclosed}, "
                f"skip={self.skip}, at_end={self.at_end}, indentations_count={self.indentations_count}")

