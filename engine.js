// Essay Math engine - word-count budget arithmetic for writers.
// Mirrored by oracle.py; keep the op order identical.
// Everything is whole words, whole pages and whole days.

function _whole(x, lo, hi, msg) {
  if (!Number.isInteger(x) || x < lo || x > hi) throw new Error(msg);
  return x;
}

function _words(x, label, lo) {
  return _whole(x, lo, 10000000, label + " must be a whole number from " + lo + " to 10000000");
}

function _plural(n, word) {
  return n + " " + word + (n === 1 ? "" : "s");
}

// The budget truth: a word total shared across sections by weight, to the word.
function budgetTruth(total, list) {
  var t = _words(total, "total words", 1);
  var parts = String(list).split(",").map(function (p) { return p.trim(); });
  if (parts.length < 2 || parts.length > 12) throw new Error("enter 2 to 12 weights separated by commas");
  var ws = parts.map(function (p) {
    if (!/^[0-9]+$/.test(p) || parseInt(p, 10) > 1000) throw new Error("each weight must be a whole number from 0 to 1000");
    return parseInt(p, 10);
  });
  var s = ws.reduce(function (a, b) { return a + b; }, 0);
  if (s <= 0) throw new Error("weights must add up to more than 0");
  var base = ws.map(function (w) { return Math.floor(t * w / s); });
  var rem = ws.map(function (w) { return (t * w) % s; });
  var left = t - base.reduce(function (a, b) { return a + b; }, 0);
  var order = ws.map(function (_, i) { return i; }).sort(function (a, b) { return rem[b] - rem[a] || a - b; });
  for (var k = 0; k < left; k++) base[order[k]] += 1;
  return "Total " + _plural(t, "word") + " over weights " + ws.join(", ") + ": " + base.join(", ") + " per section.";
}

// The pages truth: how many pages a word count fills at a words-per-page figure.
function pagesTruth(words, perPage) {
  var w = _words(words, "words", 1);
  var p = _whole(perPage, 1, 100000, "words per page must be a whole number from 1 to 100000");
  var full = Math.floor(w / p), rem = w % p;
  var head = _plural(w, "word") + " at " + p + " per page: ";
  if (rem === 0) return head + _plural(full, "page") + " exactly.";
  return head + _plural(full, "full page") + " and " + _plural(rem, "word") + ", so " + _plural(full + 1, "page") + ".";
}

// The daily truth: words a day still needed to reach a target.
function dailyTruth(target, written, days) {
  var t = _words(target, "target", 1);
  var w = _words(written, "words written", 0);
  var d = _whole(days, 1, 3660, "days left must be a whole number from 1 to 3660");
  var togo = t > w ? t - w : 0;
  var head = "Target " + t + ", written " + w + ", " + _plural(d, "day") + " left: " + _plural(togo, "word") + " to go";
  if (togo === 0) return head + (w > t ? ", " + (w - t) + " over." : ".");
  return head + ", " + Math.floor((togo + d - 1) / d) + " a day (rounded up).";
}
