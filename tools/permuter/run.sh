#!/bin/bash
# usage: run.sh SRC FUNC SECONDS SEED... — start one climber per seed, splitting the cores between them
here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../.." && pwd)
src=$1; func=$2; secs=$3; shift 3
jobs=$(( $(nproc) / $# )); [ $jobs -lt 1 ] && jobs=1
cd "$repo"
for seed in "$@"; do
    name=$func-$(basename "$seed" .c)
    work=$here/work/$name
    [ -d "$work" ] && { echo "$work exists; skipping (delete it to restart)"; continue; }
    python3 "$here/prep.py" "$src" "$func" "$seed" "$work" || exit 1
    nohup "$here/climb.sh" "$work" "$secs" "$jobs" > "$here/work/$name.climb.log" 2>&1 &
    echo "started $name with -j$jobs (log: tools/permuter/work/$name.climb.log)"
done
