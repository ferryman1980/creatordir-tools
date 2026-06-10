# -*- coding: utf-8 -*-
import io, sys, requests, json, os, re
from datetime import datetime
import concurrent.futures
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CATEGORIES = {
    "writing": {"keywords": ["writing", "copy", "text", "content", "blog", "article", "markdown", "document", "nlp", "language-model", "llm", "gpt", "chatbot", "translation", "summarization"], "max": 8},
    "image": {"keywords": ["image", "design", "cover", "thumbnail", "photo", "illustration", "drawing", "art", "stable-diffusion", "midjourney", "generative-image", "computer-vision", "canvas", "graphic"], "max": 8},
    "video": {"keywords": ["video", "audio", "music", "voice", "editing", "clip", "movie", "sound", "speech", "voiceover", "caption", "subtitles", "tts", "music-generation", "video-generation"], "max": 8}
}

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
TIMEOUT = 15
results = {"writing": [], "image": [], "video": [], "uncategorized": [], "errors": []}

def classify_repo(topics, name, desc):
    text = f"{name} {desc or ''} {' '.join(topics or [])}".lower()
    scores = {}
    for cat, config in CATEGORIES.items():
        score = sum(2 if kw in text else 0 for kw in config["keywords"])
        if "ai" in text or "artificial" in text or "machine-learning" in text:
            score += 1
        if score > 0:
            scores[cat] = score
    if scores:
        return max(scores, key=scores.get)
    return "uncategorized"

def fetch_github_search(query, per_page=15):
    try:
        r = requests.get(f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={per_page}", headers=HEADERS, timeout=TIMEOUT)
        if r.status_code == 200:
            return r.json().get("items", [])
    except Exception as e:
        results["errors"].append(f"search({query[:30]}): {e}")
    return []

def fetch_github_trending():
    items = []
    queries = [
        "ai+tool+content+creator",
        "ai+writing+tool",
        "ai+image+generator",
        "ai+video+editor",
        "content+creation+ai",
        "ai+voice+generator",
        "stable-diffusion",
        "llm+chatbot",
        "open-source+ai+tool",
        "creative+ai"
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(fetch_github_search, q, 12): q for q in queries}
        for future in concurrent.futures.as_completed(futures):
            items.extend(future.result())
    seen = set()
    unique = []
    for item in items:
        if item["id"] not in seen:
            seen.add(item["id"])
            unique.append(item)
    return unique

def fetch_trending_page():
    try:
        return fetch_github_search("stars:>1000+created:>2025-01-01", 20)
    except Exception as e:
        results["errors"].append(f"trending: {e}")
    return []

def fetch_top_topics():
    topics = ["ai-tools", "artificial-intelligence", "content-creation", "creative-tools", "generative-ai", "machine-learning"]
    all_items = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(fetch_github_search, f"topic:{t}", 10): t for t in topics}
        for future in concurrent.futures.as_completed(futures):
            all_items.extend(future.result())
    seen = set()
    unique = []
    for item in all_items:
        if item["id"] not in seen:
            seen.add(item["id"])
            unique.append(item)
    return unique

def process_results(items):
    seen_names = set()
    for item in items:
        name = item.get("full_name", "")
        if name in seen_names:
            continue
        seen_names.add(name)
        entry = {
            "name": name,
            "url": item.get("html_url", ""),
            "description": (item.get("description") or "")[:200],
            "stars": item.get("stargazers_count", 0),
            "topics": item.get("topics", []),
            "language": item.get("language") or "N/A",
            "updated_at": item.get("updated_at", ""),
            "homepage": item.get("homepage") or ""
        }
        cat = classify_repo(item.get("topics", []), name, item.get("description"))
        if cat in CATEGORIES:
            if len(results[cat]) < CATEGORIES[cat]["max"]:
                results[cat].append(entry)
        else:
            if len(results["uncategorized"]) < 10:
                results["uncategorized"].append(entry)

def gen_html(cat_name, entries, emoji):
    if not entries:
        return ""
    today = datetime.now().strftime("%Y-%m-%d")
    html = f'''    <div class="resource-cat">
      <h2>{emoji} Trending GitHub: {cat_name.title()} AI Tools</h2>
      <p>Top open-source AI projects for {cat_name}. Fetched {today} from GitHub API. Sorted by stars.</p>
      <div class="resource-grid">
'''
    for e in entries:
        desc = e["description"][:120] + ("..." if len(e["description"]) > 120 else "")
        stars = f'{e["stars"]:,}'
        lang = e["language"][:15] if e["language"] else ""
        html += f'''        <a href="{e["url"]}" target="_blank" rel="noopener" class="resource-link">
          <div class="rl-icon" style="background:#1e293b;color:white;font-size:0.8rem">GH</div>
          <div class="rl-body">
            <div class="rl-title">{e["name"]}</div>
            <div class="rl-desc">{desc}</div>
          </div>
          <span class="rl-arrow" style="display:flex;flex-direction:column;align-items:flex-end;gap:0.1rem;font-size:0.75rem">
            <span style="font-weight:700;color:var(--text)">{stars} stars</span>
            <span style="color:var(--text-muted)">{lang}</span>
          </span>
        </a>
'''
    html += '''      </div>
    </div>
    <p style="color:var(--text-muted);font-size:0.82rem;margin-top:0.5rem">Source: GitHub API. Stars and descriptions as of fetch time.</p>
'''
    return html

def main():
    print("=" * 50)
    print(f"GitHub Crawler �� Started at {datetime.now().isoformat()}")
    print(f"Parallel workers: 10 search + 6 topic = 16 concurrent")
    print("=" * 50)

    print("\n[PHASE 1] Fetching data from GitHub...")
    all_items = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        f1 = pool.submit(fetch_github_trending)
        f2 = pool.submit(fetch_trending_page)
        f3 = pool.submit(fetch_top_topics)
        for future in concurrent.futures.as_completed([f1, f2, f3]):
            items = future.result()
            all_items.extend(items)
            print(f"  Received batch: {len(items)} items")

    seen = set()
    unique_items = []
    for item in all_items:
        if item["id"] not in seen:
            seen.add(item["id"])
            unique_items.append(item)

    print(f"\n[DATA] Total unique repos: {len(unique_items)}")
    print(f"[PHASE 2] Classifying...")

    process_results(unique_items)

    print(f"\n[RESULTS]")
    for cat in CATEGORIES:
        print(f"  {cat}: {len(results[cat])} repos")
    print(f"  uncategorized: {len(results['uncategorized'])} repos")
    if results["errors"]:
        print(f"\n[WARN] {len(results['errors'])} errors:")
        for e in results["errors"][:5]:
            print(f"  {e}")

    print(f"\n[PHASE 3] Generating HTML...")
    html_parts = []
    for cat in ["writing", "image", "video"]:
        emoji = {"writing": "DP", "image": "AR", "video": "VI"}[cat]
        emoji_full = {"writing": "DP Trending GitHub: ", "image": "AR Trending GitHub: ", "video": "VI Trending GitHub: "}
        h = gen_html(cat, results[cat], cat.upper()[0])
        if h:
            html_parts.append(h)

    output = {
        "summary": {
            "total_fetched": len(unique_items),
            "classified": {k: len(v) for k, v in results.items() if k != "errors"},
            "errors": len(results["errors"]),
            "timestamp": datetime.now().isoformat()
        },
        "html_snippets": html_parts,
        "raw_data": results
    }

    print(f"\n[OK] Done! Generated {len(html_parts)} HTML sections")
    total_classified = sum(len(results[c]) for c in CATEGORIES)
    print(f"     {total_classified} repos classified across 3 categories")

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "github_crawl_output.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"     Saved to: {out_path}")

    # Print the HTML snippets to stdout for easy copying
    print("\n" + "=" * 50)
    print("HTML OUTPUT FOR RESOURCES PAGE:")
    print("=" * 50)
    print('\n'.join(html_parts))

    return output

if __name__ == "__main__":
    output = main()
