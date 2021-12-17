#!/bin/bash
#
# Run Python unit tests

# Exit on first error
set -o errexit

# Run our unit tests with code coverage
# shellcheck disable=SC2140
python -m coverage run -m unittest discover tests/

python -m coverage combine

# Show the lines our tests miss
python -m coverage report --show-missing
