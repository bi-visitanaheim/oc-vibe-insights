/* Page-by-page reading (Oct. 15, 2026, John Picou): every section is split into separate pages, one segment per page,
   so readers step through the report instead of scrolling one long page. "All pages" still shows everything in one scroll.
   Runs last; reuses app.js globals ($, esc, PAGES, CUR, LONG, goPage, updateNav, setView). */
(function () {
  const H0 = location.hash || '';
  const SP = {};      /* page id -> [{ w: wrapper, id: segment heading id, t: title }] */
  const SUB = {};     /* page id -> current sub-page index */
  const reduce = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  const pageTitle = id => ($(id) && $(id).dataset.title) || '';

  /* 1. Wrap each page's segments (a .seg-h heading and everything up to the next one) into .subpage blocks.
        Anything before the first heading (title, headline, byline, segment chips) stays on every page of the section. */
  PAGES.forEach(id => {
    const pg = $(id); if (!pg) return;
    const kids = [...pg.children], first = kids.findIndex(k => k.classList.contains('seg-h'));
    if (first < 0) return;
    const groups = [];
    kids.slice(first).forEach(k => { if (k.classList.contains('seg-h')) groups.push({ h: k, els: [] }); groups[groups.length - 1].els.push(k); });
    groups.forEach((g, i) => {
      if (!g.h.id) g.h.id = id + '-seg' + (i + 1);
      const w = document.createElement('div'); w.className = 'subpage'; w.dataset.sp = i;
      w.setAttribute('role', 'region'); w.setAttribute('aria-label', `${pageTitle(id)}, page ${i + 1} of ${groups.length}: ${g.h.querySelector('h3').textContent}`);
      g.h.before(w); g.els.forEach(e => w.appendChild(e));
      g.w = w; g.t = g.h.querySelector('h3').textContent.trim();
    });
    SP[id] = groups.map(g => ({ w: g.w, id: g.h.id, t: g.t }));
    SUB[id] = 0;
    /* pages without their own segment chips get a page strip under the title */
    if (!pg.querySelector('.seg-nav')) {
      const nav = document.createElement('nav'); nav.className = 'seg-nav sp-tabs'; nav.setAttribute('aria-label', 'Pages in ' + pageTitle(id));
      nav.innerHTML = SP[id].map((s, i) => `<button type="button" class="seg-chip" data-seg="${s.id}"><span aria-hidden="true">${i + 1}</span> ${esc(s.t)}</button>`).join('');
      SP[id][0].w.before(nav);
    }
  });

  /* 2. Sticky page bar: always on screen, so the next page is one tap away without scrolling to the end */
  const bar = document.createElement('nav'); bar.id = 'spBar'; bar.setAttribute('aria-label', 'Page navigation');
  bar.innerHTML = `<button type="button" class="sp-b sp-prev" id="spPrev"><span aria-hidden="true">‹</span> <span class="sp-bt"></span></button>
    <div class="sp-mid"><span class="sp-where" id="spWhere"></span><span class="sp-dots" id="spDots" aria-hidden="true"></span></div>
    <button type="button" class="sp-b sp-next" id="spNext"><span class="sp-bt"></span> <span aria-hidden="true">›</span></button>`;
  const foot = document.querySelector('#main > footer'); foot.before(bar);
  document.body.classList.add('paged');

  const single = () => !LONG;
  function showSub(id, i, scroll) {
    const subs = SP[id]; if (!subs) return;
    i = Math.max(0, Math.min(subs.length - 1, i)); SUB[id] = i;
    subs.forEach((s, k) => s.w.classList.toggle('cur', k === i));
    const pg = $(id);
    pg.querySelectorAll('.seg-nav .seg-chip').forEach(c => {
      const on = c.dataset.seg === subs[i].id; c.classList.toggle('on', on);
      if (on) c.setAttribute('aria-current', 'step'); else c.removeAttribute('aria-current');
    });
    /* the "See the data" button only shows on the page it points away from */
    if (scroll && single()) $('main').scrollIntoView({ block: 'start', behavior: 'auto' });
    if (single() && id === PAGES[CUR]) { try { history.replaceState(null, '', '#' + id.slice(2) + (i ? '/p' + (i + 1) : '')); } catch (_) {} }
    /* charts and diagrams that were drawn while hidden re-measure */
    requestAnimationFrame(() => window.dispatchEvent(new Event('resize')));
    syncBar();
  }

  /* where the reader lands: [page index, sub-page] for one step back or forward */
  function step(dir) {
    const id = PAGES[CUR], subs = SP[id], i = SUB[id] || 0;
    if (single() && subs && i + dir >= 0 && i + dir < subs.length) return showSub(id, i + dir, true);
    const ni = CUR + dir; if (ni < 0 || ni >= PAGES.length) return;
    goPage(ni);
    const nid = PAGES[ni]; if (single() && SP[nid]) showSub(nid, dir < 0 ? SP[nid].length - 1 : 0, false);
  }
  function label(dir) {
    const id = PAGES[CUR], subs = SP[id], i = SUB[id] || 0;
    if (single() && subs && i + dir >= 0 && i + dir < subs.length) return (dir > 0 ? 'Next: ' : 'Back: ') + subs[i + dir].t;
    const ni = CUR + dir; if (ni < 0 || ni >= PAGES.length) return '';
    return (dir > 0 ? 'Next section: ' : 'Back to ') + pageTitle(PAGES[ni]);
  }
  function syncBar() {
    const id = PAGES[CUR], subs = SP[id], i = SUB[id] || 0;
    bar.hidden = !single();
    const p = label(-1), n = label(1);
    $('spPrev').hidden = !p; $('spPrev').querySelector('.sp-bt').textContent = p;
    $('spNext').hidden = !n; $('spNext').querySelector('.sp-bt').textContent = n;
    $('spNext').classList.toggle('sec', !!n && n.startsWith('Next section'));
    $('spWhere').textContent = subs ? `${pageTitle(id)} · page ${i + 1} of ${subs.length}` : pageTitle(id);
    $('spDots').innerHTML = subs ? subs.map((_, k) => `<i class="${k === i ? 'on' : k < i ? 'done' : ''}"></i>`).join('') : '';
    $('prevBtn').disabled = CUR === 0 && (!subs || i === 0 || !single());
    $('nextBtn').disabled = CUR >= PAGES.length - 1 && (!subs || i >= subs.length - 1 || !single());
    const pn = $('pgNum'); if (pn && subs && single()) pn.textContent = pn.textContent.replace(/ · part.*$/, '') + ` · part ${i + 1} of ${subs.length}`;
  }
  $('spPrev').onclick = () => step(-1);
  $('spNext').onclick = () => step(1);
  $('prevBtn').onclick = () => step(-1);
  $('nextBtn').onclick = () => step(1);

  /* 3. goPage: open the sub-page that holds the target (or the first page of the section) */
  const goPage0 = goPage;
  goPage = function (i, target) {
    const id = PAGES[i];
    if (single() && SP[id]) {
      const t = target ? $(target) : null, w = t && t.closest('.subpage');
      showSub(id, w ? +w.dataset.sp : 0, false);
      const isHead = t && SP[id].some(s => s.id === target);
      goPage0(i, isHead ? undefined : target);
      showSub(id, SUB[id], false);
      return;
    }
    goPage0(i, target);
    syncBar();
  };
  const updateNav0 = updateNav;
  updateNav = function () { updateNav0(); syncBar(); };

  /* segment chips and "See the data" open their page instead of scrolling a long page */
  document.addEventListener('click', e => {
    const c = e.target.closest('.seg-chip'); if (!c || !single()) return;
    const t = $(c.dataset.seg), pg = t && t.closest('.page'); if (!pg || !SP[pg.id]) return;
    e.stopImmediatePropagation(); e.preventDefault();
    showSub(pg.id, +t.closest('.subpage').dataset.sp, true);
    const chip = pg.querySelector(`.seg-nav .seg-chip[data-seg="${t.id}"]`); if (chip && c.classList.contains('data-jump')) chip.focus();
  }, true);


  /* long lists (questions, library files) read one topic at a time in page-by-page view; typing a search looks across all topics */
  const LISTS = [['askTopics', 'askQ', '#askList', 'q-', id => (DATA.ask.items.find(q => q.id === id) || {}).topic],
                 ['libTopics', 'libQ', '#libFiles', 'f-', id => (DATA.lib.files.find(f => f.id === id) || {}).topic]];
  const chip = (set, t) => [...$(set).querySelectorAll('.chip')].find(c => c.dataset.t === (t || ''));
  function topicView() {
    LISTS.forEach(([set, q]) => {
      const cs = $(set); if (!cs) return;
      const pressed = cs.querySelector('.chip[aria-pressed="true"]'), first = cs.querySelectorAll('.chip')[1];
      if (single() && pressed && !pressed.dataset.t && !$(q).value.trim() && first) first.click();
      if (!single() && pressed && pressed.dataset.t) chip(set, '').click();
    });
  }
  LISTS.forEach(([set, q]) => { const inp = $(q); if (inp) inp.addEventListener('input', () => { const pr = $(set).querySelector('.chip[aria-pressed="true"]'); if (inp.value.trim() && pr && pr.dataset.t) { const v = inp.value; chip(set, '').click(); inp.value = v; inp.dispatchEvent(new Event('input')); } }); });
  function revealInList(el) {
    LISTS.forEach(([set, q, sel, pre, topicOf]) => {
      const item = el.closest(sel + ' [id^="' + pre + '"]'); if (!item || !item.closest('[hidden]') && !item.hidden) return;
      const c = chip(set, topicOf(item.id.slice(pre.length))) || chip(set, ''); if (c) { $(q).value = ''; c.click(); }
    });
  }

  /* anything that scrolls to an element (data cards, question links, library links) first opens its page */
  const siv = Element.prototype.scrollIntoView;
  Element.prototype.scrollIntoView = function (o) {
    if (single() && this.closest) {
      const pg = this.closest('.page'), w = this.closest('.subpage');
      if (pg && PAGES.indexOf(pg.id) >= 0 && PAGES.indexOf(pg.id) !== CUR) { CUR = PAGES.indexOf(pg.id); document.querySelectorAll('.page').forEach(p => p.classList.toggle('cur', p === pg)); updateNav(); }
      if (pg && w && SP[pg.id] && !w.classList.contains('cur')) showSub(pg.id, +w.dataset.sp, false);
    }
    if (this.closest) revealInList(this);
    return siv.call(this, o);
  };

  /* view switch: "All pages" shows every segment in one scroll; "One page" returns to the page-by-page view */
  const setView0 = setView;
  setView = function (long) { setView0(long); document.body.classList.toggle('paged', !long); topicView(); PAGES.forEach(id => SP[id] && showSub(id, SUB[id] || 0, false)); syncBar(); };
  $('vsOne').onclick = () => { setView(false); goPage(CUR); };
  $('vsLong').onclick = () => { setView(true); goPage(CUR); };
  $('vsLong').textContent = 'Scroll all';
  $('vsLong').title = 'Show every page of every section in one long scroll';
  $('vsOne').textContent = 'Page by page';

  /* keyboard: left and right arrow keys turn pages when focus is not in a field */
  document.addEventListener('keydown', e => {
    if (!single() || e.altKey || e.ctrlKey || e.metaKey) return;
    const tg = e.target; if (tg.closest('input,textarea,select,[contenteditable],dialog,.scroll,#dpanel')) return;
    if (e.key === 'ArrowRight') { step(1); e.preventDefault(); } else if (e.key === 'ArrowLeft') { step(-1); e.preventDefault(); }
  });

  /* deep links: #spend/p3 opens page 3 of Visitor spending */
  function deep(h) {
    const m = (typeof h === 'string' ? h : (location.hash || '')).slice(1).match(/^([\w-]+)\/p(\d+)$/); if (!m) return;
    const i = PAGES.indexOf('p-' + m[1]); if (i < 0) return;
    if (i !== CUR) goPage(i);
    showSub(PAGES[i], +m[2] - 1, false);
  }
  window.addEventListener('hashchange', deep);
  PAGES.forEach(id => SP[id] && showSub(id, 0, false));
  topicView();
  deep(H0);
  syncBar();
  /* searching the questions list jumps to that page */
  const aq = $('askQ'); if (aq) aq.addEventListener('focus', () => { const w = aq.closest('.subpage'); if (w && single()) showSub('p-ask', +w.dataset.sp, false); });
})();
