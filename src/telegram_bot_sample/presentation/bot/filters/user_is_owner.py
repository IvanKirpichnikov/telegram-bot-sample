from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject, User
from dishka import FromDishka

from telegram_bot_sample.application.interactors.user.check_user_is_owner import CheckUserIsOwnerInteractor
from telegram_bot_sample.infrastructure.dishka.injects import inject


class UserIsOwnerFilter(BaseFilter):
    @inject.aiogram.filter
    async def __call__(
        self,
        event: TelegramObject,
        check_user_is_owner: FromDishka[CheckUserIsOwnerInteractor],
        event_from_user: User | None = None,
    ) -> bool:
        if event_from_user:
            return await check_user_is_owner.execute(
                data=event_from_user.id,
            )
        return False
