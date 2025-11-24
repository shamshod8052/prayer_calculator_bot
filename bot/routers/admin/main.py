from aiogram import types, Router
from aiogram.filters import Command

from bot.filters.admin_filter import AdminFilter

router = Router(name=__name__)


@router.message(AdminFilter(), Command("admin"))
async def admin_commands(message: types.Message):
    commands = (
        f"Available commands:\n\n"
        f"/statistics - Bot statistics list\n"
        f"/send_message - Send message for users"
    )

    await message.answer(commands)


@router.message(Command("admin"))
async def admin_commands(message: types.Message):
    commands = "Afsus, siz admin emassiz!"

    await message.answer(commands)
