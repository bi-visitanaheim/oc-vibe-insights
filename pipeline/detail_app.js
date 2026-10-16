/* Select any value (Oct. 15, 2026): every chart mark, table cell, key figure and bold number in the text opens a small
   data card with the value, what it measures, the chart or table it comes from, the period, the source, and the
   library file to read more. Hover tooltips stay as they were; this adds click, tap and keyboard (Enter) access. */
(function () {
  const SECT = Object.fromEntries(S.map(s => [s.id, s]));
  const LIBF = (DATA.lib && DATA.lib.files) || [];
  const SKIP = 'button, a, summary, input, select, textarea, label, [data-go], [data-ask-open], [data-export], .exp-dlg, .lib-file, header.band, .side, .secnav, #dpanel, .mk-paper, .sp-grid, .mk-design, .mk-mot, .upnext2, .kts';
  const txt = el => el ? el.textContent.replace(/\s+/g, ' ').trim() : '';
  const stopWords = new Set(['the', 'and', 'of', 'for', 'via', 'pub', 'data', 'report', 'to', 'in', 'on', 'a', 'an', 'by', 'with', 'through', 'published', 'calendar', 'visit', 'anaheim', 'analysis', 'calculation', 'bi', 'calc', 'oct', 'sept', 'aug', 'apr', 'may']);
  function libFor(src, sid) {
    if (!src || !LIBF.length) return null;
    const words = (src.toLowerCase().match(/[a-z][a-z.&-]{2,}/g) || []).filter(w => !stopWords.has(w));
    if (!words.length) return null;
    let best = null, bestScore = 0;
    LIBF.forEach(f => {
      if (f.topic === 'report') return;
      const hay = (f.title + ' ' + f.publisher + ' ' + (f.kind || '')).toLowerCase();
      let sc = words.reduce((n, w) => n + (hay.includes(w) ? 1 : 0), 0);
      if (sid && (f.used_in || []).includes(sid)) sc += 1.5;
      if (sc > bestScore) { bestScore = sc; best = f; }
    });
    return bestScore >= 2.5 ? best : null;
  }
  /* ---------- the card ---------- */
  const pn = document.createElement('div');
  pn.id = 'dpanel'; pn.setAttribute('role', 'dialog'); pn.setAttribute('aria-label', 'Data detail'); pn.hidden = true; pn.tabIndex = -1;
  document.body.appendChild(pn);
  let lastFocus = null, hotEl = null;
  function close() { if (pn.hidden) return; pn.hidden = true; if (hotEl) hotEl.classList.remove('dp-hot'); hotEl = null; if (lastFocus && document.contains(lastFocus)) try { lastFocus.focus({ preventScroll: true }); } catch (_) {} }
  function place(x, y) {
    const W = window.innerWidth, H = window.innerHeight, r = pn.getBoundingClientRect(); let left = x + 16, top = y + 16;
    if (left + r.width > W - 12) left = Math.max(12, x - r.width - 16);
    if (top + r.height > H - 12) top = Math.max(12, y - r.height - 16);
    pn.style.left = left + 'px'; pn.style.top = top + 'px';
  }
  function open(d, el, x, y, viaKey) {
    const page = el.closest('.page'), sid = page ? page.id : '', s = SECT[sid];
    const src = d.src || (s && s.ans_src) || '';
    const lib = libFor(src, sid);
    const period = d.period || (s && s.period) || '';
    const rows = (d.ctx || []).filter(r => r && r[1]);
    pn.innerHTML = `<div class="dp-h"><span class="dp-k">${esc(page ? page.dataset.title : 'OC Vibe Insights')}</span><button type="button" class="dp-x" aria-label="Close">×</button></div>
      <p class="dp-v">${esc(d.value)}</p>${d.label ? `<p class="dp-l">${esc(d.label)}</p>` : ''}
      ${rows.length ? `<dl class="dp-dl">${rows.map(([k, v]) => `<div><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join('')}</dl>` : ''}
      ${period ? `<p class="dp-p"><b>Period:</b> ${esc(period)}</p>` : ''}
      ${src ? `<p class="dp-s"><b>Source:</b> ${esc(src)}</p>` : ''}
      <div class="dp-acts"><button type="button" class="ctl accent" data-dp="copy">Copy with source</button>${lib ? `<button type="button" class="ctl" data-dp="lib">Open the source file</button>` : ''}${d.jump && $(d.jump) ? `<button type="button" class="ctl" data-dp="jump">Show the data</button>` : ''}</div>
      ${lib ? `<p class="dp-f">${esc(lib.title)} · ${esc(lib.publisher)}</p>` : ''}`;
    pn.hidden = false;
    if (hotEl) hotEl.classList.remove('dp-hot'); hotEl = el; el.classList.add('dp-hot');
    const phone = window.innerWidth < 640;
    pn.classList.toggle('sheet', phone);
    if (!phone) place(x, y); else { pn.style.left = ''; pn.style.top = ''; }
    const line = `${d.label ? d.label + ': ' : ''}${d.value}${rows.length ? ' (' + rows.map(r => r[1]).join('; ') + ')' : ''}${period ? ', ' + period : ''}. Source: ${src || 'OC Vibe Insights, Visit Anaheim Business Intelligence'}.`;
    pn.querySelector('.dp-x').onclick = close;
    pn.querySelector('[data-dp="copy"]').onclick = async () => { try { await navigator.clipboard.writeText(line); toast('Copied: ' + line.slice(0, 120) + (line.length > 120 ? '…' : '')); } catch (_) { toast(line); } };
    const lb = pn.querySelector('[data-dp="lib"]'); if (lb) lb.onclick = () => { close(); location.hash = '#library/' + lib.id; };
    const jb = pn.querySelector('[data-dp="jump"]'); if (jb) jb.onclick = () => { close(); const t = $(d.jump); if (t) { t.scrollIntoView({ block: 'start', behavior: 'smooth' }); } };
    if (viaKey) { lastFocus = el; pn.focus(); } else lastFocus = null;
  }
  /* ---------- what was selected ---------- */
  const figInfo = el => {
    const f = el.closest('figure, .ig, .chartf, .art-fig, .tbl, .ann, .mp');
    if (!f) return {};
    const title = txt(f.querySelector('h3, h4, .tbl-cap b'));
    const sub = txt(f.querySelector('.csub2, .ig-h p, .tbl-cap span'));
    const src = txt(f.querySelector('p.src, .ig-src, .src-inline')).replace(/^Sources?:\s*/, '');
    return { title, sub, src };
  };
  const dataSeg = el => { const p = el.closest('.page'); if (!p || !SECT[p.id]) return null; const s = SECT[p.id], g = (s.info || []).length || (s.maps || []).length; return `${p.id}-s${g ? 3 : 2}`; };
  function fromTip(el) {
    const t = el.getAttribute('data-tip') || '', i = t.indexOf(': ');
    const fi = figInfo(el);
    return { value: i > 0 ? t.slice(i + 2) : t, label: i > 0 ? t.slice(0, i) : '', ctx: [['Chart', fi.title], ['Measure', fi.sub]], src: fi.src };
  }
  function fromCell(cell) {
    const tr = cell.parentElement, table = cell.closest('table'), idx = [...tr.children].indexOf(cell);
    const head = table.querySelectorAll('thead th')[idx], rowH = tr.querySelector('th[scope="row"], td');
    const fi = figInfo(cell);
    const sc = table.closest('.scroll'), capT = fi.title || (sc && sc.getAttribute('aria-label')) || '';
    return { value: txt(cell), label: cell === rowH ? txt(head) : txt(rowH), ctx: [['Column', cell === rowH ? '' : txt(head)], ['Table', capT], ['Measure', fi.sub]], src: fi.src };
  }
  function fromCard(card) {
    const v = card.querySelector('.as-v, .dfig, .ak-v, .mdb-kpi b, .ask-key b'), l = card.querySelector('.as-l, .dfl, .ak-l');
    const k = card.querySelector('.as-k, .dk'), p = card.querySelector('.as-p, .calc-line');
    return { value: txt(v), label: txt(l), ctx: [['Area and period', txt(k)], ['Detail', txt(p).replace(/^Calculation:\s*/, '')]], src: txt(card.querySelector('.src-inline')).replace(/^Sources?:\s*/, '') || txt(card.closest('.answer') && card.closest('.answer').querySelector('.src-inline')).replace(/^Sources?:\s*/, ''), jump: dataSeg(card) };
  }
  function fromKv(b) {
    const blk = b.closest('p, li, .dcard, .answer, .nut, td') || b.parentElement;
    let sentence = txt(blk); const v = txt(b);
    const parts = sentence.split(/(?<=[.;])\s+(?=[A-Z])/); sentence = parts.find(x => x.includes(v)) || sentence;
    const box = b.closest('.answer, .nut, .dcard, li, .art-stat, .ocv-whole li, .ann-paper, .ask-item, details') || blk;
    const src = txt(box.querySelector && box.querySelector('.src-inline')).replace(/^Sources?:\s*/, '');
    return { value: v, label: '', ctx: [['In context', sentence.length > 260 ? sentence.slice(0, 257) + '…' : sentence]], src, jump: dataSeg(b) };
  }
  function resolve(t) {
    if (!t || !t.closest || t.closest(SKIP)) return null;
    let el = t.closest('[data-tip]'); if (el && !el.closest('[data-ask-open]')) return [el, fromTip(el)];
    el = t.closest('.art-stat, .dcard, .answer-key'); if (el) return [el, fromCard(el)];
    el = t.closest('b.kv, .t8-value'); if (el) return [el, fromKv(el)];
    el = t.closest('.page td, .page tbody th[scope="row"], #dpanel td');
    if (el && el.closest('.page') && txt(el)) return [el, fromCell(el)];
    return null;
  }
  document.addEventListener('click', e => {
    if (pn.contains(e.target) || (e.target.closest && e.target.closest('.g2-on'))) return;
    const hit = resolve(e.target);
    if (!hit) { close(); return; }
    if (window.getSelection && String(window.getSelection()).length > 2) return;   // let readers select text to copy
    open(hit[1], hit[0], e.clientX, e.clientY, false);
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { close(); return; }
    if (e.key !== 'Enter' || !e.target.closest) return;
    const hit = resolve(e.target); if (!hit) return;
    e.preventDefault(); const r = hit[0].getBoundingClientRect(); open(hit[1], hit[0], r.left + r.width / 2, r.bottom, true);
  });
  // the card follows its value while the page scrolls (charts loading above can shift the page); it closes once the value leaves the screen
  window.addEventListener('scroll', () => {
    if (pn.hidden || pn.classList.contains('sheet') || !hotEl) return;
    const r = hotEl.getBoundingClientRect();
    if (r.bottom < 0 || r.top > window.innerHeight) { close(); return; }
    place(r.left + Math.min(r.width, 60), r.bottom - 8);
  }, { passive: true });
  /* keyboard reach: key figures and bold numbers can be focused */
  const reach = () => document.querySelectorAll('.page .as-v, .page .dfig, .page .ak-v, .page b.kv, .page .t8-value').forEach(v => { if (v.tabIndex !== 0 && !v.closest(SKIP)) { v.tabIndex = 0; v.setAttribute('role', 'button'); v.setAttribute('aria-label', txt(v) + ': show source and detail'); } });
  reach(); setTimeout(reach, 2500); setTimeout(reach, 7000);   // T8 text renders after load
  /* G2 canvas charts report their clicked mark here */
  window.DATA_DETAIL = {
    fromG2(host, c, d, ev) {
      if (!d) return;
      const label = d.l || d.x || (d.m ? d.m + (d.k ? ', ' + d.k : '') : '') || d.cat || '';
      const value = d.t || (d.v != null ? String(d.v) : '');
      const fi = figInfo(host), r = host.getBoundingClientRect();
      const x = ev && ev.clientX != null ? ev.clientX : r.left + r.width / 2, y = ev && ev.clientY != null ? ev.clientY : r.top + 40;
      open({ value, label: [label, d.s || d.g].filter(Boolean).join(' · '), ctx: [['Chart', fi.title || c.title], ['Measure', fi.sub], ['Note', d.extra || (d.fc ? 'Forecast' : d.k === 'Forecast' ? 'Forecast' : '')]], src: fi.src || c.src }, host, x, y, false);
    }
  };
})();
