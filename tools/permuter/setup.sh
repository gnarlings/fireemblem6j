#!/bin/bash
# Fetch decomp-permuter at a pinned commit and give it a private venv under tools/permuter/.cache.
set -e
here=$(cd "$(dirname "$0")" && pwd)
commit=8556c81d80d1c1af98a858c8f4dc951357f29139
mkdir -p "$here/.cache"
if [ ! -d "$here/.cache/decomp-permuter" ]; then
    git clone -q https://github.com/simonlindholm/decomp-permuter.git "$here/.cache/decomp-permuter"
fi
git -C "$here/.cache/decomp-permuter" -c advice.detachedHead=false checkout -q "$commit"
[ -x "$here/.cache/venv/bin/python" ] || python3 -m venv "$here/.cache/venv"
"$here/.cache/venv/bin/pip" install -q toml pycparser
echo "permuter ready"
