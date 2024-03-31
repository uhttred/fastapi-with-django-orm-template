from typing import Annotated

from fastapi import Request, Depends
from fastapi.exceptions import HTTPException
from fastapi import status

from jose.exceptions import ExpiredSignatureError, JWTError

from cliver.core.security import validate_jwt
from cliver.core.validators.types import DecodedJWTPayload
from cliver.models import User


async def is_authenticated(request: Request) -> DecodedJWTPayload:
    if token := request.headers.get('Authorization'):
        token = token.split(' ')[1]
        try:
            payload: DecodedJWTPayload = validate_jwt(token)
        except ExpiredSignatureError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Provided authorization token has expired')
        except JWTError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Ivalid token')
        if payload['type'] == 'access':
            return payload
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Invalid token type for this scope')
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Authorization details not provided')


async def authenticated_user(payload: Annotated[DecodedJWTPayload, Depends(is_authenticated)]) -> User:
    try:
        user = await User.query.aget(uid=payload['sub'])
    except User.DoesNotExist:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Authenticated user account not found')
    return user


AuthenticatedUser = Annotated[User, Depends(authenticated_user)]
