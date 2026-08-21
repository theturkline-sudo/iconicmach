---
name: arabic-blog
description: Research the Arabic Google SERP for a target keyword, extract the structure of the pages that already rank, and write a competitive Arabic article for iconicmach.com with full SEO scaffolding. Use when asked to write a blog post, add an article, target a keyword, or improve blog rankings.
---

# Arabic blog workflow — iconicmach.com

Write an Arabic article that can compete with what already ranks, rather than
one that merely reads well. Every step below produces something checkable.

Never skip step 1. Writing before looking at the SERP is how you end up with a
520-word post competing against 3,000-word pages — which is exactly what the
first three articles on this site did.

---

## 1. Read the SERP

```
WebSearch: <target keyword in Arabic>
```

Run the query in Arabic, not translated from English. Arabic searchers use
different phrasing than the literal translation, and Egyptian usage often
differs from Gulf usage (`ماكينة` vs `آلة`, `خط إنتاج` vs `خط تعبئة`).

Record the top 5-8 results. Note which are:

- **manufacturers/suppliers** — the direct competitors
- **feasibility-study or "مشروع" sites** — these signal commercial intent
- **marketplaces** (Alibaba, made-in-china) — usually beatable on depth

## 2. Extract the winning structure

Pick the 2-3 strongest non-marketplace results and, for each:

```
WebFetch: <url>
prompt: List every H2 and H3 heading in order, exactly as written in Arabic.
        Then report: approximate word count, whether there is an FAQ section,
        whether there are numbered lists or tables, and whether the article
        ends with a call to action. Do not summarise the content.
```

Build a table of their headings side by side. You are looking for:

- **the common spine** — headings that appear in every competitor. These are
  the questions Google has decided the query means. Cover all of them.
- **the gaps** — a question one competitor answers and the others miss, or a
  question none answers. This is where the article earns its ranking.
- **the length bar** — do not aim for the average; aim for the top result.

**Reference measurement.** For `خطوط إنتاج المياه المعدنية` the leading result
runs ~3,000 words across 11 H2s and 7 H3s, with an FAQ section, heavy bullet
lists, no tables, and a WhatsApp CTA at the end.

## 3. Write the brief, then the article

Create `content/ar/<slug>.json` (see `articles.py` for the schema).

Rules that come from this site specifically:

- **Arabic first.** Write in Arabic. Do not draft in English and translate —
  it reads translated, and it loses the phrasing real searchers use.
- **Modern Standard Arabic**, with Egyptian industry terms where the trade
  actually uses them. The audience is factory owners and plant engineers.
- **Cover the common spine, then add the gap.** Matching alone ties; the gap
  is the reason to rank above.
- **Answer the query in the first 120 words.** Featured snippets and AI
  assistants both lift the opening. Do not warm up.
- **`faq[]` is not optional.** It generates FAQPage schema and is the single
  biggest lever for AI-assistant citations now that the AI crawlers are
  unblocked. Take the questions from the "People also ask" box and from what
  competitors put in their own FAQ.
- **At least 3 internal links**, one of which must reach a money page:
  `production-lines`, `conveyor-systems`, `spare-parts`, `request-quotation`,
  `services`, `technical-support`, `contact`. Extensionless — no `.html`.
- **No invented numbers.** No fake case studies, no statistics without a
  source, no client names. Ranges framed as typical engineering practice are
  fine; fabricated specifics are not.
- **No H1 in the body.** The page template owns it.

Write the English counterpart at `content/en/<slug>.json` with the same slug,
or the hreflang pair will point at a 404. It should be a genuine English
article on the same topic, not a machine translation.

## 4. Audit

```bash
python scripts/seo_audit.py ar <slug>
```

Nine angles: depth, structure, keyword placement, keyword density, answer
targeting, scannability, internal links, metadata, media, language, and
translation parity. Fix every `FAIL`. Justify or fix every `WARN`.

The audit is mechanical — it cannot tell you whether the writing is any good.
Read the draft yourself before shipping it.

## 5. Build, verify, ship

```bash
python generate_ar.py && python generate_en.py && python generate_sitemap.py
python scripts/seo_audit.py ar && python scripts/seo_audit.py en
```

Then check the rendered page: the article resolves, the FAQ accordion opens,
JSON-LD parses and contains `BlogPosting` + `FAQPage` + `BreadcrumbList`, and
the Arabic page renders `dir="rtl"` with no horizontal overflow.

Commit and push to `main`; Cloudflare builds automatically. Afterwards, request
indexing for the new URL in Search Console rather than waiting for a crawl.

---

## The SEO angles, and why each is here

| Angle | What it wins |
|---|---|
| Topical spine from the SERP | Relevance for the head term |
| Gap coverage | The reason to outrank, not just match |
| Depth to the top result's bar | Competes on the axis Google already rewards |
| `faq[]` -> FAQPage schema | Rich results, People-also-ask, AI citations |
| Answer in the first 120 words | Featured snippet, AI answer extraction |
| Lists and tables | Snippet formats Google lifts directly |
| Internal links to money pages | Moves crawl equity and readers toward quotes |
| `BlogPosting` + `BreadcrumbList` | Article rich results, site-tree understanding |
| hreflang pair (ar + en) | Both language markets, no duplicate-content split |
| Extensionless URLs | No redirect hop; hreflang is honoured |

## Files

- `articles.py` — loads `content/<lang>/*.json`, builds FAQ HTML and schema
- `content/<lang>/<slug>.json` — one article
- `scripts/seo_audit.py` — the gate
- `generate_ar.py` / `generate_en.py` — render pages; do not put article text in them
