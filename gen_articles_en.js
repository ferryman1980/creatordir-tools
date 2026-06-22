
const fs2 = require("fs");
const dir = "D:\\项目\\工作区\\工作5\\articles\\";
const sample = fs2.readFileSync(dir + "ai-article-writer-2026.html", "utf-8");
const templateBefore = sample.substring(0, sample.indexOf('<article class="article-content">'));
const templateAfter = sample.substring(sample.indexOf("</article>") + 10);

function createArticle(file, title, desc, h1, body, keywords) {
  const url = "https://creatordir-tools.vercel.app/articles/" + file;
  const ogTitle = title + " - CreatorAI Tools";
  let html = templateBefore
    .replace(/<title>.*?<\/title>/, "<title>" + ogTitle + "<\/title>")
    .replace(/property="og:title" content="[^"]*"/, 'property="og:title" content="' + ogTitle + '"')
    .replace(/property="og:description" content="[^"]*"/, 'property="og:description" content="' + desc + '"')
    .replace(/property="og:url" content="[^"]*"/, 'property="og:url" content="' + url + '"')
    .replace(/name="twitter:title" content="[^"]*"/, 'name="twitter:title" content="' + ogTitle + '"')
    .replace(/name="twitter:description" content="[^"]*"/, 'name="twitter:description" content="' + desc + '"')
    .replace(/name="description" content="[^"]*"/, 'name="description" content="' + desc + '"')
    .replace(/name="keywords" content="[^"]*"/, 'name="keywords" content="' + keywords + '"');
  const article = '\n<article class="article-content">\n<h1>' + h1 + '<\/h1>\n<p class="article-meta">Published: 2026-06-22<\/p>\n' + body + '\n<\/article>\n';
  html += article + templateAfter;
  fs2.writeFileSync(dir + file, html, "utf-8");
  console.log("Created:", file);
}

createArticle("best-ai-video-generators-2026.html","Best AI Video Generators 2026: Top 15 Compared for Creators","Compare the best AI video generators for content creators.","Best AI Video Generators 2026: Complete Comparison","<p>Video content dominates social media. AI video generators make it possible to create professional-looking videos from text prompts.<\/p><h2>Top 5 AI Video Generators<\/h2><h3>1. Runway Gen-3<\/h3><p>Produces cinema-quality video from text prompts. Excels at realistic motion and lighting.<\/p><h3>2. Pika Labs<\/h3><p>Intuitive interface for generating and editing videos with simple text commands.<\/p><h3>3. HeyGen<\/h3><p>AI avatars for talking-head videos. Perfect for educational content and YouTube.<\/p><h3>4. Synthesia<\/h3><p>140+ AI avatars and 120+ languages. Industry leader for training and marketing videos.<\/p><h3>5. Invideo AI<\/h3><p>Converts blog posts into complete video productions with voiceover and music.<\/p><p>Browse our full collection of <a href=\"../tools/\">AI video tools<\/a>.<\/p>","AI video generators, text to video, AI video editing");

createArticle("ai-music-generator-tools-2026.html","AI Music Generator Tools 2026: Create Royalty-Free Music","Discover the best AI music generators for creators.","AI Music Generator Tools 2026","<p>AI music generators allow anyone to create professional-quality, royalty-free music in seconds.<\/p><h2>Top AI Music Generators<\/h2><h3>1. Suno AI<\/h3><p>Creates complete songs with lyrics, melody, and instrumentation.<\/p><h3>2. Udio<\/h3><p>High-fidelity music generation, good at reproducing specific genres.<\/p><h3>3. MusicFX (Google)<\/h3><p>Excellent for background music and ambient tracks. Free to use.<\/p><h3>4. AIVA<\/h3><p>Specializes in classical and orchestral music for filmmakers.<\/p><h3>5. Beatoven.ai<\/h3><p>Creates mood-based background music for videos and podcasts.<\/p><p>Explore more <a href=\"../tools/\">AI music tools<\/a>.<\/p>","AI music generator, royalty free music, AI song creator");

createArticle("ai-productivity-tools-creators-2026.html","Best AI Productivity Tools for Content Creators 2026","Boost your workflow with AI productivity tools.","Best AI Productivity Tools for Content Creators","<p>Content creators juggle many tasks. AI productivity tools automate repetitive work.<\/p><h2>Top AI Productivity Tools<\/h2><h3>1. Notion AI<\/h3><p>Writing assistance, summarization, and project management.<\/p><h3>2. Motion<\/h3><p>Automatically schedules tasks and optimizes daily workflow.<\/p><h3>3. Mem<\/h3><p>AI-powered knowledge management connecting related ideas.<\/p><h3>4. Bardeen<\/h3><p>Automates repetitive browser tasks without coding.<\/p><h3>5. Krisp<\/h3><p>Removes background noise from calls and recordings.<\/p><p>Check our <a href=\"../tools/\">full directory<\/a>.<\/p>","AI productivity tools, content creator workflow");

createArticle("ai-seo-tools-guide-2026.html","AI SEO Tools Guide 2026: Rank Higher with AI","Master SEO with AI-powered tools for 2026.","AI SEO Tools Guide 2026","<p>SEO has been transformed by AI. Modern tools analyze search patterns automatically.<\/p><h2>Best AI SEO Tools<\/h2><h3>1. Semrush<\/h3><p>AI-powered content optimization and real-time SEO scoring.<\/p><h3>2. Surfer SEO<\/h3><p>Data-driven content guidelines based on top-ranking analysis.<\/p><h3>3. Frase.io<\/h3><p>AI topic research and content brief generation.<\/p><h3>4. Clearscope<\/h3><p>Gold standard content optimization.<\/p><h3>5. Neuron Writer<\/h3><p>Affordable NLP-powered content analysis.<\/p><p>Find more <a href=\"../tools/\">AI SEO tools<\/a>.<\/p>","AI SEO tools, SEO optimization, content optimization");

createArticle("ai-social-media-management-2026.html","AI Social Media Management Tools 2026","Manage social media with AI scheduling and analytics.","AI Social Media Management Tools 2026","<p>Managing multiple social accounts is a major time drain. AI tools automate this.<\/p><h2>Top AI Social Media Tools<\/h2><h3>1. Hootsuite<\/h3><p>AI smart scheduling, caption writer, content recommendations.<\/p><h3>2. Buffer<\/h3><p>AI-powered post suggestions and optimal timing.<\/p><h3>3. Later<\/h3><p>Visual planning for Instagram and TikTok.<\/p><h3>4. Vista Social<\/h3><p>All-in-one platform with AI content generation.<\/p><h3>5. ContentStudio<\/h3><p>AI discovers trending content in your niche.<\/p><p>Explore our <a href=\"../tools/\">AI tools directory<\/a>.<\/p>","AI social media management, social media automation");

console.log("Done!");
