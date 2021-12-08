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


def generate_badge(profile_name, toc):
    """Return some badge markdown and a list of files to insert it into."""
    del profile_name
    del toc
