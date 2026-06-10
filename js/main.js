// Site search data
const searchIndex = [
  { title: "AI Writing & Copy Tools", url: "tools/writing-ai.html", cat: "Tool", keywords: "ChatGPT Claude Jasper DeepSeek writing copy script blog" },
  { title: "AI Image & Cover Design Tools", url: "tools/image-ai.html", cat: "Tool", keywords: "Midjourney Canva DALL-E image design thumbnail cover" },
  { title: "AI Video & Audio Tools", url: "tools/video-ai.html", cat: "Tool", keywords: "CapCut Runway ElevenLabs Suno video editing voiceover music" },
  { title: "I Used ChatGPT for 30 Days", url: "articles/chatgpt-30-days.html", cat: "Guide", keywords: "ChatGPT experiment writing prompts 30 days content" },
  { title: "Essential AI Tools for Creators 2026", url: "articles/essential-ai-tools-creators.html", cat: "Guide", keywords: "essential tools workflow writing design video audio" },
  { title: "The $0 Content Setup: Free AI Video Editing", url: "articles/free-ai-video-editing.html", cat: "Guide", keywords: "free video editing CapCut ElevenLabs Canva zero budget" },
  { title: "AI Voice Clone Experiment", url: "articles/ai-voice-clone-experiment.html", cat: "Guide", keywords: "voice clone ElevenLabs AI voiceover recording" },
  { title: "YouTube Thumbnails with AI", url: "articles/ai-youtube-thumbnail-guide.html", cat: "Guide", keywords: "thumbnail YouTube Canva Midjourney CTR design" },
  { title: "Why Most People Fail at Using AI for Content", url: "articles/why-ai-content-fails.html", cat: "Guide", keywords: "AI content mistakes generic specific angle 70-30" },
  { title: "From 0 to 1000 Subscribers with AI", url: "articles/zero-to-thousand-ai.html", cat: "Guide", keywords: "subscribers grow channel AI tools consistency" },
  { title: "AI Video Script Writers Compared", url: "articles/ai-video-script-benchmark.html", cat: "Guide", keywords: "script writing benchmark ChatGPT Claude DeepSeek comparison" },
  { title: "Faceless YouTube Channels with AI", url: "articles/faceless-youtube-ai.html", cat: "Guide", keywords: "faceless YouTube channel AI voiceover workflow" },
  { title: "AI Script Prompt Template", url: "articles/ai-script-prompt-template.html", cat: "Guide", keywords: "prompt template script writing copy paste formula" },
  { title: "Social Media AI Workflow", url: "articles/social-media-ai-workflow.html", cat: "Guide", keywords: "social media automation workflow repurpose content" },
  { title: "AI Content Detection Truth", url: "articles/ai-content-detection-truth.html", cat: "Guide", keywords: "AI detection quality human readers experiment" },
  { title: "How to Write AI Prompts That Work", url: "articles/ai-prompts-that-work.html", cat: "Guide", keywords: "prompts framework role context format constraints" },
  { title: "Creator Resources", url: "resources/", cat: "Resource", keywords: "resources stock photos music fonts communities plugins" },
  { title: "AI Tool Comparisons", url: "compare/", cat: "Resource", keywords: "compare ChatGPT Claude Midjourney Canva CapCut Runway" },
];

function searchSite(query) {
  const results = document.getElementById("searchResults");
  if (!results) return;

  if (!query || query.length < 1) {
    results.style.display = "none";
    return;
  }

  const q = query.toLowerCase();
  const matches = searchIndex.filter(item => {
    return item.title.toLowerCase().includes(q) ||
           item.keywords.toLowerCase().includes(q) ||
           item.cat.toLowerCase().includes(q);
  }).slice(0, 8);

  if (matches.length === 0) {
    results.innerHTML = "<div style='padding:1rem;color:var(--text-muted);font-size:0.9rem'>No results found</div>";
  } else {
    results.innerHTML = matches.map(m =>
      `<a href="${m.url}"><span class="cat-tag">${m.cat}</span> ${m.title}</a>`
    ).join("");
  }
  results.style.display = "block";
}

// Close search on click outside
document.addEventListener("click", function(e) {
  const wrap = document.getElementById("searchResults");
  if (wrap && !e.target.closest(".search-wrap")) {
    wrap.style.display = "none";
  }
});

// Header scroll effect
const header = document.querySelector(".site-header");
if (header) {
  window.addEventListener("scroll", () => {
    header.classList.toggle("scrolled", window.scrollY > 10);
  });
}
