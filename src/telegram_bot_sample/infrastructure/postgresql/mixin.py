from psqlpy import Connection


class PostgresqlConnectionMixin:
    __slots__ = ["_connection"]
    
    def __init__(
        self,
        connection: Connection,
    ) -> None:
        self._connection = connection
    
    @property
    def connection(self) -> Connection:
        return self._connection
