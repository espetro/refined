"""
Refined string types.

Note that most of the predicates defined `collection` also work for strings, by treating
them as a sequence of characters.
"""

from typing import Generic, TypeVar, Tuple, Any, Dict
from typing_extensions import TypeGuard
from csv import reader as CsvReader
from ipaddress import ip_address
from xml.etree import ElementTree
from io import StringIO

from .base import RefinementPredicate

_S = TypeVar("_S", bound=str)


__all__ = [
    'TrimmedPredicate',
    'ValidIntPredicate',
    'ValidFloatPredicate',
    'XmlPredicate',
    'CsvPredicate',
    'IPv6Predicate',
    'IPv4Predicate'
]


class TrimmedPredicate(Generic[_S], RefinementPredicate):
    """Predicate that checks if a `str` has no leading or trailing whitespace"""

    @staticmethod
    def type_guard(value: _S, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_S]:
        return value.strip() == value


class ValidIntPredicate(Generic[_S], RefinementPredicate):
    """Predicate that checks if a `str` is a parsable `int`"""

    @staticmethod
    def type_guard(value: _S, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_S]:
        try:
            _ = int(value)
            return True
        except:
            return False


class ValidFloatPredicate(Generic[_S], RefinementPredicate):
    """Predicate that checks if a `str` is a parsable `float`"""

    @staticmethod
    def type_guard(value: _S, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_S]:
        try:
            _ = float(value)
            return True
        except:
            return False


class XmlPredicate(Generic[_S], RefinementPredicate):
    """Predicate that checks if a `str` is well-formed XML"""

    @staticmethod
    def type_guard(value: _S, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_S]:
        try:
            with StringIO(value) as f:
                _ = ElementTree.parse(f)
            return True
        except:
            return False


class CsvPredicate(Generic[_S], RefinementPredicate):
    """
    Predicate that checks if a `str` is well-formed CSV. It uses a custom separator,
    which by default is ','
    """

    @staticmethod
    def type_guard(value: _S, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_S]:
        try:
            separator = args[0]
        except IndexError:
            separator = ","

        try:
            with StringIO(value) as f:
                for _ in CsvReader(f, delimiter=separator):
                    pass

            return True
        except:
            return False


class IPv4Predicate(Generic[_S], RefinementPredicate):
    """Predicate that checks if a `str` is a valid IPv4"""

    @staticmethod
    def type_guard(value: _S, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_S]:
        try:
            return ip_address(value).version == 4
        except:
            return False


class IPv6Predicate(Generic[_S], RefinementPredicate):
    """Predicate that checks if a `str` is a valid IPv6"""

    @staticmethod
    def type_guard(value: _S, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> TypeGuard[_S]:
        try:
            return ip_address(value).version == 6
        except:
            return False
