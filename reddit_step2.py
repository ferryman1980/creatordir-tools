import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    
    # Check current state - might already be on step 2
    print(f"URL: {pg.url}")
    text = await pg.evaluate("document.body.innerText")
    print(text[:1500])
    
    # Check all inputs
    inputs = await pg.evaluate("""() => {
        return Array.from(document.querySelectorAll("input")).map(i => ({
            type: i.type,
            name: i.name,
            id: i.id,
            placeholder: i.placeholder || "",
            autocomplete: i.autocomplete || ""
        }));
    }""")
    print(f"\nInputs ({len(inputs)}):")
    for inp in inputs:
        print(f"  {inp}")
    
    await p.stop()

asyncio.run(main())
