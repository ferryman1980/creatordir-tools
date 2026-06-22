#!/usr/bin/env python3
"""
AI Directory Submission Script - connects to Edge CDP and submits to AI directories.
"""
import asyncio
import json
import os
from datetime import datetime
from playwright.async_api import async_playwright

EDGE_CDP_URL = "ws://127.0.0.1:9222/devtools/browser/3d547708-be2e-405e-a141-f0029cfacd1c"
SITE_NAME = "CreatorAI Tools"
SITE_URL = "https://creatordir-tools.vercel.app"
SITE_DESC = "Curated directory of 160+ AI tools for content creators"
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_FILE = os.path.join(WORK_DIR, "submission_results.json")

DIRECTORIES = [
    {"name": "AI Wizard", "url": "https://aizwizard.com/submit"},
    {"name": "AI Tool Guru", "url": "https://aitoolguru.com/submit-tool"},
    {"name": "Futurepedia", "url": "https://www.futurepedia.io/submit-tool"},
    {"name": "EasyWithAI", "url": "https://easywithai.com/submit"},
    {"name": "TopAI.tools", "url": "https://topai.tools/submit"},
    {"name": "Aixploria", "url": "https://www.aixploria.com/en/submit-tool"},
    {"name": "ToolPilot", "url": "https://toolpilot.ai/submit"},
    {"name": "That AI Collection", "url": "https://www.thataicollection.com/en/submit"},
    {"name": "AI Scout", "url": "https://aiscout.net/submit"},
    {"name": "AIContentfy", "url": "https://www.aicontentfy.com/tool-submission"},
    {"name": "SaaS AI Tools", "url": "https://saasaitools.com/submit"},
    {"name": "AI Collection", "url": "https://aicollection.org/submit"},
    {"name": "AI Top Tools", "url": "https://aitoptools.com/submit"},
    {"name": "Tools4Noobs", "url": "https://www.tools4noobs.com/submit"},
    {"name": "AI Picks", "url": "https://aipicks.io/submit"},
]

results = []

async def connect_browser():
    p = await async_playwright().start()
    browser = await p.chromium.connect_over_cdp(EDGE_CDP_URL)
    print(f"[OK] Connected to Edge CDP")
    if browser.contexts:
        context = browser.contexts[0]
    else:
        context = await browser.new_context()
    pages = context.pages
    if pages:
        page = pages[0]
    else:
        page = await context.new_page()
    return p, browser, page

async def create_github_issue(page):
    print("\n=== Step 1: Creating GitHub Issue ===")
    issue_url = "https://github.com/ferryman1980/creatordir-tools/issues/new"
    try:
        await page.goto(issue_url, timeout=30000, wait_until="domcontentloaded")
        await asyncio.sleep(3)
        print(f"  Current URL: {page.url}")
        if "issues/new" in page.url:
            # Title
            try:
                await page.fill('input[name="issue[title]"]', "Submit to 177+ AI Directories - Tracking", timeout=3000)
                print("  [OK] Title filled")
            except:
                print("  [WARN] Could not fill title")
            # Body
            body_text = "## AI Directory Submission Plan\n\nWe are submitting **CreatorAI Tools** (https://creatordir-tools.vercel.app) to 177+ AI directories.\n\n### Target Directories (30+)\n\n1. AI Wizard\n2. AI Tool Guru\n3. Futurepedia\n4. Theres An AI For That\n5. EasyWithAI\n6. TopAI.tools\n7. AI Tools Club\n8. SaaS AI Tools\n9. AI Tools Directory\n10. ToolPilot\n11. AI Scout\n12. Aixploria\n13. That AI Collection\n14. AI Collection\n15. AI Top Tools\n16. Tools4Noobs\n17. AI Picks\n18. AIContentfy\n\n### Details\n\n- **Site Name:** CreatorAI Tools\n- **URL:** https://creatordir-tools.vercel.app\n- **Description:** Curated directory of 160+ AI tools for content creators\n- **Started:** 2026-06-23\n- **Batch 1:** 18 directories\n"
            try:
                await page.fill('textarea[name="issue[body]"]', body_text, timeout=3000)
                print("  [OK] Body filled")
            except:
                try:
                    await page.keyboard.type(body_text, delay=5)
                    print("  [OK] Body typed via keyboard")
                except:
                    print("  [WARN] Could not fill body")
            # Submit
            try:
                btn = page.get_by_role("button", name="Submit new issue")
                if await btn.count() > 0:
                    await btn.click()
                    await asyncio.sleep(3)
                    print("  [OK] Issue submitted")
            except:
                print("  [WARN] No submit button found")
            return {"status": "done", "url": page.url}
        else:
            print(f"  [WARN] Not on issue page: {page.url}")
            return {"status": "navigate_only", "url": page.url}
    except Exception as e:
        print(f"  [ERROR] {e}")
        return {"status": "error", "error": str(e)}

async def fill_submit(page, dir_info):
    name = dir_info["name"]
    url = dir_info["url"]
    print(f"\n  --- {name}: {url} ---")
    result = {"status": "pending", "time": datetime.now().isoformat(), "fields_found": {"name": False, "url": False, "description": False}, "submitted": False, "final_url": ""}
    try:
        await page.goto(url, timeout=30000, wait_until="domcontentloaded")
        await asyncio.sleep(3)
        result["final_url"] = page.url
        print(f"  Loaded: {page.url}")
        # Name
        for sel in ['input[name*="name" i]', 'input[placeholder*="name" i]', 'input[placeholder*="tool" i]', 'input[id*="name" i]', 'input[placeholder*="site" i]']:
            try:
                el = await page.wait_for_selector(sel, timeout=500)
                if el and await el.is_visible():
                    await el.fill(SITE_NAME); result["fields_found"]["name"] = True; print(f"  [OK] Name"); break
            except:
                continue
        # URL
        for sel in ['input[name*="url" i]', 'input[name*="website" i]', 'input[placeholder*="url" i]', 'input[placeholder*="website" i]', 'input[id*="url" i]', 'input[type="url"]']:
            try:
                el = await page.wait_for_selector(sel, timeout=500)
                if el and await el.is_visible():
                    await el.fill(SITE_URL); result["fields_found"]["url"] = True; print(f"  [OK] URL"); break
            except:
                continue
        # Description
        for sel in ['textarea[name*="desc" i]', 'textarea[placeholder*="desc" i]', 'input[name*="desc" i]', 'textarea[id*="desc" i]', 'textarea[placeholder*="about" i]', 'textarea[placeholder*="short" i]']:
            try:
                el = await page.wait_for_selector(sel, timeout=500)
                if el and await el.is_visible():
                    await el.fill(SITE_DESC); result["fields_found"]["description"] = True; print(f"  [OK] Desc"); break
            except:
                continue
        # Submit button
        for sel in ['button[type="submit"]', 'input[type="submit"]', 'button:has-text("Submit")', 'button:has-text("submit")', 'button:has-text("Add")', 'button:has-text("Send")', 'button:has-text("Save")', 'button:has-text("Publish")', 'button:has-text("List")']:
            try:
                btn = await page.wait_for_selector(sel, timeout=800)
                if btn and await btn.is_visible():
                    await btn.click(); await asyncio.sleep(3); result["submitted"] = True; print(f"  [OK] Submit"); break
            except:
                continue
        result["status"] = "submitted" if result["submitted"] else "filled"
        print(f"  -> {result['status']}")
    except Exception as e:
        result["status"] = "error"; result["error"] = str(e); print(f"  [ERROR] {e}")
    return result

async def main():
    print("=" * 60)
    print("AI Directory Submission Bot")
    print("=" * 60)
    p, browser, page = await connect_browser()
    try:
        issue_result = await create_github_issue(page)
        results.append({"step": "github_issue", "result": issue_result})
        print("\n\n=== Step 2: Submitting to AI Directories ===")
        for i, dir_info in enumerate(DIRECTORIES, 1):
            print(f"\n[{i}/{len(DIRECTORIES)}] ", end="")
            dir_result = await fill_submit(page, dir_info)
            results.append({"step": f"submit_{i}", "dir": dir_info["name"], "result": dir_result})
            with open(RESULTS_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
        print("\n\n=== Summary ===")
        sc = sum(1 for r in results if r.get("result",{}).get("status")=="submitted")
        fc = sum(1 for r in results if r.get("result",{}).get("status")=="filled")
        ec = sum(1 for r in results if r.get("result",{}).get("status")=="error")
        print(f"  Submitted: {sc}, Filled: {fc}, Errors: {ec}")
    finally:
        await browser.close()
        await p.stop()

if __name__ == "__main__":
    asyncio.run(main())
