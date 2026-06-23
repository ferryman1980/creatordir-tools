import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pages = ctx.pages
    print("Open pages:")
    for i, pg in enumerate(pages):
        print(f"  [{i}] {pg.url[:120]}")
    
    # Check findmyaitool page
    for pg in pages:
        if "findmyaitool" in pg.url:
            await pg.bring_to_front()
            await pg.wait_for_timeout(2000)
            print(f"\n=== findmyaitool: {pg.url} ===")
            text = await pg.evaluate("document.body.innerText")
            print(text[:2000])
    
    # Open Amazon Associates signup
    print("\n=== Opening Amazon Associates ===")
    amz = await ctx.new_page()
    await amz.goto("https://affiliate-program.amazon.com/", wait_until="domcontentloaded", timeout=20000)
    await amz.wait_for_timeout(2000)
    print(f"URL: {amz.url}")
    btns = await amz.evaluate("""() => {
        const links = document.querySelectorAll("a, button");
        return Array.from(links).map(l => ({text: l.textContent.trim(), href: l.href || ""})).filter(x => x.text.includes("Sign") || x.text.includes("sign") || x.text.includes("\u6ce8\u518c") || x.href.includes("signup") || x.href.includes("register"));
    }""")
    print("Signup links:")
    for b in btns:
        print(f"  [{b['text']}] {b['href'][:80]}")
    
    await p.stop()

asyncio.run(main())
