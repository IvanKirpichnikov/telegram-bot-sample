from abc import abstractmethod
from typing import Any, Protocol

from aiogram.fsm.storage.base import BaseEventIsolation, StateType, StorageKey
from aiogram.fsm.storage.memory import (
    MemoryStorage as AiogramMemoryStorage,
    SimpleEventIsolation,
)


class BaseStorageProtocol(Protocol):
    @abstractmethod
    async def set_state(
        self,
        key: StorageKey,
        state: StateType = None,
    ) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_state(self, key: StorageKey) -> str | None:
        raise NotImplementedError
    
    @abstractmethod
    async def set_data(
        self,
        key: StorageKey,
        data: dict[str, Any],
    ) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        raise NotImplementedError
    
    async def update_data(
        self,
        key: StorageKey,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        raise NotImplementedError
    
    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def create_isolation(self, **kwargs: Any) -> BaseEventIsolation:
        raise NotImplementedError


class MemoryStorage(AiogramMemoryStorage, BaseStorageProtocol):
    def create_isolation(self, **kwargs: Any) -> BaseEventIsolation:
        return SimpleEventIsolation()
