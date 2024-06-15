from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from telegram_bot_sample.application.interfaces.transaction_manager import TransactionManager
from telegram_bot_sample.infrastructure.postgresql.mixin import PostgresqlConnectionMixin


class PostgresqlTransactionManager(
    PostgresqlConnectionMixin,
    TransactionManager,
):
    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[Any]:
        async with self._connection.transaction():
            yield None
