"""Tests for the hello module."""
import unittest
from unittest import mock

from badge import extract_files, generate_badge


class TestGenerateBadges(unittest.TestCase):
    def test_generate_badge(self):
        toc = None
        expected = None
        actual = generate_badge()
        self.assertEqual(expected, actual)


class TestExtractFiles(unittest.TestCase):
    def test_extract_files(self):
        toc = {
            "chapters": [
                {
                    "file": "file1",
                    "title": "title1",
                    "sections": [
                        {
                            "title": "title2",
                            "file": "file2",
                            "sections": [{"title": "title3", "file": "file3"}],
                        }
                    ],
                },
            ]
        }
        actual = extract_files(toc)
        expected = ["file1", "file2", "file3"]
        self.assertListEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
