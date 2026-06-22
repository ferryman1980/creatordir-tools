import os, json, requests, re, concurrent.futures, time
from datetime import datetime

BASE = "D:/项目/工作区/工作5"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

# === DEEP CATEGORY TAXONOMY ===
CATEGORIES = {
    "writing": {
        "name": "AI Writing & Content",
        "emoji": "\U0001f4dd",
        "color": "#6366f1",
        "subs": {
            "general": {"name": "General Writing", "keywords": ["writing", "content", "copy", "text", "blog", "article"]},
            "longform": {"name": "Long-form Content", "keywords": ["longform", "long-form", "book", "essay", "report", "document"]},
            "copywriting": {"name": "Copywriting & Sales", "keywords": ["copywriting", "sales", "marketing copy", "ad copy", "landing page"]},
            "summarization": {"name": "Summarization", "keywords": ["summariz", "summary", "abstract", "tl dr"]},
            "translation": {"name": "Translation", "keywords": ["translat", "language", "multilingual", "i18n"]},
        }
    },
    "image": {
        "name": "AI Image & Design",
        "emoji": "\U0001f3a8",
        "color": "#ec4899",
        "subs": {
            "generation": {"name": "Image Generation", "keywords": ["image generation", "text-to-image", "txt2img", "generate image"]},
            "editing": {"name": "Image Editing", "keywords": ["image edit", "photo edit", "retouch", "inpaint", "outpaint"]},
            "design": {"name": "Graphic Design", "keywords": ["design", "graphic", "layout", "template", "brand"]},
            "screenshot": {"name": "Screenshots & Mockups", "keywords": ["screenshot", "mockup", "prototype", "wireframe"]},
            "svg": {"name": "SVG & Icons", "keywords": ["svg", "icon", "illustration", "vector"]},
        }
    },
    "video": {
        "name": "AI Video & Animation",
        "emoji": "\U0001f3ac",
        "color": "#10b981",
        "subs": {
            "generation": {"name": "Video Generation", "keywords": ["video generation", "text-to-video", "txt2video", "gen video"]},
            "editing": {"name": "Video Editing", "keywords": ["video edit", "clip", "timeline", "cut", "trim"]},
            "subtitles": {"name": "Subtitles & Captions", "keywords": ["subtitle", "caption", "transcript", "auto-caption"]},
            "animation": {"name": "Animation & Motion", "keywords": ["animat", "motion", "cartoon", "character"]},
        }
    },
    "audio": {
        "name": "AI Audio & Music",
        "emoji": "\U0001f3b5",
        "color": "#06b6d4",
        "subs": {
            "tts": {"name": "Text-to-Speech", "keywords": ["tts", "text to speech", "voice", "voiceover", "speech synthesis"]},
            "music": {"name": "Music Generation", "keywords": ["music", "song", "beat", "melody", "compos"]},
            "transcription": {"name": "Transcription", "keywords": ["transcri", "speech to text", "stt", "whisper"]},
            "voice_cloning": {"name": "Voice Cloning", "keywords": ["voice clone", "voice copy", "voice mimic"]},
            "podcast": {"name": "Podcast & Audio Production", "keywords": ["podcast", "audio edit", "daw", "recording"]},
        }
    },
    "marketing": {
        "name": "AI Marketing & SEO",
        "emoji": "\U0001f4ca",
        "color": "#f59e0b",
        "subs": {
            "seo": {"name": "SEO & Search", "keywords": ["seo", "search", "rank", "keyword", "google search"]},
            "analytics": {"name": "Analytics & Data", "keywords": ["analytics", "dashboard", "metric", "report", "data viz"]},
            "email": {"name": "Email Marketing", "keywords": ["email", "newsletter", "mail", "campaign"]},
            "social": {"name": "Social Media", "keywords": ["social", "twitter", "instagram", "tiktok", "facebook", "linkedin"]},
            "ads": {"name": "Advertising", "keywords": ["ad", "advert", "ppc", "cpc", "campaign"]},
        }
    },
    "code": {
        "name": "AI Code & Development",
        "emoji": "\U0001f4bb",
        "color": "#3b82f6",
        "subs": {
            "assistant": {"name": "Code Assistants", "keywords": ["code assistant", "copilot", "code complet", "autocomplete"]},
            "generation": {"name": "Code Generation", "keywords": ["code generat", "text-to-code", "code from prompt"]},
            "debugging": {"name": "Debugging & Testing", "keywords": ["debug", "test", "bug", "qa", "quality"]},
            "cli": {"name": "CLI & Terminal", "keywords": ["cli", "terminal", "command line", "shell"]},
            "api": {"name": "API & Integration", "keywords": ["api", "sdk", "integration", "webhook"]},
        }
    },
    "productivity": {
        "name": "AI Productivity",
        "emoji": "\u26a1",
        "color": "#f97316",
        "subs": {
            "notes": {"name": "Notes & Knowledge", "keywords": ["note", "knowledge", "wiki", "document", "second brain"]},
            "calendar": {"name": "Calendar & Schedule", "keywords": ["calendar", "schedule", "meeting", "appointment"]},
            "task": {"name": "Task & Project", "keywords": ["task", "project", "todo", "kanban", "sprint"]},
            "automation": {"name": "Automation", "keywords": ["automation", "workflow", "zapier", "ifttt", "no-code"]},
        }
    }
}

# === SEARCH QUERIES PER CATEGORY ===
SEARCH_QUERIES = []
for main_cat, main_data in CATEGORIES.items():
    SEARCH_QUERIES.append(f"ai+{main_cat}+tool")
    for sub_cat, sub_data in main_data["subs"].items():
        kw = sub_data["keywords"][0].replace(" ", "+")
        SEARCH_QUERIES.append(f"ai+{kw}")
    SEARCH_QUERIES.append(f"best+ai+{main_cat}+tool")
    SEARCH_QUERIES.append(f"open-source+ai+{main_cat}")

# === GITHUB CRAWLER ===
results = {cat: [] for cat in CATEGORIES}
results["uncategorized"] = []
results["errors"] = []
all_fetched = {}

def fetch_github(q, per_page=15):
    try:
        r = requests.get(f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page={per_page}", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            return r.json().get("items", [])
        if r.status_code == 403 and "rate" in r.text.lower():
            print(f"  Rate limited on: {q[:30]}")
            time.sleep(5)
    except Exception as e:
        results["errors"].append(f"{q[:30]}: {str(e)[:40]}")
    return []

def classify_deep(topics, name, desc, readme=""):
    text = f"{name} {desc or ''} {' '.join(topics or [])} {readme[:500]}".lower()
    scores = {}
    for main_cat, main_data in CATEGORIES.items():
        for sub_cat, sub_data in main_data["subs"].items():
            score = 0
            for kw in sub_data["keywords"]:
                if kw.lower() in text:
                    score += len(kw)  # Longer match = more specific
            if score > 0:
                scores[f"{main_cat}.{sub_cat}"] = score
    if scores:
        best = max(scores, key=scores.get)
        main = best.split(".")[0]
        return main
    # Fallback to main category matching
    for main_cat in CATEGORIES:
        if main_cat in text:
            return main_cat
    return "uncategorized"

def fetch_all():
    print(f"Fetching {len(SEARCH_QUERIES)} queries from GitHub API...")
    print(f"Categories: {list(CATEGORIES.keys())}")
    print()
    
    all_items = []
    batch_size = 8
    for i in range(0, len(SEARCH_QUERIES), batch_size):
        batch = SEARCH_QUERIES[i:i+batch_size]
        with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as pool:
            futures = {pool.submit(fetch_github, q, 10): q for q in batch}
            for f in concurrent.futures.as_completed(futures):
                items = f.result()
                all_items.extend(items)
        print(f"  Batch {i//batch_size + 1}/{(len(SEARCH_QUERIES)+batch_size-1)//batch_size}: got {len(all_items)} unique so far")
        time.sleep(2)  # Rate limit protection
    
    # Deduplicate
    seen = set()
    unique = []
    for item in all_items:
        if item["id"] not in seen:
            seen.add(item["id"])
            unique.append(item)
    
    print(f"\nTotal unique: {len(unique)}")
    print(f"Classifying...")
    
    for item in unique:
        entry = {
            "id": item["id"],
            "name": item["full_name"],
            "url": item["html_url"],
            "description": (item.get("description") or "")[:300],
            "stars": item["stargazers_count"],
            "topics": item.get("topics", []),
            "language": item.get("language") or "N/A",
            "updated": item.get("updated_at", ""),
            "homepage": item.get("homepage") or "",
            "owner": item.get("owner", {}).get("login", ""),
            "license": item.get("license", {}).get("spdx_id", "") if item.get("license") else "",
            "forks": item.get("forks_count", 0),
            "issues": item.get("open_issues_count", 0),
        }
        
        cat = classify_deep(entry["topics"], entry["name"], entry["description"])
        scored_cats = {c: 0 for c in CATEGORIES}
        for c in CATEGORIES:
            if c in cat or cat.startswith(c):
                scored_cats[c] = 1
        
        # Add to best matching category
        if cat in CATEGORIES:
            results[cat].append(entry)
        else:
            results["uncategorized"].append(entry)
    
    # Limit per category
    for cat in results:
        if cat != "errors" and cat != "uncategorized":
            results[cat] = sorted(results[cat], key=lambda x: -x["stars"])[:25]

fetch_all()

# === GENERATE DATA FILE ===
output = {
    "generated": datetime.now().isoformat(),
    "categories": {k: v["name"] for k, v in CATEGORIES.items()},
    "stats": {cat: len(items) for cat, items in results.items() if cat not in ["errors", "uncategorized"]},
    "total": sum(len(items) for cat, items in results.items() if cat not in ["errors"]),
    "data": results,
}

out_path = os.path.join(BASE, "data", "tools_database.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n=== RESULTS ===")
for cat in CATEGORIES:
    print(f"  {CATEGORIES[cat]['name']}: {len(results[cat])} tools")
print(f"  Uncategorized: {len(results['uncategorized'])}")
print(f"  Total: {output['total']} tools")
print(f"\nSaved to: data/tools_database.json")
