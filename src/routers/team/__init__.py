
from fastapi import APIRouter
from .team import router as team
from .tree import router as tree
from .matrix import router as matrix

router = APIRouter(
    prefix="/team_details"
)

router.include_router(team)
router.include_router(tree)
router.include_router(matrix)