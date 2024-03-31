from fastapi import status
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from cliver.models import User
from cliver.schemas.users import UserSchema
from cliver.schemas.auth import AuthenticationSchema
from cliver.core.security import create_access_token
from cliver.dependencies.auth import AuthenticatedUser


router = APIRouter()


@router.get('/user', response_model=UserSchema)
async def get_authenticated_user(user: AuthenticatedUser):
    return user


@router.post('/token')
async def authenticate_user(body: AuthenticationSchema):

    user = await User.query.get_by_email(body.email)

    if user and user.check_password(body.password):
        if user.is_active:
            access_token = create_access_token(user.uid.__str__())
            return {'token_access': access_token, 'token_type': 'Bearer'}
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Your account is disabled, please contact support!'
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Invalid user or password'
    )
