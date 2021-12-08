"""Generate different pathways of the book, as determined by profiles.yml."""


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
    del profiles
    del book_path
    del badges
    print("insert_badges not implemented!")
