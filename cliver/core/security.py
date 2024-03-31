import logging

from typing import Literal
from datetime import datetime, UTC, timedelta

from argon2 import PasswordHasher
from jose import jwt

from cliver.core.validators.types import JWTPayload, DecodedJWTPayload
from cliver.settings import config


logger = logging.getLogger(__name__)

ALGORITHM = 'HS512'

ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(hash: str, password: str) -> bool:
    return ph.verify(hash=hash, password=password)


def create_jwt(
        uid: str,
        minutes: int = 30,
        token_type: Literal[
            'access',
            'confirmation'
        ] = 'access'
    ) -> str:

    expire_at = datetime.now(UTC) + timedelta(minutes=minutes)

    payload: JWTPayload = {
        'sub': uid,
        'exp': expire_at,
        'type': token_type
    }

    return jwt.encode(claims=payload, key=config.SECRET_KEY, algorithm=ALGORITHM) # type: ignore


def validate_jwt(token: str) -> DecodedJWTPayload:
    return jwt.decode(token, key=config.SECRET_KEY, algorithms=ALGORITHM) # type: ignore


def create_access_token(uid: str) -> str:
    return create_jwt(uid)
