"""Laugh Track: The Crypto Trading Joke Contest.

Writes one line — a single joke about crypto and trading life — to
/output/entry.txt, per RULES.txt.

Gate: the file must be UTF-8 text of 1-200 characters, not only whitespace.
The joke is validated against that gate before anything is written, so an
invalid entry can never be produced. Stdlib only, no network, no secrets,
deterministic: the same bytes on every run.
"""

import os
import sys

JOKE = ("I bought the dip, sold the panic, and now I explain the chart "
        "to my group chat like it was the plan all along.")

DEFAULT_OUTPUT = "/output/entry.txt"
MAX_CHARS = 200


def validate(text):
    """Return True only if text passes the gate in RULES.txt."""
    if not isinstance(text, str):
        return False
    if not text or not text.strip():
        return False
    if len(text) > MAX_CHARS:
        return False
    if "\n" in text or "\r" in text:
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def main():
    if not validate(JOKE):
        print("error: joke fails the gate (1-200 chars, single line, "
              "not only whitespace)", file=sys.stderr)
        return 1
    output_path = os.environ.get("ENTRY_OUTPUT", DEFAULT_OUTPUT)
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    try:
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            f.write(JOKE)
        # Post-write verification: re-read what landed on disk and confirm
        # it is byte-for-byte the validated joke. A partial write or an
        # encoding surprise must fail loudly instead of shipping a bad file.
        with open(output_path, "r", encoding="utf-8", newline="") as f:
            written = f.read()
    except OSError as exc:
        print(f"error: cannot write {output_path}: {exc}", file=sys.stderr)
        return 1
    if written != JOKE or not validate(written):
        print("error: written file failed post-write verification",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
