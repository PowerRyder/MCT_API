
from fastapi import APIRouter
from .topup_receipt import router as topup_receipt_router
from .welcome_letter import router as welcome_letter_router
from .id_card import router as id_card_router
from .payout_statement import router as payout_statement_router

router = APIRouter(
    prefix="/docs",
    tags=["Docs"]
)

router.include_router(topup_receipt_router)
router.include_router(welcome_letter_router)
router.include_router(id_card_router)
router.include_router(payout_statement_router)