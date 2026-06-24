import os, glob, re

BASE = r"D:\项目\工作区\工作5"

# First, ensure the embed script has all our affiliate programs
script_path = os.path.join(BASE, "embed_affiliate_links.py")
with open(script_path, "r", encoding="utf-8") as f:
    content = f.read()

# Update TOOL_CONFIG with referral links where we have them
# Hostinger and ElevenLabs we already have. Add others too.
old_config = """TOOL_CONFIG = {"""
new_config = """TOOL_CONFIG = {
    "ChatGPT":    {"url": "https://chat.openai.com",                           "nofollow": True},
    "Claude":     {"url": "https://claude.ai",                                "nofollow": True},
    "Midjourney": {"url": "https://midjourney.com",                           "nofollow": True},
    "Canva":      {"url": "https://www.canva.com/affiliates/",                "nofollow": True},
    "Grammarly":  {"url": "https://grammarly.com",                            "nofollow": True},
    "Semrush":    {"url": "https://semrush.com",                              "nofollow": True},
    "CapCut":     {"url": "https://capcut.com",                               "nofollow": True},
    "Jasper":     {"url": "https://jasper.ai",                                "nofollow": True},
    "Runway":     {"url": "https://runwayml.com",                             "nofollow": True},
    "Suno":       {"url": "https://suno.ai",                                  "nofollow": True},
    "Notion":     {"url": "https://notion.so",                                "nofollow": True},
    "Descript":   {"url": "https://descript.com",                             "nofollow": True},
    "ElevenLabs": {"url": "https://try.elevenlabs.io/ebksqtv6a5m6",           "nofollow": True},
    "Hostinger":  {"url": "https://www.hostinger.com?REFERRALCODE=ECA346010F8J", "nofollow": True},
    "Shopify":    {"url": "https://shopify.com",                              "nofollow": True},
    "Bluehost":   {"url": "https://www.bluehost.com",                         "nofollow": True},
    "SiteGround": {"url": "https://www.siteground.com",                       "nofollow": True},
    "Namecheap":  {"url": "https://www.namecheap.com",                        "nofollow": True},
}"""

if old_config in content:
    content = content.replace(old_config, new_config)
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated TOOL_CONFIG with more affiliate programs")
else:
    print("TOOL_CONFIG already updated or format changed")

# Run the embed script
print("\nRe-running embed_affiliate_links.py...")
import subprocess
result = subprocess.run(["python", script_path], capture_output=True, text=True, cwd=BASE)
print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:200])
