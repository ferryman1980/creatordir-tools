import json, sys, os
sys.path.insert(0, r"D:\项目\工作区\工作5")

exec(open(r"D:\项目\工作区\工作5\gen_40_articles.py", encoding="utf-8").read())

data_file = os.path.join(DIR, "_articles_data.json")
with open(data_file, "r", encoding="utf-8") as f:
    data = json.load(f)

articles = data["articles"]
print(f"Generating {len(articles)} articles...")

for i, a in enumerate(articles):
    make_article(a["fn"], a["title"], a["desc"], a["h1"], a["body"])

print("\nDone! All 40 articles generated.")
