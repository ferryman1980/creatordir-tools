
import asyncio, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

SITE_URL = "https://creatordir-tools.vercel.app"
SITE_NAME = "CreatorAI Tools"
SITE_DESC = "Curated directory of 200+ AI tools for content creators"
SITE_EMAIL = "346010735@qq.com"

DIRECTORIES = [
    ("Futurepedia", "https://www.futurepedia.io/submit-tool"),
    ("EasyWithAI", "https://easywithai.com/submit"),
    ("TopAI.tools", "https://topai.tools/submit"),
    ("ToolPilot", "https://toolpilot.ai/submit"),
    ("AI Scout", "https://aiscout.net/submit"),
    ("ThereAIForThat", "https://theresanaiforthat.com/submit/"),
    ("AITopTools", "https://aitoptools.com/submit"),
]

async def main():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        for name, url in DIRECTORIES:
            print(f"\n=== {name} ===")
            r = {"name": name, "url": url, "status": "pending"}
            try:
                await page.goto(url, timeout=20000, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)
                title = await page.title()
                print(f"  Title: {title}")
                inputs = await page.query_selector_all('input[type="text"], input[type="url"], input[type="email"], textarea')
                filled = []
                for inp in inputs:
                    ph = (await inp.get_attribute("placeholder") or "").lower()
                    na = (await inp.get_attribute("name") or "").lower()
                    idi = (await inp.get_attribute("id") or "").lower()
                    cx = ph + " " + na + " " + idi
                    if any(w in cx for w in ["name","title","tool"]):
                        await inp.fill(SITE_NAME); filled.append("name")
                    elif any(w in cx for w in ["url","website","link","site"]):
                        await inp.fill(SITE_URL); filled.append("url")
                    elif any(w in cx for w in ["desc","about","detail","summary"]):
                        await inp.fill(SITE_DESC); filled.append("desc")
                    elif any(w in cx for w in ["email","mail"]):
                        await inp.fill(SITE_EMAIL); filled.append("email")
                r["fields"] = filled
                print(f"  Fields: {filled}")
                btns = await page.query_selector_all('button[type="submit"], input[type="submit"], button:has-text("Submit"), button:has-text("Add"), button:has-text("List Tool")')
                if btns:
                    await btns[0].click()
                    await page.wait_for_timeout(4000)
                    r["status"] = "submitted"
                    r["final_url"] = page.url
                    print(f"  SUBMITTED! URL: {page.url}")
                else:
                    r["status"] = "no_button"
                    print(f"  No submit button")
            except Exception as e:
                r["status"] = "error"
                r["error"] = str(e)[:100]
                print(f"  Error: {str(e)[:80]}")
            results.append(r)
            await page.wait_for_timeout(2000)
        await browser.close()
    print(f"\n=== RESULTS ===")
    for r in results:
        icon = "OK" if r["status"] == "submitted" else r["status"]
        print(f"  {r['name']}: {icon}")
    out = os.path.join(os.path.dirname(__file__) if "__file__" in dir() else ".", "submission_results_v2.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Done")

asyncio.run(main())
