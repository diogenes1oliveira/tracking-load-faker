#!/usr/bin/env sh

set -e

echo 'Testing if requirements.txt needs rebuilding...'
echo

current_hash="`cat ./requirements.txt | md5sum | awk '{print $1}'`"
target_hash="`poetry export -f requirements.txt --without-hashes --dev | md5sum | awk '{print $1}'`"

if [ "$current_hash" != "$target_hash" ]; then
  echo 'requirements.txt is outdated! Run the following to update:'
  echo
  echo '    poetry export -f requirements.txt --without-hashes --dev -o requirements.txt'
  exit 1
else
  echo '    requirements.txt is updated'
fi
