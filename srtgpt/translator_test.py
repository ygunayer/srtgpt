import unittest
from typing import NamedTuple

from .translator import parse_ai_response


class ParseTestFixture(NamedTuple):
    input_str: str
    expected: str


def load_fixture(name: str) -> ParseTestFixture:
    with open(f"test/{name}.input.txt") as f:
        input_str = f.read()
    with open(f"test/{name}.expect.txt") as f:
        expected = f.read()
    return ParseTestFixture(input_str, expected)


class ParseTests(unittest.TestCase):
    def test_parse_ai_slop(self):
        fixture = load_fixture("slop1")
        actual = parse_ai_response(fixture.input_str)
        self.assertEqual(actual, fixture.expected)

    def test_parse_ai_slop2(self):
        fixture = load_fixture("slop2")
        actual = parse_ai_response(fixture.input_str)
        self.assertEqual(actual, fixture.expected)

    def test_parse_just_srt(self):
        fixture = load_fixture("justsrt1")
        actual = parse_ai_response(fixture.input_str)
        self.assertEqual(actual, fixture.expected)


if __name__ == '__main__':
    unittest.main()

