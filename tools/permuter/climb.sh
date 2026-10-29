#!/bin/bash
# usage: climb.sh WORKDIR SECONDS JOBS — rerun the permuter from each new non-fakematch best until a zero or time runs out
here=$(cd "$(dirname "$0")" && pwd)
permuter=${PERMUTER_DIR:-$here/.cache/decomp-permuter}
python=${PERMUTER_PYTHON:-$here/.cache/venv/bin/python}
dir=$(cd "$1" && pwd); total=$2; jobs=${3:-4}
end=$((SECONDS + total)); gen=0

best() {
    for o in $(ls "$dir" | grep '^output-' | sort -t- -k2 -n); do
        python3 "$here/ishack.py" "$dir/$o/source.c" || { echo "$o"; return; }
    done
}

while [ $((end - SECONDS)) -gt 30 ]; do
    gen=$((gen + 1))
    (cd "$permuter" && exec timeout $((end - SECONDS)) "$python" permuter.py "$dir" -j"$jobs" --stop-on-zero) > "$dir/run.log" 2>&1 &
    pid=$!
    base=""
    until [ -n "$base" ] || ! kill -0 $pid 2>/dev/null; do
        sleep 2
        base=$(grep -o 'base score = [0-9]*' "$dir/run.log" | grep -o '[0-9]*$')
    done
    [ -z "$base" ] && { echo "$(date +%T) permuter failed to start; see $dir/run.log"; exit 1; }
    echo "$(date +%T) gen $gen base=$base"
    [ "$base" = 0 ] && { kill $pid; echo "ZERO $dir/base.c"; exit 0; }
    while kill -0 $pid 2>/dev/null; do
        o=$(best)
        b=${o#output-}; b=${b%%-*}
        if [ -n "$o" ] && [ "$b" -lt "$base" ]; then
            kill $pid; wait $pid 2>/dev/null
            mkdir -p "$dir/gen-$gen"
            mv "$dir/base.c" "$dir"/output-* "$dir/run.log" "$dir/gen-$gen/"
            cp "$dir/gen-$gen/$o/source.c" "$dir/base.c"
            echo "$(date +%T) gen $gen: $base -> $b"
            [ "$b" = 0 ] && { echo "ZERO $dir/base.c"; exit 0; }
            break
        fi
        sleep 10
    done
done
echo "$(date +%T) out of time"
