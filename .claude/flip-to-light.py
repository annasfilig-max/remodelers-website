"""Flip remodelers from dark+navy to light+red (JC Remodeling DFW style)."""
import os, re

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open('assets/css/styles.css', encoding='utf-8') as f:
    css = f.read()

swaps = [
    ('REMODELERS — Dark Premium + Brass Accent',
     'REMODELERS — Light Premium + Red Accent'),
    # Core color tokens
    ('--bg:          #0a0a0a;', '--bg:          #ffffff;'),
    ('--bg-2:        #121212;', '--bg-2:        #f7f7f7;'),
    ('--bg-card:     #161616;', '--bg-card:     #ffffff;'),
    ('--bg-elev:     #1c1c1c;', '--bg-elev:     #fafafa;'),
    ('--ink:         #fafafa;', '--ink:         #0a0a0a;'),
    ('--ink-muted:   #a3a3a3;', '--ink-muted:   #525252;'),
    ('--ink-faint:   #6b6b6b;', '--ink-faint:   #8a8a8a;'),
    ('--line:        #262626;', '--line:        #e5e5e5;'),
    ('--line-soft:   #1f1f1f;', '--line-soft:   #f0f0f0;'),
    # Accent: navy -> red
    ('--brass:        #4870A8', '--brass:        #dc2626'),
    ('--brass-bright: #6090C8', '--brass-bright: #ef4444'),
    ('--brass-deep:   #2D4F7E', '--brass-deep:   #991b1b'),
    ('rgba(72, 112, 168, 0.5)',  'rgba(220, 38, 38, 0.4)'),
    ('rgba(72, 112, 168, 0.1)',  'rgba(220, 38, 38, 0.1)'),
    ('rgba(72, 112, 168, 0.45)', 'rgba(220, 38, 38, 0.4)'),
    ('rgba(72, 112, 168, 0.3)',  'rgba(220, 38, 38, 0.3)'),
    ('rgba(72, 112, 168, 0.04) 1px', 'rgba(220, 38, 38, 0.04) 1px'),
    ('rgba(96, 144, 200, 0.32)', 'rgba(239, 68, 68, 0.32)'),
    ('#9DC0E8', '#FBA8A8'),
    ('#4870A8', '#dc2626'),
    # GHL container overrides: dark -> light
    ('background: #0a0a0a !important;\n  background-color: #0a0a0a !important;\n  color: #a3a3a3 !important;',
     'background: #ffffff !important;\n  background-color: #ffffff !important;\n  color: #525252 !important;'),
    ('background: #121212 !important;\n  background-color: #121212 !important;',
     'background: #f7f7f7 !important;\n  background-color: #f7f7f7 !important;'),
    # cta-band & hero-split forced dark -> forced light
    ('.cta-band, .hero-split {\n  background: #0a0a0a !important;\n  background-color: #0a0a0a !important;\n}',
     '.cta-band, .hero-split {\n  background: #ffffff !important;\n  background-color: #ffffff !important;\n}'),
    # Nav, headings hardcoded white -> dark
    ('.nav-main a, .nav-main a:link, .nav-main a:visited {\n  color: #fafafa !important;\n}',
     '.nav-main a, .nav-main a:link, .nav-main a:visited {\n  color: #0a0a0a !important;\n}'),
    ('.logo-name { color: #fafafa !important; }',
     '.logo-name { color: #0a0a0a !important; }'),
    ('.header-phone { color: #fafafa !important; }',
     '.header-phone { color: #0a0a0a !important; }'),
    ('h1, h2, h3, h4 { color: #fafafa !important; }',
     'h1, h2, h3, h4 { color: #0a0a0a !important; }'),
    ('.svc-wide-body h3, .svc-card h3 { color: #fafafa !important; }',
     '.svc-wide-body h3 { color: #0a0a0a !important; } .svc-card h3 { color: #ffffff !important; }'),
    ('.svc-wide-body p { color: #a3a3a3 !important; }',
     '.svc-wide-body p { color: #525252 !important; }'),
    # Sticky header
    ('background: rgba(10, 10, 10, 0.85);',
     'background: rgba(255, 255, 255, 0.92);'),
    # Hero ::before overlay
    ('linear-gradient(180deg, rgba(10,10,10,0.55) 0%, rgba(10,10,10,0.85) 70%, var(--bg) 100%)',
     'linear-gradient(180deg, rgba(255,255,255,0.5) 0%, rgba(255,255,255,0.78) 70%, var(--bg) 100%)'),
    # btn-primary
    ('.btn-primary {\n  background: var(--brass);\n  color: var(--bg);\n  border-color: var(--brass);\n}',
     '.btn-primary {\n  background: var(--brass);\n  color: #ffffff;\n  border-color: var(--brass);\n}'),
    ('  color: var(--bg);\n  box-shadow: 0 8px 30px var(--brass-glow);',
     '  color: #ffffff;\n  box-shadow: 0 8px 30px var(--brass-glow);'),
    # btn-secondary hover
    ('.btn-secondary:hover {\n  background: var(--ink);\n  color: var(--bg);\n  border-color: var(--ink);\n}',
     '.btn-secondary:hover {\n  background: var(--ink);\n  color: #ffffff;\n  border-color: var(--ink);\n}'),
    # ::selection
    ('::selection { background: var(--brass); color: var(--bg); }',
     '::selection { background: var(--brass); color: #ffffff; }'),
]
for old, new in swaps:
    css = css.replace(old, new)

# Append light-theme polish overrides
extra = """
/* ============================================================
   LIGHT THEME POLISH (Naz JC-style) — keep footer dark, banner dark
   ============================================================ */
.site-footer {
  background: #0a0a0a !important;
  color: #a3a3a3 !important;
}
.site-footer .logo-name { color: #fafafa !important; }
.site-footer a { color: #a3a3a3 !important; }
.site-footer a:hover { color: var(--brass) !important; }
.site-footer .footer-bottom { color: #6b6b6b !important; }
.site-footer h4 { color: var(--brass) !important; }
.marquee {
  background: #f7f7f7 !important;
  color: #525252 !important;
  border-top: 1px solid #e5e5e5 !important;
  border-bottom: 1px solid #e5e5e5 !important;
}
.hero-split-text h1 { color: #0a0a0a !important; }
.hero-split-text .lead { color: #525252 !important; }
.hero-meta-num { color: #0a0a0a !important; }
.hero-meta-label { color: #8a8a8a !important; }
.hero-split-tag {
  background: rgba(255,255,255,0.92) !important;
  border-color: #e5e5e5 !important;
  color: #0a0a0a !important;
}
.hero-split-tag-label { color: #525252 !important; }
.svc-wide { background: #ffffff !important; border-color: #e5e5e5 !important; }
.svc-wide-body { color: #525252 !important; }
.testimonial { background: #ffffff !important; border-color: #e5e5e5 !important; }
.big-quote blockquote { color: #0a0a0a !important; }
.big-quote-meta strong { color: #0a0a0a !important; }
.cta-band--form .form {
  background: #ffffff !important;
  border-color: #e5e5e5 !important;
  box-shadow: 0 24px 60px rgba(0,0,0,0.08);
}
.cta-band h2 { color: #0a0a0a !important; }
.cta-band p { color: #525252 !important; }
.cta-direct-num { color: #0a0a0a !important; }
.form-group input,
.form-group select,
.form-group textarea {
  background: #ffffff !important;
  color: #0a0a0a !important;
  border-color: #e5e5e5 !important;
}
.form-group input::placeholder,
.form-group textarea::placeholder { color: #a3a3a3 !important; }
.step:hover { background: rgba(220, 38, 38, 0.04) !important; }
.stat-num { color: #0a0a0a !important; }
.about-strip { background: #f7f7f7 !important; }
.about-strip .col-body p { color: #525252 !important; }
.page-hero {
  background: #ffffff !important;
  border-bottom: 1px solid #e5e5e5 !important;
}
.page-hero h1 { color: #0a0a0a !important; }
.page-hero p { color: #525252 !important; }
.card { background: #ffffff !important; border-color: #e5e5e5 !important; }
.card:hover { box-shadow: 0 24px 60px rgba(0,0,0,0.1); }
.gallery-filters button {
  background: #ffffff !important;
  color: #525252 !important;
  border-color: #e5e5e5 !important;
}
.gallery-filters button.active,
.gallery-filters button:hover {
  background: var(--brass) !important;
  color: #ffffff !important;
  border-color: var(--brass) !important;
}
.gallery-item { background: #fafafa !important; border-color: #e5e5e5 !important; }
.city-grid { border-color: #e5e5e5 !important; }
.city-card {
  background: #ffffff !important;
  border-color: #e5e5e5 !important;
}
.city-card .name { color: #0a0a0a !important; }
.city-card .sub { color: #8a8a8a !important; }
.city-card:hover .name { color: #ffffff !important; }
.faq-item { border-color: #e5e5e5 !important; }
.faq-q { color: #0a0a0a !important; }
.faq-a { color: #525252 !important; }
.carousel-btn {
  background: #ffffff !important;
  border-color: #e5e5e5 !important;
  color: #0a0a0a !important;
}
.carousel-btn:hover { background: var(--brass) !important; color: #ffffff !important; border-color: var(--brass) !important; }
.hamburger {
  background: #ffffff !important;
  border-color: #e5e5e5 !important;
  color: #0a0a0a !important;
}
.mobile-menu { background: #ffffff !important; }
.mobile-menu nav a {
  color: #0a0a0a !important;
  border-bottom-color: #f0f0f0 !important;
}
.mobile-menu-head { border-bottom-color: #e5e5e5 !important; }
#jtm-promo-banner {
  background: #0a0a0a !important;
  color: #fafafa !important;
}
#jtm-promo-banner .jtm-promo-text { color: #fafafa !important; }
#jtm-promo-banner .jtm-promo-credit { color: #a3a3a3 !important; }
.section-alt { background: #f7f7f7 !important; }
.svc-wide:hover, .card:hover, .testimonial:hover, .team-card:hover {
  box-shadow:
    0 24px 60px rgba(0,0,0,0.12),
    0 0 0 1px var(--brass),
    0 0 24px rgba(220, 38, 38, 0.15) !important;
}
.hero-split-text h1 em,
.page-hero h1 em,
.cta-band h2 em {
  background: linear-gradient(110deg,
    var(--brass) 0%, var(--brass-bright) 35%,
    #FBA8A8 50%, var(--brass-bright) 65%, var(--brass) 100%) !important;
  background-size: 200% 100% !important;
  -webkit-background-clip: text !important;
  background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  color: transparent !important;
}
"""
css += extra

with open('assets/css/styles.css', 'w', encoding='utf-8', newline='\n') as f:
    f.write(css)
print('CSS flipped: dark -> light + navy -> red')

# Bump cache buster on all HTML
for f in os.listdir('.'):
    if not f.endswith('.html'): continue
    with open(f, encoding='utf-8') as fh: html = fh.read()
    html = re.sub(r'(styles\.css|main\.js)\?v=\d+', r'\1?v=30', html)
    with open(f, 'w', encoding='utf-8', newline='\n') as fh: fh.write(html)
print('Cache buster -> v=30')
