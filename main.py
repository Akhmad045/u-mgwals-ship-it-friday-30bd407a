#!/usr/bin/env python3
"""Ship It Friday — writes one funny git commit message to /output/entry.txt.

The line is a commit message an AI coding agent writes right before it
breaks production on a Friday: confident, cheerful, and completely unaware
of the disaster it is about to cause.

Stdlib only, deterministic, no network, no randomness.
"""
import hashlib
import os
import sys

ENTRY = "chore: deploy to prod at 4:59pm Friday, rollback is a Monday problem"

MAX_CHARS = 159


def validate(text):
    """Enforce the competition gate: 1-159 chars, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if len(text) == 0:
        raise ValueError("entry is empty (gate needs 1-159 characters)")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the 159-character gate"
        )
    if text.strip() == "":
        raise ValueError("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def self_test():
    """Exercise validate() against the gate's rejection cases."""
    cases = [
        ("", "empty"),
        (" ", "whitespace-only"),
        ("x" * 160, "160 chars"),
        ("a\nb", "multi-line"),
    ]
    for text, label in cases:
        try:
            validate(text)
        except ValueError as exc:
            print(f"self-test ok: rejected {label}: {exc}")
        else:
            raise SystemExit(f"self-test FAIL: {label} was accepted")
    # boundary: exactly 159 chars must pass
    validate("y" * 159)
    print("self-test ok: 159-char boundary accepted")
    print("self-test: all cases passed")
    return 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        return self_test()
    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    text = validate(ENTRY)
    data = text.encode("utf-8")
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(data)  # no trailing newline: the file is exactly the line
    with open(out_path, "rb") as fh:
        roundtrip = fh.read()
    if roundtrip != data:
        raise SystemExit("round-trip mismatch: file does not match entry")
    print(f"wrote {out_path}: {len(text)} chars, "
          f"sha256 {hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
