from typing import Any

from aiogram import F
from aiogram.types import CallbackQuery, Message, User
from aiogram_dialog import Dialog, DialogManager, ShowMode, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from dishka import FromDishka

from telegram_bot_sample.application.interactors.user.check_user_is_owner import CheckUserIsOwnerInteractor
from telegram_bot_sample.infrastructure.aiogram_dialog.widgets.localization import LocalizationText
from telegram_bot_sample.infrastructure.dishka.injects import inject
from telegram_bot_sample.presentation.bot.states import MainMenuStatesGroup


@inject.aiogd.on_click
async def check_user_is_owner(
    event: CallbackQuery,
    widget: Button,
    manager: DialogManager,
    interactor: FromDishka[CheckUserIsOwnerInteractor],
) -> None:
    result = await interactor.execute(
        data=event.from_user.id,
    )
    if result:
        await manager.switch_to(
            show_mode=ShowMode.EDIT,
            state=MainMenuStatesGroup.admin,
        )


@inject.aiogd.getter
async def user_window_getter(
    user: FromDishka[User],
    dialog_manager: DialogManager,
    interactor: FromDishka[CheckUserIsOwnerInteractor],
    **kwargs: Any,
) -> dict[str, Any]:
    return dict(
        user_is_admin=await interactor.execute(
            data=user.id,
        ),
    )


async def admin_window_getter(
    **kwargs: Any,
) -> dict[str, Any]:
    return dict()


dialog = Dialog(
    Window(
        LocalizationText("user-main-menu"),
        Button(
            LocalizationText("admin-menu"),
            id="admin_menu",
            when=F["user_is_admin"],
            on_click=check_user_is_owner,
        ),
        getter=user_window_getter,
        state=MainMenuStatesGroup.user,
    ),
    Window(
        LocalizationText("admin-main-menu"),
        SwitchTo(
            LocalizationText("back-to-user-menu"),
            id="back_to_user_menu",
            show_mode=ShowMode.EDIT,
            state=MainMenuStatesGroup.user,
        ),
        getter=admin_window_getter,
        state=MainMenuStatesGroup.admin,
    ),
)


async def start_main_menu_dialog(manager: DialogManager) -> None:
    await manager.start(
        mode=StartMode.RESET_STACK,
        state=MainMenuStatesGroup.user,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def start_handler(
    event: Message,
    dialog_manager: DialogManager,
) -> None:
    await start_main_menu_dialog(dialog_manager)
