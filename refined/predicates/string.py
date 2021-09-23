"""Refined string types"""

from typing import TypeGuard, Generic, TypeVar

from .base import RefinementType

_T = TypeVar("_T", bound=str)


class ValidInt(Generic[_T], RefinementType):

    @staticmethod
    def type_guard(value: _T) -> TypeGuard[_T]:
        try:
            _ = int(value)
            return True
        except:
            return False


class ValidFloat(Generic[_T], RefinementType):

    @staticmethod
    def type_guard(value: _T) -> TypeGuard[_T]:
        try:
            _ = float(value)
            return True
        except:
            return False
