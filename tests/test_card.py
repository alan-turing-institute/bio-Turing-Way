"""Tests for the cards module."""
import unittest

from card import create_card, create_panel, insert_text_after_string


class TestCreateCard(unittest.TestCase):
    """Tests for the create_card function."""

    def test_simple(self):
        file_list = [
            "welcome",
            "communication/communication",
            "communication/comms-overview",
            "communication/comms-overview/comms-overview-principles",
        ]
        actual = create_card("SomePersona", file_list, "sinner")
        expected = (
            "```{link-button} ./sinner.html\n"
            ":text: SomePersona\n"
            ":classes: bg-info text-white text-center font-weight-bold\n"
            "```\n"
            "^^^\n"
            "- [](welcome)\n"
            "- [](communication/communication)\n"
            "- [](communication/comms-overview)\n"
            "\nAnd more... \n"
        )
        self.assertEqual(expected, actual)


class TestGeneratePanel(unittest.TestCase):
    """Tests for the create_panel function."""

    def test_simple(self):
        list_of_cards = ["one", "two"]
        actual = create_panel(list_of_cards)
        expected = (
            ":::{panels}\n"
            ":container: +full-width\n"
            ":column: col-lg-6 px-2 py-2\n"
            ":header: text-center bg-white\n"
            ":card: text-left shadow\n"
            ":footer: text-left\n"
            "one"
            "\n---\n"
            "two"
            "\n::: \n"
        )
        self.assertEqual(expected, actual)


class TestInsertTextAfterString(unittest.TestCase):
    """Tests for the insert_text_after_string function."""

    def test_simple(self):
        input_str = "## Different Profiles"
        panel_str = (
            ":::{panels}\n"
            ":container: +full-width\n"
            ":column: col-lg-6 px-2 py-2\n"
            ":header: text-center bg-white\n"
            ":card: text-left shadow\n"
            ":footer: text-left\n"
            "one"
            "\n---\n"
            "two"
            "\n::: \n"
        )
        expected = "## Different Profiles\n" + panel_str
        actual = insert_text_after_string(input_str, "## Different Profiles", panel_str)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
