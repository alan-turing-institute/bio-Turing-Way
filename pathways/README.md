# My Jupyter Book

![Codestyle Black](https://img.shields.io/badge/code%20style-black-000000.svg)

----------------------------------------------------------------

## Instructions

### Install

#### Users

1. Clone the source code with `git clone git@github.com:alan-turing-institute/bio-Turing-Way`
1. Change to the source code directory with `cd bio-Turing-Way/`
1. Install with `pip install pathways/` (the `/` is mandatory)

#### Developers

1. Clone the source code with `git clone git@github.com:alan-turing-institute/bio-Turing-Way`
1. Change to the source code directory with `cd bio-Turing-Way/pathways`
1. Install Poetry
1. Create a poetry environment and install dependencies with `poetry install`
1. Install Git pre-commit hooks by installing Pre-Commit and then running `pre-commit install`

### Run

1. With pathways installed, you can run with `python -m pathways.main --help`

### Testing

1. Run unit tests from the pathways/ directory with `./run_tests.sh`
1. Run static check pre-commit hooks with `pre-commit run [hook-id]`
