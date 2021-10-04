"""
Refined common predicates.
These predicates do not strictly fall into one of the other categories because they mix
abstractions. For example, `ValueRangePredicate` applies for iterables of numeric type.
"""

from typing import Generic, TypeVar, Tuple, Any, Dict, Iterable
from typing_extensions import TypeGuard
from numbers import Real

from .base import RefinementPredicate

_I = TypeVar("_I", bound=Iterable[Real])


__all__ = [
    'ValueRangePredicate'
]


class ValueRangePredicate(Generic[_I], RefinementPredicate):
    """Predicate that checks if all the values in an iterable of `Real` are in a range"""
    @staticmethod
    def type_guard(iterable: _I, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_I]:
        lower_cap, upper_cap = args[:2]
        return all(lower_cap >= value <= upper_cap for value in iterable)
