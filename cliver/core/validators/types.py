from datetime import datetime
from typing import (
    Annotated,
    TypedDict,
    Literal,
    TypeVar
)
from pydantic import BeforeValidator

from .utils import (
    get_splited_comma_string_list_or_asterisk
)


T = TypeVar('T')

ListCommaStringOrAsterisk = Annotated[
    T | Literal['*'],
    BeforeValidator(get_splited_comma_string_list_or_asterisk)
]


class JWTPayload(TypedDict):
    sub: str
    exp: datetime
    type: Literal['access', 'confirmation']


class DecodedJWTPayload(TypedDict):
    sub: str
    exp: str
    type: Literal['access', 'confirmation']
