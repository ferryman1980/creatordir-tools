import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    print("URL:", pg.url)

    # Find the subreddit selector input
    inputs = await pg.evaluate("""() => {
        const inputs = document.querySelectorAll('input[type="text"], input:not([type="hidden"]), [role="combobox"], [role="searchbox"]');
        return Array.from(inputs).map(e => ({
            tag: e.tagName,
            type: e.type || "",
            role: e.getAttribute("role") || "",
            ph: e.getAttribute("placeholder") || "",
            aria: e.getAttribute("aria-label") || "",
            id: e.id || "",
            name: e.name || "",
            cls: (e.className || "").substring(0,20)
        }));
    }""")
    print(f"Inputs ({len(inputs)}):")
    for inp in inputs:
        print(f"  {inp}")

    # Also check the HTML structure around the post creation
    submit_area = await pg.evaluate("""() => {
        const divs = document.querySelectorAll('[class*="post"], [class*="submit"], [class*="create"]');
        return Array.from(divs).slice(0,5).map(d => ({
            cls: (d.className || "").substring(0,40),
            text: (d.textContent || "").trim().substring(0,60)
        }));
    }""")
    print(f"\nSubmit area divs:")
    for d in submit_area:
        print(f"  class={d['cls']} text=[{d['text']}]")
    await p.stop()

asyncio.run(main())