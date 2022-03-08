# How to set up environment to use "add-persona" feature

![Codestyle Black](https://img.shields.io/badge/code%20style-black-000000.svg)

**See [User Guide for Turing Way Pathways](documentation.md) for details on how to use this package for *[The Turing Way](https://github.com/alan-turing-institute/the-turing-way)***.

---

## Instructions

### Install

#### Users

1. Clone the source code with `git clone git@github.com:alan-turing-institute/bio-Turing-Way`
1. Change to the source code directory with `cd bio-Turing-Way/`
1. Install with `pip install pathways/` (the `/` is mandatory)
2. Install jupyter-book dependencies with `pip install -r master/requirements.txt`

#### Developers

1. Clone the source code with `git clone git@github.com:alan-turing-institute/bio-Turing-Way`
1. Change to the source code directory with `cd bio-Turing-Way/pathways`
1. Install Poetry
1. Create a poetry environment and install dependencies with `poetry install`
1. Install Git pre-commit hooks by installing Pre-Commit and then running `pre-commit install`

### Run

1. With pathways installed, you can run `python -m pathways.main --help` for help.
2. Run `python -m pathways.main pathways master` to create a new book with personas.

### Testing

1. Run unit tests from the pathways/ directory with `./run_tests.sh`
1. Run static check pre-commit hooks with `pre-commit run [hook-id]`
