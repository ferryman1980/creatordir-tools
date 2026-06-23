import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    # Go to Reddit register page
    pg = ctx.pages[0]
    await pg.goto("https://www.reddit.com/register/", wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(3)
    
    print(f"URL: {pg.url}")
    text = await pg.evaluate("document.body.innerText")
    print(text[:2000])
    
    # Check form fields
    fields = await pg.evaluate("""() => {
        const inputs = document.querySelectorAll("input");
        return Array.from(inputs).map(e => ({
            type: e.type || "",
            name: e.name || "",
            id: e.id || "",
            placeholder: e.placeholder || "",
            autocomplete: e.autocomplete || ""
        }));
    }""")
    print(f"\nForm fields ({len(fields)}):")
    for f in fields[:10]:
        print(f"  {f}")
    
    await p.stop()

asyncio.run(main())
