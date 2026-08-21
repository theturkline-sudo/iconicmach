# -*- coding: utf-8 -*-
"""Audit a blog article against the SEO angles we care about.

    python scripts/seo_audit.py ar water-bottling-line
    python scripts/seo_audit.py ar            # every Arabic article

Checks are deliberately mechanical. They catch the things that are easy to get
wrong and expensive to notice later; they cannot judge whether the writing is
any good. Exit code is 1 if any FAIL, so this can gate a commit.
"""

from __future__ import print_function

import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import articles as articles_mod  # noqa: E402

# Windows consoles default to cp1252, which cannot encode Arabic — and this
# tool exists to report on Arabic articles.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:  # Python 2 / older io stacks
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Derived from what actually ranks for these queries in Arabic: the top result
# for "خطوط إنتاج المياه المعدنية" runs ~3,000 words over 11 H2s with an FAQ.
MIN_WORDS = 900
TARGET_WORDS = 1500
MIN_H2 = 5
MIN_INTERNAL_LINKS = 3
MAX_TITLE = 60
MAX_EXCERPT = 160

MONEY_PAGES = ("production-lines", "conveyor-systems", "spare-parts",
               "request-quotation", "services", "technical-support", "contact")


class Report(object):
    def __init__(self, name):
        self.name = name
        self.rows = []

    def add(self, status, angle, detail):
        self.rows.append((status, angle, detail))

    def ok(self, angle, detail):
        self.add("PASS", angle, detail)

    def warn(self, angle, detail):
        self.add("WARN", angle, detail)

    def fail(self, angle, detail):
        self.add("FAIL", angle, detail)

    @property
    def failed(self):
        return any(r[0] == "FAIL" for r in self.rows)

    def render(self):
        print("\n" + self.name)
        print("-" * len(self.name))
        for status, angle, detail in self.rows:
            print("  [{:<4}] {:<22} {}".format(status, angle, detail))


def words(html):
    text = re.sub(r"<[^>]+>", " ", html)
    return [w for w in re.split(r"\s+", text) if w.strip()]


def audit(lang, article):
    r = Report("{} / {}".format(lang, article["slug"]))
    body = article["body"]
    kw = (article.get("target_keyword") or "").strip()

    # --- angle 1: depth ------------------------------------------------------
    n = len(words(body))
    if n < MIN_WORDS:
        r.fail("depth", "{} words — below the {} minimum".format(n, MIN_WORDS))
    elif n < TARGET_WORDS:
        r.warn("depth", "{} words — under the {} target".format(n, TARGET_WORDS))
    else:
        r.ok("depth", "{} words".format(n))

    # --- angle 2: structure --------------------------------------------------
    h2 = re.findall(r"<h2[^>]*>(.*?)</h2>", body, re.S)
    h3 = re.findall(r"<h3[^>]*>(.*?)</h3>", body, re.S)
    if len(h2) < MIN_H2:
        r.fail("structure", "{} H2s — need at least {}".format(len(h2), MIN_H2))
    else:
        r.ok("structure", "{} H2, {} H3".format(len(h2), len(h3)))

    if re.search(r"<h1", body):
        r.fail("structure", "body contains an H1 — the page template owns the H1")

    # --- angle 3: keyword placement -----------------------------------------
    if not kw:
        r.warn("keyword", "no target_keyword set — cannot check placement")
    else:
        # Case-insensitive: "Water Bottling Line" in a title must match a
        # lower-case target keyword. Arabic has no case, so this is a no-op
        # there and only ever helps the Latin-script checks.
        k = kw.lower()
        in_title = k in article["title"].lower()
        in_excerpt = k in article["excerpt"].lower()
        first_chunk = " ".join(words(body)[:120]).lower()
        in_intro = k in first_chunk
        in_h2 = any(k in h.lower() for h in h2)
        hits = body.lower().count(k)
        density = hits / float(max(n, 1)) * 100

        placed = [x for x, ok in (("title", in_title), ("excerpt", in_excerpt),
                                  ("intro", in_intro), ("an H2", in_h2)) if ok]
        missing = [x for x, ok in (("title", in_title), ("excerpt", in_excerpt),
                                   ("intro", in_intro), ("an H2", in_h2)) if not ok]
        if missing:
            r.warn("keyword", "'{}' missing from: {}".format(kw, ", ".join(missing)))
        else:
            r.ok("keyword", "'{}' in title, excerpt, intro and an H2".format(kw))

        if density > 3:
            r.fail("keyword density", "{:.1f}% — reads as stuffing".format(density))
        elif hits == 0:
            r.fail("keyword density", "target keyword never appears in the body")
        else:
            r.ok("keyword density", "{} mentions ({:.1f}%)".format(hits, density))

    # --- angle 4: answer targeting (snippets + AI assistants) ----------------
    if article.get("faq"):
        r.ok("answer targeting", "{} FAQ entries -> FAQPage schema".format(len(article["faq"])))
    else:
        r.warn("answer targeting", "no faq[] — loses FAQPage schema and AI citations")

    if re.search(r"<(ul|ol)\b", body):
        r.ok("scannability", "has lists")
    else:
        r.warn("scannability", "no lists — harder to win a featured snippet")

    if re.search(r"<table\b", body):
        r.ok("scannability", "has a table")

    # --- angle 5: internal linking ------------------------------------------
    links = re.findall(r'href="([^"]+)"', body)
    internal = [l for l in links if not l.startswith(("http", "mailto:", "tel:", "#"))]
    money = [l for l in internal if any(m in l for m in MONEY_PAGES)]
    if len(internal) < MIN_INTERNAL_LINKS:
        r.fail("internal links", "{} — need at least {}".format(len(internal), MIN_INTERNAL_LINKS))
    elif not money:
        r.warn("internal links", "{} links but none to a product or quote page".format(len(internal)))
    else:
        r.ok("internal links", "{} internal, {} to money pages".format(len(internal), len(money)))

    for l in internal:
        if l.endswith(".html"):
            r.fail("internal links", "{} uses .html — the server 307-redirects those".format(l))

    # --- angle 6: metadata ---------------------------------------------------
    if len(article["title"]) > MAX_TITLE:
        r.warn("metadata", "title {} chars — Google truncates near {}".format(len(article["title"]), MAX_TITLE))
    else:
        r.ok("metadata", "title {} chars".format(len(article["title"])))

    if len(article["excerpt"]) > MAX_EXCERPT:
        r.warn("metadata", "excerpt {} chars — over {}".format(len(article["excerpt"]), MAX_EXCERPT))
    else:
        r.ok("metadata", "excerpt {} chars".format(len(article["excerpt"])))

    # --- angle 7: media ------------------------------------------------------
    img = os.path.join(ROOT, "assets", "images", article["image"].rsplit("/", 1)[-1])
    if not os.path.exists(img):
        r.fail("media", "hero image not found: {}".format(article["image"]))
    else:
        r.ok("media", "hero image present")

    for tag in re.findall(r"<img[^>]*>", body):
        if "alt=" not in tag:
            r.fail("media", "an inline <img> has no alt attribute")

    # --- angle 8: language ---------------------------------------------------
    arabic = len(re.findall(r"[؀-ۿ]", re.sub(r"<[^>]+>", "", body)))
    latin = len(re.findall(r"[A-Za-z]", re.sub(r"<[^>]+>", "", body)))
    if lang == "ar":
        if arabic < latin:
            r.fail("language", "more Latin than Arabic characters — is this the right file?")
        else:
            r.ok("language", "Arabic body ({} Arabic chars)".format(arabic))
    else:
        if arabic > latin:
            r.fail("language", "more Arabic than Latin characters in an English article")
        else:
            r.ok("language", "English body")

    # --- angle 9: translation parity ----------------------------------------
    other = "en" if lang == "ar" else "ar"
    twin = os.path.join(ROOT, "content", other, article["slug"] + ".json")
    if os.path.exists(twin):
        r.ok("parity", "{} counterpart exists -> hreflang pairs up".format(other))
    else:
        r.warn("parity", "no {} counterpart — the hreflang link will 404".format(other))

    return r


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2

    lang = args[0]
    wanted = args[1] if len(args) > 1 else None
    found = [a for a in articles_mod.load(lang) if wanted is None or a["slug"] == wanted]

    if not found:
        print("no article matched: {} {}".format(lang, wanted or ""))
        return 2

    failed = False
    for a in found:
        rep = audit(lang, a)
        rep.render()
        failed = failed or rep.failed

    print("\n{} article(s) audited. {}".format(
        len(found), "FAILURES PRESENT" if failed else "no failures"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
