from abc import abstractmethod
from typing import Any, AsyncContextManager, Protocol


class TransactionManager(Protocol):
    @abstractmethod
    def transaction(self) -> AsyncContextManager[Any]:
        raise NotImplementedError
