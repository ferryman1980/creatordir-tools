import urllib.request, urllib.parse, json

site = 'https://creatordir-tools.vercel.app'
name = 'CreatorAI Tools'
desc = 'Curated directory of 160+ AI tools for content creators with honest reviews and comparisons.'

# Try submitting to known AI directory submission pages
results = []

# 1. AI directory submission forms (GET-based)
submit_urls = [
    ('https://www.futurepedia.io/submit-tool', 'Futurepedia'),
    ('https://theresanaiforthat.com/submit/', 'ThereIsAnAIForThat'),
    ('https://aitoptools.com/submit-tool/', 'AITopTools'),
    ('https://toolify.ai/submit-tool', 'Toolify'),
    ('https://aiscout.net/submit-tool/', 'AIScout'),
    ('https://www.aitoolsdirectory.com/submit', 'AIToolsDirectory'),
    ('https://insidr.ai/submit-tool/', 'Insidr'),
    ('https://topai.tools/submit', 'TopAITools'),
]

for url, name2 in submit_urls:
    try:
        req = urllib.request.Request(url, method='GET')
        r = urllib.request.urlopen(req, timeout=10)
        print(f'[OK] {name2}: {url} - HTTP {r.status}')
    except Exception as e:
        print(f'[--] {name2}: {str(e)[:60]}')

# 2. Search for AI directory submission pages
import urllib.parse
q = urllib.parse.quote('submit ai tool directory free')
search_url = 'https://www.startpage.com/do/dsearch?query=' + q
try:
    r = urllib.request.urlopen(search_url, timeout=15)
    html = r.read().decode('utf-8', errors='replace')
    print(f'\n[SEARCH] Found {len(html)} bytes of results')
    # extract URLs
    import re
    links = re.findall(r'href=\"(https?://[^\"]+)\"', html)
    for l in links[:20]:
        print(f'  LINK: {l}')
except Exception as e:
    print(f'[SEARCH FAIL] {str(e)[:80]}')

print('\nDone directory scanning')
