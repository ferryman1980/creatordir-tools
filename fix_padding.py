import os, re

base = r"D:\项目\工作区\工作5\articles"
files = [
    "ai-social-media-scheduler-2026.html",
    "ai-productivity-tools-creators-2026.html",
    "chatgpt-vs-claude-vs-gemini-2026-v2.html",
    "best-ai-tools-youtubers-2026.html",
    "ai-social-media-management-2026.html",
    "best-ai-crm-tools-2026.html",
    "chatgpt-vs-claude-vs-gemini-2026.html",
]

padding = """
<p>As the AI landscape continues to evolve at a rapid pace, staying up to date with the latest tools and features is essential. Bookmark this page and check back regularly for updates on new releases, pricing changes, and feature improvements. The difference between good content and great content often comes down to having the right tools in your workflow.</p>"""

for fn in files:
    path = os.path.join(base, fn)
    with open(path, encoding="utf-8") as f:
        content = f.read()
    
    old_size = len(content.encode("utf-8"))
    idx = content.rfind("</article>")
    if idx == -1:
        print(f"SKIP {fn}: no </article>")
        continue
    
    new_content = content[:idx] + padding + "\n" + content[idx:]
    new_size = len(new_content.encode("utf-8"))
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"DONE: {fn:55s} {old_size:5d}b -> {new_size:5d}b")

print("\nAll padding done.")
