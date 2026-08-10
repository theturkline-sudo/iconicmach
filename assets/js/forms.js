// assets/js/forms.js
// Handles every inquiry form on the site (contact + request-quotation, EN + AR).

document.addEventListener('DOMContentLoaded', initForms);

const STRINGS = {
    en: {
        required: 'Please fill in all required fields.',
        badEmail: 'Please enter a valid email address.',
        sending: 'Sending...',
        success: 'Thank you! Your message has been sent. Our team will get back to you within one business day.',
        failure: 'Sorry, something went wrong. Please try again, or reach us on WhatsApp at +20 108 472 717.'
    },
    ar: {
        required: 'يرجى ملء جميع الحقول المطلوبة.',
        badEmail: 'يرجى إدخال بريد إلكتروني صحيح.',
        sending: 'جارٍ الإرسال...',
        success: 'شكراً لك! تم إرسال رسالتك بنجاح. سيتواصل معك فريقنا خلال يوم عمل واحد.',
        failure: 'عذراً، حدث خطأ ما. يرجى المحاولة مرة أخرى أو التواصل معنا عبر واتساب على 717 472 108 20+.'
    }
};

function initForms() {
    document.querySelectorAll('form.inquiry-form').forEach(setupForm);
}

function setupForm(form) {
    const lang = document.documentElement.lang === 'ar' ? 'ar' : 'en';
    const t = STRINGS[lang];
    const statusEl = form.querySelector('.form-status');
    const submitBtn = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const data = Object.fromEntries(new FormData(form).entries());

        if (!data.name || !data.email || !data.message) {
            return showStatus(statusEl, t.required, 'error');
        }
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
            return showStatus(statusEl, t.badEmail, 'error');
        }

        data.form_type = form.dataset.formType || 'contact';
        data.language = lang;
        data.page = window.location.pathname;

        const originalText = submitBtn.textContent;
        submitBtn.textContent = t.sending;
        submitBtn.disabled = true;
        showStatus(statusEl, '', 'clear');

        try {
            const response = await fetch('/api/submit-inquiry', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                form.reset();
                showStatus(statusEl, t.success, 'success');
            } else {
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
