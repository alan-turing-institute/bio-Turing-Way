"""Generate different editions of the book, as determined by profiles.yml."""
import sys
from argparse import ArgumentParser
from pathlib import Path
from shutil import copytree, ignore_patterns, rmtree
from subprocess import run

from yaml import Loader, dump, load


def get_toc_and_profiles(book_path):
    """Get the contents of _toc.yml and profiles.yml."""

    with open(book_path / "_toc.yml") as f:
        toc = load(f, Loader=Loader)

    with open(book_path / "profiles.yml") as f:
        profiles = load(f, Loader=Loader)

    return toc, profiles


def build_edition(profile_name, new_toc, book_path):
    """Copy book_path to make an edition called profile_name and containing new_toc."""

    new_path = book_path.parent / (book_path.name + "_" + profile_name)

    # Copy the whole book
    copytree(book_path, new_path, dirs_exist_ok=True, ignore=ignore_patterns("_build"))

    with open(new_path / "_toc.yml", "w") as f:
        # Overwrite the _toc.yml
        dump(new_toc, f)

    # Call Jupyter Book to build the copy
    run(["jupyter-book", "build", new_path], check=True)

    # Make the directory, if it doesn't already exist
    editions_path = book_path / "_build/html/editions"
    editions_path.mkdir(parents=True, exist_ok=True)

    # Copy the built html to the editions directory
    copytree(new_path / "_build/html", editions_path / profile_name, dirs_exist_ok=True)
    rmtree(new_path)
    return new_path


def build_all(book_path):
    """Build the book and its other editions."""

    # Clean the book_path/_build dir to remove previous _build/html/edition/ dirs
    run(["jupyter-book", "clean", book_path], check=True)

    toc, profiles = get_toc_and_profiles(book_path)

    for profile_name, new_toc in generate_tocs(toc, profiles):
        build_edition(profile_name, new_toc, book_path)

        # ToDo - Delete the new_path after build?

    # Clean the book_path/_build dir to remove previous _build/html/edition/ dirs
    run(["jupyter-book", "build", book_path], check=True)

    print("Finished editions html generation")


def main(args):
    """Parse arguments and call sub-commands as appropriate."""

    # Get the arguments passed in by the user
    parser = ArgumentParser(description="Build a Jupyter Book.")
    subparsers = parser.add_subparsers()

    build_subparser = subparsers.add_parser("build")
    build_subparser.add_argument(
        "book_path", type=Path, help="the path to the root of your Jupyter Book"
    )
    build_subparser.set_defaults(func=build_all)

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
    #main(['build','master']) 
