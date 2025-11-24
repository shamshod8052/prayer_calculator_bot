from aiogram import Router

from .set_main_menu import router as set_main_menu_router
from .admin import router as admin_router
from .start import router as start_router
from .first_start import router as first_start_router
from .about_bot import router as about_bot_router
from .faq import router as faq_router
from .prayer_times import router as prayer_times_router
from .qada_adder import router as qada_adder_router

router = Router()

router.include_router(set_main_menu_router)
router.include_router(start_router)
router.include_router(first_start_router)
router.include_router(about_bot_router)
router.include_router(faq_router)
router.include_router(prayer_times_router)
router.include_router(qada_adder_router)
router.include_router(admin_router)
