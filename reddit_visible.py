import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright
async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    print("URL:", pg.url)
    await asyncio.sleep(1)
    result = await pg.evaluate("""() => {
        const all = document.querySelectorAll("button, a, [role=\"button\"], [role=\"combobox\"]");
        return Array.from(all).filter(e => e.offsetParent !== null).map(e => ({
            tag: e.tagName,
            txt: (e.textContent || "").trim().substring(0,30),
            role: e.getAttribute("role") || ""
        }));
    }""")
    print(f"Visible interactive ({len(result)}):")
    for r in result:
        print(f"  [{r['txt']}] tag={r['tag']} role={r['role']}")
    await p.stop()
asyncio.run(main())