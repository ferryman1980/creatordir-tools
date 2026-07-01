import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

EMAIL = '346010735@qq.com'
PWD = 'Ckyhy388$'
SITE = 'https://creatordir-tools.vercel.app'

async def main():
    p = await async_playwright().start()
    b = await p.chromium.launch(channel='msedge', headless=False)
    ctx = await b.new_context()
    
    targets = [
        ('Grammarly', 'https://www.grammarly.com/signup'),
        ('Shopify', 'https://accounts.shopify.com/signup'),
        ('ConvertKit', 'https://kit.com/register'),
        ('WPForms', 'https://wpforms.com/affiliate-application/'),
        ('Awin', 'https://www.awin.com/gb/affiliates/register'),
    ]
    
    for name, url in targets:
        pg = await ctx.new_page()
        try:
            await pg.goto(url, wait_until='domcontentloaded', timeout=15000)
            await pg.wait_for_timeout(2000)
            
            # Fill email
            for s in ['input[type="email"]', 'input[name*="email"]', 'input[id*="email"]', 'input[placeholder*="email" i]']:
                el = await pg.query_selector(s)
                if el and await el.is_visible():
                    await el.fill(EMAIL)
                    print(f'{name}: email filled')
                    break
            
            # Fill password
            for s in ['input[type="password"]']:
                el = await pg.query_selector(s)
                if el and await el.is_visible():
                    await el.fill(PWD)
                    print(f'{name}: password filled')
                    break
            
            print(f'{name}: {(await pg.title())[:50]}')
        except Exception as e:
            print(f'{name}: ERROR {str(e)[:40]}')
    
    await p.stop()

asyncio.run(main())

