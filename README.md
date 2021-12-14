# My Jupyter Book

![Codestyle Black](https://img.shields.io/badge/code%20style-black-000000.svg)

----------------------------------------------------------------

## Instructions

### Install

1. Clone the source code with `git clone git@github.com:alan-turing-institute/bio-Turing-Way`
1. Change to the source code directory with `cd bio-Turing-Way`
1. Set Python 3.8 as the local version to use with `pyenv local 3.8.12`
1. Make a Python 3.8 virtual environment with `virtualenv venv`
1. Activate it with `source venv/bin/activate`

#### Developers

1. Additionally, developers should install pre-commit hooks with `pre-commit install`

### Run

1. Since our code modifies the source Markdown files, and you won't want to commit those changes, make a copy with, for example, `cp -r master/ master_copy/`
1. Add the pathways from profiles.yml with `python -m main pathways master_copy/`
1. Build the book with `jupyter-book build master_copy`
1. Change to the `html` directory with `cd mynewbook/_build/html`
1. Serve it (for development) with `python -m http.server`
