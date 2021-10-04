import os

from xml.etree import ElementTree as ET
from unittest import TestCase
from numbers import Real
from typing import List
from io import StringIO


from refined import refined, RefinementTypeException
from refined.refinement_types import *

from tests.utils import get_message_lines


def base_conversion(num: Real, base: int) -> List[int]:
    digits = []
    while num > 0:
        num, remainder = divmod(num, base)
        digits.append(remainder)

    return digits[::-1]


class TestPredicatesString(TestCase):

    def test_predicate_valid_float(self):
        @refined
        def get_decimals(value: ValidFloatString) -> ValidFloatString:
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
        def add_trailing_zero(value: ValidIntString) -> ValidIntString:
            return value + "0"

        self.assertEqual(add_trailing_zero("10"), "100")

        with self.assertRaises(RefinementTypeException) as e:
            add_trailing_zero("10+1j")

        expected_message_lines = [
            "Conditions do not hold for the following parameters:",
            "For parameter value with refined type <class 'str'>, 10+1j is not a valid value"
        ]

        self.assertEqual(expected_message_lines, get_message_lines(str(e.exception)))

    def test_predicate_trimmed(self):
        @refined
        def get_first_character(value: TrimmedString) -> TrimmedString:
            if value:
                return value[0]
            else:
                return ""

        self.assertEqual(get_first_character("3.14"), "3")

        with self.assertRaises(RefinementTypeException) as e:
            get_first_character(" 3+2j ")

        expected_message_lines = [
            "Conditions do not hold for the following parameters:",
            "For parameter value with refined type <class 'str'>,  3+2j  is not a valid value"
        ]

        self.assertEqual(expected_message_lines, get_message_lines(str(e.exception)))

    def test_predicate_valid_ipv4(self):
        @refined
        def get_most_significant_digit(value: IPv4String) -> int:
            head, *_ = value.split(".")
            bin_representation = base_conversion(int(head), 2)
            return bin_representation[0]

        self.assertEqual(get_most_significant_digit("192.168.0.1"), 1)

        with self.assertRaises(RefinementTypeException) as e:
            get_most_significant_digit("182.10231.0.1")

        expected_message_lines = [
            "Conditions do not hold for the following parameters:",
            "For parameter value with refined type <class 'str'>, 182.10231.0.1 is not a valid value"
        ]

        self.assertEqual(expected_message_lines, get_message_lines(str(e.exception)))

    def test_predicate_well_formed_xml(self):
        @refined
        def get_tree_root(value: XmlString) -> ET.Element:
            with StringIO(value) as f:
                tree = ET.parse(f)

            return tree.find(".")

        sample_input = """
            <note>
                <to>Tove</to>
                <from>Jani</from>
                <heading>Reminder</heading>
                <body>Don't forget me this weekend!</body>
            </note>
        """

        root = get_tree_root(sample_input)
        self.assertEqual(root.tag, "note")

        with self.assertRaises(RefinementTypeException) as e:
            get_tree_root("")

        expected_message_lines = [
            "Conditions do not hold for the following parameters:",
            "For parameter value with refined type <class 'str'>,  is not a valid value"
        ]

        self.assertEqual(expected_message_lines, get_message_lines(str(e.exception)))
