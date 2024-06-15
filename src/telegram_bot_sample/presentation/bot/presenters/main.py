from aiogram import Dispatcher
from aiogram.filters import CommandStart

from telegram_bot_sample.presentation.bot.presenters import main_menu
from telegram_bot_sample.presentation.bot.presenters.admin.main import build_admin_router
from telegram_bot_sample.presentation.bot.presenters.user.main import build_user_router


def setup_routers(dispatcher: Dispatcher) -> None:
    dispatcher.message(CommandStart())(main_menu.start_handler)
    dispatcher.include_routers(
        main_menu.dialog,
    )
    dispatcher.include_routers(
        build_user_router(),
        build_admin_router(),
    )
