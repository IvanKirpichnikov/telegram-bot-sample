from typing import Any, Awaitable, Callable, cast

from aiogram import BaseMiddleware, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Chat, TelegramObject, User
from aiogram_dialog import BgManagerFactory
from dishka.async_container import AsyncContainer

from telegram_bot_sample.infrastructure.localization.storage import Localization, LocalizationStorage


def make_context(data: dict[str, Any]) -> dict[Any, Any]:
    context = {
        Bot: data.get("bot"),
        TelegramObject: data.get("event"),
        Chat: data.get("event_chat"),
        FSMContext: data.get("state"),
        User: data.get("event_from_user"),
        BgManagerFactory: data.get("bg_manager_factory"),
    }
    return {key: value for key, value in context.items() if value is not True}


class ContainerMiddleware(BaseMiddleware):
    def __init__(self, container: AsyncContainer):
        self._container = container
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        context = make_context(data)
        if User in context:
            localization_storage = cast(
                LocalizationStorage,
                await self._container.get(LocalizationStorage),
            )
            context[Localization] = localization_storage.get_locale(
                context[User].language_code,
            )
        
        async with self._container(context=context) as container:
            data["dishka_container"] = container
            return await handler(event, data)
