import os

articles_dir = r"D:\项目\工作区\工作5\articles"

articles = [
    {
        "filename": "ai-social-media-tools-2026.html",
        "title": "Best AI Social Media Management Tools 2026",
        "desc": "Compare the best AI social media management tools for 2026. From scheduling to content generation, find the perfect tool for your workflow.",
        "article_text": (
            '<h1>Best AI Social Media Management Tools 2026</h1>\n'
            '<p class="article-meta">Jun 13, 2026 \xb7 5 min read</p>\n'
            '<p>Managing multiple social media accounts manually is a time sink. AI social media tools now handle scheduling, content creation, analytics, and engagement \u2014 freeing you to focus on strategy. Here are the best AI social media management tools in 2026.</p>\n'
            '<h2>1. Buffer \u2014 Best AI Scheduling and Posting</h2>\n'
            '<p>Buffer AI Assistant analyzes your past top-performing posts and suggests optimal posting times, captions, and hashtags. The AI predicts engagement before you publish. Supports Instagram, TikTok, LinkedIn, Twitter, Facebook, and YouTube.</p>\n'
            '<p><a href="/go/?to=buffer">Try Buffer \u2192</a></p>\n'
            '<h2>2. Hootsuite \u2014 Best Enterprise Platform</h2>\n'
            '<p>Hootsuite OwlyWriter AI generates captions, post ideas, and hashtag sets from a URL or keyword. The AI analytics dashboard highlights what content resonates and recommends content mix adjustments.</p>\n'
            '<h2>3. Vista Social \u2014 Best Value All-in-One</h2>\n'
            '<p>Vista Social combines AI content generation, smart scheduling, and cross-platform analytics. AI Content Assistant writes platform-optimized posts from one brief. Built-in Canva integration streamlines visual creation.</p>\n'
            '<p><a href="/go/?to=vistasocial">Try Vista Social \u2192</a></p>\n'
            '<h2>4. ContentStudio \u2014 Best for Content Curation</h2>\n'
            '<p>ContentStudio AI curates relevant articles, news, and trending topics from your industry. The discovery engine scans millions of sources. Approval and collaboration tools are excellent for agencies.</p>\n'
            '<h2>5. Later \u2014 Best Visual-First Platform</h2>\n'
            '<p>Later AI-powered visual planner analyzes your feed aesthetics and suggests optimal image layouts. AI Caption Writer generates engaging copy for each platform. Best for Instagram and TikTok creators.</p>\n'
            '<h2>Which Should You Choose?</h2>\n'
            '<p>Buffer for solo creators. Hootsuite for enterprise teams. Vista Social for best value. ContentStudio for curation. Later for visual growth. Most offer free tiers \u2014 test before committing.</p>\n'
            '<p style="margin-top:2rem"><a href="https://ko-fi.com/kangjian" target="_blank" rel="noopener">\u2615 Support this guide on Ko-fi</a></p>\n'
        )
    },
    {
        "filename": "ai-email-marketing-tools-2026.html",
        "title": "AI Email Marketing Tools Compared 2026",
        "desc": "The best AI email marketing tools compared. From subject lines to automations, find which platform delivers the best ROI in 2026.",
        "article_text": (
            '<h1>AI Email Marketing Tools Compared: 2026 Edition</h1>\n'
            '<p class="article-meta">Jun 13, 2026 \xb7 5 min read</p>\n'
            '<p>Email marketing remains the highest ROI channel \u2014 and AI has made it dramatically more effective. AI tools now write subject lines, personalize content, optimize send times, and predict engagement.</p>\n'
            '<h2>1. Mailchimp \u2014 Best for Beginners</h2>\n'
            '<p>Mailchimp Creative Assistant generates branded email templates from your website. AI Subject Line Tester predicts open rates. Send Time Optimization schedules each subscriber at their peak engagement window.</p>\n'
            '<p><a href="/go/?to=mailchimp">Try Mailchimp \u2192</a></p>\n'
            '<h2>2. Klaviyo \u2014 Best for E-commerce</h2>\n'
            '<p>Klaviyo AI predicts customer lifetime value, churn risk, and purchase likelihood. Generates personalized product recommendations. AI Flow Builder creates multi-step automations. E-commerce stores report 2-3x higher revenue per email.</p>\n'
            '<h2>3. ConvertKit \u2014 Best for Creators</h2>\n'
            '<p>ConvertKit AI helps creators write email sequences and newsletters. AI Broadcast Writer drafts emails from bullet points, matching your voice. Ideal for solo creators and small teams.</p>\n'
            '<p><a href="/go/?to=convertkit">Try ConvertKit \u2192</a></p>\n'
            '<h2>4. ActiveCampaign \u2014 Best for Automation</h2>\n'
            '<p>ActiveCampaign AI Predictive Sending determines ideal email frequency. Machine learning scores leads by purchase intent. AI split testing finds winning subject lines and CTAs.</p>\n'
            '<h2>5. Brevo \u2014 Best Value</h2>\n'
            '<p>Brevo AI sends transactional and marketing emails through one platform. AI Subject Line Generator produces high-performing options. Pricing scales affordably for growing businesses.</p>\n'
            '<h2>Final Verdict</h2>\n'
            '<p>Mailchimp for simplicity. Klaviyo for e-commerce. ConvertKit for creators. ActiveCampaign for automation. Brevo for budget scaling.</p>\n'
            '<p style="margin-top:2rem"><a href="https://ko-fi.com/kangjian" target="_blank" rel="noopener">\u2615 Support this guide on Ko-fi</a></p>\n'
        )
    },
    {
        "filename": "ai-translation-tools-2026.html",
        "title": "Best AI Translation Tools 2026",
        "desc": "The best AI translation tools and platforms in 2026. Compare DeepL, Google Translate, Claude and more for accuracy and context.",
        "article_text": (
            '<h1>Best AI Translation Tools 2026: Accuracy and Speed Compared</h1>\n'
            '<p class="article-meta">Jun 13, 2026 \xb7 5 min read</p>\n'
            '<p>AI translation has reached impressive quality. Modern tools handle nuance, context, and cultural adaptation \u2014 not just word-for-word translation. Here are the best AI translation tools in 2026.</p>\n'
            '<h2>1. DeepL \u2014 Best Overall Accuracy</h2>\n'
            '<p>DeepL remains the gold standard for European languages. Its neural network produces translations that read naturally. DeepL Write refines translated text for style and tone. DeepL Pro supports unlimited API calls.</p>\n'
            '<p><a href="/go/?to=deepl">Try DeepL \u2192</a></p>\n'
            '<h2>2. Google Translate \u2014 Best Language Coverage</h2>\n'
            '<p>Google Translate supports 130+ languages. Lens integration translates text from images. Conversation mode handles bilingual dialogues. Free and ubiquitous.</p>\n'
            '<h2>3. Claude \u2014 Best for Context and Tone</h2>\n'
            '<p>Claude excels at translating marketing copy, literary works, and business communications. Large context window ensures consistent terminology. Adapts translations for specific audiences.</p>\n'
            '<p><a href="/go/?to=claude">Try Claude \u2192</a></p>\n'
            '<h2>4. ChatGPT \u2014 Best All-in-One Translation</h2>\n'
            '<p>ChatGPT handles translation with strong nuance. Adapts idioms and cultural references. Supports 95+ languages. GPT-4o offers best quality with faster response.</p>\n'
            '<h2>5. Wordly \u2014 Best for Live Events</h2>\n'
            '<p>Wordly provides AI real-time interpretation for meetings and conferences. Translates speech into text in 40+ languages. Perfect for global teams.</p>\n'
            '<h2>Choosing the Right Tool</h2>\n'
            '<p>DeepL for professional translations. Google Translate for coverage. Claude for contextual content. ChatGPT for all-purpose. Wordly for live events.</p>\n'
            '<p style="margin-top:2rem"><a href="https://ko-fi.com/kangjian" target="_blank" rel="noopener">\u2615 Support this guide on Ko-fi</a></p>\n'
        )
    },
    {
        "filename": "ai-meeting-assistant-2026.html",
        "title": "Best AI Meeting Note-Takers and Assistants 2026",
        "desc": "Best AI meeting assistants for note-taking, transcription, and action items. Compare Otter, Fireflies, Fathom and more in 2026.",
        "article_text": (
            '<h1>Best AI Meeting Assistants and Note-Takers 2026</h1>\n'
            '<p class="article-meta">Jun 13, 2026 \xb7 5 min read</p>\n'
            '<p>AI meeting assistants have transformed from simple transcription into intelligent participants that summarize, extract action items, and integrate with your workflow.</p>\n'
            '<h2>1. Otter.ai \u2014 Best for Real-Time Transcription</h2>\n'
            '<p>Otter provides real-time transcription with speaker identification. AI generates summaries, action items, and highlights. Otter Chat lets you ask about past meetings. Integrates with Zoom, Google Meet, and Teams.</p>\n'
            '<p><a href="/go/?to=otter">Try Otter \u2192</a></p>\n'
            '<h2>2. Fireflies \u2014 Best for CRM Integration</h2>\n'
            '<p>Fireflies connects with 40+ apps including Salesforce and Notion. AI generates topic trackers and sentiment analysis. Search across past meetings. Best for sales teams.</p>\n'
            '<h2>3. Fathom \u2014 Best Free Tier</h2>\n'
            '<p>Fathom offers unlimited transcription and summaries. AI identifies decisions, action items, and questions. Share highlight reels with teammates. Clean interface, excellent value.</p>\n'
            '<p><a href="/go/?to=fathom">Try Fathom \u2192</a></p>\n'
            '<h2>4. Grain \u2014 Best for Video Highlights</h2>\n'
            '<p>Grain captures and shares video clips from meetings. AI identifies customer quotes and creates shareable reels. Automated scorecards for sales calls.</p>\n'
            '<h2>5. Sembly \u2014 Best for Async Teams</h2>\n'
            '<p>Sembly creates a searchable knowledge base from meetings. Smart Tasks extracts and assigns action items. Perfect for remote teams across time zones.</p>\n'
            '<h2>Which One to Pick</h2>\n'
            '<p>Otter for live note-taking. Fireflies for CRM integration. Fathom for best free experience. Grain for video highlights. Sembly for async teams.</p>\n'
            '<p style="margin-top:2rem"><a href="https://ko-fi.com/kangjian" target="_blank" rel="noopener">\u2615 Support this guide on Ko-fi</a></p>\n'
        )
    },
    {
        "filename": "ai-cover-letter-tools-2026.html",
        "title": "Best AI Cover Letter and Job Search Tools 2026",
        "desc": "Best AI tools for cover letters, resumes, and job search in 2026. Land more interviews with AI-powered application tools.",
        "article_text": (
            '<h1>Best AI Cover Letter and Job Search Tools 2026</h1>\n'
            '<p class="article-meta">Jun 13, 2026 \xb7 5 min read</p>\n'
            '<p>Applying for jobs is a numbers game \u2014 and AI tools give you the edge. From personalized cover letters to resume optimization and interview prep, here are the best AI tools for job seekers.</p>\n'
            '<h2>1. Kickresume \u2014 Best All-in-One Job Tool</h2>\n'
            '<p>Kickresume combines AI cover letter writing, resume building, and LinkedIn optimization. AI Cover Letter Generator creates tailored letters from job descriptions. Templates are ATS-friendly.</p>\n'
            '<p><a href="/go/?to=kickresume">Try Kickresume \u2192</a></p>\n'
            '<h2>2. Teal \u2014 Best Job Search CRM</h2>\n'
            '<p>Teal AI tracks applications, identifies skill gaps, and suggests resume improvements. AI Resume Builder optimizes bullet points for ATS parsing. Chrome extension auto-fills forms.</p>\n'
            '<h2>3. ChatGPT \u2014 Best for Customization</h2>\n'
            '<p>ChatGPT crafts personalized cover letters. Feed it the job description and your resume. Adapts to any format or style. Pro tip: ask it to write in your voice.</p>\n'
            '<p><a href="/go/?to=chatgpt">Try ChatGPT \u2192</a></p>\n'
            '<h2>4. Jobscan \u2014 Best for ATS Optimization</h2>\n'
            '<p>Jobscan AI compares your resume against job descriptions. Identifies missing keywords and predicts ATS pass rate. Essential for competitive industries.</p>\n'
            '<h2>5. Interview Warmup by Google \u2014 Best Practice</h2>\n'
            '<p>Google free AI tool asks interview questions and analyzes spoken responses. Identifies filler words and areas to improve. Excellent way to practice out loud.</p>\n'
            '<h2>Strategy for 2026</h2>\n'
            '<p>Use Kickresume or ChatGPT for fast cover letters. Teal to manage your job search. Jobscan for ATS optimization. Practice with Google Warmup.</p>\n'
            '<p style="margin-top:2rem"><a href="https://ko-fi.com/kangjian" target="_blank" rel="noopener">\u2615 Support this guide on Ko-fi</a></p>\n'
        )
    },
    {
        "filename": "ai-learning-tools-2026.html",
        "title": "Best AI Learning and Tutoring Platforms 2026",
        "desc": "The best AI learning and tutoring platforms in 2026. From language learning to coding, AI tutors make education faster and more personalized.",
        "article_text": (
            '<h1>Best AI Learning and Tutoring Platforms 2026</h1>\n'
            '<p class="article-meta">Jun 13, 2026 \xb7 5 min read</p>\n'
            '<p>AI has transformed education from one-size-fits-all to personalized tutoring at scale. AI tutors adapt to your pace and style. Here are the best AI learning platforms in 2026.</p>\n'
            '<h2>1. Khan Academy Khanmigo \u2014 Best Overall Tutor</h2>\n'
            '<p>Khan Academy AI tutor Khanmigo uses the Socratic method. Tracks knowledge gaps and adapts explanations. Built on world-class content library. Best all-around learning companion.</p>\n'
            '<p><a href="/go/?to=khanmigo">Try Khanmigo \u2192</a></p>\n'
            '<h2>2. Duolingo Max \u2014 Best Language Learning</h2>\n'
            '<p>Duolingo Max uses GPT-4 for Roleplay conversations and Explain My Answer feedback. AI adapts lesson difficulty based on retention. Gamification keeps you consistent.</p>\n'
            '<h2>3. Brilliant \u2014 Best for STEM Learning</h2>\n'
            '<p>Brilliant uses AI to personalize interactive lessons in math and science. Active problem-solving leads to deeper understanding. Perfect for building technical intuition.</p>\n'
            '<p><a href="/go/?to=brilliant">Try Brilliant \u2192</a></p>\n'
            '<h2>4. GitHub Copilot \u2014 Best Coding Tutor</h2>\n'
            '<p>Copilot is an interactive coding tutor. Suggests implementations and explains reasoning. Use Copilot Chat to ask why or how. Real-time mentorship as you build.</p>\n'
            '<h2>5. NotebookLM \u2014 Best Research Tool</h2>\n'
            '<p>Google NotebookLM lets you upload materials and ask questions based only on your sources. Generates study guides, FAQs, and Audio Overviews. Ideal for self-directed learners.</p>\n'
            '<h2>Pick Your Learning Style</h2>\n'
            '<p>Khanmigo for structured subjects. Duolingo Max for languages. Brilliant for STEM. Copilot for coding. NotebookLM for research.</p>\n'
            '<p style="margin-top:2rem"><a href="https://ko-fi.com/kangjian" target="_blank" rel="noopener">\u2615 Support this guide on Ko-fi</a></p>\n'
        )
    },
    {
        "filename": "ai-music-production-2026.html",
        "title": "Best AI Music Production and Beat Makers 2026",
        "desc": "The best AI music production tools and beat makers in 2026. From generating melodies to mastering tracks, AI is changing music creation.",
        "article_text": (
            '<h1>Best AI Music Production and Beat Makers 2026</h1>\n'
            '<p class="article-meta">Jun 13, 2026 \xb7 5 min read</p>\n'
            '<p>AI music tools have matured from novelty to legitimate production instruments. Whether you need inspiration or background tracks, AI can generate, arrange, and master music.</p>\n'
            '<h2>1. Suno \u2014 Best Text-to-Music Generation</h2>\n'
            '<p>Suno creates full songs from text including vocals and instrumentation. Version 4 delivers radio-quality audio with verse-chorus structure. Specify genre, mood, tempo, and instruments.</p>\n'
            '<p><a href="/go/?to=suno">Try Suno \u2192</a></p>\n'
            '<h2>2. Udio \u2014 Best for Genre-Specific Production</h2>\n'
            '<p>Udio excels at genre-specific music. Its extension feature generates full song structures from short clips. Exceptional audio quality for AI-generated music.</p>\n'
            '<h2>3. LANDR \u2014 Best Mastering and Distribution</h2>\n'
            '<p>LANDR AI mastering analyzes genre, dynamics, and frequency balance. Offers AI sample packs, stem separation, and distribution. Replaces an entire post-production team.</p>\n'
            '<p><a href="/go/?to=landr">Try LANDR \u2192</a></p>\n'
            '<h2>4. AIVA \u2014 Best for Cinematic Composition</h2>\n'
            '<p>AIVA specializes in orchestral music. Its AI understands music theory and is trained on classical works. Perfect for game developers and video producers.</p>\n'
            '<h2>5. Mubert \u2014 Best for Streaming Background Music</h2>\n'
            '<p>Mubert generates endless royalty-free electronic music. Creates real-time compositions based on mood. No copyright concerns for content creators.</p>\n'
            '<h2>Choosing Your Music AI</h2>\n'
            '<p>Suno for full songs. Udio for genre production. LANDR for mastering. AIVA for cinematic. Mubert for background music.</p>\n'
            '<p style="margin-top:2rem"><a href="https://ko-fi.com/kangjian" target="_blank" rel="noopener">\u2615 Support this guide on Ko-fi</a></p>\n'
        )
    },
    {
        "filename": "ai-seo-tools-2026.html",
        "title": "Best AI SEO Tools for Content Creators 2026",
        "desc": "The best AI SEO tools for content creators and marketers in 2026. Rank higher with AI-powered keyword research, content optimization, and analytics.",
        "article_text": (
            '<h1>Best AI SEO Tools for Content Creators 2026</h1>\n'
            '<p class="article-meta">Jun 13, 2026 \xb7 5 min read</p>\n'
            '<p>SEO has become increasingly AI-driven. Modern tools analyze search intent, predict ranking potential, and optimize content using machine learning.</p>\n'
            '<h2>1. Surfer SEO \u2014 Best Content Optimization</h2>\n'
            '<p>Surfer SEO analyzes top-ranking pages and creates data-driven content briefs. AI recommends word count, headings, and keywords. Real-time editor scores against competitors. Integrates with WordPress.</p>\n'
            '<p><a href="/go/?to=surferseo">Try Surfer SEO \u2192</a></p>\n'
            '<h2>2. Ahrefs \u2014 Best All-in-One SEO Suite</h2>\n'
            '<p>Ahrefs AI surfaces keyword opportunities and analyzes backlinks. Content Gap analysis reveals competitor keywords. AI Site Audit finds technical issues before they impact rankings.</p>\n'
            '<h2>3. Semrush \u2014 Best for Competitive Analysis</h2>\n'
            '<p>Semrush AI includes Keyword Magic Tool and SEO Content Template. AI Writing Assistant crafts search-optimized copy. Position Tracking monitors daily ranking changes.</p>\n'
            '<p><a href="/go/?to=semrush">Try Semrush \u2192</a></p>\n'
            '<h2>4. Frase \u2014 Best for AI Content Briefs</h2>\n'
            '<p>Frase AI analyzes SERP results and generates comprehensive briefs. Covers questions to answer and optimal structure. Scores drafts against top-ranking pages.</p>\n'
            '<h2>5. NeuronWriter \u2014 Best for Entity-Based SEO</h2>\n'
            '<p>NeuronWriter focuses on entity-based SEO. Analyzes Google NLP entities from top pages. Visual entity map shows concepts to cover for topical authority.</p>\n'
            '<h2>SEO Stack for 2026</h2>\n'
            '<p>Surfer SEO or Frase for optimization. Ahrefs for keyword research. Semrush for competitive intelligence. NeuronWriter for entity authority.</p>\n'
            '<p style="margin-top:2rem"><a href="https://ko-fi.com/kangjian" target="_blank" rel="noopener">\u2615 Support this guide on Ko-fi</a></p>\n'
        )
    }
]

def make_html(a):
    fn = a["filename"]
    t = a["title"]
    d = a["desc"]
    at = a["article_text"]
    full_title = t + " - CreatorAI Tools"
    site_url = "https://creatordir-tools.vercel.app/articles/" + fn

    h = '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
    h += '<!-- Microsoft Clarity -->\n'
    h += '<script type="text/javascript">\n'
    h += '    (function(c,l,a,r,i,t,y){\n'
    h += '        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};\n'
    h += '        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;\n'
    h += '        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);\n'
    h += '    })(window, document, "clarity", "script", "x5gn56sdfi");\n'
    h += '</script>\n'
    h += '<meta name="msvalidate.01" content="12DE03330024456C4B6D9FF9E4B9C31C">\n'
    h += '<link rel="icon" href="../favicon.svg" type="image/svg+xml">\n'
    h += '<meta charset="UTF-8">\n'
    h += '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    h += '<meta property="og:title" content="' + full_title + '">\n'
    h += '<meta property="og:description" content="' + d + '">\n'
    h += '<meta property="og:type" content="article">\n'
    h += '<meta property="og:url" content="' + site_url + '">\n'
    h += '<meta property="og:image" content="https://creatordir-tools.vercel.app/images/og-default.svg">\n'
    h += '<meta property="og:site_name" content="CreatorAI Tools">\n'
    h += '<meta name="twitter:card" content="summary_large_image">\n'
    h += '<meta name="twitter:title" content="' + full_title + '">\n'
    h += '<meta name="twitter:description" content="' + d + '">\n'
    h += '<title>' + full_title + '</title>\n'
    h += '<meta name="description" content="' + d + '">\n'
    h += '<link rel="canonical" href="' + site_url + '">\n'
    h += '<meta name="robots" content="index, follow">\n'
    h += '<link rel="stylesheet" href="../css/style.css">\n'
    h += '</head>\n<body>\n'
    
    # Header
    h += '<header class="site-header">\n  <div class="container">\n'
    h += '    <a href="../" class="logo">\\u26a1 CreatorAI</a>\n'
    h += '    <button class="hamburger" onclick="this.classList.toggle('active');document.querySelector('.nav-links').classList.toggle('open')">\n'
    h += '      <span></span><span></span><span></span>\n    </button>\n    <nav>\n'
    h += '      <ul class="nav-links">\n'
    h += '        <li><a href="../">Home</a></li>\n'
    h += '        <li><a href="../tools/">Tools</a></li>\n'
    h += '        <li><a href="../articles/" class="active">Guides</a></li>\n'
    h += '        <li><a href="../resources/">Resources</a></li>\n'
    h += '        <li><a href="../compare/">Compare</a></li>\n'
    h += '        <li><a href="../extensions.html">Extensions</a></li>\n'
    h += '        <li><a href="../trending.html">Trending</a></li>\n'
    h += '        <li><a href="../free-ai-tools.html">\\U0001f4b0 Free</a></li>\n'
    h += '        <li><a href="../news.html">News</a></li>\n'
    h += '        <li><a href="../about.html">About</a></li>\n'
    h += '      </ul>\n    </nav>\n  </div>\n</header>\n'
    
    # Main content
    h += '<main>\n  <div class="container">\n'
    h += '    <nav class="breadcrumb"><a href="../">Home</a> / <a href="./">Guides</a> / <span>' + t + '</span></nav>\n'
    h += '  </div>\n'
    h += '  <article class="article-content">\n'
    h += at + '\n'
    h += '  </article>\n</main>\n'
    
    # Footer
    h += '<footer class="site-footer">\n  <div class="container">\n'
    h += '    <p><strong>CreatorAI Tools</strong> \\u2014 AI tools for content creators worldwide</p>\n'
    h += '    <p style="font-size:0.8rem;color:#64748b;margin-top:0.5rem">Disclosure: Some links on this site are affiliate links. We may earn a commission at no extra cost to you.</p>\n'
    h += '    <p>&copy; 2026 CreatorAI &middot; <a href="../privacy.html">Privacy</a> &middot; <a href="../terms.html">Terms</a> &middot; <a href="../sitemap.xml">Sitemap</a></p>\n'
    h += '  </div>\n</footer>\n'
    
    h += '<script src="../js/main.js"></script>\n'
    h += '<script src="../js/smart-bar.js"></script>\n'
    h += '<script src="../js/affiliate-widget.js"></script>\n'
    h += '<script src="../js/social-share.js"></script>\n'
    h += '</body>\n</html>'
    return h

for a in articles:
    path = os.path.join(articles_dir, a["filename"])
    with open(path, "w", encoding="utf-8") as f:
        f.write(make_html(a))
    size = os.path.getsize(path)
    print(f"Created: {a['filename']} ({size} bytes)")

print("\nAll 8 articles created successfully!")
