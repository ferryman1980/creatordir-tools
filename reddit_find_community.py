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
    # Get ALL visible elements that could be the subreddit selector
    result = await pg.evaluate("() => {
        const all = Array.from(document.querySelectorAll('*')).filter(e => e.offsetParent !== null);
        return all.filter(e => {
            const t = (e.textContent || '').toLowerCase();
            return t.includes('choose') || t.includes('community') || t.includes('subreddit') || t.includes('select') || t.includes('r/');
        }).slice(0,10).map(e => ({
            tag: e.tagName,
            txt: (e.textContent || '').trim().substring(0,50),
            cls: (e.className || '').substring(0,30)
        }));
    }")
    print("Matches:", len(result))
    for r in result:
        print(f"  [{r['txt']}] tag={r['tag']}")
    await p.stop()
asyncio.run(main())