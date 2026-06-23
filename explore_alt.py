import asyncio, json
from playwright.async_api import async_playwright

# Known AI directories with better chance of direct submission
DIRS = [
    ("AIxploria_alt", "https://www.aixploria.com/en/submit-a-tool/"),  # Try alternative URL
    ("AIPicks_co", "https://aipicks.co/submit-tool/"),
    ("EasyWithAI_alt", "https://easywithai.com/submit/"),
    ("AI_Scout_alt", "https://aiscout.net/submit"),
    ("ToolsPilot_alt", "https://toolpilot.ai/submit"),
    ("Futurepedia", "https://www.futurepedia.io/submit-a-tool"),
]

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        results = []
        
        for name, url in DIRS:
            page = await browser.new_page()
            res = {"name": name, "url": url, "status": "pending"}
            try:
                resp = await page.goto(url, timeout=20000, wait_until="domcontentloaded")
                await asyncio.sleep(3)
                title = await page.title()
                txt = (await page.content()).lower()
                
                has_form = "<form" in txt
                needs_login = any(kw in txt for kw in ["sign in", "signin", "log in", "login", "register"])
                inp_count = txt.count("<input")
                status_code = resp.status if resp else "N/A"
                
                print(f"[{name}] {status_code} | {title[:40]} | Form:{has_form} | Login:{needs_login}")
                res.update({"status_code": status_code, "title": title[:60], "has_form": has_form, "needs_login": needs_login, "input_count": inp_count})
                
            except Exception as e:
                print(f"[{name}] FAIL | {str(e)[:60]}")
                res["error"] = str(e)[:60]
            results.append(res)
            await page.close()
        
        print("\n=== RESULTS ===")
        for r in results:
            if r.get("needs_login"):
                print(f"  🔒 {r['name']}: Login required")
            elif "error" in r:
                print(f"  ❌ {r['name']}: {r['error']}")
            else:
                print(f"  🔓 {r['name']}: Possible - {r.get('title')} ({r.get('status_code')})")
        
        await browser.close()

asyncio.run(run())
