#!/usr/bin/env sh

set -e

pytest --cov -s
bats test/*.bats
