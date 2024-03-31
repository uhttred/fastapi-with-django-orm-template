from fastapi import APIRouter

from .routes import auth, admin


router = APIRouter()

router.include_router(auth.router, prefix='/auth', tags=['authentication'])
router.include_router(admin.router, prefix='/admin', tags=['administration'])
