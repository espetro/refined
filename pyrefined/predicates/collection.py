"""Refined collection types"""

from typing import TypeGuard, Generic, TypeVar, Collection

from .base import RefinementType

_T = TypeVar("_T", bound=Collection)


class Empty(RefinementType, Generic[_T]):

    @staticmethod
    def type_guard(value: _T) -> TypeGuard[_T]:
        return len(value) == 0


class NonEmpty(RefinementType, Generic[_T]):

    @staticmethod
    def type_guard(value: _T) -> TypeGuard[_T]:
        return not Empty.type_guard(value)
