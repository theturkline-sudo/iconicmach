import os

domain = "https://iconicmach.com"

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
    media_type, src, title, subtitle = page_heroes.get(filename, ('image', '../assets/images/industrial-process-1.jpeg', 'Iconic Mach Engineering', ''))
    if filename == 'index.html':
        return f'''
    <section class="page-hero" style="position:relative; height:100vh; min-height:600px; display:flex; align-items:center; justify-content:center; text-align:center; overflow:hidden;">
        <video autoplay loop muted playsinline src="{src}"
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
    <footer class="site-footer" style="background:#061226; color:#c9d8ec; padding: 64px 0 0;">
        <div class="container">
            <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:48px; padding-bottom:48px; border-bottom:1px solid rgba(255,255,255,0.08);">
                <!-- Brand -->
                <div>
                    <img src="../assets/images/iconicmach.png" alt="Iconic Mach Engineering" style="height:75px; margin-bottom:16px; filter:brightness(10);">
                    <p style="font-size:0.92rem; line-height:1.8; opacity:0.7; max-width:240px;">Designing and manufacturing world-class production lines and conveyor systems across Egypt and the GCC.</p>
                    <div style="display:flex; gap:12px; margin-top:20px;">
                        <a href="https://www.facebook.com/profile.php?id=61590272801593" target="_blank" aria-label="Facebook" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#c9d8ec;text-decoration:none;font-size:0.85rem;transition:background .2s;" onmouseover="this.style.background='#1877f2'" onmouseout="this.style.background='rgba(255,255,255,0.08)'">f</a>
                        <a href="https://www.linkedin.com/in/mahmoud-turk-82bbb8412/" target="_blank" aria-label="LinkedIn" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#c9d8ec;text-decoration:none;font-size:0.85rem;transition:background .2s;" onmouseover="this.style.background='#0077b5'" onmouseout="this.style.background='rgba(255,255,255,0.08)'">in</a>
                        <a href="https://wa.me/20108472717" aria-label="WhatsApp" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#c9d8ec;text-decoration:none;font-size:0.85rem;transition:background .2s;" onmouseover="this.style.background='#25d366'" onmouseout="this.style.background='rgba(255,255,255,0.08)'">W</a>
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
                        <li style="display:flex; gap:10px; align-items:flex-start;"><span style="margin-top:2px;">📍</span><span style="opacity:0.8;">Shams Mall, 10th Of Ramadan,<br>Al Sharqiya, Egypt</span></li>
                        <li style="display:flex; gap:10px; align-items:center;"><span>📱</span><a href="https://wa.me/20108472717" style="color:#4adeae; text-decoration:none;">+20 108 472 717</a></li>
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
                            <div><strong>Address</strong><br><span style="color:var(--text-muted);">Shams Mall, 10th Of Ramadan, Al Sharqiya, Egypt</span></div>
                        </div>
                        <div style="display:flex; align-items:flex-start; gap:16px;">
                            <div style="font-size:1.6rem; line-height:1;">📱</div>
                            <div><strong>Phone / WhatsApp</strong><br><a href="https://wa.me/20108472717" style="color:var(--primary-blue); text-decoration:none; font-weight:600;">+20 108 472 717</a></div>
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
                            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d13651.989047248354!2d31.7371987!3d30.301314!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xa9efd409ec5898fb!2z2YXZiNmEINi02YXYsw!5e0!3m2!1sen!2seg!4v1717320000000!5m2!1sen!2seg"
                            width="100%" height="300" style="border:0; display:block;" allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade">
                        </iframe>
                    </div>
                </div>
                <div>
                    <form action="#" method="POST" class="card bg-main" style="display:flex; flex-direction:column; gap:18px; padding:40px; box-shadow:var(--shadow-md);">
                        <h3 style="margin-bottom:8px;">Send us a Message</h3>
                        <input type="text" placeholder="Your Name" required style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; font-size:0.95rem; background:var(--bg-alt);">
                        <input type="email" placeholder="Your Email" required style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; font-size:0.95rem; background:var(--bg-alt);">
                        <input type="tel" placeholder="Phone Number" style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; font-size:0.95rem; background:var(--bg-alt);">
                        <input type="text" placeholder="Subject" required style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; font-size:0.95rem; background:var(--bg-alt);">
                        <textarea placeholder="Tell us about your project..." rows="5" required style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; font-size:0.95rem; background:var(--bg-alt); resize:vertical;"></textarea>
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
            <form action="#" method="POST" class="card bg-main" style="display:flex; flex-direction:column; gap:18px; padding:40px; box-shadow:var(--shadow-md);">
                <input type="text" placeholder="Full Name" required style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; background:var(--bg-alt);">
                <input type="text" placeholder="Company Name" style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; background:var(--bg-alt);">
                <input type="email" placeholder="Email Address" required style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; background:var(--bg-alt);">
                <input type="tel" placeholder="Phone / WhatsApp" style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; background:var(--bg-alt);">
                <select style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; background:var(--bg-alt);">
                    <option value="">Product / Service Required</option>
                    <option>Production Line</option>
                    <option>Conveyor System</option>
                    <option>Maintenance Contract</option>
                    <option>Automation Upgrade</option>
                    <option>Spare Parts</option>
                    <option>Other</option>
                </select>
                <textarea placeholder="Describe your project requirements..." rows="6" required style="padding:13px 16px; border:1px solid var(--border-color); border-radius:var(--radius-sm); font-family:inherit; background:var(--bg-alt); resize:vertical;"></textarea>
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
                    <a href="https://wa.me/20108472717" class="btn btn-primary" style="padding:14px 28px; text-decoration:none;">WhatsApp Support Now</a>
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

template = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Iconic Mach Engineering</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{domain}/en/{filename}">
    <meta property="og:title" content="{title} | Iconic Mach Engineering">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{domain}/en/{filename}">
    <meta property="og:type" content="website">
    <link rel="icon" type="image/png" href="../assets/images/favicon.png">
    <link rel="stylesheet" href="../assets/css/variables.css">
    <link rel="stylesheet" href="../assets/css/reset.css">
    <link rel="stylesheet" href="../assets/css/layout.css">
    <link rel="stylesheet" href="../assets/css/components.css">
    <link rel="stylesheet" href="../assets/css/animations.css">
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
    <div class="top-bar">
        <div class="container" style="display: flex; justify-content: space-between; align-items: center;">
            <div class="top-bar-contact">
                <a href="https://wa.me/20108472717" target="_blank" rel="noopener" style="margin-right: 15px;">
                    <span>📱</span> +20 108 472 717
                </a>
                <a href="mailto:sales@iconicmach.com" style="color: var(--text-muted); text-decoration: none; font-size: 0.9rem;">
                    <span>✉️</span> sales@iconicmach.com
                </a>
            </div>
            <div class="top-bar-social">
                <a href="https://www.facebook.com/profile.php?id=61590272801593" target="_blank" aria-label="Facebook">Facebook</a>
                <a href="https://www.linkedin.com/in/mahmoud-turk-82bbb8412/" target="_blank" aria-label="LinkedIn">LinkedIn</a>
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
                <a href="../ar/{filename}" id="lang-toggle" class="badge">عربي</a>
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

os.makedirs('en', exist_ok=True)
for filename, (title, description, content) in pages.items():
    hero = make_hero(filename)
    filepath = os.path.join('en', filename)
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
print("English pages generated successfully.")
