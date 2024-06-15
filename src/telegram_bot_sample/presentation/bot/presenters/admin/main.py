from aiogram import Router

from telegram_bot_sample.presentation.bot.filters.user_is_owner import UserIsOwnerFilter


def build_admin_router() -> Router:
    router = Router()
    
    router.message.filter(UserIsOwnerFilter())
    router.callback_query.filter(UserIsOwnerFilter())
    
    return router
