
from fastapi import APIRouter
from .referral import router as referral_router
from .level import router as level_router
from .roi import router as roi_router
from .spill import router as spill_router
from .single_leg import router as single_leg_router
from .matrix import router as matrix_router
from .matching import router as matching_router
from .withdrawal_level import router as withdrawal_level_router
from .repurchase_level import router as repurchase_level_router
from .weekly_bonus import router as weekly_bonus_router
from .rank_and_reward import router as rank_and_reward_router
from .monthly_bonus import router as monthly_bonus_router
from .total import router as total_router

router = APIRouter(
    prefix="/income",
    tags=["Income"]
)

router.include_router(referral_router)
router.include_router(level_router)
router.include_router(roi_router)
router.include_router(spill_router)
router.include_router(single_leg_router)
router.include_router(matrix_router)
router.include_router(matching_router)
router.include_router(total_router)
router.include_router(withdrawal_level_router)
router.include_router(repurchase_level_router)
router.include_router(weekly_bonus_router)
router.include_router(rank_and_reward_router)
router.include_router(monthly_bonus_router)
