
from fastapi import APIRouter
from .paid_payment import router as paid_payment_router

router = APIRouter(
    prefix="/investment",
    tags=["Investment"]
)

router.include_router(paid_payment_router)