"""Generate different pathways of the book, as determined by profiles.yml."""
from pathlib import Path

from markdown import markdown


def extract_recursive(components):
    files = []

    for component in components:
        for key, value in component.items():
            if key == "file":
                files.append(value)
            elif key in ("parts", "chapters", "sections"):
                files = files + extract_recursive(value)
    return files


def extract_files(toc):
    """Return a list of files in the toc."""
    return extract_recursive([toc])


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
        f"&message={profile_name}"
        f"&color={colour}"
    )
    return url


def insert_badges(book_path, badges, profiles):
    """Insert badges into the files specified by profiles."""

    # By using make_badge_dict(), we only need to open each file once
    for key, value in make_badge_dict(badges, profiles).items():
        # value is a list of badges and key is a filename
        with open(book_path / (key + ".md"), "w", encoding="utf-8") as f:
            text = f.read()
            md = markdown(text)

            # ToDo Insert badges below the title and save the file
            assert False


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
