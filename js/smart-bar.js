// ===== Smart Bar v2.0 — Full Feature Widget =====
(function() {
  var path = window.location.pathname;
  var isArticle = path.includes("/articles/") && !path.includes("index");

  // ---- Detect page context ----
  var currentCat = "all";
  if (path.includes("writing")) currentCat = "writing";
  else if (path.includes("image")) currentCat = "image";
  else if (path.includes("video")) currentCat = "video";
  else if (path.includes("audio")) currentCat = "audio";
  else if (path.includes("marketing")) currentCat = "marketing";
  else if (path.includes("code")) currentCat = "code";

  // ---- Link Database ----
  var DB = {
    tools: [
      {n:"ChatGPT",u:"https://chat.openai.com",d:"AI writing assistant",c:"writing"},
      {n:"Claude",u:"https://claude.ai",d:"AI for long-form content",c:"writing"},
      {n:"Midjourney",u:"https://www.midjourney.com",d:"AI image gen V7",c:"image"},
      {n:"Canva AI",u:"https://www.canva.com",d:"AI-powered design",c:"image"},
      {n:"CapCut",u:"https://www.capcut.com",d:"Free AI video editor",c:"video"},
      {n:"Runway",u:"https://runwayml.com",d:"AI video generation",c:"video"},
      {n:"ElevenLabs",u:"https://elevenlabs.io",d:"AI voiceover & cloning",c:"audio"},
      {n:"Suno",u:"https://suno.com",d:"AI music generation",c:"audio"},
      {n:"Descript",u:"https://www.descript.com",d:"AI audio/video editor",c:"audio"},
      {n:"Search Console",u:"https://search.google.com/search-console",d:"Free SEO tool",c:"marketing"},
      {n:"Google Analytics",u:"https://analytics.google.com",d:"Website analytics",c:"marketing"},
      {n:"Mailchimp",u:"https://mailchimp.com",d:"Email marketing",c:"marketing"},
      {n:"GitHub Copilot",u:"https://github.com/features/copilot",d:"AI code assistant",c:"code"},
      {n:"Codex CLI",u:"https://openai.com/index/codex-cli/",d:"Open-source AI coding agent",c:"code"},
      {n:"Cursor",u:"https://www.cursor.com",d:"AI-native code editor",c:"code"},
    ],
    downloads: [
      {n:"Stable Diffusion WebUI",u:"https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases",d:"Local AI image gen",c:"image"},
      {n:"OpenAI Whisper",u:"https://github.com/openai/whisper/releases",d:"Free transcription",c:"audio"},
      {n:"CapCut Desktop",u:"https://www.capcut.com/download",d:"AI video editor",c:"video"},
      {n:"Descript",u:"https://www.descript.com/download",d:"AI audio/video editor",c:"audio"},
      {n:"Copilot Extension",u:"https://marketplace.visualstudio.com/items?itemName=GitHub.copilot",d:"VS Code AI plugin",c:"code"},
      {n:"Codex CLI",u:"https://github.com/openai/codex-cli",d:"Terminal AI agent",c:"code"},
      {n:"Cursor",u:"https://www.cursor.com/downloads",d:"AI-native code editor",c:"code"},
      {n:"OBS Studio",u:"https://obsproject.com/download",d:"Free screen recording",c:"video"},
      {n:"Audacity",u:"https://www.audacityteam.org/download",d:"Free audio editor",c:"audio"},
      {n:"Blender",u:"https://www.blender.org/download",d:"3D creation suite",c:"design"},
    ],
    site: [
      {n:"Home",u:"/",d:"AI tools for content creators"},
      {n:"Writing Tools",u:"/tools/writing-ai.html",d:"ChatGPT, Claude, Jasper"},
      {n:"Image Tools",u:"/tools/image-ai.html",d:"Midjourney, Canva"},
      {n:"Video Tools",u:"/tools/video-ai.html",d:"CapCut, Runway"},
      {n:"Audio Tools",u:"/tools/audio-ai.html",d:"ElevenLabs, Suno"},
      {n:"Marketing Tools",u:"/tools/marketing-ai.html",d:"SEO, Analytics"},
      {n:"Code Tools",u:"/tools/code-ai.html",d:"Copilot, Cursor"},
      {n:"Comparisons",u:"/compare/",d:"Tool side-by-side"},
      {n:"Resources",u:"/resources/",d:"Free assets & GitHub"},
      {n:"Guides",u:"/articles/",d:"Tutorials and guides"},
    ],
    faq: [
      {q:"How do I copy a link?",a:'Click the "Copy" button next to any link, or use the copy button below.'},
      {q:"How do I switch themes?",a:'Click the theme icon (sun/moon) in the Smart Bar toolbar.'},
      {q:"Where can I find downloads?",a:'Open Smart Bar \u2192 Downloads tab for all free software.'},
      {q:"Is this site free?",a:"Yes. All resources and guides are completely free."},
      {q:"How to search?",a:'Smart Bar \u2192 Search tab. Type anything to find tools and pages.'},
    ]
  };

  // ---- Toast notification ----
  function showToast(msg) {
    var t = document.createElement("div");
    t.textContent = msg;
    t.style.cssText = "position:fixed;bottom:90px;right:24px;background:#1e293b;color:white;padding:10px 20px;border-radius:10px;font-size:13px;border:1px solid #334155;box-shadow:0 4px 20px rgba(0,0,0,0.4);z-index:10000;animation:fadeIn 0.2s;";
    document.body.appendChild(t);
    setTimeout(function(){ t.style.opacity="0";t.style.transition="opacity 0.3s";setTimeout(function(){t.remove();},300); }, 2000);
  }

  // ---- Track visit ----
  try {
    var visits = JSON.parse(localStorage.getItem("sb_visits") || "[]");
    var here = {p:path,t:document.title.replace(" - CreatorAI Tools","").replace(" | CreatorAI Tools",""),ts:Date.now()};
    visits = visits.filter(function(v){ return v.p !== here.p; });
    visits.unshift(here);
    if (visits.length > 10) visits = visits.slice(0,10);
    localStorage.setItem("sb_visits", JSON.stringify(visits));
  } catch(e) {}

  // ---- Theme toggle ----
  var theme = localStorage.getItem("sb_theme") || "dark";
  function applyTheme(t) {
    theme = t;
    document.documentElement.setAttribute("data-theme", t);
    localStorage.setItem("sb_theme", t);
  }
  applyTheme(theme);

  // ---- Build Widget ----
  var w = document.createElement("div");
  w.id = "smart-bar";
  w.style.cssText = "position:fixed;bottom:24px;right:24px;z-index:9999;font-family:system-ui,sans-serif;";

  // ---- Reading progress bar (articles only) ----
  if (isArticle) {
    var prog = document.createElement("div");
    prog.id = "sb-progress";
    prog.style.cssText = "position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,#8b5cf6,#6366f1);z-index:9998;width:0%;transition:width 0.1s;";
    document.body.appendChild(prog);
    window.addEventListener("scroll", function(){
      var h = document.documentElement.scrollHeight - window.innerHeight;
      prog.style.width = Math.min(100, (window.scrollY / h) * 100) + "%";
    });
  }

  // ---- FAB ----
  var fab = document.createElement("button");
  fab.id = "sb-fab";
  fab.textContent = "\u26a1";
  fab.title = "Quick Access";
  fab.style.cssText = "width:56px;height:56px;border-radius:50%;border:none;background:linear-gradient(135deg,#8b5cf6,#6366f1);color:white;font-size:24px;cursor:pointer;box-shadow:0 4px 20px rgba(139,92,246,0.4);transition:transform 0.2s,box-shadow 0.2s;display:flex;align-items:center;justify-content:center;";
  fab.onmouseenter = function(){this.style.transform="scale(1.1)";this.style.boxShadow="0 6px 25px rgba(139,92,246,0.6)";};
  fab.onmouseleave = function(){this.style.transform="scale(1)";this.style.boxShadow="0 4px 20px rgba(139,92,246,0.4)";};

  // ---- Toolbar (always visible above panel) ----
  var toolbar = document.createElement("div");
  toolbar.style.cssText = "display:flex;gap:4px;margin-bottom:6px;justify-content:flex-end;";

  function makeToolBtn(html, title, fn) {
    var b = document.createElement("button");
    b.innerHTML = html;
    b.title = title;
    b.style.cssText = "width:36px;height:36px;border-radius:50%;border:none;background:#1e293b;color:#94a3b8;font-size:14px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.2s;box-shadow:0 2px 8px rgba(0,0,0,0.3);";
    b.onmouseenter = function(){this.style.background="#334155";this.style.color="white";};
    b.onmouseleave = function(){this.style.background="#1e293b";this.style.color="#94a3b8";};
    b.onclick = fn;
    return b;
  }

  // Theme toggle button
  var themeBtn = makeToolBtn("\u2600\ufe0f", "Toggle theme", function(){
    var t = theme === "dark" ? "light" : "dark";
    applyTheme(t);
    this.innerHTML = t === "dark" ? "\u2600\ufe0f" : "\U0001f319";
    showToast(t === "dark" ? "Dark mode" : "Light mode");
  });

  // Copy link button
  var copyBtn = makeToolBtn("\U0001f4cb", "Copy page link", function(){
    navigator.clipboard.writeText(window.location.href).then(function(){
      showToast("Link copied!");
    }).catch(function(){
      showToast("Press Ctrl+C to copy");
    });
  });

  // Share button
  var shareBtn = makeToolBtn("\U0001f517", "Share this page", function(){
    if (navigator.share) {
      navigator.share({title:document.title,url:window.location.href}).catch(function(){});
    } else {
      navigator.clipboard.writeText(window.location.href).then(function(){ showToast("Link copied \u2014 share it!"); });
    }
  });

  // Scroll to top
  var topBtn = makeToolBtn("\u2b06\ufe0f", "Scroll to top", function(){
    window.scrollTo({top:0,behavior:"smooth"});
  });

  toolbar.appendChild(themeBtn);
  toolbar.appendChild(copyBtn);
  toolbar.appendChild(shareBtn);
  toolbar.appendChild(topBtn);

  // ---- Panel ----
  var panel = document.createElement("div");
  panel.id = "sb-panel";
  panel.style.cssText = "display:none;position:absolute;bottom:70px;right:0;width:400px;max-height:560px;background:#1e293b;border:1px solid #334155;border-radius:16px;box-shadow:0 8px 40px rgba(0,0,0,0.5);overflow:hidden;padding-bottom:4px;";

  // Tabs
  var tabs = ["Links", "Search", "Downloads", "Help"];
  panel.innerHTML = '<div style="display:flex;background:#0f172a;border-bottom:1px solid #334155;">' +
    tabs.map(function(t,i){return '<button class="sb-tab" data-tab="'+i+'" style="flex:1;padding:10px 6px;border:none;background:'+(i===0?'#1e293b':'transparent')+';color:'+(i===0?'#8b5cf6':'#94a3b8')+';font-size:12px;font-weight:600;cursor:pointer;transition:all 0.2s;">'+t+'</button>';}).join("") +
    '</div>' +
    '<div style="padding:4px 12px;">' + toolbar.outerHTML + '</div>' +
    '<div id="sb-body" style="overflow-y:auto;max-height:430px;padding:8px;"></div>';

  // Fix toolbar buttons after insert
  var body = panel.querySelector("#sb-body");

  // Tab switching
  panel.addEventListener("click", function(e){
    var tab = e.target.closest(".sb-tab");
    if (!tab) return;
    var idx = parseInt(tab.dataset.tab);
    panel.querySelectorAll(".sb-tab").forEach(function(t,i){
      t.style.background = i===idx ? "#1e293b" : "transparent";
      t.style.color = i===idx ? "#8b5cf6" : "#94a3b8";
    });
    renderTab(idx);
  });

    // Dynamic toolbar
  var tb = document.createElement("div");
  tb.style.cssText = "display:flex;gap:4px;padding:4px 12px;justify-content:flex-end;";
  function tbBtn(h,t,fn){var b=document.createElement("button");b.innerHTML=h;b.title=t;b.style.cssText="width:34px;height:34px;border-radius:50%;border:none;background:#1e293b;color:#94a3b8;font-size:13px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.2s;";b.onmouseenter=function(){this.style.background="#334155";this.style.color="white";};b.onmouseleave=function(){this.style.background="#1e293b";this.style.color="#94a3b8";};b.onclick=fn;return b;}
  tb.appendChild(tbBtn("\u2600\ufe0f","Toggle theme",function(){var t=theme==="dark"?"light":"dark";applyTheme(t);showToast(t==="dark"?"Dark mode":"Light mode");}));
  tb.appendChild(tbBtn("\U0001f4cb","Copy link",function(){navigator.clipboard.writeText(window.location.href).then(function(){showToast("Link copied!");});}));
  tb.appendChild(tbBtn("\U0001f517","Share",function(){if(navigator.share)navigator.share({title:document.title,url:window.location.href}).catch(function(){});else navigator.clipboard.writeText(window.location.href).then(function(){showToast("Link copied!");});}));
  tb.appendChild(tbBtn("\u2b06\ufe0f","Top",function(){window.scrollTo({top:0,behavior:"smooth"});}));
  panel.insertBefore(tb, body);
  function renderTab(idx) {
    if (idx === 0) renderLinks();
    else if (idx === 1) renderSearch();
    else if (idx === 2) renderDownloads();
    else if (idx === 3) renderHelp();
  }

  // ===== TAB 0: Links =====
  function renderLinks() {
    var html = "";

    // Recently visited
    try {
      var recent = JSON.parse(localStorage.getItem("sb_visits") || "[]").slice(0,4);
      if (recent.length > 1) {
        html += '<div style="padding:8px 12px 4px;font-size:11px;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;">\U0001f552 Recent</div>';
        recent.forEach(function(v){
          html += '<a href="'+v.p+'" style="display:flex;align-items:center;gap:8px;padding:7px 12px;border-radius:8px;text-decoration:none;color:#e2e8f0;font-size:13px;transition:background 0.15s;" onmouseenter="this.style.background=\'#334155\'" onmouseleave="this.style.background=\'transparent\'">' +
            '\U0001f4cc <span>'+v.t.substring(0,40)+'</span></a>';
        });
      }
    } catch(e) {}

    // Context tools
    var relevant = DB.tools.filter(function(t){ return t.c === currentCat || currentCat === "all"; });
    if (relevant.length === 0) relevant = DB.tools.slice(0,6);
    html += '<div style="padding:8px 12px 4px;margin-top:4px;font-size:11px;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;">\U0001f9f0 Tools</div>';
    relevant.slice(0,6).forEach(function(t){
      html += '<div style="display:flex;align-items:center;gap:6px;padding:6px 12px;border-radius:8px;" onmouseenter="this.style.background=\'#334155\'" onmouseleave="this.style.background=\'transparent\'">' +
        '<span style="width:6px;height:6px;border-radius:50%;background:'+catColor(t.c)+';flex-shrink:0;"></span>' +
        '<a href="'+t.u+'" target="_blank" rel="noopener" style="flex:1;text-decoration:none;color:#e2e8f0;font-size:13px;font-weight:500;">'+t.n+'</a>' +
        '<span style="font-size:11px;color:#94a3b8;">'+t.d+'</span>' +
        '<button onclick="navigator.clipboard.writeText(\''+t.u+'\');(function(t){t.textContent=\'\u2713\';setTimeout(function(){t.textContent=\'\U0001f4cb\';},1000);})(this)" style="background:none;border:none;color:#64748b;cursor:pointer;font-size:13px;padding:2px 6px;border-radius:4px;" onmouseenter="this.style.background=\'#475569\'" onmouseleave="this.style.background=\'none\'" title="Copy link">\U0001f4cb</button>' +
        '</div>';
    });

    // Site pages
    html += '<div style="padding:8px 12px 4px;margin-top:4px;font-size:11px;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;">\U0001f310 Site</div>';
    DB.site.forEach(function(p){
      var active = path === p.u || (p.u !== "/" && path.includes(p.u.replace(".html","").replace("/tools/","").replace("/articles/","")) && p.u !== "/");
      html += '<a href="'+p.u+'" style="display:flex;align-items:center;gap:8px;padding:6px 12px;border-radius:8px;text-decoration:none;color:'+(active?'#8b5cf6':'#e2e8f0')+';font-size:13px;transition:background 0.15s;" onmouseenter="this.style.background=\'#334155\'" onmouseleave="this.style.background=\'transparent\'">' +
        (active?'\u25cf ':'') + p.n + '</a>';
    });
    body.innerHTML = html;
  }

  // ===== TAB 1: Search =====
  var searchTimeout = null;
  function renderSearch() {
    body.innerHTML =
      '<div style="padding:8px 12px 4px;">' +
      '<input id="sb-search" type="text" placeholder="Search tools, downloads, pages..." style="width:100%;padding:10px 14px;border:1px solid #334155;border-radius:10px;background:#0f172a;color:white;font-size:14px;outline:none;box-sizing:border-box;" autofocus>' +
      '</div>' +
      '<div id="sb-results" style="padding:0 8px;"></div>';

    var input = document.getElementById("sb-search");
    if (input) {
      setTimeout(function(){input.focus();},100);
      input.addEventListener("input", function(){
        clearTimeout(searchTimeout);
        var q = this.value.toLowerCase().trim();
        searchTimeout = setTimeout(function(){ doSearch(q); }, 120);
      });
    }
  }

  function doSearch(q) {
    var res = document.getElementById("sb-results");
    if (!res) return;
    if (!q) { res.innerHTML = '<div style="padding:20px;text-align:center;color:#475569;font-size:13px;">Type to search all tools and pages</div>'; return; }

    var all = [];
    DB.tools.forEach(function(t){ all.push({n:t.n,d:t.d,u:t.u,c:t.c,t:"Tool"}); });
    DB.downloads.forEach(function(d){ all.push({n:d.n,d:d.d,u:d.u,c:d.c,t:"Download"}); });
    DB.site.forEach(function(s){ all.push({n:s.n,d:s.d,u:s.u,t:"Page"}); });

    var results = all.filter(function(item){
      return item.n.toLowerCase().includes(q) || (item.d && item.d.toLowerCase().includes(q));
    }).slice(0,10);

    if (results.length === 0) {
      res.innerHTML = '<div style="padding:20px;text-align:center;color:#475569;font-size:13px;">No results \u2014 try a different word</div>';
      return;
    }

    var html = "";
    results.forEach(function(r){
      var typeColor = r.t === "Tool" ? "#8b5cf6" : r.t === "Download" ? "#10b981" : "#3b82f6";
      html += '<div style="display:flex;align-items:center;gap:6px;padding:7px 10px;border-radius:8px;" onmouseenter="this.style.background=\'#334155\'" onmouseleave="this.style.background=\'transparent\'">' +
        '<span style="width:5px;height:5px;border-radius:50%;background:'+typeColor+';flex-shrink:0;"></span>' +
        '<a href="'+r.u+'" target="_blank" rel="noopener" style="flex:1;text-decoration:none;color:#e2e8f0;min-width:0;">' +
        '<span style="font-size:13px;font-weight:500;">'+hl(r.n,q)+'</span>' +
        '<span style="display:block;font-size:11px;color:#64748b;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">'+hl(r.d,q)+'</span></a>' +
        '<span style="font-size:10px;color:'+typeColor+';background:'+typeColor+'15;padding:2px 8px;border-radius:4px;white-space:nowrap;">'+r.t+'</span>' +
        '</div>';
    });
    res.innerHTML = html;
  }

  function hl(t,q) { if (!q) return t; var i=t.toLowerCase().indexOf(q); return i===-1?t:t.substring(0,i)+'<span style="color:#8b5cf6;font-weight:600;">'+t.substring(i,i+q.length)+'</span>'+t.substring(i+q.length); }

  // ===== TAB 2: Downloads =====
  function renderDownloads() {
    var html = '<div style="padding:8px 12px 4px;font-size:11px;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;">\u2b07 Free Downloads</div>';
    DB.downloads.forEach(function(d){
      html += '<div style="display:flex;align-items:center;gap:6px;padding:7px 12px;border-radius:8px;" onmouseenter="this.style.background=\'#334155\'" onmouseleave="this.style.background=\'transparent\'">' +
        '<span style="width:6px;height:6px;border-radius:50%;background:'+catColor(d.c)+';flex-shrink:0;"></span>' +
        '<a href="'+d.u+'" target="_blank" rel="noopener" style="flex:1;text-decoration:none;color:#e2e8f0;font-size:13px;font-weight:500;">'+d.n+'</a>' +
        '<span style="font-size:11px;color:#94a3b8;">'+d.d+'</span>' +
        '<a href="'+d.u+'" target="_blank" rel="noopener" style="text-decoration:none;font-size:13px;color:#10b981;padding:2px 8px;border-radius:4px;" onmouseenter="this.style.background=\'#10b98120\'" onmouseleave="this.style.background=\'none\'">\u2b07</a>' +
        '</div>';
    });
    body.innerHTML = html;
  }

  // ===== TAB 3: Help =====
  function renderHelp() {
    var html = '<div style="padding:8px 12px;font-size:11px;color:#94a3b8;">Quick help for common questions:</div>';
    DB.faq.forEach(function(f){
      html += '<div style="margin:2px 8px;border:1px solid #334155;border-radius:10px;overflow:hidden;">' +
        '<button onclick="var n=this.nextElementSibling;n.style.display=n.style.display===\'block\'?\'none\':\'block\';this.querySelector(\'span\').textContent=n.style.display===\'block\'?\'\u2212\':\'+\'" style="width:100%;padding:10px 14px;border:none;background:#0f172a;color:#e2e8f0;font-size:13px;text-align:left;cursor:pointer;display:flex;justify-content:space-between;align-items:center;">' +
        '<span>'+f.q+'</span><span style="color:#8b5cf6;font-weight:bold;">+</span></button>' +
        '<div style="display:none;padding:10px 14px;font-size:13px;color:#94a3b8;background:#1e293b;border-top:1px solid #334155;">'+f.a+'</div></div>';
    });
    body.innerHTML = html;
  }

  function catColor(c) {
    var m = {writing:"#6366f1",image:"#ec4899",video:"#10b981",audio:"#06b6d4",marketing:"#f59e0b",code:"#3b82f6",design:"#8b5cf6"};
    return m[c] || "#8b5cf6";
  }

  // ---- Toggle ----
  var open = false;
  fab.addEventListener("click", function(e){
    e.stopPropagation();
    open = !open;
    panel.style.display = open ? "block" : "none";
    if (open) renderTab(0);
  });

  document.addEventListener("click", function(e){
    if (open && !w.contains(e.target)) {
      open = false;
      panel.style.display = "none";
    }
  });

  w.appendChild(fab);
  w.appendChild(panel);
  document.body.appendChild(w);

  // ---- CSS animations ----
  var style = document.createElement("style");
  style.textContent = "@keyframes sbFadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}#sb-panel{animation:sbFadeIn 0.2s ease;}";
  document.head.appendChild(style);
})();


