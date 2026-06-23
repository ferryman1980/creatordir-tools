import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

POST_TITLE = "I built a directory of 200+ AI tools for content creators - all tested and reviewed"
POST_BODY = """After months of testing AI tools, I created a curated directory at creatordir-tools.vercel.app

Features: 200+ articles, 54 tool reviews, comparisons, and tutorials
All free, open source on GitHub.

Would love feedback from the community!"""

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    
    # Use old.reddit.com for posting - simpler HTML
    await pg.goto("https://old.reddit.com/r/ArtificialIntelligence/submit", wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(3)
    print(f"URL: {pg.url}")
    
    text = await pg.evaluate("document.body.innerText")
    print(text[:2000])
    
    # Check form on old reddit
    fields = await pg.evaluate("""() => {
        const inputs = document.querySelectorAll("input, textarea, button");
        return Array.from(inputs).map(e => ({
            tag: e.tagName,
            type: e.type || "",
            name: e.name || "",
            id: e.id || "",
            placeholder: e.placeholder || "",
            value: e.value || "",
            text: (e.textContent || "").trim().substring(0,30)
        }));
    }""")
    print(f"\nForm fields ({len(fields)}):")
    for f in fields:
        print(f"  {f['tag']} name={f['name']} id={f['id']} type={f['type']} text=[{f['text']}]")
    
    await p.stop()

asyncio.run(main())
