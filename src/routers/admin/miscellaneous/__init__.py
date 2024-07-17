
from fastapi import APIRouter
from .virtual_business import router as virtual_business_router
from .roi_percentage import router as roi_percentage_router
from .trading import router as trading_router

router = APIRouter(
    prefix="/misc",
    tags=["Misc Settings"]
)

router.include_router(virtual_business_router)
router.include_router(roi_percentage_router)
router.include_router(trading_router)
