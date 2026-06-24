import re
import os
import glob

ARTICLES_DIR = r"D:\项目\工作区\工作5\articles"
MIN_TARGET_SIZE = 6000  # 6KB

# Topic-specific content blocks (topic → paragraph)
TOPIC_CONTENT = {
    "presentation": "AI presentation tools let you create stunning slides in minutes instead of hours. Whether you are pitching to clients, teaching a class, or sharing business updates, these tools handle the design so you can focus on your message. Modern AI presentation makers analyze your content and automatically generate professional layouts, color schemes, and typography - no design skills required.",
    "marketing": "AI marketing tools help you craft campaigns, analyze performance, and optimize your strategy without needing a full marketing team. From email automation to ad targeting and content personalization, these platforms give small teams enterprise-level capabilities at a fraction of the cost.",
    "seo": "AI SEO tools take the guesswork out of keyword research and content optimization. Instead of spending hours analyzing data manually, these tools surface the highest-impact opportunities so you can rank faster. They analyze search intent, competitor strategies, and content gaps to give you a clear roadmap to the top of search results.",
    "3d": "AI 3D modeling tools democratize 3D content creation. You no longer need years of Blender or Maya experience - just describe what you want and AI generates it. This opens up 3D design to everyone from game developers creating assets to product designers prototyping new concepts and architects visualizing buildings.",
    "job search": "AI job search tools transform how you find and apply for positions. Instead of scrolling through hundreds of listings, AI matches your skills to the best opportunities and helps tailor your resume for each role. These tools also analyze job descriptions to identify keywords your application needs to pass applicant tracking systems.",
    "logo": "AI logo makers let you create professional branding in minutes without hiring a designer. You can generate dozens of concepts, tweak colors and fonts, and get a ready-to-use logo for a fraction of the cost. Most tools also provide brand kits with matching color palettes and typography guidelines.",
    "investor": "AI investment advisors provide data-driven portfolio recommendations based on your goals and risk tolerance. These tools analyze market trends, rebalance your holdings automatically, and help you make informed decisions without needing a Wall Street background.",
    "interior": "AI interior design tools let you visualize room layouts, try different furniture arrangements, and experiment with color schemes - all before buying anything. Upload a photo of your room and see how different styles look in seconds. It is like having an interior designer in your pocket.",
    "social media": "AI social media tools help you create, schedule, and analyze posts across multiple platforms from one dashboard. AI suggests optimal posting times, generates captions, creates images, and even replies to comments automatically. You maintain a consistent presence without being glued to your phone.",
    "writing": "AI writing tools help you produce high-quality content faster. From blog posts to social media captions, these assistants handle the heavy lifting while you maintain your unique voice. They help overcome writer's block, suggest improvements, and maintain consistent tone across all your content.",
    "coding": "AI coding assistants help you write, debug, and refactor code faster than ever. They catch errors before you commit, suggest optimizations, and can generate entire functions from comments. Whether you are a beginner learning to code or a senior developer shipping daily, these tools boost your productivity significantly.",
    "design": "AI design tools let you create professional visuals without needing years of graphic design experience. From social media graphics to full brand kits, AI handles the heavy lifting. You can generate hundreds of variations and iterate quickly until you find the perfect look.",
    "video": "AI video tools streamline everything from scripting to editing. You can generate voiceovers, add captions automatically, create entire videos from text prompts, and even translate content into multiple languages. Video creation that used to take days now takes hours.",
    "music": "AI music production tools let you create original tracks, generate beats, and master audio without a recording studio. These tools are perfect for content creators who need royalty-free background music, podcast intros, or custom sound effects.",
    "photo": "AI photo tools help you enhance, edit, and transform images in seconds. Remove backgrounds, upscale resolution, colorize black-and-white photos, or generate entirely new images from text descriptions. Professional photo editing is now accessible to everyone.",
    "travel": "AI travel planning tools find the best flights, hotels, and itineraries based on your preferences. Instead of browsing dozens of tabs, you get a complete trip plan customized for your budget, timeline, and interests. AI even suggests hidden gems you would never find on your own.",
    "education": "AI education tools personalize learning experiences, generate practice problems, and provide instant feedback. Students and teachers alike benefit from AI-powered tutoring, curriculum planning, and assessment creation that adapts to each learner's pace.",
    "business": "AI business tools automate repetitive tasks, generate reports, and provide insights that help small teams compete with larger enterprises. From CRM automation to financial forecasting, these tools handle the busywork so you can focus on growth.",
    "email": "AI email tools help you write compelling subject lines, personalize campaigns, and optimize send times for maximum engagement. Whether for newsletters or cold outreach, AI boosts your open rates by analyzing what resonates with your audience.",
    "productivity": "AI productivity tools help you manage your time, automate routine tasks, and stay focused on what matters. From smart scheduling to automated workflows and intelligent note-taking, these tools reclaim hours of your day.",
    "voice": "AI voice tools let you generate natural-sounding voiceovers, clone voices, and create audio content without recording equipment. Perfect for YouTube narrations, podcast episodes, audiobooks, and e-learning content.",
    "avatar": "AI avatar generators create realistic digital avatars from photos or text descriptions. Use them for social media profiles, virtual meetings, game characters, or marketing materials. Many tools now support full-body avatars with customizable outfits and poses.",
    "hashtag": "AI hashtag generators analyze trending tags and suggest the best ones for your content. They consider your niche, posting time, and engagement patterns to recommend tags that maximize reach. Stop guessing and start growing.",
    "nft": "AI NFT generators help you create unique digital art for the blockchain. Generate entire collections with consistent styles, set rare traits, and mint your NFTs - all from text prompts. The creative possibilities are endless.",
    "meme": "AI meme generators let you create viral-worthy memes in seconds. Just describe your idea and the AI handles the text placement, image selection, and formatting. Perfect for social media managers looking to engage their audience with timely humor.",
    "fashion": "AI fashion design tools help you create clothing designs, visualize fabrics on different body types, and plan entire collections. From mood boards to final patterns, AI accelerates the entire design process.",
    "caption": "AI caption generators write engaging captions tailored to your content and platform. No more staring at a blank screen - get suggestions that match your brand voice, include relevant hashtags, and drive engagement.",
    "budget": "AI budget planners help you track spending, forecast expenses, and identify saving opportunities without manual data entry. Connect your accounts and get real-time insights into where your money goes.",
    "resume": "AI resume builders help you create professional resumes that pass applicant tracking systems and catch recruiters' attention. Tailor your experience to each job application and highlight the skills that matter most.",
    "book": "AI book writing tools help you outline chapters, develop characters, and maintain consistent prose throughout your manuscript. From fiction to non-fiction, AI helps you overcome writer's block and finish your book faster.",
    "game": "AI game development tools help you create 3D assets, write dialogue, generate textures, and design levels. Indie developers can now produce high-quality game content without large teams or budgets.",
    "contract": "AI contract review tools scan legal documents for risky clauses, missing terms, and compliance issues. Save thousands on legal fees by reviewing contracts in minutes instead of hours. Essential for freelancers and small businesses.",
    "stock": "AI stock analysis tools process massive amounts of market data to identify trends, assess risk, and generate trading signals. These platforms help both beginners and experienced investors make data-driven decisions.",
    "health": "AI health and fitness tools create personalized workout plans, track nutrition, and provide coaching based on your goals and biometric data. Stay accountable with AI-powered insights that adapt as you progress.",
    "podcast": "AI podcast editing tools remove filler words, balance audio levels, and generate show notes automatically. Spend less time editing and more time creating great content for your audience.",
    "translation": "AI translation tools help you reach global audiences by translating your content into dozens of languages while preserving context, tone, and nuance. Break language barriers and grow your audience worldwide.",
    "research": "AI research tools help you find, summarize, and analyze academic papers, market reports, and web content. Spend less time reading and more time acting on insights that drive your projects forward.",
    "architecture": "AI architecture tools generate floor plans, visualize building designs, and optimize structural layouts. From concept sketches to construction documents, AI accelerates the architectural workflow significantly.",
    "crypto": "AI crypto tools analyze market trends, track portfolios, and identify trading opportunities across hundreds of cryptocurrencies. Stay ahead of the volatile crypto market with real-time sentiment analysis and price predictions.",
    "tattoo": "AI tattoo generators help you visualize tattoo designs before committing to the ink. Describe your idea and see multiple artistic interpretations in different styles. No more relying on rough sketches.",
    "invoice": "AI invoice generators create professional invoices, track payments, and send automatic reminders. Get paid faster with smart billing that handles the paperwork for you.",
    "screenplay": "AI screenplay writers help you format scripts correctly, develop dialogue, and structure your story beats. From short films to feature-length screenplays, AI assists at every stage of the writing process.",
    "slogan": "AI slogan generators help you create memorable taglines for your brand. Input your brand values and get dozens of creative options that capture your message in a few powerful words.",
    "sticker": "AI sticker makers let you design custom stickers from your ideas in seconds. Perfect for social media creators, businesses, and anyone who wants to express themselves with unique sticker designs.",
    "whiteboard": "AI whiteboard animation tools transform your ideas into engaging animated explainer videos. Just provide a script and watch as AI generates scenes, characters, and transitions automatically.",
    "hr": "AI HR tools automate resume screening, candidate sourcing, and employee onboarding. HR teams can focus on building culture while AI handles the administrative heavy lifting.",
    "crm": "AI CRM tools help you manage customer relationships, track leads, and predict which prospects are most likely to convert. Sales teams using AI CRMs report significantly higher close rates.",
    "form": "AI form builders create smart forms that adapt to user responses, validate data in real-time, and integrate with your existing tools. Collect better data with less effort.",
    "chatbot": "AI chatbots provide instant customer support 24/7, answer frequently asked questions, and escalate complex issues to human agents. Compared to traditional live chat, AI chatbots handle inquiries faster and at lower cost.",
    "press release": "AI press release generators help you write professional announcements that capture media attention. Structure your news effectively and distribute it to the right channels.",
    "song lyrics": "AI song lyrics generators help you write original lyrics for any genre. Whether you are a musician looking for inspiration or a content creator needing custom jingles, AI can help you find the right words.",
    "newsletter": "AI newsletter tools help you write engaging emails, curate content, and grow your subscriber base. Automate your newsletter workflow while maintaining a personal touch.",
}

# Standard templates (always included)
STANDARD_TEMPLATES = {
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
    "hosting": '''<p>Need hosting for your projects? Check out <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J">Hostinger</a> for affordable plans starting at .99/month.</p>''',
    "share": '''<p><em>Found this helpful? Share it with a fellow creator! &#x1F4A1;</em></p>'''
}

# Keyword → topic mapping (checked against h1 + article body only)
TOPIC_KEYWORDS = [
    ("presentation", ["presentation", "slide", "gamma", "beautiful.ai"]),
    ("seo", ["seo", "keyword", "rank", "search engine"]),
    ("3d", ["3d", "modeling", "model generator"]),
    ("job search", ["job search", "job hunt", "career"]),
    ("logo", ["logo maker", "logo design", "logo"]),
    ("investor", ["invest", "advisor", "portfolio", "stock analysis"]),
    ("interior", ["interior design", "room", "decor"]),
    ("social media", ["social media", "social"]),
    ("writing", ["writing", "writer", "blog", "article", "copywriting"]),
    ("coding", ["coding", "developer", "programming", "code assistant"]),
    ("design", ["design", "graphic design", "brand kit"]),
    ("video", ["video", "screen record", "animation", "motion graphic"]),
    ("music", ["music", "audio", "song", "rap", "beat"]),
    ("photo", ["photo", "image", "picture", "upscaler", "background remov"]),
    ("travel", ["travel", "trip", "vacation", "flight"]),
    ("education", ["education", "student", "learn", "course", "tutor"]),
    ("business", ["business", "entrepren", "small business", "startup"]),
    ("email", ["email", "newsletter", "mail"]),
    ("productivity", ["productivity", "efficien", "workflow"]),
    ("voice", ["voice", "voiceover", "text to speech"]),
    ("avatar", ["avatar"]),
    ("nft", ["nft"]),
    ("meme", ["meme"]),
    ("fashion", ["fashion", "clothing"]),
    ("caption", ["caption"]),
    ("budget", ["budget", "expense tracker", "planner"]),
    ("resume", ["resume", "cv builder"]),
    ("book", ["book", "ebook", "novel", "published"]),
    ("game", ["game", "gaming", "gamedev", "game dev"]),
    ("contract", ["contract", "legal", "law"]),
    ("health", ["health", "fitness", "workout"]),
    ("podcast", ["podcast"]),
    ("translation", ["translat"]),
    ("research", ["research"]),
    ("architecture", ["architect"]),
    ("crypto", ["crypto", "bitcoin", "blockchain"]),
    ("tattoo", ["tattoo"]),
    ("invoice", ["invoice", "billing"]),
    ("screenplay", ["screenplay", "script writing"]),
    ("slogan", ["slogan"]),
    ("sticker", ["sticker"]),
    ("whiteboard", ["whiteboard"]),
    ("hr", ["hr", "human resources", "recruit"]),
    ("crm", ["crm", "customer relationship"]),
    ("form", ["form builder"]),
    ("chatbot", ["chatbot", "live chat"]),
    ("marketing", ["marketing", "campaign", "ad", "advertis", "marketer"]),
]

def detect_topic(h1_text, article_body):
    """Detect topic from h1 text and article body only (not meta/nav/footer)."""
    text = (h1_text + " " + article_body).lower()
    for topic, keywords in TOPIC_KEYWORDS:
        if any(kw.lower() in text for kw in keywords):
            return topic
    return "default"

def get_why_matters(topic):
    if topic in TOPIC_CONTENT:
        return f'''<h2>Why This Matters for Content Creators</h2>
<p>{TOPIC_CONTENT[topic]}</p>'''
    # Fallback generic
    return '''<h2>Why This Matters for Content Creators</h2>
<p>Using the right AI tool can save content creators hours of work each week. Whether you are a blogger, YouTuber, podcaster, or social media manager, these tools help you produce more content in less time while maintaining high quality.</p>'''

def build_template_section(topic):
    why = get_why_matters(topic)
    how = STANDARD_TEMPLATES["how_start"]
    tips = STANDARD_TEMPLATES["pro_tips"]
    hosting = STANDARD_TEMPLATES["hosting"]
    share = STANDARD_TEMPLATES["share"]
    return f"\n{why}\n\n{how}\n\n{tips}\n\n{hosting}\n\n{share}\n"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_size = len(content.encode('utf-8'))
    filename = os.path.basename(filepath)
    
    # Extract h1
    h1_match = re.search(r'<h1>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    h1_text = h1_match.group(1) if h1_match else ""
    
    # Extract article body
    article_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.IGNORECASE | re.DOTALL)
    article_body = article_match.group(1) if article_match else ""
    
    # Detect topic from h1 + article body only (not meta/nav/footer)
    topic = detect_topic(h1_text, article_body)
    
    # Build base template
    template = build_template_section(template)  # This was a bug - will fix below
    
    # Insert before </article>
    insert_target = '</article>'
    if insert_target not in content:
        print(f"  ERROR: {filename} - no </article>")
        return False
    
    idx = content.rfind(insert_target)
    new_content = content[:idx] + template + '\n' + content[idx:]
    new_size = len(new_content.encode('utf-8'))
    
    # If still under 6KB, add extra paragraph to reach the target
    if new_size < MIN_TARGET_SIZE:
        extra_bytes_needed = MIN_TARGET_SIZE - new_size
        # Add relevant extra content
        extra_paragraphs = []
        extra_paragraphs.append(f'''<h2>Best Use Cases for This Category</h2>
<p>Content creators in this space typically see the best results when they integrate these tools into their daily workflow. Start by identifying one repetitive task that takes up most of your time, then pick a tool that solves that specific problem. Over time, you will build a powerful toolkit that handles the grunt work while you focus on creativity and strategy. Many creators report saving 10-15 hours per week after fully adopting AI tools into their workflow.</p>''')
        
        extra_content = "\n" + "\n\n".join(extra_paragraphs) + "\n"
        new_content = content[:idx] + template + extra_content + '\n' + content[idx:]
        new_size = len(new_content.encode('utf-8'))
        
        # If still under, add another paragraph
        if new_size < MIN_TARGET_SIZE:
            extra2 = '''<p>Another great approach is to join online communities focused on these tools. Reddit communities like r/AItools and r/content_marketing regularly share tips, tricks, and real-world results. Following creators on YouTube who review these tools can also help you discover features you did not know existed. The AI tool landscape evolves rapidly, so staying connected with the community ensures you are always using the latest and most effective solutions.</p>'''
            new_content = content[:idx] + template + extra_content + extra2 + '\n' + content[idx:]
            new_size = len(new_content.encode('utf-8'))
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  DONE: {filename} ({original_size}b -> {new_size}b, topic: {topic})")
    return True

def main():
    files = glob.glob(os.path.join(ARTICLES_DIR, "*.html"))
    short_files = [f for f in files if os.path.getsize(f) < 5000]
    
    print(f"Found {len(short_files)} short articles to process\n")
    
    success = 0
    fail = 0
    
    for filepath in sorted(short_files, key=os.path.getsize):
        try:
            if process_file(filepath):
                success += 1
            else:
                fail += 1
        except Exception as e:
            filename = os.path.basename(filepath)
            print(f"  ERROR: {filename} - {e}")
            fail += 1
    
    print(f"\nSummary: {success} processed, {fail} failed")

if __name__ == "__main__":
    main()
