
import urllib.request, ssl
ssl._create_default_https_context = ssl._create_unverified_context

dirs = [
    ("Futurepedia","https://www.futurepedia.io/submit-tool"),
    ("EasyWithAI","https://easywithai.com/submit"),
    ("TopAI.tools","https://topai.tools/submit"),
    ("ToolPilot","https://toolpilot.ai/submit"),
    ("AI Scout","https://aiscout.net/submit"),
    ("AITopTools","https://aitoptools.com/submit"),
    ("AICollection","https://aicollection.org/submit"),
]
for name, url in dirs:
    try:
        r = urllib.request.urlopen(url, timeout=10)
        body = r.read().decode("utf-8","replace")
        has_form = "form" in body.lower() and "input" in body.lower()
        has_submit = "type=\"submit\"" in body or "value=\"Submit\"" in body
        print(f"{name}: HTTP {r.status}, {len(body)}b, form={has_form}, btn={has_submit}")
    except Exception as e:
        print(f"{name}: {str(e)[:60]}")
