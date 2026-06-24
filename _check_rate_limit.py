import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    page = await edge.contexts[0].new_page()
    
    await page.goto("https://www.reddit.com", wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(2000)
    
    cookies = await page.context.cookies()
    token = None
    for c in cookies:
        if c.get("name") == "token_v2":
            token = c.get("value")
            break
    
    if not token:
        print("No token found")
        await page.close()
        await p.stop()
        return
    
    result = await page.evaluate("""
        async (token) => {
            const resp = await fetch("https://oauth.reddit.com/api/v1/me", {
                headers: { "Authorization": "Bearer " + token }
            });
            const me = await resp.json();
            
            const testResp = await fetch("https://oauth.reddit.com/api/submit", {
                method: "POST",
                headers: {
                    "Authorization": "Bearer " + token,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams({
                    api_type: "json",
                    kind: "self",
                    sr: "test",
                    title: "test post " + Date.now(),
                    text: "test",
                    sendreplies: "false"
                }).toString()
            });
            const testData = await testResp.json();
            return {
                username: me.name,
                errors: testData.json ? testData.json.errors : [],
                status: testResp.status
            };
        }
    """, token)
    
    rate_limited = any("RATELIMIT" in str(e) for e in result.get("errors", []))
    retry_after = ""
    for e in result.get("errors", []):
        if "RATELIMIT" in str(e):
            retry_after = str(e)
    
    print("Username: " + result.get("username", "unknown"))
    print("Status: " + ("RATE_LIMITED" if rate_limited else "OK"))
    print("Errors: " + str(result.get("errors", [])))
    
    await page.close()
    await p.stop()

asyncio.run(main())
