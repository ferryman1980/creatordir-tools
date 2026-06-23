# -*- coding: utf-8 -*-
"""AI Directory Batch Submission Script"""
import asyncio, json, os, re, time
from playwright.async_api import async_playwright

SITE_URL = "https://creatordir-tools.vercel.app"
SITE_NAME = "CreatorAI Tools"
SITE_DESC = "Curated directory of 200+ AI tools for content creators with honest reviews, comparisons, and tutorials."
EMAIL = "346010735@qq.com"
RESULT_FILE = "D:\\u9879\\u76ee\\u5de5\\u4f5c\\u533a\\u5de5\\u4f5c5\\submission_results.txt"
SCR_DIR = "D:\\u9879\\u76ee\\u5de5\\u4f5c\\u533a\\u5de5\\u4f5c5\\screenshots"
os.makedirs(SCR_DIR, exist_ok=True)

DIRS = [
    ("SubmitAI","https://submitaitools.org/submit-your-ai-tool/"),
    ("Doforai","https://doforai.tools/submit"),
    ("AI To Grow","https://aitogrow.com/#send-your-tool"),
    ("AI Tool Board","https://aitoolboard.com/submit-ai-tool"),
    ("AI Trendz","https://aitrendz.xyz/submit-ai-link"),
    ("AI Valley","https://aivalley.ai/submit-tool"),
    ("AI Wizard","https://www.aiwizard.ai/submit"),
    ("AIX Collection","https://aixcollection.com/submit"),
    ("AllThingsAI","https://allthingsai.com/submit"),
    ("Best AI To","https://bestaito.com/submit-a-ai-tool"),
    ("Faind AI","https://faind.ai/submit-a-tool"),
    ("Fazier","https://fazier.com/submit"),
    ("FindMyAITool","https://findmyaitool.com/submit-tool"),
    ("Free AI Apps","https://freeappsai.com/add"),
    ("Free AI Tools Dir","https://free-ai-tools-directory.com/submit-request"),
    ("Future AGI Tools","https://www.futureagitools.com/submit-a-site"),
    ("GoodAI Tools","https://goodaitools.com/submit"),
    ("GPTE","https://gpte.ai/submit-a-tool"),
    ("Insidr AI","https://www.insidr.ai/submit-tools/"),
    ("Instant AI","https://instantai.io/submit-listing/"),
    ("Launched Site","https://launched.site/submit"),
    ("MadGenius","https://madgenius.co/submit"),
    ("OneHub AI","https://www.onehubai.com/"),
    ("OpenFuture AI","https://openfuture.ai/submit-tool"),
    ("Orbic AI","https://orbic.ai/submit/tools"),
    ("SAAS AI Tools","https://saasaitools.com/submit/"),
    ("Smart Tools AI","https://www.smart-tools.ai/en/submit"),
    ("Synoptica","https://synoptica.com/submit-an-ai-tool"),
    ("TheAIGeneration","https://www.theaigeneration.com/add/"),
    ("TipSeason","https://tipseason.com/ai-tools/submit"),
    ("ToolAI","https://toolai.io/en/submit"),
    ("ToolScout","https://toolscout.ai/submit"),
    ("TopApps","https://topapps.ai/submit"),
    ("WhatTheAI","https://whattheai.tech/submit-a-tool/"),
    ("Woy AI","https://woy.ai/submit"),
    ("EasySave AI","https://easysaveai.com/submit-your-ai-tool/"),
    ("NextGen Tools","https://nextgentools.me/submit-your-tool"),
    ("NextGen Tool","https://nextgentool.io/submit"),
    ("Toolio","https://toolio.ai/submit-a-tool"),
    ("Tools AI Online","https://www.tools-ai.online/tool-submit"),
    ("Tools Nocode","https://www.toolsnocode.com/ai"),
    ("Toolspedia","https://www.toolspedia.io/submit-tool/"),
    ("Victrays","https://victrays.com/submit-tool/"),
    ("ToolsAI.net","https://toolsai.net/add-listing/"),
    ("SAASBaba","https://saasbaba.com/add-ai-tool/"),
    ("GPT Academy","https://www.gptacademy.co/submit"),
    ("Look AI Tools","https://lookaitools.com/submission-service"),
    ("NextPedia","https://www.nextpedia.io/submit-tool"),
    ("Tool Directory AI","https://tooldirectory.ai/submit-tool"),
    ("Ismail Blogger","https://ismailblogger.com/submit-tools"),
    ("Educator Tools GF","https://docs.google.com/forms/d/e/1FAIpQLSdXXbiHAdQTWUSzLvU6xw-asbIoppIiQo0W9PuZLw2DnkhKew/viewform"),
    ("Tally 31kxN1","https://tally.so/r/31kxN1"),
    ("Tally w4Jb4b","https://tally.so/r/w4Jb4b"),
    ("Tally mYaR6N","https://tally.so/r/mYaR6N"),
    ("Tally wvY09d","https://tally.so/r/wvY09d"),
    ("Tally 3lOGLk","https://tally.so/r/3lOGLk"),
    ("Tally wMzP8X","https://tally.so/r/wMzP8X"),
    ("Tally 3qVzOG","https://tally.so/r/3qVzOG"),
    ("IgniterAI","https://haroonchoudery499974.typeform.com/to/FpdvtLml"),
]

async def try_fill(page, name, url):
    result = {"name": name, "url": url, "status": "unknown", "note": ""}
    try:
        await page.goto(url, timeout=25000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        text = await page.inner_text("body")
        text_lower = text.lower()[:2000]
        needs_login = any(kw in text_lower for kw in ["sign in","log in","login","register","create account"])
        inputs = await page.query_selector_all("input[type='text'],input[type='url'],input[type='email'],textarea")
        has_form = len(inputs) > 0
        if needs_login:
            result["status"] = "login_required"
            result["note"] = "Login/register form detected"
        elif has_form:
            filled = 0
            for inp in inputs[:8]:
                try:
                    t = await inp.get_attribute("type") or "text"
                    nm = (await inp.get_attribute("name") or "").lower()
                    iid = (await inp.get_attribute("id") or "").lower()
                    ph = (await inp.get_attribute("placeholder") or "").lower()
                    cl = (await inp.get_attribute("class") or "").lower()
                    combined = nm + iid + ph + cl
                    val = None
                    if any(k in combined for k in ["url","website","link","site"]): val = SITE_URL
                    elif any(k in combined for k in ["email","mail"]): val = EMAIL
                    elif any(k in combined for k in ["name","title","tool"]): val = SITE_NAME
                    elif any(k in combined for k in ["desc","detail","about"]): val = SITE_DESC[:200]
                    elif t == "url": val = SITE_URL
                    elif t == "email": val = EMAIL
                    if val:
                        await inp.fill(val)
                        filled += 1
                except: pass
            result["status"] = "form_filled" if filled > 0 else "form_found_but_empty"
            result["note"] = f"Filled {filled} fields"
            sanitized = re.sub(r'[\\\\/:*?\"<>|]', '_', name)[:30]
            await page.screenshot(path=f"{SCR_DIR}/{sanitized}.png", full_page=True)
        else:
            result["status"] = "no_form_detected"
            result["note"] = "No visible form fields"
    except Exception as e:
        result["status"] = "error"
        result["note"] = str(e)[:200]
    return result

async def main():
    results = []
    async with async_playwright() as p:
        print("Connecting to Edge CDP...")
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = browser.contexts[0] if browser.contexts else await browser.new_context()
        print(f"Connected. Trying {len(DIRS)} directories...")
        for idx, (name, url) in enumerate(DIRS, 1):
            print(f"[{idx}/{len(DIRS)}] {name}...", end="", flush=True)
            page = await ctx.new_page()
            r = await try_fill(page, name, url)
            await page.close()
            results.append(r)
            print(f" {r['status']}")
            await asyncio.sleep(1.5)
        await browser.close()
    
    with open(RESULT_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\nBATCH 2 - New Directories\n{'='*50}\n")
        ok = [r for r in results if r["status"] == "form_filled"]
        for r in results:
            f.write(f"{r['status']:25s} | {r['name']:25s} | {r['note'][:60]}\n")
        f.write(f"\nBatch Summary: {len(ok)} form_filled out of {len(results)}\n")
    print(f"\nDone! {len(ok)} successfully filled forms out of {len(results)}")

if __name__ == "__main__":
    asyncio.run(main())
