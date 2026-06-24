import re, os, glob

base = r"D:\项目\工作区\工作5\articles"
files = glob.glob(os.path.join(base, "*.html"))

all_ok = True
for f in sorted(files, key=os.path.getsize):
    with open(f, encoding="utf-8") as fh:
        content = fh.read()
    size = len(content.encode("utf-8"))
    h1 = re.search(r"<h1>(.*?)</h1>", content)
    art = re.search(r"<article[^>]*>(.*?)</article>", content, re.DOTALL)
    
    issues = []
    if size < 6000:
        issues.append(f"size={size}<6000")
    if not h1:
        issues.append("no H1")
    if not art:
        issues.append("no <article>")
    if "Why This Matters" not in content:
        issues.append("no template")
    if "How to Get Started" not in content:
        issues.append("no how-to")
    
    if issues:
        all_ok = False
        print(f"ISSUE: {os.path.basename(f):55s} {' | '.join(issues)}")

if all_ok:
    print(f"ALL {len(files)} files OK: >=6KB, has H1, has article, has template sections")
else:
    print(f"\nSome files have issues. Total files: {len(files)}")
