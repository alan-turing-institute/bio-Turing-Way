"""Generate different pathways of the book, as determined by profiles.yml."""
import sys
from argparse import ArgumentParser
from pathlib import Path
from shutil import copytree
from subprocess import run

from yaml import Loader, load

import landing_page
from badge import generate_badge, insert_badges
from card import HEADING_TITLE, create_card, create_panel, insert_into_md


def get_toc_and_profiles(book_path):
    """Get the contents of _toc.yml and profiles.yml."""

    with open(book_path / "_toc.yml", "r", encoding="utf-8") as f:
        toc = load(f, Loader=Loader)

    with open(book_path / "profiles.yml", "r", encoding="utf-8") as f:
        profiles = load(f, Loader=Loader)

    return toc, profiles


def generate_card(profile: dict, landing_name):
    return create_card(profile["name"], profile["files"], landing_name=landing_name)


def generate_landing_page(profile, toc, landing_name):
    a_landing_page = landing_page.LandingPage(
        persona=profile, landing_name=landing_name
    )
    a_landing_page.gather_curated_links(toc)
    return a_landing_page


def insert_cards(welcome_path, cards):
    insert_into_md(welcome_path, HEADING_TITLE, create_panel(cards))


def insert_landing_pages(landing_pages):
    for lp in landing_pages:
        lp.write_content()


def generate_landing_name(profile_name):
    landing_name = profile_name.replace(" ", "-")
    landing_name = landing_name.lower()
    return landing_name


def pathways(book_path):
    """Add extra pathways to the book."""

    # The contents of _toc.yml and profiles.yml contents
    new_path = book_path.parent / (book_path.name + "_copy")
    copytree(book_path, new_path, dirs_exist_ok=True)

    landing_page.LandingPage.book_path = new_path
    toc, profiles = get_toc_and_profiles(new_path)

    landing_pages = []
    badges = []
    cards = []

    for profile in profiles:
        landing_name = generate_landing_name(profile["name"])
        # Input profile is profile name + file list
        cards.append(generate_card(profile, landing_name))
        badges.append(generate_badge(profile["name"], profile["colour"], landing_name))
        landing_pages.append(
            generate_landing_page(
                profile["name"], generate_toc(toc, profile), landing_name
            )
        )

    insert_cards(new_path / "welcome.md", cards)
    insert_landing_pages(landing_pages)
    insert_badges(new_path, badges, profiles)

    run(["jupyter-book", "build", new_path], check=True)
    # rmtree(new_path)

    print("Finished adding pathways.")


def main(args):
    """Parse arguments and call sub-commands as appropriate."""

    # Get the arguments passed in by the user
    parser = ArgumentParser(description="Build a Jupyter Book.")
    subparsers = parser.add_subparsers()

    build_subparser = subparsers.add_parser("pathways")
    build_subparser.add_argument(
        "book_path", type=Path, help="the path to the root of your Jupyter Book"
    )
    build_subparser.set_defaults(func=pathways)

    # Call the sub-parser's function with the other arguments
    arguments = parser.parse_args(args)
    arg_dict = vars(arguments)
    arg_dict.pop("func")(**arg_dict)


def mask_parts(components, whitelist):
    """Makes a new components list, containing only whitelisted files.

    Args:
        components: An iterable of parts, chapters or sections.
        whitelist: An iterable of files to keep.

    Returns:
        A new list of parts, chapters or sections that omits files that aren't
        whitelisted and components that are now empty.
    """

    # Don't modify components as they may be needed by other profiles
    new_components = []

    # We could have a list of parts, chapters or sections
    for component in components:

        new_component = dict()

        for key, value in component.items():
            if key == "file":
                if value in whitelist:
                    new_component["file"] = value

            elif key in ("parts", "chapters", "sections"):
                sub_components = mask_parts(value, whitelist)
                if sub_components:
                    new_component[key] = sub_components

        if new_component:

            # Add other entries, like "title": "my title"
            for key, value in component.items():
                if key not in ("file", "parts", "chapters", "sections"):
                    new_component[key] = value

            new_components.append(new_component)

    return new_components


def mask_toc(toc, whitelist):
    """Makes a new ToC, containing only whitelisted files.

    Args:
        toc: A Table of Contents dictionary.
        whitelist: An iterable of files to keep.

    Returns:
        A new Table of Contents that omits files that aren't whitelisted and
        components that are now empty.
    """
    masked_toc = mask_parts([toc], whitelist)
    return masked_toc[0]


def generate_toc(toc, profile):
    """Generate a new ToC for each profile."""
    return mask_toc(toc, profile["files"])


if __name__ == "__main__":
    main(sys.argv[1:])  # pragma: no cover
    # main(["pathways", "master"])
