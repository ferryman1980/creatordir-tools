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
    
    # Find subreddit input
    sr_inputs = await pg.evaluate("""() => {
        const all = document.querySelectorAll('input, div[role="combobox"], div[role="listbox"]');
        return Array.from(all).map(e => ({
            tag: e.tagName,
            role: e.getAttribute("role") || "",
            ph: e.getAttribute("placeholder") || e.getAttribute("aria-label") || "",
            id: e.id || "",
            name: e.name || ""
        }));
    }""")
    print("Subreddit inputs:")
    for s in sr_inputs:
        print(f"  {s}")
    
    # Find all divs with content
    all_divs = await pg.evaluate("""() => {
        const all = document.querySelectorAll('div');
        return Array.from(all).filter(d => d.textContent.trim().includes("Ch") || d.textContent.trim().includes("选择")).map(d => ({
            text: d.textContent.trim().substring(0,50),
            role: d.getAttribute("role") || "",
            class: (d.className || "").substring(0,40)
        }));
    }""")
    print(f"\nRelevant divs:")
    for d in all_divs:
        print(f"  [{d['text']}] role={d['role']}")
    
    await p.stop()

asyncio.run(main())
