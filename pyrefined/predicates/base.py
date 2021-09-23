from abc import ABC, abstractmethod

from typing import TypeVar, TypeGuard

_T = TypeVar("_T")


class RefinementType(ABC):
    """An abstract representation of a refinement type"""

    @staticmethod
    @abstractmethod
    def type_guard(value: _T) -> TypeGuard[_T]:
        """An user-defined type guard for a type '_T'"""
        pass
