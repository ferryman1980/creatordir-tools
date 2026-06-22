import json, os
base = r'D:\项目\工作区\工作5'

tweets = [
    'Discover 100+ AI tools curated for content creators. From writing to video, all in one place! 🚀 https://creatordir-tools.vercel.app #aitools #creators',
    'Stop jumping between 50 tabs. We handpicked the best AI tools for writers, designers, and video creators. 📚 https://creatordir-tools.vercel.app #AI #productivity',
    'New: ChatGPT vs Claude vs Gemini 2026 comparison. Which AI assistant actually wins? Full breakdown: https://creatordir-tools.vercel.app/articles/chatgpt-vs-claude-vs-gemini-2026.html',
    'Turn text into studio-quality voiceovers with ElevenLabs. 29 languages, natural voices. Try it: https://try.elevenlabs.io/ebksqtv6a5m6',
    'Need hosting for your next project? Hostinger 60% OFF - faster servers, lower cost. https://www.hostinger.com?REFERRALCODE=ECA346010F8J #webhosting',
    '10 free AI video editors that rival premium software. CapCut, DaVinci Resolve, and more: https://creatordir-tools.vercel.app/articles/free-ai-video-editing-tools-2026.html',
    'Can AI really replace writers? We tested ChatGPT, Claude, Jasper for 30 days. Results: https://creatordir-tools.vercel.app/articles/chatgpt-30-days.html',
    'Midjourney vs DALL-E vs Stable Diffusion 2026 - which creates the best images? https://creatordir-tools.vercel.app/articles/midjourney-vs-dall-e-vs-stable-diffusion-2026.html',
    '15 ways to make money with AI tools in 2026 (proven methods): https://creatordir-tools.vercel.app/articles/how-to-make-money-ai-tools-2026.html',
    'Your complete AI SEO guide for 2026. Rank higher, faster: https://creatordir-tools.vercel.app/articles/ai-seo-guide-2026.html',
    'FREE AI audio tools - voiceovers, music, podcast editing at zero cost: https://creatordir-tools.vercel.app/articles/free-ai-audio-tools-2026.html',
    'Building a faceless YouTube channel with AI? Here is exactly how: https://creatordir-tools.vercel.app/articles/faceless-youtube-ai.html',
    'Best AI tools for small business owners in 2026 (save 20+ hrs/week): https://creatordir-tools.vercel.app/articles/best-ai-tools-small-business-2026.html',
    'Grammarly vs ProWritingAid vs Hemingway - Which writing assistant is best? https://creatordir-tools.vercel.app/articles/grammarly-vs-pro-writing-aid-vs-hemingway-2026.html',
    'Runway vs Pika vs Synthesia - The ultimate AI video tool comparison: https://creatordir-tools.vercel.app/articles/runway-vs-pika-vs-synthesia-2026.html',
    '20 AI tools for YouTube creators that actually work (2026 tested): https://creatordir-tools.vercel.app/articles/best-ai-tools-youtube-2026.html',
    '25 AI tools for TikTok creators - go viral faster: https://creatordir-tools.vercel.app/articles/best-ai-tools-tiktok-2026.html',
    'Growing on Instagram? These 20 AI tools will 10x your growth: https://creatordir-tools.vercel.app/articles/best-ai-tools-instagram-2026.html',
    'Real estate agents: 15 AI tools that close more deals: https://creatordir-tools.vercel.app/articles/best-ai-tools-realtors-2026.html',
    '10 best AI chatbots for customer service in 2026: https://creatordir-tools.vercel.app/articles/best-ai-chatbots-2026.html',
    'Want to build an AI startup? Our repo has 87+ GitHub resources: https://github.com/ferryman1980/creatordir-tools',
    'Best free AI tools for creators - 50 tools at zero cost: https://creatordir-tools.vercel.app/articles/best-free-ai-tools-2026.html',
    'Your AI toolkit is incomplete without these essentials: https://creatordir-tools.vercel.app/',
    'Hostinger 60% off sale is live. Perfect for hosting AI apps and websites: https://www.hostinger.com?REFERRALCODE=ECA346010F8J',
    '54 AI tools, 111 guides, all in one directory: https://creatordir-tools.vercel.app/',
    'Jasper vs Writesonic vs Copy.ai - which AI writer wins? https://creatordir-tools.vercel.app/articles/jasper-vs-writesonic-vs-copyai-2026.html',
    'Teachers: 20 AI tools that save 10+ hours weekly: https://creatordir-tools.vercel.app/articles/best-ai-tools-teachers-2026.html',
    'AI tools for marketers - SEO, email, social complete guide: https://creatordir-tools.vercel.app/articles/best-ai-tools-marketers-2026.html',
    'Clone your voice with AI - honest review after 50 videos: https://creatordir-tools.vercel.app/articles/ai-voice-clone-experiment.html',
]

reddit = [
    {'sub': 'ArtificialIntelligence', 'title': 'I built a directory of 100+ AI tools tested for content creators', 'body': 'I spent months testing AI tools for content creation and built a directory at https://creatordir-tools.vercel.app\n\n111 detailed articles, 54 tool reviews, and honest pros/cons for each tool.\n\nTopics: AI writing, design, video, audio, marketing, productivity.\n\nEverything is free. Would love your feedback!'},
    {'sub': 'webdev', 'title': 'Show HN: AI tools directory with 100+ tools - full source on GitHub', 'body': 'Built an AI tools directory at https://creatordir-tools.vercel.app\n\nTech stack: Plain HTML/CSS/JS, Vercel deploy.\n\nSource: https://github.com/ferryman1980/creatordir-tools\n\nFeatures: 111 articles, search, categories, affiliate deals page.\n\nOpen to PRs!'},
    {'sub': 'Entrepreneur', 'title': 'I built a monetized AI tools directory - current strategy + results', 'body': 'Launched https://creatordir-tools.vercel.app 3 weeks ago.\n\nCurrent: 111 articles, affiliate links (ElevenLabs, Hostinger 60%), Ko-fi donations.\n\nStrategy: Content volume + SEO + affiliate = passive income.\n\nHappy to answer questions.'},
]

linkedin = [
    'I curated 100+ AI tools for content creators into one directory.\n\nAfter months of testing, I created a single resource where creators can find:\n- AI Writing (ChatGPT, Jasper, Claude)\n- AI Design (Midjourney, Canva)\n- AI Video (CapCut, Runway)\n- AI Audio (ElevenLabs)\n\nhttps://creatordir-tools.vercel.app\n\nWhat AI tools have you been using?',
    'Want to make money with AI? Here are 5 proven methods:\n1. AI Content Writing (-500/post)\n2. AI Voiceover Services\n3. AI Video Creation\n4. Digital Products\n5. Affiliate Marketing (e.g., Hostinger 60% commissions)\n\nFull guide: https://creatordir-tools.vercel.app/articles/how-to-make-money-ai-tools-2026.html',
]

ph = {
    'title': 'CreatorAI Tools - Curated Directory for Content Creators',
    'tagline': '100+ AI tools tested by real creators with honest reviews',
    'description': 'A curated directory of AI tools for content creators. Writing, design, video, audio, marketing, and productivity tools with honest reviews, comparisons, and how-to guides.'
}

with open(os.path.join(base, 'promo_english.txt'), 'w', encoding='utf-8') as f:
    f.write('=== TWITTER POSTS (30) ===\n\n')
    for i, t in enumerate(tweets, 1):
        f.write(str(i) + '. ' + t + '\n\n')
    f.write('=== REDDIT POSTS ===\n\n')
    for r in reddit:
        f.write('r/' + r['sub'] + '\nTitle: ' + r['title'] + '\nBody: ' + r['body'] + '\n\n')
    f.write('=== LINKEDIN POSTS ===\n\n')
    for l in linkedin:
        f.write(l + '\n\n')
    f.write('=== PRODUCT HUNT ===\n\n')
    f.write(json.dumps(ph, indent=2))

print('Promo file created!')
print('30 tweets, 3 Reddit posts, 2 LinkedIn posts, 1 Product Hunt')
