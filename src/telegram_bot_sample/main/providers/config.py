from dishka import from_context, provide, Provider, Scope

from telegram_bot_sample.config import (
    Config,
    LocalizationConfig,
    PostgresqlConfig,
    TelegramBotConfig,
)


class ConfigProvider(Provider):
    scope = Scope.APP
    config = from_context(provides=Config)
    
    @provide
    def telegram_bot(self, config: Config) -> TelegramBotConfig:
        return config.telegram_bot
    
    @provide
    def postgresql(self, config: Config) -> PostgresqlConfig:
        return config.postgresql
    
    @provide
    def localization(self, config: Config) -> LocalizationConfig:
        return config.localization
