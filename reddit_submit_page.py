import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    
    # Go to create post page via submit URL
    await pg.goto("https://www.reddit.com/r/ArtificialIntelligence/submit", wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(4)
    
    print(f"URL: {pg.url}")
    
    # Look for the post creation form
    text = await pg.evaluate("document.body.innerText")
    print(text[:1000])
    
    # Try looking for contenteditable divs or rich text editors
    editors = await pg.evaluate("""() => {
        const all = document.querySelectorAll("[contenteditable], div[role='textbox'], div[data-lexical-editor]");
        return Array.from(all).map(e => ({
            tag: e.tagName,
            role: e.getAttribute("role") || "",
            placeholder: e.getAttribute("placeholder") || e.getAttribute("aria-placeholder") || "",
            text: (e.textContent || "").trim().substring(0,40),
            inner: (e.innerHTML || "").substring(0,60)
        }));
    }""")
    print(f"\nRich editors ({len(editors)}):")
    for ed in editors:
        print(f"  role={ed['role']} ph=[{ed['placeholder']}] text=[{ed['text']}]")
    
    # Try to find title input
    title_input = await pg.locator("input[aria-label*='title' i], input[aria-label*='Title' i], input[name='title'], #post-title").count()
    print(f"Title inputs found: {title_input}")
    
    await p.stop()

asyncio.run(main())
