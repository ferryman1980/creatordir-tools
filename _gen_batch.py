import os, re

base = r"D:\项目\工作区\工作5"
adir = os.path.join(base, "articles")

with open(os.path.join(adir, "ai-article-writer-2026.html"), "r", encoding="utf-8") as f:
    s = f.read()

tb = s[:s.index('<article class="article-content">')]
ta = s[s.index("</article>") + 10:]

def make(fn, title, desc, body):
    url = "https://creatordir-tools.vercel.app/articles/" + fn
    og = title + " - CreatorAI Tools"
    h = tb
    h = re.sub(r"<title>.*?</title>", "<title>" + og + "</title>", h)
    h = re.sub(r'property="og:title" content="[^"]*"', 'property="og:title" content="' + og + '"', h)
    h = re.sub(r'property="og:description" content="[^"]*"', 'property="og:description" content="' + desc + '"', h)
    h = re.sub(r'property="og:url" content="[^"]*"', 'property="og:url" content="' + url + '"', h)
    h += '\n<article class="article-content">\n' + body + '\n</article>\n' + ta
    with open(os.path.join(adir, fn), "w", encoding="utf-8") as f:
        f.write(h)
    print("Created:", fn, "[" + str(len(body)) + " chars]")

articles = [
    ("midjourney-vs-dall-e-vs-stable-diffusion-2026.html",
     "Midjourney vs DALL-E vs Stable Diffusion: Best AI Image Gen 2026",
     "Compare three leading AI image generators. Midjourney vs DALL-E 3 vs Stable Diffusion side by side.",
     '<h1>Midjourney vs DALL-E vs Stable Diffusion 2026 Comparison</h1><p class="article-meta">Published: 2026-06-23</p><p>Three AI image generators dominate the market. Here is how they compare.</p><h2>Midjourney</h2><p>Best artistic quality. Produces stunning, stylized images. Pricing: -60/month. Best for creative professionals who want aesthetic results.</p><h2>DALL-E 3</h2><p>Best at following complex prompts. Included with ChatGPT Plus (/month). Best for commercial product images and precise concepts.</p><h2>Stable Diffusion</h2><p>Open-source and free. Maximum control with fine-tuning. Best for developers and those who want complete customization.</p><p>Try <a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a> for AI voiceovers to narrate your image creation tutorials.</p><p>Get <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a> to host your portfolio site.</p><p>Browse all <a href="../tools/">AI image tools</a>.</p>'),
    ("runway-vs-pika-vs-synthesia-2026.html",
     "Runway vs Pika vs Synthesia 2026: Best AI Video Tool",
     "Compare Runway Gen-3, Pika Labs, and Synthesia for AI video creation.",
     '<h1>Runway vs Pika vs Synthesia: Best AI Video Tool 2026</h1><p class="article-meta">Published: 2026-06-23</p><p>AI video creation tools compared side by side.</p><h2>Runway Gen-3</h2><p>Most versatile AI video platform. Text-to-video, video-to-video, inpainting. /month Standard plan. Best for creative video projects.</p><h2>Pika Labs</h2><p>Quick video generation with style transfer. Free tier available. Great for social media content.</p><h2>Synthesia</h2><p>AI avatars for professional presenter videos. /month. Best for corporate training and marketing videos.</p><p>Use <a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a> for professional voiceovers.</p><p>Host your site with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a>.</p><p>Browse <a href="../tools/">AI video tools</a>.</p>'),
    ("grammarly-vs-pro-writing-aid-vs-hemingway-2026.html",
     "Grammarly vs ProWritingAid vs Hemingway 2026 Comparison",
     "Compare Grammarly, ProWritingAid, and Hemingway App side by side.",
     '<h1>Grammarly vs ProWritingAid vs Hemingway App 2026</h1><p class="article-meta">Published: 2026-06-23</p><p>Three leading AI writing assistants compared.</p><h2>Grammarly</h2><p>Best all-around writing assistant. Grammar, tone, clarity, plagiarism. Free tier available. Premium /month. Best for everyday writing.</p><h2>ProWritingAid</h2><p>Best for deep editing. Style reports, overused words, sentence variety. /month. Best for authors and long-form writers.</p><h2>Hemingway App</h2><p>Best for readability. Highlights complex sentences, passive voice. One-time .99. Simple and effective.</p><p>Use <a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a> to turn your written content into audio.</p><p>Browse all <a href="../tools/">AI writing tools</a>.</p>'),
    ("best-ai-tools-youtube-2026.html",
     "25 Best AI Tools for YouTube Creators in 2026",
     "Grow your YouTube channel with 25 powerful AI tools for scriptwriting, thumbnails, editing, and SEO.",
     '<h1>25 Best AI Tools for YouTube Creators in 2026</h1><p class="article-meta">Published: 2026-06-23</p><p>YouTube creators save 20+ hours per week with these AI tools.</p><h2>Scriptwriting</h2><p>ChatGPT, Claude, and Jasper AI generate video scripts in seconds. Write engaging introductions, hooks, and calls to action.</p><h2>Thumbnail Design</h2><p>Canva AI and Midjourney create click-worthy thumbnails. AI generates multiple variations in minutes.</p><h2>Video Editing</h2><p>CapCut (completely free), Runway, and Descript offer AI-powered editing with auto-captions and scene detection.</p><h2>Voiceovers</h2><p><a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a> delivers studio-quality AI voiceovers in 29 languages. Perfect for narration.</p><h2>SEO and Growth</h2><p>TubeBuddy and VidIQ provide AI-powered keyword research and optimization for YouTube.</p><p>Get <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a> for your channel website.</p><p>Browse all <a href="../tools/">AI tools for creators</a>.</p>'),
    ("best-ai-tools-tiktok-2026.html",
     "20 Best AI Tools for TikTok Creators in 2026",
     "Create viral TikTok content faster with AI tools for editing, voiceovers, and trend analysis.",
     '<h1>20 Best AI Tools for TikTok Creators in 2026</h1><p class="article-meta">Published: 2026-06-23</p><p>TikTok creators use AI to produce content faster and stay ahead of trends.</p><h2>Trend Discovery</h2><p>TrendTok and Brandwatch provide AI-powered trend analysis for TikTok. Know what is trending before you create.</p><h2>Video Editing</h2><p>CapCut is ByteDance official free editor with AI captions, transitions, and effects. The best tool for TikTok editing.</p><h2>Voiceovers</h2><p><a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a> creates natural-sounding AI voices for TikTok narration and commentary.</p><h2>Caption Writing</h2><p>ChatGPT and Copy.ai generate engaging captions that drive comments and shares. AI optimizes for engagement.</p><p>Browse all <a href="../tools/">AI tools</a>.</p>'),
    ("best-ai-tools-instagram-2026.html",
     "20 Best AI Tools for Instagram Creators in 2026",
     "Grow your Instagram with AI tools for image editing, caption writing, and content planning.",
     '<h1>20 Best AI Tools for Instagram Creators in 2026</h1><p class="article-meta">Published: 2026-06-23</p><p>Instagram creators leverage AI for consistent, high-quality content.</p><h2>Image Editing</h2><p>Canva AI and Adobe Photoshop AI create stunning Instagram visuals. Remove backgrounds, generate designs, and enhance photos.</p><h2>Caption Writing</h2><p>ChatGPT and Jasper write engaging captions that drive comments and saves. AI optimizes for your audience.</p><h2>Hashtag Research</h2><p>Display Purposes and Later provide AI-powered hashtag recommendations for maximum reach.</p><h2>Content Planning</h2><p>Later, Buffer, and Planoly schedule posts with AI optimization for best posting times.</p><p>Get <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a> for your link-in-bio page.</p>'),
    ("how-to-make-money-ai-tools-2026.html",
     "How to Make Money with AI Tools in 2026: 15 Proven Ways",
     "15 proven ways to earn income using AI tools. From freelancing to digital products to affiliate marketing.",
     '<h1>How to Make Money with AI Tools in 2026: 15 Proven Ways</h1><p class="article-meta">Published: 2026-06-23</p><p>AI tools open multiple income streams. Here are 15 proven methods to start earning today.</p><h2>1. AI Content Writing</h2><p>Use ChatGPT and Jasper to write blog posts for clients. Charge -500 per article. Demand is high.</p><h2>2. AI Voiceover Services</h2><p>Offer voiceover services using <a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a>. Charge -200 per project. Voice actors earn +/month.</p><h2>3. AI Video Creation</h2><p>Create YouTube videos with AI tools. Monetize through ads, sponsorships, and affiliate marketing.</p><h2>4. Digital Products</h2><p>Sell AI-generated templates, prompts, and assets on Etsy or Gumroad. Passive income after initial creation.</p><h2>5. Affiliate Marketing</h2><p>Promote AI tools through affiliate programs. Our <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% commission</a> program is a great start.</p><p>Browse all <a href="../tools/">AI tools</a> and start earning.</p>'),
    ("ai-seo-guide-2026.html",
     "Complete AI SEO Guide 2026: Rank Higher with AI",
     "Master SEO with AI tools. Complete guide to keyword research, content optimization, and link building.",
     '<h1>Complete AI SEO Guide 2026: Rank Higher with Artificial Intelligence</h1><p class="article-meta">Published: 2026-06-23</p><p>AI tools transform search engine optimization. Here is how to use them.</p><h2>AI Keyword Research</h2><p>Semrush and Ahrefs AI features discover low-competition, high-volume keywords. Find gaps your competitors miss.</p><h2>AI Content Optimization</h2><p>Surfer SEO and Frase.io analyze top-ranking pages and optimize your content structure, headings, and keyword density.</p><h2>AI Technical SEO</h2><p>Screaming Frog with AI analysis identifies technical issues faster. Fix page speed, mobile optimization, and crawl errors.</p><h2>AI Link Building</h2><p>Use AI to identify outreach opportunities and personalize emails at scale. Save hours of manual research.</p><p>Host your SEO-optimized website with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a>.</p><p>Browse <a href="../tools/">AI marketing tools</a>.</p>'),
    ("best-ai-chatbots-2026.html",
     "10 Best AI Chatbots for Customer Service in 2026",
     "Compare the top 10 AI chatbots for customer service. Features, pricing, and integrations.",
     '<h1>10 Best AI Chatbots for Customer Service in 2026</h1><p class="article-meta">Published: 2026-06-23</p><p>AI chatbots reduce support costs and improve customer satisfaction.</p><h2>1. Intercom Fin</h2><p>AI-powered customer support with intelligent routing. Starts at /month. Best for SaaS companies.</p><h2>2. Zendesk AI</h2><p>Integrated with the full Zendesk suite. Intelligent ticket routing and response suggestions.</p><h2>3. Tidio</h2><p>Affordable AI chatbot for small businesses. Generous free tier available. Easy to set up.</p><h2>4. ManyChat</h2><p>Best for Messenger and Instagram automation. /month. Great for social commerce.</p><p>Host your business with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ("best-ai-tools-realtors-2026.html",
     "15 Best AI Tools for Real Estate Agents in 2026",
     "AI tools that help real estate agents generate leads, create listings, and close deals faster.",
     '<h1>15 Best AI Tools for Real Estate Agents in 2026</h1><p class="article-meta">Published: 2026-06-23</p><p>Real estate agents save 15+ hours per week with AI tools.</p><h2>Listing Descriptions</h2><p>ChatGPT and Jasper generate compelling property descriptions in seconds. Highlight key features automatically.</p><h2>Virtual Staging</h2><p>Interior AI and Midjourney virtually stage empty rooms. Show potential buyers how spaces can look.</p><h2>Lead Generation</h2><p>Zillow AI and Smart CRM provide AI-powered lead scoring and prioritization.</p><h2>Email Campaigns</h2><p>Mailchimp AI and HubSpot create personalized property alerts that drive engagement and conversions.</p><p>Host your real estate site with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ("free-ai-video-editing-tools-2026.html",
     "10 Best Free AI Video Editing Tools in 2026",
     "Edit videos with AI for free. Compare CapCut, DaVinci Resolve, and more free AI video editors.",
     '<h1>10 Best Free AI Video Editing Tools in 2026</h1><p class="article-meta">Published: 2026-06-23</p><p>Professional video editing with AI does not have to cost anything.</p><h2>1. CapCut</h2><p>ByteDance free AI video editor. Auto-captions, text-to-speech, transitions, effects. Completely free with no watermark.</p><h2>2. DaVinci Resolve</h2><p>Professional-grade free editor with AI color grading, voice isolation, and facial recognition.</p><h2>3. Canva Video</h2><p>Browser-based editor with AI-powered editing features. Generous free tier for basic editing.</p><h2>4. Clipchamp</h2><p>Microsoft free video editor. AI auto-composition and text-to-speech. Pre-installed on Windows 11.</p><p>Try <a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a> for free AI voiceovers.</p><p>Browse <a href="../tools/">AI video tools</a>.</p>'),
    ("free-ai-audio-tools-2026.html",
     "12 Best Free AI Audio Tools in 2026",
     "Free AI tools for audio production, voiceovers, music generation, and podcasting.",
     '<h1>12 Best Free AI Audio Tools in 2026</h1><p class="article-meta">Published: 2026-06-23</p><p>Create professional audio with AI for zero cost.</p><h2>Voice Generation</h2><p><a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a> offers a generous free tier with 10,000 characters per month. Natural-sounding voices in 29 languages.</p><h2>Music Generation</h2><p>Suno and Udio create original music from text prompts. Free tiers available for experimentation and prototyping.</p><h2>Podcast Editing</h2><p>Descript and Adobe Podcast offer free AI-powered audio editing. Remove filler words and background noise automatically.</p><h2>Transcription</h2><p>Otter.ai (free tier) and OpenAI Whisper (free open-source) provide accurate speech-to-text transcription.</p><p>Browse more <a href="../tools/">AI audio tools</a>.</p>'),
]

for a in articles:
    make(*a)

total = len([f for f in os.listdir(adir) if f.endswith(".html")])
print(f"\n=== Batch complete: {len(articles)} new articles created ===")
print(f"Total articles in directory: {total}")
