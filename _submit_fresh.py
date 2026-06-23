
import asyncio, sys, re
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

SITE = "https://creatordir-tools.vercel.app"
NAME = "CreatorAI Tools"
DESC = "Curated directory of 200+ AI tools for content creators"
EMAIL = "346010735@qq.com"

# Directories with known working submission forms
DIRS = [
    # (name, url)
    ("ThatAICollection", "https://thataicollection.com/en/submit/"),
    ("AIxploria", "https://www.aixploria.com/en/submit-tool"),
    ("AlternativeTo", "https://alternativeto.net/submit-tool/"),
]

async def try_submit(page, name, url):
    print(f"\n=== {name} ===")
    print(f"URL: {url}")
    result = {"name": name, "url": url, "status": "unknown"}
    
    try:
        await page.goto(url, timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        print(f"Title: {await page.title()}")
        await page.evaluate("window.scrollTo(0, 300)")
        await page.wait_for_timeout(1000)
        
        # Check if there's a submit button we need to click first to show form
        buttons_text = await page.evaluate("""
            () => Array.from(document.querySelectorAll("button,a"))
                .filter(el => el.offsetParent !== null)
                .map(el => (el.innerText || el.textContent || "").trim().toLowerCase().substring(0, 25))
                .filter(t => t.length > 0)
        """)
        
        submit_buttons = [b for b in buttons_text if any(w in b for w in ["submit","add","list","create","add your"])]
        if submit_buttons:
            print(f"Found submit buttons: {submit_buttons[:3]}")
        
        # Find visible form fields
        fields = await page.evaluate("""
            () => {
                const els = document.querySelectorAll("input:not([type=hidden]):not([type=checkbox]):not([type=radio]), textarea, select");
                return Array.from(els)
                    .filter(el => el.offsetParent !== null)
                    .map(el => ({
                        tag: el.tagName,
                        type: el.type || "",
                        name: el.name || "",
                        id: el.id || "",
                        placeholder: el.placeholder || "",
                        label: (el.labels && el.labels[0] ? el.labels[0].innerText : "") || "",
                        aria: el.getAttribute("aria-label") || ""
                    }));
            }
        """)
        
        print(f"Visible fields: {len(fields)}")
        
        # Fill each field
        for f in fields:
            combined = (f["name"] + " " + f["id"] + " " + f["placeholder"] + " " + f["label"] + " " + f["aria"]).lower()
            value = None
            if "name" in combined or "title" in combined:
                value = NAME
            elif "url" in combined or "website" in combined or "link" in combined or "site" in combined:
                value = SITE
            elif "desc" in combined or "about" in combined or "summary" in combined:
                value = DESC
            elif "email" in combined:
                value = EMAIL
            elif "tag" in combined or "keyword" in combined:
                value = "AI tools, content creation"
            elif "category" in combined:
                value = "AI Tools Directory"
            
            if value:
                selector = f"#{f['id']}" if f["id"] else f"[name='{f['name']}']" if f["name"] else f"[placeholder='{f['placeholder']}']"
                try:
                    el = await page.query_selector(selector)
                    if el:
                        await el.fill(value)
                        print(f"  Filled {f['name'] or f['placeholder']}: {value[:25]}")
                except:
                    pass
        
        # Try submit
        try:
            btn = await page.query_selector("button[type=submit], input[type=submit], button:has-text('Submit'), button:has-text('Add'), button:has-text('List')")
            if btn:
                await btn.click()
                await page.wait_for_timeout(3000)
                result["status"] = "submitted"
                result["final_url"] = page.url
                print(f"SUBMITTED! URL: {page.url[:70]}")
            else:
                result["status"] = "no_button"
                print("No submit button found")
        except Exception as e:
            result["status"] = "click_error"
            print(f"Click error: {str(e)[:40]}")
        
    except Exception as e:
        result["status"] = "error"
        print(f"Error: {str(e)[:60]}")
    
    return result

async def main():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        for name, url in DIRS:
            r = await try_submit(page, name, url)
            results.append(r)
            await page.wait_for_timeout(2000)
        
        await browser.close()
    
    print(f"\n=== FINAL RESULTS ===")
    for r in results:
        icon = "✅" if r["status"] == "submitted" else "❌"
        print(f"{icon} {r['name']}: {r['status']}")
    
    import json, os
    out = os.path.join(os.path.dirname(__file__) or ".", "submission_results_v3.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {out}")

asyncio.run(main())
