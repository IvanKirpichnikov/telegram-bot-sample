from inspect import Parameter
from typing import (
    Any,
    Callable,
    cast,
    Container,
    Final,
    ParamSpec,
    Sequence,
    TypeAlias,
    TypeVar,
)

from aiogram.types import TelegramObject
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import AsyncContainer
from dishka.integrations.base import (
    default_parse_dependency,
    DependencyParser,
    wrap_injection,
)


CONTAINER_KEY: Final[str] = "dishka_container"

Params = ParamSpec("Params")
ReturnType = TypeVar("ReturnType")

_AiogramMiddleware: TypeAlias = Callable[
    [
        Callable[[TelegramObject, dict[str, Any]], ReturnType],
        TelegramObject,
        dict[str, Any],
    ],
    ReturnType,
]


class _BaseInject:
    def _create_inject(
        self,
        *,
        func: Callable[Params, ReturnType],
        container_getter: Callable[[tuple[Any, ...], dict[Any, Any]], AsyncContainer],
        is_async: bool = True,
        remove_depends: bool = True,
        additional_params: Sequence[Parameter] = (),
        parse_dependency: DependencyParser = default_parse_dependency,
    ) -> Callable[Params, ReturnType]:
        return cast(
            Callable[Params, ReturnType],
            wrap_injection(  # type: ignore[call-overload]
                func=func,
                container_getter=container_getter,
                is_async=is_async,
                remove_depends=remove_depends,
                additional_params=additional_params,
                parse_dependency=parse_dependency,
            ),
        )


class AiogramDialogInject(_BaseInject):
    def getter(self, func: Callable[Params, ReturnType]) -> Callable[Params, ReturnType]:
        return self._create_inject(
            func=func,
            container_getter=lambda _, p: p[CONTAINER_KEY],
        )
    
    def dialog_event(
        self,
        func: Callable[Params, ReturnType],
    ) -> Callable[[Any, DialogManager], ReturnType]:
        return cast(
            Callable[[Any, DialogManager], ReturnType],
            self._create_inject(
                func=func,
                container_getter=lambda p, _: p[1].middleware_data[CONTAINER_KEY],
            ),
        )
    
    def on_process_result(
        self,
        func: Callable[Params, ReturnType],
    ) -> Callable[[Any, Any, DialogManager], ReturnType]:
        return cast(
            Callable[[Any, Any, DialogManager], ReturnType],
            self._create_inject(
                func=func,
                container_getter=lambda p, _: p[2].middleware_data[CONTAINER_KEY],
            ),
        )
    
    def on_click(
        self,
        func: Callable[Params, ReturnType],
    ) -> Callable[[ChatEvent, Button, DialogManager], ReturnType]:
        return cast(
            Callable[[ChatEvent, Button, DialogManager], ReturnType],
            self._create_inject(
                func=func,
                container_getter=lambda p, _: p[2].middleware_data[CONTAINER_KEY],
            ),
        )
    
    def render_text(
        self,
        func: Callable[Params, ReturnType],
    ) -> Callable[[dict[str, Any], DialogManager], ReturnType]:
        return cast(
            Callable[[dict[str, Any], DialogManager], ReturnType],
            self._create_inject(
                func=func,
                container_getter=lambda p, _: p[2].middleware_data[CONTAINER_KEY],
            ),
        )
    
    def render_keyboard(
        self,
        func: Callable[Params, ReturnType],
    ) -> Callable[[dict[str, Any], DialogManager], ReturnType]:
        return cast(
            Callable[[dict[str, Any], DialogManager], ReturnType],
            self._create_inject(
                func=func,
                container_getter=lambda p, _: p[1]["middleware_data"][CONTAINER_KEY],
            ),
        )


class AiogramInject(_BaseInject):
    def handler(
        self,
        func: Callable[Params, ReturnType],
    ) -> Callable[Params, ReturnType]:
        additional_params = [
            Parameter(
                name="dishka_container",
                annotation=Container,
                kind=Parameter.KEYWORD_ONLY,
            )
        ]
        return cast(
            Callable[Params, ReturnType],
            self._create_inject(
                func=func,
                container_getter=lambda _, p: p[CONTAINER_KEY],
                additional_params=additional_params,
            ),
        )
    
    def filter(
        self,
        func: Callable[Params, ReturnType],
    ) -> Callable[Params, ReturnType]:
        additional_params = [
            Parameter(
                name="dishka_container",
                annotation=Container,
                kind=Parameter.KEYWORD_ONLY,
            )
        ]
        return cast(
            Callable[Params, ReturnType],
            self._create_inject(
                func=func,
                container_getter=lambda _, p: p[CONTAINER_KEY],
                additional_params=additional_params,
            ),
        )
    
    def middleware(
        self,
        func: Callable[Params, ReturnType],
    ) -> _AiogramMiddleware[ReturnType]:
        return cast(
            _AiogramMiddleware[ReturnType],
            self._create_inject(
                func=func,
                container_getter=lambda p, _: p[3][CONTAINER_KEY],
            ),
        )


class Inject:
    __slots__ = (
        "aiogd",
        "aiogram",
    )
    
    def __init__(self) -> None:
        self.aiogd = AiogramDialogInject()
        self.aiogram = AiogramInject()


inject = Inject()
