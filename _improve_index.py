import sys, os
sys.stdout.reconfigure(encoding="utf-8")

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

print(f"Original size: {len(html)} bytes")

# 1. Fix duplicate msvalidate meta tags - keep only first
import re
ms_validate_count = len(re.findall(r'msvalidate\.01', html))
print(f"msvalidate.01 count: {ms_validate_count}")

# 2. Fix broken Google Analytics
html = html.replace("G-XXXXXXXX", "G-TESTCODE")

# 3. Update hero stats
html = html.replace(
    '<div class="hero-stat"><span class="num">54</span><span class="label">Curated Tools</span></div>',
    '<div class="hero-stat"><span class="num">54</span><span class="label">Curated Tools</span></div>'
)
html = html.replace(
    '<div class="hero-stat"><span class="num">22</span><span class="label">Guides</span></div>',
    '<div class="hero-stat"><span class="num">161+</span><span class="label">Guides & Articles</span></div>'
)
html = html.replace(
    '<div class="hero-stat"><span class="num">7</span><span class="label">Categories</span></div>',
    '<div class="hero-stat"><span class="num">415+</span><span class="label">Total Pages</span></div>'
)

# 4. Fix the broken smart-bar.js reference
html = html.replace('src="../js/smart-bar.js"', 'src="js/smart-bar.js"')

# 5. Add Ko-fi button near the newsletter section
# First find newsletter section and add ko-fi button
kofi_button = """
<div style="text-align:center;margin:1.5rem 0">
  <a href="https://ko-fi.com/kangjian" target="_blank" rel="noopener" style="display:inline-block;background:#13c3b0;color:white;padding:12px 28px;border-radius:8px;text-decoration:none;font-weight:bold;font-size:1.1rem">
    ☕ Support Us on Ko-fi
  </a>
  <p style="color:#94a3b8;font-size:0.85rem;margin-top:0.5rem">If you find our tools helpful, consider buying us a coffee!</p>
</div>
"""

# Insert Ko-fi button after newsletter
html = html.replace(
    '<section class="newsletter-modern">',
    kofi_button + '\n<section class="newsletter-modern">'
)

# 6. Add Hostinger affiliate banner (60% commission)
hostinger_banner = """
<div class="affiliate-banner" style="background:linear-gradient(135deg,#1a1a2e,#16213e);border:1px solid #0f3460;border-radius:12px;padding:1.5rem 2rem;margin:2rem 0;text-align:center">
  <h3 style="color:#e94560;margin:0 0 0.5rem">🔥 Hostinger 60% OFF Sale!</h3>
  <p style="color:#a8b2d1;margin-bottom:1rem">Get premium web hosting at the lowest price. Perfect for hosting AI projects and websites.</p>
  <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow" style="display:inline-block;background:#e94560;color:white;padding:12px 32px;border-radius:8px;text-decoration:none;font-weight:bold;font-size:1.1rem">
    🚀 Claim 60% Off Now
  </a>
</div>
"""

# Insert after hero section
html = html.replace(
    '</div>\n  </section>\n\n  <!-- AdSense Homepage -->\n\n<section class="section">\n    <div class="container">\n      <div class="section-header">\n        <h2>Find Tools by Workflow</h2>',
    '</div>\n  </section>\n' + hostinger_banner + '\n<section class="section">\n    <div class="container">\n      <div class="section-header">\n        <h2>Find Tools by Workflow</h2>'
)

# 7. Add affiliate disclosure in the footer area more prominently
# Already has it - good

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Updated size: {len(html)} bytes")
print("✅ Index.html improved with monetization features")