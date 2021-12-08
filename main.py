"""Generate different pathways of the book, as determined by profiles.yml."""
import sys
from argparse import ArgumentParser
from pathlib import Path

from yaml import Loader, load

from badge import generate_badge


def get_toc_and_profiles(book_path):
    """Get the contents of _toc.yml and profiles.yml."""

    with open(book_path / "_toc.yml", encoding="utf-8") as f:
        toc = load(f, Loader=Loader)

    with open(book_path / "profiles.yml", encoding="utf-8") as f:
        profiles = load(f, Loader=Loader)

    return toc, profiles


def generate_card(profile, toc):
    del profile
    del toc
    print("generate_card not implemented!")


def generate_landing_page(profile, toc):
    del profile
    del toc
    print("generate_landing_page not implemented!")


def insert_cards(welcome_path, cards):
    del welcome_path
    del cards
    print("insert_cards not implemented!")


def create_landing_pages(book_path, landing_pages):
    del book_path
    del landing_pages
    print("create_landing_pages not implemented!")


def insert_badges(book_path, badges):
    del book_path
    del badges
    print("insert_badges not implemented!")


def pathways(book_path):
    """Add extra pathways to the book."""

    toc, profiles = get_toc_and_profiles(book_path)

    landing_pages = []
    badges = []
    cards = []

    profiles_and_tocs = list(generate_tocs(toc, profiles))
    for profile_name, new_toc in profiles_and_tocs:
        cards.append(generate_card(profile_name, new_toc))

        badges.append(generate_badge(profile_name, new_toc))

        landing_pages.append(generate_landing_page(profile_name, new_toc))

    # Now that we have generated the new contents, copy the book before mutating
    # ToDo Copy mybook/ to e.g. mybook_copy/

    insert_cards("path/to/welcome.md", cards)
    create_landing_pages("/path/to/book", landing_pages)
    insert_badges("path/to/book", badges)

    # ToDo Shall we call `jupyter-book build mybook_copy/` here?

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


def generate_tocs(toc, profiles):
    """Generate a new ToC for each profile."""

    for profile_name, whitelist in profiles.items():
        yield profile_name, mask_toc(toc, whitelist)


if __name__ == "__main__":
    main(sys.argv[1:])  # pragma: no cover
