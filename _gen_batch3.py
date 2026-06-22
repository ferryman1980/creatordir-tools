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

new = [
    ('best-ai-podcast-editing-2026.html', '8 Best AI Podcast Editing Tools 2026', 'Edit podcasts with AI. Remove filler words, noise, and silence automatically.',
     '<h1>8 Best AI Podcast Editing Tools 2026</h1><h2>1. Descript</h2><p>Edit audio by editing text. Studio Sound. /mo.</p><h2>2. Adobe Podcast</h2><p>Free. AI noise removal. Enhance speech.</p><h2>3. Auphonic</h2><p>AI leveling and mastering. Free tier. Podcast standard.</p><p>Try <a href="https://try.elevenlabs.io/ebksqtv6a5m6" rel="nofollow sponsored">ElevenLabs</a> for intros.</p><p>Get <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ('best-ai-music-production-2026.html', '10 Best AI Music Production Tools 2026', 'Create music with AI. From text to song in seconds.',
     '<h1>10 Best AI Music Production Tools 2026</h1><h2>1. Suno</h2><p>Text to song. Free tier. Viral on social media.</p><h2>2. Udio</h2><p>High quality music generation. Free tier.</p><h2>3. MusicFX</h2><p>Google AI music. Free. Text-to-music.</p><p>Browse <a href="../tools/">AI audio tools</a>.</p>'),
    ('best-ai-voice-cloning-2026.html', '6 Best AI Voice Cloning Tools 2026', 'Clone any voice with AI. Realistic voice cloning for content creators.',
     '<h1>6 Best AI Voice Cloning Tools 2026</h1><h2>1. ElevenLabs</h2><p>Best voice cloning. 29 languages. <a href="https://try.elevenlabs.io/ebksqtv6a5m6" rel="nofollow sponsored">Try ElevenLabs</a></p><h2>2. Resemble AI</h2><p>Custom voice clones. /mo.</p><h2>3. Play.ht</h2><p>Text-to-speech with cloning. /mo.</p><p>Host your site with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ('best-ai-avatar-generator-2026-v2.html', '9 Best AI Avatar Generators 2026 Updated', 'Create AI avatars for social media, profiles, and content.',
     '<h1>9 Best AI Avatar Generators 2026 Updated</h1><h2>1. Synthesia</h2><p>AI video avatars. /mo. 140+ avatars.</p><h2>2. HeyGen</h2><p>AI talking avatars. /mo. Realistic.</p><h2>3. Midjourney</h2><p>Custom avatar portraits. Artistic style. /mo.</p><p>Browse <a href="../tools/">AI video tools</a>.</p>'),
    ('best-ai-storyboard-generator-2026.html', '5 Best AI Storyboard Generators 2026', 'Generate storyboards with AI for video production and animation.',
     '<h1>5 Best AI Storyboard Generators 2026</h1><h2>1. Storyboarder</h2><p>Free. AI shot suggestions. Open-source.</p><h2>2. Boords</h2><p>AI storyboard generator. /mo. Professional.</p><h2>3. Midjourney</h2><p>Generate storyboard frames. /mo.</p><p>Check <a href="../tools/">AI video tools</a>.</p>'),
    ('best-ai-3d-model-generator-2026.html', '7 Best AI 3D Model Generators 2026', 'Generate 3D models from text or images with AI.',
     '<h1>7 Best AI 3D Model Generators 2026</h1><h2>1. Meshy</h2><p>Text to 3D. /mo. Game-ready models.</p><h2>2. Luma AI</h2><p>3D from video. Photorealistic. Free tier.</p><h2>3. Spline AI</h2><p>AI 3D design. Browser-based. Free tier.</p><p>Host your 3D portfolio with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ('best-ai-animation-tools-2026.html', '8 Best AI Animation Tools 2026', 'Create animations with AI. From text to animated video.',
     '<h1>8 Best AI Animation Tools 2026</h1><h2>1. Runway Gen-3</h2><p>Text-to-animation. /mo. High quality.</p><h2>2. Pika Labs</h2><p>Free tier. Quick animations. Style transfer.</p><h2>3. Animaker AI</h2><p>AI character animation. .5/mo. Beginner friendly.</p><p>Use <a href="https://try.elevenlabs.io/ebksqtv6a5m6" rel="nofollow sponsored">ElevenLabs</a> for voiceovers.</p>'),
    ('best-ai-presentation-maker-2026.html', '10 Best AI Presentation Makers 2026', 'Create beautiful presentations with AI in seconds.',
     '<h1>10 Best AI Presentation Makers 2026</h1><h2>1. Gamma</h2><p>AI presentations. Beautiful designs. Free tier.</p><h2>2. Canva AI</h2><p>AI presentation designer. Templates. Free.</p><h2>3. Beautiful.ai</h2><p>AI design rules. /mo. Professional.</p><p>Get <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ('best-ai-data-visualization-2026.html', '7 Best AI Data Visualization Tools 2026', 'Create stunning charts and infographics with AI.',
     '<h1>7 Best AI Data Visualization Tools 2026</h1><h2>1. Tableau AI</h2><p>AI-powered analytics. /mo. Enterprise grade.</p><h2>2. Canva AI</h2><p>AI infographic maker. Free tier. Easy to use.</p><h2>3. Datawrapper</h2><p>Free for journalists. AI chart suggestions.</p><p>Browse <a href="../tools/">AI tools</a>.</p>'),
    ('best-ai-content-writing-service-2026.html', '8 Best AI Content Writing Services 2026', 'Compare AI writing services for blogs, ads, and social media content.',
     '<h1>8 Best AI Content Writing Services 2026</h1><h2>1. Jasper AI</h2><p>Best for brand content. Templates. /mo.</p><h2>2. Writesonic</h2><p>Best value. GPT-4. /mo. Unlimited words.</p><h2>3. Copy.ai</h2><p>Best for workflow automation. /mo.</p><p>Use <a href="https://try.elevenlabs.io/ebksqtv6a5m6" rel="nofollow sponsored">ElevenLabs</a> for audio versions.</p>'),
    ('best-ai-email-writer-2026.html', '6 Best AI Email Writers 2026', 'Write professional emails with AI. Cold emails, newsletters, and follow-ups.',
     '<h1>6 Best AI Email Writers 2026</h1><h2>1. ChatGPT</h2><p>Versatile email writing. Free. Custom tone.</p><h2>2. Jasper AI</h2><p>Email templates. Brand voice. /mo.</p><h2>3. Copy.ai</h2><p>Cold email workflows. A/B testing. /mo.</p><p>Host your email landing page with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ('best-ai-resume-writer-2026.html', '9 Best AI Resume Writers 2026', 'Create ATS-optimized resumes with AI. Land more interviews.',
     '<h1>9 Best AI Resume Writers 2026</h1><h2>1. Kickresume</h2><p>AI resume builder.  one-time. ATS-friendly.</p><h2>2. Rezi</h2><p>AI resume optimization. Free tier. ATS scoring.</p><h2>3. ChatGPT</h2><p>Custom resume writing. Free. Tailored content.</p><p>Browse <a href="../tools/">AI writing tools</a>.</p>'),
    ('best-ai-book-writing-2026.html', '7 Best AI Book Writing Tools 2026', 'Write books and novels with AI assistance. From outline to manuscript.',
     '<h1>7 Best AI Book Writing Tools 2026</h1><h2>1. Claude</h2><p>200K context. Best for long-form. Reasonable.</p><h2>2. Jasper AI</h2><p>Book templates. Long-form assistant. /mo.</p><h2>3. Sudowrite</h2><p>AI novel writing. /mo. Creative focus.</p><p>Get <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" rel="nofollow sponsored">Hostinger 60% off</a> for your author site.</p>'),
    ('best-ai-grammar-checker-2026.html', '5 Best AI Grammar Checkers 2026', 'Fix grammar, spelling, and style with AI writing assistants.',
     '<h1>5 Best AI Grammar Checkers 2026</h1><h2>1. Grammarly</h2><p>Best all-around. Free tier. Premium /mo.</p><h2>2. ProWritingAid</h2><p>Deep analysis. Style reports. /mo.</p><h2>3. LanguageTool</h2><p>Open-source. 25+ languages. Free tier.</p><p>Browse <a href="../tools/">AI writing tools</a>.</p>'),
    ('best-ai-plagiarism-checker-2026.html', '6 Best AI Plagiarism Checkers 2026', 'Check content for plagiarism with AI-powered tools.',
     '<h1>6 Best AI Plagiarism Checkers 2026</h1><h2>1. Turnitin</h2><p>Academic standard. Institutional. Most accurate.</p><h2>2. Grammarly</h2><p>Built-in plagiarism check. Premium /mo.</p><h2>3. Copyscape</h2><p>Web content check. .03/search. Industry standard.</p><p>Check <a href="../tools/">AI writing tools</a>.</p>'),
    ('best-ai-headline-generator-2026.html', '9 Best AI Headline Generators 2026', 'Generate clickable headlines with AI for blogs, ads, and social media.',
     '<h1>9 Best AI Headline Generators 2026</h1><h2>1. ChatGPT</h2><p>Generate 10+ headline variations. Free. Custom tone.</p><h2>2. Copy.ai</h2><p>Headline templates. Emotional targeting. /mo.</p><h2>3. Jasper AI</h2><p>Brand voice headlines. A/B testing. /mo.</p><p>Try <a href="https://try.elevenlabs.io/ebksqtv6a5m6" rel="nofollow sponsored">ElevenLabs</a> for headlines audio.</p>'),
    ('best-ai-product-description-2026.html', '7 Best AI Product Description Generators 2026', 'Generate compelling product descriptions with AI for e-commerce.',
     '<h1>7 Best AI Product Description Generators 2026</h1><h2>1. Jasper AI</h2><p>E-commerce templates. /mo. Bulk generation.</p><h2>2. Copy.ai</h2><p>Product workflows. /mo. A/B testing.</p><h2>3. Writesonic</h2><p>Affordable. /mo. 70+ templates.</p><p>Sell better with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" rel="nofollow sponsored">Hostinger 60% off</a> hosting.</p>'),
    ('best-ai-ad-generator-2026.html', '8 Best AI Ad Generators 2026', 'Create high-converting ads with AI for Google, Facebook, and social media.',
     '<h1>8 Best AI Ad Generators 2026</h1><h2>1. Copy.ai</h2><p>Ad workflow automation. /mo. A/B testing.</p><h2>2. Jasper AI</h2><p>Ad copy templates. Brand voice. /mo.</p><h2>3. AdCreative.ai</h2><p>AI ad design + copy. /mo. Conversion focused.</p><p>Browse <a href="../tools/">AI marketing tools</a>.</p>'),
    ('best-ai-seo-keyword-tool-2026.html', '10 Best AI SEO Keyword Tools 2026', 'Find profitable keywords with AI. SEO research tools compared.',
     '<h1>10 Best AI SEO Keyword Tools 2026</h1><h2>1. Semrush</h2><p>AI keyword magic tool. /mo. Industry standard.</p><h2>2. Ahrefs</h2><p>Best backlink analysis. /mo. Keyword explorer.</p><h2>3. Surfer SEO</h2><p>AI content optimization. /mo. On-page SEO.</p><p>Host your site with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ('best-ai-voice-assistant-2026.html', '6 Best AI Voice Assistants 2026', 'Compare Siri, Google Assistant, Alexa, and new AI voice assistants.',
     '<h1>6 Best AI Voice Assistants 2026</h1><h2>1. ChatGPT Voice</h2><p>Best conversational AI. GPT-5 voice mode. Free.</p><h2>2. Google Assistant</h2><p>Google integration. Smart home. Free.</p><h2>3. Amazon Alexa</h2><p>Smart home focus. Skills ecosystem. Free.</p><p>Use <a href="https://try.elevenlabs.io/ebksqtv6a5m6" rel="nofollow sponsored">ElevenLabs</a> for custom voice apps.</p>'),
    ('best-ai-fashion-design-2026.html', '5 Best AI Fashion Design Tools 2026', 'Design clothing and fashion with AI. From concept to production.',
     '<h1>5 Best AI Fashion Design Tools 2026</h1><h2>1. Midjourney</h2><p>Fashion design concepts. /mo. Stunning visuals.</p><h2>2. CLO 3D</h2><p>3D garment simulation. /mo. Professional.</p><h2>3. DALL-E 3</h2><p>Fashion concepts. Included in ChatGPT Plus.</p><p>Browse <a href="../tools/">AI design tools</a>.</p>'),
    ('best-ai-interior-design-2026.html', '8 Best AI Interior Design Tools 2026', 'Redesign rooms with AI. Virtual staging and interior design.',
     '<h1>8 Best AI Interior Design Tools 2026</h1><h2>1. Interior AI</h2><p>Virtual room staging. Free tier. Multiple styles.</p><h2>2. Midjourney</h2><p>Design concepts. Artistic. /mo.</p><h2>3. REimagine Home</h2><p>AI home design. Free. Room transformation.</p><p>Host your design portfolio with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
    ('best-ai-education-tools-2026.html', '10 Best AI Education Tools 2026', 'AI tools for learning, tutoring, and online education.',
     '<h1>10 Best AI Education Tools 2026</h1><h2>1. Khan Academy Khanmigo</h2><p>AI tutor. /year. Best for students.</p><h2>2. ChatGPT</h2><p>Free tutor. Any subject. GPT-5 reasoning.</p><h2>3. Quizlet AI</h2><p>AI study sets. Magic Notes. Free tier.</p><p>Check <a href="../tools/">AI tools</a> for more.</p>'),
    ('best-ai-health-fitness-2026.html', '7 Best AI Health and Fitness Tools 2026', 'AI-powered health, fitness, and wellness apps and tools.',
     '<h1>7 Best AI Health and Fitness Tools 2026</h1><h2>1. MyFitnessPal AI</h2><p>AI meal logging. /mo. Calorie tracking.</p><h2>2. Whoop AI</h2><p>AI fitness coach. /mo. Strain tracking.</p><h2>3. ChatGPT</h2><p>Custom workout plans. Free. AI personal trainer.</p><p>Browse <a href="../tools/">AI tools</a>.</p>'),
    ('best-ai-travel-planning-2026.html', '6 Best AI Travel Planning Tools 2026', 'Plan trips with AI. Itineraries, flights, and accommodation.',
     '<h1>6 Best AI Travel Planning Tools 2026</h1><h2>1. ChatGPT</h2><p>Custom itineraries. Free. Budget optimization.</p><h2>2. Kayak AI</h2><p>AI flight search. Price prediction. Free.</p><h2>3. TripAdvisor AI</h2><p>AI recommendations. Reviews analysis. Free.</p><p>Host your travel blog with <a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" rel="nofollow sponsored">Hostinger 60% off</a>.</p>'),
]

for a in new:
    make(*a)

total = len([f for f in os.listdir(adir) if f.endswith('.html') and f != 'index.html'])
print(f'\nCreated: {len(new)} new articles')
print(f'Total articles: {total}')
