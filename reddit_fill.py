import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    print("URL:", pg.url)
    await asyncio.sleep(2)
    result = await pg.evaluate("""() => {
        const all = document.querySelectorAll('input, textarea, [contenteditable], [role="textbox"]');
        return Array.from(all).map(e => ({
            tag: e.tagName,
            type: e.type || "",
            role: e.getAttribute("role") || "",
            ph: e.getAttribute("placeholder") || e.getAttribute("aria-label") || "",
            id: e.id || "",
            name: e.name || ""
        }));
    }""")
    print(f"Found {len(result)} elements:")
    for r in result:
        print(f"  {r}")
    await p.stop()

asyncio.run(main())
