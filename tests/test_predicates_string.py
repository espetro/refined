from unittest import TestCase

from refined.refinement_types import ValidInt, ValidFloat
from refined import refined, RefinementTypeException

from tests.utils import get_message_lines


class TestPredicatesString(TestCase):

    def test_predicate_valid_float(self):
        @refined
        def get_decimals(value: ValidFloat) -> ValidFloat:
            _, decimals = value.split(".")
            return decimals

        self.assertEqual(get_decimals("3.14"), "14")

        with self.assertRaises(RefinementTypeException) as e:
            get_decimals("3+2j")

        expected_message_lines = [
            "Conditions do not hold for the following parameters:",
            "For parameter value with refined type <class 'str'>, 3+2j is not a valid value"
        ]

        self.assertEqual(expected_message_lines, get_message_lines(str(e.exception)))

    def test_predicate_valid_int(self):
        @refined
        def add_trailing_zero(value: ValidInt) -> ValidInt:
            return value + "0"

        self.assertEqual(add_trailing_zero("10"), "100")

        with self.assertRaises(RefinementTypeException) as e:
            add_trailing_zero("10+1j")

        expected_message_lines = [
            "Conditions do not hold for the following parameters:",
            "For parameter value with refined type <class 'str'>, 10+1j is not a valid value"
        ]

        self.assertEqual(expected_message_lines, get_message_lines(str(e.exception)))
