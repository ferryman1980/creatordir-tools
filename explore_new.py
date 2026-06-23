import asyncio, json, os, re
from playwright.async_api import async_playwright

# Target directories with corrected/submit URLs
SUBMIT_LIST = [
    # Already confirmed as working directories - try submitting
    ("AIxploria", "https://www.aixploria.com/en/submit-tool", "Possible form on page"),
    # More directories from checklist to try
    ("ToolScout", "https://toolscout.com/submit", "New"),
    ("AIContentfy", "https://aicontentfy.com/submit", "New"),
    ("SaaS_AI_Tools", "https://saasaitools.com/submit/", "New"),
    ("AIToolsClub", "https://aitoolsclub.com/submit/", "New"),
    ("AIPicks", "https://aipicks.co/submit/", "New"),
    ("AIToolGuru", "https://aitoolguru.com/submit/", "New"),
    ("AIWizard", "https://aiwizard.me/submit", "New"),
    ("AICollection", "https://aicollection.com/submit/", "New"),
    ("ThereAIForThat", "https://theresanaiforthat.com/submit/", "Has form, needs check"),
]

async def try_submit():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = browser.contexts[0] if browser.contexts else await browser.new_context()
        results = {}
        
        for name, url, note in SUBMIT_LIST:
            result = {"url": url, "note": note, "status": "pending"}
            page = None
            try:
                page = await ctx.new_page()
                resp = await page.goto(url, timeout=20000, wait_until="domcontentloaded")
                await asyncio.sleep(3)
                
                title = await page.title()
                html = await page.content()
                txt = html.lower()
                status_code = resp.status if resp else "N/A"
                
                # Check for form
                has_form = "<form" in txt
                inp_count = txt.count("<input")
                has_submit_btn = any(kw in txt for kw in ["submit", "send", "add your"])
                needs_login = any(kw in txt for kw in ["sign in", "signin", "log in", "login"])
                
                result.update({
                    "title": title[:80],
                    "status_code": status_code,
                    "has_form": has_form,
                    "input_count": inp_count,
                    "needs_login": needs_login,
                })
                
                safe_name = name.replace(" ", "")
                shot_path = os.path.join(r"D:\项目\工作区\工作5", f"shot2_{safe_name}.png")
                await page.screenshot(path=shot_path)
                
                print(f"[{name}] HTTP:{status_code} | Form:{has_form} | Inputs:{inp_count} | Login:{needs_login}")
                
            except Exception as e:
                result.update({"title": "ERROR", "error": str(e)[:80]})
                print(f"[{name}] Error: {str(e)[:60]}")
            
            results[name] = result
            if page:
                try:
                    await page.close()
                except:
                    pass
        
        with open(r"D:\项目\工作区\工作5\explore_new.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print("\n=== NEW DIRECTORIES SUMMARY ===")
        for n, r in results.items():
            if "error" in r:
                print(f"  ERROR {n}")
            elif r.get("needs_login"):
                print(f"  LOGIN {n}: {r.get('title', '?')[:40]}")
            else:
                print(f"  OPEN  {n}: {r.get('title', '?')[:40]}")
        
        await browser.close()

asyncio.run(try_submit())
