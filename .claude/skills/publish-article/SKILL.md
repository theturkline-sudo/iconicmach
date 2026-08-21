---
name: publish-article
description: Autonomously research, write, audit and publish one blog article to iconicmach.com from the keyword backlog. Runs unattended on a schedule. Use when asked to publish an article, run the publishing job, or when triggered by the scheduled publishing task.
---

# Autonomous publishing run — iconicmach.com

Publish **one** article per run, in Arabic and English, and deploy it. This
runs unattended, so the rules below are hard constraints, not preferences.

Work from the repository at
`C:\Users\pc shop\Desktop\Folders\Projects\iconicmach`.

## Stop conditions — check these first

Abort the run and report, without publishing, if any hold:

- `python scripts/next_topic.py` exits **3** (backlog empty). Do not invent a
  topic. Report that the backlog needs restocking.
- `git status --porcelain` is not empty. Someone has uncommitted work; do not
  commit on top of it.
- The last commit on `main` did not build. Check:
  `gh api repos/theturkline-sudo/iconicmach/commits/main/check-runs --jq '.check_runs[].conclusion'`
  Publishing on top of a broken build buries the breakage.

## 1. Take the next topic

```bash
python scripts/next_topic.py
```

Gives `keyword`, `cluster`, `intent` and `money_page`. The money page is the
internal link this article must contain.

## 2. Research the live SERP

Follow the `arabic-blog` skill's research steps. In short: `WebSearch` the
Arabic keyword, then `WebFetch` the two or three strongest non-marketplace
results asking only for their heading structure, word count, FAQ presence and
CTA. Identify the **common spine** and the **gaps**.

Never write from memory. The whole point is to match what currently ranks.

## 3. Write both languages

Create `content/ar/<slug>.json` and `content/en/<slug>.json`. Follow every rule
in the `arabic-blog` skill. The constraints that matter most when nobody is
reviewing before publication:

- **Invent nothing.** No prices, no statistics, no client names, no case
  studies, no delivery times presented as commitments. Explain what drives a
  cost instead of quoting one. If a fact cannot be supported, leave it out.
- **Regulatory claims stay general.** Name the responsible authority and tell
  the reader to verify with it directly. Never state a specific requirement,
  fee or procedure as current fact.
- **Arabic is the original.** English is a genuine counterpart, not a
  translation of the Arabic.
- Both files use the **same slug**, or hreflang points at a 404.
- At least 3 internal links, one to the topic's `money_page`, extensionless.
- `faq[]` with 4-6 entries — this is what earns AI-assistant citations.

## 4. Gate

```bash
python scripts/seo_audit.py ar <slug>
python scripts/seo_audit.py en <slug>
```

Any **FAIL** blocks publication. Fix and re-run. Do not lower the thresholds in
`scripts/seo_audit.py` to make a draft pass — that defeats the gate. If a draft
cannot pass honestly, abort and report.

## 5. Build and verify

```bash
python generate_ar.py && python generate_en.py && python generate_sitemap.py
```

Then confirm the rendered page: JSON-LD parses and contains `BlogPosting`,
`FAQPage` and `BreadcrumbList`; the Arabic page is `dir="rtl"`; every internal
link in the body resolves.

## 6. Publish

```bash
python scripts/next_topic.py --done <slug> --keyword "<keyword>"
git add -A
git commit -m "content: <keyword>"
git push origin main
```

Then confirm the build actually succeeded — a push is not a publish:

```bash
gh api repos/theturkline-sudo/iconicmach/commits/main/check-runs --jq '.check_runs[].conclusion'
```

and that the URL returns 200:

```bash
curl -s -o /dev/null -w '%{http_code}' https://iconicmach.com/ar/blog-<slug>
```

If the build failed, say so plainly in the report. Do not mark the topic done
if it did not publish — revert the backlog entry to `todo`.

## 7. Report

State: the keyword, both URLs, the audit result, the build result, and how many
topics remain. If anything was skipped or failed, lead with that.

## Notes for whoever reads the output later

- Articles published this way have **not been read by a human before going
  live**. The constraints above exist because of that. If the site starts
  making claims it should not, the fix is to tighten this file, not to
  post-edit individual articles.
- Deploys go straight to production; there is no staging branch.
- `.assetsignore` keeps `.git`, `content/`, `scripts/` and `*.py` out of the
  public upload. Do not remove it — without it the whole repository, including
  its full history, is downloadable from the live site.
