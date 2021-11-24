#!/bin/bash
#
# Run Python unit tests

# Exit on first error
set -o errexit

# Run our unit tests with code coverage
# shellcheck disable=SC2140
coverage run -m unittest discover tests/

coverage combine

# Show the lines our tests miss
coverage report --show-missing
