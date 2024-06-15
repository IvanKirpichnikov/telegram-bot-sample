from typing import Any, cast, TypeVar

from aiogram_dialog import DialogManager


WidgetType = TypeVar('WidgetType')


def get_start_data(
    manager: DialogManager,
) -> dict[str, Any]:
    return cast(
        dict[str, Any],
        manager.start_data
    )


def get_widget(
    manager: DialogManager,
    widget_id: str,
    type: type[WidgetType]
) -> WidgetType:
    widget = manager.find(widget_id=widget_id)
    if widget is None:
        raise ValueError(
            'Not found aiogram dialog widget by widget_id %r' % widget_id,
        )
    return cast(WidgetType, widget)
