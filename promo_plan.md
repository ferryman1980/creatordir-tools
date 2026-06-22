
import webbrowser, time, sys

# Quick submission URLs for AI directories that accept simple form submissions
# These are directories with straightforward submission forms
SUBMISSION_SITES = [
    # Direct submit URLs
    ('https://www.futurepedia.io/submit-tool', 'Futurepedia'),
    ('https://easywithai.com/submit', 'EasyWithAI'),
    ('https://topai.tools/submit', 'TopAI.tools'),
    ('https://toolpilot.ai/submit', 'ToolPilot'),
    ('https://aiscout.net/submit', 'AI Scout'),
    ('https://www.aicontentfy.com/tool-submission', 'AIContentfy'),
    ('https://aitoptools.com/submit', 'AITopTools'),
    ('https://aicollection.org/submit', 'AICollection'),
]

print('=== QUICK SUBMIT SITES ===')
for url, name in SUBMISSION_SITES:
    print(f'{name}: {url}')
print()
print('=== SOCIAL PLATFORMS TO POST ON ===')
print('1. Reddit - r/ArtificialIntelligence, r/webdev, r/Entrepreneur')
print('2. LinkedIn - Post as article')
print('3. Product Hunt - Launch as maker')
print('4. GitHub Discussions')
print('5. Hacker News - Show HN')
print('6. Indie Hackers')
print('7. Dev.to - Cross-post articles')
print('8. Medium - Republish articles')
