# Essay Math

Word-count budget arithmetic. The word count is the part you can plan.

## What it computes

- **The budget truth** - a word total shared across sections by weight, to the word: 1000 words over weights 2, 5, 3 is 200, 500, 300.
- **The pages truth** - how many pages a word count fills: 5000 words at 275 per page is 18 full pages and 50 words, so 19 pages.
- **The daily truth** - words a day still needed to reach a target: 3200 to go over 8 days is 400 a day, rounded up.

## Boundary

Arithmetic only. Essay Math splits and counts the words, pages and days you type. It does not say how long a piece should be, whether it is good, or what a class, editor or publisher requires. You decide that.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (36 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/essaymath/
Repo: https://github.com/iLanis-agent/essaymath
