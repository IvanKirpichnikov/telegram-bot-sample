import os
from typing import Any, Mapping

from fluent.runtime import FluentLocalization, FluentResourceLoader

from telegram_bot_sample.config import LocalizationConfig
from telegram_bot_sample.infrastructure.localization.entities import Language


class Localization(FluentLocalization):
    def __call__(self, key: str, /, **kwargs: Any) -> str:
        text = self.format_value(key, kwargs)
        if text == key:
            raise ValueError("Not found text. Key: %r" % key)
        return text


class LocalizationStorage:
    __slots__ = (
        "_locales",
        "_default_language",
    )
    
    def __init__(
        self,
        locales: Mapping[Language, Localization],
        default_language: Language,
    ) -> None:
        self._locales = locales
        self._default_language = default_language
    
    def get_locale(self, language: Any) -> Localization:
        try:
            language_ = Language(language)
        except ValueError:
            language_ = self._default_language
        return self._locales[language_]


def build_localization_storage(
    config: LocalizationConfig,
) -> LocalizationStorage:
    locales = {}
    for language in Language:
        path = config.path / language.value
        locales[language] = Localization(
            locales=[language.value],
            resource_loader=FluentResourceLoader(roots=[str(path)]),
            resource_ids=[file for file in os.listdir(path) if file.endswith(".ftl")],
        )
    
    return LocalizationStorage(
        locales=locales,
        default_language=config.default_language,
    )
