from typing import Literal


def get_splited_comma_string_list_or_asterisk(string: str) -> list[str] | Literal['*']:
    if string != '*':
        return [part.strip() for part in string.split(',') if part]
    return '*'
