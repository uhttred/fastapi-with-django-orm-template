from fastapi import APIRouter

from . import users


router = APIRouter()

router.include_router(users.router, prefix='/users', tags=['users'])
