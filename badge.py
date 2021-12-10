"""Generate different pathways of the book, as determined by profiles.yml."""
import re
import urllib


def generate_badge(profile_name, colour):
    """Return some badge markdown and a list of files to insert it into."""

    url = generate_shields_link(profile_name, colour)
    landing_page = profile_name + ".md"
    markdown = f"[![]({url})]({landing_page})"
    return markdown


def generate_shields_link(profile_name, colour):
    """Generate a https://shields.io/ URL for this profile."""

    url = (
        "https://img.shields.io/static/v1"
        "?label=pathway"
        f"&message={urllib.parse.quote(profile_name)}"
        f"&color={colour}"
    )
    return url


def insert_badges(book_path, badges, profiles):
    """Insert badges into the files specified by profiles."""

    # By using make_badge_dict(), we only need to open each file once
    badge_dict = make_badge_dict(badges, profiles)

    for key, value in badge_dict.items():
        # value is a list of badges and key is a filename
        with open(book_path / (key + ".md"), "r", encoding="utf-8") as f:
            text = f.read()

        text = edit_text(value, text)

        with open(book_path / (key + ".md"), "w", encoding="utf-8") as f:
            f.write(text)


def edit_text(badges, text):
    """Insert badges into text, immediately after the title."""

    # Find the title line
    title_match = re.search(r"^# .*", text, re.MULTILINE)

    # Insert the badges
    text = (
        text[: title_match.end()] + "\n" + "\n".join(badges) + text[title_match.end() :]
    )
    return text


def make_badge_dict(badges, profiles):
    """Make a dict of files and their badges."""
    badge_dict = dict()

    for badge, profile in zip(badges, profiles):
        for filename in profile["files"]:
            if filename in badge_dict:
                entry = badge_dict[filename]
                entry.append(badge)

            else:
                badge_dict[filename] = [badge]

    return badge_dict
