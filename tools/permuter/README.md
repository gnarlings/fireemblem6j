# Permuter harness

Runs [decomp-permuter](https://github.com/simonlindholm/decomp-permuter) as hill-climbers against a nonmatching function.

## Current target

`func_fe6_08076060` in `src/unitlistscreen.c` (the page-scroll proc step). It is still naked asm under `NONMATCHING`.

- `seeds/func_fe6_08076060/fe7u_port.c`: FE7U's matched `sub_0808A92C` (`fireemblem7u/src/unitlistscreen.c`) ported over, with plain C in place of its `({ })` statement expressions. Score 5855.
- `p2b_65.c`: the closest so far (65; only `r8`/`sl`/`ip` rotation left), with `({ })` offsets and `do { } while (0)` around the else branch.
- `p2g_645.c` and `p2g_635.c`: the best results without either construct (645 and 635).
- `p2h_1395.c`: descended from `fe7u_port.c`, using a permuter-made `inline_fn` helper.

Code that a macro could plausibly have expanded to is fair game: `({ })`, `do { } while (0)` and inline helpers. `volatile`, `register` and `asm` are not; they don't belong in production code. The sibling `func_fe6_08075E94` matched in plain C once `off` became `u16`, so a small type or temporary change is the likely fix.

## Setup

Build the repo first (see the top-level README) and confirm `make compare` prints `fe6.gba: OK`. Then:

```
tools/permuter/setup.sh
```

## Run

```
tools/permuter/run.sh src/unitlistscreen.c func_fe6_08076060 28800 tools/permuter/seeds/func_fe6_08076060/*.c
```

This starts one climber per seed for 8 hours and splits `nproc` cores between them. Each climber lives in `tools/permuter/work/<func>-<seed>/`. When a candidate beats the current base, the climber restarts the permuter from it and archives the previous generation in `gen-N/`. Candidates with `volatile`, `register` or `asm` in the target function are still saved but never become a base (`ishack.py`).

Add climbers when a run's best turns hacky but an earlier result is still clean: copy that `source.c` into `seeds/` and pass it to `run.sh`. Retire runs that stall; a fixed hacky base rarely recovers.

## Watch

```
tail -f tools/permuter/work/*.climb.log
tools/permuter/viz/server.py 8765          # http://127.0.0.1:8765/, a best-score chart for every run in work/
```

Lower scores are better and 0 is a match. Scores are weighted: 5 per register difference, 100 per inserted or deleted instruction.

## Verify a result

```
tools/permuter/verify.py src/unitlistscreen.c func_fe6_08076060 tools/permuter/work/<run>/base.c --keep
```

This splices the candidate over the function's `NONMATCHING` block, runs `make compare`, and keeps the change only if the ROM matches. Then tidy the candidate into the file's style (the permuter prints macro-expanded C) and rebuild. Set `MAKE_ARGS=".SHELLFLAGS='-O xpg_echo -c'"` if `/bin/sh` is bash.

## Gotchas

- The permuter's pycparser can't parse `({ })` or `__attribute__`. `prep.py` strips attributes and wraps each line holding `({ })` in `PERM_IGNORE`, so such a line must hold one whole statement. The permuter leaves those lines alone.
- `prep.py` and `verify.py` take a seed's last function plus any `inline_fn` helpers; other globals the permuter adds are dropped.
- The permuter compiles with the repo's `-Werror` flags, so candidates that wouldn't build in the repo are rejected.
- The permuter diffs whole objects, so `prep.py` reduces both `target.o` and `base.c` to the one function. Don't hand it a full TU.
- The permuter writes temp files to `/tmp`; keep a few GB free there.
