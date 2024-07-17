
from fastapi import APIRouter
from .pin import router as pin_details_router
from .generate import router as generate_router
from .partial_pin import router as partial_pin_router
from .transfer import router as transfer_router
from .pin_request import router as pin_request_router
from .pin_product_dispatch import router as pin_product_dispatch_router

router = APIRouter(prefix="/pin", tags=["Pin"])

router.include_router(pin_details_router)
router.include_router(generate_router)
router.include_router(partial_pin_router)
router.include_router(transfer_router)
router.include_router(pin_request_router)
router.include_router(pin_product_dispatch_router)