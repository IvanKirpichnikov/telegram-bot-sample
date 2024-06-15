from typing import Any

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Const, Text
from dishka import FromDishka

from telegram_bot_sample.infrastructure.dishka.injects import inject
from telegram_bot_sample.infrastructure.localization.storage import Localization


class LocalizationText(Text):
    __slots__ = ["key"]
    
    def __init__(
        self,
        key: str | Text,
        when: WhenCondition = None,
    ) -> None:
        super().__init__(when)
        self.key = Const(key) if isinstance(key, str) else key
    
    @inject.aiogd.render_text
    async def _render_text(  # type: ignore[override]
        self,
        data: dict[str, Any],
        manager: DialogManager,
        localization: FromDishka[Localization],
    ) -> str:
        key = await self.key.render_text(data, manager)
        localization_data = data.get("localization")
        if localization_data:
            return localization(key, **localization_data)
        return localization(key)
