from aiogram import Router

from .set_main_menu import router as set_main_menu_router
from .admin import router as admin_router

router = Router()

router.include_router(set_main_menu_router)
router.include_router(admin_router)
