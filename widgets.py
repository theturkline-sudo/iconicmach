"""Floating contact cluster + chat assistant, shared by both generators.

Kept in one module rather than duplicated into generate_en.py and
generate_ar.py so the two languages cannot drift apart. Import it from each
generator and drop `floating_widgets(lang)` into the page template.

The assistant is scripted, not AI-backed: the site is static, so an LLM call
would mean shipping an API key in the page or running a backend. It answers
from a keyword-matched topic list and hands off to WhatsApp otherwise.
"""

import json

PHONE_E164 = "+201068472717"
PHONE_DISPLAY = "+20 10 68472717"
WHATSAPP_URL = "https://wa.me/201068472717"
SALES_EMAIL = "sales@iconicmach.com"

ICONS = {
    "whatsapp": '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>',
    "phone": '<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.02-.24c1.12.37 2.33.57 3.57.57a1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.24.2 2.45.57 3.57a1 1 0 01-.25 1.02l-2.2 2.2z"/></svg>',
    "email": '<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V6a2 2 0 00-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>',
    "chat": '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20 2H4a2 2 0 00-2 2v18l4-4h14a2 2 0 002-2V4a2 2 0 00-2-2zM7 9h10v2H7V9zm0 4h7v2H7v-2zM7 5h10v2H7V5z"/></svg>',
    "send": '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/></svg>',
}

STRINGS = {
    "en": {
        "whatsapp": "Chat on WhatsApp",
        "phone": "Call us",
        "email": "Email us",
        "chat": "Ask a question",
        "close": "Close chat",
        "title": "Iconic Mach Assistant",
        "subtitle": "Quick answers, or reach a person",
        "placeholder": "Type your question...",
        "send": "Send",
        "greeting": "Hello. I can answer common questions about our production lines, conveyors and support. Pick a topic below, or type your question.",
        "human": "Talk to a person",
        "fallback": (
            "I do not have a good answer for that one. Our engineers can help "
            'directly &mdash; <a href="' + WHATSAPP_URL + '" target="_blank" rel="noopener">message us on WhatsApp</a> '
            'or <a href="mailto:' + SALES_EMAIL + '">email ' + SALES_EMAIL + "</a>."
        ),
    },
    "ar": {
        "whatsapp": "تواصل عبر واتساب",
        "phone": "اتصل بنا",
        "email": "راسلنا بالبريد",
        "chat": "اسأل سؤالاً",
        "close": "إغلاق المحادثة",
        "title": "مساعد آيكونيك ماشين",
        "subtitle": "إجابات سريعة، أو تواصل مع فريقنا",
        "placeholder": "اكتب سؤالك...",
        "send": "إرسال",
        "greeting": "مرحباً. يمكنني الإجابة عن الأسئلة الشائعة حول خطوط الإنتاج والسيور والدعم الفني. اختر موضوعاً بالأسفل أو اكتب سؤالك.",
        "human": "التحدث مع أحد الموظفين",
        "fallback": (
            "ليس لديّ إجابة دقيقة عن هذا السؤال. يمكن لمهندسينا مساعدتك مباشرةً &mdash; "
            '<a href="' + WHATSAPP_URL + '" target="_blank" rel="noopener">راسلنا على واتساب</a> '
            'أو <a href="mailto:' + SALES_EMAIL + '">أرسل بريداً إلى ' + SALES_EMAIL + "</a>."
        ),
    },
}

# Answers mirror the FAQ pages so the assistant never contradicts the site.
TOPICS = {
    "en": [
        {
            "label": "What do you make?",
            "keywords": ["product", "make", "manufacture", "offer", "build", "line", "conveyor", "machine"],
            "answer": (
                "We design, manufacture and install:<br>"
                '&bull; <a href="production-lines">Production lines</a> for food &amp; beverage, packaging and assembly<br>'
                '&bull; <a href="conveyor-systems">Conveyor systems</a> for material handling<br>'
                '&bull; <a href="spare-parts">Spare parts</a> and automation upgrades<br><br>'
                "Every system is custom-engineered to your space and throughput targets."
            ),
        },
        {
            "label": "Get a quotation",
            "keywords": ["quote", "quotation", "price", "cost", "how much", "budget", "estimate"],
            "answer": (
                "Pricing depends on throughput, product type and site layout, so every quote is prepared individually. "
                'Send us your requirements via the <a href="request-quotation">quotation form</a> and our sales team replies '
                "within one business day."
            ),
        },
        {
            "label": "How long does installation take?",
            "keywords": ["how long", "lead time", "delivery", "timeline", "install", "duration", "when"],
            "answer": (
                "From design approval to commissioning:<br>"
                "&bull; Standard conveyor system: 2&ndash;4 weeks<br>"
                "&bull; Full production line: 6&ndash;12 weeks<br><br>"
                "Complex or custom projects are scheduled after a site visit."
            ),
        },
        {
            "label": "Technical support",
            "keywords": ["support", "maintenance", "repair", "breakdown", "service", "amc", "help", "fault"],
            "answer": (
                "We run 24/7 support: remote diagnostics and PLC troubleshooting, on-site technician dispatch, "
                "emergency spare parts, and Annual Maintenance Contracts.<br><br>"
                'Urgent issue? <a href="' + WHATSAPP_URL + '" target="_blank" rel="noopener">Message us on WhatsApp</a> '
                'or see <a href="technical-support">technical support</a>.'
            ),
        },
        {
            "label": "Can you upgrade my existing line?",
            "keywords": ["upgrade", "existing", "retrofit", "old", "modernise", "modernize", "automate"],
            "answer": (
                "Yes &mdash; that is often the most cost-effective route. Much installed equipment is mechanically sound "
                "but electrically dated, so we fit modern PLCs, sensors and drives to your existing frames rather than "
                "replacing the whole line."
            ),
        },
        {
            "label": "Which industries do you serve?",
            "keywords": ["industry", "industries", "sector", "food", "pharma", "beverage", "who"],
            "answer": (
                "Food &amp; beverage, FMCG, pharmaceuticals, automotive, warehousing and general manufacturing. "
                'More detail on the <a href="industries">industries page</a>.'
            ),
        },
        {
            "label": "Where are you located?",
            "keywords": ["where", "location", "address", "visit", "factory", "office", "egypt", "cairo"],
            "answer": (
                "Al Hashemia Mall, Tower (W), 3rd Floor, behind the Vodafone branch, 10th of Ramadan, Al Sharqiya, Egypt. We serve all of Egypt and the GCC, "
                'and we do site visits before quoting. <a href="contact">Contact details and map</a>.'
            ),
        },
    ],
    "ar": [
        {
            "label": "ماذا تصنعون؟",
            "keywords": ["منتج", "منتجات", "تصنيع", "تصنعون", "خط", "خطوط", "سيور", "ماكينات", "ماكينة"],
            "answer": (
                "نقوم بتصميم وتصنيع وتركيب:<br>"
                '&bull; <a href="production-lines">خطوط الإنتاج</a> للأغذية والمشروبات والتعبئة والتجميع<br>'
                '&bull; <a href="conveyor-systems">أنظمة السيور الناقلة</a> لمناولة المواد<br>'
                '&bull; <a href="spare-parts">قطع الغيار</a> وترقيات الأتمتة<br><br>'
                "كل نظام مصمم خصيصاً لمساحتك ومعدلات الإنتاج المطلوبة."
            ),
        },
        {
            "label": "أريد عرض سعر",
            "keywords": ["سعر", "أسعار", "تكلفة", "عرض", "تسعير", "كام", "ميزانية"],
            "answer": (
                "يعتمد السعر على معدل الإنتاج ونوع المنتج وتخطيط الموقع، لذلك يُعد كل عرض سعر بشكل منفصل. "
                'أرسل متطلباتك عبر <a href="request-quotation">نموذج طلب عرض السعر</a> وسيرد فريق المبيعات خلال يوم عمل واحد.'
            ),
        },
        {
            "label": "كم يستغرق التركيب؟",
            "keywords": ["مدة", "وقت", "متى", "تركيب", "تسليم", "يستغرق", "كم"],
            "answer": (
                "من اعتماد التصميم حتى التشغيل:<br>"
                "&bull; نظام سيور قياسي: 2&ndash;4 أسابيع<br>"
                "&bull; خط إنتاج متكامل: 6&ndash;12 أسبوعاً<br><br>"
                "أما المشاريع المعقدة أو الخاصة فتُجدول بعد زيارة ميدانية."
            ),
        },
        {
            "label": "الدعم الفني",
            "keywords": ["دعم", "صيانة", "عطل", "إصلاح", "خدمة", "مساعدة", "طوارئ"],
            "answer": (
                "لدينا دعم على مدار الساعة: تشخيص عن بُعد ومعالجة أعطال PLC، وإيفاد فنيين إلى الموقع، "
                "وتوريد قطع غيار طارئة، وعقود صيانة سنوية.<br><br>"
                'عطل عاجل؟ <a href="' + WHATSAPP_URL + '" target="_blank" rel="noopener">راسلنا على واتساب</a> '
                'أو اطّلع على <a href="technical-support">الدعم الفني</a>.'
            ),
        },
        {
            "label": "هل يمكن تطوير خط قائم؟",
            "keywords": ["تطوير", "ترقية", "قائم", "قديم", "تحديث", "أتمتة"],
            "answer": (
                "نعم &mdash; وغالباً ما يكون الخيار الأجدى اقتصادياً. كثير من المعدات القائمة سليم ميكانيكياً لكنه "
                "متقادم كهربائياً، لذا نركّب وحدات PLC وحساسات ومشغّلات حديثة على الهياكل الموجودة بدل استبدال الخط بالكامل."
            ),
        },
        {
            "label": "ما القطاعات التي تخدمونها؟",
            "keywords": ["قطاع", "قطاعات", "صناعات", "أغذية", "دوائية", "مشروبات", "مجالات"],
            "answer": (
                "الأغذية والمشروبات، والسلع الاستهلاكية، والصناعات الدوائية، والسيارات، والمستودعات، والتصنيع العام. "
                'التفاصيل في <a href="industries">صفحة القطاعات</a>.'
            ),
        },
        {
            "label": "أين مقركم؟",
            "keywords": ["أين", "مكان", "عنوان", "موقع", "زيارة", "مصر", "المصنع"],
            "answer": (
                "مول الهاشمية، برج (و)، الدور الثالث، خلف فرع فودافون، العاشر من رمضان، الشرقية، مصر. نخدم جميع أنحاء مصر ودول الخليج، "
                'ونقوم بزيارات ميدانية قبل إعداد عرض السعر. <a href="contact">بيانات التواصل والخريطة</a>.'
            ),
        },
    ],
}


def chat_data(lang):
    s = STRINGS[lang]
    return json.dumps(
        {
            "greeting": s["greeting"],
            "fallback": s["fallback"],
            "humanLabel": s["human"],
            "whatsapp": WHATSAPP_URL,
            "topics": [
                {"label": t["label"], "keywords": t["keywords"], "answer": t["answer"]}
                for t in TOPICS[lang]
            ],
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )


def floating_widgets(lang):
    """Floating contact buttons + chat panel, injected on every page."""
    s = STRINGS[lang]
    return '''
    <div class="floating-actions">
        <a class="fab-email" href="mailto:{email}" data-label="{email_label}" aria-label="{email_label}">{email_icon}</a>
        <a class="fab-phone" href="tel:{phone}" data-label="{phone_label}" aria-label="{phone_label}">{phone_icon}</a>
        <a class="fab-whatsapp" href="{whatsapp}" target="_blank" rel="noopener" data-label="{wa_label}" aria-label="{wa_label}">{wa_icon}</a>
        <button type="button" class="fab-chat" id="chat-toggle" data-label="{chat_label}" aria-label="{chat_label}" aria-expanded="false" aria-controls="chat-panel">{chat_icon}</button>
    </div>

    <div class="chat-panel" id="chat-panel" data-open="false" role="dialog" aria-label="{title}">
        <div class="chat-header">
            {chat_icon}
            <div>
                <h3>{title}</h3>
                <p>{subtitle}</p>
            </div>
            <button type="button" class="chat-close" aria-label="{close}">&times;</button>
        </div>
        <div class="chat-log" role="log" aria-live="polite"></div>
        <div class="chat-replies"></div>
        <form class="chat-form" autocomplete="off">
            <input type="text" placeholder="{placeholder}" aria-label="{placeholder}">
            <button type="submit" aria-label="{send}">{send_icon}</button>
        </form>
    </div>

    <script type="application/json" id="chat-data">{data}</script>'''.format(
        email=SALES_EMAIL,
        phone=PHONE_E164,
        whatsapp=WHATSAPP_URL,
        email_label=s["email"],
        phone_label=s["phone"],
        wa_label=s["whatsapp"],
        chat_label=s["chat"],
        title=s["title"],
        subtitle=s["subtitle"],
        placeholder=s["placeholder"],
        send=s["send"],
        close=s["close"],
        email_icon=ICONS["email"],
        phone_icon=ICONS["phone"],
        wa_icon=ICONS["whatsapp"],
        chat_icon=ICONS["chat"],
        send_icon=ICONS["send"],
        data=chat_data(lang),
    )


# --- Homepage FAQ -----------------------------------------------------------

HOME_FAQ = {
    "en": {
        "heading": "Frequently Asked Questions",
        "intro": "The questions our clients ask most. See the full list on our FAQ page.",
        "more": "View all FAQs",
        "items": [
            ("Do you offer custom-designed systems?",
             "Yes. Every system we build is custom-engineered to your specific space, throughput targets and product requirements. We start with a site visit and a detailed consultation."),
            ("How long does a typical installation take?",
             "A standard conveyor system takes 2–4 weeks from design approval to commissioning. Full production lines typically take 6–12 weeks, depending on complexity."),
            ("Can you upgrade my existing equipment?",
             "Yes. We specialise in automation upgrades — integrating modern PLCs, sensors and control systems into your existing lines without requiring a full replacement."),
            ("Do you provide after-sales maintenance?",
             "Absolutely. We offer Annual Maintenance Contracts covering scheduled inspections, preventive part replacement and priority emergency response."),
            ("Which industries do you serve?",
             "Food &amp; beverage, FMCG, pharmaceuticals, automotive, warehousing and general manufacturing. Any production environment can benefit from our solutions."),
        ],
    },
    "ar": {
        "heading": "الأسئلة الشائعة",
        "intro": "أكثر الأسئلة التي يطرحها عملاؤنا. اطّلع على القائمة الكاملة في صفحة الأسئلة الشائعة.",
        "more": "عرض كل الأسئلة",
        "items": [
            ("هل تقدمون أنظمة مصممة خصيصاً؟",
             "نعم. كل نظام ننفذه مصمم هندسياً ليناسب مساحتك ومعدلات الإنتاج المستهدفة ومتطلبات منتجك. نبدأ بزيارة ميدانية واستشارة تفصيلية."),
            ("كم يستغرق التركيب عادةً؟",
             "يستغرق نظام السيور القياسي من 2 إلى 4 أسابيع من اعتماد التصميم حتى التشغيل. أما خطوط الإنتاج المتكاملة فتستغرق عادةً من 6 إلى 12 أسبوعاً حسب درجة التعقيد."),
            ("هل يمكنكم تطوير معداتي الحالية؟",
             "نعم. نحن متخصصون في ترقيات الأتمتة — بدمج وحدات PLC والحساسات وأنظمة التحكم الحديثة في خطوطك القائمة دون الحاجة إلى استبدالها بالكامل."),
            ("هل توفرون صيانة ما بعد البيع؟",
             "بالتأكيد. نوفر عقود صيانة سنوية تشمل الفحوصات الدورية واستبدال القطع الوقائي والاستجابة الطارئة ذات الأولوية."),
            ("ما القطاعات التي تخدمونها؟",
             "الأغذية والمشروبات، والسلع الاستهلاكية، والصناعات الدوائية، والسيارات، والمستودعات، والتصنيع العام. أي بيئة إنتاج يمكن أن تستفيد من حلولنا."),
        ],
    },
}


def home_faq_section(lang):
    """FAQ block for the homepage. Markup matches the existing faq.html."""
    d = HOME_FAQ[lang]
    rows = "".join(
        '''
                <details class="card bg-main" style="padding:24px; cursor:pointer;">
                    <summary style="font-weight:600; font-size:1rem; list-style:none; display:flex; justify-content:space-between; gap:16px;">{q} <span>&#43;</span></summary>
                    <p style="margin-top:16px; line-height:1.8; color:var(--text-muted);">{a}</p>
                </details>'''.format(q=q, a=a)
        for q, a in d["items"]
    )
    return '''
    <section class="section bg-alt">
        <div class="container" style="max-width:820px;">
            <div style="text-align:center; margin-bottom:40px;">
                <h2 class="text-primary" style="font-size:2rem; margin-bottom:12px;">{heading}</h2>
                <p class="text-muted" style="line-height:1.8;">{intro}</p>
            </div>
            <div style="display:flex; flex-direction:column; gap:16px;">{rows}
            </div>
            <p style="text-align:center; margin-top:36px;">
                <a href="faq" class="btn btn-primary" style="padding:13px 30px; text-decoration:none;">{more}</a>
            </p>
        </div>
    </section>'''.format(heading=d["heading"], intro=d["intro"], more=d["more"], rows=rows)


def faq_schema_nodes(lang, page_url):
    """FAQPage JSON-LD so the questions can surface as rich results."""
    import re

    def plain(text):
        return re.sub(r"<[^>]+>", "", text).replace("&amp;", "&").strip()

    return {
        "@type": "FAQPage",
        "@id": page_url + "#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": plain(q),
                "acceptedAnswer": {"@type": "Answer", "text": plain(a)},
            }
            for q, a in HOME_FAQ[lang]["items"]
        ],
    }


# --- Google Tag Manager -----------------------------------------------------
#
# GA4 stays hardcoded in the generators and is deliberately NOT added as a tag
# inside GTM: having both would double-count every pageview. GTM is here for
# future marketing tags (Ads conversions, Meta Pixel, LinkedIn Insight).
#
# The strict CSP in /_headers already allows googletagmanager.com, so the
# container loads. Any THIRD-PARTY tag added in GTM will be blocked until its
# host is added to script-src / connect-src there.

GTM_CONTAINER_ID = "GTM-KL9S52KM"


def gtm_head():
    """Container loader, placed as high in <head> as practical."""
    if not GTM_CONTAINER_ID:
        return ""
    return (
        "<!-- Google Tag Manager -->\n"
        "    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n"
        "    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
        "    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n"
        "    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
        "    })(window,document,'script','dataLayer','" + GTM_CONTAINER_ID + "');</script>\n"
        "    <!-- End Google Tag Manager -->"
    )


def gtm_body():
    """noscript fallback, immediately after <body>."""
    if not GTM_CONTAINER_ID:
        return ""
    return (
        "<!-- Google Tag Manager (noscript) -->\n"
        '    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id='
        + GTM_CONTAINER_ID + '"\n'
        '    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'
        "    <!-- End Google Tag Manager (noscript) -->"
    )


# --- Site tree --------------------------------------------------------------
#
# URLs are flat (/en/contact, not /en/company/contact), so breadcrumbs stay
# honest: Home > Page, and Home > Blog > Article for the articles. Claiming a
# deeper hierarchy than the URLs actually have would be misleading markup.
#
# SECTIONS is the grouping used by the human-readable sitemap page only.

SECTIONS = {
    "en": [
        ("Products & Services", [
            ("production-lines", "Production Lines"),
            ("conveyor-systems", "Conveyor Systems"),
            ("spare-parts", "Spare Parts"),
            ("services", "Services"),
            ("technical-support", "Technical Support"),
            ("request-quotation", "Request a Quotation"),
        ]),
        ("Company", [
            ("about", "About Us"),
            ("industries", "Industries We Serve"),
            ("projects", "Projects"),
            ("contact", "Contact Us"),
        ]),
        ("Resources", [
            ("blog", "Blog"),
            ("blog-industry-4-0-egypt", "Industry 4.0 for Egyptian Manufacturers"),
            ("blog-conveyor-upgrade-signs", "5 Signs Your Conveyor Needs an Upgrade"),
            ("blog-lean-production-line-waste", "Reducing Waste with Lean Line Design"),
            ("faq", "Frequently Asked Questions"),
        ]),
        ("Legal", [
            ("privacy-policy", "Privacy Policy"),
            ("terms", "Terms & Conditions"),
        ]),
    ],
    "ar": [
        ("المنتجات والخدمات", [
            ("production-lines", "خطوط الإنتاج"),
            ("conveyor-systems", "أنظمة السيور الناقلة"),
            ("spare-parts", "قطع الغيار"),
            ("services", "خدماتنا"),
            ("technical-support", "الدعم الفني"),
            ("request-quotation", "طلب عرض سعر"),
        ]),
        ("الشركة", [
            ("about", "من نحن"),
            ("industries", "القطاعات التي نخدمها"),
            ("projects", "المشاريع"),
            ("contact", "اتصل بنا"),
        ]),
        ("مصادر", [
            ("blog", "المدونة"),
            ("blog-industry-4-0-egypt", "الصناعة 4.0 للمصنّعين في مصر"),
            ("blog-conveyor-upgrade-signs", "٥ علامات تدل على حاجة السيور للتطوير"),
            ("blog-lean-production-line-waste", "تقليل الهدر بالتصميم الرشيق"),
            ("faq", "الأسئلة الشائعة"),
        ]),
        ("قانوني", [
            ("privacy-policy", "سياسة الخصوصية"),
            ("terms", "الشروط والأحكام"),
        ]),
    ],
}

SITEMAP_STRINGS = {
    "en": {
        "title": "Site Map",
        "desc": "Every page on iconicmach.com, grouped by section.",
        "home": "Home",
        "blog": "Blog",
    },
    "ar": {
        "title": "خريطة الموقع",
        "desc": "جميع صفحات iconicmach.com مرتبة حسب الأقسام.",
        "home": "الرئيسية",
        "blog": "المدونة",
    },
}


def page_title_for(lang, slug):
    for _section, items in SECTIONS[lang]:
        for s, label in items:
            if s == slug:
                return label
    return None


def breadcrumb_node(lang, filename, domain, page_title):
    """BreadcrumbList JSON-LD. Returns None for the homepage."""
    if filename == "index.html":
        return None

    slug = filename[: -len(".html")]
    base = "{}/{}/".format(domain, lang)
    s = SITEMAP_STRINGS[lang]

    items = [{"@type": "ListItem", "position": 1, "name": s["home"], "item": base}]

    # Articles genuinely sit under the blog listing.
    if slug.startswith("blog-"):
        items.append({"@type": "ListItem", "position": 2, "name": s["blog"], "item": base + "blog"})
        items.append({"@type": "ListItem", "position": 3, "name": page_title, "item": base + slug})
    else:
        items.append({"@type": "ListItem", "position": 2, "name": page_title, "item": base + slug})

    return {
        "@type": "BreadcrumbList",
        "@id": base + slug + "#breadcrumb",
        "itemListElement": items,
    }


def sitemap_page(lang):
    """Human-readable site tree."""
    s = SITEMAP_STRINGS[lang]
    blocks = []
    for section, items in SECTIONS[lang]:
        links = "".join(
            '\n                    <li style="margin-bottom:10px;"><a href="{slug}" style="color:var(--primary-blue); text-decoration:none; font-weight:500;">{label}</a></li>'.format(
                slug=slug, label=label
            )
            for slug, label in items
        )
        blocks.append(
            '''
                <div>
                    <h2 style="font-size:1.15rem; margin-bottom:16px; padding-bottom:10px; border-block-end:2px solid var(--primary-blue);">{section}</h2>
                    <ul style="list-style:none; padding:0;">{links}
                    </ul>
                </div>'''.format(section=section, links=links)
        )

    return '''
    <section id="main-content" class="section">
        <div class="container" style="max-width:900px;">
            <p class="text-muted" style="text-align:center; line-height:1.8; margin-bottom:48px;">{desc}</p>
            <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:40px;">{blocks}
            </div>
        </div>
    </section>'''.format(desc=s["desc"], blocks="".join(blocks))
