from dataclasses import dataclass
from logging import getLogger

from telegram_bot_sample.application.interfaces.command import Command
from telegram_bot_sample.config import TelegramBotConfig


@dataclass(slots=True, frozen=True, kw_only=True)
class CheckUserIsOwnerInteractor(Command[int, bool]):
    logger = getLogger(name=__name__)
    
    config: TelegramBotConfig
    
    async def execute(self, data: int) -> bool:
        result = self.config.owner.tg_user_id == data
        self.logger.debug(
            "Check user is owner. User tg id %r. Result %r" % (data, result)
        )
        return result
