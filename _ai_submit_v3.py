# -*- coding: utf-8 -*-
import asyncio, os, re, sys
from playwright.async_api import async_playwright

SITE_URL = "https://creatordir-tools.vercel.app"
SITE_NAME = "CreatorAI Tools"
SITE_DESC = "Curated directory of 200+ AI tools for content creators"
EMAIL = "346010735@qq.com"
RESULT_FILE = "D:/项目/工作区/工作5/submission_results_v2.txt"
SCR_DIR = "D:/项目/工作区/工作5/screenshots"
os.makedirs(SCR_DIR, exist_ok=True)

VERIFY_DIRS = [
    ("Doforai", "https://doforai.tools/submit"),
    ("AI To Grow", "https://aitogrow.com/#send-your-tool"),
    ("AI Valley", "https://aivalley.ai/submit-tool"),
    ("Best AI To", "https://bestaito.com/submit-a-ai-tool"),
    ("FindMyAITool", "https://findmyaitool.com/submit-tool"),
    ("Insidr AI", "https://www.insidr.ai/submit-tools/"),
    ("SAAS AI Tools", "https://saasaitools.com/submit/"),
    ("TheAIGeneration", "https://www.theaigeneration.com/add/"),
    ("Toolio", "https://toolio.ai/submit-a-tool"),
    ("Tools AI Online", "https://www.tools-ai.online/tool-submit"),
    ("NextPedia", "https://www.nextpedia.io/submit-tool"),
    ("Tool Directory AI", "https://tooldirectory.ai/submit-tool"),
]

SUBMIT_SELECTORS = [
    "button[type=submit]", "input[type=submit]",
    "button:has-text(Submit)", "button:has-text(submit)",
    "button:has-text(Add Tool)", "button:has-text(Send)",
    "button:has-text(Publish)", "button:has-text(Save)",
    "button:has-text(Post)", "button:has-text(Done)",
    "button:has-text(Continue)", "button:has-text(Next)",
    "button:has-text(Get Listed)", "button:has-text(Join)",
    "a:has-text(Submit)", "[class*=submit]", "[class*=btn]",
]


async def process_one(name, url):
    result = {"name": name, "url": url, "status": "error", "note": ""}
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            ctx = browser.contexts[0] if browser.contexts else await browser.new_context()
            page = await ctx.new_page()
            
            await page.goto(url, timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)
            body_text = (await page.inner_text("body")).lower()[:2000]
            needs_login = any(kw in body_text for kw in ["sign in", "log in", "login", "register", "create account", "password"])
            inputs = await page.query_selector_all('input:not([type=hidden]):not([type=radio]):not([type=checkbox]), textarea')
            
            if needs_login and len(inputs) == 0:
                result["status"] = "login_required"
                return result

            if len(inputs) > 0:
                filled = 0
                for inp in inputs[:10]:
                    try:
                        t = (await inp.get_attribute("type") or "").lower()
                        nm = (await inp.get_attribute("name") or "").lower()
                        iid = (await inp.get_attribute("id") or "").lower()
                        ph = (await inp.get_attribute("placeholder") or "").lower()
                        combined = nm + iid + ph + t
                        val = None
                        if any(k in combined for k in ["url", "website", "link", "site"]):
                            val = SITE_URL
                        elif any(k in combined for k in ["email", "mail"]):
                            val = EMAIL
                        elif any(k in combined for k in ["name", "title", "tool"]):
                            val = SITE_NAME
                        elif any(k in combined for k in ["desc", "detail", "about"]):
                            val = SITE_DESC
                        elif t == "url":
                            val = SITE_URL
                        elif t == "email":
                            val = EMAIL
                        if val:
                            await inp.click()
                            await inp.fill(val)
                            filled += 1
                    except:
                        pass
                
                if filled > 0:
                    await page.wait_for_timeout(1000)
                    submit_clicked = False
                    for sel in SUBMIT_SELECTORS:
                        try:
                            btns = await page.query_selector_all(sel)
                            for btn in btns:
                                try:
                                    if not (await btn.is_visible()):
                                        continue
                                    b_text = (await btn.inner_text()).strip().lower()
                                    if any(s in b_text for s in ["login", "register", "sign", "cancel", "reset", "search"]):
                                        continue
                                    await btn.click()
                                    submit_clicked = True
                                    await page.wait_for_timeout(4000)
                                    break
                                except:
                                    continue
                            if submit_clicked:
                                break
                        except:
                            continue
                    
                    if submit_clicked:
                        await page.wait_for_timeout(3000)
                        try:
                            body = (await page.inner_text("body")).lower()
                            confirmed = any(kw in body for kw in ["thank", "submitted", "success", "received", "pending review"])
                            if confirmed:
                                result["status"] = "submitted"
                                result["note"] = "Filled " + str(filled) + " fields and submitted!"
                            else:
                                result["status"] = "submit_clicked"
                                result["note"] = "Filled " + str(filled) + " fields + clicked"
                        except:
                            result["status"] = "submit_clicked"
                            result["note"] = "Filled " + str(filled) + " fields + clicked"
                    else:
                        result["status"] = "form_filled"
                        result["note"] = "Filled " + str(filled) + " fields, no submit"
                else:
                    result["status"] = "form_found_empty"
            else:
                result["status"] = "no_form"
            
            sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", name)[:30]
            try:
                await page.screenshot(path=SCR_DIR + "/" + sanitized + ".png", full_page=True)
            except:
                pass
            await page.close()
            await browser.close()
        except Exception as e:
            result["status"] = "error"
            result["note"] = str(e)[:200]
    return result


async def main():
    results = []
    total = len(VERIFY_DIRS)
    print("Processing " + str(total) + " directories...")
    for i, (name, url) in enumerate(VERIFY_DIRS, 1):
        sys.stdout.write("  [" + str(i) + "/" + str(total) + "] " + name + "...")
        sys.stdout.flush()
        r = await process_one(name, url)
        results.append(r)
        print(" " + r["status"])
        await asyncio.sleep(2)
    
    submitted = [r for r in results if r["status"] == "submitted"]
    clicked = [r for r in results if r["status"] == "submit_clicked"]
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        f.write("AI Directory Submission v3\n")
        f.write("=" * 50 + "\n")
        f.write("Site: " + SITE_URL + "\nEmail: " + EMAIL + "\n\n")
        f.write("SUBMITTED (" + str(len(submitted)) + "):\n")
        f.write("-" * 40 + "\n")
        for r in submitted:
            f.write("  " + r["name"] + " | " + r["note"] + "\n")
        f.write("\nSUBMIT CLICKED (" + str(len(clicked)) + "):\n")
        f.write("-" * 40 + "\n")
        for r in clicked:
            f.write("  " + r["name"] + " | " + r["note"] + "\n")
        f.write("\nALL:\n")
        f.write("-" * 40 + "\n")
        for r in results:
            f.write(r["status"].ljust(20) + " | " + r["name"].ljust(25) + " | " + r["note"][:70] + "\n")
        f.write("\nTotal: " + str(len(results)) + " | Submitted: " + str(len(submitted)) + " | Clicked: " + str(len(clicked)) + "\n")
    print("\nDone! " + str(len(submitted)) + " submitted, " + str(len(clicked)) + " click-pending")

if __name__ == "__main__":
    asyncio.run(main())
