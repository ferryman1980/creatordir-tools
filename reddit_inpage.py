import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    
    # Try posting via browser context API (in-page fetch)
    await pg.goto("https://www.reddit.com/", wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(3)
    
    # Try submitting via fetch API from within the page
    result = await pg.evaluate("""async () => {
        const formData = new URLSearchParams();
        formData.append('kind', 'self');
        formData.append('sr', 'webdev');
        formData.append('title', 'I built a directory of 200+ AI tools for content creators');
        formData.append('text', 'After months of testing, I created a curated directory at https://creatordir-tools.vercel.app with 200+ articles, reviews and comparisons.\n\nWould love feedback!');
        formData.append('api_type', 'json');
        formData.append('sendreplies', 'true');
        
        try {
            const resp = await fetch('https://www.reddit.com/api/submit', {
                method: 'POST',
                body: formData,
                credentials: 'same-origin',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            return await resp.json();
        } catch(e) {
            return {error: e.toString()};
        }
    }""")
    
    print(f"In-page API result:")
    import json
    print(json.dumps(result, indent=2)[:1500])
    
    await p.stop()

asyncio.run(main())
