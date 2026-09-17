// assets/js/consent.js
//
// Cookie consent, wired to Google Consent Mode so that "decline" is real.
//
// How it fits together:
//   1. The GA snippet in <head> sets gtag('consent','default', ...) BEFORE
//      gtag('config'). If the visitor has not accepted, analytics_storage is
//      'denied' and GA4 runs in cookieless-ping mode: no _ga cookies, no
//      identifiers, only aggregate/modelled data.
//   2. This file shows the banner when no choice is stored, and on accept
//      calls gtag('consent','update') so GA4 switches to normal mode for the
//      rest of the visit. The choice is remembered in localStorage.
//   3. The Google Maps embed also sets cookies, so it ships with
//      data-consent-src instead of src and only loads on accept, or when the
//      visitor clicks its "Load map" placeholder.
//
// Cloudflare's __cf_bm is strictly necessary (bot protection) and is not
// gated; the privacy policy says so.

(function () {
    'use strict';

    var KEY = 'cookie-consent';
    var banner = document.getElementById('cookie-banner');
    if (!banner) return;

    function stored() {
        try { return localStorage.getItem(KEY); } catch (e) { return null; }
    }
    function remember(v) {
        try { localStorage.setItem(KEY, v); } catch (e) { /* private mode: banner just returns next visit */ }
    }

    function show() {
        banner.hidden = false;
        document.body.classList.add('cookie-open');
        // Move focus so keyboard users land on the choice, not behind it.
        var first = banner.querySelector('button');
        if (first) first.focus({ preventScroll: true });
    }
    function hide() {
        banner.hidden = true;
        document.body.classList.remove('cookie-open');
    }

    function updateGtag(state) {
        if (typeof window.gtag === 'function') {
            window.gtag('consent', 'update', { analytics_storage: state });
        }
    }

    // Embeds that were held back until consent.
    function loadGated(scope) {
        (scope || document).querySelectorAll('iframe[data-consent-src]').forEach(function (f) {
            f.src = f.getAttribute('data-consent-src');
            f.removeAttribute('data-consent-src');
            var ph = f.previousElementSibling;
            if (ph && ph.classList.contains('consent-placeholder')) ph.remove();
        });
    }

    function accept() {
        remember('granted');
        updateGtag('granted');
        loadGated();
        hide();
    }
    function decline() {
        remember('denied');
        updateGtag('denied');
        hide();
    }

    banner.querySelector('[data-consent="accept"]').addEventListener('click', accept);
    banner.querySelector('[data-consent="decline"]').addEventListener('click', decline);

    // "Load map" on the contact page: consent for that one embed only.
    document.querySelectorAll('[data-consent-load]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var ph = btn.closest('.consent-placeholder');
            var frame = ph && ph.nextElementSibling;
            if (frame && frame.hasAttribute('data-consent-src')) {
                frame.src = frame.getAttribute('data-consent-src');
                frame.removeAttribute('data-consent-src');
            }
            if (ph) ph.remove();
        });
    });

    // Footer "Cookie settings" link reopens the banner so a choice can be changed.
    window.openCookieSettings = function () { show(); };

    var choice = stored();
    if (choice === 'granted') {
        loadGated();
    } else if (choice === null) {
        show();
    }
    // 'denied': nothing to do — the head snippet already defaulted GA to denied.
})();
