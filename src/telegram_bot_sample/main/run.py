from logging import getLogger
from typing import cast

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.base import BaseStorage, DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand, ErrorEvent
from aiogram_dialog import DialogManager, setup_dialogs, ShowMode, StartMode
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from dishka import AsyncContainer
from dishka.integrations.aiogram import AutoInjectMiddleware
from redis.asyncio import Redis

from telegram_bot_sample.config import Config, TelegramBotStorageConfig, TelegramBotStorageType
from telegram_bot_sample.domain.type_hints import SecurityString
from telegram_bot_sample.infrastructure.aiogram.storage import BaseStorageProtocol, MemoryStorage
from telegram_bot_sample.infrastructure.localization.storage import LocalizationStorage
from telegram_bot_sample.main.build_container import build_container
from telegram_bot_sample.presentation.bot.middlewares.container import ContainerMiddleware
from telegram_bot_sample.presentation.bot.presenters.main import setup_routers
from telegram_bot_sample.presentation.bot.states import MainMenuStatesGroup


logger = getLogger(name=__name__)


async def on_error(
    event: ErrorEvent,
    dialog_manager: DialogManager,
) -> None:
    logger.error("Error: %s", event.exception)
    await dialog_manager.start(
        mode=StartMode.RESET_STACK,
        state=MainMenuStatesGroup.user,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        commands=[
            BotCommand(
                command="/start",
                description="Старт/перезагрузка бота",
            ),
        ]
    )


def create_telegram_bot(*, token: SecurityString) -> Bot:
    logger.debug("Create aiogram bot")
    return Bot(
        token=token.security(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )


def create_storage(
    *,
    config: TelegramBotStorageConfig,
) -> BaseStorageProtocol:
    if config.storage_type == TelegramBotStorageType.REDIS:
        if config.url is None:
            raise ValueError
        
        return RedisStorage(
            redis=Redis.from_url(url=config.url),
            key_builder=DefaultKeyBuilder(
                with_bot_id=True,
                with_destiny=True,
            ),
        )
    elif config.storage_type == TelegramBotStorageType.MEMORY:
        return MemoryStorage()
    else:
        raise ValueError("Unknown storage type %r" % config.storage_type)


def setup_middleware(
    *,
    dispatcher: Dispatcher,
    container: AsyncContainer,
) -> None:
    container_middleware = ContainerMiddleware(container=container)
    autoinject_middleware = AutoInjectMiddleware()
    
    dispatcher.update.outer_middleware(middleware=container_middleware)
    
    for update in dispatcher.resolve_used_update_types():
        if update != "update":
            dispatcher.observers[update].middleware(middleware=autoinject_middleware)


def create_disp(
    *,
    container: AsyncContainer,
    storage_config: TelegramBotStorageConfig,
) -> Dispatcher:
    storage = create_storage(config=storage_config)
    dispatcher = Dispatcher(
        name=__name__,
        storage=cast(BaseStorage, storage),
        events_isolation=storage.create_isolation(),
    )
    dispatcher.errors.register(
        on_error,
        ExceptionTypeFilter(UnknownIntent, UnknownState),
    )
    setup_middleware(
        container=container,
        dispatcher=dispatcher,
    )
    setup_routers(dispatcher)
    dispatcher["bg_manager_factory"] = setup_dialogs(router=dispatcher)
    
    return dispatcher


async def run_telegram_bot(
    config: Config,
    localization_storage: LocalizationStorage
) -> None:
    async with build_container(
        config=config,
        localization_storage=localization_storage,
    ) as container:
        disp = create_disp(
            container=container,
            storage_config=config.telegram_bot.storage,
        )
        bot = create_telegram_bot(token=config.telegram_bot.token)
        await set_commands(bot)
        allowed_updates = disp.resolve_used_update_types()
        if config.telegram_bot.skip_updates:
            await bot.delete_webhook(True)
        
        logger.info("Run telegram bot. Allowed updates %r" % allowed_updates)
        await disp.start_polling(bot, allowed_updates=allowed_updates)
