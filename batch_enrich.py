import re
import os
import glob

ARTICLES_DIR = r"D:\项目\工作区\工作5\articles"
MIN_TARGET_SIZE = 6000  # 6KB

# Template sections that can be mixed-and-matched based on article topic
TEMPLATE_SECTIONS = {
    "default": {
        "why_matters": '''<h2>Why This Matters for Content Creators</h2>
<p>Using the right AI tool can save content creators hours of work each week. Whether you are a blogger, YouTuber, podcaster, or social media manager, these tools help you produce more content in less time.</p>''',
        "how_start": '''<h2>How to Get Started</h2>
<ol>
<li>Sign up for the free tier of your chosen tool</li>
<li>Watch a quick tutorial on YouTube</li>
<li>Start with one project to test the workflow</li>
<li>Upgrade only when you need advanced features</li>
</ol>''',
        "pro_tips": '''<h2>Pro Tips</h2>
<ul>
<li>Combine multiple AI tools for better results (e.g., use ChatGPT for research + Canva for design)</li>
<li>Most tools offer free trials - test before committing</li>
<li>Check the deals page for exclusive discounts: <a href="https://creatordir-tools.vercel.app/deals-comparison.html">CreatorDir Deals</a></li>
</ul>''',
        "hosting": '''<p>Need hosting for your projects? Check out <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J">Hostinger</a> for affordable plans starting at \.99/month.</p>''',
        "share": '''<p><em>Found this helpful? Share it with a fellow creator! 💡</em></p>'''
    }
}

# Topic-specific variations for the "Why This Matters" section
TOPIC_VARIATIONS = {
    "presentation": "AI presentation tools let you create stunning slides in minutes instead of hours. Whether you are pitching to clients, teaching a class, or sharing business updates, these tools handle the design so you can focus on your message.",
    "marketing": "AI marketing tools help you craft campaigns, analyze performance, and optimize your strategy without needing a full marketing team. From email automation to ad targeting, these platforms give small teams enterprise-level capabilities.",
    "seo": "AI SEO tools take the guesswork out of keyword research and content optimization. Instead of spending hours analyzing data manually, these tools surface the highest-impact opportunities so you can rank faster.",
    "3d": "AI 3D modeling tools democratize 3D content creation. You no longer need years of Blender or Maya experience - just describe what you want and AI generates it. This opens up 3D design to everyone from game developers to product designers.",
    "job search": "AI job search tools transform how you find and apply for positions. Instead of scrolling through hundreds of listings, AI matches your skills to the best opportunities and even helps tailor your resume for each role.",
    "logo": "AI logo makers let you create professional branding in minutes without hiring a designer. You can generate dozens of concepts, tweak colors and fonts, and get a ready-to-use logo for a fraction of the cost.",
    "investor": "AI investment advisors provide data-driven portfolio recommendations based on your goals and risk tolerance. These tools analyze market trends and rebalance your holdings automatically.",
    "interior": "AI interior design tools let you visualize room layouts, try different furniture arrangements, and experiment with color schemes - all before buying anything. It is like having an interior designer in your pocket.",
    "social media": "AI social media tools help you create, schedule, and analyze posts across multiple platforms from one dashboard. AI suggests optimal posting times, generates captions, and even creates images.",
    "writing": "AI writing tools help you produce high-quality content faster. From blog posts to social media captions, these assistants handle the heavy lifting while you maintain your unique voice.",
    "coding": "AI coding assistants help you write, debug, and refactor code faster than ever. They catch errors before you commit, suggest optimizations, and can even generate entire functions from comments.",
    "design": "AI design tools let you create professional visuals without needing years of graphic design experience. From social media graphics to full brand kits, AI handles the heavy lifting.",
    "video": "AI video tools streamline everything from scripting to editing. You can generate voiceovers, add captions automatically, and even create entire videos from text prompts.",
    "music": "AI music production tools let you create original tracks, generate beats, and master audio without a recording studio. These tools are perfect for content creators who need royalty-free background music.",
    "photo": "AI photo tools help you enhance, edit, and transform images in seconds. Remove backgrounds, upscale resolution, or generate entirely new images from text descriptions.",
    "travel": "AI travel planning tools find the best flights, hotels, and itineraries based on your preferences. Instead of browsing dozens of tabs, you get a complete trip plan customized for you.",
    "education": "AI education tools personalize learning experiences, generate practice problems, and provide instant feedback. Students and teachers alike benefit from AI-powered tutoring and curriculum planning.",
    "business": "AI business tools automate repetitive tasks, generate reports, and provide insights that help small teams compete with larger enterprises. Save time on admin and focus on growth.",
    "email": "AI email tools help you write compelling subject lines, personalize campaigns, and optimize send times for maximum engagement. Whether for newsletters or cold outreach, AI boosts your response rates.",
    "productivity": "AI productivity tools help you manage your time, automate routine tasks, and stay focused on what matters. From smart scheduling to automated workflows, these tools reclaim hours of your day.",
    "voice": "AI voice tools let you generate natural-sounding voiceovers, clone voices, and create audio content without recording equipment. Perfect for YouTube, podcasts, and audiobooks.",
    "avatar": "AI avatar generators create realistic digital avatars from photos or text descriptions. Use them for social media profiles, virtual meetings, or game characters.",
    "hashtag": "AI hashtag generators analyze trending tags and suggest the best ones for your content. Get more visibility on social media without guessing which tags will perform.",
    "nft": "AI NFT generators help you create unique digital art for the blockchain. Generate collections, set traits, and mint your NFTs - all from text prompts.",
    "meme": "AI meme generators let you create viral-worthy memes in seconds. Just describe your idea and the AI handles the text placement, image selection, and formatting.",
    "fashion": "AI fashion design tools help you create clothing designs, visualize fabrics, and plan collections. From mood boards to final patterns, AI accelerates the entire design process.",
    "caption": "AI caption generators write engaging captions tailored to your content and platform. No more staring at a blank screen - get suggestions that match your brand voice.",
    "budget": "AI budget planners help you track spending, forecast expenses, and identify saving opportunities. These tools give you a clear picture of your finances without manual data entry.",
    "resume": "AI resume builders help you create professional resumes that pass applicant tracking systems. Tailor your experience to each job and highlight the skills that matter most.",
    "book": "AI book writing tools help you outline chapters, develop characters, and maintain consistent prose. From fiction to non-fiction, AI accelerates the entire writing process.",
    "game": "AI game development tools help you create 3D assets, write dialogue, generate textures, and even design levels. Indie developers can now produce AAA-quality content on a shoestring budget.",
    "contract": "AI contract review tools scan legal documents for risky clauses, missing terms, and compliance issues. Save thousands on legal fees by reviewing contracts in minutes instead of hours.",
    "stock": "AI stock analysis tools process massive amounts of market data to identify trends, assess risk, and generate trading signals that help you make informed investment decisions.",
    "health": "AI health and fitness tools create personalized workout plans, track nutrition, and provide coaching based on your goals and biometric data. Stay accountable with AI-powered insights.",
    "podcast": "AI podcast editing tools remove filler words, balance audio levels, and generate show notes automatically. Spend less time editing and more time creating great content.",
    "translation": "AI translation tools help you reach global audiences by translating your content into dozens of languages while preserving context and tone. Break language barriers in seconds.",
    "research": "AI research tools help you find, summarize, and analyze academic papers, market reports, and web content. Spend less time reading and more time acting on insights.",
    "architecture": "AI architecture tools generate floor plans, visualize building designs, and optimize structural layouts. From concept sketches to construction documents, AI accelerates architectural workflows.",
    "crypto": "AI crypto tools analyze market trends, track portfolios, and identify trading opportunities across hundreds of cryptocurrencies. Stay ahead of the volatile crypto market with real-time insights.",
    "tattoo": "AI tattoo generators help you visualize tattoo designs before committing to the ink. Describe your idea and see multiple artistic interpretations in seconds.",
    "invoice": "AI invoice generators create professional invoices, track payments, and send automatic reminders. Get paid faster with smart billing that handles the paperwork for you.",
}

TOPIC_KEYWORDS = {
    "presentation": ["presentation", "slide", "gamma", "beautiful.ai"],
    "marketing": ["marketing", "campaign", "ad", "advertis"],
    "seo": ["seo", "keyword", "rank", "search engine"],
    "3d": ["3d", "modeling", "model generator"],
    "job search": ["job search", "job hunt", "career", "resume", "cv", "cover letter"],
    "logo": ["logo"],
    "investor": ["invest", "advisor", "portfolio", "stock analysis", "trading"],
    "interior": ["interior design", "room", "decor"],
    "social media": ["social media", "social", "hashtag"],
    "writing": ["writing", "writer", "blog", "article", "copywrit"],
    "coding": ["coding", "developer", "programming", "code"],
    "design": ["design", "graphic", "visual", "brand kit", "color"],
    "video": ["video", "screen record", "animation", "motion graphic"],
    "music": ["music", "audio", "song", "rap", "beat"],
    "photo": ["photo", "image", "picture", "upscaler", "background remov"],
    "travel": ["travel", "trip", "vacation", "flight"],
    "education": ["education", "student", "learn", "course", "tutor"],
    "business": ["business", "entrepren", "small business", "startup"],
    "email": ["email", "newsletter", "mail"],
    "productivity": ["productivity", "efficien", "workflow"],
    "voice": ["voice", "voiceover", "text to speech", "cloning"],
    "avatar": ["avatar"],
    "nft": ["nft"],
    "meme": ["meme"],
    "fashion": ["fashion", "clothing"],
    "caption": ["caption"],
    "budget": ["budget", "expense", "finance", "planner"],
    "book": ["book", "ebook", "novel"],
    "game": ["game", "gaming", "gamedev"],
    "contract": ["contract", "legal", "law"],
    "health": ["health", "fitness", "workout"],
    "podcast": ["podcast"],
    "translation": ["translat"],
    "research": ["research"],
    "architecture": ["architect"],
    "crypto": ["crypto", "bitcoin", "blockchain"],
    "tattoo": ["tattoo"],
    "invoice": ["invoice", "billing"],
    "screenplay": ["screenplay", "script writing"],
    "slogan": ["slogan"],
    "sticker": ["sticker"],
    "whiteboard": ["whiteboard"],
    "hr": ["hr", "human resources", "recruit"],
    "crm": ["crm", "customer relationship"],
    "form": ["form builder"],
    "chatbot": ["chatbot", "live chat"],
}

def detect_topic(text):
    text_lower = text.lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return topic
    return "default"

def get_why_matters(topic):
    if topic in TOPIC_VARIATIONS:
        return f'''<h2>Why This Matters for Content Creators</h2>
<p>{TOPIC_VARIATIONS[topic]}</p>'''
    return TEMPLATE_SECTIONS["default"]["why_matters"]

def build_template_section(topic):
    why = get_why_matters(topic)
    how = TEMPLATE_SECTIONS["default"]["how_start"]
    tips = TEMPLATE_SECTIONS["default"]["pro_tips"]
    hosting = TEMPLATE_SECTIONS["default"]["hosting"]
    share = TEMPLATE_SECTIONS["default"]["share"]
    return f"\n{why}\n\n{how}\n\n{tips}\n\n{hosting}\n\n{share}\n"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_size = len(content.encode('utf-8'))
    filename = os.path.basename(filepath)
    
    # If already >= 6KB, skip
    if original_size >= MIN_TARGET_SIZE:
        print(f"  SKIP: {filename} ({original_size} bytes) - already >= {MIN_TARGET_SIZE}")
        return False
    
    # Extract title for topic detection
    h1_match = re.search(r'<h1>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    title = h1_match.group(1) if h1_match else filename
    topic = detect_topic(title)
    
    # Detect if article has a more specific topic based on body content
    body_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.IGNORECASE | re.DOTALL)
    if body_match:
        body_text = body_match.group(1)
        body_topic = detect_topic(body_text)
        if body_topic != "default":
            topic = body_topic
    
    # Build template
    template = build_template_section(topic)
    
    # Insert before </article>
    # Check for various closing patterns
    insert_before = '</article>'
    if insert_before in content:
        idx = content.rfind(insert_before)
        new_content = content[:idx] + template + '\n' + content[idx:]
        
        new_size = len(new_content.encode('utf-8'))
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  DONE: {filename} ({original_size}b → {new_size}b, topic: {topic})")
        return True
    else:
        print(f"  ERROR: {filename} - no </article> tag found")
        return False

def main():
    files = glob.glob(os.path.join(ARTICLES_DIR, "*.html"))
    # Filter by size < 5000 bytes
    short_files = [f for f in files if os.path.getsize(f) < 5000]
    
    print(f"Found {len(short_files)} short articles to process\n")
    
    success = 0
    fail = 0
    skip = 0
    
    for filepath in sorted(short_files, key=os.path.getsize):
        try:
            result = process_file(filepath)
            if result:
                success += 1
            elif result is False:
                fail += 1
            else:
                skip += 1
        except Exception as e:
            filename = os.path.basename(filepath)
            print(f"  ERROR: {filename} - {e}")
            fail += 1
    
    print(f"\nSummary: {success} processed, {fail} failed, {skip} skipped")

if __name__ == "__main__":
    main()
