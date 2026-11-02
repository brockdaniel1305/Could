#!/bin/sh
# Rebuild every scene of this episode from its source script.
cd "$(dirname "$0")" && for f in s[0-9]*.py; do python3 "$f"; done
