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
    await amz.wait_for_timeout(2000)
    print(f"URL: {amz.url}")
    
    # Check the registration flow
    # First, find the signup form
    links = await amz.evaluate("""() => {
        const links = document.querySelectorAll("a");
        return Array.from(links).map(l => ({text: l.textContent.trim(), href: l.href})).filter(x => x.href.includes("signup") || x.href.includes("register"));
    }""")
    print("\nSignup links:")
    for l in links:
        print(f"  [{l['text']}] {l['href'][:100]}")
    
    # Check all buttons
    btns = await amz.evaluate("""() => {
        const all = document.querySelectorAll("button, input[type=submit]");
        return Array.from(all).map(b => ({text: b.textContent.trim(), type: b.type || b.tagName, value: b.value || ""}));
    }""")
    print("\nButtons/Submit inputs:")
    for b in btns:
        print(f"  [{b['text'] or b['value']}] type={b['type']}")
    
    await p.stop()

asyncio.run(main())
