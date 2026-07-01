import asyncio  
from playwright.async_api import async_playwright  
  
async def main():  
    p = await async_playwright().start()  
    edge = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')  
    ctx = edge.contexts[0]  
    urls = [  
        ('Namecheap','https://www.namecheap.com/affiliates/apply/'),  
        ('Shopify','https://www.shopify.com/affiliates'),  
        ('ConvertKit','https://kit.com/affiliate'),  
        ('Grammarly','https://www.grammarly.com/affiliates'),  
    ]  
    for name, url in urls:  
        pg = await ctx.new_page()  
        await pg.goto(url,wait_until='domcontentloaded',timeout=15000)  
        await pg.wait_for_timeout(2000)  
        print(name + ': ' + await pg.title())  
    await p.stop()  
asyncio.run(main()) 
