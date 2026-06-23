import asyncio
from playwright.async_api import async_playwright

SITE_NAME = "CreatorAI Tools"
SITE_URL = "https://creatordir-tools.vercel.app"
SITE_DESC = "Curated directory of 200+ AI tools for content creators with honest reviews, comparisons, and tutorials."
SITE_EMAIL = "346010735@qq.com"
SITE_CAT = "AI Tools Directory"

DIRS = [
    {"name": "TopAI.tools", "url": "https://www.topai.tools/submit"},
    {"name": "AlternativeTo", "url": "https://alternativeto.net/submit-tool/"},
    {"name": "ThereAIForThat", "url": "https://theresanaiforthat.com/submit/"},
    {"name": "AI Scout", "url": "https://aiscout.net/submit-tool/"},
    {"name": "EasyWithAI", "url": "https://easywithai.com/submit-a-tool/"},
]

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    results = []
    for d in DIRS:
        print(f"\n=== {d['name']} ===")
        try:
            pg = await ctx.new_page()
            await pg.goto(d["url"], wait_until="domcontentloaded", timeout=20000)
            await pg.wait_for_timeout(3000)
            text = await pg.evaluate("document.body.innerText")
            print(text[:400])
            await pg.close()
            results.append(f"{d['name']}: OK")
        except Exception as e:
            print(f"Error: {str(e)[:100]}")
            results.append(f"{d['name']}: {str(e)[:60]}")
    
    print("\n=== SUMMARY ===")
    for r in results:
        print(f"  {r}")
    await p.stop()

asyncio.run(main())
