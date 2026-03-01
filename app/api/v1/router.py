from fastapi import APIRouter
from .endpoints import users, bills

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(bills.router, prefix="/bills", tags=["bills"])
