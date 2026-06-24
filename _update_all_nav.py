import os, re

BASE = r"D:\项目\工作区\工作5"

# Nav items to add (in order)
NEW_NAV = [
    ("courses.html", "\U0001f393 Courses"),
    ("jobs.html", "\U0001f4bc Jobs"),
    ("community.html", "\U0001f465 Community"),
    ("newsletter.html", "\U0001f4ec Newsletter"),
]

def add_nav_items(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    
    modified = False
    for fname, label in NEW_NAV:
        if f'<a href="{fname}"' in html:
            continue  # Already present
        if f'<a href="news.html"' in html:
            # Insert after news.html link
            html = html.replace(
                '<a href="news.html">News</a>',
                f'<a href="news.html">News</a></li>\n      <li><a href="{fname}">{label}</a>'
            )
            modified = True
        elif f'<a href="free-ai-tools.html">' in html:
            # Alternative: insert after free-ai-tools
            html = html.replace(
                '<a href="free-ai-tools.html">\U0001f4b0 Free</a>',
                f'<a href="free-ai-tools.html">\U0001f4b0 Free</a></li>\n      <li><a href="{fname}">{label}</a>'
            )
            modified = True
    
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    return False

# Process all HTML files
count = 0
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "__pycache__")]
    for f in files:
        if f.endswith(".html"):
            try:
                if add_nav_items(os.path.join(root, f)):
                    count += 1
            except:
                pass

print(f"Navigation updated on {count} pages")
