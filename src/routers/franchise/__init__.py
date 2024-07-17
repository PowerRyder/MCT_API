
from fastapi import APIRouter
from .details import router as details_router
from .add_update_franchise import router as add_update_franchise_router
from .profile import router as profile_router
from .products import router as products_router

router = APIRouter(
    prefix="/franchise",
    tags=["Franchise"]
)

router.include_router(details_router)
router.include_router(add_update_franchise_router)
router.include_router(profile_router)
router.include_router(products_router)
