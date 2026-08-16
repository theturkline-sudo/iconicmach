import json
import os
import re

import widgets

domain = "https://iconicmach.com"

# Google Analytics 4 — paste the Measurement ID (looks like "G-XXXXXXXXXX")
# from Analytics → Admin → Data streams → your web stream, then re-run this
# script. Leave it empty and no tracking code is emitted at all.
GA_MEASUREMENT_ID = "G-PXFLDZYHCP"

# Web3Forms access key (public by design — Web3Forms blocks server-side
# submissions on the free plan, so the form posts from the browser).
WEB3FORMS_ACCESS_KEY = "8fdf1126-4ed7-4dc6-aea5-6714b12d50ad"

# Bump when any file in assets/css or assets/js changes, so returning visitors
# do not run a stale cached script against newly generated HTML.
ASSET_VERSION = "7"


def analytics_snippet():
    if not GA_MEASUREMENT_ID:
        return ""
    return '''<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{gid}', {{ anonymize_ip: true }});
    </script>'''.format(gid=GA_MEASUREMENT_ID)


ORGANIZATION = {
    "@type": "Organization",
    "@id": domain + "/#organization",
    "name": "Iconic Mach Engineering",
    "alternateName": "آيكونيك ماشين الهندسية",
    "url": domain + "/",
    "logo": domain + "/assets/images/iconicmach.png",
    "image": domain + "/assets/images/iconicmach.png",
    "description": "Design, manufacture and installation of production lines, conveyor systems and industrial automation across Egypt and the GCC.",
    "email": "sales@iconicmach.com",
    "telephone": "+20-10-68472717",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Al Hashemia Mall, Tower W, 3rd Floor, behind the Vodafone branch, 10th of Ramadan City",
        "addressRegion": "Al Sharqiya",
        "addressCountry": "EG",
    },
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": 30.2930808,
        "longitude": 31.7461565,
    },
    "hasMap": "https://www.google.com/maps/place/El+Hashemeya+Market+Centre/@30.2930808,31.7461565,18z/data=!4m6!3m5!1s0x1457fd95bdb45c5d:0xebe21a3cdcc6d742!8m2!3d30.2930808!4d31.7461565!16s%2Fg%2F1pty73hds",
    "areaServed": ["EG", "SA", "AE", "KW", "QA", "OM", "BH"],
    "sameAs": [
        "https://www.instagram.com/iconic.mach/",
        "https://www.tiktok.com/@iconicmach",
        "https://www.facebook.com/profile.php?id=61590558549282",
        "https://www.linkedin.com/in/mahmoud-turk-82bbb8412/",
        "https://www.youtube.com/@Iconicmach",
    ],
    "contactPoint": [
        {
            "@type": "ContactPoint",
            "contactType": "sales",
            "telephone": "+20-10-68472717",
            "email": "sales@iconicmach.com",
            "availableLanguage": ["en", "ar"],
        },
        {
            "@type": "ContactPoint",
            "contactType": "technical support",
            "email": "technical@iconicmach.com",
            "availableLanguage": ["en", "ar"],
        },
    ],
}


def slug_for(filename):
    """URL path Cloudflare actually serves: index.html -> "", about.html -> about."""
    return "" if filename == "index.html" else filename[:-len(".html")]


def prettify_links(html):
    """Rewrite internal .html hrefs to the extensionless URLs the server serves.

    Cloudflare's static-asset handling 307-redirects /x.html to /x, so linking
    to .html cost a redirect hop on every click and made canonical/hreflang
    point at redirecting URLs. External links are left alone: the character
    class excludes ':' so "https://..." never matches.
    """
    html = re.sub(r'href="index\.html"', 'href="./"', html)
    html = re.sub(r'href="((?:\.\./)?[a-z]{2}/)index\.html"', r'href="\1"', html)
    html = re.sub(r'href="([^":]+?)\.html"', r'href="\1"', html)
    return html


def lazy_load_images(html):
    """Defer off-screen images.

    The header logo is skipped: it is above the fold on every page, and lazy
    loading it would delay the most visible element. Images that already
    declare `loading` are left alone.
    """
    def add(match):
        tag = match.group(0)
        if 'loading=' in tag or 'images/iconicmach.png' in tag:
            return tag
        return tag[:-1].rstrip() + ' loading="lazy" decoding="async">'

    return re.sub(r'<img\b[^>]*>', add, html)


def defer_videos(html, poster):
    """Stop every remaining <video> from downloading on load.

    make_hero() already defers the hero. This catches the videos embedded in
    page content, which autoplayed too — 45 MB of them on the English pages
    alone. They get the page's hero poster so a phone sees a still image
    rather than a black rectangle.
    """
    def fix(match):
        tag = match.group(0)
        if 'data-src=' in tag:
            return tag
        tag = tag.replace(' src="', ' data-src="')
        if 'poster=' not in tag:
            tag = tag.replace('<video', '<video poster="%s"' % poster, 1)
        if 'preload=' not in tag:
            tag = tag.replace('<video', '<video preload="none"', 1)
        return tag

    return re.sub(r'<video\b[^>]*>', fix, html)


def build_schema(filename, title, description):
    """JSON-LD graph: the Organization plus a WebPage node for this page."""
    url = "{}/en/{}".format(domain, slug_for(filename))
    graph = [
        ORGANIZATION,
        {
            "@type": "WebSite",
            "@id": domain + "/#website",
            "url": domain + "/",
            "name": "Iconic Mach Engineering",
            "inLanguage": "en",
            "publisher": {"@id": domain + "/#organization"},
        },
        {
            "@type": "WebPage",
            "@id": url + "#webpage",
            "url": url,
            "name": title + " | Iconic Mach Engineering",
            "description": description,
            "inLanguage": "en",
            "isPartOf": {"@id": domain + "/#website"},
            "about": {"@id": domain + "/#organization"},
        },
    ]

    if filename == "index.html":
        graph.append(widgets.faq_schema_nodes("en", url))

    crumb = widgets.breadcrumb_node(
        'en', filename, domain,
        widgets.page_title_for('en', slug_for(filename)) or title,
    )
    if crumb:
        graph.append(crumb)

    article = ARTICLES_BY_FILE.get(filename)
    if article:
        graph.append(
            {
                "@type": "BlogPosting",
                "@id": url + "#article",
                "headline": article["title"],
                "description": article["excerpt"],
                "image": domain + "/assets/images/" + article["image"].rsplit("/", 1)[-1],
                "datePublished": article["date"],
                "dateModified": article["date"],
                "articleSection": article["category"].title(),
                "inLanguage": "en",
                "mainEntityOfPage": {"@id": url + "#webpage"},
                "author": {"@id": domain + "/#organization"},
                "publisher": {"@id": domain + "/#organization"},
            }
        )

    return json.dumps(
        {"@context": "https://schema.org", "@graph": graph},
        ensure_ascii=False,
        separators=(",", ":"),
    )

# Still image shown in place of each hero video. It renders instantly, and on
# mobile or a metered/slow connection it is ALL that loads — the video file is
# only attached when the connection can afford it (see VIDEO_LOADER below).
VIDEO_POSTERS = {
    'index.html':            '../assets/images/industrial-process-8.jpeg',
    'production-lines.html': '../assets/images/industrial-process-1.jpeg',
    'conveyor-systems.html': '../assets/images/industrial-process-3.jpeg',
    'services.html':         '../assets/images/industrial-process-5.jpeg',
    'industries.html':       '../assets/images/industrial-process-7.jpeg',
    'projects.html':         '../assets/images/industrial-process-10.jpeg',
}

DEFAULT_POSTER = '../assets/images/industrial-process-1.jpeg'

# The hero videos are 8-21 MB each and autoplay. Downloading one over Egyptian
# mobile data to decorate a page is not a reasonable trade, so the <video> ships
# with no src at all: the poster carries the page, and the file is attached only
# on a wide viewport with a connection that is not save-data or 2g/3g.
VIDEO_LOADER = """
    <script>
        (function () {
            var vids = [].slice.call(document.querySelectorAll('video[data-src]'));
            if (!vids.length) return;
            var c = navigator.connection || {};
            var stingy = c.saveData === true || /(^|-)(2g|slow-2g)$/.test(c.effectiveType || '');
            // Narrow screen, save-data, or 2g: posters only, no video bytes.
            if (window.innerWidth < 768 || stingy) return;
            var load = function (v) {
                if (v.getAttribute('data-loaded')) return;
                v.setAttribute('data-loaded', '1');
                v.src = v.getAttribute('data-src');
                v.load();
            };
            // The hero is always above the fold, so load it directly rather
            // than relying on IntersectionObserver, which never fires in a
            // tab that is not compositing.
            load(vids.shift());
            if (!vids.length) return;
            if (!('IntersectionObserver' in window)) { vids.forEach(load); return; }
            // The rest wait until they are near the viewport, so a page with
            // several videos does not pull them all at once.
            var io = new IntersectionObserver(function (entries) {
                entries.forEach(function (e) {
                    if (e.isIntersecting) { load(e.target); io.unobserve(e.target); }
                });
            }, { rootMargin: '200px' });
            vids.forEach(function (v) { io.observe(v); });
        })();
    </script>"""


# Hero section per page: (bg_image_or_video, title, subtitle)
page_heroes = {
    'index.html':              ('video', '../assets/videos/full line.mp4', 'Leading Industrial Engineering', 'We design, manufacture & install world-class production lines across Egypt and the GCC.'),
    'production-lines.html':   ('video', '../assets/videos/production-line-video-12.mp4', 'Production Lines', 'Integrated solutions for food & beverage, packaging, and industrial assembly.'),
    'conveyor-systems.html':   ('video', '../assets/videos/conveyor.mp4',  'Conveyor Systems', 'Advanced material handling systems built for speed, precision, and durability.'),
    'services.html':           ('video', '../assets/videos/designing.mp4',    'Our Services', 'Engineering design, manufacturing, installation, and 24/7 technical support.'),
    'contact.html':            ('image', '../assets/images/industrial-process-9.jpeg',    'Contact Us', 'We are here to help. Reach out for a consultation or site visit.'),
    'about.html':              ('image', '../assets/images/industrial-process-6.jpeg',    'About Iconic Mach', 'Built on innovation, trust, and two decades of industrial engineering excellence.'),
    'industries.html':         ('video', '../assets/videos/sorting.mp4','Industries We Serve', 'From food processing to logistics — we power the sectors that power Egypt.'),
    'projects.html':           ('video', '../assets/videos/full line.mp4', 'Our Portfolio', 'Explore completed installations and success stories from across the region.'),
    'blog.html':               ('image', '../assets/images/industrial-process-7.jpeg',    'Insights & News', 'Stay up to date with the latest in industrial engineering and automation.'),
    'faq.html':                ('image', '../assets/images/industrial-process-3.jpeg',    'Frequently Asked Questions', 'Quick answers to the questions our clients ask most.'),
    'request-quotation.html':  ('image', '../assets/images/industrial-process-4.jpeg',    'Request a Quotation', 'Tell us about your project and we will deliver a competitive estimate.'),
    'technical-support.html':  ('image', '../assets/images/industrial-process-5.jpeg',    '24/7 Technical Support', 'Our engineers are always on standby to keep your systems running.'),
    'spare-parts.html':        ('image', '../assets/images/industrial-process-1.jpeg',    'Spare Parts', 'Genuine replacement parts delivered fast to minimise your downtime.'),
    'privacy-policy.html':     ('image', '../assets/images/industrial-process-2.jpeg',    'Privacy Policy', 'How we collect, use and protect your information.'),
    'terms.html':              ('image', '../assets/images/industrial-process-10.jpeg',   'Terms & Conditions', 'The terms that govern the use of our services and website.'),
}

def make_hero(filename):
    poster = VIDEO_POSTERS.get(filename, DEFAULT_POSTER)
    media_type, src, title, subtitle = page_heroes.get(filename, ('image', '../assets/images/industrial-process-1.jpeg', 'Iconic Mach Engineering', ''))
    if filename == 'index.html':
        return f'''
    <section class="page-hero" style="position:relative; height:100vh; min-height:600px; display:flex; align-items:center; justify-content:center; text-align:center; overflow:hidden;">
        <video autoplay loop muted playsinline preload="none" poster="{poster}" data-src="{src}"
            style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:0; transform:scale(1.15) translate(-2%, -2%);"></video>
        <div style="position:absolute; inset:0; background:rgba(6,18,38,0.62); z-index:1;"></div>
        <div class="container reveal fade-in" style="position:relative; z-index:2; color:#fff; padding: 0 20px;">
            <p style="font-size:1rem; letter-spacing:3px; text-transform:uppercase; opacity:0.8; margin-bottom:16px;">Iconic Mach Engineering</p>
            <h1 style="font-size:clamp(2.2rem,5vw,4rem); font-weight:700; line-height:1.15; margin-bottom:22px; text-shadow:0 2px 16px rgba(0,0,0,0.4);">{title}</h1>
            <p style="font-size:1.15rem; max-width:640px; margin:0 auto 36px; opacity:0.88; line-height:1.7;">{subtitle}</p>
            <div style="display:flex; gap:16px; justify-content:center; flex-wrap:wrap;">
                <a href="production-lines.html" class="btn btn-primary" style="padding:14px 32px; font-size:1rem; text-decoration:none;">Our Products</a>
                <a href="contact.html" style="padding:14px 32px; font-size:1rem; border:2px solid rgba(255,255,255,0.7); border-radius:var(--radius-sm); color:#fff; text-decoration:none; backdrop-filter:blur(4px);">Get in Touch</a>
            </div>
        </div>
        <a href="#main-content" style="position:absolute; bottom:32px; left:50%; transform:translateX(-50%); z-index:2; color:rgba(255,255,255,0.7); font-size:2rem; text-decoration:none; animation:bounceDown 2s infinite;">&#8964;</a>
    </section>'''
    elif media_type == 'video':
        return f'''
    <section class="page-hero" style="position:relative; height:55vh; min-height:380px; display:flex; align-items:center; justify-content:center; text-align:center; overflow:hidden;">
        <video autoplay loop muted playsinline preload="none" poster="{poster}" data-src="{src}"
            style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:0; transform:scale(1.15) translate(-2%, -2%);"></video>
        <div style="position:absolute; inset:0; background:rgba(6,18,38,0.58); z-index:1;"></div>
        <div class="container reveal fade-in" style="position:relative; z-index:2; color:#fff; padding:0 20px;">
            <h1 style="font-size:clamp(1.8rem,4vw,3.2rem); font-weight:700; margin-bottom:14px; text-shadow:0 2px 12px rgba(0,0,0,0.4);">{title}</h1>
            <p style="font-size:1.1rem; max-width:600px; margin:0 auto; opacity:0.88; line-height:1.7;">{subtitle}</p>
        </div>
    </section>'''
    else:
        return f'''
    <section class="page-hero" style="position:relative; height:55vh; min-height:380px; display:flex; align-items:center; justify-content:center; text-align:center; overflow:hidden; background:url('{src}') center/cover no-repeat;">
        <div style="position:absolute; inset:0; background:rgba(6,18,38,0.58);"></div>
        <div class="container reveal fade-in" style="position:relative; z-index:2; color:#fff; padding:0 20px;">
            <h1 style="font-size:clamp(1.8rem,4vw,3.2rem); font-weight:700; margin-bottom:14px; text-shadow:0 2px 12px rgba(0,0,0,0.4);">{title}</h1>
            <p style="font-size:1.1rem; max-width:600px; margin:0 auto; opacity:0.88; line-height:1.7;">{subtitle}</p>
        </div>
    </section>'''

FOOTER = '''
    <footer class="site-footer" style="background:#061226; color:#c9d8ec; padding: 64px 0 0;">
        <div class="container">
            <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:48px; padding-bottom:48px; border-bottom:1px solid rgba(255,255,255,0.08);">
                <!-- Brand -->
                <div>
                    <img src="../assets/images/footer_logo.png" alt="Iconic Mach Engineering" style="height:75px; margin-bottom:16px;">
                    <p style="font-size:0.92rem; line-height:1.8; opacity:0.7; max-width:240px;">Designing and manufacturing world-class production lines and conveyor systems across Egypt and the GCC.</p>
                                        <div style="display:flex; gap:12px; margin-top:20px; flex-wrap:wrap;">
                        <a href="https://www.instagram.com/iconic.mach/" target="_blank" aria-label="Instagram" title="Instagram" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#c9d8ec;text-decoration:none;transition:background .2s;" onmouseover="this.style.background='#e1306c';" onmouseout="this.style.background='rgba(255,255,255,0.08)';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg></a>
                        <a href="https://www.tiktok.com/@iconicmach" target="_blank" aria-label="TikTok" title="TikTok" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#c9d8ec;text-decoration:none;transition:background .2s;" onmouseover="this.style.background='#010101';" onmouseout="this.style.background='rgba(255,255,255,0.08)';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.32 6.32 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.69a8.16 8.16 0 004.77 1.52V6.74a4.85 4.85 0 01-1-.05z"/></svg></a>
                        <a href="https://www.facebook.com/profile.php?id=61590558549282" target="_blank" aria-label="Facebook" title="Facebook" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#c9d8ec;text-decoration:none;transition:background .2s;" onmouseover="this.style.background='#1877f2';" onmouseout="this.style.background='rgba(255,255,255,0.08)';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a>
                        <a href="https://www.linkedin.com/in/mahmoud-turk-82bbb8412/" target="_blank" aria-label="LinkedIn" title="LinkedIn" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#c9d8ec;text-decoration:none;transition:background .2s;" onmouseover="this.style.background='#0077b5';" onmouseout="this.style.background='rgba(255,255,255,0.08)';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>
                        <a href="https://www.youtube.com/@Iconicmach" target="_blank" aria-label="YouTube" title="YouTube" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#c9d8ec;text-decoration:none;transition:background .2s;" onmouseover="this.style.background='#ff0000';" onmouseout="this.style.background='rgba(255,255,255,0.08)';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a>
                        <a href="https://wa.me/201068472717" target="_blank" aria-label="WhatsApp" title="WhatsApp" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#c9d8ec;text-decoration:none;transition:background .2s;" onmouseover="this.style.background='#25d366';" onmouseout="this.style.background='rgba(255,255,255,0.08)';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg></a>
                    </div>
                </div>
                <!-- Products -->
                <div>
                    <h4 style="color:#fff; font-size:1rem; font-weight:600; margin-bottom:18px; letter-spacing:0.5px;">Products</h4>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:10px;">
                        <li><a href="production-lines.html" style="color:#c9d8ec; text-decoration:none; font-size:0.9rem; opacity:0.8; transition:opacity .2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">Production Lines</a></li>
                        <li><a href="conveyor-systems.html" style="color:#c9d8ec; text-decoration:none; font-size:0.9rem; opacity:0.8; transition:opacity .2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">Conveyor Systems</a></li>
                        <li><a href="spare-parts.html" style="color:#c9d8ec; text-decoration:none; font-size:0.9rem; opacity:0.8; transition:opacity .2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">Spare Parts</a></li>
                        <li><a href="request-quotation.html" style="color:#c9d8ec; text-decoration:none; font-size:0.9rem; opacity:0.8; transition:opacity .2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">Request a Quote</a></li>
                    </ul>
                </div>
                <!-- Company -->
                <div>
                    <h4 style="color:#fff; font-size:1rem; font-weight:600; margin-bottom:18px; letter-spacing:0.5px;">Company</h4>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:10px;">
                        <li><a href="about.html" style="color:#c9d8ec; text-decoration:none; font-size:0.9rem; opacity:0.8; transition:opacity .2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">About Us</a></li>
                        <li><a href="services.html" style="color:#c9d8ec; text-decoration:none; font-size:0.9rem; opacity:0.8; transition:opacity .2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">Services</a></li>
                        <li><a href="industries.html" style="color:#c9d8ec; text-decoration:none; font-size:0.9rem; opacity:0.8; transition:opacity .2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">Industries</a></li>
                        <li><a href="projects.html" style="color:#c9d8ec; text-decoration:none; font-size:0.9rem; opacity:0.8; transition:opacity .2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">Projects</a></li>
                        <li><a href="blog.html" style="color:#c9d8ec; text-decoration:none; font-size:0.9rem; opacity:0.8; transition:opacity .2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">Blog</a></li>
                        <li><a href="faq.html" style="color:#c9d8ec; text-decoration:none; font-size:0.9rem; opacity:0.8; transition:opacity .2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">FAQs</a></li>
                    </ul>
                </div>
                <!-- Contact -->
                <div>
                    <h4 style="color:#fff; font-size:1rem; font-weight:600; margin-bottom:18px; letter-spacing:0.5px;">Contact</h4>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:12px; font-size:0.9rem;">
                        <li style="display:flex; gap:10px; align-items:flex-start;"><span style="margin-top:2px;">📍</span><span style="opacity:0.8;">10th of Ramadan &ndash; Al Hashemia Mall<br>Tower (W) &ndash; 3rd Floor<br>Behind the Vodafone branch<br>Al Sharqiya, Egypt<br><a href="https://www.google.com/maps/place/El+Hashemeya+Market+Centre/@30.2930808,31.7461565,18z/data=!4m6!3m5!1s0x1457fd95bdb45c5d:0xebe21a3cdcc6d742!8m2!3d30.2930808!4d31.7461565!16s%2Fg%2F1pty73hds" target="_blank" rel="noopener" style="color:#4adeae; text-decoration:none;">Open in Google Maps</a></span></li>
                        <li style="display:flex; gap:10px; align-items:center;"><span>📱</span><a href="https://wa.me/201068472717" style="color:#4adeae; text-decoration:none;">+20 10 68472717</a></li>
                        <li style="display:flex; gap:10px; align-items:center;"><span>✉️</span><a href="mailto:sales@iconicmach.com" style="color:#4adeae; text-decoration:none;">sales@iconicmach.com</a></li>
                        <li style="display:flex; gap:10px; align-items:center;"><span>🔧</span><a href="mailto:technical@iconicmach.com" style="color:#4adeae; text-decoration:none;">technical@iconicmach.com</a></li>
                    </ul>
                </div>
            </div>
            <!-- Bottom bar -->
            <div style="padding:24px 0; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; font-size:0.85rem; opacity:0.6;">
                <p style="margin:0;">&copy; 2026 Iconic Mach Engineering. All rights reserved.</p>
                <div style="display:flex; gap:20px;">
                    <a href="privacy-policy.html" style="color:#c9d8ec; text-decoration:none;">Privacy Policy</a>
                    <a href="terms.html" style="color:#c9d8ec; text-decoration:none;">Terms &amp; Conditions</a>
                    <a href="sitemap.html" style="color:#c9d8ec; text-decoration:none;">Site Map</a>
                </div>
            </div>
        </div>
    </footer>'''

pages = {
    'index.html': ('Home', 'Iconic Mach Engineering — production lines, conveyor systems & industrial automation.', '''
    <section id="main-content" class="section" style="padding-top:80px;">
        <div class="container">
            <div style="text-align:center; margin-bottom:60px;">
                <h2 class="text-primary" style="font-size:2rem; margin-bottom:12px;">What We Do</h2>
                <p class="text-muted" style="max-width:640px; margin:0 auto; line-height:1.8;">From concept to commissioning — we build the systems that keep factories running at peak performance.</p>
            </div>
            <div class="grid grid-3" style="margin-bottom:80px;">
                <div class="card bg-main" style="padding:32px; text-align:center; box-shadow:var(--shadow-sm);">
                    <div style="font-size:2.5rem; margin-bottom:16px;">🏭</div>
                    <h3 style="margin-bottom:12px; color:var(--primary-blue);">Production Lines</h3>
                    <p style="line-height:1.7; margin-bottom:20px;">Complete end-to-end production line design and installation for food, beverage, and industrial sectors.</p>
                    <a href="production-lines.html" style="color:var(--primary-blue); font-weight:600; text-decoration:none;">Learn more &rarr;</a>
                </div>
                <div class="card bg-main" style="padding:32px; text-align:center; box-shadow:var(--shadow-sm);">
                    <div style="font-size:2.5rem; margin-bottom:16px;">⚙️</div>
                    <h3 style="margin-bottom:12px; color:var(--primary-blue);">Conveyor Systems</h3>
                    <p style="line-height:1.7; margin-bottom:20px;">Belt, roller, and modular conveyor systems engineered for maximum throughput and reliability.</p>
                    <a href="conveyor-systems.html" style="color:var(--primary-blue); font-weight:600; text-decoration:none;">Learn more &rarr;</a>
                </div>
                <div class="card bg-main" style="padding:32px; text-align:center; box-shadow:var(--shadow-sm);">
                    <div style="font-size:2.5rem; margin-bottom:16px;">🔧</div>
                    <h3 style="margin-bottom:12px; color:var(--primary-blue);">Maintenance & Support</h3>
                    <p style="line-height:1.7; margin-bottom:20px;">24/7 technical support, preventative maintenance contracts, and genuine spare parts delivery.</p>
                    <a href="services.html" style="color:var(--primary-blue); font-weight:600; text-decoration:none;">Learn more &rarr;</a>
                </div>
            </div>
            <!-- Mission & Vision -->
            <div class="grid grid-2" style="margin-bottom:80px; gap:40px;">
                <div class="card bg-main" style="padding:40px; border-left:4px solid var(--primary-blue); box-shadow:var(--shadow-sm);">
                    <h3 style="font-size:1.8rem; margin-bottom:16px;">🎯 Our Mission</h3>
                    <p style="line-height:1.8; font-size:1.1rem; color:var(--text-muted);">To deliver world-class industrial engineering solutions that empower Egyptian and GCC manufacturers to compete globally.</p>
                </div>
                <div class="card bg-main" style="padding:40px; border-left:4px solid var(--primary-blue); box-shadow:var(--shadow-sm);">
                    <h3 style="font-size:1.8rem; margin-bottom:16px;">👁️ Our Vision</h3>
                    <p style="line-height:1.8; font-size:1.1rem; color:var(--text-muted);">To be the leading industrial automation partner in the MENA region, known for quality, reliability, and innovation.</p>
                </div>
            </div>
            <!-- Stats -->
            <div style="background:var(--primary-blue); border-radius:var(--radius-md); padding:48px; display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:32px; text-align:center; color:#fff; margin-bottom:80px;">
                <div><p style="font-size:3rem; font-weight:700; margin:0;">100+</p><p style="opacity:0.8; margin:4px 0 0;">Systems Installed</p></div>
                <div><p style="font-size:3rem; font-weight:700; margin:0;">15+</p><p style="opacity:0.8; margin:4px 0 0;">Years Experience</p></div>
                <div><p style="font-size:3rem; font-weight:700; margin:0;">24/7</p><p style="opacity:0.8; margin:4px 0 0;">Technical Support</p></div>
                <div><p style="font-size:3rem; font-weight:700; margin:0;">GCC</p><p style="opacity:0.8; margin:4px 0 0;">Region Coverage</p></div>
            </div>
            <!-- Projects & Partners -->
            <div style="margin-bottom:80px;">
                <div style="text-align:center; margin-bottom:40px;">
                    <h2 class="text-primary" style="font-size:2rem; margin-bottom:12px;">Featured Projects</h2>
                    <p class="text-muted" style="max-width:640px; margin:0 auto; line-height:1.8;">A glimpse into our recent successful installations.</p>
                </div>
                <div class="grid grid-3" style="margin-bottom:40px;">
                    <div class="card bg-main" style="padding:0; overflow:hidden; box-shadow:var(--shadow-sm);"><video autoplay loop muted playsinline src="../assets/videos/beverages.mp4" style="width:100%;height:180px;object-fit:cover;"></video><div style="padding:20px;"><h4 style="margin-bottom:6px;">Beverage Filling Line</h4><p style="font-size:0.9rem;color:var(--text-muted);">Complete filling and capping line — 12,000 bottles/hr</p></div></div>
                    <div class="card bg-main" style="padding:0; overflow:hidden; box-shadow:var(--shadow-sm);"><video autoplay loop muted playsinline src="../assets/videos/packing.mp4" style="width:100%;height:180px;object-fit:cover;"></video><div style="padding:20px;"><h4 style="margin-bottom:6px;">FMCG Packaging System</h4><p style="font-size:0.9rem;color:var(--text-muted);">Multi-lane cartoning</p></div></div>
                    <div class="card bg-main" style="padding:0; overflow:hidden; box-shadow:var(--shadow-sm);"><video autoplay loop muted playsinline src="../assets/videos/sorting.mp4" style="width:100%;height:180px;object-fit:cover;"></video><div style="padding:20px;"><h4 style="margin-bottom:6px;">Warehouse Conveyors</h4><p style="font-size:0.9rem;color:var(--text-muted);">Belt &amp; roller sorters</p></div></div>
                </div>
                <div style="text-align:center; margin-bottom:80px;">
                    <a href="projects.html" style="color:var(--primary-blue); font-weight:600; text-decoration:none;">View all projects &rarr;</a>
                </div>

                <div style="text-align:center; margin-bottom:40px;">
                    <h2 class="text-primary" style="font-size:2rem; margin-bottom:12px;">Trusted Partners</h2>
                    <p class="text-muted" style="max-width:640px; margin:0 auto; line-height:1.8;">We collaborate with industry leaders to deliver the best components and solutions.</p>
                </div>
                <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:48px; opacity:0.5; filter:grayscale(100%);">
                    <div style="font-size:1.6rem; font-weight:700; font-family:'Outfit', sans-serif; letter-spacing:1px;">OMRON</div>
                    <div style="font-size:1.6rem; font-weight:700; font-family:'Outfit', sans-serif; letter-spacing:1px;">SIEMENS</div>
                    <div style="font-size:1.6rem; font-weight:700; font-family:'Outfit', sans-serif; letter-spacing:1px;">SEW-EURODRIVE</div>
                    <div style="font-size:1.6rem; font-weight:700; font-family:'Outfit', sans-serif; letter-spacing:1px;">FESTO</div>
                    <div style="font-size:1.6rem; font-weight:700; font-family:'Outfit', sans-serif; letter-spacing:1px;">SICK</div>
                </div>
            </div>
            <!-- CTA -->
            <div style="text-align:center;">
                <h2 class="text-primary" style="font-size:1.8rem; margin-bottom:16px;">Ready to upgrade your production?</h2>
                <p class="text-muted" style="margin-bottom:28px;">Get a free consultation from our engineering team.</p>
                <a href="contact.html" class="btn btn-primary" style="padding:14px 36px; font-size:1rem; text-decoration:none;">Talk to an Engineer</a>
            </div>
        </div>
    </section>'''),

    'production-lines.html': ('Production Lines', 'Integrated solutions for production lines, food & beverage industry, packaging, and warehouses.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-3" style="margin-bottom:60px;">
                <div class="card bg-main" style="padding:0; overflow:hidden; box-shadow:var(--shadow-sm);">
                    <video autoplay loop muted playsinline src="../assets/videos/filling.mp4" style="width:100%; height:220px; object-fit:cover;"></video>
                    <div style="padding:24px;">
                        <h3 style="margin-bottom:10px; color:var(--primary-blue);">Food & Beverage</h3>
                        <p style="line-height:1.7;">Sanitary, high-efficiency lines for processing, filling, and packaging food products to the highest safety standards.</p>
                    </div>
                </div>
                <div class="card bg-main" style="padding:0; overflow:hidden; box-shadow:var(--shadow-sm);">
                    <video autoplay loop muted playsinline src="../assets/videos/packing.mp4" style="width:100%; height:220px; object-fit:cover;"></video>
                    <div style="padding:24px;">
                        <h3 style="margin-bottom:10px; color:var(--primary-blue);">FMCG Packaging</h3>
                        <p style="line-height:1.7;">High-speed packaging lines that eliminate bottlenecks and keep your fast-moving consumer goods flowing.</p>
                    </div>
                </div>
                <div class="card bg-main" style="padding:0; overflow:hidden; box-shadow:var(--shadow-sm);">
                    <video autoplay loop muted playsinline src="../assets/videos/production-line-video-14.mp4" style="width:100%; height:220px; object-fit:cover;"></video>
                    <div style="padding:24px;">
                        <h3 style="margin-bottom:10px; color:var(--primary-blue);">Industrial Assembly</h3>
                        <p style="line-height:1.7;">Heavy-duty assembly lines built for continuous operation in demanding industrial environments.</p>
                    </div>
                </div>
            </div>
            <div style="text-align:center; margin-top:40px;">
                <a href="request-quotation.html" class="btn btn-primary" style="padding:14px 32px; text-decoration:none;">Request a Quotation</a>
            </div>
        </div>
    </section>'''),

    'conveyor-systems.html': ('Conveyor Systems', 'Conveyor systems to facilitate material handling, including belt, roller, and chain conveyors.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-2" style="align-items:start; margin-bottom:60px;">
                <div>
                    <h2 class="text-primary" style="font-size:1.8rem; margin-bottom:24px;">Material Handling Solutions</h2>
                    <div style="border-left:3px solid var(--primary-blue); padding-left:20px; margin-bottom:28px;">
                        <h3 style="margin-bottom:8px;">Belt Conveyors</h3>
                        <p style="line-height:1.7;">Ideal for moving various products quickly. Available in flat, inclined, and curved configurations for any floor plan.</p>
                    </div>
                    <div style="border-left:3px solid var(--primary-blue); padding-left:20px; margin-bottom:28px;">
                        <h3 style="margin-bottom:8px;">Roller Conveyors</h3>
                        <p style="line-height:1.7;">Gravity and powered roller systems designed for heavy boxes, pallets, and large industrial components.</p>
                    </div>
                    <div style="border-left:3px solid var(--primary-blue); padding-left:20px; margin-bottom:28px;">
                        <h3 style="margin-bottom:8px;">Modular Plastic Belts</h3>
                        <p style="line-height:1.7;">Easy to clean, highly durable, and flexible — perfect for food processing and pharmaceutical environments.</p>
                    </div>
                    <div style="border-left:3px solid var(--primary-blue); padding-left:20px;">
                        <h3 style="margin-bottom:8px;">Chain Conveyors</h3>
                        <p style="line-height:1.7;">Heavy-load chain systems for automotive, metal fabrication, and warehouse pallet movement applications.</p>
                    </div>
                </div>
                <div style="display:flex; flex-direction:column; gap:20px;">
                    <video autoplay loop muted playsinline src="../assets/videos/conveyor-1.mp4" style="width:100%; height:280px; object-fit:cover; border-radius:var(--radius-md);"></video>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
                        <div class="card bg-main" style="padding:20px; text-align:center;"><p class="text-primary" style="font-size:2rem; font-weight:700; margin:0;">100+</p><p style="font-size:0.9rem; margin:4px 0 0;">Systems Installed</p></div>
                        <div class="card bg-main" style="padding:20px; text-align:center;"><p class="text-primary" style="font-size:2rem; font-weight:700; margin:0;">24/7</p><p style="font-size:0.9rem; margin:4px 0 0;">Support Available</p></div>
                    </div>
                </div>
            </div>
        </div>
    </section>'''),

    'services.html': ('Services', 'Engineering design, manufacturing, installation, technical support, and maintenance services.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-3" style="margin-bottom:60px;">
                <div class="card bg-main" style="padding:32px; box-shadow:var(--shadow-sm);">
                    <div style="font-size:2rem; margin-bottom:14px;">📐</div>
                    <h3 style="margin-bottom:12px; color:var(--primary-blue);">Engineering Design</h3>
                    <p style="line-height:1.7;">3D CAD modelling and process-flow optimisation tailored to your specific facility layout and capacity targets.</p>
                </div>
                <div class="card bg-main" style="padding:32px; box-shadow:var(--shadow-sm);">
                    <div style="font-size:2rem; margin-bottom:14px;">🏭</div>
                    <h3 style="margin-bottom:12px; color:var(--primary-blue);">Manufacturing</h3>
                    <p style="line-height:1.7;">In-house fabrication using food-grade stainless steel, precision aluminium profiles, and certified components.</p>
                </div>
                <div class="card bg-main" style="padding:32px; box-shadow:var(--shadow-sm);">
                    <div style="font-size:2rem; margin-bottom:14px;">🔧</div>
                    <h3 style="margin-bottom:12px; color:var(--primary-blue);">Installation</h3>
                    <p style="line-height:1.7;">Professional on-site assembly, electrical wiring, PLC programming, and full commissioning by certified engineers.</p>
                </div>
                <div class="card bg-main" style="padding:32px; box-shadow:var(--shadow-sm);">
                    <div style="font-size:2rem; margin-bottom:14px;">⚙️</div>
                    <h3 style="margin-bottom:12px; color:var(--primary-blue);">Preventative Maintenance</h3>
                    <p style="line-height:1.7;">Annual Maintenance Contracts (AMC) designed to prevent breakdowns and extend the life of your equipment.</p>
                </div>
                <div class="card bg-main" style="padding:32px; box-shadow:var(--shadow-sm);">
                    <div style="font-size:2rem; margin-bottom:14px;">🤖</div>
                    <h3 style="margin-bottom:12px; color:var(--primary-blue);">Automation Upgrades</h3>
                    <p style="line-height:1.7;">Integrating modern PLC systems, vision sensors, and robotics into existing manual production lines.</p>
                </div>
                <div class="card bg-main" style="padding:32px; box-shadow:var(--shadow-sm);">
                    <div style="font-size:2rem; margin-bottom:14px;">📦</div>
                    <h3 style="margin-bottom:12px; color:var(--primary-blue);">Spare Parts Supply</h3>
                    <p style="line-height:1.7;">Stocked inventory of genuine belts, motors, sensors, and rollers for fast dispatch across Egypt and the GCC.</p>
                </div>
            </div>
            <div style="text-align:center;">
                <a href="contact.html" class="btn btn-primary" style="padding:14px 32px; text-decoration:none;">Speak with Our Team</a>
            </div>
        </div>
    </section>'''),

    'contact.html': ('Contact Us', 'Contact Iconic Mach Engineering for inquiries or to request a site visit.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-2" style="align-items:start; margin-bottom:60px;">
                <div>
                    <h2 class="text-primary" style="font-size:1.8rem; margin-bottom:16px;">Get in Touch</h2>
                    <p style="line-height:1.8; margin-bottom:32px; color:var(--text-muted);">Have a project in mind? Our engineering team is ready to consult, visit your site, and design the perfect solution.</p>
                    <div style="display:flex; flex-direction:column; gap:20px; margin-bottom:32px;">
                        <div style="display:flex; align-items:flex-start; gap:16px;">
                            <div style="font-size:1.6rem; line-height:1;">📍</div>
                            <div><strong>Address</strong><br><span style="color:var(--text-muted);">10th of Ramadan &ndash; Al Hashemia Mall &ndash; Tower (W) &ndash; 3rd Floor &ndash; behind the Vodafone branch, Al Sharqiya, Egypt<br><a href="https://www.google.com/maps/place/El+Hashemeya+Market+Centre/@30.2930808,31.7461565,18z/data=!4m6!3m5!1s0x1457fd95bdb45c5d:0xebe21a3cdcc6d742!8m2!3d30.2930808!4d31.7461565!16s%2Fg%2F1pty73hds" target="_blank" rel="noopener" style="color:var(--primary-blue); font-weight:600; text-decoration:none;">Open in Google Maps &rarr;</a></span></div>
                        </div>
                        <div style="display:flex; align-items:flex-start; gap:16px;">
                            <div style="font-size:1.6rem; line-height:1;">📱</div>
                            <div><strong>Phone / WhatsApp</strong><br><a href="https://wa.me/201068472717" style="color:var(--primary-blue); text-decoration:none; font-weight:600;">+20 10 68472717</a></div>
                        </div>
                        <div style="display:flex; align-items:flex-start; gap:16px;">
                            <div style="font-size:1.6rem; line-height:1;">✉️</div>
                            <div><strong>Sales Enquiries</strong><br><a href="mailto:sales@iconicmach.com" style="color:var(--primary-blue); text-decoration:none;">sales@iconicmach.com</a></div>
                        </div>
                        <div style="display:flex; align-items:flex-start; gap:16px;">
                            <div style="font-size:1.6rem; line-height:1;">🔧</div>
                            <div><strong>Technical Support</strong><br><a href="mailto:technical@iconicmach.com" style="color:var(--primary-blue); text-decoration:none;">technical@iconicmach.com</a></div>
                        </div>
                    </div>
                    <!-- Map -->
                    <div style="border-radius:var(--radius-md); overflow:hidden; box-shadow:var(--shadow-sm);">
                        <iframe
                            title="Iconic Mach Engineering Location"
                            src="https://www.google.com/maps?q=30.2930808,31.7461565&z=18&output=embed"
                            width="100%" height="300" style="border:0; display:block;" allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade">
                        </iframe>
                    </div>
                </div>
                <div>
                    <form id="contact-form" class="inquiry-form card bg-main" data-form-type="contact" method="POST" action="https://api.web3forms.com/submit" style="display:flex; flex-direction:column; gap:18px; padding:40px; box-shadow:var(--shadow-md);">
                        <h3 style="margin-bottom:8px;">Send us a Message</h3>
                        <input type="text" id="name" name="name" autocomplete="name" placeholder="Your Name *" aria-label="Your Name" required style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; font-size:0.95rem; background:var(--bg-alt);">
                        <input type="email" id="email" name="email" autocomplete="email" placeholder="Your Email *" aria-label="Your Email" required style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; font-size:0.95rem; background:var(--bg-alt);">
                        <input type="tel" id="phone" name="phone" autocomplete="tel" placeholder="Phone Number" aria-label="Phone Number" style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; font-size:0.95rem; background:var(--bg-alt);">
                        <input type="text" id="subject" name="subject" placeholder="Subject *" aria-label="Subject" required style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; font-size:0.95rem; background:var(--bg-alt);">
                        <textarea id="message" name="message" placeholder="Tell us about your project... *" aria-label="Message" rows="5" required style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; font-size:0.95rem; background:var(--bg-alt); resize:vertical;"></textarea>
                        <input type="text" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute; left:-9999px; opacity:0; height:0; width:0;">
                        <div class="form-status" role="status" aria-live="polite" hidden></div>
                        <button type="submit" class="btn btn-primary" style="padding:14px; font-weight:600; border:none; cursor:pointer; font-size:1rem;">Send Message</button>
                    </form>
                </div>
            </div>
        </div>
    </section>'''),

    'about.html': ('About Us', 'Learn about Iconic Mach Engineering — our story, team and mission.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-2" style="align-items:center; margin-bottom:60px;">
                <div>
                    <h2 class="text-primary" style="font-size:1.8rem; margin-bottom:16px;">Our Story</h2>
                    <p style="line-height:1.8; margin-bottom:16px;">Founded on principles of innovation and reliability, Iconic Mach Engineering has grown to become a trusted industrial partner across Egypt and the Gulf region.</p>
                    <p style="line-height:1.8; margin-bottom:24px;">We believe that quality engineering stands the test of time — every system we build is designed to maximise efficiency, minimise downtime, and deliver measurable ROI to our clients.</p>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
                        <div class="card bg-main" style="padding:20px; text-align:center;"><p class="text-primary" style="font-size:2rem; font-weight:700; margin:0;">100+</p><p style="font-size:0.85rem; margin:4px 0 0;">Projects Delivered</p></div>
                        <div class="card bg-main" style="padding:20px; text-align:center;"><p class="text-primary" style="font-size:2rem; font-weight:700; margin:0;">15+</p><p style="font-size:0.85rem; margin:4px 0 0;">Years of Excellence</p></div>
                    </div>
                </div>
                <div>
                    <img src="../assets/images/mahmoud-turk.jpeg" alt="Mahmoud Turk — Founder" style="width:100%; border-radius:var(--radius-md); box-shadow:var(--shadow-sm);">
                    <p style="text-align:center; font-size:0.9rem; margin-top:10px; color:var(--text-muted);">Mahmoud Turk — Founder & CEO</p>
                </div>
            </div>
            <!-- Mission & Vision -->
            <div class="grid grid-3" style="margin-bottom:40px;">
                <div class="card bg-main" style="padding:28px; border-top:4px solid var(--primary-blue);">
                    <h3 style="margin-bottom:10px;">🎯 Our Mission</h3>
                    <p style="line-height:1.7;">To deliver world-class industrial engineering solutions that empower Egyptian and GCC manufacturers to compete globally.</p>
                </div>
                <div class="card bg-main" style="padding:28px; border-top:4px solid var(--primary-blue);">
                    <h3 style="margin-bottom:10px;">👁️ Our Vision</h3>
                    <p style="line-height:1.7;">To be the leading industrial automation partner in the MENA region, known for quality, reliability, and innovation.</p>
                </div>
                <div class="card bg-main" style="padding:28px; border-top:4px solid var(--primary-blue);">
                    <h3 style="margin-bottom:10px;">💡 Our Values</h3>
                    <p style="line-height:1.7;">Precision engineering, transparent partnerships, and a relentless commitment to our clients' operational success.</p>
                </div>
            </div>
        </div>
    </section>'''),

    'industries.html': ('Industries Served', 'We power manufacturing across food & beverage, FMCG, logistics, and more.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-3" style="margin-bottom:60px;">
                <div class="card bg-main" style="padding:28px; border-top:4px solid var(--primary-blue);">
                    <div style="font-size:2.2rem; margin-bottom:14px;">🍽️</div>
                    <h3 style="margin-bottom:10px; color:var(--primary-blue);">Food & Beverage</h3>
                    <p style="line-height:1.7;">Sanitary production and conveyor lines compliant with food-safety regulations.</p>
                </div>
                <div class="card bg-main" style="padding:28px; border-top:4px solid var(--primary-blue);">
                    <div style="font-size:2.2rem; margin-bottom:14px;">📦</div>
                    <h3 style="margin-bottom:10px; color:var(--primary-blue);">FMCG & Packaging</h3>
                    <p style="line-height:1.7;">Ultra-high-speed packaging lines for consumer goods, eliminating every bottleneck.</p>
                </div>
                <div class="card bg-main" style="padding:28px; border-top:4px solid var(--primary-blue);">
                    <div style="font-size:2.2rem; margin-bottom:14px;">🏗️</div>
                    <h3 style="margin-bottom:10px; color:var(--primary-blue);">Warehousing & Logistics</h3>
                    <p style="line-height:1.7;">Sorting, palletising, and distribution conveyor systems for modern warehouses.</p>
                </div>
                <div class="card bg-main" style="padding:28px; border-top:4px solid var(--primary-blue);">
                    <div style="font-size:2.2rem; margin-bottom:14px;">🚗</div>
                    <h3 style="margin-bottom:10px; color:var(--primary-blue);">Automotive</h3>
                    <p style="line-height:1.7;">Heavy-duty assembly and welding lines engineered for automotive manufacturing plants.</p>
                </div>
                <div class="card bg-main" style="padding:28px; border-top:4px solid var(--primary-blue);">
                    <div style="font-size:2.2rem; margin-bottom:14px;">💊</div>
                    <h3 style="margin-bottom:10px; color:var(--primary-blue);">Pharmaceuticals</h3>
                    <p style="line-height:1.7;">Cleanroom-grade conveyors and filling lines meeting GMP and FDA standards.</p>
                </div>
                <div class="card bg-main" style="padding:28px; border-top:4px solid var(--primary-blue);">
                    <div style="font-size:2.2rem; margin-bottom:14px;">🏭</div>
                    <h3 style="margin-bottom:10px; color:var(--primary-blue);">General Manufacturing</h3>
                    <p style="line-height:1.7;">Custom solutions for any industrial application — if you manufacture it, we can automate it.</p>
                </div>
            </div>
        </div>
    </section>'''),

    'projects.html': ('Projects', 'Iconic Mach Engineering portfolio of completed industrial projects.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div style="margin-bottom:48px;">
                <video autoplay loop muted playsinline src="../assets/videos/full line.mp4" style="width:100%; height:380px; object-fit:cover; border-radius:var(--radius-md); box-shadow:var(--shadow-sm);"></video>
            </div>
            <p style="max-width:760px; margin:0 auto 48px; text-align:center; line-height:1.8; color:var(--text-muted);">From high-speed packaging lines to complex multi-tier sorting systems &mdash; explore how we have transformed manufacturing floors across Egypt and the GCC.</p>
            <div class="grid grid-2">
                <div class="card bg-main" style="padding:0; overflow:hidden;"><video autoplay loop muted playsinline src="../assets/videos/beverages.mp4" style="width:100%;height:200px;object-fit:cover;"></video><div style="padding:20px;"><h4 style="margin-bottom:6px;">Beverage Filling Line</h4><p style="font-size:0.9rem;color:var(--text-muted);">Complete filling and capping line &mdash; 12,000 bottles/hr</p></div></div>
                <div class="card bg-main" style="padding:0; overflow:hidden;"><video autoplay loop muted playsinline src="../assets/videos/packing.mp4" style="width:100%;height:200px;object-fit:cover;"></video><div style="padding:20px;"><h4 style="margin-bottom:6px;">FMCG Packaging System</h4><p style="font-size:0.9rem;color:var(--text-muted);">Multi-lane cartoning and case-packing line</p></div></div>
            </div>
            <div style="text-align:center; margin-top:40px;">
                <a href="contact.html" class="btn btn-primary" style="padding:14px 32px; text-decoration:none;">Start Your Project</a>
            </div>
        </div>
    </section>'''),

    'blog.html': ('Blog', 'Latest articles, insights and news from Iconic Mach Engineering.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-3">
                <div class="card bg-main" style="padding:0; overflow:hidden; box-shadow:var(--shadow-sm);">
                    <img src="../assets/images/industrial-process-1.jpeg" alt="" style="width:100%;height:180px;object-fit:cover;">
                    <div style="padding:24px;"><span style="font-size:0.8rem;color:var(--primary-blue);font-weight:600;">AUTOMATION</span><h3 style="margin:10px 0 10px;font-size:1.1rem;">Industry 4.0: What It Means for Egyptian Manufacturers</h3><p style="font-size:0.9rem;line-height:1.7;color:var(--text-muted);">Exploring how smart factory technologies are transforming local production floors.</p></div>
                </div>
                <div class="card bg-main" style="padding:0; overflow:hidden; box-shadow:var(--shadow-sm);">
                    <img src="../assets/images/industrial-process-7.jpeg" alt="" style="width:100%;height:180px;object-fit:cover;">
                    <div style="padding:24px;"><span style="font-size:0.8rem;color:var(--primary-blue);font-weight:600;">MAINTENANCE</span><h3 style="margin:10px 0 10px;font-size:1.1rem;">5 Signs Your Conveyor System Needs an Upgrade</h3><p style="font-size:0.9rem;line-height:1.7;color:var(--text-muted);">Recognising early warning signs before they turn into costly breakdowns.</p></div>
                </div>
                <div class="card bg-main" style="padding:0; overflow:hidden; box-shadow:var(--shadow-sm);">
                    <img src="../assets/images/industrial-process-8.jpeg" alt="" style="width:100%;height:180px;object-fit:cover;">
                    <div style="padding:24px;"><span style="font-size:0.8rem;color:var(--primary-blue);font-weight:600;">LEAN MANUFACTURING</span><h3 style="margin:10px 0 10px;font-size:1.1rem;">Reducing Waste with Lean Production Line Design</h3><p style="font-size:0.9rem;line-height:1.7;color:var(--text-muted);">How strategic layout changes can dramatically boost overall equipment effectiveness.</p></div>
                </div>
            </div>
        </div>
    </section>'''),

    'faq.html': ('FAQs', 'Frequently asked questions about Iconic Mach Engineering products and services.', '''
    <section id="main-content" class="section">
        <div class="container" style="max-width:800px;">
            <div style="display:flex; flex-direction:column; gap:16px;">
                <details class="card bg-main" style="padding:24px; cursor:pointer;"><summary style="font-weight:600; font-size:1rem; list-style:none; display:flex; justify-content:space-between;">Do you offer custom-designed systems? <span>&#43;</span></summary><p style="margin-top:16px; line-height:1.8; color:var(--text-muted);">Yes. Every system we build is custom-engineered to your specific space, throughput targets, and product requirements. We start with a site visit and detailed consultation.</p></details>
                <details class="card bg-main" style="padding:24px; cursor:pointer;"><summary style="font-weight:600; font-size:1rem; list-style:none; display:flex; justify-content:space-between;">What industries do you serve? <span>&#43;</span></summary><p style="margin-top:16px; line-height:1.8; color:var(--text-muted);">We work across food & beverage, FMCG, pharmaceuticals, automotive, warehousing, and general manufacturing. Any production environment can benefit from our solutions.</p></details>
                <details class="card bg-main" style="padding:24px; cursor:pointer;"><summary style="font-weight:600; font-size:1rem; list-style:none; display:flex; justify-content:space-between;">Do you provide after-sales maintenance? <span>&#43;</span></summary><p style="margin-top:16px; line-height:1.8; color:var(--text-muted);">Absolutely. We offer Annual Maintenance Contracts (AMC) that include scheduled inspections, preventive part replacements, and priority emergency response.</p></details>
                <details class="card bg-main" style="padding:24px; cursor:pointer;"><summary style="font-weight:600; font-size:1rem; list-style:none; display:flex; justify-content:space-between;">How long does a typical installation take? <span>&#43;</span></summary><p style="margin-top:16px; line-height:1.8; color:var(--text-muted);">Timelines vary by project complexity. A standard conveyor system takes 2–4 weeks from design approval to commissioning. Full production lines may take 6–12 weeks.</p></details>
                <details class="card bg-main" style="padding:24px; cursor:pointer;"><summary style="font-weight:600; font-size:1rem; list-style:none; display:flex; justify-content:space-between;">Can you upgrade my existing equipment? <span>&#43;</span></summary><p style="margin-top:16px; line-height:1.8; color:var(--text-muted);">Yes. We specialise in automation upgrades — integrating modern PLCs, sensors, and control systems into your existing lines without requiring a full replacement.</p></details>
            </div>
        </div>
    </section>'''),

    'request-quotation.html': ('Request Quotation', 'Request a quotation from Iconic Mach Engineering for your industrial project.', '''
    <section id="main-content" class="section">
        <div class="container" style="max-width:700px;">
            <p style="text-align:center; line-height:1.8; margin-bottom:40px; color:var(--text-muted);">Fill in the form below and our sales team will get back to you within one business day with a detailed, competitive quotation.</p>
            <form id="quotation-form" class="inquiry-form card bg-main" data-form-type="quotation" method="POST" action="https://api.web3forms.com/submit" style="display:flex; flex-direction:column; gap:18px; padding:40px; box-shadow:var(--shadow-md);">
                <input type="text" id="name" name="name" autocomplete="name" placeholder="Full Name *" aria-label="Full Name" required style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; background:var(--bg-alt);">
                <input type="text" id="company" name="company" autocomplete="organization" placeholder="Company Name" aria-label="Company Name" style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; background:var(--bg-alt);">
                <input type="email" id="email" name="email" autocomplete="email" placeholder="Email Address *" aria-label="Email Address" required style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; background:var(--bg-alt);">
                <input type="tel" id="phone" name="phone" autocomplete="tel" placeholder="Phone / WhatsApp" aria-label="Phone or WhatsApp" style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; background:var(--bg-alt);">
                <select id="product" name="product" aria-label="Product or Service Required" style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; background:var(--bg-alt);">
                    <option value="">Product / Service Required</option>
                    <option>Production Line</option>
                    <option>Conveyor System</option>
                    <option>Maintenance Contract</option>
                    <option>Automation Upgrade</option>
                    <option>Spare Parts</option>
                    <option>Other</option>
                </select>
                <textarea id="message" name="message" placeholder="Describe your project requirements... *" aria-label="Project requirements" rows="6" required style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; background:var(--bg-alt); resize:vertical;"></textarea>
                <input type="text" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute; left:-9999px; opacity:0; height:0; width:0;">
                <div class="form-status" role="status" aria-live="polite" hidden></div>
                <button type="submit" class="btn btn-primary" style="padding:14px; font-weight:600; border:none; cursor:pointer; font-size:1rem;">Submit Quotation Request</button>
            </form>
        </div>
    </section>'''),

    'technical-support.html': ('Technical Support', '24/7 technical support for all Iconic Mach Engineering installations.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-2" style="align-items:center; margin-bottom:60px;">
                <div>
                    <h2 class="text-primary" style="font-size:1.8rem; margin-bottom:16px;">Always On, Always Ready</h2>
                    <p style="line-height:1.8; margin-bottom:16px;">Machine downtime is costly. Our rapid-response engineering team is on standby around the clock to diagnose and resolve issues before they impact your production targets.</p>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:12px; margin-bottom:28px;">
                        <li style="display:flex; gap:12px; align-items:flex-start;"><span style="color:var(--primary-blue); font-weight:700; font-size:1.2rem;">✓</span> Remote diagnostics &amp; PLC troubleshooting</li>
                        <li style="display:flex; gap:12px; align-items:flex-start;"><span style="color:var(--primary-blue); font-weight:700; font-size:1.2rem;">✓</span> On-site field technician dispatch</li>
                        <li style="display:flex; gap:12px; align-items:flex-start;"><span style="color:var(--primary-blue); font-weight:700; font-size:1.2rem;">✓</span> Emergency spare parts delivery</li>
                        <li style="display:flex; gap:12px; align-items:flex-start;"><span style="color:var(--primary-blue); font-weight:700; font-size:1.2rem;">✓</span> Annual Maintenance Contracts (AMC)</li>
                    </ul>
                    <a href="https://wa.me/201068472717" class="btn btn-primary" style="padding:14px 28px; text-decoration:none;">WhatsApp Support Now</a>
                </div>
                <div><img src="../assets/images/industrial-process-5.jpeg" alt="Technical Support" style="width:100%; border-radius:var(--radius-md); box-shadow:var(--shadow-sm);"></div>
            </div>
        </div>
    </section>'''),

    'spare-parts.html': ('Spare Parts', 'Order genuine spare parts for your Iconic Mach Engineering systems.', '''
    <section id="main-content" class="section">
        <div class="container">
            <p style="max-width:700px; margin:0 auto 48px; text-align:center; line-height:1.8; color:var(--text-muted);">Using genuine parts ensures optimal performance and extends the lifespan of your equipment. We maintain a comprehensive inventory for immediate dispatch.</p>
            <div class="grid grid-3" style="margin-bottom:48px;">
                <div class="card bg-main" style="padding:28px; text-align:center;">
                    <div style="font-size:2rem; margin-bottom:12px;">🔗</div>
                    <h3 style="margin-bottom:8px;">Conveyor Belts</h3>
                    <p style="line-height:1.7; font-size:0.92rem;">PVC, PU, modular plastic, and metal belts in all standard widths.</p>
                </div>
                <div class="card bg-main" style="padding:28px; text-align:center;">
                    <div style="font-size:2rem; margin-bottom:12px;">⚡</div>
                    <h3 style="margin-bottom:8px;">Drive Motors</h3>
                    <p style="line-height:1.7; font-size:0.92rem;">Single and three-phase motors, gearboxes, and frequency inverters.</p>
                </div>
                <div class="card bg-main" style="padding:28px; text-align:center;">
                    <div style="font-size:2rem; margin-bottom:12px;">📡</div>
                    <h3 style="margin-bottom:8px;">Sensors & Controls</h3>
                    <p style="line-height:1.7; font-size:0.92rem;">Proximity sensors, photo-eyes, encoders, and PLC modules.</p>
                </div>
            </div>
            <div style="text-align:center;">
                <a href="contact.html" class="btn btn-primary" style="padding:14px 32px; text-decoration:none;">Order Parts</a>
            </div>
        </div>
    </section>'''),

    'privacy-policy.html': ('Privacy Policy', 'Privacy policy for Iconic Mach Engineering.', '''
    <section id="main-content" class="section">
        <div class="container" style="max-width:800px;">
            <div class="card bg-main" style="padding:40px; box-shadow:var(--shadow-sm);">
                <h2 class="text-primary" style="margin-bottom:20px;">Your Privacy Matters</h2>
                <p style="line-height:1.8; margin-bottom:16px;">Iconic Mach Engineering is committed to protecting your personal information. We collect only the data necessary to respond to your enquiries and improve our services.</p>
                <h3 style="margin:24px 0 10px;">What We Collect</h3>
                <p style="line-height:1.8; margin-bottom:16px;">Name, email address, phone number, and project details provided through our contact or quotation forms.</p>
                <h3 style="margin:24px 0 10px;">How We Use It</h3>
                <p style="line-height:1.8; margin-bottom:16px;">Your data is used solely to respond to your enquiries and, where consented, to send relevant engineering updates. It is never sold to third parties.</p>
                <h3 style="margin:24px 0 10px;">Contact Us</h3>
                <p style="line-height:1.8;">For any privacy concerns, please email <a href="mailto:sales@iconicmach.com" style="color:var(--primary-blue);">sales@iconicmach.com</a>.</p>
            </div>
        </div>
    </section>'''),

    'terms.html': ('Terms & Conditions', 'Terms and conditions for Iconic Mach Engineering services.', '''
    <section id="main-content" class="section">
        <div class="container" style="max-width:800px;">
            <div class="card bg-main" style="padding:40px; box-shadow:var(--shadow-sm);">
                <h2 class="text-primary" style="margin-bottom:20px;">Terms & Conditions</h2>
                <p style="line-height:1.8; margin-bottom:16px;">By engaging with Iconic Mach Engineering for products or services, you agree to the following terms. These terms govern the use of our website, quotations, contracts, and installations.</p>
                <h3 style="margin:24px 0 10px;">Quotations</h3>
                <p style="line-height:1.8; margin-bottom:16px;">All quotations are valid for 30 days from the date of issue unless otherwise stated. Prices are subject to material and currency fluctuations.</p>
                <h3 style="margin:24px 0 10px;">Warranties</h3>
                <p style="line-height:1.8; margin-bottom:16px;">All manufactured systems carry a 12-month warranty against defects in materials and workmanship from the date of commissioning.</p>
                <h3 style="margin:24px 0 10px;">Intellectual Property</h3>
                <p style="line-height:1.8;">All engineering drawings, designs, and documentation produced by Iconic Mach Engineering remain our intellectual property unless explicitly transferred in writing.</p>
            </div>
        </div>
    </section>'''),
}

# ---------------------------------------------------------------------------
# Blog articles
# ---------------------------------------------------------------------------
# NOTE: these are first drafts written to give the blog real, linkable pages.
# Review the copy before treating it as final marketing material.

ARTICLES = [
    {
        "file": "blog-industry-4-0-egypt.html",
        "category": "AUTOMATION",
        "title": "Industry 4.0: What It Means for Egyptian Manufacturers",
        "excerpt": "Exploring how smart factory technologies are transforming local production floors.",
        "image": "../assets/images/industrial-process-1.jpeg",
        "date": "2026-07-14",
        "date_label": "14 July 2026",
        "read": "6 min read",
        "body": '''
            <p>&ldquo;Industry 4.0&rdquo; gets used loosely enough that it has started to sound like a slogan. Stripped of the marketing, it describes something concrete: machines on the factory floor that report what they are doing, and software that turns those reports into decisions. Nothing more mystical than that.</p>
            <p>For manufacturers in Egypt, the practical question is not whether the concept is valid. It is where to start, and what actually pays for itself on a local production floor.</p>

            <h2>Start with visibility, not robots</h2>
            <p>The most common mistake we see is treating Industry 4.0 as a hardware purchase. A plant invests in an expensive automated cell, installs it beside lines that are still managed on paper, and the bottleneck simply moves somewhere else.</p>
            <p>The cheaper and far more useful first step is instrumentation. Before you automate a process, you need to know how that process currently behaves:</p>
            <ul>
                <li>How many units per hour does each station really produce, on an average shift rather than a good one?</li>
                <li>Where does the line stop, how often, and for how long each time?</li>
                <li>Which stoppages are mechanical, which are material starvation, and which are operator-dependent?</li>
            </ul>
            <p>Sensors and a PLC that logs downtime by reason code will answer these questions within a few weeks of running. That data almost always redirects the investment plan — the constraint is rarely where management assumed it was.</p>

            <h2>OEE is the number that matters</h2>
            <p>Overall Equipment Effectiveness combines three things into one figure: how much of the planned time the line was available, how close it ran to its rated speed, and how much of its output was good on the first pass.</p>
            <p>It is useful precisely because it refuses to let any one of the three hide behind the others. A line running at full rated speed for four hours a day is not a fast line. A line running continuously while producing rework is not a productive line. Tracking OEE per shift, and reviewing it with the people who run the shift, tends to surface problems that never make it into a management report.</p>

            <h2>What the Egyptian context changes</h2>
            <p>Some of the standard advice needs adjusting for local conditions.</p>
            <ul>
                <li><strong>Power stability.</strong> Control systems and drives should be specified with the assumption that supply will not always be clean. Protection and a graceful, controlled restart matter more than an extra feature on the HMI.</li>
                <li><strong>Spare parts lead time.</strong> An imported component with a long lead time is a production risk, not just a purchasing line item. Where the engineering allows it, choosing parts that are locally serviceable is worth a small compromise on specification.</li>
                <li><strong>Operator familiarity.</strong> An interface in Arabic, with the alarm text written in the language the maintenance team actually uses, is not a nicety. It is the difference between a fault that is diagnosed in minutes and one that waits for a call-out.</li>
                <li><strong>Retrofit over replacement.</strong> Much of the installed base in Egypt is mechanically sound but electrically dated. Modern PLCs, sensors and drives can frequently be fitted to existing frames, which changes the economics considerably.</li>
            </ul>

            <h2>A sensible sequence</h2>
            <p>For most plants, the order that works looks like this:</p>
            <ol>
                <li>Instrument the existing line and collect downtime data for a full production cycle.</li>
                <li>Fix what the data exposes — usually changeover time, material handling, or a single recurring mechanical fault.</li>
                <li>Automate the step that remains the constraint once the easy problems are gone.</li>
                <li>Connect the line to a central dashboard so the improvement is visible and does not quietly decay.</li>
            </ol>
            <p>Each stage funds the next. That matters more than technological ambition, because it means the programme survives a change in budget or priorities.</p>

            <h2>The honest summary</h2>
            <p>Industry 4.0 is not a threshold you cross. It is a habit of measuring what your equipment does and acting on the measurement. Plants that build that habit get value from modest, incremental investment. Plants that buy the technology without the habit generally end up with expensive equipment and the same output.</p>
        ''',
    },
    {
        "file": "blog-conveyor-upgrade-signs.html",
        "category": "MAINTENANCE",
        "title": "5 Signs Your Conveyor System Needs an Upgrade",
        "excerpt": "Recognising early warning signs before they turn into costly breakdowns.",
        "image": "../assets/images/industrial-process-7.jpeg",
        "date": "2026-06-23",
        "date_label": "23 June 2026",
        "read": "5 min read",
        "body": '''
            <p>Conveyor systems rarely fail without warning. They degrade — slowly enough that the people working beside them every day stop noticing, until an unplanned stoppage makes the problem impossible to ignore.</p>
            <p>These are the five signals that most reliably indicate a system has moved past routine maintenance and into upgrade territory.</p>

            <h2>1. Belt tracking needs constant correction</h2>
            <p>A belt that drifts off centre and has to be adjusted every few days is telling you something structural. Persistent mistracking usually points to a frame that is out of square, worn or misaligned idlers, or a pulley that is no longer true.</p>
            <p>Repeated adjustment treats the symptom. Meanwhile the belt edge wears against the frame, and material spills at the point of drift. When tracking correction has become part of the weekly routine rather than an occasional task, the frame and roller set are due for assessment.</p>

            <h2>2. Motor current is climbing for the same load</h2>
            <p>If your drive is drawing measurably more current than it did for an identical duty, something is resisting the motion — seized rollers, bearing wear, contaminated take-up, or a belt that has stiffened with age.</p>
            <p>This one is worth watching because it is quantifiable and it precedes failure by a comfortable margin. A drive that is working harder is also running hotter, and heat shortens the life of every component around it. A simple trend log on motor current is one of the cheapest early-warning systems available.</p>

            <h2>3. Changeover takes longer than the run</h2>
            <p>Many older conveyor installations were designed around a single product at a stable volume. If your product mix has broadened since then, you may be spending a disproportionate share of the shift reconfiguring guides, adjusting heights and re-timing transfers.</p>
            <p>This is a design constraint, not a maintenance problem, and no amount of servicing will resolve it. Adjustable guide rails, quick-release fittings and recipe-driven positioning are the kind of change that pays back in recovered production hours rather than reduced repair cost.</p>

            <h2>4. Spare parts are getting hard to source</h2>
            <p>When a control component is discontinued and the only supply is the second-hand market, your production continuity now depends on a scarce part. The risk is not gradual — it is a single failure away from an extended stoppage.</p>
            <p>The same applies to a PLC that no longer has vendor support, or a drive whose programming software will not run on any computer you currently own. If restoring the system after a failure depends on knowledge held by one person, the exposure is real, and an upgrade to a supported platform is cheaper than the outage it prevents.</p>

            <h2>5. Product damage or spillage has crept upward</h2>
            <p>Rising reject rates at the end of a line are often attributed to upstream process variation when the actual cause is transport. Worn transfer plates, gaps at junctions, misaligned side guides and inconsistent speed matching between sections all cause product to tip, jam or abrade.</p>
            <p>Because the damage is distributed across the line rather than caused by a single obvious fault, it tends to be absorbed into the accepted scrap figure. It is worth checking directly: inspect the product immediately before and immediately after each transfer point and see where the condition changes.</p>

            <h2>How to decide</h2>
            <p>One of these signs on its own is usually a maintenance item. Three or more together generally means the system has drifted far enough from its original condition that continued repair is the more expensive path.</p>
            <p>The useful comparison is not upgrade cost against repair cost. It is upgrade cost against the annual value of the downtime, scrap and labour the current system consumes. Once that figure is written down, the decision is normally straightforward.</p>
        ''',
    },
    {
        "file": "blog-lean-production-line-waste.html",
        "category": "LEAN MANUFACTURING",
        "title": "Reducing Waste with Lean Production Line Design",
        "excerpt": "How strategic layout changes can dramatically boost overall equipment effectiveness.",
        "image": "../assets/images/industrial-process-8.jpeg",
        "date": "2026-05-30",
        "date_label": "30 May 2026",
        "read": "6 min read",
        "body": '''
            <p>Lean is usually introduced as a set of practices applied to an existing line — reduce inventory, shorten changeovers, standardise work. All of that is sound. But a significant share of the waste in a typical plant was designed in before the first unit was ever produced, and no amount of operational discipline fully removes it.</p>
            <p>Layout decisions are the ones that keep costing money quietly, every shift, for the working life of the line.</p>

            <h2>Waste that layout creates</h2>
            <p>Of the classic categories of waste, three are largely determined by physical arrangement:</p>
            <ul>
                <li><strong>Transport.</strong> Every metre a part travels between operations is handling that adds cost and no value. Long runs also introduce more transfer points, and every transfer point is a potential jam.</li>
                <li><strong>Motion.</strong> If an operator turns, stretches or walks to complete a cycle, that movement repeats thousands of times a week. It is both a productivity cost and an ergonomic one.</li>
                <li><strong>Inventory.</strong> Work in progress accumulates wherever the line's flow rate changes. Buffers between mismatched stations are a symptom of an unbalanced layout, not a solution to it.</li>
            </ul>

            <h2>Balance the line to the constraint</h2>
            <p>A production line runs at the speed of its slowest station, and every station faster than that is producing inventory rather than output.</p>
            <p>The practical exercise is to measure the real cycle time of each station — including the variation, not just the average — and plot them side by side. Two patterns usually appear: one station is clearly the constraint, and several others have far more capacity than they will ever be allowed to use.</p>
            <p>That chart directs the investment. Adding capacity anywhere except the constraint changes nothing. Splitting the constraint's work across two stations, or reducing its cycle time directly, raises the output of the whole line.</p>

            <h2>Design for changeover from the start</h2>
            <p>Where product mix is broad, changeover time is often the single largest recoverable loss, and it is far cheaper to design out than to retrofit.</p>
            <p>The principle is to convert work that currently stops the line into work that can happen while it runs — staging tooling in advance, using positive stops instead of measured adjustment, keeping fasteners uniform so one tool serves the whole line, and holding format settings in the control system rather than in an operator's notebook.</p>
            <p>None of this is exotic. It simply has to be decided at design stage, because adding it later usually means dismantling what is already installed.</p>

            <h2>Let the layout show its own state</h2>
            <p>A well-designed line makes its condition visible without anyone having to ask. Clear sightlines down its length, defined floor space for work in progress so that accumulation is immediately obvious, and status indication that can be read from a distance all mean problems are noticed while they are still small.</p>
            <p>This is the least technical item on the list and frequently the most effective. Waste that is visible tends to get addressed. Waste hidden behind a machine or absorbed into a buffer does not.</p>

            <h2>Leave room to change</h2>
            <p>A line optimised precisely for today's product and volume is fragile. Product ranges widen, volumes shift, and a layout with no slack has to be rebuilt rather than adapted.</p>
            <p>Modular frames, service connections with spare capacity, and physical space reserved for an additional station are all modest costs at build time and expensive omissions later. The most efficient line is not the one that squeezes the most into the smallest footprint — it is the one still running efficiently after the third product change.</p>

            <h2>Where to begin</h2>
            <p>Walk your line and follow a single unit from raw material to finished pack, timing each step and recording every metre it travels and every point at which it waits. Most teams are surprised by the ratio of waiting to working.</p>
            <p>That one measurement, done honestly, will identify more opportunity than a general commitment to lean principles ever does.</p>
        ''',
    },
]


def article_page(a):
    """Full page content for one blog article."""
    return '''
    <section id="main-content" class="section">
        <div class="container" style="max-width:760px;">
            <p style="margin-bottom:28px;"><a href="blog.html" style="color:var(--primary-blue); text-decoration:none; font-size:0.9rem; font-weight:600;">&larr; Back to all articles</a></p>
            <p style="display:flex; gap:14px; flex-wrap:wrap; align-items:center; font-size:0.82rem; color:var(--text-muted); margin-bottom:28px;">
                <span style="color:var(--primary-blue); font-weight:700; letter-spacing:0.5px;">{category}</span>
                <span>&middot;</span><time datetime="{date}">{date_label}</time>
                <span>&middot;</span><span>{read}</span>
            </p>
            <article class="article-body" style="line-height:1.85; font-size:1.02rem;">
                {body}
            </article>
            <div class="card bg-alt" style="margin-top:56px; padding:36px; text-align:center; box-shadow:var(--shadow-sm);">
                <h3 style="margin-bottom:12px; font-size:1.2rem;">Planning a project like this?</h3>
                <p style="color:var(--text-muted); line-height:1.8; margin-bottom:24px;">Our engineers can review your current line and advise on the most cost-effective route forward &mdash; no obligation.</p>
                <div style="display:flex; gap:14px; justify-content:center; flex-wrap:wrap;">
                    <a href="request-quotation.html" class="btn btn-primary" style="padding:13px 28px; text-decoration:none;">Request a Quotation</a>
                    <a href="https://wa.me/201068472717" target="_blank" rel="noopener" style="padding:13px 28px; border:1px solid var(--border-color); border-radius:var(--radius-sm); text-decoration:none; color:inherit;">Ask on WhatsApp</a>
                </div>
            </div>
        </div>
    </section>'''.format(**a)


def blog_index():
    """Blog listing built from ARTICLES so cards and pages can't drift apart."""
    cards = []
    for a in ARTICLES:
        cards.append('''
                <a href="{file}" class="card bg-main" style="padding:0; overflow:hidden; box-shadow:var(--shadow-sm); text-decoration:none; color:inherit; display:block;">
                    <img src="{image}" alt="" style="width:100%;height:180px;object-fit:cover;">
                    <div style="padding:24px;">
                        <span style="font-size:0.8rem;color:var(--primary-blue);font-weight:600;">{category}</span>
                        <h3 style="margin:10px 0 10px;font-size:1.1rem;">{title}</h3>
                        <p style="font-size:0.9rem;line-height:1.7;color:var(--text-muted);">{excerpt}</p>
                        <p style="margin-top:16px;font-size:0.85rem;color:var(--text-muted);"><time datetime="{date}">{date_label}</time> &middot; {read}</p>
                        <span style="display:inline-block;margin-top:14px;color:var(--primary-blue);font-weight:600;font-size:0.9rem;">Read article &rarr;</span>
                    </div>
                </a>'''.format(**a))
    return '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-3">{}
            </div>
        </div>
    </section>'''.format("".join(cards))


# Homepage FAQ: the questions clients actually ask, plus FAQPage schema.
_home = pages['index.html']
pages['index.html'] = (_home[0], _home[1], _home[2] + widgets.home_faq_section('en'))

pages['blog.html'] = (
    'Blog',
    'Latest articles, insights and news from Iconic Mach Engineering.',
    blog_index(),
)

# Human-readable site tree.
page_heroes['sitemap.html'] = ('image', '../assets/images/industrial-process-2.jpeg', 'Site Map', 'Find any page on the site.')
pages['sitemap.html'] = ('Site Map', 'Every page on iconicmach.com, grouped by section.', widgets.sitemap_page('en'))

for _a in ARTICLES:
    page_heroes[_a['file']] = ('image', _a['image'], _a['title'], _a['excerpt'])
    pages[_a['file']] = (_a['title'], _a['excerpt'], article_page(_a))

ARTICLES_BY_FILE = {a['file']: a for a in ARTICLES}

template = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Iconic Mach Engineering</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{domain}/en/{slug}">
    <link rel="alternate" hreflang="en" href="{domain}/en/{slug}">
    <link rel="alternate" hreflang="ar" href="{domain}/ar/{slug}">
    <link rel="alternate" hreflang="x-default" href="{domain}/en/{slug}">
    <meta property="og:site_name" content="Iconic Mach Engineering">
    <meta property="og:title" content="{title} | Iconic Mach Engineering">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{domain}/en/{slug}">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="en_US">
    <meta property="og:locale:alternate" content="ar_EG">
    <meta property="og:image" content="{domain}/assets/images/iconicmach.png">
    <meta property="og:image:alt" content="Iconic Mach Engineering">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title} | Iconic Mach Engineering">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{domain}/assets/images/iconicmach.png">
    <meta name="theme-color" content="#0a3150">
    <meta name="google-site-verification" content="ZxGmIEGYMqXTRKbL504-jNNkEfy4EMSgmGBTkjyf20Y">
    <link rel="manifest" href="../site.webmanifest">
    <link rel="icon" type="image/png" href="../assets/images/favicon.png">
    <link rel="apple-touch-icon" href="../assets/images/iconicmach.png">
    <meta name="web3forms-key" content="{web3forms_key}">
    <script type="application/ld+json">{schema}</script>
    {analytics}
    {gtm_head}
    <link rel="stylesheet" href="../assets/css/variables.css?v={asset_version}">
    <link rel="stylesheet" href="../assets/css/reset.css?v={asset_version}">
    <link rel="stylesheet" href="../assets/css/layout.css?v={asset_version}">
    <link rel="stylesheet" href="../assets/css/components.css?v={asset_version}">
    <link rel="stylesheet" href="../assets/css/animations.css?v={asset_version}">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        @keyframes bounceDown {{
            0%,100% {{ transform: translateX(-50%) translateY(0); opacity:0.7; }}
            50% {{ transform: translateX(-50%) translateY(10px); opacity:1; }}
        }}
        details summary::-webkit-details-marker {{ display:none; }}
        details[open] summary span {{ transform:rotate(45deg); display:inline-block; transition:transform .2s; }}
    </style>
</head>
<body>
    {gtm_body}
    <div class="top-bar">
        <div class="container" style="display: flex; justify-content: space-between; align-items: center;">
            <div class="top-bar-contact">
                <a href="https://wa.me/201068472717" target="_blank" rel="noopener" style="margin-right: 15px;">
                    <span>📱</span> +20 10 68472717
                </a>
                <a href="mailto:sales@iconicmach.com" style="color: var(--text-muted); text-decoration: none; font-size: 0.9rem;">
                    <span>✉️</span> sales@iconicmach.com
                </a>
            </div>
                        <div class="top-bar-social">
                <a href="https://www.instagram.com/iconic.mach/" target="_blank" aria-label="Instagram" title="Instagram" style="display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,0.12);color:inherit;text-decoration:none;transition:background .2s,color .2s;" onmouseover="this.style.background='#e1306c';this.style.color='#fff';" onmouseout="this.style.background='rgba(255,255,255,0.12)';this.style.color='inherit';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg></a>
                <a href="https://www.tiktok.com/@iconicmach" target="_blank" aria-label="TikTok" title="TikTok" style="display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,0.12);color:inherit;text-decoration:none;transition:background .2s,color .2s;" onmouseover="this.style.background='#000000';this.style.color='#fff';" onmouseout="this.style.background='rgba(255,255,255,0.12)';this.style.color='inherit';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.32 6.32 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.69a8.16 8.16 0 004.77 1.52V6.74a4.85 4.85 0 01-1-.05z"/></svg></a>
                <a href="https://www.facebook.com/profile.php?id=61590558549282" target="_blank" aria-label="Facebook" title="Facebook" style="display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,0.12);color:inherit;text-decoration:none;transition:background .2s,color .2s;" onmouseover="this.style.background='#1877f2';this.style.color='#fff';" onmouseout="this.style.background='rgba(255,255,255,0.12)';this.style.color='inherit';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a>
                <a href="https://www.linkedin.com/in/mahmoud-turk-82bbb8412/" target="_blank" aria-label="LinkedIn" title="LinkedIn" style="display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,0.12);color:inherit;text-decoration:none;transition:background .2s,color .2s;" onmouseover="this.style.background='#0077b5';this.style.color='#fff';" onmouseout="this.style.background='rgba(255,255,255,0.12)';this.style.color='inherit';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>
                <a href="https://www.youtube.com/@Iconicmach" target="_blank" aria-label="YouTube" title="YouTube" style="display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,0.12);color:inherit;text-decoration:none;transition:background .2s,color .2s;" onmouseover="this.style.background='#ff0000';this.style.color='#fff';" onmouseout="this.style.background='rgba(255,255,255,0.12)';this.style.color='inherit';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a>
            </div>
        </div>
    </div>
    <header class="site-header">
        <div class="container">
            <a href="index.html" class="logo-container">
                <img src="../assets/images/iconicmach.png" alt="Iconic Mach Engineering">
            </a>
            <nav class="main-nav">
                <ul class="nav-links">
                    <li><a href="index.html">Home</a></li>
                    <li><a href="about.html">About Us</a></li>
                    <li><a href="production-lines.html">Production Lines</a></li>
                    <li><a href="conveyor-systems.html">Conveyor Systems</a></li>
                    <li><a href="services.html">Services</a></li>
                    <li><a href="contact.html">Contact Us</a></li>
                </ul>
            </nav>
            <div class="header-actions">
                <button id="theme-toggle" class="icon-btn">🌙</button>
                <a href="../ar/{slug}" id="lang-toggle" class="badge">عربي</a>
                <div class="menu-toggle"><span></span><span></span><span></span></div>
            </div>
        </div>
    </header>

    <main>
        {hero}
        {content}
    </main>

    {footer}
    <script src="../assets/js/main.js?v={asset_version}"></script>
    <script src="../assets/js/animations.js?v={asset_version}"></script>
    <script src="../assets/js/forms.js?v={asset_version}"></script>
    <script src="../assets/js/chat.js?v={asset_version}" defer></script>
{floating}
{video_loader}
</body>
</html>"""

os.makedirs('en', exist_ok=True)
for filename, (title, description, content) in pages.items():
    hero = make_hero(filename)
    filepath = os.path.join('en', filename)
    page = template.format(
        title=title,
        description=description,
        domain=domain,
        filename=filename,
        content=content,
        hero=hero,
        footer=FOOTER,
        schema=build_schema(filename, title, description),
        analytics=analytics_snippet(),
        gtm_head=widgets.gtm_head(),
        gtm_body=widgets.gtm_body(),
        web3forms_key=WEB3FORMS_ACCESS_KEY,
        slug=slug_for(filename),
        video_loader=VIDEO_LOADER,
        floating=widgets.floating_widgets("en"),
        asset_version=ASSET_VERSION,
    )
    page = prettify_links(page)
    page = lazy_load_images(page)
    page = defer_videos(page, VIDEO_POSTERS.get(filename, DEFAULT_POSTER))

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(page)
print("English pages generated successfully.")
