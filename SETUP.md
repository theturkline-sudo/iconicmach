# Iconic Mach — setup & deployment

Static bilingual site (EN + AR) deployed on Cloudflare Pages.

## How the site is built

The HTML in `en/` and `ar/` is **generated output — do not edit it directly.**
Every change goes into the Python generators, then you regenerate:

```bash
python generate_en.py
python generate_ar.py
python generate_sitemap.py
```

| File | What it holds |
|---|---|
| `generate_en.py` | English page content, hero config, blog articles, HTML template |
| `generate_ar.py` | Arabic equivalents (RTL) |
| `generate_sitemap.py` | URL list → `sitemap.xml` with hreflang alternates |
| `assets/` | CSS, JS, images, videos (shared by both languages) |
| `functions/api/submit-inquiry.js` | Cloudflare Pages Function handling form submissions |

Adding a page means adding an entry to `pages` (and usually `page_heroes`) in
both generators, plus `PAGES` in `generate_sitemap.py`.

---

## Outstanding setup steps

### 1. Web3Forms access key — required, forms are broken without it

Inquiry emails are delivered by [Web3Forms](https://web3forms.com). Mail goes to
whichever inbox owns the access key, so the key **must** be created using
`sales@iconicmach.com`.

1. Go to <https://web3forms.com>, enter `sales@iconicmach.com`
2. Check that inbox for the access key
3. Cloudflare dashboard → your Pages project → **Settings → Environment variables**
4. Add `WEB3FORMS_ACCESS_KEY` = the key, to **both Production and Preview**
5. Redeploy

Until this is set, the form shows the visitor a clear error and writes the
submission to the Worker logs, so nothing is silently lost.

Web3Forms was chosen over Resend/SMTP because it needs no verified sending
domain and no SMTP credentials — there is no "from address" to configure.

**Why the Function proxies instead of the browser posting directly:** validation,
length caps and the honeypot run server-side, and the access key never appears
in page HTML.

### 2. Google Analytics 4 — done, verify after deploy

Already configured. No action needed unless something looks wrong.

| | |
|---|---|
| Google account | `theturkline@gmail.com` |
| Analytics account | Iconic Mach Engineering |
| Property | `iconicmach.com` (Egypt time, EGP) |
| Stream | Iconic Mach Website — `https://iconicmach.com` |
| Measurement ID | `G-PXFLDZYHCP` |

`GA_MEASUREMENT_ID` is set in both generators, so the tag is on all 36 pages
with `anonymize_ip: true`. Data-sharing with Google for its own product and
marketing purposes was left off.

**Verify once deployed:** visit the live site, then check
Analytics → Reports → Realtime. Nothing appeared during local testing, which is
normal for a property created minutes earlier — Google warns collection can take
up to 48 hours to start. The tag itself was confirmed working: the page_view hit
was accepted by Google with HTTP 204.

Business size was set to "Medium (11-100 employees)" as a guess — correct it in
Admin → Property details if wrong. It only affects Google's benchmarking.

### 3. Blog articles are drafts

The three articles in each language were drafted to give the blog real,
linkable pages. Review the copy before treating it as final marketing material.

Publication dates live in the `ARTICLES` list in each generator (`date` and
`date_label`) — change both together, and re-run `generate_sitemap.py`.

---

## Local preview

```bash
python -m http.server 8788
```

Then open <http://localhost:8788/en/> or <http://localhost:8788/ar/>.

Note that `python -m http.server` does not handle POST, so form submissions
return 501 locally. That is expected — the form is only fully testable on a
Cloudflare deployment, where the Pages Function runs. To test Functions
locally instead, use `npx wrangler pages dev .`.

## Deploy

Pushing to `main` triggers the Cloudflare Pages build. `wrangler.jsonc` serves
the repository root as static assets, with `functions/` picked up automatically.
