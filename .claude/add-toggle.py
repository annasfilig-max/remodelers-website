"""Inject the theme-toggle button into every page header.
Adds it as the first child of .header-cta on each page, so it sits next to
the phone link + Free Quote button on desktop and is auto-hidden on mobile
(via CSS rule). Bumps the cache buster too.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

TOGGLE_HTML = '''      <button type="button" class="theme-toggle" data-theme-toggle aria-label="Toggle light/dark theme" aria-pressed="false">
        <svg class="ico-moon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        <svg class="ico-sun" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>
      </button>
'''

count = 0
for f in sorted(os.listdir('.')):
    if not f.endswith('.html'): continue
    with open(f, encoding='utf-8') as fh: html = fh.read()
    if 'data-theme-toggle' in html:
        # Already present — skip
        pass
    else:
        # Insert toggle as first item inside .header-cta (after the opening tag)
        new = re.sub(
            r'(<div class="header-cta">\s*\n)',
            r'\1' + TOGGLE_HTML,
            html, count=1)
        if new != html:
            html = new
            count += 1
    # Bump cache buster
    html = re.sub(r'(styles\.css|main\.js)\?v=\d+', r'\1?v=6', html)
    with open(f, 'w', encoding='utf-8', newline='\n') as fh: fh.write(html)
print(f'Injected toggle button into {count} pages.')
print('Cache buster bumped to ?v=6')
