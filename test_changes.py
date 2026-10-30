"""Fail if the three ranked lines of `python3 changes.py` change."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EXPECTED = [
    "1. route  BE-BE    25 ->   60  +35",
    "2. route  NL-BE    77 ->  101  +24",
    "3. route  BE-FR    71 ->   48  -23",
]


def test_three_lines_unchanged():
    result = subprocess.run(
        [sys.executable, "changes.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    # The first line is the header; everything after it must match exactly.
    assert result.stdout.splitlines()[1:] == EXPECTED
