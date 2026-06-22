import asyncio, json, websockets, urllib.request, os
from datetime import datetime

SITE_NAME = "CreatorAI Tools"
SITE_URL_STR = "https://creatordir-tools.vercel.app"
SITE_DESC = "Curated directory of 160+ AI tools for content creators"
RESULTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "submission_results.json")

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

async def send_cmd(ws, cmd_id, method, params=None):
    msg = {"id": cmd_id, "method": method}
    if params:
        msg["params"] = params
    await ws.send(json.dumps(msg))
    async for msg in ws:
        data = json.loads(msg)
        if data.get("id") == cmd_id:
            return data.get("result", {})

async def get_page_ws():
    resp = urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=5)
    pages = json.loads(resp.read())
    # Find the GitHub page if available
    for p in pages:
        if "github.com" in p.get("url", ""):
            return p.get("webSocketDebuggerUrl", "")
    # Fall back to first non-service-worker page
    for p in pages:
        ws_url = p.get("webSocketDebuggerUrl", "")
        if ws_url and "service" not in p.get("url", "").lower():
            return ws_url
    return pages[0].get("webSocketDebuggerUrl", "") if pages else None

async def navigate(ws, url, timeout=15):
    result = await send_cmd(ws, 1, "Page.navigate", {"url": url})
    frame_id = result.get("frameId", "")
    # Wait for page load
    for _ in range(timeout):
        await asyncio.sleep(1)
        result = await send_cmd(ws, 2, "Runtime.evaluate", {"expression": "document.readyState"})
        state = result.get("result", {}).get("value", "")
        if state == "complete":
            break
    # Get current URL
    result = await send_cmd(ws, 3, "Runtime.evaluate", {"expression": "window.location.href"})
    current_url = result.get("result", {}).get("value", "")
    return current_url

async def fill_field(ws, cmd_start, selector, value):
    """Fill a form field by selector using JavaScript"""
    js = f"""
    (() => {{
        const el = document.querySelector('{selector}');
        if (!el) return false;
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value'
        ).set;
        nativeInputValueSetter.call(el, '{value.replace("'", "\\'")}');
        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        return true;
    }})()
    """
    js = js.replace("'", "'")
    result = await send_cmd(ws, cmd_start, "Runtime.evaluate", {"expression": js})
    return result.get("result", {}).get("value", False)

async def click_button(ws, cmd_start, selector):
    """Click a button by selector"""
    js = f"""
    (() => {{
        const btn = document.querySelector('{selector}');
        if (!btn) return false;
        btn.click();
        return true;
    }})()
    """
    result = await send_cmd(ws, cmd_start, "Runtime.evaluate", {"expression": js})
    return result.get("result", {}).get("value", False)

async def get_page_text(ws, cmd_start):
    result = await send_cmd(ws, cmd_start, "Runtime.evaluate", {"expression": "document.body.innerText.substring(0, 2000)"})
    return result.get("result", {}).get("value", "")

async def create_github_issue(ws):
    print("\n=== Step 1: Creating GitHub Issue ===")
    url = await navigate(ws, "https://github.com/ferryman1980/creatordir-tools/issues/new")
    print(f"  URL: {url}")
    
    if "issues/new" not in url and "issues/new/choose" not in url:
        print(f"  [WARN] Not on issue page: {url}")
        return {"status": "navigate_only", "url": url}
    
    if "issues/new/choose" in url:
        # Click "Open a blank issue"
        await send_cmd(ws, 10, "Runtime.evaluate", {
            "expression": "document.querySelector('a[href*=\"issues/new/\"], a:has-text(\"Open a blank issue\")')?.click()"
        })
        await asyncio.sleep(2)
    
    # Fill title
    title_js = """
    (() => {
        const el = document.querySelector('input[name="issue[title]"]');
        if (!el) return false;
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, 'Submit to 177+ AI Directories - Tracking');
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        return true;
    })()
    """
    result = await send_cmd(ws, 20, "Runtime.evaluate", {"expression": title_js})
    filled = result.get("result", {}).get("value", False)
    print(f"  Title filled: {filled}")
    
    # Fill body
    body_text = "## AI Directory Submission Plan\\n\\nWe are submitting **CreatorAI Tools** (https://creatordir-tools.vercel.app) to 177+ AI directories to increase visibility and traffic.\\n\\n### Target Directories (30+)\\n\\n1. AI Wizard\\n2. AI Tool Guru\\n3. Futurepedia\\n4. There\\'s An AI For That\\n5. EasyWithAI\\n6. TopAI.tools\\n7. AI Tools Club\\n8. SaaS AI Tools\\n9. AI Tools Directory\\n10. ToolPilot\\n11. AI Scout\\n12. Aixploria\\n13. That AI Collection\\n14. AI Collection\\n15. AI Top Tools\\n16. Tools4Noobs\\n17. AI Picks\\n18. AIContentfy\\n\\n### Status\\n\\n- [ ] Batch 1 (18 directories) - In Progress\\n- [ ] Batch 2 (more directories)\\n\\n### Details\\n\\n- **Site Name:** CreatorAI Tools\\n- **URL:** https://creatordir-tools.vercel.app\\n- **Description:** Curated directory of 160+ AI tools for content creators\\n- **Started:** 2026-06-23\\n"
    body_js = """
    (() => {
        const el = document.querySelector('textarea[name="issue[body]"]');
        if (!el) return false;
        const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        setter.call(el, arguments[0]);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        return true;
    })()
    """
    result = await send_cmd(ws, 30, "Runtime.evaluate", {
        "expression": f"({body_js})('{body_text.replace(chr(39), chr(39) + chr(92) + chr(39))}')"
    })
    filled = result.get("result", {}).get("value", False)
    print(f"  Body filled: {filled}")
    
    # Submit
    submit_js = """
    (() => {
        const btn = document.querySelector('button[type="submit"]');
        if (btn) { btn.click(); return true; }
        const btns = document.querySelectorAll('button');
        for (const b of btns) {
            if (b.textContent.includes('Submit new issue') || b.textContent.includes('Create')) {
                b.click(); return true;
            }
        }
        return false;
    })()
    """
    result = await send_cmd(ws, 40, "Runtime.evaluate", {"expression": submit_js})
    clicked = result.get("result", {}).get("value", False)
    print(f"  Submit clicked: {clicked}")
    await asyncio.sleep(3)
    
    # Get final URL
    result = await send_cmd(ws, 41, "Runtime.evaluate", {"expression": "window.location.href"})
    final_url = result.get("result", {}).get("value", "")
    print(f"  Final URL: {final_url}")
    
    return {"status": "done" if "issues" in final_url else "submitted", "url": final_url}

async def submit_directory(ws, dir_info):
    name = dir_info["name"]
    url = dir_info["url"]
    print(f"\n  [{name}]: {url}")
    
    result = {
        "status": "pending",
        "time": datetime.now().isoformat(),
        "fields_found": {"name": False, "url": False, "description": False},
        "submitted": False,
        "final_url": ""
    }
    
    try:
        current_url = await navigate(ws, url, timeout=20)
        result["final_url"] = current_url
        print(f"  Loaded: {current_url[:60]}")
        
        page_text = await get_page_text(ws, 50)
        has_form = "form" in page_text.lower() or "submit" in page_text.lower() or "input" in page_text.lower()
        result["has_form"] = has_form
        print(f"  Has form content: {has_form}")
        
        # Try to fill fields using JavaScript to find them by various attributes
        fill_commands = [
            # Name field
            (60, """
            (() => {
                const selectors = [
                    'input[name*="name" i]', 'input[placeholder*="name" i]', 'input[placeholder*="tool" i]',
                    'input[id*="name" i]', 'input[placeholder*="site" i]', 'input[name*="title" i]'
                ];
                for (const sel of selectors) {
                    const el = document.querySelector(sel);
                    if (el) {
                        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                        setter.call(el, arguments[0]);
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                        return sel;
                    }
                }
                return false;
            })()
            """, SITE_NAME, "name"),
            # URL field
            (70, """
            (() => {
                const selectors = [
                    'input[name*="url" i]', 'input[name*="website" i]', 'input[placeholder*="url" i]',
                    'input[placeholder*="website" i]', 'input[id*="url" i]', 'input[type="url"]',
                    'input[name*="link" i]', 'input[placeholder*="link" i]'
                ];
                for (const sel of selectors) {
                    const el = document.querySelector(sel);
                    if (el) {
                        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                        setter.call(el, arguments[0]);
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                        return sel;
                    }
                }
                return false;
            })()
            """, SITE_URL_STR, "url"),
            # Description field  
            (80, """
            (() => {
                const selectors = [
                    'textarea[name*="desc" i]', 'textarea[placeholder*="desc" i]', 'input[name*="desc" i]',
                    'textarea[id*="desc" i]', 'textarea[placeholder*="about" i]', 'textarea[placeholder*="short" i]',
                    'textarea[placeholder*="Describe" i]', 'textarea[name*="about" i]'
                ];
                for (const sel of selectors) {
                    const el = document.querySelector(sel);
                    if (el) {
                        const isTextarea = el.tagName === 'TEXTAREA';
                        const setter = Object.getOwnPropertyDescriptor(
                            window[isTextarea ? 'HTMLTextAreaElement' : 'HTMLInputElement'].prototype, 'value'
                        ).set;
                        setter.call(el, arguments[0]);
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                        return sel;
                    }
                }
                return false;
            })()
            """, SITE_DESC, "description"),
        ]
        
        for cmd_id, js_template, value, field_name in fill_commands:
            js = js_template.replace("arguments[0]", f"'{value.replace(chr(39), chr(92) + chr(39))}'")
            cmd_result = await send_cmd(ws, cmd_id, "Runtime.evaluate", {"expression": js})
            found = cmd_result.get("result", {}).get("value", False)
            if found:
                result["fields_found"][field_name] = True if found == True else (found if isinstance(found, bool) else True)
                print(f"  [OK] {field_name.capitalize()}: {found}")
        
        # Try clicking submit
        submit_js = """
        (() => {
            const selectors = [
                'button[type="submit"]', 'input[type="submit"]',
                'button:has-text("Submit")', 'button:has-text("submit")',
                'button:has-text("Add")', 'button:has-text("Send")',
                'button:has-text("Save")', 'button:has-text("Publish")',
                'button:has-text("List")'
            ];
            for (const sel of selectors) {
                try {
                    const el = document.querySelector(sel);
                    if (el && el.offsetParent !== null) {
                        el.click();
                        return sel;
                    }
                } catch(e) {}
            }
            // Try buttons containing submit text
            const buttons = document.querySelectorAll('button, a');
            for (const btn of buttons) {
                const text = btn.textContent.toLowerCase();
                if (text.includes('submit') || text.includes('add tool') || text.includes('list my')) {
                    btn.click();
                    return text.trim().substring(0, 30);
                }
            }
            return false;
        })()
        """
        cmd_result = await send_cmd(ws, 90, "Runtime.evaluate", {"expression": submit_js})
        clicked = cmd_result.get("result", {}).get("value", False)
        if clicked:
            result["submitted"] = True
            print(f"  [OK] Submit clicked: {str(clicked)[:30]}")
            await asyncio.sleep(3)
        
        # Check for success
        if result["submitted"]:
            page_text2 = await get_page_text(ws, 95)
            if "success" in page_text2.lower() or "thank" in page_text2.lower():
                result["status"] = "confirmed_submitted"
            else:
                result["status"] = "submitted"
        elif any(result["fields_found"].values()):
            result["status"] = "filled"
        else:
            result["status"] = "visited"
        
        print(f"  -> {result['status']}")
        
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        print(f"  [ERROR] {e}")
    
    return result

async def save_results():
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n  [SAVED] Results saved to {RESULTS_FILE}")

async def main():
    print("=" * 60)
    print("AI Directory Submission Bot")
    print("=" * 60)
    
    page_ws_url = await get_page_ws()
    if not page_ws_url:
        print("ERROR: No page WebSocket URL found!")
        return
    
    print(f"Connecting to page...")
    async with websockets.connect(page_ws_url) as ws:
        print("Connected!")
        
        # Step 1: Create GitHub Issue
        issue_result = await create_github_issue(ws)
        results.append({"step": "github_issue", "result": issue_result})
        await save_results()
        
        # Step 2: Submit to directories
        print("\n\n=== Step 2: Submitting to AI Directories ===")
        for i, dir_info in enumerate(DIRECTORIES, 1):
            print(f"\n[{i}/{len(DIRECTORIES)}]", end="")
            dir_result = await submit_directory(ws, dir_info)
            results.append({
                "step": f"submit_{i}",
                "dir": dir_info["name"],
                "url": dir_info["url"],
                "result": dir_result
            })
            await save_results()
        
        # Summary
        print("\n\n=== Summary ===")
        submitted = sum(1 for r in results if r.get("result", {}).get("status") in ("submitted", "confirmed_submitted"))
        filled = sum(1 for r in results if r.get("result", {}).get("status") == "filled")
        errors = sum(1 for r in results if r.get("result", {}).get("status") == "error")
        visited = sum(1 for r in results if r.get("result", {}).get("status") == "visited")
        print(f"  Submitted: {submitted}")
        print(f"  Filled (needs manual): {filled}")
        print(f"  Visited: {visited}")
        print(f"  Errors: {errors}")
        await save_results()

if __name__ == "__main__":
    asyncio.run(main())
