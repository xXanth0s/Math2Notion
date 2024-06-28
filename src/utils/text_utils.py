def count_leading_spaces(string: str) -> int:
    leading_spaces = 0
    for char in string:
        if char == ' ':
            leading_spaces += 1
        else:
            break
    return leading_spaces
