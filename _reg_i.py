import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = await ctx.new_page()
    await pg.goto("https://app.impact.com/auth/signup",wait_until="domcontentloaded",timeout=15000)
    await pg.wait_for_timeout(2000)
    print(await pg.title())
    inputs = await pg.query_selector_all('input')
    for inp in inputs:
        try:
            t = await inp.get_attribute('type')
            if t and t == 'email':
                await inp.fill('346010735@qq.com')
                print('  - email filled')
                break
        except: pass
    await p.stop()

asyncio.run(main())
