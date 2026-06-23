
import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=10000)
            page = browser.contexts[0].pages[0]
            
            # Try different PartnerStack URLs
            urls = [
                "https://partnerships.partnerstack.com/",
                "https://app.partnerstack.com/auth/signup",
                "https://impact.com/signup/",
                "https://partnerships.partnerstack.com/platform/affiliate/",
            ]
            
            for url in urls:
                print(f"\nTrying: {url}")
                try:
                    await page.goto(url, timeout=15000, wait_until="domcontentloaded")
                    await page.wait_for_timeout(3000)
                    print(f"  URL: {page.url[:70]}")
                    print(f"  Title: {(await page.title())[:50]}")
                    
                    # Check for signup/register links
                    signup_links = await page.evaluate("""
                        () => Array.from(document.querySelectorAll("a, button"))
                            .filter(el => el.offsetParent !== null)
                            .map(el => el.innerText || el.textContent || "")
                            .filter(t => {
                                const l = t.trim().toLowerCase();
                                return l.includes("sign") || l.includes("register") || l.includes("get started") || l.includes("create");
                            })
                    """)
                    if signup_links:
                        print(f"  Found: {signup_links[:3]}")
                    
                    # Count inputs
                    inputs = await page.evaluate("""
                        () => document.querySelectorAll("input:not([type=hidden])").length
                    """)
                    print(f"  Inputs: {inputs}")
                    
                except Exception as e:
                    print(f"  Error: {str(e)[:40]}")
            
            await browser.close()
        except Exception as e:
            print(f"  Connection error: {str(e)[:60]}")

asyncio.run(main())
