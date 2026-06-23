import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    # Check Amazon page
    amz = None
    for pg in ctx.pages:
        if "amazon.com" in pg.url:
            amz = pg
            break
    if not amz:
        amz = await ctx.new_page()
        await amz.goto("https://affiliate-program.amazon.com/signup", wait_until="domcontentloaded", timeout=20000)
        await amz.wait_for_timeout(3000)
    
    await amz.bring_to_front()
    print(f"URL: {amz.url}")
    text = await amz.evaluate("document.body.innerText")
    print(text[:3000])
    
    # Check form fields
    fields = await amz.evaluate("""() => {
        const inputs = document.querySelectorAll("input, select, textarea");
        return Array.from(inputs).map(e => ({
            tag: e.tagName,
            type: e.type || "",
            name: e.name || "",
            id: e.id || "",
            placeholder: e.placeholder || ""
        }));
    }""")
    print(f"\nForm fields ({len(fields)}):")
    for f in fields:
        print(f"  {f['tag']} type={f['type']} name={f['name']} id={f['id']}")
    
    await p.stop()

asyncio.run(main())
