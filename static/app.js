/* === LLM Wiki — Client-side Search & Tag Interaction === */

(function () {
  'use strict';

  const TYPE_LABELS = {
    concept: '概念',
    entity: '實體',
    summary: '摘要',
    analysis: '分析'
  };

  let searchIndex = null;

  // --- Search ---
  async function loadSearchIndex() {
    try {
      const base = document.querySelector('script[src$="app.js"]').src.replace('app.js', '');
      const res = await fetch(base + 'search-index.json');
      searchIndex = await res.json();
    } catch (e) {
      console.warn('Failed to load search index:', e);
    }
  }

  function initSearch() {
    const input = document.getElementById('search-input');
    const dropdown = document.getElementById('search-results');
    if (!input || !dropdown) return;

    let debounceTimer = null;

    input.addEventListener('input', function () {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => doSearch(input.value.trim(), dropdown), 200);
    });

    input.addEventListener('focus', function () {
      if (input.value.trim() && dropdown.children.length > 0) {
        dropdown.classList.add('active');
      }
    });

    document.addEventListener('click', function (e) {
      if (!e.target.closest('.search-wrapper')) {
        dropdown.classList.remove('active');
      }
    });

    // keyboard nav
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        dropdown.classList.remove('active');
        input.blur();
      }
    });
  }

  function doSearch(query, dropdown) {
    dropdown.innerHTML = '';
    if (!query || !searchIndex) {
      dropdown.classList.remove('active');
      return;
    }

    const tokens = query.toLowerCase().split(/\s+/);
    const base = document.querySelector('script[src$="app.js"]').src.replace('app.js', '');

    const results = searchIndex
      .map(page => {
        const haystack = (page.title + ' ' + (page.tags || []).join(' ') + ' ' + page.body).toLowerCase();
        const score = tokens.reduce((s, t) => s + (haystack.includes(t) ? 1 : 0), 0);
        return { ...page, score };
      })
      .filter(p => p.score === tokens.length)
      .sort((a, b) => {
        // title match ranks higher
        const aTitle = tokens.every(t => a.title.toLowerCase().includes(t)) ? 1 : 0;
        const bTitle = tokens.every(t => b.title.toLowerCase().includes(t)) ? 1 : 0;
        return bTitle - aTitle || b.score - a.score;
      })
      .slice(0, 10);

    if (results.length === 0) {
      dropdown.innerHTML = '<div class="search-item"><span class="si-title">找不到結果</span></div>';
      dropdown.classList.add('active');
      return;
    }

    results.forEach(r => {
      const a = document.createElement('a');
      a.className = 'search-item';
      a.href = base + r.slug + '.html';

      // excerpt around first match
      let excerpt = '';
      const bodyLower = r.body.toLowerCase();
      const idx = bodyLower.indexOf(tokens[0]);
      if (idx >= 0) {
        const start = Math.max(0, idx - 30);
        const end = Math.min(r.body.length, idx + 60);
        excerpt = (start > 0 ? '…' : '') + r.body.slice(start, end) + (end < r.body.length ? '…' : '');
      }

      a.innerHTML =
        '<div><span class="si-title">' + escapeHtml(r.title) + '</span>' +
        '<span class="si-type">' + (TYPE_LABELS[r.type] || r.type) + '</span></div>' +
        (excerpt ? '<div class="si-excerpt">' + escapeHtml(excerpt) + '</div>' : '');
      dropdown.appendChild(a);
    });

    dropdown.classList.add('active');
  }

  // --- Tag Cloud Filter (on index page) ---
  function initTagFilter() {
    const cloud = document.getElementById('tag-cloud');
    if (!cloud) return;

    cloud.addEventListener('click', function (e) {
      const pill = e.target.closest('.tag-pill');
      if (!pill) return;
      e.preventDefault();

      // If it's a link, just follow it
      if (pill.tagName === 'A') {
        window.location.href = pill.href;
        return;
      }

      // Toggle active state for filtering on index page
      const wasActive = pill.classList.contains('active');
      cloud.querySelectorAll('.tag-pill').forEach(p => p.classList.remove('active'));
      if (!wasActive) {
        pill.classList.add('active');
        filterPagesByTag(pill.dataset.tag);
      } else {
        filterPagesByTag(null);
      }
    });
  }

  function filterPagesByTag(tag) {
    const cards = document.querySelectorAll('.page-card[data-tags]');
    cards.forEach(card => {
      if (!tag) {
        card.style.display = '';
        return;
      }
      const tags = card.dataset.tags.split(',');
      card.style.display = tags.includes(tag) ? '' : 'none';
    });

    // Hide empty sections
    document.querySelectorAll('.index-section').forEach(sec => {
      const visible = sec.querySelectorAll('.page-card:not([style*="display: none"])');
      sec.style.display = visible.length > 0 ? '' : 'none';
    });
  }

  // --- Mobile sidebar toggle ---
  function initMobileToggle() {
    const sidebar = document.getElementById('sidebar');
    if (!sidebar || window.innerWidth > 768) return;
    // Sidebar is auto-visible on mobile via CSS flex layout — no toggle needed at this scale
  }

  // --- Utilities ---
  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // --- Init ---
  document.addEventListener('DOMContentLoaded', function () {
    loadSearchIndex();
    initSearch();
    initTagFilter();
    initMobileToggle();
  });

  // Global keyboard shortcut: / to focus search
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
      const active = document.activeElement;
      if (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA') return;
      e.preventDefault();
      document.getElementById('search-input')?.focus();
    }
  });
})();
