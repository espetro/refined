from unittest import TestCase, skip
from typing import List

from refined import refined, RefinementTypeException
from refined.refinement_types import Empty, NonEmptyList, NonEmptyString

from tests.utils import get_message_lines


class TestPredicatesCollection(TestCase):

    def test_predicate_empty(self):
        @refined
        def list_as_str(ls: Empty[List[str]]) -> str:
            return ", ".join(ls)

        self.assertEqual(list_as_str([]), "")

        with self.assertRaises(RefinementTypeException) as e:
            list_as_str(["hello", "there"])

        expected_message_lines = [
            "Conditions do not hold for the following parameters:",
            "For parameter ls with refined type typing.List[str], ['hello', 'there'] is not a valid value"
        ]

        self.assertEqual(expected_message_lines, get_message_lines(str(e.exception)))

    @skip("To be done")
    def test_predicate_non_empty_list(self):
        @refined
        def greatest(ls: NonEmptyList[int]) -> int:
            return max(ls)

        self.assertEqual(greatest([1, 3, 2]), 3)

        with self.assertRaises(RefinementTypeException) as e:
            greatest([])

        expected_message_lines = [
            "Conditions do not hold for the following parameters:",
            "For parameter ls with refined type typing.List[int], [] is not a valid value"
        ]

        self.assertEqual(expected_message_lines, get_message_lines(str(e.exception)))

    @skip("To be done")
    def test_predicate_non_empty_string(self):
        @refined
        def upper(value: NonEmptyString) -> NonEmptyString:
            return value.upper()

        self.assertEqual(upper("hello"), "HELLO")

        with self.assertRaises(RefinementTypeException) as e:
            upper("")

        expected_message_lines = [
            "Conditions do not hold for the following parameters:",
            "For parameter value with refined type <class 'str'>,  is not a valid value"
        ]

        self.assertEqual(expected_message_lines, get_message_lines(str(e.exception)))
