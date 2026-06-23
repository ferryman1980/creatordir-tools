import asyncio, json, os
from playwright.async_api import async_playwright

DIRECTORIES = [
    ("ThatAICollection", "https://thataicollection.com/en/submit/", "Has login form"),
    ("AIxploria", "https://www.aixploria.com/en/submit-tool", "Page not found - check URL"),
    ("SaaS Hub", "https://www.saashub.com/submit", "Needs account"),
    ("TopAI.tools", "https://www.topai.tools/submit", "DNS fail"),
    ("AlternativeTo", "https://alternativeto.net/submit-tool/", "Need to check"),
    ("Futurepedia", "https://www.futurepedia.io/submit-tool", "Need to check"),
    ("EasyWithAI", "https://easywithai.com/submit-ai-tool/", "Need to check"),
    ("AIScout", "https://aiscout.net/submit/", "Need to check"),
    ("AITopTools", "https://aitoptools.com/submit/", "Need to check"),
    ("ThereAIForThat", "https://theresanaiforthat.com/submit/", "Need to check"),
]

async def explore_all():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = browser.contexts[0] if browser.contexts else await browser.new_context()
        all_results = {}
        
        for name, url, note in DIRECTORIES:
            result = {"url": url, "note": note, "status": "pending"}
            page = None
            try:
                page = await ctx.new_page()
                resp = await page.goto(url, timeout=20000, wait_until="domcontentloaded")
                await asyncio.sleep(3)
                
                title = await page.title()
                html = await page.content()
                txt = html.lower()
                
                has_form = "<form" in txt
                inp_count = txt.count("<input")
                has_submit = any(kw in txt for kw in ["submit", "send", "add your"])
                needs_login = any(kw in txt for kw in ["sign in", "signin", "log in", "login"])
                
                result.update({
                    "title": title,
                    "status_code": resp.status if resp else "N/A",
                    "has_form_tag": has_form,
                    "input_count": inp_count,
                    "has_submit_btn": has_submit,
                    "needs_login": needs_login,
                })
                
                safe_name = name.replace(" ", "")
                shot_path = os.path.join(r"D:\项目\工作区\工作5", f"screenshot_{safe_name}.png")
                await page.screenshot(path=shot_path)
                
                print(f"[{name}] Title: {title[:50]} | Form: {has_form} | Login: {needs_login}")
                
            except Exception as e:
                result.update({"title": "ERROR", "error": str(e)[:100]})
                print(f"[{name}] Error: {str(e)[:80]}")
            
            all_results[name] = result
            if page:
                try:
                    await page.close()
                except:
                    pass
        
        with open(r"D:\项目\工作区\工作5\explore_all.json", "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        
        print("\n=== SUMMARY ===")
        for n, r in all_results.items():
            e = "ERROR" if "error" in r else "OK"
            lk = "LOGIN" if r.get("needs_login") else "OPEN"
            print(f"  {e} [{lk}] {n}: {r.get('title', '?')[:40]}")
        
        await browser.close()

asyncio.run(explore_all())
