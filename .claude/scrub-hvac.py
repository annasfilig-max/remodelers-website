"""Scrub HVAC leftovers from remodelers site + swap brass to navy.
Run from repo root: python .claude/scrub-hvac.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# 1. Color swap in CSS
with open('assets/css/styles.css', encoding='utf-8') as f:
    css = f.read()
css = css.replace('--brass:        #C68F47', '--brass:        #4870A8')
css = css.replace('--brass-bright: #DAA561', '--brass-bright: #6090C8')
css = css.replace('--brass-deep:   #8B6532', '--brass-deep:   #2D4F7E')
css = css.replace('--brass-glow:   rgba(198, 143, 71, 0.45)', '--brass-glow:   rgba(72, 112, 168, 0.5)')
css = css.replace('--brass-subtle: rgba(198, 143, 71, 0.08)', '--brass-subtle: rgba(72, 112, 168, 0.1)')
with open('assets/css/styles.css', 'w', encoding='utf-8', newline='\n') as f:
    f.write(css)
print('CSS: brass -> navy #4870A8')

# 2. HVAC content fixes per file
fixes = {
    'gallery.html': [
        ('<button role="tab">Installs</button>',     '<button role="tab">Kitchens</button>'),
        ('<button role="tab">Repairs</button>',      '<button role="tab">Baths</button>'),
        ('<button role="tab">Air Quality</button>',  '<button role="tab">Cabinetry</button>'),
        ('Before and after comparison of AC unit replacement', 'Kitchen before and after — full remodel'),
        ('Close-up of clean refrigerant line-set installation along exterior wall', 'Clean tile line-up along shower wall'),
        ('Gas furnace and labeled ductwork in basement mechanical room', 'Custom cabinetry install with labeled hardware'),
        ('Modern ductless mini-split in bright living room', 'Modern primary bath with floating vanity'),
        ('Technician with flashlight inspecting attic ductwork', 'Designer reviewing tile selection on site'),
        ('Technician loading equipment from back of service van', 'Crew loading materials at job site'),
        ("Close-up of technician's hands on manifold gauge set", 'Close-up of installer hands on quartz template'),
        ('Completed outdoor AC installation with tools on site', 'Completed kitchen island with tools on site'),
        ('System warranty binder and maintenance record', 'Materials selection binder and project plans'),
        ('Technician inspecting filter on commercial rooftop unit', 'Designer measuring built-in shelving'),
        ('Fleet of Nano Banana HVAC service vans in neighborhood', 'Crew vans staged at a project home'),
        ('Company van convoy heading out for service calls', 'Project trucks heading to a job site'),
        ('Installs, upgrades, and repairs across', 'Kitchens, baths, and whole-home remodels across'),
    ],

    'services.html': [
        ('SERVICE 01 — AC REPAIR', 'SERVICE 01 — KITCHEN REMODELS'),
        ('SERVICE 02 — FURNACE REPAIR', 'SERVICE 02 — BATH REMODELS'),
        ('SERVICE 03 — AC INSTALLATION', 'SERVICE 03 — CABINETS'),
        ('SERVICE 04 — FURNACE INSTALL', 'SERVICE 04 — COUNTERTOPS'),
        ('SERVICE 05 — INDOOR AIR', 'SERVICE 05 — TILE'),
        ('SERVICE 06 — MAINTENANCE', 'SERVICE 06 — DESIGN'),
        ('Technician diagnosing residential AC condenser', 'Designer reviewing kitchen layout with homeowner'),
        ('Technician servicing residential gas furnace', 'Tile installer hand-laying primary bath shower wall'),
        ('New AC condenser installation on concrete pad', 'Custom cabinetry install in finished kitchen'),
        ('Technician installing high-efficiency gas furnace', 'Quartz countertop being templated and installed'),
        ('Whole-home air filtration and duct system', 'Custom backsplash and floor tile work in primary bath'),
        ('Technician performing seasonal HVAC tune-up', '3D rendering review during design consultation'),

        # Spec lines per service
        (' Full system diagnostic &amp; load test', ' Layout planning, demo, framing &amp; finishing'),
        (' Refrigerant leak check &amp; recharge (R-410A / R-32)', ' Custom cabinetry, counters &amp; lighting'),
        (' Capacitor, contactor, fan motor &amp; coil work', ' Backsplash, tile floors, hardwood &amp; LVP'),
        (' Honest repair-vs-replace recommendation', ' Honest scope-vs-budget recommendations'),

        (' Ignitor, flame sensor &amp; pilot diagnostics', ' Tile, plumbing &amp; vanity install'),
        (' Blower motor, belt &amp; bearing service', ' Frameless glass, custom shower pans &amp; benches'),
        (' Heat exchanger inspection &amp; CO testing', ' Heated floors, fans, lighting &amp; ventilation'),
        (' Thermostat, control board &amp; wiring repair', ' Smart fixtures &amp; touchless tech'),

        (' Manual J load calculation &mdash; sized to your square footage', ' Custom builds sized to your exact kitchen'),
        (' Lennox, Trane, Carrier, Goodman, Daikin &amp; Mitsubishi', ' Wood-Mode, Brookhaven, Crystal &amp; semi-custom'),
        (' Pad, line set, electrical, thermostat &mdash; included', ' Hardware, soft-close, lighting &mdash; included'),
        (' 10-year parts &amp; labor warranty, financing available', ' 10-year warranty, financing available'),

        (' 95-98% AFUE gas furnaces &amp; cold-climate heat pumps', ' Quartz, granite, marble, butcher block, soapstone'),
        (' Permits, gas line, venting, condensate &mdash; handled', ' Templating, fabrication, install &mdash; handled in-house'),
        (' Federal &amp; utility rebate paperwork done for you', ' Honest material guidance &mdash; no markup games'),
        (' 10-year warranty &amp; lifetime workmanship guarantee', ' Lifetime workmanship guarantee'),

        (' Whole-home media filtration (MERV 11&ndash;16)', ' Backsplashes, accent walls &amp; mosaics'),
        (' Steam &amp; bypass humidifiers, whole-home dehumidifiers', ' Shower walls, niches &amp; benches'),
        (' UV-C &amp; bipolar ionization air purifiers', ' Heated floors, Schluter trim &amp; waterproofing'),
        (' Full duct cleaning, sealing &amp; rebalancing', ' Hand-laid by tile specialists, not subs'),

        (' Spring AC + Fall furnace tune-up (21-point each)', ' 3D renderings &amp; layout drawings'),
        (' Front-of-the-line dispatch &mdash; you skip the queue', ' On-site material &amp; finish selection'),
        (' 15% off all repairs, no overtime fees ever', ' Fixed-price quote within 5 business days'),
        (' Cancel anytime &mdash; no contracts, no penalties', ' No-obligation consult — only commit if you love it'),

        ('NATE-certified, and uniformed', 'NKBA-trained, and uniformed'),
    ],

    'about.html': [
        ('NATE-certified.', 'NKBA-certified.'),
    ],

    'contact.html': [
        ('Real person, no phone tree.<br>24/7 emergency dispatch.',
         'Real person reads every message.<br>One business day reply.'),
    ],

    'quote.html': [
        ('Mon&ndash;Fri 7a&ndash;7p<br>24/7 emergency dispatch',
         'Mon&ndash;Fri 8a&ndash;6p<br>Free in-home design visits'),
    ],

    'service-areas.html': [
        (' 24/7 emergency dispatch in same-day cities',
         ' Free in-home design visits in same-day cities'),
    ],
}

for fname, swaps in fixes.items():
    if not os.path.exists(fname):
        print(f'  skip {fname} (not found)'); continue
    with open(fname, encoding='utf-8') as f:
        html = f.read()
    applied = 0
    for old, new in swaps:
        if old in html:
            html = html.replace(old, new)
            applied += 1
    with open(fname, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print(f'  fixed {fname} ({applied}/{len(swaps)})')

# Cache buster bump
for f in os.listdir('.'):
    if not f.endswith('.html'): continue
    with open(f, encoding='utf-8') as fh:
        html = fh.read()
    html = re.sub(r'(styles\.css|main\.js)\?v=\d+', r'\1?v=5', html)
    with open(f, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(html)
print('\nCache bumped to ?v=5')
