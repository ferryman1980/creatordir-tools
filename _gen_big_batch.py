import os, re

base = r'D:\项目\工作区\工作5'
adir = os.path.join(base, 'articles')

with open(os.path.join(adir, 'ai-article-writer-2026.html'), 'r', encoding='utf-8') as f:
    s = f.read()

tb = s[:s.index('<article class="article-content">')]
ta = s[s.index('</article>') + 10:]

def make(fn, title, desc, body):
    url = 'https://creatordir-tools.vercel.app/articles/' + fn
    og = title + ' - CreatorAI Tools'
    h = tb
    h = re.sub(r'<title>.*?</title>', '<title>' + og + '</title>', h)
    h = re.sub(r'property="og:title" content="[^"]*"', 'property="og:title" content="' + og + '"', h)
    h = re.sub(r'property="og:description" content="[^"]*"', 'property="og:description" content="' + desc + '"', h)
    h = re.sub(r'property="og:url" content="[^"]*"', 'property="og:url" content="' + url + '"', h)
    h += '\n<article class="article-content">\n' + body + '\n</article>\n' + ta
    with open(os.path.join(adir, fn), 'w', encoding='utf-8') as f:
        f.write(h)
    print('Created: ' + fn)

articles = [
    ('top-ai-video-editors-2026.html', 'Top 10 AI Video Editors in 2026 Ranked', 'Ranked list of the best AI video editors for 2026.',
     '<h1>Top 10 AI Video Editors in 2026 Ranked</h1><p class="article-meta">Published: 2026-06-23</p><p>We ranked the best AI video editors based on features, price, and ease of use.</p><h2>1. CapCut</h2><p>Best free option. AI captions, effects, text-to-speech. Used by 500M+ creators.</p><h2>2. Runway Gen-3</h2><p>Best for creative video. Text-to-video, inpainting. /mo.</p><h2>3. Descript</h2><p>Best for editing by text. AI-powered editing, filler word removal. /mo.</p><p>Use <a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a> for professional voiceovers.</p>'),
    ('best-ai-noise-reduction-tools-2026.html', '5 Best AI Noise Reduction Tools 2026', 'Remove background noise from audio with AI. Top tools compared.',
     '<h1>5 Best AI Noise Reduction Tools 2026</h1><p>Clean audio is essential for professional content.</p><h2>1. Adobe Podcast</h2><p>Free. AI-powered noise removal. Web-based.</p><h2>2. Krisp</h2><p>Real-time noise removal. /mo. Best for meetings.</p><h2>3. Descript</h2><p>Studio Sound feature. AI noise reduction built-in.</p><p>Use <a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a> for clean AI voiceovers.</p>'),
    ('ai-caption-generator-tools-2026.html', '8 Best AI Caption Generator Tools 2026', 'Auto-generate captions and subtitles with AI for videos and social media.',
     '<h1>8 Best AI Caption Generator Tools 2026</h1><p>Auto-captions save hours of manual work.</p><h2>1. CapCut</h2><p>Free AI auto-captions for TikTok, YouTube, Reels.</p><h2>2. Descript</h2><p>AI transcription + caption export. /mo.</p><h2>3. Otter.ai</h2><p>Best for meetings and podcasts. Free tier.</p><p>Host your site with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ('best-ai-transcription-services-2026.html', '7 Best AI Transcription Services 2026', 'Accurate speech-to-text with AI. Compare top transcription tools.',
     '<h1>7 Best AI Transcription Services 2026</h1><p>AI transcription is faster and cheaper than human transcription.</p><h2>1. Otter.ai</h2><p>Free tier. Real-time transcription. Best for meetings.</p><h2>2. Whisper</h2><p>OpenAI free open-source. 99% accuracy. Download for free.</p><h2>3. Rev AI</h2><p>API for developers. .25/min. High accuracy.</p><p>Try <a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a> to add voice to your transcriptions.</p>'),
    ('best-ai-screen-recorder-2026.html', '6 Best AI Screen Recorders 2026', 'Record your screen with AI-enhanced features for tutorials and demos.',
     '<h1>6 Best AI Screen Recorders 2026</h1><p>Screen recording with AI features saves editing time.</p><h2>1. Loom AI</h2><p>Auto-enhance, filler word removal, chapters. Free tier.</p><h2>2. OBS Studio</h2><p>Free open-source. AI plugins available.</p><h2>3. Screen Studio</h2><p>Mac only. AI cursor enhancement.  one-time.</p><p>Host your tutorials with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ('best-ai-thumbnail-maker-2026.html', '10 Best AI Thumbnail Makers 2026', 'Create clickable YouTube thumbnails with AI. Top tools compared.',
     '<h1>10 Best AI Thumbnail Makers 2026</h1><p>Thumbnails drive clicks. AI makes them faster.</p><h2>1. Canva AI</h2><p>AI thumbnail generator. Templates included. Free tier.</p><h2>2. Midjourney</h2><p>Stunning custom thumbnails. -60/mo.</p><h2>3. Adobe Express</h2><p>Free. AI-powered design suggestions.</p><p>Use <a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a> for YouTube voiceovers.</p>'),
    ('best-ai-video-script-generator-2026.html', '9 Best AI Video Script Generators 2026', 'Generate engaging video scripts with AI. Perfect for YouTube and TikTok.',
     '<h1>9 Best AI Video Script Generators 2026</h1><p>Video scripts in seconds, not hours.</p><h2>1. ChatGPT</h2><p>Best versatility. Customizable scripts for any niche.</p><h2>2. Jasper AI</h2><p>Best for branded content. Templates included. /mo.</p><h2>3. Writesonic</h2><p>Affordable. /mo. YouTube script templates.</p><p>Get <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a> for your video site.</p>'),
    ('ai-video-enhancer-tools-2026.html', '7 Best AI Video Enhancer Tools 2026', 'Upscale and enhance video quality with AI. 4K upscaling, denoising, and more.',
     '<h1>7 Best AI Video Enhancer Tools 2026</h1><p>AI enhances video quality automatically.</p><h2>1. Topaz Video AI</h2><p>Best upscaling. 4K from 720p.  one-time.</p><h2>2. Runway Gen-3</h2><p>Video enhancement built-in. /mo.</p><h2>3. CapCut</h2><p>Free AI enhancement. Upscale to 4K.</p><p>Browse <a href="../tools/">AI video tools</a>.</p>'),
    ('best-ai-image-upscaler-2026.html', '8 Best AI Image Upscalers 2026', 'Upscale images to 4K/8K with AI. Free and paid tools compared.',
     '<h1>8 Best AI Image Upscalers 2026</h1><p>AI upscaling makes low-res images look professional.</p><h2>1. Topaz Gigapixel</h2><p>Best quality.  one-time. 6x upscale.</p><h2>2. Clipdrop</h2><p>Free. Stability AI. Quick upscale.</p><h2>3. Let Enhance</h2><p>Free tier. AI enhancement + upscale.</p><p>Host your portfolio with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ('best-ai-background-remover-2026.html', '10 Best AI Background Removers 2026', 'Remove backgrounds from images instantly with AI. Free and paid options.',
     '<h1>10 Best AI Background Removers 2026</h1><p>Remove backgrounds in one click with AI.</p><h2>1. Remove.bg</h2><p>Industry standard. Free preview. .99/image full res.</p><h2>2. Adobe Express</h2><p>Free. Integrated with Creative Cloud.</p><h2>3. Canva AI</h2><p>Free. One-click background removal. Pro /mo.</p><p>Browse all <a href="../tools/">AI image tools</a>.</p>'),
    ('best-ai-image-generator-free-2026.html', '12 Best Free AI Image Generators 2026', 'Generate images with AI for free. No credit card required.',
     '<h1>12 Best Free AI Image Generators 2026</h1><p>Create stunning AI images at zero cost.</p><h2>1. Leonardo AI</h2><p>150 free credits daily. High quality. Best free option.</p><h2>2. Stable Diffusion</h2><p>Free open-source. Run locally. Unlimited.</p><h2>3. Clipdrop</h2><p>Free. Stable Diffusion powered. No login needed.</p><p>Use <a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a> for AI voiceovers.</p>'),
    ('best-ai-logo-maker-2026.html', '9 Best AI Logo Makers 2026', 'Design professional logos with AI. Free and premium options.',
     '<h1>9 Best AI Logo Makers 2026</h1><p>Create a professional logo in minutes with AI.</p><h2>1. Looka</h2><p>AI logo designer.  one-time. High quality.</p><h2>2. Canva AI</h2><p>Free. AI logo templates. Easy customization.</p><h2>3. Hatchful by Shopify</h2><p>Free. AI-powered. Multiple formats.</p><p>Host your site with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ('ai-social-media-scheduler-2026.html', '7 Best AI Social Media Schedulers 2026', 'Schedule and optimize social media posts with AI. Best tools for automation.',
     '<h1>7 Best AI Social Media Schedulers 2026</h1><p>AI scheduling saves hours of manual posting.</p><h2>1. Buffer</h2><p>AI scheduling. Best posting times. Free tier.</p><h2>2. Hootsuite</h2><p>Enterprise features. AI content suggestions. /mo.</p><h2>3. Later</h2><p>Best for Instagram. AI visual planner. Free tier.</p><p>Browse <a href="../tools/">AI marketing tools</a>.</p>'),
    ('best-ai-hashtag-generator-2026.html', '6 Best AI Hashtag Generators 2026', 'Generate viral hashtags with AI for Instagram, TikTok, and Twitter.',
     '<h1>6 Best AI Hashtag Generators 2026</h1><p>AI finds the best hashtags for maximum reach.</p><h2>1. Display Purposes</h2><p>Free. AI-powered hashtag recommendations. Clean UI.</p><h2>2. Later</h2><p>AI hashtag suggestions built-in. Free tier.</p><h2>3. Hashtag Expert</h2><p>AI analysis of trending tags. /mo.</p><p>Browse <a href="../tools/">AI marketing tools</a>.</p>'),
    ('best-ai-email-marketing-tools-2026.html', '10 Best AI Email Marketing Tools 2026', 'Optimize email campaigns with AI. Compare Mailchimp, ConvertKit, and more.',
     '<h1>10 Best AI Email Marketing Tools 2026</h1><p>AI makes email marketing more effective and personal.</p><h2>1. Mailchimp</h2><p>AI subject lines, send time optimization. Free tier up to 500 contacts.</p><h2>2. ConvertKit</h2><p>Best for creators. AI email sequences. /mo.</p><h2>3. ActiveCampaign</h2><p>AI predictive sending. Advanced automation. /mo.</p><p>Get <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a> for your email landing page.</p>'),
    ('best-ai-crm-tools-2026.html', '8 Best AI CRM Tools for Small Business 2026', 'Manage customer relationships with AI-powered CRM. Top picks for small business.',
     '<h1>8 Best AI CRM Tools for Small Business 2026</h1><p>AI CRM helps small businesses compete with enterprise.</p><h2>1. HubSpot</h2><p>Free CRM with AI features. Contact scoring, email tracking.</p><h2>2. Salesforce Einstein</h2><p>Enterprise AI CRM. Predictive analytics. /mo.</p><h2>3. Zoho CRM</h2><p>Affordable AI CRM. /mo. AI sales assistant.</p><p>Browse <a href="../tools/">AI marketing tools</a>.</p>'),
    ('best-ai-analytics-tools-2026.html', '9 Best AI Analytics Tools 2026', 'Data analysis and visualization with AI. Tools for business intelligence.',
     '<h1>9 Best AI Analytics Tools 2026</h1><p>AI analytics find insights faster than manual analysis.</p><h2>1. Google Analytics 4</h2><p>AI-powered insights. Free. Industry standard.</p><h2>2. Mixpanel</h2><p>AI product analytics. Free tier. User behavior tracking.</p><h2>3. Hotjar</h2><p>AI heatmaps and recordings. Free tier. User behavior.</p><p>Browse <a href="../tools/">AI tools</a>.</p>'),
    ('best-ai-productivity-tools-2026.html', '20 Best AI Productivity Tools 2026', 'Boost productivity with AI. Task management, notes, automation tools.',
     '<h1>20 Best AI Productivity Tools 2026</h1><p>AI productivity tools save 20+ hours per week.</p><h2>1. Notion AI</h2><p>AI writing, summarization, project management. /mo add-on.</p><h2>2. Motion</h2><p>AI calendar and task management. /mo.</p><h2>3. Mem</h2><p>AI-powered notes. Auto-organize. Free tier.</p><p>Get <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ('best-ai-meeting-assistant-2026.html', '7 Best AI Meeting Assistants 2026', 'AI tools that take meeting notes, transcribe, and summarize automatically.',
     '<h1>7 Best AI Meeting Assistants 2026</h1><p>Never take meeting notes again with AI.</p><h2>1. Otter.ai</h2><p>Best for transcription. Free tier. Real-time notes.</p><h2>2. Fireflies</h2><p>AI meeting assistant. /mo. CRM integration.</p><h2>3. Fathom</h2><p>Free. AI meeting notes. Zoom integration.</p><p>Try <a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a> for meeting voiceovers.</p>'),
    ('best-ai-research-tools-2026.html', '10 Best AI Research Tools 2026', 'Academic research with AI. Literature review, citations, and analysis tools.',
     '<h1>10 Best AI Research Tools 2026</h1><p>AI accelerates academic research significantly.</p><h2>1. Perplexity AI</h2><p>AI research assistant. Citations included. Free tier.</p><h2>2. Scite</h2><p>AI citation analysis. /mo. See how papers are cited.</p><h2>3. Elicit</h2><p>AI literature review. Extract data from papers.</p><p>Browse <a href="../tools/">AI tools</a>.</p>'),
    ('best-ai-coding-assistant-2026.html', '12 Best AI Coding Assistants 2026', 'AI coding tools that help developers write better code faster.',
     '<h1>12 Best AI Coding Assistants 2026</h1><p>AI coding assistants boost developer productivity by 55%.</p><h2>1. GitHub Copilot</h2><p>Best overall. VS Code integration. /mo.</p><h2>2. Cursor</h2><p>AI-first IDE. Best for code generation. /mo.</p><h2>3. Claude</h2><p>Best for complex reasoning. 200K context.</p><p>Host your projects with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ('best-ai-website-builder-2026.html', '9 Best AI Website Builders 2026', 'Build websites with AI. No coding required. Best platforms compared.',
     '<h1>9 Best AI Website Builders 2026</h1><p>AI builds complete websites from a prompt.</p><h2>1. Wix ADI</h2><p>AI website builder. Answer questions, get a site. /mo.</p><h2>2. Hostinger Website Builder</h2><p>AI builder included. <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">60% off</a>. Quick setup.</p><h2>3. Framer AI</h2><p>AI design to code. Beautiful sites. /mo.</p>'),
    ('best-ai-form-builder-2026.html', '6 Best AI Form Builders 2026', 'Create forms and surveys with AI. Best tools for data collection.',
     '<h1>6 Best AI Form Builders 2026</h1><p>AI creates forms in seconds instead of hours.</p><h2>1. Typeform</h2><p>Beautiful forms. AI form builder. /mo.</p><h2>2. Jotform</h2><p>AI form generator. Free tier. 10,000 submissions/mo.</p><h2>3. Google Forms</h2><p>Free. Basic AI suggestions. Google integration.</p><p>Browse <a href="../tools/">AI tools</a>.</p>'),
    ('ai-chatbot-vs-live-chat-2026.html', 'AI Chatbot vs Live Chat 2026: Which is Better?', 'Compare AI chatbots with human live chat for customer service.',
     '<h1>AI Chatbot vs Live Chat 2026: Which is Better?</h1><p>Both have strengths. Here is the comparison.</p><h2>AI Chatbot Pros</h2><p>24/7 availability, instant responses, lower cost, scalable.</p><h2>Live Chat Pros</h2><p>Human empathy, complex problem solving, personal touch.</p><h2>Best Approach</h2><p>Hybrid: AI handles 80% of queries, humans handle complex cases.</p><p>Host with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ('best-ai-translation-tools-2026.html', '8 Best AI Translation Tools 2026', 'Translate content with AI. Best tools for accuracy and language support.',
     '<h1>8 Best AI Translation Tools 2026</h1><p>AI translation handles 100+ languages with near-human accuracy.</p><h2>1. DeepL</h2><p>Best accuracy. European languages. Free tier (1500 chars).</p><h2>2. Google Translate</h2><p>133 languages. Free. Best for global reach.</p><h2>3. ChatGPT</h2><p>Context-aware translation. Understands nuance. Free.</p><p>Check <a href="../tools/">AI tools</a> for more.</p>'),
]

for a in articles:
    make(*a)

total = len([f for f in os.listdir(adir) if f.endswith('.html') and f != 'index.html'])
print(f'\nCreated: {len(articles)} new articles')
print(f'Total articles: {total}')
