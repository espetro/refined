from abc import ABC, abstractmethod

from typing import TypeVar, Any, Tuple, Dict
from typing_extensions import TypeGuard

_T = TypeVar("_T")


__all__ = ['RefinementPredicate', 'RefinementTypeException']


class RefinementTypeException(Exception):
    pass


class RefinementPredicate(ABC):
    """An abstract representation of a refinement predicate"""

    @staticmethod
    @abstractmethod
    def type_guard(value: _T, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_T]:
        """An user-defined type guard for a type '_T'"""
        raise NotImplementedError(f"Type guard for type {type(value)} is not implemented")
