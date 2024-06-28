from src.models.TextBlock import TextBlock


def is_block_equation(text_bock: TextBlock) -> bool:
    return text_bock.is_enclosed and text_bock.at_start and text_bock.at_end