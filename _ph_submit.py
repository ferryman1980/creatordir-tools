import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    # Find PH tab
    pg = None
    for tab in ctx.pages:
        if "producthunt" in tab.url.lower():
            pg = tab
            await tab.bring_to_front()
            break
    
    if not pg:
        pg = await ctx.new_page()
        await pg.goto("https://www.producthunt.com/posts/new", wait_until="domcontentloaded", timeout=20000)
    
    await pg.wait_for_timeout(3000)
    print(f"PH: {await pg.title()} | {pg.url[:80]}")
    
    # Dump all form fields
    page_info = await pg.evaluate("""
        () => {
            const inputs = document.querySelectorAll("input, textarea, button, [contenteditable], [role='textbox']");
            return Array.from(inputs).map(el => ({
                tag: el.tagName,
                type: el.type || "",
                id: el.id,
                name: el.name || "",
                placeholder: el.placeholder || "",
                text: (el.textContent || "").slice(0, 40),
                class: (el.className || "").slice(0, 30),
                aria: el.getAttribute("aria-label") || "",
            }));
        }
    """)
    
    print(f"Found {len(page_info)} elements")
    for el in page_info[:30]:
        print(f"  {el['tag']} type={el['type']} id={el['id']} ph={el['placeholder'][:20]} aria={el['aria'][:20]}")
    
    await p.stop()

asyncio.run(main())
