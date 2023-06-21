"""Generate different pathways of the book, as determined by profiles.yml."""
import re
import urllib


def generate_badge(profile_name, colour, landing_name):
    """Return some badge markdown and a list of files to insert it into."""

    url = generate_shields_link()
    #landing_page = "{0}.md".format(landing_name)
    markdown = f"[![]({url})]()"
    return markdown

def generate_shields_link():
    """Generate a https://shields.io/ URL for this profile."""

    url = (
        "https://img.shields.io/static/v1"
        "?label=pathway"
        "&message=text"
    )
    return url


def insert_badges(book_path, badges, profiles):
   # print(profiles["files"])
    """Insert badges into the files specified by profiles."""

    # By using make_badge_dict(), we only need to open each file once
    badge_dict = make_badge_dict(badges, profiles)

    for key, value in badge_dict.items():
        code ="""<script> 
        const images = document.querySelectorAll('img[src="https://img.shields.io/static/v1?label=pathway&message=text"]');
        const urlSearchParams = new URLSearchParams(window.location.search);
        const pathwayValue = urlSearchParams.get('pathway');
        for (let i = 0; i <= images.length; i++) {
        images[i].setAttribute('src', `https://img.shields.io/static/v1?label=pathway&message=${pathwayValue}`);
       }

        </script>
        """
        with open(book_path / (key + ".md"), "r", encoding="utf-8") as f:
            text = f.read()

        text = edit_text(value, text)

        with open(book_path / (key + ".md"), "w", encoding="utf-8") as f:
            f.write(text)
            f.write(code)


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
    for profile in profiles:
        for filename in profile["files"]:
            if filename not in badge_dict:
                badge_dict[filename] = ['[![](https://img.shields.io/static/v1?label=pathway&message=text)]()']

    return badge_dict
