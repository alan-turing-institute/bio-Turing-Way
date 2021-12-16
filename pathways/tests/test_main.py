"""Tests for the main module."""
import unittest
from pathlib import Path
from unittest import mock

from yaml import Loader, load

from pathways.main import get_toc_and_profiles, main, mask_parts, mask_toc


class TestMain(unittest.TestCase):
    """Test main function from the main module."""

    def test_main(self):
        # Redirect stdout
        with mock.patch("pathways.main.pathways") as mock_build:
            main(["pathways", "/path/to/my/book/"])

            mock_build.assert_called_once_with(book_path=Path("/path/to/my/book/"))


class TestMask(unittest.TestCase):
    """Test the mask_x functions from the main module."""

    maxDiff = None

    def test_mask_single_profile(self):
        whitelist = ["intro", "setup", "version_control/git"]

        with open("tests/test_files/test_one/_toc.yml", "r", encoding="utf-8") as f:
            toc = load(f, Loader=Loader)

        with open("tests/test_files/test_one/dsg_toc.yml", "r", encoding="utf-8") as f:
            expected = load(f, Loader=Loader)

        actual = mask_toc(toc, whitelist)

        self.assertDictEqual(expected, actual)

    def test_mask_toc(self):
        with mock.patch("pathways.main.mask_parts") as mock_parts:
            mock_parts.return_value = [5.5]

            toc = {
                "format": "jb-book",
                "root": "intro",
                "parts": [1, 2, 3],
            }
            whitelist = [
                "a filename",
            ]

            expected = 5.5
            actual = mask_toc(toc, whitelist)

            self.assertEqual(expected, actual)
            mock_parts.assert_called_once_with([toc], whitelist)

    def test_chapters(self):
        parts = [{"chapters": [{"file": "file1"}, {"file": "file2"}]}]
        whitelist = [
            "file1",
        ]

        expected = [{"chapters": [{"file": "file1"}]}]
        actual = mask_parts(parts, whitelist)
        self.assertListEqual(expected, actual)

    def test_sections(self):
        parts = [
            {
                "chapters": [
                    {"file": "file1", "sections": [{"file": "file2"}]},
                    {"file": "file3", "sections": [{"file": "file4"}]},
                ]
            },
            {"chapters": [{"file": "file5"}]},
        ]
        whitelist = [
            "file1",
            "file2",
        ]

        expected = [
            {
                "chapters": [
                    {"file": "file1", "sections": [{"file": "file2"}]},
                ]
            }
        ]
        actual = mask_parts(parts, whitelist)
        self.assertListEqual(expected, actual)

    def test_sub_sections(self):
        parts = [
            {
                "chapters": [
                    {
                        "file": "file1",
                        "sections": [
                            {
                                "file": "file2",
                                "sections": [{"file": "file3"}, {"file": "file4"}],
                            }
                        ],
                    },
                ]
            },
        ]
        whitelist = [
            "file1",
            "file2",
            "file4",
        ]

        expected = [
            {
                "chapters": [
                    {
                        "file": "file1",
                        "sections": [
                            {"file": "file2", "sections": [{"file": "file4"}]}
                        ],
                    },
                ]
            }
        ]
        actual = mask_parts(parts, whitelist)
        self.assertListEqual(expected, actual)

    def test_preserves_title(self):
        parts = [
            {
                "chapters": [
                    {
                        "file": "file1",
                        "title": "title1",
                        "sections": [
                            {
                                "file": "file2",
                                "title": "title2",
                                "sections": [
                                    {"title": "title3", "file": "file3"},
                                    {"title": "title4", "file": "file4"},
                                ],
                            }
                        ],
                    },
                ]
            },
        ]
        whitelist = [
            "file1",
            "file2",
            "file3",
        ]

        expected = [
            {
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
        ]
        actual = mask_parts(parts, whitelist)
        self.assertListEqual(expected, actual)


class TestPathways(unittest.TestCase):
    """Test the pathways function from the main module."""

    def test_pathways(self):
        # ToDo Test main.pathways()
        pass


class TestGetTocAndProfiles(unittest.TestCase):
    """Test the get_toc_and_profiles function from the main module."""

    def test_simple_case(self):
        """Check that open() and load() are called."""

        with mock.patch("pathways.main.open") as mock_open:
            with mock.patch("pathways.main.load") as mock_load:
                mock_load.return_value = 44

                path = Path("mybook")
                toc, profiles = get_toc_and_profiles(path)

                try:
                    mock_open.assert_any_call(
                        Path("mybook/_toc.yml"), "r", encoding="utf-8"
                    )
                    mock_open.assert_any_call(
                        Path("mybook/profiles.yml"), "r", encoding="utf-8"
                    )
                except AssertionError as e:
                    print(mock_open.call_args_list)
                    raise e

                self.assertEqual(44, toc)
                self.assertEqual(44, profiles)


class TestGenerateLandingPageName(unittest.TestCase):
    def test_lowercase(self):
        expected = "dsg"
        actual = generate_landing_name("Dsg")
        self.assertEqual(expected, actual)

    def test_spaces(self):
        expected = "enrichment-students"
        actual = generate_landing_name("Enrichment Students")
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
