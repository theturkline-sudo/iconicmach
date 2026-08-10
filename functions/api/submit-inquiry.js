// Cloudflare Pages Function — POST /api/submit-inquiry
//
// Delivers website inquiries to sales@iconicmach.com via Web3Forms.
// Chosen over SMTP/Resend because it needs no verified sending domain and no
// SMTP credentials — Web3Forms sends from its own infrastructure and delivers
// to the inbox that owns the access key.
//
// Environment variable (Cloudflare dashboard → Pages project → Settings →
// Environment variables), required in both Production and Preview:
//
//   WEB3FORMS_ACCESS_KEY — access key issued to sales@iconicmach.com
//                          (get one at https://web3forms.com — the key is
//                          public by design, but we keep it server-side so
//                          bots can't scrape it out of the page HTML)
//
// This runs as a proxy rather than posting to Web3Forms from the browser so
// that validation, length caps and the honeypot are enforced server-side.

const WEB3FORMS_ENDPOINT = 'https://api.web3forms.com/submit';

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
    // Return 200 so the bot believes it succeeded and does not retry.
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

    if (!env.WEB3FORMS_ACCESS_KEY) {
      // Not configured yet — log the submission so it is at least recoverable
      // from Worker logs instead of silently vanishing, and tell the visitor.
      console.error(
        'WEB3FORMS_ACCESS_KEY is not set; inquiry not delivered:',
        JSON.stringify(inquiry)
      );
      return json({ error: 'Email delivery is not configured' }, 500);
    }

    const sent = await deliver(env, inquiry);
    if (!sent.ok) {
      console.error('Web3Forms delivery failed:', sent.status, sent.detail);
      return json({ error: 'Failed to deliver inquiry' }, 502);
    }

    return json({ success: true, message: 'Inquiry received' }, 200);
  } catch (error) {
    console.error('submit-inquiry error:', error && error.message);
    return json({ error: 'Invalid request' }, 400);
  }
}

async function deliver(env, i) {
  const label = i.formType === 'quotation' ? 'Quotation Request' : 'Contact Inquiry';

  // Web3Forms emails every key it receives, so send readable labels rather
  // than raw field names, and omit anything the visitor left blank.
  const payload = {
    access_key: env.WEB3FORMS_ACCESS_KEY,
    from_name: 'Iconic Mach Website',
    subject: `[${label}] ${i.subject || i.name}${i.company ? ' — ' + i.company : ''}`,
    replyto: i.email,

    name: i.name,
    email: i.email,
    message: i.message
  };

  const optional = {
    Phone: i.phone,
    Company: i.company,
    'Product / Service': i.product,
    'Form': label,
    'Language': i.language.toUpperCase(),
    'Submitted from': i.page,
    'Visitor country': i.country,
    'Received (UTC)': i.receivedAt
  };
  for (const [key, value] of Object.entries(optional)) {
    if (value) payload[key] = value;
  }

  let res;
  try {
    res = await fetch(WEB3FORMS_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json'
      },
      body: JSON.stringify(payload)
    });
  } catch (err) {
    return { ok: false, status: 0, detail: err && err.message };
  }

  const detail = await res.text();
  if (!res.ok) return { ok: false, status: res.status, detail };

  // Web3Forms can answer 200 with {"success": false} on a rejected key.
  try {
    const parsed = JSON.parse(detail);
    if (parsed.success === false) {
      return { ok: false, status: res.status, detail };
    }
  } catch {
    // Non-JSON 200 — treat as delivered rather than failing a real send.
  }

  return { ok: true };
}

function clean(value, max) {
  if (typeof value !== 'string') return '';
  return value.trim().slice(0, max);
}

function json(payload, status) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });
}
