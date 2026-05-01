"""Clone the HVAC site verbatim into remodelers-website, then swap:
 - jsDelivr repo URL: hvac-website -> remodelers-website
 - Image extensions: .jpg -> .png
 - HVAC services (AC, furnace, etc.) -> kitchen/bath remodel services
 - HVAC tagline 'Heating · Cooling · Air Quality' -> 'Kitchen · Bath · Whole-Home Remodels'
 - HVAC-specific copy -> remodeler copy
"""
import os, re, shutil

HVAC = os.path.expanduser('~/Downloads/Claude/hvac-website')
REM  = os.path.expanduser('~/Downloads/Claude/remodelers-website')

PAGES = ['index.html','about.html','services.html','service-areas.html',
         'gallery.html','testimonials.html','faq.html','contact.html',
         'quote.html','privacy.html','terms.html','404.html']

# Service slug remapping for hash anchors and content
SERVICE_SWAPS_HASH = [
    ('#ac-repair',       '#kitchen'),
    ('#heating-repair',  '#bath'),
    ('#ac-install',      '#cabinets'),
    ('#furnace-install', '#counters'),
    ('#air-quality',     '#tile'),
    ('#maintenance',     '#design'),
]

# Service NAMES (must be ordered specific->general so longer phrases match first)
SERVICE_NAME_SWAPS = [
    ('Furnace &amp; Heat Pump',   'Countertops &amp; Surfaces'),
    ('Indoor Air &amp; Ducts',     'Custom Tile &amp; Stone'),
    ('Furnace Repair',             'Bath Remodels'),
    ('AC Installation',            'Cabinets &amp; Refacing'),
    ('Maintenance Plans',          'Design Consultation'),
    ('AC Repair',                  'Kitchen Remodels'),
]

# Section subtitles in homepage svc cards
SVC_NUM_SWAPS = [
    ('01 / Cooling',    '01 / Kitchen'),
    ('02 / Heating',    '02 / Bath'),
    ('03 / Install',    '03 / Cabinets'),
    ('04 / Install',    '04 / Counters'),
    ('05 / Air Quality','05 / Tile'),
    ('06 / Plans',      '06 / Design'),
]

# Generic textual swaps — HVAC lingo -> remodeler lingo
TEXT_SWAPS = [
    # tagline + tone
    ('Heating &middot; Cooling &middot; Air Quality',
     'Kitchen &middot; Bath &middot; Whole-Home Remodels'),
    ('HVAC Services in [City, State]', 'Remodeling in [City, State]'),
    ('HVAC Services in [City, State ZIP]', 'Remodeling in [City, State ZIP]'),
    ('local HVAC experts', 'design-build remodelers'),
    ('HVAC Done Right', 'Remodels Done Right'),
    ('HVAC company', 'remodeling company'),
    ('Heating, cooling, and indoor air',
     'Kitchens, baths, and whole-home renovations'),

    # hero copy
    ('Heat, Cool &amp; <em>Comfort</em> &mdash; Done Right.',
     'Kitchens &amp; Baths &mdash; <em>Done Right.</em>'),
    ("When the AC quits at 2 a.m. or the furnace gives up on the coldest night of the year, you don't need a sales pitch. You need someone who shows up, fixes it, and stands behind the work.",
     "When you've waited years for the right kitchen or bath, you don't want a sales pitch. You want a crew that shows up clean, builds it right, and stands behind the work for the life of the home."),

    # trust labels (hero)
    ('24/7 Emergency', '15-Yr Workmanship'),
    ('NATE-Certified', 'NKBA Members'),

    # stat labels
    ('Years On The Job', 'Years Building'),
    ('Homes Serviced', 'Rooms Remodeled'),
    ('Of 50 Avg Rating', 'Of 50 Avg Rating'),

    # marquee items (HVAC -> remodel)
    ('24/7 Emergency Service', 'In-Home Design Visits'),
    ('NATE-Certified Technicians', 'NKBA-Member Designers'),
    ('Same-Day Service', 'On-Time Completion'),

    # service section header
    ('What We Do.<br>How We Do It Differently.',
     'Kitchens &amp; Baths.<br>Built To Be Lived In.'),
    ('6 Core Services', '6 Core Services'),

    # service card teasers
    ('Same-day diagnosis on every brand. Honest call on repair vs. replace &mdash; no upsell scripts.',
     'Full-gut to sleek refresh &mdash; cabinets, counters, tile, and lighting handled by one crew, one timeline.'),
    ("No heat at 2 a.m.? We're up. Gas, electric, oil &mdash; fixed right, parts in the truck.",
     'Spa-grade primary baths to clean second-bath refreshes. Tile, plumbing, vanities, glass &mdash; done in-house.'),
    ('Right-sized systems, clean install, and a manufacturer warranty we actually honor.',
     'Custom, semi-custom, or refacing. We size, design, and install &mdash; with warranties we actually honor.'),
    ("High-efficiency systems sized to your home &mdash; not what's on the truck this week.",
     'Quartz, granite, marble, butcher block. Templated, fabricated, and installed without the markup games.'),
    ('Filtration, humidifiers, UV, and full duct cleaning. The stuff that actually moves the needle.',
     'Backsplashes, shower walls, floors. Hand-laid by tile specialists &mdash; not the lowest-bid sub.'),
    ('Two visits a year, priority dispatch, no overtime fees. Cancel anytime &mdash; that\'s the deal.',
     '3D visualization, material selection, and an honest budget &mdash; before any demo starts.'),

    # about section
    ('A Crew That<br>Treats Your Home<br>Like Their Own.',
     'A Crew That<br>Treats Your Home<br>Like Their Own.'),
    ("We're a family-owned HVAC company built on the idea that homeowners shouldn't have to be afraid of contractors.",
     "We're a family-owned design-build remodeler built on the idea that homeowners shouldn't have to be afraid of contractors."),

    # process
    ('From Call To Comfort', 'From Sketch To Reveal'),
    ('Diagnose', 'Design'),
    ('We inspect, explain what we find, and quote a flat rate before any work begins.',
     'We measure, design in 3D, and lock in materials &mdash; with a flat-rate quote before demo.'),
    ('Fix It Right', 'Build It Right'),
    ("Quality parts, code-correct work, and we don't leave until you're comfortable again.",
     "Code-correct framing, plumbing, electrical, finishing &mdash; we don't leave until it's reveal-ready."),
    ('Stand Behind It', 'Reveal &amp; Warranty'),
    ('Workmanship guaranteed. If something\'s not right, one call gets us back out &mdash; no charge.',
     '15-year workmanship warranty. One call brings us back if anything settles wrong &mdash; no charge.'),

    # CTA
    ('System Down?<br>We&#39;re On The Way.',
     'Ready To Remodel?<br>Let\'s Sketch It.'),
    ('System Down?<br>We\'re On The Way.',
     'Ready To Remodel?<br>Let\'s Sketch It.'),
    ('24/7 emergency dispatch across [Service Region]. Most calls answered in under 60 seconds. Most homes back up and running same day.',
     'Free in-home design visits across [Service Region]. Most quotes in under 5 days. Most kitchens done in 4&ndash;6 weeks.'),
    ('System Down', "Let's Sketch It"),

    # services page
    ('Services<br><em style="color:var(--orange);font-style:normal;">Done Right.</em>',
     'Services<br><em style="color:var(--orange);font-style:normal;">Done Right.</em>'),
    ('Six core services. One standard. Flat-rate pricing, clean work, and a workmanship guarantee on every job we do.',
     'Six core services. One standard. Flat-rate pricing, clean work, and a 15-year workmanship guarantee on every job.'),

    # quote/contact form options
    ('AC not cooling',                   'Kitchen remodel'),
    ('Furnace not heating',              'Bath remodel'),
    ('New AC install',                   'Cabinets / refacing'),
    ('New furnace / heat pump',          'Countertops / surfaces'),
    ('Indoor air quality',               'Custom tile work'),
    ('Maintenance plan',                 'Design consultation'),
    ('Emergency &mdash; system down now', 'Whole-home renovation'),

    # footer hours
    ('Mon&ndash;Fri 7a&ndash;7p &middot; Sat 8a&ndash;4p<br>24/7 Emergency Dispatch',
     'Mon&ndash;Fri 8a&ndash;6p &middot; Sat By Appt<br>Free In-Home Design Visits'),

    # services anchor in services page deep section heads
    ('AC Repair &mdash;<br>Same-Day, Every Brand.', 'Kitchen Remodels &mdash;<br>Designed &amp; Built In-House.'),
    ('Diagnosis &middot; Repair &middot; Recharge', 'Design &middot; Demo &middot; Build'),
    ('Furnace Repair &mdash;<br>Up When You&#39;re Not.', 'Bath Remodels &mdash;<br>From Sleek To Spa.'),
    ('Furnace Repair &mdash;<br>Up When You\'re Not.', 'Bath Remodels &mdash;<br>From Sleek To Spa.'),
    ('Gas &middot; Electric &middot; Oil', 'Primary &middot; Guest &middot; Powder'),
    ('AC Installation &mdash;<br>Sized For Your Home.', 'Cabinets &amp; Refacing &mdash;<br>Tight Joinery, Real Wood.'),
    ('Manual J Load Calc &middot; 10-Yr Warranty', 'Custom &middot; Semi-Custom &middot; Refacing'),
    ('Furnace &amp; Heat Pump<br>Installation.', 'Countertops &amp;<br>Surface Materials.'),
    ('High-Efficiency &middot; Rebate-Ready', 'Quartz &middot; Granite &middot; Marble'),
    ('Indoor Air &amp; Ducts &mdash;<br>Cleaner, Quieter, Drier.', 'Custom Tile &amp; Stone<br>&mdash; Hand-Laid.'),
    ('Filtration &middot; Humidity &middot; UV', 'Showers &middot; Backsplashes &middot; Floors'),
    ('Maintenance Plans &mdash;<br>Set It &amp; Forget It.', 'Design Consultation &mdash;<br>Before Any Demo Starts.'),
    ('Two Visits A Year &middot; Priority Dispatch', '3D Visualization &middot; Material Selection'),

    # about page bits
    ('NATE-Certified Techs', 'NKBA Designers'),
    ('Master HVAC license #[XXX].', 'Master Builder license #[XXX].'),
    ('15 years on the trucks. Specializes in heat pumps and tricky diagnostics.',
     '20 years on the saw. Specializes in custom cabinetry and built-ins.'),
    ('Runs dispatch &mdash; the reason your call gets answered in under 60 seconds.',
     'Runs design &mdash; the reason every project lands on budget and on calendar.'),
    ('NATE<br>', 'NKBA<br>'),
    ('CERTIFIED', 'MEMBER'),
    ('EPA 608<br>', 'NARI<br>'),
    ('UNIVERSAL', 'MEMBER'),
    ('ENERGY STAR<br>', 'EPA RRP<br>'),
    ('PARTNER', 'CERTIFIED'),
    ('ACCA<br>', 'IBHS<br>'),

    # generic everywhere
    ('HVAC', 'Remodeling'),
    ('hvac', 'remodeling'),
]

def transform(html):
    # 1) Repo URL
    html = html.replace(
        'cdn.jsdelivr.net/gh/annasfilig-max/hvac-website',
        'cdn.jsdelivr.net/gh/annasfilig-max/remodelers-website')
    # 2) Image extension .jpg -> .png (only inside the jsDelivr image paths)
    html = re.sub(
        r'(cdn\.jsdelivr\.net/gh/annasfilig-max/remodelers-website@main/assets/images/[a-zA-Z0-9_-]+)\.jpg',
        r'\1.png', html)
    # 3) Service hash anchors
    for old, new in SERVICE_SWAPS_HASH:
        html = html.replace(old, new)
    # 4) Service section numbers
    for old, new in SVC_NUM_SWAPS:
        html = html.replace(old, new)
    # 5) Service names (longer first)
    for old, new in SERVICE_NAME_SWAPS:
        html = html.replace(old, new)
    # 6) All other text swaps
    for old, new in TEXT_SWAPS:
        html = html.replace(old, new)
    return html

if __name__ == '__main__':
    # Wipe existing remodelers .html files (we own the rebuild)
    for f in os.listdir(REM):
        if f.endswith('.html') and os.path.isfile(os.path.join(REM, f)):
            os.remove(os.path.join(REM, f))

    # Copy each HVAC .html, transform, write to remodelers
    for p in PAGES:
        src = os.path.join(HVAC, p)
        dst = os.path.join(REM, p)
        with open(src, encoding='utf-8') as fh: html = fh.read()
        html = transform(html)
        with open(dst, 'w', encoding='utf-8', newline='\n') as fh: fh.write(html)
        print(f'  built {p:25s}  {len(html):6d}b')

    # Copy CSS as-is from HVAC (already done earlier but ensure latest)
    shutil.copy(os.path.join(HVAC, 'assets/css/styles.css'),
                os.path.join(REM,  'assets/css/styles.css'))
    print('\n  copied styles.css')

    # Sitemap
    with open(os.path.join(REM, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
''' + ''.join(
        f'  <url><loc>[https://yourdomain.com]/{p}</loc><lastmod>2026-05-01</lastmod><changefreq>monthly</changefreq><priority>{pri}</priority></url>\n'
        for p, pri in [('index.html','1.0'),('about.html','0.8'),('services.html','0.9'),
                       ('service-areas.html','0.8'),('gallery.html','0.7'),
                       ('testimonials.html','0.7'),('faq.html','0.7'),
                       ('contact.html','0.9'),('quote.html','0.9'),
                       ('privacy.html','0.3'),('terms.html','0.3')]
    ) + '</urlset>\n')
    print('  wrote sitemap.xml')
    print(f'\nDone. {len(PAGES)} pages built.')
