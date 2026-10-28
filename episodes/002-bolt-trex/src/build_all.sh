#!/bin/sh
# Rebuild every scene of this episode from its source script.
cd "$(dirname "$0")" && for f in s*.py; do python3 "$f"; done
