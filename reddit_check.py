import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    reddit = ctx.pages[0]
    await reddit.bring_to_front()
    await asyncio.sleep(2)
    
    links = await reddit.evaluate("""() => {
        return Array.from(document.querySelectorAll("a, button")).map(e => ({
            text: e.textContent.trim().substring(0,40),
            href: e.href || "",
            id: e.id || ""
        })).filter(x => 
            x.text.toLowerCase().includes("register") || 
            x.text.toLowerCase().includes("sign") || 
            x.text.toLowerCase().includes("login") ||
            x.text.includes("註冊") ||
            x.text.includes("登入") ||
            x.text.includes("create")
        );
    }""")
    print("Auth buttons:")
    for l in links:
        print(f"  [{l['text']}] href={l['href'][:80]}")
    
    print("\nURL:", reddit.url)
    await p.stop()

asyncio.run(main())
