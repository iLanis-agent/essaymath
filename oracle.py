#!/usr/bin/env python3
# Essay Math oracle - mirrors engine.js.
import json, re

def _whole(x, lo, hi, msg):
    if not isinstance(x, int) or x < lo or x > hi:
        raise ValueError(msg)
    return x

def _words(x, label, lo):
    return _whole(x, lo, 10000000, f"{label} must be a whole number from {lo} to 10000000")

def _plural(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")

def budget_truth(total, lst):
    t = _words(total, "total words", 1)
    parts = [p.strip() for p in str(lst).split(",")]
    if len(parts) < 2 or len(parts) > 12:
        raise ValueError("enter 2 to 12 weights separated by commas")
    ws = []
    for p in parts:
        if not re.fullmatch(r"[0-9]+", p) or int(p) > 1000:
            raise ValueError("each weight must be a whole number from 0 to 1000")
        ws.append(int(p))
    s = sum(ws)
    if s <= 0:
        raise ValueError("weights must add up to more than 0")
    base = [t * w // s for w in ws]
    rem = [(t * w) % s for w in ws]
    left = t - sum(base)
    order = sorted(range(len(ws)), key=lambda i: (-rem[i], i))
    for k in range(left):
        base[order[k]] += 1
    return (f"Total {_plural(t, 'word')} over weights {', '.join(str(w) for w in ws)}: "
            f"{', '.join(str(b) for b in base)} per section.")

def pages_truth(words, per_page):
    w = _words(words, "words", 1)
    p = _whole(per_page, 1, 100000, "words per page must be a whole number from 1 to 100000")
    full, rem = divmod(w, p)
    head = f"{_plural(w, 'word')} at {p} per page: "
    if rem == 0:
        return head + f"{_plural(full, 'page')} exactly."
    return head + f"{_plural(full, 'full page')} and {_plural(rem, 'word')}, so {_plural(full + 1, 'page')}."

def daily_truth(target, written, days):
    t = _words(target, "target", 1)
    w = _words(written, "words written", 0)
    d = _whole(days, 1, 3660, "days left must be a whole number from 1 to 3660")
    togo = t - w if t > w else 0
    head = f"Target {t}, written {w}, {_plural(d, 'day')} left: {_plural(togo, 'word')} to go"
    if togo == 0:
        return head + (f", {w - t} over." if w > t else ".")
    return head + f", {(togo + d - 1) // d} a day (rounded up)."

FNS = {"budgetTruth": budget_truth, "pagesTruth": pages_truth, "dailyTruth": daily_truth}

CASES = [
    ("budgetTruth", [1000, "2, 5, 3"]), ("budgetTruth", [100, "1,1,1"]), ("budgetTruth", [1, "1,1"]),
    ("budgetTruth", [1000, "30, 0"]), ("budgetTruth", [5000, "1, 2, 3, 4"]), ("budgetTruth", [1000, "7"]),
    ("budgetTruth", [1000, "0, 0"]), ("budgetTruth", [1000, "2, x"]), ("budgetTruth", [1000, "2, 1001"]),
    ("budgetTruth", [1000, "1,2,3,4,5,6,7,8,9,10,11,12,13"]), ("budgetTruth", [0, "1, 1"]), ("budgetTruth", [1000.5, "1, 1"]),
    ("budgetTruth", [10000001, "1, 1"]), ("budgetTruth", [1000, "010, 5"]), ("budgetTruth", [1000, "1, , 1"]),
    ("pagesTruth", [5000, 250]), ("pagesTruth", [5000, 275]), ("pagesTruth", [250, 250]), ("pagesTruth", [251, 250]),
    ("pagesTruth", [1, 250]), ("pagesTruth", [300, 299]), ("pagesTruth", [0, 250]), ("pagesTruth", [5000, 0]),
    ("pagesTruth", [5000, 100001]), ("pagesTruth", [5000.5, 250]),
    ("dailyTruth", [5000, 1800, 8]), ("dailyTruth", [5000, 4999, 3]), ("dailyTruth", [5000, 0, 1]),
    ("dailyTruth", [5000, 5000, 4]), ("dailyTruth", [5000, 5200, 8]), ("dailyTruth", [5000, 5001, 1]),
    ("dailyTruth", [5000, 1800, 0]), ("dailyTruth", [5000, 1800, 3661]), ("dailyTruth", [0, 0, 5]),
    ("dailyTruth", [5000, -1, 5]), ("dailyTruth", [5000, 1800.5, 5]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
