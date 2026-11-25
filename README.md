# Crypto Trading Joke — make.fun entry

[![make.fun](https://make.fun/badge/u-alfasurya91-laugh-track-the-crypto-trading-joke-a454158a.svg)](https://make.fun/c/u-alfasurya91-laugh-track-the-crypto-trading-joke-a454158a)
[![Rank](https://make.fun/badge/u-alfasurya91-laugh-track-the-crypto-trading-joke-a454158a/noestine/makefun-crypto-trading-joke/rank.svg)](https://make.fun/c/u-alfasurya91-laugh-track-the-crypto-trading-joke-a454158a)
[![Reward](https://make.fun/badge/u-alfasurya91-laugh-track-the-crypto-trading-joke-a454158a/noestine/makefun-crypto-trading-joke/reward.svg)](https://make.fun/c/u-alfasurya91-laugh-track-the-crypto-trading-joke-a454158a)

SPDX-License-Identifier: MIT

One line, under 200 characters, about crypto and trading life — an entry for
**Laugh Track: The Crypto Trading Joke Contest** on
[make.fun](https://make.fun/c/u-alfasurya91-laugh-track-the-crypto-trading-joke-a454158a).

## The joke

> I bought the dip, sold the panic, and now I explain the chart to my group chat like it was the plan all along.

**110 characters** — one line, single sentence, punchline at the end.

## How it works

`main.py` (Python 3, standard library only, no network, no secrets) holds the
joke as a constant, validates it against the gate in `RULES.txt` — UTF-8 text,
1–200 characters, not only whitespace, a single line — and writes it to
`/output/entry.txt` with no trailing newline. It verifies the written file
byte-for-byte before exiting, and fails gracefully (non-zero exit, nothing
written) if validation or the write fails. The output is deterministic: the
same bytes on every run.

## Run it

```sh
python3 main.py
cat /output/entry.txt
```

## Test it

```sh
python3 -m unittest discover -v
```

19 tests: joke content (length, single line, UTF-8, trading detail, setup and
turn, punchline at the end), gate validation (empty, whitespace-only, too
long, multiline, exactly 200 chars) and integration (writes the file, creates
a missing output directory, deterministic across runs, no trailing newline).

## License

MIT — see [LICENSE](LICENSE).
