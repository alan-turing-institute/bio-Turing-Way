"""Tests for the hello module."""
import unittest
from pathlib import Path
from unittest import mock

from yaml import Loader, load

from main import (
    build_all,
    build_pathway,
    edit_config_title,
    generate_tocs,
    get_toc_and_profiles,
    main,
    mask_parts,
    mask_toc,
)


class TestMain(unittest.TestCase):
    """Test main function from the main module."""

    def test_main(self):
        # Redirect stdout
        with mock.patch("main.build_all") as mock_build:
            main(["build", "/path/to/my/book/"])

            mock_build.assert_called_once_with(book_path=Path("/path/to/my/book/"))


class TestMask(unittest.TestCase):
    """Test the mask_x functions from the main module."""

    maxDiff = None

    def test_mask_single_profile(self):
        whitelist = ["intro", "setup", "version_control/git"]

        with open("tests/test_files/test_one/_toc.yml", "r") as f:
            toc = load(f, Loader=Loader)

        with open("tests/test_files/test_one/dsg_toc.yml", "r") as f:
            expected = load(f, Loader=Loader)

        actual = mask_toc(toc, whitelist)

        self.assertDictEqual(expected, actual)

    def test_mask_toc(self):
        with mock.patch("main.mask_parts") as mock_parts:
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


class TestGenerateTocs(unittest.TestCase):
    """Test the generate_tocs function from the main module."""

    def test_one_profile(self):
        with mock.patch("main.mask_toc") as mock_mask_toc:
            mock_mask_toc.return_value = {"new": "toc"}

            toc = {"a": "toc"}
            profiles = {"dsg": [], "phd": []}

            actual = list(generate_tocs(toc, profiles))
            expected = [("dsg", {"new": "toc"}), ("phd", {"new": "toc"})]
            self.assertListEqual(expected, actual)


class TestBuild(unittest.TestCase):
    """Test the build function from the main module."""

    def test_build_pathway(self):
        with mock.patch("main.copytree") as mock_copy:
            with mock.patch("main.customise_config") as mock_config:
                with mock.patch("main.open") as mock_open:
                    with mock.patch("main.dump") as mock_dump:

                        build_pathway("dsg", {"new": "toc"}, Path("mybook"))

                        mock_dump.assert_called_once_with(
                            {"new": "toc"},
                            mock_open.return_value.__enter__.return_value,
                        )

                    mock_open.assert_called_with(Path("mybook_dsg/_toc.yml"), "w")
                mock_config.assert_called_once_with(
                    new_path=Path("mybook_dsg"), new_title="dsg"
                )

            mock_copy.assert_has_calls(
                [
                    mock.call(Path("mybook"), Path("mybook_dsg"), dirs_exist_ok=True),
                ]
            )

    def test_build_all(self):
        with mock.patch("main.run") as mock_run:
            with mock.patch("main.get_toc_and_profiles") as mock_get:
                mock_get.return_value = {"a": "toc"}, {"dsg": "profile"}

                with mock.patch("main.generate_tocs") as mock_generate:
                    mock_generate.return_value = [("dsg", {"new": "toc"})]

                    with mock.patch("main.build_pathway") as mock_edition:
                        with mock.patch("main.Path.mkdir") as mock_mkdir:
                            with mock.patch("main.copytree") as mock_copytree:

                                with mock.patch("main.rmtree") as mock_rmtree:
                                    build_all(Path("mybook"))

                                    mock_rmtree.assert_called_once_with(
                                        Path("mybook_dsg")
                                    )

                                # ToDo Actual: copytree(PosixPath('mybook_dsg/_build/html'), PosixPath('mybook/_build/html/editions/dsg'), dirs_exist_ok=True)
                                # mock_copytree.assert_called_once_with()

                        mock_edition.assert_called_once_with(
                            "dsg", {"new": "toc"}, Path("mybook")
                        )

                    mock_generate.assert_called_once_with(
                        {"a": "toc"}, {"dsg": "profile"}
                    )
                mock_get.assert_called_once_with(Path("mybook"))
            mock_run.assert_has_calls(
                [
                    mock.call(["jupyter-book", "clean", Path("mybook")], check=True),
                    mock.call(["jupyter-book", "build", Path("mybook")], check=True),
                ]
            )


class TestGetTocAndProfiles(unittest.TestCase):
    """Test the get_toc_and_profiles function from the main module."""

    def test_simple_case(self):
        """Check that open() and load() are called."""

        with mock.patch("main.open") as mock_open:
            with mock.patch("main.load") as mock_load:
                mock_load.return_value = 44

                path = Path("mybook")
                toc, profiles = get_toc_and_profiles(path)

                try:
                    mock_open.assert_any_call(Path("mybook/_toc.yml"))
                    mock_open.assert_any_call(Path("mybook/profiles.yml"))
                except AssertionError as e:
                    print(mock_open.call_args)
                    raise e

                self.assertEqual(44, toc)
                self.assertEqual(44, profiles)


class TestEditConfigTitle(unittest.TestCase):
    """Test that title is edited in config.yaml"""

    def test_edit_case(self):
        """Test that title edits are made"""
        config_dict = {"title": "The Turing Way"}
        edited_config_dict = edit_config_title(config=config_dict, new_title="Test")
        expected_config = {"title": "The Turing Way Test Pathway"}
        self.assertDictEqual(expected_config, edited_config_dict)


if __name__ == "__main__":
    unittest.main()
