import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    
    # Go to homepage and click Create Post
    await pg.goto("https://www.reddit.com/", wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(4)
    
    # Look for Create Post button - try multiple approaches
    # First using text content
    buttons = await pg.evaluate("""() => {
        const all = document.querySelectorAll("button, a, [role='button'], shrine-update");
        return Array.from(all).map(b => {
            const txt = (b.textContent || "").trim();
            return {
                text: txt.substring(0, 60),
                tag: b.tagName,
                role: b.getAttribute("role") || "",
                id: b.id || "",
                class: (b.className || "").substring(0,50),
                href: b.href || ""
            };
        }).filter(x => 
            x.text.includes("Create") || 
            x.text.includes("Post") ||
            x.text.includes("\u521b\u5efa") ||
            x.text.includes("\u5e16\u5b50")
        );
    }""")
    print(f"Post creation buttons ({len(buttons)}):")
    for b in buttons:
        print(f"  [{b['text']}] tag={b['tag']} id={b['id']}")

    # Try clicking the "Create" button if found
    for b in buttons:
        if "\u521b\u5efa" in b['text'] or "Create" in b['text']:
            print(f"\nClicking: [{b['text']}]")
            el = await pg.locator(f"button:has-text('{b['text'][:20]}'), a:has-text('{b['text'][:20]}')").first
            if await el.count() > 0:
                await el.click()
                print("Clicked!")
                await asyncio.sleep(3)
                break
    
    print(f"\nFinal URL: {pg.url}")
    text = await pg.evaluate("document.body.innerText")
    print(text[:1000])
    
    await p.stop()

asyncio.run(main())
