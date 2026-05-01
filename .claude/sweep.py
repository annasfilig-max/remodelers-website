"""Remodelers site chrome sweep — same shape as HVAC sweep, but:
 - Repo: annasfilig-max/remodelers-website (jsDelivr base)
 - Tagline: 'Kitchen & Bath Remodels' instead of 'Heating · Cooling · Air Quality'
 - Image extensions: .png not .jpg
 - Service nav anchors: kitchen, bath, cabinets, counters, tile, design
"""
import re, os

BASE = os.path.join(os.path.dirname(__file__), '..')
CDN = 'https://cdn.jsdelivr.net/gh/annasfilig-max/remodelers-website@main'

PROMO = '''<!-- ================= JT MARKETING PROMO BANNER ================= -->
<div id="jtm-promo-banner" role="note" aria-label="Preview by JT Marketing">
  <span class="jtm-promo-inner">
    <svg class="jtm-star" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l2.6 6.3L21 9l-5 4.4L17.4 20 12 16.7 6.6 20 8 13.4 3 9l6.4-.7L12 2z"/></svg>
    <span class="jtm-promo-text">This site could be yours.</span>
    <span class="jtm-promo-sep" aria-hidden="true"></span>
    <span class="jtm-promo-credit">Built by <b>JT Marketing</b></span>
  </span>
  <button type="button" class="jtm-close" aria-label="Dismiss" onclick="this.parentElement.style.display='none'">&times;</button>
</div>

'''

def header_block(current_page):
    nav_items = [
        ('index.html', 'Home', 'home'),
        ('about.html', 'About', 'about'),
        ('services.html', 'Services', 'services'),
        ('service-areas.html', 'Service Areas', 'service-areas'),
        ('gallery.html', 'Portfolio', 'gallery'),
        ('testimonials.html', 'Reviews', 'testimonials'),
        ('faq.html', 'FAQ', 'faq'),
        ('contact.html', 'Contact', 'contact'),
    ]
    lis = []
    for href, label, key in nav_items:
        cur = ' aria-current="page"' if key == current_page else ''
        lis.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    nav_main = ''.join(lis)
    nav_mobile = ''.join(f'<li><a href="{href}">{label}</a></li>' for href, label, _ in nav_items)
    return f'''<!-- ================= HEADER ================= -->
<header class="site-header">
  <div class="container header-inner">
    <a href="index.html" class="logo" aria-label="[Your Company Name] home">
      <span class="logo-name">[Your Company Name]</span>
      <span class="logo-tag">Kitchen &middot; Bath &middot; Whole-Home Remodels</span>
    </a>
    <nav class="nav-main" aria-label="Primary">
      <ul>{nav_main}</ul>
    </nav>
    <div class="header-cta">
      <a href="tel:[Phone Number]" class="header-phone">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        [Phone Number]
      </a>
      <a href="quote.html" class="btn btn-primary">Free Quote</a>
    </div>
    <button class="hamburger" data-menu-toggle aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
  </div>
</header>

<!-- ================= MOBILE MENU ================= -->
<div class="mobile-menu" id="mobile-menu" data-mobile-menu aria-hidden="true">
  <div class="mobile-menu-head">
    <span class="logo-name">[Your Company Name]</span>
    <button class="hamburger" data-menu-close aria-label="Close menu">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
  </div>
  <nav aria-label="Mobile primary"><ul>{nav_mobile}</ul></nav>
  <div class="mobile-menu-footer">
    <a href="tel:[Phone Number]" class="btn btn-outline-white">Call [Phone Number]</a>
    <a href="quote.html" class="btn btn-primary">Free Quote</a>
  </div>
</div>

'''

FOOTER = '''<!-- ================= FOOTER ================= -->
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="logo-name">[Your Company Name]</div>
        <div class="logo-tag">Kitchen &middot; Bath &middot; Whole-Home Remodels</div>
        <p style="margin-top:1rem;color:rgba(255,255,255,0.7);max-width:36ch;">Family-owned remodeling company serving [Service Region] since [Year Founded]. Honest quotes, clean work, and transformations that hold their value.</p>
        <p style="font-family:var(--font-mono);font-size:0.6875rem;letter-spacing:0.1em;text-transform:uppercase;color:rgba(255,255,255,0.5);margin-top:1rem;">Lic #[License #] &middot; Insured &middot; Bonded</p>
      </div>
      <div>
        <h4>Site</h4>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="services.html">Services</a></li>
          <li><a href="service-areas.html">Service Areas</a></li>
          <li><a href="gallery.html">Portfolio</a></li>
          <li><a href="testimonials.html">Reviews</a></li>
          <li><a href="faq.html">FAQ</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="services.html#kitchen">Kitchen Remodels</a></li>
          <li><a href="services.html#bath">Bath Remodels</a></li>
          <li><a href="services.html#cabinets">Cabinets &amp; Refacing</a></li>
          <li><a href="services.html#counters">Countertops</a></li>
          <li><a href="services.html#tile">Custom Tile</a></li>
          <li><a href="services.html#design">Design Consultation</a></li>
        </ul>
      </div>
      <div>
        <h4>Reach Us</h4>
        <ul>
          <li><a href="tel:[Phone Number]" style="font-family:var(--font-heading);font-weight:700;color:#fff;font-size:1.125rem;">[Phone Number]</a></li>
          <li><a href="mailto:[Email]">[Email]</a></li>
          <li>[Street Address]<br>[City, State ZIP]</li>
          <li style="margin-top:0.75rem;font-family:var(--font-mono);font-size:0.6875rem;letter-spacing:0.08em;text-transform:uppercase;color:rgba(255,255,255,0.6);">Mon&ndash;Fri 8a&ndash;6p &middot; Sat By Appt<br>Free In-Home Design Visits</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="social-row">
        <a href="#" aria-label="Facebook"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></a>
        <a href="#" aria-label="Instagram"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg></a>
        <a href="#" aria-label="Houzz"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M16 8v8h-3v-5H11v5H8V4h3v4h5z"/></svg></a>
      </div>
      <div>&copy; <span data-year>2026</span> [Your Company Name] &middot; <a href="privacy.html">Privacy</a> &middot; <a href="terms.html">Terms</a></div>
    </div>
  </div>
</footer>
'''

PAGE_KEYS = {
    'index.html': 'home', 'about.html': 'about', 'services.html': 'services',
    'service-areas.html': 'service-areas', 'gallery.html': 'gallery',
    'testimonials.html': 'testimonials', 'faq.html': 'faq', 'contact.html': 'contact',
    'quote.html': 'contact', 'privacy.html': '', 'terms.html': '', '404.html': '',
}

def sweep(filename):
    path = os.path.join(BASE, filename)
    with open(path, 'r', encoding='utf-8') as f: html = f.read()
    key = PAGE_KEYS.get(filename, '')

    # Drop legacy Google Fonts links
    html = re.sub(
        r'<link rel="preconnect" href="https://fonts\.googleapis\.com"[^>]*>\s*<link rel="preconnect" href="https://fonts\.gstatic\.com"[^>]*>\s*<link href="https://fonts\.googleapis\.com/css2[^"]*"[^>]*>\s*',
        '', html, flags=re.S)
    # Skip-link
    html = re.sub(r'<a href="#main" class="skip-link">[^<]*</a>\s*', '', html)

    # Convert relative asset paths to jsDelivr absolute
    html = re.sub(
        r'<link rel="stylesheet" href="assets/css/styles\.css">',
        f'<link rel="stylesheet" href="{CDN}/assets/css/styles.css?v=1">', html)
    html = re.sub(
        r'<script src="assets/js/main\.js" defer></script>',
        f'<script src="{CDN}/assets/js/main.js?v=1" defer></script>', html)
    html = re.sub(
        r'<link rel="icon" type="image/svg\+xml" href="assets/favicon\.svg">',
        f'<link rel="icon" type="image/svg+xml" href="{CDN}/assets/favicon.svg">', html)
    html = re.sub(r"url\('assets/images/([^']+)'\)", rf"url('{CDN}/assets/images/\1')", html)
    html = re.sub(r'src="assets/images/([^"]+)"', rf'src="{CDN}/assets/images/\1"', html)

    # Replace header through end of mobile menu
    new_chrome = PROMO + header_block(key)
    html = re.sub(
        r'<header class="site-header">.*?</div>\s*\n\s*(?=<main)',
        new_chrome, html, count=1, flags=re.S)

    # Replace footer
    html = re.sub(
        r'<footer class="site-footer">.*?</footer>',
        FOOTER.rstrip(), html, count=1, flags=re.S)

    # Nuke blog refs
    html = re.sub(r'<li><a href="blog\.html">Blog</a></li>\s*', '', html)
    html = re.sub(r'<li><a href="blog/post-\d+\.html"[^>]*>[^<]*</a></li>\s*', '', html)
    html = re.sub(r'href="blog\.html"', 'href="services.html"', html)

    with open(path, 'w', encoding='utf-8', newline='\n') as f: f.write(html)

if __name__ == '__main__':
    files = [f for f in os.listdir(BASE) if f.endswith('.html')]
    for f in sorted(files):
        sweep(f); print(f'  swept {f}')
    print(f'\n{len(files)} files swept.')
