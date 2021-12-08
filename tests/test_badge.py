"""Tests for the hello module."""
import unittest
from pathlib import Path
from unittest import mock

from badge import generate_badge, generate_shields_link, insert_badges, make_badge_dict


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


class TestMakeBadgeDict(unittest.TestCase):
    """Tests for insert_badges function."""

    def test_simple(self):
        self.assertDictEqual(
            {
                "file1": [
                    "badgeA",
                ],
                "file2": [
                    "badgeB",
                ],
                "file3": [
                    "badgeA",
                    "badgeB",
                ],
            },
            make_badge_dict(
                ["badgeA", "badgeB"],
                [
                    {"name": "profileA", "files": ["file1", "file3"]},
                    {"name": "profileB", "files": ["file2", "file3"]},
                ],
            ),
        )


if __name__ == "__main__":
    unittest.main()
