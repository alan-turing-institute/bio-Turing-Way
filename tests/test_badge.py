"""Tests for the hello module."""
import unittest
from unittest import mock

from badge import generate_badge, generate_shields_link


class TestGenerateBadges(unittest.TestCase):
    """Tests for generate_badge function."""

    def test_simple(self):
        # pylint: disable=line-too-long
        expected = "[![](https://img.shields.io/static/v1?label=pathway&message=myprofile&color=green)](myprofile.md)"
        actual = generate_badge("myprofile", "green")
        self.assertEqual(expected, actual)


class TestGenerateShieldsLink(unittest.TestCase):
    """Tests for generate_shields_link function."""

    def test_simple(self):
        expected = (
            "https://img.shields.io/static/v1"
            "?label=pathway"
            "&message=myprofilename"
            "&color=blue"
        )
        actual = generate_shields_link("myprofilename", "blue")
        self.assertEqual(expected, actual)

    def test_escape(self):
        # ToDo We should escape chars with urllib.parse.quote
        #  https://stackoverflow.com/a/1695199/3324095
        self.assertTrue(False)


class TestInsertBadges(unittest.TestCase):
    """Tests for insert_badges function."""

    def test_simple(self):
        self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
