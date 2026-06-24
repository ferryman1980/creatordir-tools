/**
 * CreatorAI Tools - Site Search (v2)
 * Client-side search with modal overlay, fuzzy matching, category filters, sorting, and results counter
 */
(function() {
    'use strict';

    var searchIndex = [];
    var searchModal = null;
    var searchInput = null;
    var searchResults = null;
    var searchStats = null;
    var categoryFilter = 'all';
    var currentSort = 'relevance';
    var isOpen = false;
    var searchOverlay = null;

    // Category definitions for filter tags
    var CATEGORIES = [
        { id: 'all', label: 'All' },
        { id: 'tool', label: 'Tools' },
        { id: 'article', label: 'Articles' },
        { id: 'page', label: 'Pages' },
        { id: 'deals', label: 'Deals' },
        { id: 'course', label: 'Courses' },
        { id: 'job', label: 'Jobs' }
    ];

    // Sort options
    var SORT_OPTIONS = [
        { id: 'relevance', label: 'Relevance' },
        { id: 'az', label: 'A-Z' },
        { id: 'newest', label: 'Newest First' }
    ];

    // CSS styles inline
    var SEARCH_STYLES = [
        '.search-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px); z-index: 9999; display: none; animation: searchFadeIn 0.2s ease; }',
        '.search-overlay.open { display: block; }',
        '.search-modal { position: fixed; top: 15%; left: 50%; transform: translateX(-50%); width: 90%; max-width: 640px; max-height: 75vh; background: #1a1a2e; border: 1px solid #2a2a4a; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.5); z-index: 10000; display: none; flex-direction: column; overflow: hidden; animation: searchSlideDown 0.25s ease; }',
        '.search-modal.open { display: flex; }',
        '.search-modal-header { display: flex; align-items: center; padding: 16px 20px; border-bottom: 1px solid #2a2a4a; gap: 10px; background: #0f172a; }',
        '.search-modal-header .search-icon-inline { font-size: 1.2rem; color: #64748b; }',
        '.search-modal-header input { flex: 1; border: none; outline: none; font-size: 1rem; padding: 8px 0; background: transparent; font-family: inherit; color: #e2e8f0; }',
        '.search-modal-header input::placeholder { color: #64748b; }',
        '.search-modal-header .search-shortcut { font-size: 0.75rem; color: #64748b; background: #1e293b; padding: 3px 8px; border-radius: 4px; white-space: nowrap; }',
        '.search-toolbar { display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; border-bottom: 1px solid #2a2a4a; flex-wrap: wrap; gap: 8px; background: #0f172a; }',
        '.search-cat-filters { display: flex; gap: 6px; flex-wrap: wrap; }',
        '.search-filter-btn { padding: 4px 14px; border-radius: 20px; border: 1px solid #2a2a4a; background: transparent; font-size: 0.8rem; font-weight: 500; color: #94a3b8; cursor: pointer; transition: all 0.2s; font-family: inherit; }',
        '.search-filter-btn:hover { border-color: #8b5cf6; color: #8b5cf6; }',
        '.search-filter-btn.active { background: #8b5cf6; color: #fff; border-color: #8b5cf6; }',
        '.search-sort-group { display: flex; align-items: center; gap: 6px; }',
        '.search-sort-label { font-size: 0.75rem; color: #64748b; white-space: nowrap; }',
        '.search-sort-select { padding: 4px 10px; border: 1px solid #2a2a4a; border-radius: 6px; background: #1e293b; color: #e2e8f0; font-size: 0.8rem; font-family: inherit; cursor: pointer; outline: none; }',
        '.search-sort-select:focus { border-color: #8b5cf6; }',
        '.search-stats { padding: 8px 20px 4px; font-size: 0.78rem; color: #64748b; border-bottom: 1px solid #1e293b; background: #0f172a; }',
        '.search-results-container { flex: 1; overflow-y: auto; padding: 8px 0; max-height: 45vh; }',
        '.search-results-container::-webkit-scrollbar { width: 6px; }',
        '.search-results-container::-webkit-scrollbar-thumb { background: #2a2a4a; border-radius: 3px; }',
        '.search-group-label { padding: 8px 20px 4px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; }',
        '.search-result-item { display: flex; flex-direction: column; padding: 10px 20px; cursor: pointer; transition: background 0.15s; border-left: 3px solid transparent; }',
        '.search-result-item:hover { background: #1e293b; border-left-color: #8b5cf6; }',
        '.search-result-item .result-title { font-weight: 600; font-size: 0.9rem; color: #e2e8f0; line-height: 1.3; }',
        '.search-result-item .result-title mark { background: #854d0e; color: #fef08a; padding: 0 2px; border-radius: 2px; }',
        '.search-result-item .result-desc { font-size: 0.8rem; color: #94a3b8; margin-top: 2px; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }',
        '.search-result-item .result-desc mark { background: #854d0e; color: #fef08a; padding: 0 2px; border-radius: 2px; }',
        '.search-result-item .result-meta { display: flex; gap: 6px; margin-top: 4px; align-items: center; flex-wrap: wrap; }',
        '.search-result-item .result-badge { font-size: 0.68rem; padding: 2px 8px; border-radius: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }',
        '.result-badge.tool { background: rgba(139,92,246,0.15); color: #a78bfa; }',
        '.result-badge.article { background: rgba(6,182,212,0.15); color: #22d3ee; }',
        '.result-badge.comparison { background: rgba(245,158,11,0.15); color: #fbbf24; }',
        '.result-badge.deals { background: rgba(239,68,68,0.15); color: #f87171; }',
        '.result-badge.news { background: rgba(34,197,94,0.15); color: #4ade80; }',
        '.result-badge.page { background: rgba(148,163,184,0.15); color: #94a3b8; }',
        '.result-badge.tool_category { background: rgba(99,102,241,0.15); color: #818cf8; }',
        '.result-badge.extension { background: rgba(236,72,153,0.15); color: #f472b6; }',
        '.result-badge.promo { background: rgba(251,191,36,0.15); color: #fbbf24; }',
        '.result-badge.course { background: rgba(16,185,129,0.15); color: #34d399; }',
        '.result-badge.job { background: rgba(245,158,11,0.15); color: #fbbf24; }',
        '.search-result-item .result-tags { display: flex; gap: 4px; margin-left: auto; }',
        '.search-result-item .result-tag { font-size: 0.68rem; padding: 2px 6px; border-radius: 4px; background: #1e293b; color: #64748b; }',
        '.search-empty { padding: 3rem 2rem; text-align: center; color: #94a3b8; }',
        '.search-empty .empty-icon { font-size: 3rem; display: block; margin-bottom: 1rem; }',
        '.search-empty h3 { font-size: 1.1rem; color: #e2e8f0; margin: 0 0 0.5rem; }',
        '.search-empty p { font-size: 0.85rem; color: #64748b; margin: 0 0 0.3rem; line-height: 1.5; }',
        '.search-empty .empty-suggestions { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; margin-top: 1rem; }',
        '.search-empty .empty-suggestion { padding: 6px 16px; border: 1px solid #2a2a4a; border-radius: 20px; font-size: 0.8rem; color: #94a3b8; cursor: pointer; transition: all 0.2s; background: transparent; font-family: inherit; }',
        '.search-empty .empty-suggestion:hover { border-color: #8b5cf6; color: #8b5cf6; background: rgba(139,92,246,0.08); }',
        '@keyframes searchFadeIn { from { opacity:0; } to { opacity:1; } }',
        '@keyframes searchSlideDown { from { opacity:0; transform:translateX(-50%) translateY(-10px); } to { opacity:1; transform:translateX(-50%) translateY(0); } }',
    ].join('\n');

    // ----------------------
    // injectStyles
    // ----------------------

    function injectStyles() {
        if (document.getElementById('search-styles')) return;
        var style = document.createElement('style');
        style.id = 'search-styles';
        style.textContent = SEARCH_STYLES;
        document.head.appendChild(style);
    }

    // ----------------------
    // openSearch
    // ----------------------

    function openSearch() {
        if (isOpen) return;
        isOpen = true;
        searchOverlay.classList.add('open');
        searchModal.classList.add('open');
        searchInput.value = '';
        searchInput.focus();
        document.body.style.overflow = 'hidden';
        categoryFilter = 'all';
        currentSort = 'relevance';
        updateFilterButtons();
        updateSortSelect();
        renderResults('', 'all');
    }

    // ----------------------
    // closeSearch
    // ----------------------

    function closeSearch() {
        if (!isOpen) return;
        isOpen = false;
        searchOverlay.classList.remove('open');
        searchModal.classList.remove('open');
        document.body.style.overflow = '';
    }

    // ----------------------
    // buildModal
    // ----------------------

    function buildModal() {
        // Overlay
        searchOverlay = document.createElement('div');
        searchOverlay.className = 'search-overlay';
        document.body.appendChild(searchOverlay);

        // Modal
        searchModal = document.createElement('div');
        searchModal.className = 'search-modal';
        searchModal.innerHTML = [
            '<div class="search-modal-header">',
            '  <span class="search-icon-inline">\ud83d\udd0d</span>',
            '  <input type="text" placeholder="Search tools, articles, jobs..." autocomplete="off" autocorrect="off" spellcheck="false">',
            '  <span class="search-shortcut">ESC</span>',
            '</div>',
            '<div class="search-toolbar">',
            '  <div class="search-cat-filters"></div>',
            '  <div class="search-sort-group">',
            '    <span class="search-sort-label">Sort:</span>',
            '    <select class="search-sort-select"></select>',
            '  </div>',
            '</div>',
            '<div class="search-stats"></div>',
            '<div class="search-results-container"></div>'
        ].join('');
        document.body.appendChild(searchModal);

        searchInput = searchModal.querySelector('input');
        searchResults = searchModal.querySelector('.search-results-container');
        searchStats = searchModal.querySelector('.search-stats');

        // Build category filter buttons
        var filtersContainer = searchModal.querySelector('.search-cat-filters');
        CATEGORIES.forEach(function(cat) {
            var btn = document.createElement('button');
            btn.className = 'search-filter-btn' + (cat.id === 'all' ? ' active' : '');
            btn.dataset.cat = cat.id;
            btn.textContent = cat.label;
            btn.addEventListener('click', function() {
                categoryFilter = this.dataset.cat;
                updateFilterButtons();
                renderResults(searchInput.value, categoryFilter);
            });
            filtersContainer.appendChild(btn);
        });

        // Build sort select
        var sortSelect = searchModal.querySelector('.search-sort-select');
        SORT_OPTIONS.forEach(function(opt) {
            var option = document.createElement('option');
            option.value = opt.id;
            option.textContent = opt.label;
            if (opt.id === 'relevance') option.selected = true;
            sortSelect.appendChild(option);
        });
        sortSelect.addEventListener('change', function() {
            currentSort = this.value;
            renderResults(searchInput.value, categoryFilter);
        });

        // Input event
        searchInput.addEventListener('input', function() {
            renderResults(this.value, categoryFilter);
        });

        // Overlay click to close
        searchOverlay.addEventListener('click', closeSearch);

        // Prevent modal click from closing
        searchModal.addEventListener('click', function(e) {
            e.stopPropagation();
        });

        // Keyboard nav
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') closeSearch();
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                var first = searchResults.querySelector('.search-result-item');
                if (first) first.focus();
            }
        });
        searchResults.addEventListener('keydown', function(e) {
            var items = searchResults.querySelectorAll('.search-result-item');
            var idx = Array.prototype.indexOf.call(items, document.activeElement);
            if (e.key === 'ArrowDown') { e.preventDefault(); if (idx + 1 < items.length) items[idx + 1].focus(); }
            if (e.key === 'ArrowUp') { e.preventDefault(); if (idx > 0) items[idx - 1].focus(); else searchInput.focus(); }
            if (e.key === 'Enter') { e.preventDefault(); var a = document.activeElement; if (a && a.dataset && a.dataset.url) window.location.href = a.dataset.url; }
            if (e.key === 'Escape') closeSearch();
        });
    }

    function updateFilterButtons() {
        var btns = searchModal.querySelectorAll('.search-filter-btn');
        btns.forEach(function(btn) {
            btn.classList.toggle('active', btn.dataset.cat === categoryFilter);
        });
    }

    function updateSortSelect() {
        var select = searchModal.querySelector('.search-sort-select');
        if (select) select.value = currentSort;
    }

    // ----------------------
    // renderResults
    // ----------------------

    function renderResults(query, category) {
        var results;
        if (!query || query.trim() === '') {
            results = searchIndex.slice();
        } else {
            var q = query.toLowerCase().trim();
            results = searchIndex.filter(function(item) {
                var haystack = (item.title + ' ' + (item.description || '') + ' ' + (item.tags || []).join(' ')).toLowerCase();
                return fuzzyScore(haystack, q) > 0;
            });
            results = results.map(function(item) {
                return { item: item, score: scoreItem(item, q) };
            });
        }
        if (category && category !== 'all') {
            results = results.filter(function(r) {
                var cat = r.item ? r.item.category : r.category;
                return cat === category;
            });
        }
        var totalAvailable = results.length;
        var displayResults = results.slice ? results.slice() : results;
        if (currentSort === 'az') {
            displayResults.sort(function(a, b) {
                var ta = a.item ? a.item.title : a.title;
                var tb = b.item ? b.item.title : b.title;
                return (ta || '').localeCompare(tb || '');
            });
        } else if (currentSort === 'newest') {
            displayResults.sort(function(a, b) {
                var da = (a.item ? a.item.date || a.item.title : a.date || a.title) || '';
                var db = (b.item ? b.item.date || b.item.title : b.date || b.title) || '';
                return db.localeCompare(da);
            });
        } else {
            if (displayResults[0] && displayResults[0].score !== undefined) {
                displayResults.sort(function(a, b) { return b.score - a.score; });
            }
        }
        var normalized = displayResults.map(function(r) { return r.item ? r.item : r; });
        normalized = normalized.slice(0, 30);
        var shown = normalized.length;
        searchStats.textContent = 'Showing ' + shown + ' of ' + totalAvailable + ' results';
        if (normalized.length === 0) {
            var suggestions = ['AI writing', 'video editing', 'design tools', 'text to speech', 'image generator', 'productivity'];
            if (category === 'tool') suggestions = ['AI writing', 'video editing', 'design', 'text to speech'];
            else if (category === 'article') suggestions = ['guide', 'tutorial', 'review', 'workflow'];
            else if (category === 'deals') suggestions = ['discount', 'coupon', 'free', 'sale'];
            searchResults.innerHTML = [
                '<div class="search-empty">',
                '  <span class="empty-icon">\ud83d\udd0d</span>',
                '  <h3>No results found' + (query ? ' for &quot;' + escapeHtml(query) + '&quot;' : '') + '</h3>',
                '  <p>Try different keywords or browse by category above.</p>',
                '  <p style="font-size:0.8rem;color:#64748b;margin-top:0.3rem">Suggestions:</p>',
                '  <div class="empty-suggestions">',
                suggestions.map(function(s) { return '<button class="empty-suggestion" data-suggestion="' + s + '">' + s + '</button>'; }).join(''),
                '  </div>',
                '</div>'
            ].join('');
            searchResults.querySelectorAll('.empty-suggestion').forEach(function(el) {
                el.addEventListener('click', function() {
                    searchInput.value = this.dataset.suggestion;
                    renderResults(searchInput.value, categoryFilter);
                    searchInput.focus();
                });
            });
            return;
        }
        var groups = {};
        var catLabels = { tool: 'Tools', article: 'Guides & Articles', comparison: 'Comparisons', deals: 'Deals & Offers', news: 'News', page: 'Pages', tool_category: 'Tool Categories', extension: 'Extensions', promo: 'Promotions', course: 'Courses', job: 'Jobs' };
        var catOrder = ['tool', 'tool_category', 'article', 'comparison', 'deals', 'news', 'extension', 'promo', 'course', 'job', 'page'];
        normalized.forEach(function(item) {
            var cat = item.category || 'page';
            if (!groups[cat]) groups[cat] = [];
            groups[cat].push(item);
        });
        var html = '';
        catOrder.forEach(function(cat) {
            var items = groups[cat];
            if (!items || items.length === 0) return;
            html += '<div class="search-group-label">' + (catLabels[cat] || cat) + '</div>';
            items.forEach(function(item) {
                var bc = item.category || 'page';
                html += '<div class="search-result-item" data-url="' + item.url + '" tabindex="0" role="button">';
                html += '  <div class="result-title">' + (query ? highlightMatch(item.title, query) : escapeHtml(item.title)) + '</div>';
                if (item.description) {
                    html += '  <div class="result-desc">' + (query ? highlightMatch(item.description.substring(0, 150), query) : escapeHtml(item.description.substring(0, 150))) + '</div>';
                }
                html += '  <div class="result-meta">';
                html += '    <span class="result-badge ' + bc + '">' + (catLabels[item.category] || item.category) + '</span>';
                if (item.tags && item.tags.length) {
                    html += '    <span class="result-tags">';
                    item.tags.slice(0, 3).forEach(function(tag) {
                        html += '<span class="result-tag">#' + tag + '</span>';
                    });
                    html += '    </span>';
                }
                html += '  </div>';
                html += '</div>';
            });
        });
        searchResults.innerHTML = html;
        searchResults.querySelectorAll('.search-result-item').forEach(function(el) {
            el.addEventListener('click', function() {
                window.location.href = this.dataset.url;
            });
        });
    }

    function fuzzyScore(text, query) {
        text = text.toLowerCase();
        query = query.toLowerCase();
        var score = 0;
        var qi = 0;
        var prev = false;
        for (var ti = 0; qi < query.length && ti < text.length; ti++) {
            if (text[ti] === query[qi]) {
                score += prev ? 5 : 10;
                if (ti === 0) score += 15;
                if (ti > 0 && (text[ti-1] === ' ' || text[ti-1] === '-')) score += 8;
                qi++;
                prev = true;
            } else {
                prev = false;
            }
        }
        if (qi < query.length) return 0;
        score -= (text.length - query.length) * 0.5;
        return Math.max(1, score);
    }

    function scoreItem(item, query) {
        var score = 0;
        var title = (item.title || '').toLowerCase();
        var desc = (item.description || '').toLowerCase();
        var tags = (item.tags || []).join(' ').toLowerCase();
        if (title.indexOf(query) !== -1) {
            score += 50;
            if (title === query) score += 30;
            if (title.indexOf(' ' + query) !== -1) score += 20;
        }
        if (desc.indexOf(query) !== -1) score += 20;
        if (tags.indexOf(query) !== -1) score += 15;
        return score;
    }

    function highlightMatch(text, query) {
        if (!query || !query.trim()) return escapeHtml(text);
        var q = query.replace(/[.*+?^${}(|)[\]\\]/g, "$&");
        var re = new RegExp('(' + q + ')', 'gi');
        return escapeHtml(text).replace(new RegExp(escapeHtml(q), 'gi'), '<mark>$&</mark>');
    }

    function escapeHtml(text) {
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // ----------------------
    // addSearchButtonToNav
    // ----------------------

    function addSearchButtonToNav() {
        var nav = document.querySelector('.site-header .container');
        if (!nav) return;
        if (nav.querySelector('.search-trigger-btn')) return;
        var btn = document.createElement('button');
        btn.className = 'search-trigger-btn';
        btn.setAttribute('aria-label', 'Search');
        btn.innerHTML = '\ud83d\udd0d <span class="kbd">Ctrl+K</span>';
        btn.style.cssText = 'background:none;border:none;cursor:pointer;font-size:1rem;padding:8px;border-radius:8px;transition:all 0.2s;color:#94a3b8';
        btn.addEventListener('mouseenter', function() { this.style.background = 'rgba(139,92,246,0.1)'; });
        btn.addEventListener('mouseleave', function() { this.style.background = 'none'; });
        var hamburger = nav.querySelector('.hamburger');
        if (hamburger) nav.insertBefore(btn, hamburger);
        else nav.appendChild(btn);
        btn.addEventListener('click', openSearch);
    }

    function loadSearchIndex() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/search-index.json', true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                try { searchIndex = JSON.parse(xhr.responseText); } catch(e) {}
            }
        };
        xhr.onerror = function() { console.warn('Failed to load search index'); };
        xhr.send();
    }

    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            if (isOpen) closeSearch(); else openSearch();
        }
        if (e.key === 'Escape' && isOpen) closeSearch();
    });

    function init() {
        injectStyles();
        buildModal();
        addSearchButtonToNav();
        loadSearchIndex();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();