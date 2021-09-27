from typing import Annotated, TypeVar, List, Set, Dict

from refined.predicates import (
    PositivePredicate,
    NegativePredicate,
    ValidIntPredicate,
    ValidFloatPredicate,
    EmptyPredicate,
    NonEmptyPredicate
)

_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")

Positive = Annotated[_T1, PositivePredicate[_T1]]
Negative = Annotated[_T1, NegativePredicate[_T1]]

ValidInt = Annotated[str, ValidIntPredicate[str]]
ValidFloat = Annotated[str, ValidFloatPredicate[str]]

Empty = Annotated[_T1, EmptyPredicate[_T1]]
NonEmpty = Annotated[_T1, NonEmptyPredicate[_T1]]

NonEmptyString = Annotated[str, NonEmptyPredicate[str]]
NonEmptyList = Annotated[List[_T1], NonEmptyPredicate[List[_T1]]]
NonEmptySet = Annotated[Set[_T1], NonEmptyPredicate[Set[_T1]]]
NonEmptyDict = Annotated[Dict[_T1, _T2], NonEmptyPredicate[Dict[_T1, _T2]]]
