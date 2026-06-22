import asyncio, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
HOSTINGER = 'https://www.hostinger.com?REFERRALCODE=ECA346010F8J'
ELEVENLABS = 'https://try.elevenlabs.io/ebksqtv6a5m6'
SITE = 'https://creatordir-tools.vercel.app'
NAME = 'CreatorAI Tools'
DESC = 'Curated directory of 200+ AI tools for content creators. Honest reviews, comparisons, and guides.'
EMAIL = '346010735@qq.com'
DIRS = [
    ('Futurepedia','https://www.futurepedia.io/submit-tool'),
    ('EasyWithAI','https://easywithai.com/submit'),
    ('TopAI.tools','https://topai.tools/submit'),
    ('ToolPilot','https://toolpilot.ai/submit'),
    ('AI Scout','https://aiscout.net/submit'),
    ('ThereAIForThat','https://theresanaiforthat.com/submit/'),
    ('AITopTools','https://aitoptools.com/submit'),
]
print('Script loaded with', len(DIRS), 'directories')
for n,u in DIRS:
    print(f'  {n}: {u}')
