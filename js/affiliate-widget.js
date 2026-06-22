// ===== Affiliate Recommendation Widget =====
(function() {
  // Check if we're on an article page
  var path = window.location.pathname;
  if (!path.includes('/articles/')) return;

  var tools = [
    {name:"ChatGPT", url:"/go/?to=chatgpt", desc:"Best all-around AI for writing", icon:"🤖", color:"#10a37f"},
    {name:"Claude", url:"/go/?to=claude", desc:"Best for long-form content", icon:"🟣", color:"#8b5cf6"},
    {name:"Midjourney", url:"/go/?to=midjourney", desc:"Best AI image generation", icon:"🎨", color:"#ff4500"},
    {name:"ElevenLabs", url:"/go/?to=elevenlabs", desc:"Best AI voice cloning", icon:"🎙️", color:"#06b6d4"},
    {name:"Canva", url:"/go/?to=canva", desc:"Best AI design tool", icon:"✨", color:"#6366f1"}
  ];

  // Randomly pick 3
  var shuffled = tools.sort(function(){return 0.5 - Math.random()});
  var picks = shuffled.slice(0, 3);

  var html = '<div style="margin-top:2rem;padding:1.5rem;background:linear-gradient(135deg,#1e1b4b,#0f172a);border:1px solid #312e81;border-radius:12px">';
  html += '<h3 style="margin:0 0 0.75rem 0;color:#e2e8f0;font-size:1.1rem">🔥 Recommended AI Tools</h3>';
  html += '<p style="color:#94a3b8;font-size:0.85rem;margin-bottom:1rem">Try these AI tools trusted by creators worldwide:</p>';
  html += '<div style="display:flex;flex-direction:column;gap:0.5rem">';
  for (var i = 0; i < picks.length; i++) {
    var t = picks[i];
    html += '<a href="' + t.url + '" target="_blank" rel="noopener sponsored" style="display:flex;align-items:center;gap:0.75rem;padding:0.75rem 1rem;background:#1e293b;border:1px solid #334155;border-radius:8px;text-decoration:none;transition:all 0.2s" onmouseover="this.style.borderColor='' + t.color + ''" onmouseout="this.style.borderColor='#334155'">';
    html += '<span style="font-size:1.5rem">' + t.icon + '</span>';
    html += '<div><div style="font-weight:700;color:#f1f5f9;font-size:0.9rem">' + t.name + '</div>';
    html += '<div style="font-size:0.8rem;color:#94a3b8">' + t.desc + '</div></div>';
    html += '<span style="margin-left:auto;color:' + t.color + ';font-size:0.8rem">→</span>';
    html += '</a>';
  }
  html += '</div>';
  html += '<p style="font-size:0.7rem;color:#475569;margin-top:0.75rem">Disclosure: Some links are affiliate links. We may earn a commission at no extra cost to you.</p>';
  html += '</div>';

  // Find article content area and append
  var main = document.querySelector('main') || document.querySelector('article');
  if (!main) {
    // Fallback: insert after h1
    var h1 = document.querySelector('h1');
    if (h1 && h1.parentNode) {
      var div = document.createElement('div');
      div.innerHTML = html;
      h1.parentNode.insertBefore(div.firstElementChild, h1.nextSibling);
    }
    return;
  }

  // Insert before footer
  var section = main.querySelector('.section:last-of-type') || main.lastElementChild;
  if (section) {
    section.insertAdjacentHTML('afterend', html);
  } else {
    main.insertAdjacentHTML('beforeend', html);
  }
})();

// ===== Ko-fi Support Button =====
(function() {
  var btn = document.createElement('div');
  btn.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:999';
  btn.innerHTML = '<a href="https://ko-fi.com/kangjian" target="_blank" rel="noopener"><img src="https://storage.ko-fi.com/cdn/kofi2.png?v=3" alt="Buy Me a Coffee" style="height:40px;border:none;box-shadow:0 4px 12px rgba(0,0,0,0.15);border-radius:4px"></a>';
  document.body.appendChild(btn);
})();
