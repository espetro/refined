from unittest import TestCase

from refined import refined, RefinementTypeException
from refined.refinement_types import Positive, Negative

from tests.utils import get_message_lines


class TestPredicatesNumeric(TestCase):

    def test_predicate_positive(self):
        @refined
        def plus_1(value: Positive[int]) -> Positive[int]:
            return value + 1

        self.assertEqual(plus_1(3), 4)

        with self.assertRaises(RefinementTypeException) as e:
            plus_1(-1)

        expected_message_lines = [
            "Conditions do not hold for the following parameters:",
            "For parameter value with refined type <class 'int'>, -1 is not a valid value"
        ]

        self.assertEqual(expected_message_lines, get_message_lines(str(e.exception)))

    def test_predicate_negative(self):
        @refined
        def plus_1(value: Negative[float]) -> Negative[float]:
            return value + 1

        self.assertEqual(plus_1(-100.0), -99)

        with self.assertRaises(RefinementTypeException) as e:
            plus_1(1.23)

        expected_message_lines = [
            "Conditions do not hold for the following parameters:",
            "For parameter value with refined type <class 'float'>, 1.23 is not a valid value"
        ]

        self.assertEqual(expected_message_lines, get_message_lines(str(e.exception)))
