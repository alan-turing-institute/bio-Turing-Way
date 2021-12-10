"""Tests for the badge module."""
import unittest
from pathlib import Path
from unittest import mock

from badge import (
    edit_text,
    generate_badge,
    generate_shields_link,
    insert_badges,
    make_badge_dict,
)


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
        expected = (
            "https://img.shields.io/static/v1"
            "?label=pathway"
            "&message=my%20profilename"
            "&color=blue"
        )
        actual = generate_shields_link("my profilename", "blue")
        self.assertEqual(expected, actual)


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


class TestInsertBadges(unittest.TestCase):
    """Tests for the insert_badges function."""

    def test_simple(self):
        with mock.patch("badge.open") as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = (
                "# MyTitle"
            )

            fake_path = Path("/fake/path")
            insert_badges(
                fake_path,
                ["badgeA", "badgeB"],
                [
                    {"name": "profileA", "files": ["file1", "file3"]},
                    {"name": "profileB", "files": ["file2", "file3"]},
                ],
            )

            # Check we're reading the files that we think we are
            mock_open.assert_any_call(fake_path / "file1.md", "r", encoding="utf-8")
            mock_open.assert_any_call(fake_path / "file2.md", "r", encoding="utf-8")
            mock_open.assert_any_call(fake_path / "file3.md", "r", encoding="utf-8")

            # Check we're writing those same files
            mock_open.assert_any_call(fake_path / "file1.md", "w", encoding="utf-8")
            mock_open.assert_any_call(fake_path / "file2.md", "w", encoding="utf-8")
            mock_open.assert_any_call(fake_path / "file3.md", "w", encoding="utf-8")

            # ToDo Put spaces between badges
            mock_open.return_value.__enter__.return_value.write.assert_has_calls(
                [
                    mock.call("# MyTitle\nbadgeA"),
                    mock.call("# MyTitle\nbadgeA\nbadgeB"),
                    mock.call("# MyTitle\nbadgeB"),
                ]
            )


class TestEditText(unittest.TestCase):
    """Tests for the exit_text function."""

    def test_simple(self):
        markdown = "(welcome)=\n# Welcome"
        expected = "(welcome)=\n# Welcome\nbadgeA\nbadgeB"
        actual = edit_text(["badgeA", "badgeB"], markdown)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
