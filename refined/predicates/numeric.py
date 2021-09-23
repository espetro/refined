"""Refined numeric types"""

import math
from typing import TypeGuard, Generic, TypeVar
from numbers import Real

from .base import RefinementType

_R = TypeVar("_R", bound=Real)


class Positive(Generic[_R], RefinementType):

    @staticmethod
    def type_guard(value: _R) -> TypeGuard[_R]:
        return value > 0


class Negative(Generic[_R], RefinementType):

    @staticmethod
    def type_guard(value: _R) -> TypeGuard[_R]:
        return value < 0


class Even(Generic[_R], RefinementType):

    @staticmethod
    def type_guard(value: _R) -> TypeGuard[_R]:
        return value % 2 == 0


class Odd(Generic[_R], RefinementType):

    @staticmethod
    def type_guard(value: _R) -> TypeGuard[_R]:
        return not Even.type_guard(value)


class NonNan(Generic[_R], RefinementType):

    @staticmethod
    def type_guard(value: _R) -> TypeGuard[_R]:
        return math.isnan(value)
