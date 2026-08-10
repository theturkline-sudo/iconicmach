// Cloudflare Pages Function — POST /api/submit-inquiry
//
// Required environment variables (Cloudflare dashboard → Settings → Environment variables):
//   RESEND_API_KEY  — API key from https://resend.com  (free tier: 100 emails/day)
//   INQUIRY_TO      — optional, defaults to sales@iconicmach.com
//   INQUIRY_FROM    — optional, defaults to website@iconicmach.com (domain must be verified in Resend)

const MAX_LEN = {
  name: 120,
  email: 160,
  phone: 40,
  company: 160,
  subject: 200,
  product: 80,
  message: 4000
};

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    const body = await request.json();

    // Honeypot — bots fill hidden fields, humans never see them.
    if (body.company_website) {
      return json({ success: true, message: 'Inquiry received' }, 200);
    }

    const name = clean(body.name, MAX_LEN.name);
    const email = clean(body.email, MAX_LEN.email);
    const message = clean(body.message, MAX_LEN.message);

    if (!name || !email || !message) {
      return json({ error: 'Missing required fields' }, 400);
    }
    if (!EMAIL_RE.test(email)) {
      return json({ error: 'Invalid email address' }, 400);
    }

    const inquiry = {
      name,
      email,
      message,
      phone: clean(body.phone, MAX_LEN.phone),
      company: clean(body.company, MAX_LEN.company),
      subject: clean(body.subject, MAX_LEN.subject),
      product: clean(body.product, MAX_LEN.product),
      formType: body.form_type === 'quotation' ? 'quotation' : 'contact',
      language: body.language === 'ar' ? 'ar' : 'en',
      page: clean(body.page, 200),
      country: request.headers.get('CF-IPCountry') || '',
      receivedAt: new Date().toISOString()
    };

    if (!env.RESEND_API_KEY) {
      // Not configured yet — log so the submission is at least visible in Worker logs
      // instead of being silently dropped, and surface the failure to the visitor.
      console.error('RESEND_API_KEY is not set; inquiry not delivered:', JSON.stringify(inquiry));
      return json({ error: 'Email delivery is not configured' }, 500);
    }

    const sent = await sendEmail(env, inquiry);
    if (!sent.ok) {
      console.error('Resend API error:', sent.status, sent.detail);
      return json({ error: 'Failed to deliver inquiry' }, 502);
    }

    return json({ success: true, message: 'Inquiry received' }, 200);
  } catch (error) {
    console.error('submit-inquiry error:', error && error.message);
    return json({ error: 'Invalid request' }, 400);
  }
}

async function sendEmail(env, i) {
  const to = env.INQUIRY_TO || 'sales@iconicmach.com';
  const from = env.INQUIRY_FROM || 'website@iconicmach.com';
  const label = i.formType === 'quotation' ? 'Quotation Request' : 'Contact Inquiry';

  const rows = [
    ['Name', i.name],
    ['Email', i.email],
    ['Phone', i.phone],
    ['Company', i.company],
    ['Subject', i.subject],
    ['Product / Service', i.product],
    ['Language', i.language.toUpperCase()],
    ['Page', i.page],
    ['Country', i.country],
    ['Received', i.receivedAt]
  ].filter(([, v]) => v);

  const html = `
    <div style="font-family:Arial,Helvetica,sans-serif;max-width:640px">
      <h2 style="color:#0a3150;margin:0 0 16px">New ${label} — iconicmach.com</h2>
      <table cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;font-size:14px">
        ${rows.map(([k, v]) => `<tr><td style="background:#f4f7fb;font-weight:600;width:170px">${esc(k)}</td><td>${esc(v)}</td></tr>`).join('')}
      </table>
      <h3 style="color:#0a3150;margin:24px 0 8px">Message</h3>
      <p style="white-space:pre-wrap;line-height:1.7;font-size:14px">${esc(i.message)}</p>
    </div>`;

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      from: `Iconic Mach Website <${from}>`,
      to: [to],
      reply_to: i.email,
      subject: `[${label}] ${i.subject || i.name}${i.company ? ' — ' + i.company : ''}`,
      html
    })
  });

  if (res.ok) return { ok: true };
  return { ok: false, status: res.status, detail: await res.text() };
}

function clean(value, max) {
  if (typeof value !== 'string') return '';
  return value.trim().slice(0, max);
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}

function json(payload, status) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });
}
