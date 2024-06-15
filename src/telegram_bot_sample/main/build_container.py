from contextlib import asynccontextmanager
from typing import AsyncIterator

from dishka import AsyncContainer, make_async_container

from telegram_bot_sample.config import Config
from telegram_bot_sample.infrastructure.localization.storage import LocalizationStorage
from telegram_bot_sample.main.providers.config import ConfigProvider
from telegram_bot_sample.main.providers.interactor import InteractorProvider


@asynccontextmanager
async def build_container(
    config: Config,
    localization_storage: LocalizationStorage,
) -> AsyncIterator[AsyncContainer]:
    container = make_async_container(
        ConfigProvider(),
        InteractorProvider(),
        context={
            Config: config,
            LocalizationStorage: localization_storage,
        },
    )
    try:
        yield container
    finally:
        await container.close()
