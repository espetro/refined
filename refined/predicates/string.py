"""Refined string types"""

from typing import TypeGuard, Generic, TypeVar, Tuple, Any, Dict

from .base import RefinementPredicate

_S = TypeVar("_S", bound=str)


class ValidIntPredicate(Generic[_S], RefinementPredicate):

    @staticmethod
    def type_guard(value: _S, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_S]:
        try:
            _ = int(value)
            return True
        except:
            return False


class ValidFloatPredicate(Generic[_S], RefinementPredicate):

    @staticmethod
    def type_guard(value: _S, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_S]:
        try:
            _ = float(value)
            return True
        except:
            return False
