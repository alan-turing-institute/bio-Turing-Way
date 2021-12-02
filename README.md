# My Jupyter Book

![Codestyle Black](https://img.shields.io/badge/code%20style-black-000000.svg)

----------------------------------------------------------------

## Instructions

### Install

1. Clone the source code with `git clone git@github.com:Iain-S/my_jupyter_book.git`
1. Change to the source code directory with `cd my_jupyter_book`
1. Set Python 3.8 as the local version to use with `pyenv local 3.8.12`
1. Make a Python 3.8 virtual environment with `virtualenv venv`
1. Activate it with `source venv/bin/activate`
1. Install pre-commit hooks with `pre-commit install`

### Run

1. Build our example book with `jupyter-book build mynewbook`
1. Build our other editions with `python -m main build mynewbook`
1. Change to the `html` directory with `cd mynewbook/_build/html`
1. Serve it (for development) with `python -m http.server`
