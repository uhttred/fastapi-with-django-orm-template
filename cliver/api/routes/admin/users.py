"""
Users Administration APIs
"""
import logging

from fastapi import APIRouter, Depends

from cliver.models import User
from cliver.schemas.users import UserSchema
from cliver.dependencies.auth import authenticated_user


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    '',
    response_model=list[UserSchema],
    dependencies=[Depends(authenticated_user)]
)
async def get_users():
    users: list[UserSchema] = []
    async for user in User.query.all():
        users.append(UserSchema.from_orm(user))
    return users
