import unittest
from pathlib import Path
from unittest import mock

from LandingPage import (
    LandingPage as LandingPageClass,
)


class TestGetPageTitle(unittest.TestCase):
    """Tests for generate_badge function."""

    def test_simple(self):
      aLandingPage = LandingPageClass('test')
      markdown_text = """
  (welcome)=
  # Welcome

  *Welcome to The Turing Way handbook to reproducible, ethical and collaborative data science.*
  """
      expected = "Welcome"
      actual = aLandingPage.get_title_from_text(markdown_text)
      self.assertEqual(expected, actual)
      pass

class TestGetCuratedList(unittest.TestCase):
    """Tests for generate_badge function."""

    def test_simple(self):
      aLandingPage = LandingPageClass('test')
      toc = {'parts': [{'chapters': [{'file': 'communication/communication', 'sections': [{'file': 'communication/comms-overview', 'sections': [{'file': 'communication/comms-overview/comms-overview-principles', 'title': 'Principles of Communicating with Wider Audiences'}], 'title': 'Overview of Guide for Communication'}]}]}], 'format': 'jb-book', 'root': 'welcome'}
      aLandingPage.gather_curated_links(toc)
      actual = aLandingPage.curated_links
      expected = ['[](./communication/communication.md)', ['[](./communication/comms-overview.md)', ['[](./communication/comms-overview/comms-overview-principles.md)']]]
      self.assertEqual(actual, expected)
      
class TestGetLandingPage(unittest.TestCase):
    """Tests for generate_badge function."""

    def test_simple(self):
        pass
