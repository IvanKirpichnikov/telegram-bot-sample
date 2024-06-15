from typing import Any, NewType


Id = NewType("Id", int)


class SecurityString:
    _string: str
    __slots__ = ['_string']
    
    def __init__(self, string: str) -> None:
        self._string = string
    
    def security(self) -> str:
        return self._string
    
    def __repr__(self) -> str:
        return "********"
    
    def __delattr__(self, item: Any) -> None:
        raise NotImplementedError
    
    def __setattr__(self, key: Any, value: Any) -> None:
        raise NotImplementedError
