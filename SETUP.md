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

### 1. Web3Forms — done, no action needed

Inquiry emails are delivered by [Web3Forms](https://web3forms.com) to the inbox
that owns the access key (`sales@iconicmach.com`).

Access key: `8fdf1126-4ed7-4dc6-aea5-6714b12d50ad`, set as
`WEB3FORMS_ACCESS_KEY` in both generators.

**The key is in the page HTML on purpose.** Web3Forms states it is public and
safe in client code — the worst it permits is sending mail to the address that
owns it. There is no Cloudflare environment variable and no server-side secret.

**Why the form posts straight from the browser:** Web3Forms rejects server-side
calls on the free plan —

> This method is not allowed. Use our API in client side or contact support
> with server IP address (Pro plan is required)

An earlier design proxied through a Cloudflare Pages Function to keep the key
private; it was removed because it could never have worked. `functions/` no
longer exists.

**Spam protection.** A hidden `botcheck` field (Web3Forms' native honeypot) is
in both forms; when filled, `forms.js` skips the network call entirely and
shows a fake success so the bot does not retry. Web3Forms also runs its own
spam filtering. If spam ever becomes a problem, the next step is Cloudflare
Turnstile, which Web3Forms supports natively and is free.

Verified end to end on 10 August 2026: EN contact form and AR quotation form
both submitted successfully through the real handler, and the honeypot path
made zero network calls.

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

Forms work locally, since they post directly to Web3Forms rather than to a
local endpoint. Be aware that browsers cache `assets/`, so after changing CSS
or JS you may keep running the old file — bump `ASSET_VERSION` in both
generators (it appends `?v=N` to every local CSS/JS URL) and regenerate. That
same mechanism stops returning visitors running stale assets after a deploy.

## URLs

The site is served **extensionless**: Cloudflare 307-redirects `/en/contact.html`
to `/en/contact`. Generators therefore emit extensionless internal links,
canonical tags, hreflang tags and sitemap entries — `prettify_links()` in each
generator rewrites `href="x.html"` to `href="x"` (and `index.html` to `./`) on
the rendered page. Files on disk keep their `.html` names; only the links change.

Do not reintroduce `.html` links: hreflang pointing at a redirecting URL can be
ignored by Google, and every internal click would cost a redirect hop.

## Deploy

Pushing to `main` triggers a Cloudflare Workers build (the project is
Git-connected to `theturkline-sudo/iconicmach`). `wrangler.jsonc` serves the
repository root as static assets.
