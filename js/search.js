/**
 * CreatorAI Tools - Site Search
 * Client-side search with modal overlay, fuzzy matching, and category filtering
 */
(function() {
    'use strict';

    let searchIndex = [];
    let searchModal = null;
    let searchInput = null;
    let searchResults = null;
    let categoryFilter = 'all';
    let isOpen = false;

    // CSS styles injected once
    const SEARCH_STYLES = `
        .search-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.5);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
            z-index: 9999;
            display: none;
            animation: searchFadeIn 0.2s ease;
        }
        .search-overlay.open { display: block; }
        .search-modal {
            position: fixed;
            top: 15%; left: 50%;
            transform: translateX(-50%);
            width: 90%; max-width: 640px;
            max-height: 70vh;
            background: #fff;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            z-index: 10000;
            display: none;
            flex-direction: column;
            overflow: hidden;
            animation: searchSlideDown 0.25s ease;
        }
        .search-modal.open { display: flex; }
        .search-modal-header {
            display: flex;
            align-items: center;
            padding: 16px 20px;
            border-bottom: 1px solid #e2e8f0;
            gap: 10px;
            background: #f8fafc;
        }
        .search-modal-header .search-icon-inline {
            font-size: 1.2rem;
            color: #94a3b8;
        }
        .search-modal-header input {
            flex: 1;
            border: none;
            outline: none;
            font-size: 1rem;
            padding: 8px 0;
            background: transparent;
            font-family: inherit;
            color: #1e293b;
        }
        .search-modal-header input::placeholder { color: #94a3b8; }
        .search-modal-header .search-shortcut {
            font-size: 0.75rem;
            color: #94a3b8;
            background: #e2e8f0;
            padding: 3px 8px;
            border-radius: 4px;
            white-space: nowrap;
        }
        .search-filters {
            display: flex;
            gap: 6px;
            padding: 10px 20px;
            border-bottom: 1px solid #f1f5f9;
            flex-wrap: wrap;
        }
        .search-filter-btn {
            padding: 4px 14px;
            border-radius: 20px;
            border: 1px solid #e2e8f0;
            background: transparent;
            font-size: 0.8rem;
            font-weight: 500;
            color: #64748b;
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
        }
        .search-filter-btn:hover { border-color: #8b5cf6; color: #8b5cf6; }
        .search-filter-btn.active {
            background: #8b5cf6;
            color: #fff;
            border-color: #8b5cf6;
        }
        .search-results-container {
            flex: 1;
            overflow-y: auto;
            padding: 8px 0;
            max-height: 50vh;
        }
        .search-results-container::-webkit-scrollbar { width: 6px; }
        .search-results-container::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 3px; }
        .search-group-label {
            padding: 8px 20px 4px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94a3b8;
        }
        .search-result-item {
            display: flex;
            flex-direction: column;
            padding: 10px 20px;
            cursor: pointer;
            transition: background 0.15s;
            border-left: 3px solid transparent;
        }
        .search-result-item:hover { background: #f1f5f9; border-left-color: #8b5cf6; }
        .search-result-item .result-title {
            font-weight: 600;
            font-size: 0.9rem;
            color: #1e293b;
            line-height: 1.3;
        }
        .search-result-item .result-title mark {
            background: #fef08a;
            color: #1e293b;
            padding: 0 2px;
            border-radius: 2px;
        }
        .search-result-item .result-desc {
            font-size: 0.8rem;
            color: #64748b;
            margin-top: 2px;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .search-result-item .result-desc mark {
            background: #fef08a;
            color: #475569;
            padding: 0 2px;
            border-radius: 2px;
        }
        .search-result-item .result-meta {
            display: flex;
            gap: 6px;
            margin-top: 4px;
            align-items: center;
        }
        .search-result-item .result-badge {
            font-size: 0.68rem;
            padding: 2px 8px;
            border-radius: 10px;
            font-weight: 600;
        }
        .result-badge.tool { background: #ede9fe; color: #6d28d9; }
        .result-badge.article { background: #dbeafe; color: #1d4ed8; }
        .result-badge.page { background: #f1f5f9; color: #475569; }
        .result-badge.deals { background: #fef3c7; color: #b45309; }
        .result-badge.news { background: #fce7f3; color: #be185d; }
        .result-badge.comparison { background: #d1fae5; color: #047857; }
        .result-badge.tool_category { background: #e0e7ff; color: #3730a3; }
        .result-badge.extension { background: #ffedd5; color: #9a3412; }
        .result-badge.promo { background: #f3e8ff; color: #7c3aed; }
        .search-result-item .result-tags {
            display: flex;
            gap: 4px;
            flex-wrap: wrap;
        }
        .search-result-item .result-tag {
            font-size: 0.65rem;
            padding: 1px 6px;
            border-radius: 4px;
            background: #f1f5f9;
            color: #64748b;
        }
        .search-empty, .search-loading {
            padding: 40px 20px;
            text-align: center;
            color: #94a3b8;
            font-size: 0.9rem;
        }
        .search-empty em { font-style: normal; font-weight: 600; color: #475569; }
        .search-trigger-btn {
            background: none;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 6px 14px;
            cursor: pointer;
            font-size: 0.85rem;
            color: #64748b;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
            font-family: inherit;
        }
        .search-trigger-btn:hover {
            border-color: #8b5cf6;
            color: #8b5cf6;
            background: #f5f3ff;
        }
        .search-trigger-btn .kbd {
            font-size: 0.7rem;
            padding: 1px 5px;
            border-radius: 3px;
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            color: #94a3b8;
        }
        @keyframes searchFadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes searchSlideDown {
            from { opacity: 0; transform: translateX(-50%) translateY(-20px); }
            to { opacity: 1; transform: translateX(-50%) translateY(0); }
        }
        @media (max-width: 768px) {
            .search-modal { top: 5%; width: 95%; max-height: 85vh; }
            .search-modal-header input { font-size: 0.9rem; }
        }
    `;

    function injectStyles() {
        const style = document.createElement('style');
        style.textContent = SEARCH_STYLES;
        document.head.appendChild(style);
    }

    function buildModal() {
        searchModal = document.createElement('div');
        searchModal.innerHTML = `
            <div class="search-overlay" id="searchOverlay"></div>
            <div class="search-modal" id="searchModal">
                <div class="search-modal-header">
                    <span class="search-icon-inline">🔍</span>
                    <input type="text" id="searchInput" placeholder="Search tools, guides, comparisons..." autofocus>
                    <span class="search-shortcut">ESC</span>
                </div>
                <div class="search-filters" id="searchFilters">
                    <button class="search-filter-btn active" data-filter="all">All</button>
                    <button class="search-filter-btn" data-filter="tool">Tools</button>
                    <button class="search-filter-btn" data-filter="article">Guides</button>
                    <button class="search-filter-btn" data-filter="comparison">Comparisons</button>
                    <button class="search-filter-btn" data-filter="deals">Deals</button>
                    <button class="search-filter-btn" data-filter="news">News</button>
                    <button class="search-filter-btn" data-filter="page">Pages</button>
                </div>
                <div class="search-results-container" id="searchResults">
                    <div class="search-loading">Type to start searching...</div>
                </div>
            </div>
        `;
        document.body.appendChild(searchModal);

        searchInput = searchModal.querySelector('#searchInput');
        searchResults = searchModal.querySelector('#searchResults');
        const overlay = searchModal.querySelector('#searchOverlay');

        // Bind events
        searchInput.addEventListener('input', function() {
            doSearch(this.value);
        });

        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') closeSearch();
            if (e.key === 'Enter') {
                const firstLink = searchResults.querySelector('.search-result-item');
                if (firstLink) window.location.href = firstLink.dataset.url;
            }
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                const items = searchResults.querySelectorAll('.search-result-item');
                if (items.length) items[0].focus();
            }
        });

        // Result keyboard navigation
        searchResults.addEventListener('keydown', function(e) {
            const items = [...this.querySelectorAll('.search-result-item')];
            const idx = items.indexOf(document.activeElement);
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                const next = items[Math.min(idx + 1, items.length - 1)];
                if (next) next.focus();
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                const prev = items[Math.max(idx - 1, 0)];
                if (prev) prev.focus();
                if (idx === 0) searchInput.focus();
            } else if (e.key === 'Escape') {
                closeSearch();
            }
        });

        overlay.addEventListener('click', closeSearch);

        // Filter buttons
        searchModal.querySelectorAll('.search-filter-btn').forEach(function(btn) {
            btn.addEventListener('click', function() {
                searchModal.querySelectorAll('.search-filter-btn').forEach(function(b) { b.classList.remove('active'); });
                this.classList.add('active');
                categoryFilter = this.dataset.filter;
                doSearch(searchInput.value);
            });
        });

        // Close on resize to mobile
        window.addEventListener('resize', function() {
            if (window.innerWidth < 768 && isOpen) {
                // keep open, it's fine
            }
        });
    }

    function openSearch() {
        if (isOpen) return;
        isOpen = true;
        searchModal.querySelector('.search-overlay').classList.add('open');
        searchModal.querySelector('.search-modal').classList.add('open');
        setTimeout(function() { searchInput.focus(); }, 100);
        document.body.style.overflow = 'hidden';
    }

    function closeSearch() {
        if (!isOpen) return;
        isOpen = false;
        searchModal.querySelector('.search-overlay').classList.remove('open');
        searchModal.querySelector('.search-modal').classList.remove('open');
        document.body.style.overflow = '';
    }

    function highlightMatch(text, query) {
        if (!query) return text;
        const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp('(' + escaped + ')', 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }

    function scoreItem(item, query) {
        const q = query.toLowerCase();
        let score = 0;
        const titleLow = item.title.toLowerCase();
        const descLow = (item.description || '').toLowerCase();
        const tagsLow = (item.tags || []).join(' ').toLowerCase();

        // Exact title match = highest
        if (titleLow === q) score += 100;
        // Title starts with query
        if (titleLow.startsWith(q)) score += 80;
        // Title contains query
        if (titleLow.includes(q)) score += 50;
        // Word boundary in title
        if (new RegExp('\\b' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i').test(item.title)) score += 40;
        // Description contains query
        if (descLow.includes(q)) score += 20;
        // Tags match
        if (tagsLow.includes(q)) score += 15;
        // Partial word match in title
        const titleWords = titleLow.split(/\s+/);
        for (const word of titleWords) {
            if (word.startsWith(q) && word.length > q.length) score += 10;
            if (q.startsWith(word) && q.length > word.length) score += 5;
        }

        return score;
    }

    function doSearch(query) {
        query = query.trim();
        if (!query || query.length < 1) {
            searchResults.innerHTML = '<div class="search-loading">Type to start searching...</div>';
            return;
        }

        // Filter and score
        let results = searchIndex.filter(function(item) {
            if (categoryFilter !== 'all' && item.category !== categoryFilter) return false;
            const score = scoreItem(item, query);
            return score > 0;
        });

        // Score again for display
        results = results.map(function(item) {
            return { item: item, score: scoreItem(item, query) };
        });

        results.sort(function(a, b) { return b.score - a.score; });
        results = results.slice(0, 30); // top 30

        if (results.length === 0) {
            searchResults.innerHTML = '<div class="search-empty">No results found for <em>' + escapeHtml(query) + '</em></div>';
            return;
        }

        // Group by category
        const groups = {};
        const catLabels = {
            'tool': 'Tools', 'article': 'Guides & Articles', 'comparison': 'Comparisons',
            'deals': 'Deals & Offers', 'news': 'News', 'page': 'Pages',
            'tool_category': 'Tool Categories', 'extension': 'Extensions', 'promo': 'Promotions'
        };
        const catOrder = ['tool', 'tool_category', 'article', 'comparison', 'deals', 'news', 'extension', 'promo', 'page'];

        results.forEach(function(r) {
            const cat = r.item.category || 'page';
            if (!groups[cat]) groups[cat] = [];
            groups[cat].push(r);
        });

        let html = '';
        catOrder.forEach(function(cat) {
            if (!groups[cat]) return;
            html += '<div class="search-group-label">' + (catLabels[cat] || cat) + '</div>';
            groups[cat].forEach(function(r) {
                const item = r.item;
                const badgeClass = item.category || 'page';
                html += '<div class="search-result-item" data-url="' + item.url + '" tabindex="0" role="button">';
                html += '  <div class="result-title">' + highlightMatch(item.title, query) + '</div>';
                if (item.description) {
                    html += '  <div class="result-desc">' + highlightMatch(item.description.substring(0, 150), query) + '</div>';
                }
                html += '  <div class="result-meta">';
                html += '    <span class="result-badge ' + badgeClass + '">' + (catLabels[item.category] || item.category) + '</span>';
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

        // Click handlers
        searchResults.querySelectorAll('.search-result-item').forEach(function(el) {
            el.addEventListener('click', function() {
                window.location.href = this.dataset.url;
            });
        });
    }

    function escapeHtml(text) {
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function addSearchButtonToNav() {
        // Find the nav element
        var nav = document.querySelector('.site-header .container');
        if (!nav) return;

        // Check if search button already exists
        if (nav.querySelector('.search-trigger-btn')) return;

        var searchBtn = document.createElement('button');
        searchBtn.className = 'search-trigger-btn';
        searchBtn.setAttribute('aria-label', 'Search');
        searchBtn.innerHTML = '🔍 <span class="kbd">Ctrl+K</span>';

        // Insert before hamburger or at end of nav
        var hamburger = nav.querySelector('.hamburger');
        if (hamburger) {
            nav.insertBefore(searchBtn, hamburger);
        } else {
            nav.appendChild(searchBtn);
        }

        searchBtn.addEventListener('click', openSearch);
    }

    function loadSearchIndex() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/search-index.json', true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                try {
                    searchIndex = JSON.parse(xhr.responseText);
                } catch(e) {
                    console.warn('Search index parse error');
                }
            }
        };
        xhr.onerror = function() {
            console.warn('Failed to load search index');
        };
        xhr.send();
    }

    // Keyboard shortcut
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            openSearch();
        }
        if (e.key === 'Escape' && isOpen) {
            closeSearch();
        }
    });

    // Init on DOM ready
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
