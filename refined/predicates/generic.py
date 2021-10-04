"""Refined generic types."""

from typing import Generic, TypeVar, Tuple, Any, Dict
from typing_extensions import TypeGuard

from .base import RefinementPredicate

_G = TypeVar("_G", bound=str)


__all__ = ['EqualPredicate']


class EqualPredicate(Generic[_G], RefinementPredicate):
    """Predicate that checks if a value is equal to another value"""

    @staticmethod
    def type_guard(value: _G, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_G]:
        other_value = args[0]
        return value == other_value
