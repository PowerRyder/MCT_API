
from fastapi import APIRouter
from .withdrawal import router as withdrawal_router
from .crypto_withdrawal import router as crypto_withdrawal_router

router = APIRouter(
    prefix="/withdrawal",
    tags=["Withdrawal"]
)

router.include_router(withdrawal_router)
router.include_router(crypto_withdrawal_router)
