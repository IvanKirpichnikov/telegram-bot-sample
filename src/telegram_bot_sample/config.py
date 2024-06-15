import tomllib
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Final

from adaptix import loader, Retort

from telegram_bot_sample.domain.type_hints import SecurityString
from telegram_bot_sample.infrastructure.localization.entities import Language


retort: Final[Retort] = Retort(
    recipe=[
        loader(SecurityString, SecurityString),
    ]
)


class TelegramBotStorageType(Enum):
    REDIS = "redis"
    MEMORY = "memory"


@dataclass(slots=True, frozen=True)
class TelegramBotStorageConfig:
    url: str | None = field(repr=False, default=None)
    storage_type: TelegramBotStorageType = TelegramBotStorageType.MEMORY
    events_isolation_type: TelegramBotStorageType = TelegramBotStorageType.MEMORY


@dataclass(slots=True, frozen=True)
class TelegramBotOwnerConfig:
    tg_user_id: int
    tg_chat_id: int


@dataclass(slots=True, frozen=True)
class TelegramBotConfig:
    token: SecurityString = field(repr=False)
    user_name: str
    skip_updates: bool
    owner: TelegramBotOwnerConfig
    storage: TelegramBotStorageConfig


@dataclass(frozen=True, slots=True)
class PostgresqlConfig:
    url: SecurityString
    pool_size: int


@dataclass(frozen=True, slots=True)
class LocalizationConfig:
    path: Path
    default_language: Language


@dataclass(frozen=True, slots=True)
class Config:
    telegram_bot: TelegramBotConfig
    localization: LocalizationConfig
    postgresql: PostgresqlConfig


def build_config(path: Path) -> Config:
    with open(path, "rb") as file:
        raw_data = tomllib.load(file)
    return retort.load(raw_data, Config)
