from abc import abstractmethod
from typing import Protocol, TypeVar


DataType = TypeVar("DataType", contravariant=True)
ReturnType = TypeVar("ReturnType", covariant=True)


class Command(Protocol[DataType, ReturnType]):
    @abstractmethod
    async def execute(self, data: DataType) -> ReturnType:
        raise NotImplementedError
