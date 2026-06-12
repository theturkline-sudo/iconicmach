import os

domain = "https://iconicmach.com"

page_heroes = {
    'index.html':              ('video', '../assets/videos/full line.mp4', 'رواد الهندسة الصناعية', 'نصمم وننتج ونركب خطوط إنتاج عالمية المستوى في مصر ودول الخليج.'),
    'production-lines.html':   ('video', '../assets/videos/production-line-video-12.mp4', 'خطوط الإنتاج', 'حلول متكاملة للأغذية والمشروبات والتغليف والتجميع الصناعي.'),
    'conveyor-systems.html':   ('video', '../assets/videos/conveyor.mp4',  'السيور الناقلة', 'أنظمة مناولة متقدمة مصممة للسرعة والدقة والمتانة.'),
    'services.html':           ('video', '../assets/videos/designing.mp4',    'خدماتنا', 'تصميم هندسي، تصنيع، تركيب، ودعم فني على مدار الساعة.'),
    'contact.html':            ('image', '../assets/images/industrial-process-9.jpeg',    'اتصل بنا', 'نحن هنا لمساعدتك. تواصل معنا للحصول على استشارة أو زيارة ميدانية.'),
    'about.html':              ('image', '../assets/images/industrial-process-6.jpeg',    'عن آيكونيك ماشين', 'مبنية على الابتكار والثقة وعقدين من التميز في الهندسة الصناعية.'),
    'industries.html':         ('video', '../assets/videos/sorting.mp4','الصناعات التي نخدمها', 'من تصنيع الغذاء إلى اللوجستيات — نحن نُشغّل القطاعات التي تُشغّل مصر.'),
    'projects.html':           ('video', '../assets/videos/full line.mp4', 'مشاريعنا', 'استعرض تركيباتنا المنجزة وقصص النجاح من جميع أنحاء المنطقة.'),
    'blog.html':               ('image', '../assets/images/industrial-process-7.jpeg',    'رؤى وأخبار', 'ابق على اطلاع بآخر مستجدات الهندسة الصناعية والأتمتة.'),
    'faq.html':                ('image', '../assets/images/industrial-process-3.jpeg',    'الأسئلة الشائعة', 'إجابات سريعة على أكثر الأسئلة التي يطرحها عملاؤنا.'),
    'request-quotation.html':  ('image', '../assets/images/industrial-process-4.jpeg',    'اطلب عرض سعر', 'أخبرنا عن مشروعك وسنقدم لك تسعيرة تنافسية.'),
    'technical-support.html':  ('image', '../assets/images/industrial-process-5.jpeg',    'الدعم الفني 24/7', 'مهندسونا دائماً في حالة تأهب للحفاظ على تشغيل أنظمتك.'),
    'spare-parts.html':        ('image', '../assets/images/industrial-process-1.jpeg',    'قطع الغيار', 'قطع غيار أصلية تُسلَّم بسرعة للحد من وقت التوقف.'),
    'privacy-policy.html':     ('image', '../assets/images/industrial-process-2.jpeg',    'سياسة الخصوصية', 'كيف نجمع بياناتك ونستخدمها ونحميها.'),
    'terms.html':              ('image', '../assets/images/industrial-process-10.jpeg',   'الشروط والأحكام', 'الشروط التي تحكم استخدام خدماتنا وموقعنا.'),
}

def make_hero(filename):
    media_type, src, title, subtitle = page_heroes.get(filename, ('image', '../assets/images/industrial-process-1.jpeg', 'آيكونيك ماشين الهندسية', ''))
    if filename == 'index.html':
        return f'''
    <section class="page-hero" style="position:relative; height:100vh; min-height:600px; display:flex; align-items:center; justify-content:center; text-align:center; overflow:hidden;">
        <video autoplay loop muted playsinline src="{src}"
            style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:0; transform:scale(1.15) translate(-2%, -2%);"></video>
        <div style="position:absolute; inset:0; background:rgba(6,18,38,0.62); z-index:1;"></div>
        <div class="container reveal fade-in" style="position:relative; z-index:2; color:#fff; padding:0 20px;">
            <p style="font-size:1rem; letter-spacing:3px; text-transform:uppercase; opacity:0.8; margin-bottom:16px;">آيكونيك ماشين الهندسية</p>
            <h1 style="font-size:clamp(2.2rem,5vw,4rem); font-weight:700; line-height:1.2; margin-bottom:22px; text-shadow:0 2px 16px rgba(0,0,0,0.4);">{title}</h1>
            <p style="font-size:1.15rem; max-width:640px; margin:0 auto 36px; opacity:0.88; line-height:1.7;">{subtitle}</p>
            <div style="display:flex; gap:16px; justify-content:center; flex-wrap:wrap;">
                <a href="production-lines.html" class="btn btn-primary" style="padding:14px 32px; font-size:1rem; text-decoration:none;">منتجاتنا</a>
                <a href="contact.html" style="padding:14px 32px; font-size:1rem; border:2px solid rgba(255,255,255,0.7); border-radius:var(--radius-sm); color:#fff; text-decoration:none; backdrop-filter:blur(4px);">تواصل معنا</a>
            </div>
        </div>
        <a href="#main-content" style="position:absolute; bottom:32px; left:50%; transform:translateX(-50%); z-index:2; color:rgba(255,255,255,0.7); font-size:2rem; text-decoration:none; animation:bounceDown 2s infinite;">&#8964;</a>
    </section>'''
    elif media_type == 'video':
        return f'''
    <section class="page-hero" style="position:relative; height:55vh; min-height:380px; display:flex; align-items:center; justify-content:center; text-align:center; overflow:hidden;">
        <video autoplay loop muted playsinline src="{src}"
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
    <footer class="site-footer" style="background:#061226; color:#c9d8ec; padding:64px 0 0;">
        <div class="container">
            <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:48px; padding-bottom:48px; border-bottom:1px solid rgba(255,255,255,0.08);">
                <!-- Brand -->
                <div>
                    <img src="../assets/images/footer_logo.png" alt="آيكونيك ماشين الهندسية" style="height:75px; margin-bottom:16px;">
                    <p style="font-size:0.92rem; line-height:1.8; opacity:0.7; max-width:240px;">نصمم وننتج أنظمة خطوط إنتاج وسيور ناقلة بمعايير عالمية في مصر ودول الخليج.</p>
                                        <div style="display:flex; gap:12px; margin-top:20px; flex-wrap:wrap;">
                        <a href="https://www.instagram.com/iconic.mach/" target="_blank" aria-label="Instagram" title="Instagram" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#c9d8ec;text-decoration:none;transition:background .2s;" onmouseover="this.style.background='#e1306c';" onmouseout="this.style.background='rgba(255,255,255,0.08)';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg></a>
                        <a href="https://www.tiktok.com/@iconicmach" target="_blank" aria-label="TikTok" title="TikTok" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#c9d8ec;text-decoration:none;transition:background .2s;" onmouseover="this.style.background='#010101';" onmouseout="this.style.background='rgba(255,255,255,0.08)';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.32 6.32 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.69a8.16 8.16 0 004.77 1.52V6.74a4.85 4.85 0 01-1-.05z"/></svg></a>
                        <a href="https://www.facebook.com/profile.php?id=61590558549282" target="_blank" aria-label="Facebook" title="Facebook" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#c9d8ec;text-decoration:none;transition:background .2s;" onmouseover="this.style.background='#1877f2';" onmouseout="this.style.background='rgba(255,255,255,0.08)';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a>
                        <a href="https://www.linkedin.com/in/mahmoud-turk-82bbb8412/" target="_blank" aria-label="LinkedIn" title="LinkedIn" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#c9d8ec;text-decoration:none;transition:background .2s;" onmouseover="this.style.background='#0077b5';" onmouseout="this.style.background='rgba(255,255,255,0.08)';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>
                        <a href="https://www.youtube.com/@Iconicmach" target="_blank" aria-label="YouTube" title="YouTube" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#c9d8ec;text-decoration:none;transition:background .2s;" onmouseover="this.style.background='#ff0000';" onmouseout="this.style.background='rgba(255,255,255,0.08)';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a>
                        <a href="https://wa.me/20108472717" target="_blank" aria-label="WhatsApp" title="WhatsApp" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#c9d8ec;text-decoration:none;transition:background .2s;" onmouseover="this.style.background='#25d366';" onmouseout="this.style.background='rgba(255,255,255,0.08)';"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg></a>
                    </div>
                </div>
                <!-- المنتجات -->
                <div>
                    <h4 style="color:#fff; font-size:1rem; font-weight:600; margin-bottom:18px;">المنتجات</h4>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:10px;">
                        <li><a href="production-lines.html" style="color:#c9d8ec;text-decoration:none;font-size:0.9rem;opacity:0.8;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">خطوط الإنتاج</a></li>
                        <li><a href="conveyor-systems.html" style="color:#c9d8ec;text-decoration:none;font-size:0.9rem;opacity:0.8;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">السيور الناقلة</a></li>
                        <li><a href="spare-parts.html" style="color:#c9d8ec;text-decoration:none;font-size:0.9rem;opacity:0.8;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">قطع الغيار</a></li>
                        <li><a href="request-quotation.html" style="color:#c9d8ec;text-decoration:none;font-size:0.9rem;opacity:0.8;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">طلب عرض سعر</a></li>
                    </ul>
                </div>
                <!-- الشركة -->
                <div>
                    <h4 style="color:#fff; font-size:1rem; font-weight:600; margin-bottom:18px;">الشركة</h4>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:10px;">
                        <li><a href="about.html" style="color:#c9d8ec;text-decoration:none;font-size:0.9rem;opacity:0.8;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">من نحن</a></li>
                        <li><a href="services.html" style="color:#c9d8ec;text-decoration:none;font-size:0.9rem;opacity:0.8;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">خدماتنا</a></li>
                        <li><a href="industries.html" style="color:#c9d8ec;text-decoration:none;font-size:0.9rem;opacity:0.8;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">الصناعات</a></li>
                        <li><a href="projects.html" style="color:#c9d8ec;text-decoration:none;font-size:0.9rem;opacity:0.8;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">المشاريع</a></li>
                        <li><a href="blog.html" style="color:#c9d8ec;text-decoration:none;font-size:0.9rem;opacity:0.8;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">المدونة</a></li>
                        <li><a href="faq.html" style="color:#c9d8ec;text-decoration:none;font-size:0.9rem;opacity:0.8;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">الأسئلة الشائعة</a></li>
                    </ul>
                </div>
                <!-- التواصل -->
                <div>
                    <h4 style="color:#fff; font-size:1rem; font-weight:600; margin-bottom:18px;">تواصل معنا</h4>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:12px; font-size:0.9rem;">
                        <li style="display:flex; gap:10px; align-items:flex-start;"><span style="margin-top:2px;">📍</span><span style="opacity:0.8;">شمس مول، العاشر من رمضان،<br>الشرقية، مصر</span></li>
                        <li style="display:flex; gap:10px; align-items:center;"><span>📱</span><a href="https://wa.me/20108472717" style="color:#4adeae; text-decoration:none;" dir="ltr">+20 108 472 717</a></li>
                        <li style="display:flex; gap:10px; align-items:center;"><span>✉️</span><a href="mailto:sales@iconicmach.com" style="color:#4adeae; text-decoration:none;">sales@iconicmach.com</a></li>
                        <li style="display:flex; gap:10px; align-items:center;"><span>🔧</span><a href="mailto:technical@iconicmach.com" style="color:#4adeae; text-decoration:none;">technical@iconicmach.com</a></li>
                    </ul>
                </div>
            </div>
            <div style="padding:24px 0; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; font-size:0.85rem; opacity:0.6;">
                <p style="margin:0;">&copy; 2026 آيكونيك ماشين الهندسية. جميع الحقوق محفوظة.</p>
                <div style="display:flex; gap:20px;">
                    <a href="privacy-policy.html" style="color:#c9d8ec; text-decoration:none;">سياسة الخصوصية</a>
                    <a href="terms.html" style="color:#c9d8ec; text-decoration:none;">الشروط والأحكام</a>
                </div>
            </div>
        </div>
    </footer>'''

pages = {
    'index.html': ('الرئيسية', 'آيكونيك ماشين الهندسية — خطوط إنتاج وسيور ناقلة وأتمتة صناعية.', '''
    <section id="main-content" class="section" style="padding-top:80px;">
        <div class="container">
            <div style="text-align:center; margin-bottom:60px;">
                <h2 class="text-primary" style="font-size:2rem; margin-bottom:12px;">ماذا نقدم</h2>
                <p class="text-muted" style="max-width:640px; margin:0 auto; line-height:1.8;">من الفكرة حتى التشغيل — نبني الأنظمة التي تُبقي المصانع تعمل بأقصى كفاءة.</p>
            </div>
            <div class="grid grid-3" style="margin-bottom:80px;">
                <div class="card bg-main" style="padding:32px; text-align:center; box-shadow:var(--shadow-sm);">
                    <div style="font-size:2.5rem; margin-bottom:16px;">🏭</div>
                    <h3 style="margin-bottom:12px; color:var(--primary-blue);">خطوط الإنتاج</h3>
                    <p style="line-height:1.7; margin-bottom:20px;">تصميم وتركيب خطوط إنتاج متكاملة لقطاعات الأغذية والمشروبات والصناعة.</p>
                    <a href="production-lines.html" style="color:var(--primary-blue); font-weight:600; text-decoration:none;">اعرف المزيد &larr;</a>
                </div>
                <div class="card bg-main" style="padding:32px; text-align:center; box-shadow:var(--shadow-sm);">
                    <div style="font-size:2.5rem; margin-bottom:16px;">⚙️</div>
                    <h3 style="margin-bottom:12px; color:var(--primary-blue);">السيور الناقلة</h3>
                    <p style="line-height:1.7; margin-bottom:20px;">سيور حزام ودرفيل وبلاستيكية مهندسة لأقصى إنتاجية وموثوقية.</p>
                    <a href="conveyor-systems.html" style="color:var(--primary-blue); font-weight:600; text-decoration:none;">اعرف المزيد &larr;</a>
                </div>
                <div class="card bg-main" style="padding:32px; text-align:center; box-shadow:var(--shadow-sm);">
                    <div style="font-size:2.5rem; margin-bottom:16px;">🔧</div>
                    <h3 style="margin-bottom:12px; color:var(--primary-blue);">الصيانة والدعم</h3>
                    <p style="line-height:1.7; margin-bottom:20px;">دعم فني 24/7 وعقود صيانة وتوريد قطع غيار أصلية.</p>
                    <a href="services.html" style="color:var(--primary-blue); font-weight:600; text-decoration:none;">اعرف المزيد &larr;</a>
                </div>
            </div>
            <!-- الرسالة والرؤية -->
            <div class="grid grid-2" style="margin-bottom:80px; gap:40px;">
                <div class="card bg-main" style="padding:40px; border-right:4px solid var(--primary-blue); box-shadow:var(--shadow-sm);">
                    <h3 style="font-size:1.8rem; margin-bottom:16px;">🎯 رسالتنا</h3>
                    <p style="line-height:1.8; font-size:1.1rem; color:var(--text-muted);">تقديم حلول هندسية صناعية عالمية المستوى تمكّن المصنعين في مصر ودول الخليج من المنافسة عالمياً.</p>
                </div>
                <div class="card bg-main" style="padding:40px; border-right:4px solid var(--primary-blue); box-shadow:var(--shadow-sm);">
                    <h3 style="font-size:1.8rem; margin-bottom:16px;">👁️ رؤيتنا</h3>
                    <p style="line-height:1.8; font-size:1.1rem; color:var(--text-muted);">أن نكون الشريك الرائد في الأتمتة الصناعية بمنطقة الشرق الأوسط وشمال أفريقيا، معروفين بالجودة والموثوقية والابتكار.</p>
                </div>
            </div>
            <!-- الإحصائيات -->
            <div style="background:var(--primary-blue); border-radius:var(--radius-md); padding:48px; display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:32px; text-align:center; color:#fff; margin-bottom:80px;">
                <div><p style="font-size:3rem; font-weight:700; margin:0;">+100</p><p style="opacity:0.8; margin:4px 0 0;">نظام مُركَّب</p></div>
                <div><p style="font-size:3rem; font-weight:700; margin:0;">+15</p><p style="opacity:0.8; margin:4px 0 0;">سنة خبرة</p></div>
                <div><p style="font-size:3rem; font-weight:700; margin:0;">24/7</p><p style="opacity:0.8; margin:4px 0 0;">دعم فني</p></div>
                <div><p style="font-size:3rem; font-weight:700; margin:0;">الخليج</p><p style="opacity:0.8; margin:4px 0 0;">تغطية إقليمية</p></div>
            </div>
            <!-- المشاريع والشركاء -->
            <div style="margin-bottom:80px;">
                <div style="text-align:center; margin-bottom:40px;">
                    <h2 class="text-primary" style="font-size:2rem; margin-bottom:12px;">مشاريع مميزة</h2>
                    <p class="text-muted" style="max-width:640px; margin:0 auto; line-height:1.8;">نظرة على أحدث تركيباتنا الناجحة.</p>
                </div>
                <div class="grid grid-2" style="margin-bottom:40px;">
                    <div class="card bg-main" style="padding:0; overflow:hidden; box-shadow:var(--shadow-sm);"><video autoplay loop muted playsinline src="../assets/videos/beverages.mp4" style="width:100%;height:180px;object-fit:cover;"></video><div style="padding:20px;"><h4 style="margin-bottom:6px;">خط تعبئة المشروبات</h4><p style="font-size:0.9rem;color:var(--text-muted);">12,000 زجاجة/ساعة</p></div></div>
                    <div class="card bg-main" style="padding:0; overflow:hidden; box-shadow:var(--shadow-sm);"><video autoplay loop muted playsinline src="../assets/videos/packing.mp4" style="width:100%;height:180px;object-fit:cover;"></video><div style="padding:20px;"><h4 style="margin-bottom:6px;">نظام تغليف السلع الاستهلاكية</h4><p style="font-size:0.9rem;color:var(--text-muted);">تعبئة كرتون متعدد المسارات</p></div></div>
                </div>
                <div style="text-align:center; margin-bottom:80px;">
                    <a href="projects.html" style="color:var(--primary-blue); font-weight:600; text-decoration:none;">عرض كل المشاريع &larr;</a>
                </div>

                <div style="text-align:center; margin-bottom:40px;">
                    <h2 class="text-primary" style="font-size:2rem; margin-bottom:12px;">شركاء نثق بهم</h2>
                    <p class="text-muted" style="max-width:640px; margin:0 auto; line-height:1.8;">نتعاون مع رواد الصناعة لتقديم أفضل المكونات والحلول.</p>
                </div>
                <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:48px; opacity:0.5; filter:grayscale(100%);" dir="ltr">
                    <div style="font-size:1.6rem; font-weight:700; font-family:sans-serif; letter-spacing:1px;">OMRON</div>
                    <div style="font-size:1.6rem; font-weight:700; font-family:sans-serif; letter-spacing:1px;">SIEMENS</div>
                    <div style="font-size:1.6rem; font-weight:700; font-family:sans-serif; letter-spacing:1px;">SEW-EURODRIVE</div>
                    <div style="font-size:1.6rem; font-weight:700; font-family:sans-serif; letter-spacing:1px;">FESTO</div>
                    <div style="font-size:1.6rem; font-weight:700; font-family:sans-serif; letter-spacing:1px;">SICK</div>
                </div>
            </div>
            <div style="text-align:center;">
                <h2 class="text-primary" style="font-size:1.8rem; margin-bottom:16px;">هل أنت مستعد لترقية إنتاجك؟</h2>
                <p class="text-muted" style="margin-bottom:28px;">احصل على استشارة مجانية من فريقنا الهندسي.</p>
                <a href="contact.html" class="btn btn-primary" style="padding:14px 36px; font-size:1rem; text-decoration:none;">تحدث مع مهندس</a>
            </div>
        </div>
    </section>'''),

    'production-lines.html': ('خطوط الإنتاج', 'حلول متكاملة لخطوط الإنتاج والأغذية والمشروبات والتغليف والمستودعات.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-3" style="margin-bottom:60px;">
                <div class="card bg-main" style="padding:0; overflow:hidden; box-shadow:var(--shadow-sm);">
                    <video autoplay loop muted playsinline src="../assets/videos/beverages.mp4" style="width:100%;height:220px;object-fit:cover;"></video>
                    <div style="padding:24px;"><h3 style="margin-bottom:10px;color:var(--primary-blue);">الأغذية والمشروبات</h3><p style="line-height:1.7;">خطوط صحية عالية الكفاءة لمعالجة وتعبئة وتغليف المنتجات الغذائية بأعلى معايير السلامة.</p></div>
                </div>
                <div class="card bg-main" style="padding:0; overflow:hidden; box-shadow:var(--shadow-sm);">
                    <video autoplay loop muted playsinline src="../assets/videos/packing.mp4" style="width:100%;height:220px;object-fit:cover;"></video>
                    <div style="padding:24px;"><h3 style="margin-bottom:10px;color:var(--primary-blue);">تغليف السلع الاستهلاكية</h3><p style="line-height:1.7;">خطوط تغليف عالية السرعة تُلغي الاختناقات وتُبقي السلع الاستهلاكية سريعة الحركة تتدفق بسلاسة.</p></div>
                </div>
                <div class="card bg-main" style="padding:0; overflow:hidden; box-shadow:var(--shadow-sm);">
                    <video autoplay loop muted playsinline src="../assets/videos/assembly.mp4" style="width:100%;height:220px;object-fit:cover;"></video>
                    <div style="padding:24px;"><h3 style="margin-bottom:10px;color:var(--primary-blue);">التجميع الصناعي</h3><p style="line-height:1.7;">خطوط تجميع شاقة للتشغيل المتواصل في البيئات الصناعية القاسية.</p></div>
                </div>
            </div>
            <div style="text-align:center; margin-top:40px;">
                <a href="request-quotation.html" class="btn btn-primary" style="padding:14px 32px; text-decoration:none;">اطلب عرض سعر</a>
            </div>
        </div>
    </section>'''),

    'conveyor-systems.html': ('السيور الناقلة', 'أنظمة سيور ناقلة لتسهيل مناولة المواد، بما في ذلك سيور الحزام والدرفيل والسلسلة.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-2" style="align-items:start; margin-bottom:60px;">
                <div>
                    <h2 class="text-primary" style="font-size:1.8rem; margin-bottom:24px;">حلول مناولة المواد</h2>
                    <div style="border-right:3px solid var(--primary-blue); padding-right:20px; margin-bottom:28px;">
                        <h3 style="margin-bottom:8px;">سيور الحزام</h3>
                        <p style="line-height:1.7;">مثالية لنقل المنتجات المختلفة بسرعة، متوفرة بتكوينات مسطحة ومائلة ومنحنية لأي مسقط أفقي.</p>
                    </div>
                    <div style="border-right:3px solid var(--primary-blue); padding-right:20px; margin-bottom:28px;">
                        <h3 style="margin-bottom:8px;">سيور الدرفيل</h3>
                        <p style="line-height:1.7;">أنظمة جاذبية وأسطوانات آلية مصممة للصناديق الثقيلة والمنصات والمكونات الصناعية الكبيرة.</p>
                    </div>
                    <div style="border-right:3px solid var(--primary-blue); padding-right:20px; margin-bottom:28px;">
                        <h3 style="margin-bottom:8px;">الأحزمة البلاستيكية المعيارية</h3>
                        <p style="line-height:1.7;">سهلة التنظيف ومتينة ومرنة — مثالية لبيئات معالجة الأغذية والأدوية.</p>
                    </div>
                    <div style="border-right:3px solid var(--primary-blue); padding-right:20px;">
                        <h3 style="margin-bottom:8px;">سيور السلسلة</h3>
                        <p style="line-height:1.7;">أنظمة سلاسل ثقيلة لتطبيقات السيارات والتصنيع المعدني وحركة المنصات في المستودعات.</p>
                    </div>
                </div>
                <div style="display:flex; flex-direction:column; gap:20px;">
                    <video autoplay loop muted playsinline src="../assets/videos/conveyor-1.mp4" style="width:100%;height:280px;object-fit:cover;border-radius:var(--radius-md);"></video>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
                        <div class="card bg-main" style="padding:20px;text-align:center;"><p class="text-primary" style="font-size:2rem;font-weight:700;margin:0;">+100</p><p style="font-size:0.9rem;margin:4px 0 0;">نظام مُركَّب</p></div>
                        <div class="card bg-main" style="padding:20px;text-align:center;"><p class="text-primary" style="font-size:2rem;font-weight:700;margin:0;">24/7</p><p style="font-size:0.9rem;margin:4px 0 0;">دعم متاح</p></div>
                    </div>
                </div>
            </div>
        </div>
    </section>'''),

    'services.html': ('خدماتنا', 'تصميم هندسي، تصنيع، تركيب، دعم فني وصيانة.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-3" style="margin-bottom:60px;">
                <div class="card bg-main" style="padding:32px;box-shadow:var(--shadow-sm);"><div style="font-size:2rem;margin-bottom:14px;">📐</div><h3 style="margin-bottom:12px;color:var(--primary-blue);">التصميم الهندسي</h3><p style="line-height:1.7;">نمذجة 3D وتحسين تدفق العمليات مصمم خصيصاً لمنشأتك وأهدافها الإنتاجية.</p></div>
                <div class="card bg-main" style="padding:32px;box-shadow:var(--shadow-sm);"><div style="font-size:2rem;margin-bottom:14px;">🏭</div><h3 style="margin-bottom:12px;color:var(--primary-blue);">التصنيع</h3><p style="line-height:1.7;">تصنيع داخلي باستخدام الفولاذ المقاوم للصدأ الملائم للأغذية ومقاطع الألومنيوم الدقيقة.</p></div>
                <div class="card bg-main" style="padding:32px;box-shadow:var(--shadow-sm);"><div style="font-size:2rem;margin-bottom:14px;">🔧</div><h3 style="margin-bottom:12px;color:var(--primary-blue);">التركيب</h3><p style="line-height:1.7;">تجميع ميداني احترافي وتمديد كهربائي وبرمجة PLC وتشغيل كامل بواسطة مهندسين معتمدين.</p></div>
                <div class="card bg-main" style="padding:32px;box-shadow:var(--shadow-sm);"><div style="font-size:2rem;margin-bottom:14px;">⚙️</div><h3 style="margin-bottom:12px;color:var(--primary-blue);">الصيانة الوقائية</h3><p style="line-height:1.7;">عقود صيانة سنوية (AMC) مصممة لمنع الأعطال وإطالة عمر معداتك.</p></div>
                <div class="card bg-main" style="padding:32px;box-shadow:var(--shadow-sm);"><div style="font-size:2rem;margin-bottom:14px;">🤖</div><h3 style="margin-bottom:12px;color:var(--primary-blue);">ترقيات الأتمتة</h3><p style="line-height:1.7;">دمج أنظمة PLC حديثة وحساسات رؤية وروبوتات في خطوط الإنتاج اليدوية القائمة.</p></div>
                <div class="card bg-main" style="padding:32px;box-shadow:var(--shadow-sm);"><div style="font-size:2rem;margin-bottom:14px;">📦</div><h3 style="margin-bottom:12px;color:var(--primary-blue);">توريد قطع الغيار</h3><p style="line-height:1.7;">مخزون من الأحزمة والمحركات والحساسات والبكرات الأصلية للشحن السريع.</p></div>
            </div>
            <div style="text-align:center;"><a href="contact.html" class="btn btn-primary" style="padding:14px 32px;text-decoration:none;">تحدث مع فريقنا</a></div>
        </div>
    </section>'''),

    'contact.html': ('اتصل بنا', 'تواصل مع آيكونيك ماشين الهندسية للاستفسار أو لطلب زيارة ميدانية.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-2" style="align-items:start; margin-bottom:60px;">
                <div>
                    <h2 class="text-primary" style="font-size:1.8rem; margin-bottom:16px;">تواصل معنا</h2>
                    <p style="line-height:1.8; margin-bottom:32px; color:var(--text-muted);">هل لديك مشروع في ذهنك؟ فريقنا الهندسي مستعد للاستشارة وزيارة الموقع وتصميم الحل المثالي.</p>
                    <div style="display:flex; flex-direction:column; gap:20px; margin-bottom:32px;">
                        <div style="display:flex; align-items:flex-start; gap:16px;"><div style="font-size:1.6rem;line-height:1;">📍</div><div><strong>العنوان</strong><br><span style="color:var(--text-muted);">شمس مول، العاشر من رمضان، الشرقية، مصر</span></div></div>
                        <div style="display:flex; align-items:flex-start; gap:16px;"><div style="font-size:1.6rem;line-height:1;">📱</div><div><strong>الهاتف / واتساب</strong><br><a href="https://wa.me/20108472717" style="color:var(--primary-blue);text-decoration:none;font-weight:600;" dir="ltr">+20 108 472 717</a></div></div>
                        <div style="display:flex; align-items:flex-start; gap:16px;"><div style="font-size:1.6rem;line-height:1;">✉️</div><div><strong>استفسارات المبيعات</strong><br><a href="mailto:sales@iconicmach.com" style="color:var(--primary-blue);text-decoration:none;">sales@iconicmach.com</a></div></div>
                        <div style="display:flex; align-items:flex-start; gap:16px;"><div style="font-size:1.6rem;line-height:1;">🔧</div><div><strong>الدعم الفني</strong><br><a href="mailto:technical@iconicmach.com" style="color:var(--primary-blue);text-decoration:none;">technical@iconicmach.com</a></div></div>
                    </div>
                    <div style="border-radius:var(--radius-md); overflow:hidden; box-shadow:var(--shadow-sm);">
                        <iframe title="موقع آيكونيك ماشين الهندسية"
                            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d13651.989047248354!2d31.7371987!3d30.301314!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xa9efd409ec5898fb!2z2YXZiNmEINi02YXYsw!5e0!3m2!1sar!2seg!4v1717320000000!5m2!1sar!2seg"
                            width="100%" height="300" style="border:0; display:block;" allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade">
                        </iframe>
                    </div>
                </div>
                <div>
                    <form action="#" method="POST" class="card bg-main" style="display:flex;flex-direction:column;gap:18px;padding:40px;box-shadow:var(--shadow-md);">
                        <h3 style="margin-bottom:8px;">أرسل لنا رسالة</h3>
                        <input type="text" placeholder="الاسم الكامل" required style="padding:13px 16px;border:1px solid var(--border-color);border-radius:var(--radius-sm);font-family:inherit;font-size:0.95rem;background:var(--bg-alt);">
                        <input type="email" placeholder="البريد الإلكتروني" required style="padding:13px 16px;border:1px solid var(--border-color);border-radius:var(--radius-sm);font-family:inherit;font-size:0.95rem;background:var(--bg-alt);">
                        <input type="tel" placeholder="رقم الهاتف" style="padding:13px 16px;border:1px solid var(--border-color);border-radius:var(--radius-sm);font-family:inherit;font-size:0.95rem;background:var(--bg-alt);">
                        <input type="text" placeholder="الموضوع" required style="padding:13px 16px;border:1px solid var(--border-color);border-radius:var(--radius-sm);font-family:inherit;font-size:0.95rem;background:var(--bg-alt);">
                        <textarea placeholder="أخبرنا عن مشروعك..." rows="5" required style="padding:13px 16px;border:1px solid var(--border-color);border-radius:var(--radius-sm);font-family:inherit;font-size:0.95rem;background:var(--bg-alt);resize:vertical;"></textarea>
                        <button type="submit" class="btn btn-primary" style="padding:14px;font-weight:600;border:none;cursor:pointer;font-size:1rem;">إرسال الرسالة</button>
                    </form>
                </div>
            </div>
        </div>
    </section>'''),

    'about.html': ('من نحن', 'تعرف على آيكونيك ماشين الهندسية — قصتنا وفريقنا ورسالتنا.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-2" style="align-items:center; margin-bottom:60px;">
                <div>
                    <h2 class="text-primary" style="font-size:1.8rem; margin-bottom:16px;">قصتنا</h2>
                    <p style="line-height:1.8; margin-bottom:16px;">تأسست آيكونيك ماشين الهندسية على مبادئ الابتكار والموثوقية، ونمت لتصبح شريكاً صناعياً موثوقاً في مصر ودول الخليج.</p>
                    <p style="line-height:1.8; margin-bottom:24px;">نؤمن بأن الهندسة الجيدة تصمد أمام اختبار الزمن — كل نظام نبنيه مصمم لتحقيق أقصى كفاءة وأدنى توقف وعائد استثمار قابل للقياس.</p>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
                        <div class="card bg-main" style="padding:20px;text-align:center;"><p class="text-primary" style="font-size:2rem;font-weight:700;margin:0;">+100</p><p style="font-size:0.85rem;margin:4px 0 0;">مشروع منجز</p></div>
                        <div class="card bg-main" style="padding:20px;text-align:center;"><p class="text-primary" style="font-size:2rem;font-weight:700;margin:0;">+15</p><p style="font-size:0.85rem;margin:4px 0 0;">سنة تميز</p></div>
                    </div>
                </div>
                <div>
                    <img src="../assets/images/mahmoud-turk.jpeg" alt="محمود ترك — المؤسس" style="width:100%;border-radius:var(--radius-md);box-shadow:var(--shadow-sm);">
                    <p style="text-align:center;font-size:0.9rem;margin-top:10px;color:var(--text-muted);">محمود ترك — المؤسس والرئيس التنفيذي</p>
                </div>
            </div>
            <div class="grid grid-3" style="margin-bottom:40px;">
                <div class="card bg-main" style="padding:28px;border-top:4px solid var(--primary-blue);"><h3 style="margin-bottom:10px;">🎯 رسالتنا</h3><p style="line-height:1.7;">تقديم حلول هندسية صناعية عالمية المستوى تمكّن المصنعين المصريين والخليجيين من المنافسة عالمياً.</p></div>
                <div class="card bg-main" style="padding:28px;border-top:4px solid var(--primary-blue);"><h3 style="margin-bottom:10px;">👁️ رؤيتنا</h3><p style="line-height:1.7;">أن نكون الشريك الرائد في الأتمتة الصناعية بمنطقة الشرق الأوسط وشمال أفريقيا، معروفين بالجودة والابتكار.</p></div>
                <div class="card bg-main" style="padding:28px;border-top:4px solid var(--primary-blue);"><h3 style="margin-bottom:10px;">💡 قيمنا</h3><p style="line-height:1.7;">الدقة الهندسية والشراكة الشفافة والالتزام الدائم بنجاح عملياتنا.</p></div>
            </div>
        </div>
    </section>'''),

    'industries.html': ('الصناعات التي نخدمها', 'نُشغّل التصنيع عبر الأغذية والمشروبات والسلع الاستهلاكية واللوجستيات والمزيد.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-3" style="margin-bottom:60px;">
                <div class="card bg-main" style="padding:28px;border-top:4px solid var(--primary-blue);"><div style="font-size:2.2rem;margin-bottom:14px;">🍽️</div><h3 style="margin-bottom:10px;color:var(--primary-blue);">الأغذية والمشروبات</h3><p style="line-height:1.7;">خطوط إنتاج وسيور صحية متوافقة مع لوائح سلامة الغذاء.</p></div>
                <div class="card bg-main" style="padding:28px;border-top:4px solid var(--primary-blue);"><div style="font-size:2.2rem;margin-bottom:14px;">📦</div><h3 style="margin-bottom:10px;color:var(--primary-blue);">السلع الاستهلاكية والتغليف</h3><p style="line-height:1.7;">خطوط تغليف فائقة السرعة للسلع الاستهلاكية، تُلغي كل اختناق.</p></div>
                <div class="card bg-main" style="padding:28px;border-top:4px solid var(--primary-blue);"><div style="font-size:2.2rem;margin-bottom:14px;">🏗️</div><h3 style="margin-bottom:10px;color:var(--primary-blue);">التخزين واللوجستيات</h3><p style="line-height:1.7;">أنظمة فرز وتحديد مواضع وتوزيع للمستودعات الحديثة.</p></div>
                <div class="card bg-main" style="padding:28px;border-top:4px solid var(--primary-blue);"><div style="font-size:2.2rem;margin-bottom:14px;">🚗</div><h3 style="margin-bottom:10px;color:var(--primary-blue);">السيارات</h3><p style="line-height:1.7;">خطوط تجميع ولحام شاقة مهندسة لمصانع تصنيع السيارات.</p></div>
                <div class="card bg-main" style="padding:28px;border-top:4px solid var(--primary-blue);"><div style="font-size:2.2rem;margin-bottom:14px;">💊</div><h3 style="margin-bottom:10px;color:var(--primary-blue);">الأدوية</h3><p style="line-height:1.7;">سيور ناقلة وخطوط تعبئة بغرفة نظيفة متوافقة مع معايير GMP وFDA.</p></div>
                <div class="card bg-main" style="padding:28px;border-top:4px solid var(--primary-blue);"><div style="font-size:2.2rem;margin-bottom:14px;">🏭</div><h3 style="margin-bottom:10px;color:var(--primary-blue);">التصنيع العام</h3><p style="line-height:1.7;">حلول مخصصة لأي تطبيق صناعي — إذا كنت تصنعه، يمكننا أتمتته.</p></div>
            </div>
        </div>
    </section>'''),

    'projects.html': ('المشاريع', 'معرض أعمال آيكونيك ماشين الهندسية من المشاريع المنجزة.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div style="margin-bottom:48px;">
                <video autoplay loop muted playsinline src="../assets/videos/production-line-video-1.mp4" style="width:100%;height:380px;object-fit:cover;border-radius:var(--radius-md);box-shadow:var(--shadow-sm);"></video>
            </div>
            <p style="max-width:760px;margin:0 auto 48px;text-align:center;line-height:1.8;color:var(--text-muted);">من خطوط التعبئة عالية السرعة إلى أنظمة الفرز المعقدة — استكشف كيف حوّلنا أرضيات التصنيع في مصر ومنطقة الخليج.</p>
            <div class="grid grid-3">
                <div class="card bg-main" style="padding:0;overflow:hidden;"><video autoplay loop muted playsinline src="../assets/videos/production-line-video-3.mp4" style="width:100%;height:180px;object-fit:cover;"></video><div style="padding:20px;"><h4 style="margin-bottom:6px;">خط تعبئة المشروبات</h4><p style="font-size:0.9rem;color:var(--text-muted);">خط تعبئة وتغطية متكامل — 12,000 زجاجة/ساعة</p></div></div>
                <div class="card bg-main" style="padding:0;overflow:hidden;"><video autoplay loop muted playsinline src="../assets/videos/production-line-video-4.mp4" style="width:100%;height:180px;object-fit:cover;"></video><div style="padding:20px;"><h4 style="margin-bottom:6px;">نظام تغليف السلع الاستهلاكية</h4><p style="font-size:0.9rem;color:var(--text-muted);">خط كرتنة ووضع في صناديق متعدد المسارات</p></div></div>
                <div class="card bg-main" style="padding:0;overflow:hidden;"><video autoplay loop muted playsinline src="../assets/videos/production-line-video-5.mp4" style="width:100%;height:180px;object-fit:cover;"></video><div style="padding:20px;"><h4 style="margin-bottom:6px;">شبكة سيور المستودع</h4><p style="font-size:0.9rem;color:var(--text-muted);">تركيب سيور حزام ودرفيل لمستودع كامل</p></div></div>
            </div>
            <div style="text-align:center;margin-top:40px;"><a href="contact.html" class="btn btn-primary" style="padding:14px 32px;text-decoration:none;">ابدأ مشروعك</a></div>
        </div>
    </section>'''),

    'blog.html': ('المدونة', 'أحدث المقالات والرؤى والأخبار من آيكونيك ماشين الهندسية.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-3">
                <div class="card bg-main" style="padding:0;overflow:hidden;box-shadow:var(--shadow-sm);"><img src="../assets/images/industrial-process-1.jpeg" alt="" style="width:100%;height:180px;object-fit:cover;"><div style="padding:24px;"><span style="font-size:0.8rem;color:var(--primary-blue);font-weight:600;">الأتمتة</span><h3 style="margin:10px 0;font-size:1.1rem;">الصناعة 4.0: ما تعنيه للمصنعين المصريين</h3><p style="font-size:0.9rem;line-height:1.7;color:var(--text-muted);">كيف تعيد تقنيات المصانع الذكية تشكيل أرضيات الإنتاج المحلية.</p></div></div>
                <div class="card bg-main" style="padding:0;overflow:hidden;box-shadow:var(--shadow-sm);"><img src="../assets/images/industrial-process-7.jpeg" alt="" style="width:100%;height:180px;object-fit:cover;"><div style="padding:24px;"><span style="font-size:0.8rem;color:var(--primary-blue);font-weight:600;">الصيانة</span><h3 style="margin:10px 0;font-size:1.1rem;">5 علامات تدل على أن نظام السيور يحتاج ترقية</h3><p style="font-size:0.9rem;line-height:1.7;color:var(--text-muted);">التعرف على التحذيرات المبكرة قبل أن تتحول إلى أعطال مكلفة.</p></div></div>
                <div class="card bg-main" style="padding:0;overflow:hidden;box-shadow:var(--shadow-sm);"><img src="../assets/images/industrial-process-8.jpeg" alt="" style="width:100%;height:180px;object-fit:cover;"><div style="padding:24px;"><span style="font-size:0.8rem;color:var(--primary-blue);font-weight:600;">التصنيع الرشيق</span><h3 style="margin:10px 0;font-size:1.1rem;">تقليل الهدر بتصميم خط إنتاج رشيق</h3><p style="font-size:0.9rem;line-height:1.7;color:var(--text-muted);">كيف يمكن للتغييرات الاستراتيجية في التخطيط أن ترفع كفاءة المعدات بشكل ملحوظ.</p></div></div>
            </div>
        </div>
    </section>'''),

    'faq.html': ('الأسئلة الشائعة', 'إجابات على الأسئلة الأكثر شيوعاً حول منتجات وخدمات آيكونيك ماشين الهندسية.', '''
    <section id="main-content" class="section">
        <div class="container" style="max-width:800px;">
            <div style="display:flex;flex-direction:column;gap:16px;">
                <details class="card bg-main" style="padding:24px;cursor:pointer;"><summary style="font-weight:600;font-size:1rem;list-style:none;display:flex;justify-content:space-between;">هل تقدمون أنظمة مصممة حسب الطلب؟ <span>&#43;</span></summary><p style="margin-top:16px;line-height:1.8;color:var(--text-muted);">نعم. كل نظام نبنيه مهندَس خصيصاً لمساحتك وأهداف الإنتاج ومتطلبات المنتج. نبدأ بزيارة ميدانية واستشارة تفصيلية.</p></details>
                <details class="card bg-main" style="padding:24px;cursor:pointer;"><summary style="font-weight:600;font-size:1rem;list-style:none;display:flex;justify-content:space-between;">ما الصناعات التي تخدمونها؟ <span>&#43;</span></summary><p style="margin-top:16px;line-height:1.8;color:var(--text-muted);">نعمل في الأغذية والمشروبات والسلع الاستهلاكية والأدوية والسيارات والتخزين والتصنيع العام. أي بيئة إنتاجية يمكن الاستفادة من حلولنا.</p></details>
                <details class="card bg-main" style="padding:24px;cursor:pointer;"><summary style="font-weight:600;font-size:1rem;list-style:none;display:flex;justify-content:space-between;">هل تقدمون صيانة ما بعد البيع؟ <span>&#43;</span></summary><p style="margin-top:16px;line-height:1.8;color:var(--text-muted);">بالتأكيد. نقدم عقود صيانة سنوية (AMC) تشمل الفحوصات الدورية والاستبدال الوقائي للقطع والاستجابة الطارئة ذات الأولوية.</p></details>
                <details class="card bg-main" style="padding:24px;cursor:pointer;"><summary style="font-weight:600;font-size:1rem;list-style:none;display:flex;justify-content:space-between;">كم يستغرق التركيب النموذجي؟ <span>&#43;</span></summary><p style="margin-top:16px;line-height:1.8;color:var(--text-muted);">تتفاوت الجداول الزمنية بحسب تعقيد المشروع. ينتهي نظام السيور القياسي في 2-4 أسابيع من اعتماد التصميم. قد تستغرق خطوط الإنتاج الكاملة 6-12 أسبوعاً.</p></details>
                <details class="card bg-main" style="padding:24px;cursor:pointer;"><summary style="font-weight:600;font-size:1rem;list-style:none;display:flex;justify-content:space-between;">هل يمكنكم ترقية معداتي الموجودة؟ <span>&#43;</span></summary><p style="margin-top:16px;line-height:1.8;color:var(--text-muted);">نعم. نتخصص في ترقيات الأتمتة — دمج وحدات PLC الحديثة والحساسات وأنظمة التحكم في خطوطك القائمة دون الحاجة لاستبدال كامل.</p></details>
            </div>
        </div>
    </section>'''),

    'request-quotation.html': ('اطلب عرض سعر', 'اطلب عرض سعر من آيكونيك ماشين الهندسية لمشروعك الصناعي.', '''
    <section id="main-content" class="section">
        <div class="container" style="max-width:700px;">
            <p style="text-align:center;line-height:1.8;margin-bottom:40px;color:var(--text-muted);">املأ النموذج أدناه وسيتواصل معك فريق المبيعات خلال يوم عمل واحد بعرض سعر تفصيلي ومنافس.</p>
            <form action="#" method="POST" class="card bg-main" style="display:flex;flex-direction:column;gap:18px;padding:40px;box-shadow:var(--shadow-md);">
                <input type="text" placeholder="الاسم الكامل" required style="padding:13px 16px;border:1px solid var(--border-color);border-radius:var(--radius-sm);font-family:inherit;background:var(--bg-alt);">
                <input type="text" placeholder="اسم الشركة" style="padding:13px 16px;border:1px solid var(--border-color);border-radius:var(--radius-sm);font-family:inherit;background:var(--bg-alt);">
                <input type="email" placeholder="البريد الإلكتروني" required style="padding:13px 16px;border:1px solid var(--border-color);border-radius:var(--radius-sm);font-family:inherit;background:var(--bg-alt);">
                <input type="tel" placeholder="رقم الهاتف / واتساب" style="padding:13px 16px;border:1px solid var(--border-color);border-radius:var(--radius-sm);font-family:inherit;background:var(--bg-alt);">
                <select style="padding:13px 16px;border:1px solid var(--border-color);border-radius:var(--radius-sm);font-family:inherit;background:var(--bg-alt);">
                    <option value="">المنتج / الخدمة المطلوبة</option>
                    <option>خط إنتاج</option>
                    <option>سيور ناقلة</option>
                    <option>عقد صيانة</option>
                    <option>ترقية أتمتة</option>
                    <option>قطع غيار</option>
                    <option>أخرى</option>
                </select>
                <textarea placeholder="صف متطلبات مشروعك..." rows="6" required style="padding:13px 16px;border:1px solid var(--border-color);border-radius:var(--radius-sm);font-family:inherit;background:var(--bg-alt);resize:vertical;"></textarea>
                <button type="submit" class="btn btn-primary" style="padding:14px;font-weight:600;border:none;cursor:pointer;font-size:1rem;">إرسال طلب عرض السعر</button>
            </form>
        </div>
    </section>'''),

    'technical-support.html': ('الدعم الفني', 'دعم فني على مدار الساعة لجميع تركيبات آيكونيك ماشين الهندسية.', '''
    <section id="main-content" class="section">
        <div class="container">
            <div class="grid grid-2" style="align-items:center;margin-bottom:60px;">
                <div>
                    <h2 class="text-primary" style="font-size:1.8rem;margin-bottom:16px;">دائماً مستعدون</h2>
                    <p style="line-height:1.8;margin-bottom:16px;">توقف الماكينة مكلف. فريقنا الهندسي سريع الاستجابة في حالة تأهب على مدار الساعة لتشخيص المشكلات وحلها قبل أن تؤثر على أهداف إنتاجك.</p>
                    <ul style="list-style:none;display:flex;flex-direction:column;gap:12px;margin-bottom:28px;">
                        <li style="display:flex;gap:12px;align-items:flex-start;"><span style="color:var(--primary-blue);font-weight:700;font-size:1.2rem;">✓</span> تشخيص عن بُعد وحل مشكلات PLC</li>
                        <li style="display:flex;gap:12px;align-items:flex-start;"><span style="color:var(--primary-blue);font-weight:700;font-size:1.2rem;">✓</span> إرسال فني ميداني للموقع</li>
                        <li style="display:flex;gap:12px;align-items:flex-start;"><span style="color:var(--primary-blue);font-weight:700;font-size:1.2rem;">✓</span> توصيل طارئ لقطع الغيار</li>
                        <li style="display:flex;gap:12px;align-items:flex-start;"><span style="color:var(--primary-blue);font-weight:700;font-size:1.2rem;">✓</span> عقود الصيانة السنوية (AMC)</li>
                    </ul>
                    <a href="https://wa.me/20108472717" class="btn btn-primary" style="padding:14px 28px;text-decoration:none;">واتساب الدعم الآن</a>
                </div>
                <div><img src="../assets/images/industrial-process-5.jpeg" alt="الدعم الفني" style="width:100%;border-radius:var(--radius-md);box-shadow:var(--shadow-sm);"></div>
            </div>
        </div>
    </section>'''),

    'spare-parts.html': ('قطع الغيار', 'اطلب قطع غيار أصلية لأنظمة آيكونيك ماشين الهندسية.', '''
    <section id="main-content" class="section">
        <div class="container">
            <p style="max-width:700px;margin:0 auto 48px;text-align:center;line-height:1.8;color:var(--text-muted);">استخدام القطع الأصلية يضمن الأداء الأمثل ويطيل عمر معداتك. نحتفظ بمخزون شامل للإرسال الفوري.</p>
            <div class="grid grid-3" style="margin-bottom:48px;">
                <div class="card bg-main" style="padding:28px;text-align:center;"><div style="font-size:2rem;margin-bottom:12px;">🔗</div><h3 style="margin-bottom:8px;">أحزمة السيور</h3><p style="line-height:1.7;font-size:0.92rem;">PVC وPU وبلاستيك معياري وأحزمة معدنية بجميع العروض القياسية.</p></div>
                <div class="card bg-main" style="padding:28px;text-align:center;"><div style="font-size:2rem;margin-bottom:12px;">⚡</div><h3 style="margin-bottom:8px;">محركات الكهرباء</h3><p style="line-height:1.7;font-size:0.92rem;">محركات أحادية وثلاثية الأوجه وعلب تروس ومحولات تردد.</p></div>
                <div class="card bg-main" style="padding:28px;text-align:center;"><div style="font-size:2rem;margin-bottom:12px;">📡</div><h3 style="margin-bottom:8px;">الحساسات والتحكم</h3><p style="line-height:1.7;font-size:0.92rem;">حساسات تقارب وكاميرات فوتو وموديلات PLC.</p></div>
            </div>
            <div style="text-align:center;"><a href="contact.html" class="btn btn-primary" style="padding:14px 32px;text-decoration:none;">اطلب قطع الغيار</a></div>
        </div>
    </section>'''),

    'privacy-policy.html': ('سياسة الخصوصية', 'سياسة الخصوصية لشركة آيكونيك ماشين الهندسية.', '''
    <section id="main-content" class="section">
        <div class="container" style="max-width:800px;">
            <div class="card bg-main" style="padding:40px;box-shadow:var(--shadow-sm);">
                <h2 class="text-primary" style="margin-bottom:20px;">خصوصيتك تهمنا</h2>
                <p style="line-height:1.8;margin-bottom:16px;">تلتزم آيكونيك ماشين الهندسية بحماية بياناتك الشخصية. نجمع فقط البيانات الضرورية للرد على استفساراتك وتحسين خدماتنا.</p>
                <h3 style="margin:24px 0 10px;">ما نجمعه</h3>
                <p style="line-height:1.8;margin-bottom:16px;">الاسم والبريد الإلكتروني ورقم الهاتف وتفاصيل المشروع المقدمة عبر نماذج التواصل أو عروض الأسعار.</p>
                <h3 style="margin:24px 0 10px;">كيف نستخدمه</h3>
                <p style="line-height:1.8;margin-bottom:16px;">تُستخدم بياناتك فقط للرد على استفساراتك، وحيث يتم الموافقة، لإرسال تحديثات هندسية ذات صلة. لا تُباع لأطراف ثالثة قط.</p>
                <h3 style="margin:24px 0 10px;">تواصل معنا</h3>
                <p style="line-height:1.8;">لأي استفسارات تتعلق بالخصوصية، يُرجى مراسلتنا على <a href="mailto:sales@iconicmach.com" style="color:var(--primary-blue);">sales@iconicmach.com</a>.</p>
            </div>
        </div>
    </section>'''),

    'terms.html': ('الشروط والأحكام', 'الشروط والأحكام الخاصة بشركة آيكونيك ماشين الهندسية.', '''
    <section id="main-content" class="section">
        <div class="container" style="max-width:800px;">
            <div class="card bg-main" style="padding:40px;box-shadow:var(--shadow-sm);">
                <h2 class="text-primary" style="margin-bottom:20px;">الشروط والأحكام</h2>
                <p style="line-height:1.8;margin-bottom:16px;">بالتعامل مع آيكونيك ماشين الهندسية للمنتجات أو الخدمات، فإنك توافق على الشروط التالية التي تحكم استخدام موقعنا وعروض الأسعار والعقود والتركيبات.</p>
                <h3 style="margin:24px 0 10px;">عروض الأسعار</h3>
                <p style="line-height:1.8;margin-bottom:16px;">جميع عروض الأسعار سارية لمدة 30 يوماً من تاريخ الإصدار ما لم يُذكر خلاف ذلك. الأسعار عرضة للتغيير بسبب تذبذب أسعار المواد والعملات.</p>
                <h3 style="margin:24px 0 10px;">الضمانات</h3>
                <p style="line-height:1.8;margin-bottom:16px;">تحمل جميع الأنظمة المصنوعة ضماناً لمدة 12 شهراً ضد عيوب المواد والتصنيع من تاريخ التشغيل.</p>
                <h3 style="margin:24px 0 10px;">الملكية الفكرية</h3>
                <p style="line-height:1.8;">جميع الرسومات الهندسية والتصاميم والوثائق التي ينتجها تبقى ملكاً فكرياً لنا ما لم يتم نقلها صراحةً كتابياً.</p>
            </div>
        </div>
    </section>'''),
}

template = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | آيكونيك ماشين الهندسية</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{domain}/ar/{filename}">
    <meta property="og:title" content="{title} | آيكونيك ماشين الهندسية">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{domain}/ar/{filename}">
    <meta property="og:type" content="website">
    <link rel="icon" type="image/png" href="../assets/images/favicon.png">
    <link rel="stylesheet" href="../assets/css/variables.css">
    <link rel="stylesheet" href="../assets/css/reset.css">
    <link rel="stylesheet" href="../assets/css/layout.css">
    <link rel="stylesheet" href="../assets/css/components.css">
    <link rel="stylesheet" href="../assets/css/animations.css">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        @keyframes bounceDown {{
            0%,100% {{ transform: translateX(-50%) translateY(0); opacity:0.7; }}
            50% {{ transform: translateX(-50%) translateY(10px); opacity:1; }}
        }}
        details summary::-webkit-details-marker {{ display:none; }}
    </style>
</head>
<body>
    <div class="top-bar">
        <div class="container" style="display:flex; justify-content:space-between; align-items:center; flex-direction:row-reverse;">
            <div class="top-bar-contact">
                <a href="https://wa.me/20108472717" target="_blank" rel="noopener" style="margin-left:15px;" dir="ltr">
                    <span>📱</span> +20 108 472 717
                </a>
                <a href="mailto:sales@iconicmach.com" style="color:var(--text-muted); text-decoration:none; font-size:0.9rem;">
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
                <img src="../assets/images/iconicmach.png" alt="آيكونيك ماشين الهندسية">
            </a>
            <nav class="main-nav">
                <ul class="nav-links">
                    <li><a href="index.html">الرئيسية</a></li>
                    <li><a href="about.html">من نحن</a></li>
                    <li><a href="production-lines.html">خطوط الإنتاج</a></li>
                    <li><a href="conveyor-systems.html">السيور الناقلة</a></li>
                    <li><a href="services.html">خدماتنا</a></li>
                    <li><a href="contact.html">اتصل بنا</a></li>
                </ul>
            </nav>
            <div class="header-actions">
                <button id="theme-toggle" class="icon-btn">🌙</button>
                <a href="../en/{filename}" id="lang-toggle" class="badge">English</a>
                <div class="menu-toggle"><span></span><span></span><span></span></div>
            </div>
        </div>
    </header>

    <main>
        {hero}
        {content}
    </main>

    {footer}
    <script src="../assets/js/main.js"></script>
    <script src="../assets/js/animations.js"></script>
</body>
</html>"""

os.makedirs('ar', exist_ok=True)
for filename, (title, description, content) in pages.items():
    hero = make_hero(filename)
    filepath = os.path.join('ar', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(template.format(
            title=title,
            description=description,
            domain=domain,
            filename=filename,
            content=content,
            hero=hero,
            footer=FOOTER
        ))
print("Arabic pages generated successfully.")
