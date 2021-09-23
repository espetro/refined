import os
from unittest import TestCase
from typing import Annotated, TypeGuard

from refined.main import RefinementTypeException, refined
from refined.predicates import NonEmpty


class TestMain(TestCase):

    def test_refine_non_typed_method(self):

        @refined
        def hello(name):
            return f"Hello {name}!"

        hello("peter")

    def test_refine_non_refined_method(self):

        @refined
        def hello(name: str) -> str:
            return f"Hello {name}!"

        hello("peter")

    def test_refine_refined_method(self):
        @refined
        def hello(name: Annotated[str, NonEmpty[str]]) -> str:
            return f"Hello {name}!"

        hello("peter")

        with self.assertRaises(RefinementTypeException) as e:
            hello("")

        expected_message_lines = [
            "Conditions do not hold for the following parameters:",
            "For parameter name with refined type <class 'str'>,  is not a valid value"
        ]

        self.assertEqual(expected_message_lines, [_.strip() for _ in str(e.exception).split(os.linesep)])

