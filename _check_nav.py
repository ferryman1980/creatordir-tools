import os, re

BASE = r"D:\项目\工作区\工作5"

# New nav items to add
NAV_ITEMS = {
    "courses.html": "🎓 Courses",
    "jobs.html": "💼 Jobs",
    "community.html": "👥 Community",
    "newsletter.html": "📬 Newsletter"
}

# First, check current nav in index.html as reference
with open(os.path.join(BASE, "index.html"), "r", encoding="utf-8") as f:
    index_html = f.read()

# Find the nav section
nav_match = re.search(r"<ul[^>]*class=\"nav-links\"[^>]*>.*?</ul>", index_html, re.DOTALL)
if nav_match:
    nav_section = nav_match.group()
    print("Current nav items:")
    for m in re.finditer(r'<li><a href="([^"]+)"[^>]*>([^<]+)</a></li>', nav_section):
        print(f"  {m.group(1)} -> {m.group(2)}")
    
    # Check which new items are missing
    existing = set(m.group(1) for m in re.finditer(r'<li><a href="([^"]+)"', nav_section))
    for fname, label in NAV_ITEMS.items():
        if fname not in existing:
            print(f"\n  MISSING: {fname} ({label})")

# Count total HTML files
all_html = []
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "__pycache__")]
    for f in files:
        if f.endswith(".html"):
            all_html.append(os.path.join(root, f))

print(f"\nTotal HTML files: {len(all_html)}")
print("Ready to update navigation on all pages.")
