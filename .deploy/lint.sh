#!/bin/sh

set -e

echo 'Linting with flake8...'

flake8

echo '    no linting issues found'
