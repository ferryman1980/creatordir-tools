import asyncio
from playwright.async_api import async_playwright

EMAIL = "346010735@qq.com"
PWD = "Ckyhy388$"
SITE = "https://creatordir-tools.vercel.app"
NAME = "kangjian"

async def fill_email(page):
    for s in ['input[type="email"]', 'input[name*="email" i]', 'input[id*="email" i]']:
        try: el = await page.query_selector(s); 
        if el: 
            await el.fill(EMAIL); 
            return True
        except: pass
    return False

async def fill_site(page):
    for s in ['input[name*="site" i]', 'input[name*="url" i]', 'input[name*="web" i]', 'input[placeholder*="site" i]', 'input[placeholder*="url" i]']:
        try: el = await page.query_selector(s);
        if el:
            await el.fill(SITE);
            return True
        except: pass
    return False

async def click_btn(page, texts):
    for t in texts:
        for s in [f'button:has-text("{t}")', f'a:has-text("{t}")', f'input[type="submit"][value*="{t}" i]']:
            try: el = await page.query_selector(s);
            if el:
                await el.click();
                await page.wait_for_timeout(2000);
                return True
            except: pass
    return False

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    # Close existing tabs except first
    for pg in ctx.pages[1:]:
        try:
            if "dev.to" not in pg.url and "zeabur" not in pg.url:
                await pg.close()
        except: pass
    
    results = []
    
    # 1. Namecheap - try signup page
    try:
        pg = await ctx.new_page()
        await pg.goto("https://www.namecheap.com/affiliates/apply/", wait_until="domcontentloaded", timeout=15000)
        await pg.wait_for_timeout(2000)
        t = await pg.title()
        await fill_email(pg)
        await fill_site(pg)
        await click_btn(pg, ["Apply", "Sign Up", "Join", "Submit", "Get Started"])
        results.append(f"Namecheap: {t}")
        await pg.close()
    except Exception as e:
        results.append(f"Namecheap: ERR {str(e)[:40]}")
    
    # 2. Shopify - has form
    try:
        pg = await ctx.new_page()
        await pg.goto("https://www.shopify.com/affiliates", wait_until="domcontentloaded", timeout=15000)
        await pg.wait_for_timeout(2000)
        t = await pg.title()
        await click_btn(pg, ["Join", "Get started", "Sign up", "Apply"])
        await pg.wait_for_timeout(2000)
        await fill_email(pg)
        results.append(f"Shopify: {t}")
        await pg.close()
    except Exception as e:
        results.append(f"Shopify: ERR {str(e)[:40]}")
    
    # 3. ConvertKit
    try:
        pg = await ctx.new_page()
        await pg.goto("https://kit.com/affiliate", wait_until="domcontentloaded", timeout=15000)
        await pg.wait_for_timeout(2000)
        t = await pg.title()
        await click_btn(pg, ["Join", "Apply", "Get started", "Sign up"])
        results.append(f"ConvertKit: {t}")
        await pg.close()
    except Exception as e:
        results.append(f"ConvertKit: ERR {str(e)[:40]}")
    
    # 4. Grammarly
    try:
        pg = await ctx.new_page()
        await pg.goto("https://www.grammarly.com/affiliates", wait_until="domcontentloaded", timeout=15000)
        await pg.wait_for_timeout(2000)
        t = await pg.title()
        await click_btn(pg, ["Join", "Apply", "Get started", "Become"])
        results.append(f"Grammarly: {t}")
        await pg.close()
    except Exception as e:
        results.append(f"Grammarly: ERR {str(e)[:40]}")
    
    # 5. Elegant Themes
    try:
        pg = await ctx.new_page()
        await pg.goto("https://www.elegantthemes.com/affiliates/", wait_until="domcontentloaded", timeout=15000)
        await pg.wait_for_timeout(2000)
        t = await pg.title()
        await click_btn(pg, ["Sign Up", "Join", "Apply", "Register"])
        await fill_email(pg)
        results.append(f"ElegantThemes: {t}")
        await pg.close()
    except Exception as e:
        results.append(f"ElegantThemes: ERR {str(e)[:40]}")
    
    # 6. WPForms
    try:
        pg = await ctx.new_page()
        await pg.goto("https://wpforms.com/affiliates/", wait_until="domcontentloaded", timeout=15000)
        await pg.wait_for_timeout(2000)
        t = await pg.title()
        await click_btn(pg, ["Get Started", "Join", "Apply", "Register"])
        await fill_email(pg)
        results.append(f"WPForms: {t}")
        await pg.close()
    except Exception as e:
        results.append(f"WPForms: ERR {str(e)[:40]}")
    
    # 7. Bluehost 
    try:
        pg = await ctx.new_page()
        await pg.goto("https://bluehost.com/affiliates", wait_until="domcontentloaded", timeout=15000)
        await pg.wait_for_timeout(2000)
        t = await pg.title()
        await click_btn(pg, ["Apply", "Join", "Sign Up", "Get Started"])
        results.append(f"Bluehost: {t}")
        await pg.close()
    except Exception as e:
        results.append(f"Bluehost: ERR {str(e)[:40]}")
    
    # 8. HostGator
    try:
        pg = await ctx.new_page()
        await pg.goto("https://www.hostgator.com/affiliates", wait_until="domcontentloaded", timeout=15000)
        await pg.wait_for_timeout(2000)
        t = await pg.title()
        await click_btn(pg, ["Apply", "Join", "Sign Up", "Get Started"])
        results.append(f"HostGator: {t}")
        await pg.close()
    except Exception as e:
        results.append(f"HostGator: ERR {str(e)[:40]}")
    
    print("\n=== REGISTRATION RESULTS ===")
    for r in results:
        print(f"  {r}")
    print("============================")
    
    await p.stop()

asyncio.run(main())
