"""Blog articles, loaded from content/<lang>/*.json.

Articles used to be Python literals inside generate_en.py / generate_ar.py.
That made them impossible to add without editing a 1,200-line generator, so
they now live as data files that tooling can create and validate.

Each file looks like:

    {
      "slug":        "conveyor-belt-types",      -> /ar/blog-conveyor-belt-types
      "category":    "الصيانة",
      "title":       "...",
      "excerpt":     "...",                       -> meta description + card text
      "image":       "industrial-process-7.jpeg", -> filename only, under assets/images
      "date":        "2026-08-16",                -> ISO, drives sort order
      "date_label":  "١٦ أغسطس ٢٠٢٦",             -> displayed
      "read":        "٨ دقائق قراءة",
      "target_keyword": "أنواع السيور الناقلة",
      "faq":  [{"q": "...", "a": "..."}],         -> optional, becomes FAQPage schema
      "body": "<p>...</p>"                        -> article HTML
    }

Newest first, so the blog listing needs no manual reordering.
"""

import glob
import io
import json
import os

CONTENT_DIR = "content"

REQUIRED = ("slug", "category", "title", "excerpt", "image", "date", "date_label", "read", "body")


def _path(lang):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), CONTENT_DIR, lang)


def load(lang):
    """Every article for a language, newest first."""
    out = []
    for f in sorted(glob.glob(os.path.join(_path(lang), "*.json"))):
        with io.open(f, encoding="utf-8") as fh:
            try:
                a = json.load(fh)
            except ValueError as e:
                raise ValueError("{} is not valid JSON: {}".format(f, e))

        missing = [k for k in REQUIRED if not a.get(k)]
        if missing:
            raise ValueError("{} is missing: {}".format(f, ", ".join(missing)))

        # Generators expect a file name and a relative image path.
        a["file"] = "blog-{}.html".format(a["slug"])
        a["image"] = "../assets/images/{}".format(a["image"])
        a.setdefault("faq", [])
        a.setdefault("target_keyword", "")
        out.append(a)

    out.sort(key=lambda a: a["date"], reverse=True)
    return out


def faq_schema(article, url, lang):
    """FAQPage node for an article that declares questions."""
    import re

    def plain(t):
        return re.sub(r"<[^>]+>", "", t).replace("&amp;", "&").strip()

    if not article.get("faq"):
        return None

    return {
        "@type": "FAQPage",
        "@id": url + "#faq",
        "inLanguage": lang,
        "mainEntity": [
            {
                "@type": "Question",
                "name": plain(q["q"]),
                "acceptedAnswer": {"@type": "Answer", "text": plain(q["a"])},
            }
            for q in article["faq"]
        ],
    }


def faq_html(article, lang):
    """Rendered FAQ block, matching the accordion used elsewhere on the site."""
    if not article.get("faq"):
        return ""

    heading = "الأسئلة الشائعة" if lang == "ar" else "Frequently Asked Questions"
    rows = "".join(
        '''
                <details class="card bg-main" style="padding:22px; cursor:pointer;">
                    <summary style="font-weight:600; list-style:none; display:flex; justify-content:space-between; gap:16px;">{q} <span>&#43;</span></summary>
                    <div style="margin-top:14px; line-height:1.85; color:var(--text-muted);">{a}</div>
                </details>'''.format(**q)
        for q in article["faq"]
    )

    return '''
            <h2>{heading}</h2>
            <div style="display:flex; flex-direction:column; gap:14px; margin-top:20px;">{rows}
            </div>'''.format(heading=heading, rows=rows)
