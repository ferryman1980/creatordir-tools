import asyncio, sys, os
sys.stdout.reconfigure(encoding="utf-8")
os.chdir("D:\\项目\\工作区\\工作5")
from playwright.async_api import async_playwright

async def main():
    # First run embed affiliate links on new articles
    exec(open("embed_affiliate_links.py", encoding="utf-8-sig").read())
    print("Affiliate links embedded")
    
    # Run monetization
    exec(open("_monetization_master.py", encoding="utf-8-sig").read())
    print("Monetization done")
    
    await p.stop()

p = None
try:
    p = await async_playwright().start()
except:
    pass
print("Content ready for deploy")
