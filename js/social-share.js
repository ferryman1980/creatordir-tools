// ===== Social Share Buttons =====
(function() {
  var article = document.querySelector('article') || document.querySelector('main .section');
  if (!article) return;

  var url = encodeURIComponent(window.location.href);
  var title = encodeURIComponent(document.title);
  var desc = encodeURIComponent((document.querySelector('meta[name="description"]') || {}).content || '');

  var html = '<div style="margin:2rem 0;padding:1rem 0;border-top:1px solid var(--border);border-bottom:1px solid var(--border)">';
  html += '<p style="font-size:0.85rem;color:var(--text-muted);margin-bottom:0.75rem;font-weight:600">📤 Share this guide</p>';
  html += '<div style="display:flex;gap:8px;flex-wrap:wrap">';
  html += '<a href="https://twitter.com/intent/tweet?text=' + title + '&url=' + url + '" target="_blank" rel="noopener" style="padding:8px 16px;background:#1d9bf0;color:#fff;border-radius:8px;text-decoration:none;font-size:0.85rem;font-weight:600">𝕏 Twitter</a>';
  html += '<a href="https://www.facebook.com/sharer/sharer.php?u=' + url + '" target="_blank" rel="noopener" style="padding:8px 16px;background:#1877f2;color:#fff;border-radius:8px;text-decoration:none;font-size:0.85rem;font-weight:600">📘 Facebook</a>';
  html += '<a href="https://www.linkedin.com/sharing/share-offsite/?url=' + url + '" target="_blank" rel="noopener" style="padding:8px 16px;background:#0a66c2;color:#fff;border-radius:8px;text-decoration:none;font-size:0.85rem;font-weight:600">💼 LinkedIn</a>';
  html += '<a href="https://www.reddit.com/submit?url=' + url + '&title=' + title + '" target="_blank" rel="noopener" style="padding:8px 16px;background:#ff4500;color:#fff;border-radius:8px;text-decoration:none;font-size:0.85rem;font-weight:600">🔴 Reddit</a>';
  html += '<button onclick="navigator.clipboard.writeText(decodeURIComponent('' + url + ''));this.textContent='✅ Copied!'" style="padding:8px 16px;background:var(--bg-alt);color:var(--text);border:1px solid var(--border);border-radius:8px;font-size:0.85rem;font-weight:600;cursor:pointer">🔗 Copy Link</button>';
  html += '</div></div>';

  article.insertAdjacentHTML('afterend', html);
})();
