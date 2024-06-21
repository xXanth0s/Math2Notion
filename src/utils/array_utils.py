from typing import TypeVar, List

T = TypeVar('T')

def insert_between_elements_to_array(array: List[T], element: T) -> List[T]:
    if not array:
        return []
    result = [array[0]]
    for item in array[1:]:
        result.append(element)
        result.append(item)
    return result