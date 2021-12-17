"""Tests for the landing-page class."""
import json
import unittest

from pathways.landing_page import LandingPage


class TestGetPageTitle(unittest.TestCase):
    """Tests for generate_badge function."""

    def test_simple(self):
        a_landing_page = LandingPage("test_persona", "test")
        curated_page_path = "tests/test_files/test_landing/welcome.md"
        actual = a_landing_page.get_title_from_curated_page(curated_page_path)
        expected = "Welcome"
        self.assertEqual(expected, actual)
        pass


class TestGetCuratedList(unittest.TestCase):
    """Tests for generate_badge function."""

    def test_simple(self):
        a_landing_page = LandingPage("test", "sinner")
        whitelisted_toc_path = "tests/test_files/test_landing/toc_whitelist.json"
        with open(whitelisted_toc_path) as f:
            toc = json.load(f)
        a_landing_page.gather_curated_links(toc)
        actual = a_landing_page.curated_links
        expected = [
            "[](./communication/communication.md)",
            [
                "[](./communication/comms-overview.md)",
                ["[](./communication/comms-overview/comms-overview-principles.md)"],
            ],
        ]
        self.assertEqual(actual, expected)


class TestWriteLandingPageContent(unittest.TestCase):
    """Tests for generate_badge function."""

    def test_simple(self):
        a_landing_page = LandingPage(
            persona="test", landing_name="tests/test_files/test_landing/actual_landing"
        )
        a_landing_page.curated_links = [
            "[](./communication/communication.md)",
            [
                "[](./communication/comms-overview.md)",
                ["[](./communication/comms-overview/comms-overview-principles.md)"],
            ],
        ]
        actual_text = a_landing_page.write_content()
        with open(
            "tests/test_files/test_landing/expected_landing.md", "r"
        ) as expected_landing_file:
            expected_landing_text = expected_landing_file.read()
        self.assertMultiLineEqual(actual_text, expected_landing_text)
