#!/usr/bin/env python3
"""Monetization Master: Add affiliate disclosures, deal banners, comparison tables, and urgency elements."""

import os, glob, re
from bs4 import BeautifulSoup, Tag

BASE = r"D:\项目\工作区\工作5"

# Tools that have affiliate/referral programs and their deal text
AFFILIATE_DEALS = {
    "Hostinger": ("https://www.hostinger.com?REFERRALCODE=ECA346010F8J", "60% OFF - Exclusive Hostinger Deal"),
    "ElevenLabs": ("https://try.elevenlabs.io/ebksqtv6a5m6", "Free Trial - ElevenLabs Voice AI"),
}

# Tools with special deal IDs in articles
DEAL_KEYWORDS = {
    "Hostinger": "Hostinger",
    "ElevenLabs": "ElevenLabs",
    "Canva": "Canva",
    "ChatGPT": "ChatGPT",
    "Claude": "Claude",
    "CapCut": "CapCut",
    "Descript": "Descript",
    "Notion": "Notion",
    "Semrush": "Semrush",
    "Grammarly": "Grammarly",
}

AFFILIATE_DISCLOSURE = """
<p class="affiliate-disclosure" style="font-size:0.8em;color:#888;margin-top:20px;border-top:1px solid #333;padding-top:10px">
  <em>Disclosure: Some links on this page are affiliate links. We may earn a commission at no extra cost to you.</em>
</p>"""

DEAL_BANNER_TEMPLATE = """
<div class="deal-banner" style="background:linear-gradient(135deg,#f59e0b,#d97706);color:#1e293b;padding:16px 20px;border-radius:12px;margin:24px 0;text-align:center;font-weight:700">
  🔥 {deal_text} &rarr; <a href="{url}" style="color:#7c3aed;background:#fff;padding:8px 20px;border-radius:6px;text-decoration:none;display:inline-block;margin-top:8px" target="_blank" rel="nofollow">Claim Deal</a>
</div>"""

COMPARISON_TABLE = """
<h2 style="margin-top:40px">Compare Top AI Tools</h2>
<div style="overflow-x:auto">
<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:0.9em">
<thead>
<tr style="background:#1e293b;color:#fff">
<th style="padding:12px;text-align:left;border:1px solid #333">Tool</th>
<th style="padding:12px;text-align:center;border:1px solid #333">Best For</th>
<th style="padding:12px;text-align:center;border:1px solid #333">Free Tier</th>
<th style="padding:12px;text-align:center;border:1px solid #333">Starting Price</th>
<th style="padding:12px;text-align:center;border:1px solid #333">Rating</th>
<th style="padding:12px;text-align:center;border:1px solid #333">Deal</th>
</tr>
</thead>
<tbody>
<tr style="background:#0f172a">
<td style="padding:10px;border:1px solid #333"><a href="https://chat.openai.com" target="_blank" rel="nofollow">ChatGPT</a></td>
<td style="padding:10px;text-align:center;border:1px solid #333">Writing & Code</td>
<td style="padding:10px;text-align:center;border:1px solid #333;color:#22c55e">Yes</td>
<td style="padding:10px;text-align:center;border:1px solid #333">$20/month</td>
<td style="padding:10px;text-align:center;border:1px solid #333">⭐⭐⭐⭐⭐</td>
<td style="padding:10px;text-align:center;border:1px solid #333"><a href="https://chat.openai.com" style="color:#f59e0b" target="_blank" rel="nofollow">Try Free</a></td>
</tr>
<tr style="background:#1e293a">
<td style="padding:10px;border:1px solid #333"><a href="https://claude.ai" target="_blank" rel="nofollow">Claude</a></td>
<td style="padding:10px;text-align:center;border:1px solid #333">Analysis & Long-form</td>
<td style="padding:10px;text-align:center;border:1px solid #333;color:#22c55e">Yes</td>
<td style="padding:10px;text-align:center;border:1px solid #333">$20/month</td>
<td style="padding:10px;text-align:center;border:1px solid #333">⭐⭐⭐⭐⭐</td>
<td style="padding:10px;text-align:center;border:1px solid #333"><a href="https://claude.ai" style="color:#f59e0b" target="_blank" rel="nofollow">Try Free</a></td>
</tr>
<tr style="background:#0f172a">
<td style="padding:10px;border:1px solid #333"><a href="https://www.canva.com" target="_blank" rel="nofollow">Canva AI</a></td>
<td style="padding:10px;text-align:center;border:1px solid #333">Design & Visual</td>
<td style="padding:10px;text-align:center;border:1px solid #333;color:#22c55e">Yes</td>
<td style="padding:10px;text-align:center;border:1px solid #333">Free / $13/month</td>
<td style="padding:10px;text-align:center;border:1px solid #333">⭐⭐⭐⭐⭐</td>
<td style="padding:10px;text-align:center;border:1px solid #333"><a href="https://www.canva.com" style="color:#f59e0b" target="_blank" rel="nofollow">Try Free</a></td>
</tr>
<tr style="background:#1e293a">
<td style="padding:10px;border:1px solid #333"><a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow">Hostinger</a></td>
<td style="padding:10px;text-align:center;border:1px solid #333">Web Hosting</td>
<td style="padding:10px;text-align:center;border:1px solid #333;color:#ef4444">No</td>
<td style="padding:10px;text-align:center;border:1px solid #333">$2.99/month</td>
<td style="padding:10px;text-align:center;border:1px solid #333">⭐⭐⭐⭐</td>
<td style="padding:10px;text-align:center;border:1px solid #333"><a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" style="color:#22c55e;font-weight:700" target="_blank" rel="nofollow">60% OFF</a></td>
</tr>
<tr style="background:#0f172a">
<td style="padding:10px;border:1px solid #333"><a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow">ElevenLabs</a></td>
<td style="padding:10px;text-align:center;border:1px solid #333">Text-to-Speech</td>
<td style="padding:10px;text-align:center;border:1px solid #333;color:#22c55e">Yes</td>
<td style="padding:10px;text-align:center;border:1px solid #333">Free / $5/month</td>
<td style="padding:10px;text-align:center;border:1px solid #333">⭐⭐⭐⭐⭐</td>
<td style="padding:10px;text-align:center;border:1px solid #333"><a href="https://try.elevenlabs.io/ebksqtv6a5m6" style="color:#f59e0b" target="_blank" rel="nofollow">Free Trial</a></td>
</tr>
</tbody>
</table>
</div>
<p style="font-size:0.8em;color:#888">Prices may change. Check each tool website for current pricing.</p>
"""

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    
    soup = BeautifulSoup(html, "html.parser")
    modified = False
    
    # 1. Add affiliate disclosure before </body>
    if soup.body and 'affiliate-disclosure' not in html:
        disclosure_soup = BeautifulSoup(AFFILIATE_DISCLOSURE, "html.parser")
        soup.body.append(disclosure_soup)
        modified = True
    
    # 2. Add deal banners for tools mentioned in the article
    text_lower = html.lower()
    for tool_name, (url, deal_text) in AFFILIATE_DEALS.items():
        keyword = tool_name.lower()
        if keyword in text_lower and f"deal-banner-{tool_name.lower()}" not in html:
            # Find a good insertion point - before the footer or end of article
            footer = soup.find("footer")
            article_end = soup.find("article")
            insert_point = footer or article_end or soup.body
            if insert_point and insert_point != soup.body:
                banner_html = DEAL_BANNER_TEMPLATE.format(deal_text=deal_text, url=url)
                banner_soup = BeautifulSoup(banner_html, "html.parser")
                # Mark as inserted
                for div in banner_soup.find_all("div"):
                    div["class"] = div.get("class", []) + [f"deal-banner-{tool_name.lower()}"]
                insert_point.insert_before(banner_soup)
                modified = True
                print(f"  Added deal banner for {tool_name} in {os.path.basename(filepath)}")
    
    # 3. Add comparison table on longer articles (>8KB)
    if len(html) > 8000 and "compare-top-ai-tools" not in html:
        footer = soup.find("footer")
        article_end = soup.find("article")
        insert_point = footer or article_end or (soup.body and list(soup.body.children)[-1] if soup.body else None)
        if insert_point:
            table_html = COMPARISON_TABLE.replace('compare-top-ai-tools', '')
            # Mark it
            table_html = table_html.replace('<h2', '<h2 class="compare-top-ai-tools"')
            table_soup = BeautifulSoup(table_html, "html.parser")
            insert_point.insert_before(table_soup)
            modified = True
            print(f"  Added comparison table in {os.path.basename(filepath)}")
    
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(soup))
        return True
    return False

# Process all HTML files
all_files = []
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "__pycache__")]
    for f in files:
        if f.endswith(".html"):
            all_files.append(os.path.join(root, f))

print(f"Processing {len(all_files)} HTML files for monetization...")
count = 0
for fp in all_files:
    try:
        if process_file(fp):
            count += 1
    except Exception as e:
        print(f"  Error in {os.path.basename(fp)}: {e}")

print(f"\nTotal files modified: {count}")
print("Done!")
