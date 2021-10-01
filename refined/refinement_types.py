from typing_extensions import Annotated, TypeGuard
from typing import TypeVar, List, Set, Dict

from refined.predicates import (
    PositivePredicate,
    NegativePredicate,
    ValidIntPredicate,
    ValidFloatPredicate,
    EmptyPredicate,
    NonEmptyPredicate,
    TrimmedPredicate,
    IPv4Predicate,
    IPv6Predicate,
    XmlPredicate,
    CsvPredicate
)

__all__ = [
    # numeric types
    'Positive',
    'Negative',

    # string types
    'TrimmedString',
    'ValidIntString',
    'ValidFloatString',
    'XmlString',
    'CsvString',
    'IPv4String',
    'IPv6String',

    # generic collection types
    'Empty',
    'NonEmpty',

    # concrete collection types
    'NonEmptyString',
    'NonEmptyList',
    'NonEmptySet',
    'NonEmptyDict',
]

_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")

Positive = Annotated[_T1, PositivePredicate[_T1]]
Negative = Annotated[_T1, NegativePredicate[_T1]]

TrimmedString = Annotated[str, TrimmedPredicate[str]]
ValidIntString = Annotated[str, ValidIntPredicate[str]]
ValidFloatString = Annotated[str, ValidFloatPredicate[str]]
XmlString = Annotated[str, XmlPredicate[str]]
CsvString = Annotated[str, CsvPredicate[str]]
IPv4String = Annotated[str, IPv4Predicate[str]]
IPv6String = Annotated[str, IPv6Predicate[str]]

Empty = Annotated[_T1, EmptyPredicate[_T1]]
NonEmpty = Annotated[_T1, NonEmptyPredicate[_T1]]

NonEmptyString = Annotated[str, NonEmptyPredicate[str]]
NonEmptyList = Annotated[List[_T1], NonEmptyPredicate[List[_T1]]]
NonEmptySet = Annotated[Set[_T1], NonEmptyPredicate[Set[_T1]]]
NonEmptyDict = Annotated[Dict[_T1, _T2], NonEmptyPredicate[Dict[_T1, _T2]]]
