from aiogram import Router

from .main import router as main_router
from .get_statistics import router as get_statistics_router
from .message_sender import router as message_sender_router

router = Router()

router.include_router(main_router)
router.include_router(get_statistics_router)
router.include_router(message_sender_router)
