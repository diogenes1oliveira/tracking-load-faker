#!/bin/sh

set -e

if [ "$#" -eq 1 ] || [ "`head -c "$1"`" = '-' ]; then
  exec locust-tracking-load-faker "$@"
else
  exec "$@"
fi
