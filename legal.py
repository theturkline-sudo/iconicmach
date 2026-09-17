# -*- coding: utf-8 -*-
"""Privacy policy and terms & conditions, shared by both generators.

Replaces the 85- and 96-word placeholders that shipped before the site did
anything. Written to what the site actually does now, which anyone reading a
privacy policy is entitled to know:

  - contact / quotation forms are relayed through Web3Forms (a third party)
  - Google Analytics 4 with IP anonymisation, plus an empty Tag Manager container
  - Cloudflare hosting, CDN and its cookieless Web Analytics beacon
  - Google Maps embed and Google Fonts, which contact Google when a page loads
  - a chat assistant that runs entirely in the browser and sends nothing
  - WhatsApp / phone / email buttons that leave the site

Commitments carried over from the old pages, because visitors may already be
relying on them: 30-day quotation validity, 12-month warranty from
commissioning, drawings remain ours unless transferred in writing, data never
sold.

Kept as data + a small renderer so the two languages share one structure.
"""

import re

COMPANY_EN = "Iconic Mach Engineering"
COMPANY_AR = "آيكونيك ماشين الهندسية"
ADDRESS_EN = ("Al Hashemia Mall, Tower (W), 3rd Floor, behind the Vodafone branch, "
              "10th of Ramadan City, Al Sharqiya, Egypt")
ADDRESS_AR = "مول الهاشمية، برج (و)، الدور الثالث، خلف فرع فودافون، العاشر من رمضان، الشرقية، مصر"
EMAIL = "sales@iconicmach.com"
PHONE = "+20 10 68472717"
UPDATED_EN = "17 September 2026"
UPDATED_AR = "١٧ سبتمبر ٢٠٢٦"

# --------------------------------------------------------------------------
# Privacy policy
# --------------------------------------------------------------------------

PRIVACY = {
    "en": {
        "intro": (
            "This policy explains what information iconicmach.com collects, why, who it is shared "
            "with, and the rights you have over it. It is written for the site as it actually "
            "operates, and it will be updated when the site changes."
        ),
        "sections": [
            ("Who we are", [
                "{co} operates this website. We design, manufacture and install production lines and "
                "conveyor systems for industrial clients in Egypt and the GCC.",
                "Address: {addr}",
                "Email: {email} · Phone: {phone}",
            ]),
            ("What we collect, and how", [
                "<strong>Contact and quotation forms.</strong> When you submit a form we receive the "
                "details you type: name, email address, phone number, company name, the product or "
                "service you are asking about, and your message. The form also records which page it "
                "was sent from. Submissions are relayed to our inbox by Web3Forms, a third-party form "
                "service, which additionally logs the IP address the submission came from.",
                "<strong>Website analytics.</strong> We use Google Analytics 4 to understand how the "
                "site is used: pages viewed, time on page, approximate location by country or city, "
                "device and browser type, and how you arrived. IP addresses are anonymised before "
                "storage. Google Tag Manager is installed as a container; at the time of writing it "
                "loads no third-party tags.",
                "<strong>Hosting and security.</strong> The site is served through Cloudflare, which "
                "processes connection data such as IP address and request headers to deliver pages and "
                "block abuse, and which runs a cookieless traffic beacon on each page.",
                "<strong>Embedded Google services.</strong> The contact page embeds a Google Map, and "
                "every page loads fonts from Google Fonts. Loading these sends your IP address to "
                "Google, and the Maps embed may set Google cookies.",
                "<strong>The chat assistant.</strong> The question box in the corner of each page runs "
                "entirely inside your browser. It matches your question against a fixed list of topics "
                "and shows a prepared answer. Nothing you type in it is transmitted to us or to anyone "
                "else, and it is not stored.",
                "<strong>What we do not collect.</strong> The site has no user accounts, takes no "
                "payments, and does not sell products online. We do not collect data about children "
                "and the site is not directed at anyone under 18.",
            ]),
            ("Why we use it", [
                "- To answer your enquiry and, where you ask for one, to prepare a quotation. This is "
                "the reason the forms exist.",
                "- To understand which pages and articles are useful, so we can improve the site. "
                "Analytics is used in aggregate; we do not try to identify individual visitors.",
                "- To keep the site secure and available.",
                "- To send you information about our products and services, but <strong>only if you "
                "have asked for it</strong>. Submitting an enquiry does not sign you up to anything.",
                "We do not sell your information, and we do not share it with anyone for their own "
                "marketing.",
            ]),
            ("Legal basis under Egyptian law", [
                "We process personal data in accordance with Egypt's Personal Data Protection Law "
                "No. 151 of 2020. Our bases are: <strong>your consent</strong>, given when you submit "
                "a form or ask to receive updates; <strong>steps toward a contract</strong>, when we "
                "prepare a quotation you requested; and our <strong>legitimate interest</strong> in "
                "keeping the site secure and understanding how it is used, which we balance against "
                "your interests by anonymising analytics data.",
                "You may withdraw consent at any time by contacting us. Doing so does not affect "
                "processing that already took place.",
            ]),
            ("Who we share it with", [
                "The following services process data on our behalf so the site can work. We choose "
                "them for what they do and we do not permit them to use your data for their own "
                "purposes:",
                "- <strong>Web3Forms</strong> — relays contact and quotation forms to our email.",
                "- <strong>Google</strong> — Analytics 4, Tag Manager, the Maps embed and Fonts.",
                "- <strong>Cloudflare</strong> — hosting, content delivery, security and traffic "
                "statistics.",
                "When you tap the WhatsApp, phone or email buttons, you leave this site and continue "
                "on WhatsApp (Meta), your phone dialler or your email client. Those services apply "
                "their own privacy terms.",
                "Some of these providers store data outside Egypt, including in the European Union "
                "and the United States. Each is bound by its own published data-protection "
                "commitments.",
                "We will disclose information if the law requires it, or to protect our rights or "
                "someone's safety.",
            ]),
            ("How long we keep it", [
                "- <strong>Enquiries and quotation requests:</strong> for as long as we are in "
                "contact about the project, and up to three years after our last exchange so we can "
                "refer back to it if you return. Earlier on request.",
                "- <strong>Analytics data:</strong> held by Google Analytics under its default "
                "retention settings for event-level data. Aggregated reports may be kept longer.",
                "- <strong>Security logs:</strong> retained briefly by Cloudflare under its own "
                "policy.",
            ]),
            ("Cookies", [
                "This site sets few cookies, and none for advertising:",
                "- <code>_ga</code>, <code>_ga_*</code> — Google Analytics, to tell returning visits "
                "from new ones. Expire after up to two years.",
                "- <code>__cf_bm</code> and similar — Cloudflare, to distinguish humans from "
                "automated traffic. Short-lived.",
                "- The embedded Google Map may set Google's own cookies when it loads.",
                "A banner asks for your choice on your first visit. Until you accept, Google Analytics runs "
                "without cookies and receives only aggregate, unidentifiable data, and the Google Map on the "
                "contact page is not loaded. Your choice is remembered in your browser; change it at any time "
                "through the <em>Cookie settings</em> link in the footer.",
                "You can also block or delete cookies in your browser settings; the site will still work. "
                "To opt out of Google Analytics across all sites, Google offers a browser add-on at "
                "tools.google.com/dlpage/gaoptout.",
            ]),
            ("Your rights", [
                "Under Law 151 of 2020 you are entitled to:",
                "- Know whether we hold data about you, and receive a copy.",
                "- Have inaccurate data corrected.",
                "- Have your data deleted, unless we must keep it for a legal reason.",
                "- Object to, or ask us to limit, particular uses.",
                "- Withdraw consent you previously gave.",
                "- Complain to the Personal Data Protection Centre in Egypt.",
                "To exercise any of these, email {email}. We will reply within 30 days, and we may "
                "ask you to confirm your identity before releasing or deleting data.",
            ]),
            ("Security", [
                "The site is served over HTTPS only, with security headers that prevent it being "
                "framed by other sites or having its content types guessed. Form submissions travel "
                "encrypted to Web3Forms and on to our mailbox. Only staff who handle enquiries have "
                "access to them.",
                "No system is entirely secure. If a breach affects your information we will tell "
                "you, and the authorities, as the law requires.",
            ]),
            ("Changes to this policy", [
                "We will update this page when the site starts collecting something new or stops "
                "collecting something listed here. The date at the top shows when it was last "
                "changed. Significant changes will be noted on the page for a period after they take "
                "effect.",
            ]),
            ("Contact", [
                "{co}<br>{addr}<br>Email: {email}<br>Phone: {phone}",
            ]),
        ],
    },
    "ar": {
        "intro": (
            "توضح هذه السياسة ما يجمعه موقع iconicmach.com من معلومات، ولماذا، ومع من يشاركها، "
            "وما لك من حقوق عليها. كُتبت لتصف الموقع كما يعمل فعلياً، وستُحدَّث عند تغيّره."
        ),
        "sections": [
            ("من نحن", [
                "تدير شركة {co} هذا الموقع. نصمّم ونصنّع ونركّب خطوط الإنتاج وأنظمة السيور الناقلة "
                "للعملاء الصناعيين في مصر ودول الخليج.",
                "العنوان: {addr}",
                "البريد الإلكتروني: {email} · الهاتف: {phone}",
            ]),
            ("ما نجمعه وكيف", [
                "<strong>نماذج التواصل وطلب عرض السعر.</strong> عند إرسال نموذج نستلم ما تكتبه: "
                "الاسم، والبريد الإلكتروني، ورقم الهاتف، واسم الشركة، والمنتج أو الخدمة محل "
                "الاستفسار، ورسالتك. يسجّل النموذج أيضاً الصفحة التي أُرسل منها. تُحوَّل الطلبات إلى "
                "بريدنا عبر خدمة Web3Forms، وهي خدمة نماذج تابعة لطرف ثالث تسجّل كذلك عنوان IP الذي "
                "أُرسل منه الطلب.",
                "<strong>تحليلات الموقع.</strong> نستخدم Google Analytics 4 لفهم كيفية استخدام "
                "الموقع: الصفحات المعروضة، ومدة البقاء، والموقع التقريبي بالدولة أو المدينة، ونوع "
                "الجهاز والمتصفح، وكيف وصلت إلينا. تُخفى عناوين IP قبل تخزينها. كما نستخدم Google Tag "
                "Manager كحاوية، ولا تحمّل حالياً أي وسوم لأطراف ثالثة.",
                "<strong>الاستضافة والأمان.</strong> يُقدَّم الموقع عبر Cloudflare التي تعالج بيانات "
                "الاتصال مثل عنوان IP وترويسات الطلب لتقديم الصفحات وصدّ الاستخدام المسيء، وتشغّل "
                "أداة قياس زيارات لا تستخدم ملفات تعريف ارتباط.",
                "<strong>خدمات جوجل المضمّنة.</strong> تتضمن صفحة التواصل خريطة جوجل، وتحمّل كل صفحة "
                "خطوطاً من Google Fonts. يرسل تحميلها عنوان IP الخاص بك إلى جوجل، وقد تضع خريطة جوجل "
                "ملفات تعريف ارتباط خاصة بها.",
                "<strong>المساعد الآلي.</strong> صندوق الأسئلة في زاوية الصفحة يعمل بالكامل داخل "
                "متصفحك؛ يطابق سؤالك مع قائمة ثابتة من الموضوعات ويعرض إجابة مُعدّة مسبقاً. لا يُرسل "
                "ما تكتبه فيه إلينا ولا إلى أي جهة أخرى، ولا يُخزَّن.",
                "<strong>ما لا نجمعه.</strong> لا يحتوي الموقع على حسابات مستخدمين، ولا يقبل مدفوعات، "
                "ولا يبيع منتجات عبر الإنترنت. لا نجمع بيانات عن الأطفال، والموقع غير موجَّه لمن هم "
                "دون 18 عاماً.",
            ]),
            ("لماذا نستخدمها", [
                "- للرد على استفسارك، وإعداد عرض سعر إن طلبته. هذا هو سبب وجود النماذج.",
                "- لمعرفة الصفحات والمقالات المفيدة بهدف تحسين الموقع. تُستخدم التحليلات بشكل "
                "مجمّع ولا نحاول تحديد هوية الزوار.",
                "- للحفاظ على أمان الموقع وتوافره.",
                "- لإرسال معلومات عن منتجاتنا وخدماتنا، لكن <strong>فقط إذا طلبت ذلك</strong>. إرسال "
                "استفسار لا يعني الاشتراك في أي شيء.",
                "لا نبيع معلوماتك، ولا نشاركها مع أي جهة لأغراضها التسويقية.",
            ]),
            ("الأساس القانوني وفق القانون المصري", [
                "نعالج البيانات الشخصية وفق قانون حماية البيانات الشخصية المصري رقم 151 لسنة 2020. "
                "وأسسنا في ذلك: <strong>موافقتك</strong> عند إرسال نموذج أو طلب تلقي مستجدات؛ "
                "و<strong>الخطوات التمهيدية للتعاقد</strong> عند إعداد عرض سعر طلبته؛ "
                "و<strong>مصلحتنا المشروعة</strong> في تأمين الموقع وفهم استخدامه، والتي نوازنها مع "
                "مصالحك بإخفاء هوية بيانات التحليلات.",
                "يمكنك سحب موافقتك في أي وقت بالتواصل معنا، دون أن يؤثر ذلك على ما تمت معالجته "
                "قبل السحب.",
            ]),
            ("مع من نشاركها", [
                "تعالج الخدمات التالية البيانات نيابةً عنا ليعمل الموقع. نختارها لما تؤديه، ولا "
                "نسمح لها باستخدام بياناتك لأغراضها الخاصة:",
                "- <strong>Web3Forms</strong> — تحويل نماذج التواصل وطلب عرض السعر إلى بريدنا.",
                "- <strong>Google</strong> — التحليلات، وTag Manager، وخريطة جوجل المضمّنة، والخطوط.",
                "- <strong>Cloudflare</strong> — الاستضافة، وتوزيع المحتوى، والأمان، وإحصاءات الزيارات.",
                "عند الضغط على أزرار واتساب أو الهاتف أو البريد الإلكتروني فإنك تغادر الموقع وتكمل "
                "على واتساب (ميتا) أو تطبيق الاتصال أو البريد لديك، وتسري عليها شروط الخصوصية الخاصة "
                "بكل منها.",
                "يخزّن بعض هؤلاء المزوّدين البيانات خارج مصر، بما في ذلك الاتحاد الأوروبي والولايات "
                "المتحدة، ويلتزم كل منهم بتعهدات حماية البيانات المنشورة لديه.",
                "سنفصح عن المعلومات إذا ألزمنا القانون بذلك، أو لحماية حقوقنا أو سلامة أي شخص.",
            ]),
            ("مدة الاحتفاظ", [
                "- <strong>الاستفسارات وطلبات عروض الأسعار:</strong> طوال فترة التواصل بشأن المشروع، "
                "وحتى ثلاث سنوات بعد آخر مراسلة حتى نتمكن من الرجوع إليها إن عدت إلينا. وأقل من ذلك "
                "عند الطلب.",
                "- <strong>بيانات التحليلات:</strong> تحتفظ بها Google Analytics وفق إعدادات "
                "الاحتفاظ الافتراضية لبيانات الأحداث. وقد تُحفظ التقارير المجمّعة لمدة أطول.",
                "- <strong>سجلات الأمان:</strong> تحتفظ بها Cloudflare لفترة قصيرة وفق سياستها.",
            ]),
            ("ملفات تعريف الارتباط", [
                "يستخدم الموقع عدداً قليلاً من ملفات تعريف الارتباط، ولا شيء منها للإعلانات:",
                "- <code>_ga</code> و<code>_ga_*</code> — من Google Analytics، للتفريق بين الزيارات "
                "الجديدة والعائدة. تنتهي صلاحيتها خلال عامين على الأكثر.",
                "- <code>__cf_bm</code> وما شابهه — من Cloudflare، للتمييز بين البشر والزيارات "
                "الآلية. قصير الأجل.",
                "- قد تضع خريطة جوجل المضمّنة ملفات تعريف ارتباط خاصة بجوجل عند تحميلها.",
                "يطلب شريط في أول زيارة اختيارك. وحتى توافق، يعمل Google Analytics دون ملفات تعريف "
                "ارتباط ولا يتلقى سوى بيانات مجمّعة لا تحدد الهوية، ولا تُحمَّل خريطة جوجل في صفحة التواصل. "
                "يُحفظ اختيارك في متصفحك، ويمكنك تغييره في أي وقت عبر رابط <em>إعدادات ملفات تعريف "
                "الارتباط</em> في أسفل الصفحة.",
                "يمكنك أيضاً حظر ملفات تعريف الارتباط أو حذفها من إعدادات المتصفح وسيظل الموقع يعمل. "
                "ولإيقاف Google Analytics في كل المواقع، توفر جوجل إضافة للمتصفح على "
                "tools.google.com/dlpage/gaoptout.",
            ]),
            ("حقوقك", [
                "بموجب القانون رقم 151 لسنة 2020 يحق لك:",
                "- معرفة ما إذا كنا نحتفظ ببيانات عنك والحصول على نسخة منها.",
                "- تصحيح البيانات غير الدقيقة.",
                "- حذف بياناتك ما لم يلزمنا القانون بالاحتفاظ بها.",
                "- الاعتراض على استخدامات معينة أو طلب تقييدها.",
                "- سحب موافقة سبق أن منحتها.",
                "- تقديم شكوى إلى مركز حماية البيانات الشخصية في مصر.",
                "لممارسة أي من هذه الحقوق راسلنا على {email}. سنرد خلال 30 يوماً، وقد نطلب تأكيد "
                "هويتك قبل الإفصاح عن البيانات أو حذفها.",
            ]),
            ("الأمان", [
                "يُقدَّم الموقع عبر HTTPS فقط، مع ترويسات أمان تمنع تضمينه داخل مواقع أخرى أو تخمين "
                "أنواع محتواه. تنتقل بيانات النماذج مشفّرة إلى Web3Forms ثم إلى بريدنا، ولا يطّلع "
                "عليها إلا الموظفون المعنيون بالرد على الاستفسارات.",
                "لا يوجد نظام آمن بشكل مطلق. إذا أثّر خرق ما على معلوماتك فسنبلغك ونبلغ الجهات "
                "المختصة وفق ما يقتضيه القانون.",
            ]),
            ("التغييرات على هذه السياسة", [
                "سنحدّث هذه الصفحة عندما يبدأ الموقع بجمع شيء جديد أو يتوقف عن جمع شيء مذكور هنا. "
                "يبيّن التاريخ في أعلى الصفحة آخر تعديل، وستُبرز التغييرات الجوهرية على الصفحة لفترة "
                "بعد سريانها.",
            ]),
            ("التواصل", [
                "{co}<br>{addr}<br>البريد الإلكتروني: {email}<br>الهاتف: {phone}",
            ]),
        ],
    },
}

# --------------------------------------------------------------------------
# Terms & conditions
# --------------------------------------------------------------------------

TERMS = {
    "en": {
        "intro": (
            "These terms govern your use of iconicmach.com and set out how our quotations and "
            "projects work. Supply and installation of equipment is always covered by a separate "
            "written contract; where that contract and these terms differ, the contract prevails."
        ),
        "sections": [
            ("Using this website", [
                "By using this site you agree to these terms. The site is provided for information "
                "and to let prospective clients contact us. You may not use it in any way that damages "
                "it, interferes with other visitors, or attempts to gain access to systems behind it, "
                "and you may not use automated tools to submit the forms.",
            ]),
            ("Information on the site", [
                "Product descriptions, capacities, timelines and technical details on this site are "
                "<strong>indicative</strong>. They describe what we typically build and are not an "
                "offer to supply any particular specification. Photographs and videos show past and "
                "representative installations, not necessarily what you will receive.",
                "We try to keep the site accurate and current, but we do not warrant that it is "
                "error-free, and nothing on it should be relied on without confirmation from us in "
                "writing.",
            ]),
            ("Quotations", [
                "- A quotation is valid for <strong>30 days</strong> from its date unless it states "
                "otherwise.",
                "- Prices exclude VAT and any applicable duties unless the quotation says they are "
                "included.",
                "- Prices are subject to change with the cost of materials, components and currency "
                "exchange rates between the quotation and a signed contract.",
                "- Quotations are prepared from the information you give us and are subject to a "
                "site survey and to final agreement of the specification. They do not form a contract "
                "until both parties sign one.",
                "- A quotation request through this site is an enquiry, not an order.",
            ]),
            ("Contracts, delivery and installation", [
                "Each project is governed by a written contract that sets out the specification, "
                "price, payment schedule, delivery and installation terms, and acceptance criteria. "
                "Any timeline given before that contract is signed is an estimate.",
                "Installation and commissioning depend on the site being ready: access, floor "
                "condition, power, water, compressed air and any permits are the client's "
                "responsibility unless the contract says otherwise. Delays caused by site readiness "
                "are not attributable to us.",
            ]),
            ("Warranty", [
                "Systems we manufacture carry a <strong>12-month warranty from the date of "
                "commissioning</strong> against defects in materials and workmanship. During that "
                "period we will repair or, at our option, replace a defective part or assembly.",
                "The warranty does not cover: normal wear and consumables such as belts, bearings, "
                "seals and filters; damage from misuse, overloading, inadequate maintenance or "
                "operation outside the agreed parameters; modifications or repairs not carried out "
                "or authorised by us; damage from power supply faults, water quality or environmental "
                "conditions outside the specification; or third-party equipment integrated into the "
                "line, which carries its manufacturer's warranty.",
                "Warranty on components we source from other manufacturers is passed through on the "
                "terms those manufacturers provide.",
            ]),
            ("Intellectual property", [
                "Engineering drawings, designs, calculations, control programs and documentation we "
                "produce remain our intellectual property unless a contract expressly transfers them "
                "in writing. A client may use them to operate and maintain the equipment we supplied, "
                "but not to have it reproduced by others.",
                "The content of this website — text, images, video and layout — is ours or used with "
                "permission, and may not be reproduced without consent beyond ordinary browsing and "
                "sharing of links.",
            ]),
            ("Blog and technical articles", [
                "Articles on this site are general engineering guidance. They do not account for the "
                "particulars of any individual installation, and they are not a substitute for a "
                "site-specific assessment. Regulatory information in articles describes the position "
                "as we understood it when written; requirements change, and you should confirm them "
                "with the relevant authority before acting.",
            ]),
            ("Third-party services and links", [
                "Buttons and links on this site take you to WhatsApp, social networks, Google Maps and "
                "other services we do not control. We are not responsible for their content, "
                "availability or how they handle your data. Our <a href=\"privacy-policy\">privacy "
                "policy</a> explains which third-party services this site itself relies on.",
            ]),
            ("Liability", [
                "To the extent the law allows, we are not liable for indirect or consequential loss "
                "arising from use of this website, including lost production, lost profit or loss of "
                "data. Liability in respect of supplied equipment is as set out in the relevant "
                "contract. Nothing in these terms excludes liability that cannot be excluded under "
                "Egyptian law.",
            ]),
            ("Governing law", [
                "These terms are governed by the laws of the Arab Republic of Egypt, and the Egyptian "
                "courts have jurisdiction over any dispute arising from them. We would rather resolve "
                "a disagreement directly, and invite you to contact us first.",
            ]),
            ("Changes", [
                "We may revise these terms. The date at the top shows the current version. Changes "
                "apply to use of the website from the date they are published; they do not alter a "
                "contract already signed.",
            ]),
            ("Contact", [
                "{co}<br>{addr}<br>Email: {email}<br>Phone: {phone}",
            ]),
        ],
    },
    "ar": {
        "intro": (
            "تحكم هذه الشروط استخدامك لموقع iconicmach.com وتبيّن كيفية عمل عروض الأسعار "
            "والمشاريع لدينا. يخضع توريد المعدات وتركيبها دائماً لعقد مكتوب منفصل؛ وعند اختلاف "
            "ذلك العقد مع هذه الشروط يُعمل بالعقد."
        ),
        "sections": [
            ("استخدام هذا الموقع", [
                "باستخدامك الموقع فإنك توافق على هذه الشروط. يُقدَّم الموقع للتعريف بخدماتنا "
                "ولتمكين العملاء المحتملين من التواصل معنا. لا يجوز استخدامه بأي طريقة تضر به أو "
                "تعيق زواره الآخرين أو تحاول الوصول إلى الأنظمة خلفه، ولا يجوز استخدام أدوات آلية "
                "لإرسال النماذج.",
            ]),
            ("المعلومات الواردة في الموقع", [
                "أوصاف المنتجات والسعات والجداول الزمنية والتفاصيل الفنية في هذا الموقع "
                "<strong>استرشادية</strong>؛ فهي تصف ما ننفذه عادةً وليست عرضاً لتوريد مواصفة بعينها. "
                "وتُظهر الصور ومقاطع الفيديو تركيبات سابقة أو نموذجية، وليس بالضرورة ما ستحصل عليه.",
                "نحرص على دقة الموقع وتحديثه، لكننا لا نضمن خلوّه من الأخطاء، ولا ينبغي الاعتماد "
                "على أي مما فيه دون تأكيد كتابي منا.",
            ]),
            ("عروض الأسعار", [
                "- يسري عرض السعر لمدة <strong>30 يوماً</strong> من تاريخه ما لم يُذكر فيه خلاف ذلك.",
                "- الأسعار لا تشمل ضريبة القيمة المضافة ولا أي رسوم جمركية إلا إذا نص العرض على "
                "شمولها.",
                "- الأسعار قابلة للتغيير تبعاً لتكلفة الخامات والمكوّنات وأسعار صرف العملات بين "
                "تاريخ العرض وتوقيع العقد.",
                "- تُعد عروض الأسعار بناءً على المعلومات التي تزوّدنا بها، وتخضع لزيارة ميدانية "
                "وللاتفاق النهائي على المواصفات، ولا تشكّل عقداً قبل توقيع الطرفين عليه.",
                "- طلب عرض السعر عبر هذا الموقع استفسار وليس أمر شراء.",
            ]),
            ("العقود والتوريد والتركيب", [
                "يخضع كل مشروع لعقد مكتوب يحدد المواصفات والسعر وجدول الدفع وشروط التوريد "
                "والتركيب ومعايير الاستلام. وأي جدول زمني يُذكر قبل توقيع ذلك العقد هو تقدير فقط.",
                "يعتمد التركيب والتشغيل على جاهزية الموقع: فالوصول وحالة الأرضية والكهرباء والمياه "
                "والهواء المضغوط وأي تراخيص مطلوبة مسؤولية العميل ما لم ينص العقد على غير ذلك. "
                "والتأخير الناتج عن عدم جاهزية الموقع لا يُنسب إلينا.",
            ]),
            ("الضمان", [
                "تتمتع الأنظمة التي نصنّعها بضمان <strong>12 شهراً من تاريخ التشغيل</strong> ضد عيوب "
                "الخامات والصناعة. وخلال هذه المدة نقوم بإصلاح الجزء المعيب أو استبداله وفق تقديرنا.",
                "لا يشمل الضمان: التآكل الطبيعي والمستهلكات كالسيور والمحامل والجوانات والفلاتر؛ "
                "ولا الأضرار الناتجة عن سوء الاستخدام أو التحميل الزائد أو قصور الصيانة أو التشغيل "
                "خارج المعايير المتفق عليها؛ ولا التعديلات أو الإصلاحات التي لم ننفذها أو نعتمدها؛ "
                "ولا الأضرار الناتجة عن أعطال التغذية الكهربائية أو جودة المياه أو الظروف البيئية "
                "خارج المواصفات؛ ولا معدات الأطراف الأخرى المدمجة في الخط، والتي يسري عليها ضمان "
                "مصنّعها.",
                "ويُمرَّر ضمان المكوّنات التي نورّدها من مصنّعين آخرين وفق الشروط التي يقدمها "
                "هؤلاء المصنّعون.",
            ]),
            ("الملكية الفكرية", [
                "تبقى الرسومات الهندسية والتصاميم والحسابات وبرامج التحكم والوثائق التي ننتجها "
                "ملكية فكرية لنا ما لم ينقلها عقد صراحةً وكتابةً. ويجوز للعميل استخدامها لتشغيل "
                "المعدات التي ورّدناها وصيانتها، لا لتصنيعها لدى الغير.",
                "محتوى هذا الموقع من نصوص وصور وفيديو وتصميم مملوك لنا أو مستخدم بإذن، ولا يجوز "
                "إعادة إنتاجه دون موافقة فيما يتجاوز التصفح المعتاد ومشاركة الروابط.",
            ]),
            ("المدونة والمقالات الفنية", [
                "المقالات في هذا الموقع إرشادات هندسية عامة لا تراعي خصوصيات أي تركيب بعينه، وليست "
                "بديلاً عن تقييم ميداني. وتصف المعلومات التنظيمية فيها الوضع كما فهمناه وقت "
                "كتابتها؛ والاشتراطات تتغير، فيجب التأكد منها لدى الجهة المختصة قبل التصرف.",
            ]),
            ("خدمات الأطراف الأخرى والروابط", [
                "تنقلك الأزرار والروابط في هذا الموقع إلى واتساب وشبكات التواصل وخرائط جوجل "
                "وخدمات أخرى لا نتحكم فيها، ولسنا مسؤولين عن محتواها أو توافرها أو كيفية تعاملها "
                "مع بياناتك. وتوضح <a href=\"privacy-policy\">سياسة الخصوصية</a> الخدمات الخارجية "
                "التي يعتمد عليها الموقع نفسه.",
            ]),
            ("المسؤولية", [
                "في الحدود التي يسمح بها القانون، لا نتحمل مسؤولية الخسائر غير المباشرة أو "
                "التبعية الناشئة عن استخدام هذا الموقع، بما فيها فقدان الإنتاج أو الأرباح أو "
                "البيانات. أما المسؤولية عن المعدات المورَّدة فوفق ما يحدده العقد المعني. ولا "
                "يستبعد شيء في هذه الشروط أي مسؤولية لا يجيز القانون المصري استبعادها.",
            ]),
            ("القانون الواجب التطبيق", [
                "تخضع هذه الشروط لقوانين جمهورية مصر العربية، وتختص المحاكم المصرية بأي نزاع "
                "ينشأ عنها. ونفضّل حل أي خلاف مباشرةً، وندعوك إلى التواصل معنا أولاً.",
            ]),
            ("التغييرات", [
                "قد نراجع هذه الشروط. ويبيّن التاريخ في أعلى الصفحة النسخة الحالية. تسري "
                "التغييرات على استخدام الموقع من تاريخ نشرها، ولا تعدّل عقداً وُقّع بالفعل.",
            ]),
            ("التواصل", [
                "{co}<br>{addr}<br>البريد الإلكتروني: {email}<br>الهاتف: {phone}",
            ]),
        ],
    },
}


# --------------------------------------------------------------------------
# Renderer
# --------------------------------------------------------------------------

def _fill(text, lang):
    return text.format(
        co=COMPANY_AR if lang == "ar" else COMPANY_EN,
        addr=ADDRESS_AR if lang == "ar" else ADDRESS_EN,
        email=EMAIL,
        phone=PHONE,
    )


def _render_section(title, paras, lang, index):
    out = ['<h2 id="s{n}" class="text-primary" style="font-size:1.25rem; margin:36px 0 14px;">'
           '<span style="opacity:.55; font-size:.9em;">{n}.</span> {t}</h2>'.format(n=index, t=title)]
    in_list = False
    for p in paras:
        p = _fill(p, lang)
        if p.startswith("- "):
            if not in_list:
                out.append('<ul style="padding-inline-start:22px; line-height:1.85; margin-bottom:14px;">')
                in_list = True
            out.append("    <li style=\"margin-bottom:6px;\">{}</li>".format(p[2:]))
        else:
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append('<p style="line-height:1.85; margin-bottom:14px;">{}</p>'.format(p))
    if in_list:
        out.append("</ul>")
    return "\n                ".join(out)


def _page(spec, lang, updated_label, updated, toc_label):
    sections = spec["sections"]
    toc = "".join(
        '<li><a href="#s{n}" style="color:var(--primary-blue); text-decoration:none;">{t}</a></li>'.format(
            n=i + 1, t=t) for i, (t, _) in enumerate(sections)
    )
    body = "\n                ".join(
        _render_section(t, ps, lang, i + 1) for i, (t, ps) in enumerate(sections)
    )
    return '''
    <section id="main-content" class="section">
        <div class="container" style="max-width:820px;">
            <div class="card bg-main legal-card" style="padding:40px; box-shadow:var(--shadow-sm);">
                <p style="font-size:.85rem; color:var(--text-muted); margin-bottom:18px;">{updated_label}: {updated}</p>
                <p style="line-height:1.85; margin-bottom:28px; font-size:1.05rem;">{intro}</p>
                <nav aria-label="{toc_label}" class="bg-alt legal-toc" style="padding:18px 22px; border-radius:var(--radius-md); margin-bottom:8px;">
                    <strong style="display:block; margin-bottom:10px;">{toc_label}</strong>
                    <ol style="padding-inline-start:20px; line-height:1.9; margin:0;">{toc}</ol>
                </nav>
                {body}
            </div>
        </div>
    </section>'''.format(
        updated_label=updated_label, updated=updated, intro=_fill(spec["intro"], lang),
        toc_label=toc_label, toc=toc, body=body,
    )


def privacy_page(lang):
    if lang == "ar":
        return _page(PRIVACY["ar"], "ar", "آخر تحديث", UPDATED_AR, "المحتويات")
    return _page(PRIVACY["en"], "en", "Last updated", UPDATED_EN, "Contents")


def terms_page(lang):
    if lang == "ar":
        return _page(TERMS["ar"], "ar", "آخر تحديث", UPDATED_AR, "المحتويات")
    return _page(TERMS["en"], "en", "Last updated", UPDATED_EN, "Contents")


def word_count(html):
    return len(re.sub(r"<[^>]+>", " ", html).split())
