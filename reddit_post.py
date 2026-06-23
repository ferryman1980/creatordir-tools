import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

POST_TITLE = "I built a directory of 200+ AI tools for content creators - all tested and reviewed"
POST_BODY = """After months of testing AI tools, I created a curated directory at **creatordir-tools.vercel.app**

Features: 200+ articles, 54 tool reviews, comparisons, and tutorials
All free, open source on GitHub.

Would love feedback from the community! 🚀"""

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    
    # Go to r/ArtificialIntelligence submit page
    await pg.goto("https://www.reddit.com/r/ArtificialIntelligence/submit", wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(5)
    print(f"URL: {pg.url}")
    
    # Find all interactive elements
    els = await pg.evaluate("""() => {
        const all = document.querySelectorAll("input, textarea, button, div[role='textbox'], [contenteditable]");
        return Array.from(all).map(e => ({
            tag: e.tagName,
            type: e.type || "",
            role: e.getAttribute("role") || "",
            placeholder: e.placeholder || "",
            aria_label: e.getAttribute("aria-label") || "",
            id: e.id || "",
            text: (e.textContent || "").trim().substring(0,40),
            class: (e.className || "").substring(0,40)
        }));
    }""")
    print(f"Interactive elements ({len(els)}):")
    for e in els:
        print(f"  {e['tag']} type={e['type']} role={e['role']} ph=[{e['placeholder']}] aria=[{e['aria_label']}]")
    
    await p.stop()

asyncio.run(main())
