import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    amz = None
    for pg in ctx.pages:
        if "affiliate-program.amazon.com" in pg.url:
            amz = pg
            break
    if not amz:
        amz = await ctx.new_page()
    await amz.goto("https://affiliate-program.amazon.com/signup", wait_until="domcontentloaded", timeout=20000)
    await amz.bring_to_front()
    await amz.wait_for_timeout(3000)
    print(f"Current URL: {amz.url}")
    
    # Check what the current page looks like
    html = await amz.content()
    # Search for text that shows the current state
    text = await amz.evaluate("document.body.innerText")
    print(text[:2000])
    
    # If this is the landing page, try to go directly to signup
    if "signup" in amz.url or "/" == amz.url.rstrip("/").split("/")[-1]:
        print("\nOn landing page, clicking signup link...")
        await amz.goto("https://affiliate-program.amazon.com/signup?language=en_US&country=US", wait_until="domcontentloaded", timeout=15000)
        await amz.wait_for_timeout(3000)
        print(f"New URL: {amz.url}")
        text = await amz.evaluate("document.body.innerText")
        print(text[:3000])
    
    # Check form
    fields = await amz.evaluate("""() => {
        const inputs = document.querySelectorAll("input, select, textarea");
        return Array.from(inputs).map(e => ({
            tag: e.tagName,
            type: e.type || "",
            name: e.name || "",
            id: e.id || "",
            placeholder: e.placeholder || "",
            value: e.value || ""
        }));
    }""")
    print(f"\nForm fields: {len(fields)}")
    for f in fields[:30]:
        print(f"  {f['tag']} type={f['type']} name={f['name']}")
    
    await p.stop()

asyncio.run(main())
