"""Generate sitemap.xml covering every EN + AR page, with hreflang alternates.

Run after generate_en.py / generate_ar.py:  python generate_sitemap.py
"""
import datetime
import os

domain = "https://iconicmach.com"

# filename -> (changefreq, priority)
PAGES = {
    "index.html": ("weekly", "1.0"),
    "production-lines.html": ("monthly", "0.9"),
    "conveyor-systems.html": ("monthly", "0.9"),
    "services.html": ("monthly", "0.9"),
    "industries.html": ("monthly", "0.8"),
    "spare-parts.html": ("monthly", "0.8"),
    "technical-support.html": ("monthly", "0.8"),
    "request-quotation.html": ("monthly", "0.8"),
    "projects.html": ("monthly", "0.7"),
    "about.html": ("monthly", "0.7"),
    "contact.html": ("monthly", "0.7"),
    "blog.html": ("weekly", "0.6"),
    "faq.html": ("monthly", "0.6"),
    "privacy-policy.html": ("yearly", "0.3"),
    "terms.html": ("yearly", "0.3"),
}


def loc(lang, filename):
    return "{}/{}/{}".format(domain, lang, "" if filename == "index.html" else filename)


def main():
    lastmod = datetime.date.today().isoformat()
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]

    for lang in ("ar", "en"):
        for filename, (changefreq, priority) in PAGES.items():
            out.append("    <url>")
            out.append("        <loc>{}</loc>".format(loc(lang, filename)))
            for alt in ("ar", "en"):
                out.append(
                    '        <xhtml:link rel="alternate" hreflang="{}" href="{}"/>'.format(
                        alt, loc(alt, filename)
                    )
                )
            out.append(
                '        <xhtml:link rel="alternate" hreflang="x-default" href="{}"/>'.format(
                    loc("en", filename)
                )
            )
            out.append("        <lastmod>{}</lastmod>".format(lastmod))
            out.append("        <changefreq>{}</changefreq>".format(changefreq))
            out.append("        <priority>{}</priority>".format(priority))
            out.append("    </url>")

    out.append("</urlset>")
    out.append("")

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    print("sitemap.xml generated with {} URLs.".format(len(PAGES) * 2))


if __name__ == "__main__":
    main()
