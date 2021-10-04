"""Refined collection types"""

from typing import Generic, TypeVar, Collection, Tuple, Any, Dict
from typing_extensions import TypeGuard

from .base import RefinementPredicate

_C = TypeVar("_C", bound=Collection)


__all__ = [
    'EmptyPredicate',
    'NonEmptyPredicate'
]


class EmptyPredicate(Generic[_C], RefinementPredicate):

    @staticmethod
    def type_guard(value: _C, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_C]:
        return len(value) == 0


class NonEmptyPredicate(Generic[_C], RefinementPredicate):

    @staticmethod
    def type_guard(value: _C, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_C]:
        return not EmptyPredicate.type_guard(value)
