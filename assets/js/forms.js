// assets/js/forms.js
// Handles every inquiry form on the site (contact + request-quotation, EN + AR).
//
// Submissions go straight from the browser to Web3Forms. This is deliberate:
// Web3Forms rejects server-side calls on the free plan ("This method is not
// allowed. Use our API in client side..."), so proxying through a Cloudflare
// Function does not work. The access key is public by design — Web3Forms
// states it is safe in client code, since the worst it allows is sending mail
// to the address that owns it.

const ENDPOINT = 'https://api.web3forms.com/submit';

const STRINGS = {
    en: {
        required: 'Please fill in all required fields.',
        badEmail: 'Please enter a valid email address.',
        sending: 'Sending...',
        success: 'Thank you! Your message has been sent. Our team will get back to you within one business day.',
        failure: 'Sorry, something went wrong. Please try again, or reach us on WhatsApp at +20 10 68472717.'
    },
    ar: {
        required: 'يرجى ملء جميع الحقول المطلوبة.',
        badEmail: 'يرجى إدخال بريد إلكتروني صحيح.',
        sending: 'جارٍ الإرسال...',
        success: 'شكراً لك! تم إرسال رسالتك بنجاح. سيتواصل معك فريقنا خلال يوم عمل واحد.',
        failure: 'عذراً، حدث خطأ ما. يرجى المحاولة مرة أخرى أو التواصل معنا عبر واتساب على 71768472 10 20+.'
    }
};

const LABELS = {
    en: { phone: 'Phone', company: 'Company', product: 'Product / Service', form: 'Form', page: 'Submitted from' },
    ar: { phone: 'الهاتف', company: 'الشركة', product: 'المنتج / الخدمة', form: 'النموذج', page: 'أُرسل من' }
};

const FORM_LABEL = {
    en: { contact: 'Contact Inquiry', quotation: 'Quotation Request' },
    ar: { contact: 'استفسار', quotation: 'طلب عرض سعر' }
};

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form.inquiry-form').forEach(setupForm);
});

function setupForm(form) {
    const lang = document.documentElement.lang === 'ar' ? 'ar' : 'en';
    const t = STRINGS[lang];
    const statusEl = form.querySelector('.form-status');
    const submitBtn = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const f = Object.fromEntries(new FormData(form).entries());

        // Honeypot — bots fill hidden fields, humans never see them.
        // Report success so the bot does not retry.
        if (f.botcheck) {
            form.reset();
            return showStatus(statusEl, t.success, 'success');
        }

        if (!f.name || !f.email || !f.message) {
            return showStatus(statusEl, t.required, 'error');
        }
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email)) {
            return showStatus(statusEl, t.badEmail, 'error');
        }

        const key = (document.querySelector('meta[name="web3forms-key"]') || {}).content;
        if (!key) {
            console.error('web3forms-key meta tag is missing — cannot submit.');
            return showStatus(statusEl, t.failure, 'error');
        }

        const originalText = submitBtn.textContent;
        submitBtn.textContent = t.sending;
        submitBtn.disabled = true;
        showStatus(statusEl, '', 'clear');

        try {
            const res = await fetch(ENDPOINT, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
                body: JSON.stringify(buildPayload(form, f, key, lang))
            });
            const body = await res.json().catch(() => ({}));

            // Web3Forms can answer 200 with success:false (e.g. rejected key),
            // so status alone is not enough.
            if (res.ok && body.success !== false) {
                trackLead(form, lang);
                form.reset();
                showStatus(statusEl, t.success, 'success');
            } else {
                console.error('Web3Forms rejected the submission:', res.status, body);
                showStatus(statusEl, t.failure, 'error');
            }
        } catch (error) {
            console.error('Form submission error:', error);
            showStatus(statusEl, t.failure, 'error');
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
}

// Fires only after Web3Forms confirms delivery, so the count reflects real
// inquiries rather than clicks on the button. Sent to GA4 directly (gtag) and
// pushed to the dataLayer so a GTM tag can pick it up too — GA4 is not inside
// GTM, so these are not duplicates of each other.
function trackLead(form, lang) {
    var type = form.dataset.formType === 'quotation' ? 'quotation' : 'contact';
    var payload = {
        form_type: type,
        form_language: lang,
        page_path: window.location.pathname
    };

    try {
        if (typeof window.gtag === 'function') {
            window.gtag('event', 'generate_lead', payload);
        }
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push(Object.assign({ event: 'generate_lead' }, payload));
    } catch (e) {
        // Never let analytics break the visitor's confirmation.
        console.error('generate_lead tracking failed:', e);
    }
}

function buildPayload(form, f, key, lang) {
    const type = form.dataset.formType === 'quotation' ? 'quotation' : 'contact';
    const label = FORM_LABEL[lang][type];
    const L = LABELS[lang];

    const payload = {
        access_key: key,
        from_name: 'Iconic Mach Website',
        subject: `[${label}] ${f.subject || f.name}${f.company ? ' — ' + f.company : ''}`,
        replyto: f.email,
        name: f.name,
        email: f.email,
        message: f.message
    };

    // Web3Forms emails every key it receives, so use readable labels and skip blanks.
    const extras = {
        [L.phone]: f.phone,
        [L.company]: f.company,
        [L.product]: f.product,
        [L.form]: label,
        [L.page]: window.location.pathname
    };
    for (const [k, v] of Object.entries(extras)) {
        if (v) payload[k] = v;
    }

    return payload;
}

function showStatus(el, message, kind) {
    if (!el) return;
    if (kind === 'clear') {
        el.hidden = true;
        el.textContent = '';
        return;
    }
    el.hidden = false;
    el.textContent = message;
    el.style.padding = '13px 16px';
    el.style.borderRadius = 'var(--radius-sm)';
    el.style.fontSize = '0.92rem';
    el.style.lineHeight = '1.6';
    if (kind === 'success') {
        el.style.background = 'rgba(74,222,174,0.14)';
        el.style.color = '#0d7a58';
        el.style.border = '1px solid rgba(74,222,174,0.5)';
    } else {
        el.style.background = 'rgba(220,53,69,0.10)';
        el.style.color = '#b02a37';
        el.style.border = '1px solid rgba(220,53,69,0.4)';
    }
}
