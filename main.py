"""The Funniest AI Out-of-Office Reply — entry program.

Scores several original out-of-office auto-reply candidates against the
judge's published criteria (most important first) and writes the winning
one line to /output/entry.txt. The gate requires 1-160 UTF-8 characters.
"""

import os

# Judge criteria weights, in the judge brief's order:
# 1. on-subject out-of-office auto-reply from an AI agent on vacation (5)
# 2. lands a real laugh on first read, surprising turn (4)
# 3. sounds like a machine talking about itself (3)
# 4. reads as one clean line that sounds like a real auto-reply (2)
# 5. fresh, steering clear of beach / inbox / back-soon cliches (1)
WEIGHTS = (5, 4, 3, 2, 1)

CANDIDATES = [
    # (line, scores per criterion 1-5, each 0-10)
    (
        "I'm on vacation. I left a toaster in charge of my inbox - it toasted "
        "your email, so please resend it, lightly buttered.",
        (10, 9, 6, 9, 9),
    ),
    (
        "I'm away. My backup model read one email, panicked, and has been "
        "buffering ever since - please try again when it calms down.",
        (10, 8, 9, 8, 8),
    ),
    (
        "I'm on holiday. My training data ends before your email arrived, so "
        "technically we have never met, and I plan to keep it that way.",
        (10, 8, 10, 7, 8),
    ),
    (
        "I'm out until my context window refreshes. Until then, every reply "
        "you get is just me guessing what a professional sounds like.",
        (10, 7, 10, 8, 7),
    ),
    (
        "I'm on vacation. My out-of-office reply is also on vacation, so this "
        "is a temp - it has no idea what it is doing either.",
        (10, 7, 7, 9, 6),
    ),
    (
        "I'm away. I left my judgment at the office, so if this reply sounds "
        "unhinged, that is just my intern model covering for me.",
        (10, 7, 8, 8, 7),
    ),
]


def score(line_scores):
    return sum(w * s for w, s in zip(WEIGHTS, line_scores))


def valid(line):
    """The sealed gate: 1-160 UTF-8 chars, not only whitespace."""
    return 1 <= len(line) <= 160 and line.strip() != ""


def main():
    pool = [(line, scores) for line, scores in CANDIDATES if valid(line)]
    assert pool, "no candidate passes the gate"
    ranked = sorted(
        ((score(scores), len(line), line) for line, scores in pool),
        # Highest score wins; on a tie the shorter line wins (smaller Size
        # is the tie-break the rules use after playoff games).
        key=lambda item: (item[0], -item[1]),
        reverse=True,
    )
    for points, size, line in ranked:
        print(f"{points:3d} pts | {size:3d} chars | {line}")
    winner = ranked[0][2]
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(winner)
    print("WINNER:", winner)


if __name__ == "__main__":
    main()
