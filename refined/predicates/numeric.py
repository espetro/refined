"""Refined numeric types"""

import math
from typing import Generic, TypeVar, Tuple, Any, Dict
from typing_extensions import TypeGuard, Literal, get_args
from numbers import Real

from .base import RefinementPredicate

_R = TypeVar("_R", bound=Real)
_0 = Literal[0]
_2 = Literal[2]


__all__ = [
    'Greater',
    'Less',
    'Modulo',
    'NonNan',
    'PositivePredicate',
    'NegativePredicate',
    'Divisible'
]


class Greater(Generic[_R], RefinementPredicate):

    @staticmethod
    def type_guard(value: _R, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_R]:
        threshold = args[0]
        threshold_value = get_args(threshold)[0]

        return value > threshold_value


class Less(Generic[_R], RefinementPredicate):

    @staticmethod
    def type_guard(value: _R, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_R]:
        threshold = args[0]
        threshold_value = get_args(threshold)[0]

        return value < threshold_value


class Modulo(Generic[_R], RefinementPredicate):

    @staticmethod
    def type_guard(value: _R, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_R]:
        divisor = args[0]
        divisor_value = get_args(divisor)[0]

        return value % divisor_value == 0


class NonNan(Generic[_R], RefinementPredicate):

    @staticmethod
    def type_guard(value: _R, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_R]:
        return math.isnan(value)


class PositivePredicate(Generic[_R], RefinementPredicate):

    @staticmethod
    def type_guard(value: _R, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_R]:
        return Greater[_R].type_guard(value, _0)


class NegativePredicate(Generic[_R], RefinementPredicate):

    @staticmethod
    def type_guard(value: _R, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_R]:
        return Less[_R].type_guard(value, _0)


class Divisible(Generic[_R], RefinementPredicate):

    @staticmethod
    def type_guard(value: _R, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_R]:
        return Modulo[_R].type_guard(value, _0)
