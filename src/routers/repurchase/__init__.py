
from fastapi import APIRouter
from .categories import router as categories_router
from .products import router as products_router
from .product_stocks import router as product_stocks_router
from .orders import router as orders_router

router = APIRouter(
    prefix="/repurchase",
    tags=["Repurchase"]
)

router.include_router(categories_router)
router.include_router(products_router)
router.include_router(product_stocks_router)
router.include_router(orders_router)
