/* Make something new (Oct. 15, 2026): Doc, Slides, Design, Dashboard and Motion, built live from the reader's selections.
   Every figure is used exactly as published in the sections and Questions answered (value, period, source); nothing is recalculated.
   VA Branded: Escapism palette, Sharp Sans Display No. 2 (Proxima Nova in Office files), the approved logo on a light plate.
   Everything runs in the page: PptxGenJS 4.0.1 for slides, JSZip for Word, pdf-lib for PDF, canvas + MediaRecorder for video. No network. */
(function () {
  if (typeof DATA === 'undefined' || !document.getElementById('expDlg')) return;
  const SECS = S.filter(s => s.id !== 'p-appx');
  const SEC = Object.fromEntries(SECS.map(s => [s.id, s]));
  const VA = { dark: '#231F20', light: '#F9F9F2', white: '#FFFFFF', e1: '#43A3A3', e2: '#77C7C9', e3: '#125C60', e4: '#B4D9E3', p3: '#A10009', p2: '#FF7980' };
  const FONT = '"Sharp Sans Disp No2","Sharp Sans Display No. 2","Proxima Nova",system-ui,sans-serif';
  const LOGO = (document.querySelector('.logo-chip img') || {}).src || '';
  const LOGO_AR = 600 / 219;
  const ASOF = 'Data through Sept. 2026';
  const PREP = 'Prepared by Visit Anaheim Business Intelligence';
  const CONTACT = 'visitanaheim.org · bi@visitanaheim.org';

  /* ---------- the data pool: sections, areas, measures, charts ---------- */
  const GEOS = [['ana', 'Anaheim'], ['d5', 'OC Vibe area and District 5'], ['gg', 'Garden Grove'], ['oc', 'Orange County'], ['ca', 'California'], ['us', 'U.S.']];
  const GEO_N = Object.fromEntries(GEOS);
  const geoOf = w => /^Garden Grove/.test(w) ? 'gg' : /^Orange County/.test(w) ? 'oc' : /^(District 5|OC Vibe area|SR-57 beside OC Vibe)/.test(w) ? 'd5' : /^(California|West Coast)/.test(w) ? 'ca' : /^U\.S\./.test(w) ? 'us' : 'ana';
  const SHORT = { 'avg-spend': 'Spending per visitor', 'spend-growth': 'Visitor spending growth, 2025', 'q2-report': 'Q2 2026 visitors and spending', 'spend-mix': 'Largest share of visitor spending',
    jobs: 'Jobs supported by visitors', 'fb-jobs': 'Food and beverage share of visitor jobs', impact: 'Total economic impact', taxes: 'State and local taxes from visitors',
    'night-value': 'One more night', 'night-1pct': 'Each 1% of visitors adding a day', 'transport-impact': 'Visitor transportation spending and jobs', 'getting-here': 'Getting here',
    'travel-cost': 'Travel costs', 'd5-who': 'Who visits', 'd5-share': 'Share of Anaheim visitor days', 'd5-markets': 'Origin markets', media: 'Marketing reach', hotels: 'Hotel occupancy and rate', outlook: 'Outlook' };
  const norm = v => String(v).replace(/[▲▼\s]/g, '');
  const POOL = [];
  SECS.forEach(s => (s.cards || []).forEach((c, i) => POOL.push({ id: s.id.slice(2) + '-c' + i, sec: s.id, geo: geoOf(c[0]), where: c[0], label: c[1], value: String(c[2]).replace(/^[▲▼]\s?/, ''), detail: c[3] || '', src: c[4] || s.ans_src || '', kind: 'card' })));
  (DATA.ask.items || []).forEach(q => {
    if (!SEC[q.go]) return;
    q.geo.forEach((g, j) => {
      const geo = geoOf(g[0]);
      if (POOL.some(m => m.sec === q.go && m.geo === geo && norm(m.value) === norm(g[1]))) return;
      POOL.push({ id: q.id + '-' + j, sec: q.go, geo, where: g[0], label: SHORT[q.id] || q.topic, value: g[1], detail: g[2], src: g[3], kind: 'ask', q: q.id });
    });
  });
  const MBY = Object.fromEntries(POOL.map(m => [m.id, m]));
  const CHARTS = {};
  SECS.forEach(s => { CHARTS[s.id] = [...(s.feature || []), ...(s.charts || []), ...(s.more_charts || [])].filter(c => ['bars', 'cols', 'line'].includes(c.kind) && (c.rows ? c.rows.length : (c.series || []).length)); });

  /* One Export panel (Oct. 15, 2026): every file the app makes comes from the header's Export button. */
  const TOOLS = [
    { id: 'report', name: 'Full report', icon: 'file-document-multiple', desc: 'The report pages for the sections you choose, same layout as the deck.', fmts: [['pdf', 'PDF'], ['pptx', 'PowerPoint']] },
    { id: 'doc', name: 'Doc', tag: 'New', icon: 'file-document-outline', desc: 'A written brief: summary, each section’s story, key figures, charts, what it means and sources.', fmts: [['docx', 'Word'], ['html', 'Web page'], ['md', 'Markdown']] },
    { id: 'slides', name: 'Slides', tag: 'New', icon: 'presentation', desc: 'A short deck from your choices, with key-figure cards and charts you can edit.', fmts: [['pptx', 'PowerPoint']] },
    { id: 'design', name: 'Design', tag: 'New', icon: 'palette-outline', desc: 'A one-page graphic for social posts, print or screens.', fmts: [['png', 'PNG'], ['pdf', 'PDF'], ['svg', 'SVG']] },
    { id: 'motion', name: 'Motion', tag: 'Beta', icon: 'movie-open-outline', desc: 'A short video of the figures you choose.', fmts: [['video', 'Video'], ['png', 'Still image']] },
    { id: 'data', name: 'Data', icon: 'table-large', desc: 'Every table in the sections you choose, each with its source.', fmts: [['xlsx', 'Excel'], ['csv', 'CSV']] },
    { id: 'link', name: 'Share link', icon: 'link-variant', desc: 'A link to the public site, or to one section.', fmts: [['link', 'Link']] }];
  const TOOL = Object.fromEntries(TOOLS.map(t => [t.id, t]));
  const MAKES = ['doc', 'slides', 'design', 'motion'];
  const isMake = t => MAKES.includes(t);

  /* ---------- state (remembered per viewer) ---------- */
  const DEF = { tool: 'report', out: {}, pages: EXP_PAGES.slice(), geos: ['ana', 'd5', 'oc', 'us'], off: [], charts: 1, title: '', sub: '', fmt: 'social', theme: 'teal' };
  const saved = store.get('export') || {};
  const ST = Object.assign({}, DEF, saved);
  ST.pages = (ST.pages || []).filter(id => EXP_PAGES.includes(id)); ST.geos = (ST.geos || []).filter(g => GEO_N[g]); ST.off = ST.off || []; ST.out = ST.out || {};
  if (!TOOL[ST.tool]) ST.tool = 'report';
  const syncSecs = () => { ST.secs = SECS.map(s => s.id).filter(id => ST.pages.includes(id)); };
  syncSecs();
  const fmtOf = (t = ST.tool) => ST.out[t] && TOOL[t].fmts.some(f => f[0] === ST.out[t]) ? ST.out[t] : TOOL[t].fmts[0][0];
  const persist = () => store.set('export', Object.assign({}, ST, { secs: undefined }));
  const measures = (st = ST) => POOL.filter(m => st.secs.includes(m.sec) && st.geos.includes(m.geo)).sort((a, b) => st.secs.indexOf(a.sec) - st.secs.indexOf(b.sec));
  const chosen = (st = ST) => measures(st).filter(m => !st.off.includes(m.id));
  // featured figures: one from each section in turn, so a short list covers every section chosen
  const featured = (st = ST, n = 6, list = null) => { const ms = list || chosen(st), by = st.secs.map(id => ms.filter(m => m.sec === id)), out = [];
    for (let k = 0; out.length < n && by.some(g => g[k]); k++) by.forEach(g => { if (g[k] && out.length < n) out.push(g[k]); }); return out; };
  const chartsFor = (sid, st = ST) => (CHARTS[sid] || []).slice(0, st.charts);
  const titleOf = (st = ST) => st.title.trim() || (st.secs.length === 1 ? SEC[st.secs[0]].head : st.secs.length ? 'OC Vibe Insights: ' + listJoin(st.secs.map(id => SEC[id].tab.toLowerCase().replace(/^anaheim and oc vibe today$/, 'Anaheim and OC Vibe today'))) : 'OC Vibe Insights');
  const subOf = (st = ST) => st.sub.trim() || (st.geos.length ? listJoin(st.geos.map(g => GEO_N[g])) + ' · ' + ASOF : ASOF);
  function listJoin(a) { a = a.map(x => x.charAt(0).toUpperCase() === x.charAt(0) ? x : x); return a.length < 3 ? a.join(' and ') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1]; }
  const uniq = a => [...new Set(a.filter(Boolean))];
  const srcList = a => uniq(a.filter(Boolean).flatMap(x => String(x).split(/;\s+(?![^()]*\))/)).map(x => x.trim().replace(/\.$/, '')));
  const sourcesOf = (st = ST) => srcList([...chosen(st).map(m => m.src), ...st.secs.flatMap(id => chartsFor(id, st).map(c => c.src)), ...st.secs.map(id => SEC[id].ans_src)]);
  const today = () => apDate(new Date());
  const slug = (st = ST) => 'OC_Vibe_' + (st.secs.length === 1 ? SEC[st.secs[0]].tab.replace(/[^A-Za-z0-9]+/g, '_') : 'Insights_custom').replace(/_+$/, '');
  const icon = (n, sz = 22) => window.MDI && MDI[n] ? `<svg viewBox="0 0 24 24" width="${sz}" height="${sz}" aria-hidden="true"><path d="${MDI[n]}" fill="currentColor"/></svg>` : '';

  /* ---------- text helpers ---------- */
  const _mc = document.createElement('canvas').getContext('2d');
  function wrap(text, maxW, size, weight = 350, maxLines = 99) {
    _mc.font = `${weight} ${size}px ${FONT}`;
    const words = String(text).split(/\s+/), lines = []; let cur = '';
    words.forEach(w => { const t = cur ? cur + ' ' + w : w; if (_mc.measureText(t).width > maxW && cur) { lines.push(cur); cur = w; } else cur = t; });
    if (cur) lines.push(cur);
    if (lines.length > maxLines) { const k = lines.slice(0, maxLines); let last = k[maxLines - 1]; while (last.length && _mc.measureText(last + '…').width > maxW) last = last.replace(/\s*\S+$/, ''); k[maxLines - 1] = last + '…'; return k; }
    return lines;
  }
  const fitSize = (text, maxW, size, weight, minSize) => { _mc.font = `${weight} ${size}px ${FONT}`; let s = size; while (s > minSize && _mc.measureText(text).width > maxW) { s -= 2; _mc.font = `${weight} ${s}px ${FONT}`; } return s; };
  const xesc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  /* ---------- chart as SVG (doc, slides preview, design): deterministic, from the section's published rows ---------- */
  const THEMES = {
    teal: { name: 'Teal', bg: VA.e3, ink: VA.white, muted: VA.e4, bar: VA.e2, hi: VA.white, fc: 'rgba(255,255,255,.35)', grid: 'rgba(255,255,255,.28)', card: 'rgba(255,255,255,.09)', cardLine: 'rgba(180,217,227,.45)', value: VA.white, kick: VA.e4, plate: VA.white },
    dark: { name: 'Dark', bg: VA.dark, ink: VA.light, muted: '#D8D4CC', bar: VA.e1, hi: VA.e4, fc: 'rgba(119,199,201,.35)', grid: '#4A4546', card: '#302C2D', cardLine: '#4A4546', value: VA.e2, kick: VA.e2, plate: VA.light },
    light: { name: 'Light', bg: VA.light, ink: VA.dark, muted: '#4A4546', bar: VA.e2, hi: VA.e3, fc: 'rgba(67,163,163,.25)', grid: '#D9D6CE', card: VA.white, cardLine: VA.e4, value: VA.e3, kick: VA.e3, plate: VA.white } };
  function chartSvg(c, w, h, T, fs = 14) {
    // T = theme object (inline colors, for images) or null (CSS classes, follows light and dark mode)
    const P = (cls, k) => T ? `fill="${T[k]}"` : `class="${cls}"`;
    const L = (cls, k) => T ? `stroke="${T[k]}"` : `class="${cls}"`;
    let b = '';
    if (c.kind === 'bars') {
      const rows = c.rows.slice(0, 9), max = Math.max(...rows.map(r => r.v), 0) || 1;
      _mc.font = `350 ${fs}px ${FONT}`;
      const lw = Math.min(w * 0.42, Math.max(...rows.map(r => _mc.measureText(r.l).width)) + 12), vw = Math.max(...rows.map(r => _mc.measureText(r.t).width)) + fs * 1.4;
      const bw = Math.max(20, w - lw - vw), rh = h / rows.length;
      rows.forEach((r, i) => {
        const bh = Math.min(rh * 0.64, fs * 2.2), by = i * rh + (rh - bh) / 2, ww = Math.max(2, bw * Math.max(0, r.v) / max);
        const lab = wrap(r.l, lw - 12, fs, 350, 1)[0];
        b += `<text x="${(lw - 12).toFixed(1)}" y="${(by + bh / 2).toFixed(1)}" text-anchor="end" dominant-baseline="central" font-size="${fs}" ${P('mk-tx', 'ink')}>${xesc(lab)}</text>`;
        b += `<rect x="${lw.toFixed(1)}" y="${by.toFixed(1)}" width="${ww.toFixed(1)}" height="${bh.toFixed(1)}" rx="3" ${P(r.hi ? 'mk-bh' : 'mk-b', r.hi ? 'hi' : 'bar')} data-tip="${xesc(r.l + ': ' + r.t)}"/>`;
        b += `<text x="${(lw + ww + 8).toFixed(1)}" y="${(by + bh / 2).toFixed(1)}" dominant-baseline="central" font-size="${fs}" font-weight="700" ${P('mk-tx', 'ink')}>${xesc(r.t)}</text>`;
      });
    } else if (c.kind === 'cols') {
      const rows = c.rows, max = Math.max(...rows.map(r => r.v), 0) || 1, top = fs * 1.8, bot = fs * 1.9, ch = h - top - bot, cw = w / rows.length;
      b += `<line x1="0" x2="${w}" y1="${top + ch}" y2="${top + ch}" stroke-width="1" ${L('mk-gr', 'grid')}/>`;
      rows.forEach((r, i) => {
        const bh = Math.max(1, ch * Math.max(0, r.v) / max), x = i * cw + cw * 0.18, bw = cw * 0.64, y = top + ch - bh;
        b += `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${bw.toFixed(1)}" height="${bh.toFixed(1)}" rx="3" ${P(r.fc ? 'mk-fc' : r.hi ? 'mk-bh' : 'mk-b', r.fc ? 'fc' : r.hi ? 'hi' : 'bar')}${r.fc ? ` stroke-dasharray="4 3" stroke-width="1.5" ${T ? `stroke="${T.bar}"` : 'class="mk-fc"'}` : ''} data-tip="${xesc(r.l + ': ' + r.t + (r.fc ? ' (forecast)' : ''))}"/>`;
        b += `<text x="${(x + bw / 2).toFixed(1)}" y="${(y - 6).toFixed(1)}" text-anchor="middle" font-size="${fs * 0.86}" font-weight="700" ${P('mk-tx', 'ink')}>${xesc(r.t)}</text>`;
        b += `<text x="${(x + bw / 2).toFixed(1)}" y="${(h - fs * 0.5).toFixed(1)}" text-anchor="middle" font-size="${fs * 0.86}" ${P('mk-mu', 'muted')}>${xesc(r.l)}</text>`;
      });
    } else if (c.kind === 'line') {
      const sr = c.series.find(x => x.focal) || c.series[0], xs = c.x, v = sr.v, f = c.yfmt || {};
      const lo = Math.min(...v), hi = Math.max(...v), pad = (hi - lo) * 0.15 || 1, y0 = lo - pad, y1 = hi + pad;
      const top = fs * 1.6, bot = fs * 1.9, lft = fs * 0.6, rgt = fs * 3.2, ph = h - top - bot, pw = w - lft - rgt;
      const X = i => lft + pw * (xs.length === 1 ? 0.5 : i / (xs.length - 1)), Y = val => top + ph * (1 - (val - y0) / (y1 - y0));
      const fmt = val => (f.pre || '') + (+val).toFixed(f.dec != null ? f.dec : 1) + (f.suf || '');
      [0, 0.5, 1].forEach(k => { const yy = top + ph * k; b += `<line x1="${lft}" x2="${lft + pw}" y1="${yy.toFixed(1)}" y2="${yy.toFixed(1)}" stroke-width="1" ${L('mk-gr', 'grid')}/>`; });
      b += `<polyline fill="none" stroke-width="3.5" stroke-linejoin="round" ${L('mk-ln', 'hi')} points="${v.map((val, i) => X(i).toFixed(1) + ',' + Y(val).toFixed(1)).join(' ')}"/>`;
      const every = Math.ceil(xs.length / 8);
      v.forEach((val, i) => {
        b += `<circle cx="${X(i).toFixed(1)}" cy="${Y(val).toFixed(1)}" r="${i === v.length - 1 ? 6 : 4}" ${P('mk-pt', 'hi')} data-tip="${xesc(xs[i] + ': ' + fmt(val))}"/>`;
        if (i % every === 0 || i === xs.length - 1) b += `<text x="${X(i).toFixed(1)}" y="${(h - fs * 0.5).toFixed(1)}" text-anchor="middle" font-size="${fs * 0.86}" ${P('mk-mu', 'muted')}>${xesc(xs[i])}</text>`;
        if (i === 0 || i === v.length - 1 || val === hi) b += `<text x="${X(i).toFixed(1)}" y="${(Y(val) - 12).toFixed(1)}" text-anchor="middle" font-size="${fs * 0.86}" font-weight="700" ${P('mk-tx', 'ink')}>${xesc(fmt(val))}</text>`;
      });
    }
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family='${FONT}' role="img" aria-label="${xesc(c.title + '. ' + chartAlt(c))}">${b}</svg>`;
  }
  function chartAlt(c) {
    if (c.rows) return c.rows.map(r => r.l + ' ' + r.t + (r.fc ? ' (forecast)' : '')).join('; ');
    const sr = c.series.find(x => x.focal) || c.series[0], f = c.yfmt || {};
    return c.x.map((x, i) => x + ' ' + (f.pre || '') + (+sr.v[i]).toFixed(f.dec != null ? f.dec : 1) + (f.suf || '')).join('; ');
  }
  function chartRows(c) {   // [label, value text] for CSV, Word and Markdown tables
    if (c.rows) return c.rows.map(r => [r.l + (r.fc ? ' (forecast)' : ''), r.t]);
    const sr = c.series.find(x => x.focal) || c.series[0], f = c.yfmt || {};
    return c.x.map((x, i) => [x, (f.pre || '') + (+sr.v[i]).toFixed(f.dec != null ? f.dec : 1) + (f.suf || '')]);
  }

  /* ---------- the Export panel: what, which sections and areas, preview, save ---------- */
  const dlg = $('expDlg');
  dlg.innerHTML = `
    <div class="xp-h"><h3 id="expTitle">Export</h3><p>Choose what you want, choose the sections, and save. Everything is built in your browser from the figures in this app, with their periods and sources.</p><button type="button" class="xp-x" id="xpClose" aria-label="Close">${icon('close', 22)}</button></div>
    <div class="xp-body">
      <div class="xp-left">
        <p class="xp-step"><span>1</span> What do you want?</p>
        <div class="xp-tools" role="radiogroup" aria-label="What to export">${TOOLS.map(t => `<button type="button" role="radio" class="xp-tool" data-tool="${t.id}" aria-checked="false"><span class="xp-ic">${icon(t.icon, 22)}</span><span class="xp-tn"><b>${t.name}</b>${t.tag ? `<em class="mk-tag ${t.tag === 'Beta' ? 'beta' : ''}">${t.tag}</em>` : ''}</span><span class="xp-td">${t.desc}</span></button>`).join('')}</div>
        <div class="xp-fmts" id="xpFmts"></div>
        <p class="xp-step"><span>2</span> Which sections?</p>
        <div class="xp-q"><button type="button" class="ctl" id="xpAll">All</button><button type="button" class="ctl" id="xpCur">Current page</button><button type="button" class="ctl" id="xpCore">The four core questions</button><button type="button" class="ctl" id="xpNone">Clear</button></div>
        <div class="chipset" id="xpPages" role="group" aria-label="Sections">${EXP_PAGES.map(id => `<button type="button" class="chip" data-page="${id}" aria-pressed="false">${esc(pageTitle(id).replace(/ \(.*\)$/, ''))}</button>`).join('')}</div>
        <p class="xp-note" id="xpPageNote"></p>
        <div id="xpMake">
          <p class="xp-step"><span>3</span> Areas and details</p>
          <div class="chipset" id="mkGeos" role="group" aria-label="Areas">${GEOS.map(([k, n]) => `<button type="button" class="chip" data-geo="${k}" aria-pressed="false">${esc(n)}</button>`).join('')}</div>
          <div class="mk-opts">
            <label>Title <input type="text" id="mkTitle" maxlength="110"></label>
            <label>Subtitle <input type="text" id="mkSub" maxlength="140"></label>
            <label>Charts per section <select id="mkCharts"><option value="0">None</option><option value="1">1</option><option value="2">2</option></select></label>
            <label class="xp-dz" data-for="design">Size <select id="mkFmt"><option value="social">Social post (1080 × 1350)</option><option value="letter">Letter one-pager (8.5 × 11)</option><option value="wide">Widescreen (1920 × 1080)</option></select></label>
            <label class="xp-dz" data-for="design motion">Colors <select id="mkTheme"><option value="teal">Teal</option><option value="dark">Dark</option><option value="light">Light</option></select></label>
          </div>
          <details class="fold" id="mkMeasFold"><summary><span class="fd-ic" aria-hidden="true">+</span><span class="fd-t"><b>Key figures <span id="mkMeasN"></span></b><span>Design features 6 and Motion 8, one from each section in turn.</span></span><span class="fd-btn"><span class="fd-open">Show</span><span class="fd-close">Hide</span></span></summary><div class="fd-body"><div class="xp-q"><button type="button" class="ctl" id="mkMAll">Select all</button><button type="button" class="ctl" id="mkMNone">Clear</button></div><div class="mk-meas" id="mkMeas"></div></div></details>
        </div>
      </div>
      <div class="xp-right"><p class="xp-step"><span id="xpPrevN">3</span> Preview</p><div class="xp-prev" id="mkPrev" aria-live="polite"></div></div>
    </div>
    <div class="xp-foot"><p id="mkSel" aria-live="polite"></p><button type="button" class="ctl" id="xpCancel">Cancel</button><button type="button" class="ctl" id="xpShare" hidden>Share…</button><button type="button" class="ctl accent" id="xpGo">Save</button></div>`;

  function syncControls() {
    dlg.querySelectorAll('.xp-tool').forEach(b => { const on = b.dataset.tool === ST.tool; b.setAttribute('aria-checked', on); b.tabIndex = on ? 0 : -1; });
    const t = TOOL[ST.tool], f = fmtOf();
    $('xpFmts').innerHTML = t.fmts.length > 1 ? `<span class="xp-fl">Format</span>${t.fmts.map(([k, l]) => `<button type="button" class="chip" data-fmt="${k}" aria-pressed="${k === f}">${l}</button>`).join('')}` : '';
    dlg.querySelectorAll('[data-page]').forEach(b => { b.setAttribute('aria-pressed', ST.pages.includes(b.dataset.page)); b.classList.toggle('xp-off', isMake(ST.tool) && !SEC[b.dataset.page]); });
    dlg.querySelectorAll('[data-geo]').forEach(b => b.setAttribute('aria-pressed', ST.geos.includes(b.dataset.geo)));
    $('xpMake').hidden = !isMake(ST.tool); $('xpPrevN').textContent = isMake(ST.tool) ? '4' : '3';
    $('mkTitle').value = ST.title; $('mkSub').value = ST.sub; $('mkCharts').value = String(ST.charts); $('mkFmt').value = ST.fmt; $('mkTheme').value = ST.theme;
    $('mkTitle').placeholder = titleOf(Object.assign({}, ST, { title: '' })); $('mkSub').placeholder = subOf(Object.assign({}, ST, { sub: '' }));
    dlg.querySelectorAll('.xp-dz').forEach(l => l.hidden = !l.dataset.for.split(' ').includes(ST.tool));
    const extra = ST.pages.filter(id => !SEC[id]).length;
    $('xpPageNote').textContent = isMake(ST.tool) && extra ? `${t.name} uses the content sections; Overview, Questions answered, the library, Appendix and Sources are left out.` : '';
    $('xpShare').hidden = ST.tool !== 'link' || !navigator.share;
    $('xpGo').textContent = ST.tool === 'link' ? 'Copy link' : 'Save ' + (t.fmts.find(x => x[0] === f) || [, ''])[1];
  }
  function drawMeasures() {
    const ms = measures(), on = ms.filter(m => !ST.off.includes(m.id)).length;
    $('mkMeasN').textContent = `(${on} of ${ms.length} selected)`;
    $('mkMeas').innerHTML = ST.secs.map(id => { const g = ms.filter(m => m.sec === id); return g.length ? `<fieldset><legend>${esc(SEC[id].tab)}</legend>${g.map(m => `<label class="mk-m"><input type="checkbox" value="${m.id}"${ST.off.includes(m.id) ? '' : ' checked'}><span><b>${esc(m.value)}</b> ${esc(m.label)} <em>${esc(m.where)}</em></span></label>`).join('')}</fieldset>` : ''; }).join('') || '<p class="csub">Choose at least one content section and one area.</p>';
  }
  const pagesOK = () => isMake(ST.tool) ? ST.secs.length > 0 : ST.tool === 'data' ? S.some(x => ST.pages.includes(x.id)) : ST.pages.length > 0;
  let rt = 0;
  function refresh(now) {
    syncSecs(); persist(); syncControls(); if (isMake(ST.tool)) drawMeasures();
    const n = chosen().length, np = ST.pages.length;
    $('mkSel').textContent = !pagesOK() ? (isMake(ST.tool) || ST.tool === 'data' ? 'Choose at least one content section, for example Visitor spending.' : 'Choose at least one section.')
      : isMake(ST.tool) ? `${ST.secs.length} section${ST.secs.length > 1 ? 's' : ''} · ${ST.geos.length} area${ST.geos.length !== 1 ? 's' : ''} · ${n} key figure${n !== 1 ? 's' : ''}`
      : np === EXP_PAGES.length ? 'All sections' : `${np} of ${EXP_PAGES.length} sections`;
    $('xpGo').disabled = !pagesOK();
    clearTimeout(rt); rt = setTimeout(renderPreview, now ? 0 : 150);
  }
  const togglePage = id => { ST.pages = ST.pages.includes(id) ? ST.pages.filter(x => x !== id) : EXP_PAGES.filter(x => x === id || ST.pages.includes(x)); };
  dlg.addEventListener('click', e => {
    if (e.target === dlg) { close(); return; }
    const tb = e.target.closest('.xp-tool'); if (tb) { ST.tool = tb.dataset.tool; refresh(true); return; }
    const fb = e.target.closest('[data-fmt]'); if (fb) { ST.out[ST.tool] = fb.dataset.fmt; refresh(); return; }
    const pb = e.target.closest('[data-page]'); if (pb) { togglePage(pb.dataset.page); refresh(); return; }
    const gb = e.target.closest('[data-geo]'); if (gb) { const g = gb.dataset.geo; ST.geos = ST.geos.includes(g) ? ST.geos.filter(x => x !== g) : GEOS.map(x => x[0]).filter(x => x === g || ST.geos.includes(x)); refresh(); return; }
  });
  dlg.querySelector('.xp-tools').addEventListener('keydown', e => {
    if (!['ArrowRight', 'ArrowLeft', 'ArrowDown', 'ArrowUp'].includes(e.key)) return; e.preventDefault();
    const i = TOOLS.findIndex(t => t.id === ST.tool), j = (i + (e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : TOOLS.length - 1)) % TOOLS.length;
    ST.tool = TOOLS[j].id; refresh(true); dlg.querySelector(`[data-tool="${ST.tool}"]`).focus();
  });
  $('xpAll').onclick = () => { ST.pages = EXP_PAGES.slice(); refresh(); };
  $('xpCur').onclick = () => { ST.pages = [PAGES[CUR]].filter(id => EXP_PAGES.includes(id)); refresh(); };
  $('xpCore').onclick = () => { ST.pages = EXP_PAGES.filter(id => ['p-spend', 'p-night', 'p-transport', 'p-d5'].includes(id)); refresh(); };
  $('xpNone').onclick = () => { ST.pages = []; refresh(); };
  $('mkMeas').addEventListener('change', e => { const id = e.target.value; ST.off = e.target.checked ? ST.off.filter(x => x !== id) : [...ST.off, id]; refresh(); });
  $('mkMAll').onclick = () => { const ids = measures().map(m => m.id); ST.off = ST.off.filter(x => !ids.includes(x)); refresh(); };
  $('mkMNone').onclick = () => { ST.off = uniq([...ST.off, ...measures().map(m => m.id)]); refresh(); };
  $('mkTitle').addEventListener('input', e => { ST.title = e.target.value; refresh(); });
  $('mkSub').addEventListener('input', e => { ST.sub = e.target.value; refresh(); });
  $('mkCharts').onchange = e => { ST.charts = +e.target.value; refresh(); };
  $('mkFmt').onchange = e => { ST.fmt = e.target.value; refresh(); };
  $('mkTheme').onchange = e => { ST.theme = e.target.value; refresh(); };
  $('xpCancel').onclick = () => close();
  $('xpClose').onclick = () => close();
  $('xpShare').onclick = async () => { try { await navigator.share({ title: 'OC Vibe Insights', url: shareUrl(ST.pages) }); close(); } catch (_) {} };
  $('xpGo').onclick = () => save($('xpGo'));
  dlg.addEventListener('close', () => { if (MOT) { MOT.stop(); MOT = null; } });
  function open(tool) { if (tool && TOOL[tool]) ST.tool = tool; refresh(true); if (dlg.showModal) { if (!dlg.open) dlg.showModal(); } else dlg.setAttribute('open', ''); }
  function close() { if (MOT) { MOT.stop(); MOT = null; } if (dlg.close) dlg.close(); else dlg.removeAttribute('open'); }
  $('exportPdf').onclick = () => open();
  document.addEventListener('click', e => { const b = e.target.closest('[data-export]'); if (b) { e.preventDefault(); open(b.dataset.export || null); } });
  window.EXPORT = { open, close, state: () => JSON.parse(JSON.stringify(ST)) };

  /* ---------- previews ---------- */
  let MOT = null;
  function renderPreview() {
    const el = $('mkPrev'); if (MOT) { MOT.stop(); MOT = null; }
    if (!pagesOK()) { el.innerHTML = '<p class="mk-empty">Choose at least one section in step 2.</p>'; return; }
    try {
      const t = ST.tool, f = fmtOf();
      if (t === 'report') el.innerHTML = `<div class="xp-sum"><b>${f === 'pdf' ? 'PDF report' : 'PowerPoint deck'}</b><p>${ST.pages.length === EXP_PAGES.length ? 'The full report, every section.' : 'The title page plus the pages for:'}</p>${ST.pages.length === EXP_PAGES.length ? '' : `<ul>${ST.pages.map(id => `<li>${esc(pageTitle(id))}</li>`).join('')}</ul>`}<p class="mk-cap">Same layout as the published deck${f === 'pptx' ? '; slides stay editable' : ''}.</p></div>`;
      else if (t === 'data') { const ts = S.filter(x => ST.pages.includes(x.id)); el.innerHTML = `<div class="xp-sum"><b>${f === 'xlsx' ? 'Excel workbook' : 'CSV file'}</b><p>${ts.reduce((n, x) => n + x.tables.length, 0)} tables from ${ts.length} section${ts.length !== 1 ? 's' : ''}${f === 'xlsx' ? ', one sheet per section, numbers stored as numbers' : ''}, each followed by its source and period.</p><ul>${ts.map(x => `<li>${esc(x.tab)}: ${x.tables.length} table${x.tables.length !== 1 ? 's' : ''}</li>`).join('')}</ul></div>`; }
      else if (t === 'link') { const u = shareUrl(ST.pages); el.innerHTML = `<div class="xp-sum"><b>Link to the public site</b><p>${ST.pages.length === 1 ? 'Opens ' + esc(pageTitle(ST.pages[0])) + '.' : 'Opens the Overview. Choose one section to link straight to it.'}</p><label class="sr" for="xpLink">Link</label><input id="xpLink" class="xp-link" type="text" readonly value="${esc(u)}"><p class="mk-cap">Anyone with this link can open the public site. The claude.ai version stays private.</p></div>`; }
      else if (t === 'doc') el.innerHTML = `<div class="mk-paper">${docHtml(ST)}</div>`;
      else if (t === 'slides') el.innerHTML = slidesPreview(ST);
      else if (t === 'design') { const d = designSvg(ST); el.innerHTML = `<div class="mk-design" style="--ar:${d.w}/${d.h}">${d.svg}</div><p class="mk-cap">${d.w} × ${d.h} px · ${THEMES[ST.theme].name} colors · ${Math.min(6, chosen().length)} featured key figures, one from each section in turn</p>`; }
      else if (t === 'motion') { el.innerHTML = motionShell(); MOT = motionPlayer($('mkCanvas'), ST, true); }
    } catch (err) { el.innerHTML = '<p class="mk-empty">This preview could not be built. Try other choices, or contact the BI team.</p>'; console.error(err); }
  }

  /* ----- Doc ----- */
  function docModel(st) {
    const ms = chosen(st);
    return { title: titleOf(st), sub: subOf(st), date: today(),
      summary: st.secs.map(id => ({ tab: SEC[id].tab, head: SEC[id].head, ans: SEC[id].ans })),
      secs: st.secs.map(id => { const s = SEC[id]; return { id, tab: s.tab, head: s.head, dek: s.dek, period: s.period, nut: s.nut, lede: s.ans, ms: ms.filter(m => m.sec === id), charts: chartsFor(id, st),
        means: ((s.for_ocv || {}).enhance || []).slice(0, 3), table: (s.tables || [])[0] }; }),
      sources: sourcesOf(st) };
  }
  function docHtml(st) {
    const d = docModel(st);
    return `<header class="mkd-h"><img src="${LOGO}" alt="Visit Anaheim" class="mkd-logo"><div><p class="mkd-kick">OC Vibe Insights · ${esc(d.date)}</p><h1>${esc(d.title)}</h1><p class="mkd-sub">${esc(d.sub)}</p></div></header>
      <h2>Summary</h2><ul class="mkd-sum">${d.summary.map(x => `<li><b>${esc(x.tab)}:</b> ${emph(x.ans)}</li>`).join('')}</ul>
      ${d.secs.map(s => `<section class="mkd-s"><p class="mkd-kick">${esc(s.tab)} · ${esc(s.period)}</p><h2>${esc(s.head)}</h2><p>${emph(s.nut || s.lede)}</p>
        ${s.ms.length ? `<table class="mkd-t"><caption>Key figures</caption><thead><tr><th>Area and period</th><th>Measure</th><th class="n">Value</th><th>Detail</th></tr></thead><tbody>${s.ms.map(m => `<tr><td>${esc(m.where)}</td><td>${esc(m.label)}</td><td class="n"><b>${esc(m.value)}</b></td><td>${esc(m.detail)}<span class="mkd-src">Source: ${esc(m.src)}</span></td></tr>`).join('')}</tbody></table>` : ''}
        ${s.charts.map(c => `<figure class="mkd-f"><figcaption><b>${esc(c.title)}</b><span>${esc(c.sub || '')}</span></figcaption>${chartSvg(c, 760, c.kind === 'bars' ? Math.max(140, c.rows.length * 34) : 300, null, 14)}<p class="mkd-src">Source: ${esc(c.src || s.period)}</p></figure>`).join('')}
        ${s.means.length ? `<h3>What it means for OC Vibe</h3><ul>${s.means.map(x => `<li><b>${esc(x.tag)}.</b> ${emph(x.text)} <span class="mkd-src">(${esc(x.src)})</span></li>`).join('')}</ul>` : ''}</section>`).join('')}
      <h2>Sources</h2><ol class="mkd-srcs">${d.sources.map(x => `<li>${esc(x)}</li>`).join('')}</ol>
      <p class="mkd-foot">${PREP} · ${esc(d.date)} · ${ASOF} · ${CONTACT}. Figures are as published by each source; the full tables and source files are in the OC Vibe Insights app.</p>`;
  }
  function docMd(st) {
    const d = docModel(st), L = [`# ${d.title}`, '', `*${d.sub}*  `, `OC Vibe Insights · ${PREP} · ${d.date}`, '', '## Summary', '', ...d.summary.map(x => `- **${x.tab}:** ${x.ans}`), ''];
    d.secs.forEach(s => {
      L.push(`## ${s.head}`, '', `*${s.tab} · ${s.period}*`, '', s.nut || s.lede, '');
      if (s.ms.length) { L.push('| Area and period | Measure | Value | Detail | Source |', '|---|---|---:|---|---|'); s.ms.forEach(m => L.push(`| ${[m.where, m.label, '**' + m.value + '**', m.detail, m.src].map(x => String(x).replace(/\|/g, '/')).join(' | ')} |`)); L.push(''); }
      s.charts.forEach(c => { L.push(`**${c.title}**${c.sub ? ' (' + c.sub + ')' : ''}`, '', '| | Value |', '|---|---:|', ...chartRows(c).map(r => `| ${r[0]} | ${r[1]} |`), '', `Source: ${c.src || s.period}`, ''); });
      if (s.means.length) { L.push('### What it means for OC Vibe', '', ...s.means.map(x => `- **${x.tag}.** ${x.text} (${x.src})`), ''); }
    });
    L.push('## Sources', '', ...d.sources.map((x, i) => `${i + 1}. ${x}`), '', `${PREP} · ${ASOF} · ${CONTACT}`);
    return L.join('\n');
  }

  /* ----- Slides (one model for the preview and the .pptx) ----- */
  function slidesModel(st) {
    const ms = chosen(st), out = [];
    out.push({ t: 'title', title: titleOf(st), sub: subOf(st), date: today() });
    const top = st.secs.map(id => ms.find(m => m.sec === id)).filter(Boolean).slice(0, 4);
    out.push({ t: 'sum', title: 'At a glance', kicker: 'The headline figure from each section', kpis: top, bullets: st.secs.map(id => SEC[id].tab + ': ' + SEC[id].ans).slice(0, 6), src: uniq(top.map(m => m.src)).join('; ') });
    st.secs.forEach(id => {
      const s = SEC[id], sm = ms.filter(m => m.sec === id), ch = chartsFor(id, st);
      out.push({ t: 'sec', title: s.head, kicker: s.tab + ' · ' + s.period, text: s.nut || s.ans, kpis: sm.slice(0, 3), chart: ch[0] || null, src: uniq([...sm.slice(0, 3).map(m => m.src), ch[0] && ch[0].src]).join('; ') || s.ans_src });
      if (ch[1]) out.push({ t: 'chart', title: ch[1].title, kicker: s.tab + ' · ' + (ch[1].sub || s.period), chart: ch[1], src: ch[1].src || s.ans_src });
      const rest = sm.slice(3);
      for (let i = 0; i < rest.length; i += 8) out.push({ t: 'table', title: s.tab + ': more key figures' + (i ? ' (continued)' : ''), kicker: 'Area, period, value and source', rows: rest.slice(i, i + 8), src: uniq(rest.slice(i, i + 8).map(m => m.src)).join('; ') });
    });
    const means = st.secs.flatMap(id => ((SEC[id].for_ocv || {}).enhance || []).slice(0, 2).map(x => ({ tab: SEC[id].tab, ...x }))).slice(0, 8);
    if (means.length) out.push({ t: 'means', title: 'What it means for OC Vibe', kicker: 'By topic, from the sections chosen', items: means, src: uniq(means.map(x => x.src)).join('; ') });
    const srcs = sourcesOf(st);
    for (let i = 0; i < srcs.length; i += 10) out.push({ t: 'sources', title: 'Sources' + (i ? ' (continued)' : ''), kicker: ASOF + ' · ' + CONTACT, items: srcs.slice(i, i + 10) });
    return out;
  }
  function slidesPreview(st) {
    const sl = slidesModel(st);
    const kp = ks => `<div class="sp-kpis n${ks.length}">${ks.map(m => `<div class="sp-k"><span>${esc(m.where)}</span><b>${esc(m.value)}</b><i>${esc(m.label)}</i></div>`).join('')}</div>`;
    const one = (s, i) => {
      let b = '';
      if (s.t === 'title') b = `<div class="sp-title"><div class="sp-plate"><img src="${LOGO}" alt=""></div><h4>${esc(s.title)}</h4><p>${esc(s.sub)}</p><p class="sp-d">${PREP} · ${esc(s.date)}</p></div>`;
      else {
        b = `<div class="sp-c"><img class="sp-logo" src="${LOGO}" alt=""><h4>${esc(s.title)}</h4><p class="sp-kick">${esc(s.kicker || '')}</p><div class="sp-body">`;
        if (s.t === 'sum') b += `${kp(s.kpis)}<ul>${s.bullets.map(x => `<li>${emph(x)}</li>`).join('')}</ul>`;
        if (s.t === 'sec') b += `<div class="sp-two${s.chart ? '' : ' one'}"><div>${kp(s.kpis)}<p>${emph(s.text)}</p></div>${s.chart ? `<div class="sp-ch"><b>${esc(s.chart.title)}</b>${chartSvg(s.chart, 520, 300, null, 15)}</div>` : ''}</div>`;
        if (s.t === 'chart') b += `<div class="sp-ch wide">${chartSvg(s.chart, 900, 330, null, 15)}</div>`;
        if (s.t === 'table') b += `<table><tr><th>Area and period</th><th>Measure</th><th>Value</th><th>Detail</th></tr>${s.rows.map(m => `<tr><td>${esc(m.where)}</td><td>${esc(m.label)}</td><td><b>${esc(m.value)}</b></td><td>${esc(m.detail)}</td></tr>`).join('')}</table>`;
        if (s.t === 'means') b += `<ul>${s.items.map(x => `<li><b>${esc(x.tag)} (${esc(x.tab)}).</b> ${emph(x.text)}</li>`).join('')}</ul>`;
        if (s.t === 'sources') b += `<ol class="sp-src">${s.items.map(x => `<li>${esc(x)}</li>`).join('')}</ol>`;
        b += `</div>${s.src ? `<p class="sp-s">Source: ${esc(s.src)}</p>` : ''}<p class="sp-f">Visit Anaheim | visitanaheim.org<span>${i + 1}</span></p></div>`;
      }
      return `<figure class="sp" aria-label="Slide ${i + 1}: ${esc(s.title)}"><div class="sp-in">${b}</div><figcaption>${i + 1}. ${esc(s.title)}</figcaption></figure>`;
    };
    return `<p class="mk-cap">${sl.length} slides · 16:9 · charts are native PowerPoint charts you can edit</p><div class="sp-grid">${sl.map(one).join('')}</div>`;
  }
  const pptxFmt = c => { const t = (c.rows ? c.rows[0].t : ''), f = c.yfmt || {}; const m = t.match(/^([^\d−-]*)[−-]?[\d,]*(\.(\d+))?(.*)$/) || []; const dec = m[3] ? m[3].length : (f.dec || 0), pre = m[1] || f.pre || '', suf = (m[4] || f.suf || '').trim();
    return (pre ? `"${pre}"` : '') + (dec ? '#,##0.' + '0'.repeat(dec) : '#,##0') + (suf ? `"${suf}"` : ''); };
  async function buildPptx(st) {
    if (typeof PptxGenJS === 'undefined') throw Object.assign(new Error('unavailable'), { code: 'unavailable' });
    const H = { dark: '231F20', light: 'F9F9F2', e1: '43A3A3', e2: '77C7C9', e3: '125C60', e4: 'B4D9E3', white: 'FFFFFF' }, W = 13.333, M = 0.6;
    const pres = new PptxGenJS(); pres.layout = 'LAYOUT_WIDE'; pres.title = titleOf(st); pres.author = 'Visit Anaheim Business Intelligence'; pres.company = 'Visit Anaheim';
    pres.theme = { headFontFace: 'Proxima Nova', bodyFontFace: 'Proxima Nova' };
    const LG = LOGO.replace(/^data:/, '');
    pres.defineSlideMaster({ title: 'VA Title', background: { color: H.e3 }, objects: [] });
    pres.defineSlideMaster({ title: 'VA Content', background: { color: H.white }, objects: [
      { image: { x: W - M - 1.6, y: 0.3, w: 1.6, h: 1.6 / LOGO_AR, data: LG } },
      { line: { x: M, y: 7.0, w: W - 2 * M, h: 0, line: { color: H.e1, width: 1 } } },
      { text: { text: 'Visit Anaheim | visitanaheim.org', options: { x: M, y: 7.02, w: 6, h: 0.3, fontSize: 9, color: H.dark, margin: 0, fontFace: 'Proxima Nova' } } }],
      slideNumber: { x: W - M - 0.6, y: 7.02, w: 0.6, h: 0.3, fontSize: 9, color: H.dark, align: 'right' } });
    const ft = o => Object.assign({ isTextBox: true, margin: 0, fontFace: 'Proxima Nova' }, o);
    const head = (s, x) => { s.addText(x.title, ft({ x: M, y: 0.3, w: W - 2 * M - 2.0, h: 0.85, fontSize: 22, bold: true, color: H.e3, valign: 'top', fit: 'shrink' })); if (x.kicker) s.addText(x.kicker, ft({ x: M, y: 1.2, w: W - 2 * M - 2.0, h: 0.3, fontSize: 12, color: H.dark })); };
    const src = (s, t) => { if (t) s.addText('Source: ' + t, ft({ x: M, y: 6.45, w: W - 2 * M, h: 0.5, fontSize: 8.5, color: H.dark, valign: 'bottom', fit: 'shrink' })); };
    const kpis = (s, ks, x, y, w, h) => { const gap = 0.18, cw = (w - gap * (ks.length - 1)) / ks.length;
      ks.forEach((m, i) => { const cx = x + i * (cw + gap);
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx, y, w: cw, h, fill: { color: H.white }, line: { color: H.e4, width: 1 }, rectRadius: 0.08 });
        s.addText(m.where.toUpperCase(), ft({ x: cx + 0.16, y: y + 0.12, w: cw - 0.32, h: 0.25, fontSize: 8.5, bold: true, color: H.e3, charSpacing: 1, fit: 'shrink' }));
        s.addText(m.value, ft({ x: cx + 0.16, y: y + 0.4, w: cw - 0.32, h: 0.6, fontSize: m.value.length > 14 ? 18 : 26, bold: true, color: H.e3, fit: 'shrink' }));
        s.addText(m.label, ft({ x: cx + 0.16, y: y + 1.02, w: cw - 0.32, h: h - 1.1, fontSize: 10.5, bold: true, color: H.dark, valign: 'top', fit: 'shrink' })); }); };
    const chart = (s, c, x, y, w, h) => {
      s.addText(c.title, ft({ x, y, w, h: 0.5, fontSize: 12, bold: true, color: H.e3, valign: 'top', fit: 'shrink' }));
      const base = { x, y: y + 0.55, w, h: h - 0.55, catAxisLabelColor: H.dark, catAxisLabelFontSize: 10, catAxisLabelFontFace: 'Proxima Nova', valGridLine: { style: 'none' }, catGridLine: { style: 'none' },
        showValue: true, dataLabelColor: H.dark, dataLabelFontSize: 9.5, dataLabelFontBold: true, dataLabelFontFace: 'Proxima Nova', showLegend: false };
      if (c.kind === 'line') {
        const sr = c.series.find(q => q.focal) || c.series[0], f = c.yfmt || {}, code = (f.pre ? `"${f.pre}"` : '') + (f.dec ? '0.' + '0'.repeat(f.dec) : '0') + (f.suf ? `"${f.suf}"` : '');
        s.addChart(pres.charts.LINE, [{ name: sr.name, labels: c.x, values: sr.v }], Object.assign(base, { chartColors: [H.e1], lineSize: 3, lineDataSymbol: 'circle', lineDataSymbolSize: 6, valAxisHidden: c.x.length <= 8, showValue: c.x.length <= 8, valAxisLabelFormatCode: code, valAxisLabelFontSize: 9, valGridLine: c.x.length <= 8 ? { style: 'none' } : { color: 'D9D9D9', size: 0.5 }, dataLabelPosition: 't', dataLabelFormatCode: code }));
      } else {
        const colors = c.rows.map(r => r.fc ? H.e4 : r.hi ? H.e1 : (c.kind === 'cols' ? H.e1 : H.e4));
        s.addChart(pres.charts.BAR, [{ name: c.title, labels: c.rows.map(r => r.l + (r.fc ? ' (F)' : '')), values: c.rows.map(r => r.v) }], Object.assign(base, { barDir: c.kind === 'cols' ? 'col' : 'bar', chartColors: colors, invertedColors: colors,
          catAxisOrientation: c.kind === 'cols' ? 'minMax' : 'maxMin', valAxisHidden: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: pptxFmt(c), barGapWidthPct: 45 }));
      }
    };
    const bullets = (s, items, x, y, w, h, fs) => s.addText(items.map((t, i) => ({ text: t, options: { bullet: { indent: 14 }, paraSpaceAfter: 6, breakLine: i < items.length - 1 } })), ft({ x, y, w, h, fontSize: fs, color: H.dark, valign: 'top', fit: 'shrink' }));
    const table = (s, rows, y) => s.addTable([['Area and period', 'Measure', 'Value', 'Detail'].map(t => ({ text: t, options: { bold: true, color: H.white, fill: { color: H.e3 } } })),
      ...rows.map((m, i) => [m.where, m.label, m.value, m.detail].map((t, j) => ({ text: String(t), options: { bold: j === 2, color: j === 2 ? H.e3 : H.dark, fill: { color: i % 2 ? H.light : H.white } } })))],
      { x: M, y, w: W - 2 * M, colW: [2.6, 2.8, 1.9, W - 2 * M - 7.3], fontFace: 'Proxima Nova', fontSize: 10, border: { type: 'solid', pt: 0.5, color: H.e4 }, rowH: 0.42, valign: 'middle', margin: [0.04, 0.08, 0.04, 0.08] });
    slidesModel(st).forEach(x => {
      if (x.t === 'title') {
        const s = pres.addSlide({ masterName: 'VA Title' });
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 0.6, w: 2.6, h: 2.6 / LOGO_AR + 0.3, fill: { color: H.white }, line: { color: H.white }, rectRadius: 0.1 });
        s.addImage({ data: LG, x: M + 0.15, y: 0.75, w: 2.3, h: 2.3 / LOGO_AR });
        s.addText(x.title, ft({ x: M, y: 2.55, w: 11, h: 1.6, fontSize: 40, bold: true, italic: true, color: H.white, valign: 'top', fit: 'shrink' }));
        s.addText(x.sub, ft({ x: M, y: 4.25, w: 11, h: 0.6, fontSize: 18, color: H.white }));
        s.addText(PREP + ' · ' + x.date, ft({ x: M, y: 6.6, w: 11, h: 0.4, fontSize: 12, color: H.e4 }));
        return;
      }
      const s = pres.addSlide({ masterName: 'VA Content' }); head(s, x);
      if (x.t === 'sum') { if (x.kpis.length) kpis(s, x.kpis, M, 1.65, W - 2 * M, 1.75); bullets(s, x.bullets, M, x.kpis.length ? 3.6 : 1.7, W - 2 * M, 2.8, 12.5); }
      if (x.t === 'sec') {
        const lw = x.chart ? 6.3 : W - 2 * M;
        if (x.kpis.length) kpis(s, x.kpis, M, 1.65, lw, 1.75);
        s.addText(x.text, ft({ x: M, y: x.kpis.length ? 3.6 : 1.7, w: lw, h: 2.7, fontSize: 13, color: H.dark, valign: 'top', fit: 'shrink' }));
        if (x.chart) chart(s, x.chart, M + lw + 0.35, 1.65, W - 2 * M - lw - 0.35, 4.6);
      }
      if (x.t === 'chart') chart(s, x.chart, M, 1.65, W - 2 * M, 4.7);
      if (x.t === 'table') table(s, x.rows, 1.7);
      if (x.t === 'means') bullets(s, x.items.map(i => `${i.tag} (${i.tab}). ${i.text}`), M, 1.7, W - 2 * M, 4.6, 12.5);
      if (x.t === 'sources') { bullets(s, x.items, M, 1.7, W - 2 * M, 4.6, 11.5); }
      src(s, x.src);
    });
    return pres.write({ outputType: 'blob' });
  }

  /* ----- Design (SVG poster; PNG and PDF are rendered from it) ----- */
  const SIZES = { social: [1080, 1350], letter: [1275, 1650], wide: [1920, 1080] };
  function fontCss() {
    if (fontCss._c != null) return fontCss._c;
    let css = '';
    try { [...document.styleSheets].forEach(sh => { let rules; try { rules = sh.cssRules; } catch (_) { return; } [...rules].forEach(r => { if (r.type === 5 && /Sharp Sans/.test(r.cssText)) css += r.cssText + '\n'; }); }); } catch (_) {}
    return (fontCss._c = css);
  }
  function designSvg(st, embedFonts) {
    const [W, H] = SIZES[st.fmt] || SIZES.social, T = THEMES[st.theme] || THEMES.teal, wide = st.fmt === 'wide';
    const ms = featured(st, 6), ch = st.charts ? st.secs.map(id => chartsFor(id, st)[0]).find(Boolean) : null;
    const pad = Math.round(W * (wide ? 0.04 : 0.06)), u = wide ? H / 1080 : W / 1080;
    let g = `<rect width="${W}" height="${H}" fill="${T.bg}"/>`;
    // ribbon accent (Escapism)
    g += `<path d="M${W} 0 L${W} ${H * 0.34} C${W * 0.82} ${H * 0.22} ${W * 0.74} ${H * 0.1} ${W * 0.7} 0 Z" fill="${st.theme === 'light' ? VA.e4 : VA.e1}" opacity="${st.theme === 'light' ? 0.55 : 0.28}"/>`;
    const ph = Math.round(78 * u), pw = Math.round(ph * LOGO_AR * 0.92) + Math.round(28 * u);
    g += `<rect x="${pad}" y="${pad}" width="${pw}" height="${ph}" rx="${Math.round(12 * u)}" fill="${T.plate}"/><image href="${LOGO}" x="${pad + 14 * u}" y="${pad + 8 * u}" width="${pw - 28 * u}" height="${ph - 16 * u}" preserveAspectRatio="xMidYMid meet"/>`;
    const kx = W - pad, ky = pad + ph / 2;
    g += `<text x="${kx}" y="${ky - 6 * u}" text-anchor="end" font-size="${Math.round(20 * u)}" font-weight="700" letter-spacing="${2 * u}" fill="${T.kick}">OC VIBE INSIGHTS</text><text x="${kx}" y="${ky + 22 * u}" text-anchor="end" font-size="${Math.round(18 * u)}" font-weight="350" fill="${T.ink}">${xesc(ASOF)}</text>`;
    let y = pad + ph + Math.round(36 * u) + Math.round((wide ? 64 : 70) * u);
    const tw = W - 2 * pad, hs = Math.round((wide ? 64 : st.fmt === 'letter' ? 60 : 70) * u);
    const hl = wrap(titleOf(st), tw, hs, 900, 3);
    hl.forEach((l, i) => { g += `<text x="${pad}" y="${y + i * hs * 1.08}" font-size="${hs}" font-weight="900" font-style="oblique" fill="${T.ink}">${xesc(l)}</text>`; });
    y += (hl.length - 1) * hs * 1.08 + Math.round(48 * u);
    const sl = wrap(subOf(st), tw, Math.round(28 * u), 350, 2);
    sl.forEach((l, i) => { g += `<text x="${pad}" y="${y + i * 36 * u}" font-size="${Math.round(28 * u)}" font-weight="350" fill="${T.muted}">${xesc(l)}</text>`; });
    y += (sl.length - 1) * 36 * u + Math.round(44 * u);
    // footer
    const fs = Math.round(15 * u), srcs = srcList(ms.map(m => m.src).concat(ch ? [ch.src] : [])), fl = wrap('Sources: ' + (srcs.join('; ') || 'OC Vibe Insights'), tw, fs, 350, wide ? 2 : 3);
    const fy = H - pad - fl.length * fs * 1.35 - Math.round(34 * u);
    g += `<line x1="${pad}" x2="${W - pad}" y1="${fy}" y2="${fy}" stroke="${T.kick}" stroke-width="${2 * u}"/>`;
    fl.forEach((l, i) => { g += `<text x="${pad}" y="${fy + Math.round(30 * u) + i * fs * 1.35}" font-size="${fs}" fill="${T.muted}">${xesc(l)}</text>`; });
    g += `<text x="${pad}" y="${H - pad + 4 * u}" font-size="${Math.round(17 * u)}" font-weight="700" fill="${T.ink}">${xesc(PREP)} · ${CONTACT}</text>`;
    // body regions
    const bodyH = fy - Math.round(30 * u) - y;
    let gx = pad, gw = tw, chartBox = null;
    if (ch && wide) { gw = Math.round(tw * 0.52); chartBox = [pad + gw + Math.round(40 * u), y, tw - gw - Math.round(40 * u), bodyH]; }
    else if (ch && (ms.length <= 4 || st.fmt === 'letter')) { const chH = Math.round(bodyH * (ms.length ? 0.38 : 1)); chartBox = [pad, fy - Math.round(30 * u) - chH, tw, chH]; }
    const gridH = chartBox && !wide ? chartBox[1] - y - Math.round(28 * u) : bodyH;
    if (ms.length && gridH > 120 * u) {
      const cols = wide ? 2 : 2, rows = Math.ceil(ms.length / cols), gap = Math.round(22 * u), cw = (gw - gap * (cols - 1)) / cols, rh = Math.min((gridH - gap * (rows - 1)) / rows, 240 * u);
      ms.forEach((m, i) => {
        const cx = gx + (i % cols) * (cw + gap), cy = y + Math.floor(i / cols) * (rh + gap), ip = Math.round(22 * u);
        g += `<rect x="${cx}" y="${cy}" width="${cw}" height="${rh}" rx="${Math.round(14 * u)}" fill="${T.card}" stroke="${T.cardLine}" stroke-width="${1.5 * u}"/>`;
        g += `<text x="${cx + ip}" y="${cy + ip + 14 * u}" font-size="${Math.round(15 * u)}" font-weight="700" letter-spacing="${1.2 * u}" fill="${T.kick}">${xesc(wrap(m.where.toUpperCase(), cw - 2 * ip, Math.round(15 * u), 700, 1)[0])}</text>`;
        // label sits on the tile's bottom padding; the value takes the space between the area line and the label
        const ll = wrap(m.label, cw - 2 * ip, Math.round(19 * u), 700, rh > 190 * u ? 2 : 1), lb = cy + rh - ip - (ll.length - 1) * 24 * u;
        const room = lb - 24 * u - (cy + ip + 26 * u), vs = fitSize(m.value, cw - 2 * ip, Math.round(Math.max(24 * u, Math.min(64 * u, room * 0.9))), 750, Math.round(22 * u));
        g += `<text x="${cx + ip}" y="${(cy + ip + 26 * u + (room + vs) / 2).toFixed(1)}" font-size="${vs}" font-weight="750" fill="${T.value}">${xesc(m.value)}</text>`;
        ll.forEach((l, k) => { g += `<text x="${cx + ip}" y="${(lb + k * 24 * u).toFixed(1)}" font-size="${Math.round(19 * u)}" font-weight="700" fill="${T.ink}">${xesc(l)}</text>`; });
      });
    }
    if (chartBox) {
      const [cx, cy, cw, chh] = chartBox, ts = Math.round(21 * u), tl = wrap(ch.title, cw, ts, 700, 2);
      tl.forEach((l, i) => { g += `<text x="${cx}" y="${cy + ts + i * ts * 1.2}" font-size="${ts}" font-weight="700" fill="${T.ink}">${xesc(l)}</text>`; });
      const oy = cy + ts * 1.2 * tl.length + 16 * u, ih = chh - (oy - cy);
      if (ih > 80 * u) { const inner = chartSvg(ch, Math.round(cw), Math.round(ih), T, Math.round(17 * u)); g += inner.replace('<svg ', `<svg x="${cx}" y="${oy}" `); }
    }
    const style = embedFonts ? `<style>${fontCss()}</style>` : '';
    return { w: W, h: H, svg: `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family='${FONT}' role="img" aria-label="${xesc(titleOf(st) + '. ' + ms.map(m => m.where + ': ' + m.label + ' ' + m.value).join('; '))}">${style}${g}</svg>` };
  }
  function svgToPng(svg, w, h, scale = 1) {
    return new Promise((res, rej) => {
      const img = new Image(); img.onload = () => { try { const c = document.createElement('canvas'); c.width = w * scale; c.height = h * scale; const x = c.getContext('2d'); x.scale(scale, scale); x.drawImage(img, 0, 0, w, h); c.toBlob(b => b ? res(b) : rej(new Error('png')), 'image/png'); } catch (e) { rej(e); } };
      img.onerror = rej; img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
    });
  }
  async function designPdf(st) {
    if (typeof PDFLib === 'undefined') throw Object.assign(new Error('unavailable'), { code: 'unavailable' });
    const d = designSvg(st, true), png = await svgToPng(d.svg, d.w, d.h, 2);
    const doc = await PDFLib.PDFDocument.create(); doc.setTitle(titleOf(st)); doc.setAuthor('Visit Anaheim Business Intelligence'); doc.setCreator('OC Vibe Insights');
    const im = await doc.embedPng(await png.arrayBuffer()), pw = st.fmt === 'letter' ? 612 : d.w * 0.75, ph = st.fmt === 'letter' ? 792 : d.h * 0.75;
    doc.addPage([pw, ph]).drawImage(im, { x: 0, y: 0, width: pw, height: ph });
    return new Blob([await doc.save()], { type: 'application/pdf' });
  }

  function pageHtml(title, body, css) {
    return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${xesc(title)}</title><meta name="generator" content="OC Vibe Insights, Visit Anaheim BI"><style>${fontCss()}\n${css}</style></head><body>${body}</body></html>`;
  }
  const DOC_CSS = `body{margin:0;background:${VA.light};color:${VA.dark};font-family:${FONT};font-weight:350;line-height:1.5}.mk-paper{max-width:860px;margin:24px auto;background:#fff;padding:40px 48px;border-top:6px solid ${VA.e3}}
@media (max-width:700px){.mk-paper{padding:22px 16px}}h1{font-size:34px;font-weight:900;font-style:oblique;color:${VA.e3};margin:4px 0}h2{font-size:22px;color:${VA.e3};margin:28px 0 6px;font-weight:750}h3{font-size:16px;color:${VA.e3}}
.mkd-h{display:flex;gap:20px;align-items:center;border-bottom:3px solid ${VA.e1};padding-bottom:14px}.mkd-logo{width:150px}.mkd-kick{font-size:12.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:${VA.e3};margin:0}.mkd-sub{margin:0}
.mkd-t{width:100%;border-collapse:collapse;font-size:14px;margin:10px 0}.mkd-t caption{text-align:left;font-weight:700;color:${VA.e3};padding-bottom:4px}.mkd-t th{background:${VA.e3};color:#fff;text-align:left;padding:7px}.mkd-t td{border-bottom:1px solid ${VA.e4};padding:7px;vertical-align:top}.mkd-t .n{text-align:right;white-space:nowrap}
.mkd-src{display:block;font-size:12px;font-style:italic;color:#4A4546}.mkd-f{margin:14px 0}.mkd-f figcaption{display:flex;flex-direction:column}.mkd-f figcaption span{font-size:13px}.mkd-f svg{width:100%;height:auto}.mkd-foot{font-size:12.5px;border-top:1px solid ${VA.e4};padding-top:10px;margin-top:24px}
b.kv{color:${VA.e3}}.mk-tx{fill:${VA.dark}}.mk-mu{fill:#4A4546}.mk-b{fill:${VA.e2}}.mk-bh,.mk-pt{fill:${VA.e3}}.mk-fc{fill:rgba(67,163,163,.25);stroke:${VA.e1}}.mk-gr{stroke:#D9D6CE}.mk-ln{stroke:${VA.e3}}`;

  /* ----- Word (.docx) built with JSZip: headings, tables, chart images, sources ----- */
  async function buildDocx(st) {
    if (typeof JSZip === 'undefined') throw Object.assign(new Error('unavailable'), { code: 'unavailable' });
    const d = docModel(st), z = new JSZip(), media = [];
    const X = s => xesc(s).replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, '');
    const run = (t, o = {}) => `<w:r><w:rPr>${o.b ? '<w:b/>' : ''}${o.i ? '<w:i/>' : ''}${o.c ? `<w:color w:val="${o.c}"/>` : ''}${o.sz ? `<w:sz w:val="${o.sz}"/><w:szCs w:val="${o.sz}"/>` : ''}${o.f ? `<w:rFonts w:ascii="${o.f}" w:hAnsi="${o.f}" w:cs="${o.f}"/>` : ''}</w:rPr><w:t xml:space="preserve">${X(t)}</w:t></w:r>`;
    const runsKv = (t, base = {}) => { const out = []; let last = 0; String(t).replace(KV_RX, (m, off, str) => { if (!m.trim() || !kvKeep(m)) return m; const pv = str.slice(Math.max(0, off - 10), off); if (/(Route |Q|SR-|I-|No\. |District |Line |Phase |Lot |Dock )$/.test(pv) || /[A-Za-z]$/.test(pv)) return m; const lead = m.match(/^\s*/)[0].length; if (off + lead > last) out.push(run(str.slice(last, off + lead), base)); out.push(run(m.slice(lead), Object.assign({}, base, { b: true, c: '125C60' }))); last = off + m.length; return m; }); if (last < String(t).length) out.push(run(String(t).slice(last), base)); return out.join(''); };
    const P = (inner, style, extra = '') => `<w:p><w:pPr>${style ? `<w:pStyle w:val="${style}"/>` : ''}${extra}</w:pPr>${inner}</w:p>`;
    const bullet = inner => P(inner, 'ListBullet');
    const cellX = (inner, o = {}) => `<w:tc><w:tcPr>${o.w ? `<w:tcW w:w="${o.w}" w:type="dxa"/>` : ''}${o.fill ? `<w:shd w:val="clear" w:color="auto" w:fill="${o.fill}"/>` : ''}</w:tcPr>${P(inner, null, o.r ? '<w:jc w:val="right"/>' : '')}</w:tc>`;
    const tbl = (cols, rows, widths) => `<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:tblBorders>${['top', 'left', 'bottom', 'right', 'insideH', 'insideV'].map(k => `<w:${k} w:val="single" w:sz="4" w:space="0" w:color="B4D9E3"/>`).join('')}</w:tblBorders><w:tblCellMar><w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>${widths.map(w => `<w:gridCol w:w="${w}"/>`).join('')}</w:tblGrid>
      <w:tr><w:trPr><w:tblHeader/></w:trPr>${cols.map((c, j) => cellX(run(c[0], { b: true, c: 'FFFFFF', sz: 19 }), { w: widths[j], fill: '125C60', r: c[1] })).join('')}</w:tr>
      ${rows.map((r, i) => `<w:tr>${r.map((c, j) => cellX(Array.isArray(c) ? c.join('') : run(c, { sz: 19, b: cols[j][1] }), { w: widths[j], fill: i % 2 ? 'F9F9F2' : null, r: cols[j][1] })).join('')}</w:tr>`).join('')}</w:tbl>${P('')}`;
    let rid = 10;
    const img = async (svgOrPng, w, h, name, alt) => { const b = svgOrPng instanceof Blob ? svgOrPng : await svgToPng(svgOrPng, w, h, 2); const id = ++rid, fn = `image${id}.png`; z.file('word/media/' + fn, b); media.push([id, fn]);
      const cx = Math.round(Math.min(6.3, w / 120) * 914400), cy = Math.round(cx * h / w);
      return P(`<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="${cx}" cy="${cy}"/><wp:docPr id="${id}" name="${X(name)}" descr="${X(alt)}"/><wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="${id}" name="${fn}" descr="${X(alt)}"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="rId${id}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="${cx}" cy="${cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>`); };
    const logoBlob = await (await fetch(LOGO)).blob();
    let body = await img(logoBlob, 240, 240 / LOGO_AR, 'Visit Anaheim logo', 'Visit Anaheim');
    body += P(run('OC VIBE INSIGHTS · ' + d.date.toUpperCase(), { b: true, c: '125C60', sz: 18 }));
    body += P(run(d.title), 'Title') + P(run(d.sub, { c: '231F20' }), 'Subtitle');
    body += P(run('Summary'), 'Heading1') + d.summary.map(x => bullet(run(x.tab + ': ', { b: true }) + runsKv(x.ans))).join('');
    for (const s of d.secs) {
      body += P(run(s.tab.toUpperCase() + ' · ' + s.period, { b: true, c: '125C60', sz: 17 }), null, '<w:spacing w:before="320"/>') + P(run(s.head), 'Heading1') + P(runsKv(s.nut || s.lede));
      if (s.ms.length) { body += P(run('Key figures'), 'Heading2'); body += tbl([['Area and period', 0], ['Measure', 0], ['Value', 1], ['Detail and source', 0]], s.ms.map(m => [m.where, m.label, m.value, [run(m.detail, { sz: 19 }), run(' Source: ' + m.src, { sz: 16, i: true })]]), [1900, 2100, 1400, 4200]); }
      for (const c of s.charts) { const ww = 760, hh = c.kind === 'bars' ? Math.max(140, c.rows.length * 34) : 300; body += P(run(c.title, { b: true, c: '125C60' })) + (c.sub ? P(run(c.sub, { sz: 18 })) : '') + await img(chartSvg(c, ww, hh, THEMES.light, 14), ww, hh, c.title, c.title + '. ' + chartAlt(c)) + P(run('Source: ' + (c.src || s.period), { i: true, sz: 16 })); }
      if (s.means.length) { body += P(run('What it means for OC Vibe'), 'Heading2') + s.means.map(x => bullet(run(x.tag + '. ', { b: true }) + runsKv(x.text) + run(' (' + x.src + ')', { i: true, sz: 17 }))).join(''); }
    }
    body += P(run('Sources'), 'Heading1') + d.sources.map((x, i) => P(run(`${i + 1}. ${x}`, { sz: 18 }))).join('');
    body += P(run(`${PREP} · ${d.date} · ${ASOF} · ${CONTACT}. Figures are as published by each source; the full tables and source files are in the OC Vibe Insights app.`, { sz: 17, i: true }), null, '<w:spacing w:before="320"/>');
    const NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"';
    z.file('word/document.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document ${NS}><w:body>${body}<w:sectPr><w:footerReference w:type="default" r:id="rId3"/><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" w:header="540" w:footer="540" w:gutter="0"/></w:sectPr></w:body></w:document>`);
    z.file('word/footer1.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr ${NS}><w:p><w:pPr><w:pBdr><w:top w:val="single" w:sz="6" w:space="4" w:color="43A3A3"/></w:pBdr><w:tabs><w:tab w:val="right" w:pos="10080"/></w:tabs></w:pPr>${run('Visit Anaheim | visitanaheim.org', { sz: 16 })}<w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:tab/></w:r><w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r><w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>`);
    const st_ = (id, name, rp, pp = '', based = 'Normal') => `<w:style w:type="paragraph" w:styleId="${id}"><w:name w:val="${name}"/><w:basedOn w:val="${based}"/><w:qFormat/><w:pPr>${pp}</w:pPr><w:rPr>${rp}</w:rPr></w:style>`;
    z.file('word/styles.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Proxima Nova" w:hAnsi="Proxima Nova" w:cs="Proxima Nova" w:eastAsia="Proxima Nova"/><w:color w:val="231F20"/><w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="en-US"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
      <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
      ${st_('Title', 'Title', '<w:rFonts w:ascii="Sharp Sans Display No. 2" w:hAnsi="Sharp Sans Display No. 2"/><w:b/><w:i/><w:color w:val="125C60"/><w:sz w:val="52"/><w:szCs w:val="52"/>', '<w:spacing w:after="60"/>')}
      ${st_('Subtitle', 'Subtitle', '<w:sz w:val="24"/>', '<w:pBdr><w:bottom w:val="single" w:sz="12" w:space="6" w:color="43A3A3"/></w:pBdr><w:spacing w:after="240"/>')}
      ${st_('Heading1', 'heading 1', '<w:rFonts w:ascii="Sharp Sans Display No. 2" w:hAnsi="Sharp Sans Display No. 2"/><w:b/><w:color w:val="125C60"/><w:sz w:val="32"/><w:szCs w:val="32"/>', '<w:keepNext/><w:spacing w:before="200" w:after="100"/><w:outlineLvl w:val="0"/>')}
      ${st_('Heading2', 'heading 2', '<w:b/><w:color w:val="125C60"/><w:sz w:val="24"/><w:szCs w:val="24"/>', '<w:keepNext/><w:spacing w:before="200" w:after="80"/><w:outlineLvl w:val="1"/>')}
      ${st_('ListBullet', 'List Bullet', '', '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr><w:ind w:left="360" w:hanging="360"/>')}</w:styles>`);
    z.file('word/numbering.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="360" w:hanging="360"/></w:pPr><w:rPr><w:color w:val="43A3A3"/></w:rPr></w:lvl></w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>`);
    z.file('word/_rels/document.xml.rels', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>${media.map(([id, fn]) => `<Relationship Id="rId${id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/${fn}"/>`).join('')}</Relationships>`);
    z.file('[Content_Types].xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/><Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>`);
    z.file('_rels/.rels', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>`);
    z.file('docProps/core.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>${X(d.title)}</dc:title><dc:creator>Visit Anaheim Business Intelligence</dc:creator><cp:lastModifiedBy>Visit Anaheim Business Intelligence</cp:lastModifiedBy></cp:coreProperties>`);
    return z.generateAsync({ type: 'blob', compression: 'DEFLATE', mimeType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
  }

  /* ----- Motion: a canvas timeline (deterministic for a given time), recorded with MediaRecorder ----- */
  function motionScenes(st) {
    const ms = featured(st, 8), out = [{ k: 'intro', d: 3.2 }];
    ms.forEach(m => out.push({ k: 'stat', m, d: 3.4 }));
    if (st.charts) st.secs.map(id => chartsFor(id, st)[0]).filter(c => c && c.kind !== 'line' && c.rows.length <= 9).slice(0, 2).forEach(c => out.push({ k: 'chart', c, d: 4.2 }));
    out.push({ k: 'outro', d: 3.6 });
    let t = 0; out.forEach(s => { s.t0 = t; t += s.d; });
    return { scenes: out, dur: t };
  }
  const ease = x => x < 0 ? 0 : x > 1 ? 1 : 1 - Math.pow(1 - x, 3);
  function countText(v, p) {
    const m = String(v).match(/^([^\d]*?)(\d[\d,]*\.?\d*)(.*)$/); if (!m) return v;
    const num = parseFloat(m[2].replace(/,/g, '')), dec = (m[2].split('.')[1] || '').length, comma = /,/.test(m[2]) || num >= 10000;
    const cur = num * p; let s = cur.toFixed(dec); if (comma) s = (+s).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
    return m[1] + s + m[3];
  }
  let logoImg = null; const getLogo = () => { if (!logoImg && LOGO) { logoImg = new Image(); logoImg.src = LOGO; } return logoImg; };
  function drawFrame(ctx, st, sc, t) {
    const W = 1920, H = 1080, T = THEMES[st.theme] || THEMES.teal, pad = 110;
    const s = sc.scenes.find(x => t >= x.t0 && t < x.t0 + x.d) || sc.scenes[sc.scenes.length - 1], lt = Math.min(t - s.t0, s.d);
    const inA = ease(lt / 0.6), outA = 1 - ease((lt - (s.d - 0.45)) / 0.45), a = Math.max(0, Math.min(inA, outA)), dy = (1 - inA) * 40;
    ctx.save(); ctx.fillStyle = T.bg; ctx.fillRect(0, 0, W, H);
    ctx.globalAlpha = st.theme === 'light' ? 0.55 : 0.28; ctx.fillStyle = st.theme === 'light' ? VA.e4 : VA.e1;
    ctx.beginPath(); ctx.moveTo(W, 0); ctx.lineTo(W, H * 0.4); ctx.bezierCurveTo(W * 0.84, H * 0.26, W * 0.76, H * 0.12, W * 0.72, 0); ctx.closePath(); ctx.fill(); ctx.globalAlpha = 1;
    const lg = getLogo(), ph = 84, pw = ph * LOGO_AR * 0.92 + 28;
    ctx.fillStyle = T.plate; rr(ctx, pad, 70, pw, ph, 12); ctx.fill(); if (lg && lg.complete) ctx.drawImage(lg, pad + 14, 78, pw - 28, ph - 16);
    ctx.textBaseline = 'alphabetic'; ctx.fillStyle = T.kick; ctx.textAlign = 'right'; ctx.font = `700 22px ${FONT}`; ctx.fillText('OC VIBE INSIGHTS', W - pad, 104); ctx.fillStyle = T.ink; ctx.font = `350 20px ${FONT}`; ctx.fillText(ASOF, W - pad, 134); ctx.textAlign = 'left';
    ctx.globalAlpha = a; ctx.translate(0, dy);
    const lines = (txt, x, y, mw, size, wt, col, lh, max, style = '') => { const l = wrap(txt, mw, size, wt, max); ctx.fillStyle = col; ctx.font = `${style}${wt} ${size}px ${FONT}`; l.forEach((q, i) => ctx.fillText(q, x, y + i * size * lh)); return l.length; };
    if (s.k === 'intro') {
      const n = lines(titleOf(st), pad, 430, W - 2 * pad, 96, 900, T.ink, 1.06, 3, 'oblique ');
      lines(subOf(st), pad, 430 + (n - 1) * 102 + 90, W - 2 * pad, 38, 350, T.muted, 1.3, 2);
      ctx.fillStyle = T.kick; ctx.fillRect(pad, 300, Math.min(1, lt / 1.2) * 240, 8);
    } else if (s.k === 'stat') {
      const m = s.m, p = ease((lt - 0.2) / 1.3);
      ctx.fillStyle = T.kick; ctx.font = `700 30px ${FONT}`; ctx.fillText((m.where.toLowerCase().startsWith(SEC[m.sec].tab.toLowerCase()) ? m.where : m.where + ' · ' + SEC[m.sec].tab).toUpperCase(), pad, 330);
      const vs = fitSize(m.value, W - 2 * pad, 190, 750, 70); ctx.fillStyle = T.value; ctx.font = `750 ${vs}px ${FONT}`; ctx.fillText(countText(m.value, p), pad, 330 + vs + 20);
      const n = lines(m.label, pad, 330 + vs + 110, W - 2 * pad, 52, 700, T.ink, 1.15, 2);
      lines(m.detail, pad, 330 + vs + 110 + n * 60 + 30, W - 2 * pad, 32, 350, T.muted, 1.3, 2);
      lines('Source: ' + m.src, pad, H - 150, W - 2 * pad, 22, 350, T.muted, 1.35, 2);
    } else if (s.k === 'chart') {
      const c = s.c, n = lines(c.title, pad, 300, W - 2 * pad, 50, 750, T.ink, 1.15, 2); lines(c.sub || '', pad, 300 + n * 58 + 4, W - 2 * pad, 26, 350, T.muted, 1.3, 1);
      const top = 300 + n * 58 + 60, bh = H - 190 - top, rows = c.rows, max = Math.max(...rows.map(r => r.v)) || 1, p = ease((lt - 0.3) / 1.6);
      if (c.kind === 'bars') {
        const rh = bh / rows.length, lw = 520; ctx.font = `350 28px ${FONT}`;
        rows.forEach((r, i) => { const y = top + i * rh, h = Math.min(rh * 0.62, 56), w = (W - 2 * pad - lw - 200) * Math.max(0, r.v) / max * p;
          ctx.fillStyle = T.ink; ctx.textAlign = 'right'; ctx.font = `350 28px ${FONT}`; ctx.fillText(wrap(r.l, lw - 30, 28, 350, 1)[0], pad + lw - 24, y + rh / 2 + 10); ctx.textAlign = 'left';
          ctx.fillStyle = r.hi ? T.hi : T.bar; rr(ctx, pad + lw, y + (rh - h) / 2, Math.max(3, w), h, 4); ctx.fill();
          ctx.globalAlpha = a * ease((lt - 1.2) / 0.5); ctx.fillStyle = T.ink; ctx.font = `700 28px ${FONT}`; ctx.fillText(r.t, pad + lw + w + 14, y + rh / 2 + 10); ctx.globalAlpha = a; });
      } else {
        const cw = (W - 2 * pad) / rows.length;
        rows.forEach((r, i) => { const h = (bh - 70) * Math.max(0, r.v) / max * p, x = pad + i * cw + cw * 0.18, w = cw * 0.64, y = top + bh - 40 - h;
          ctx.fillStyle = r.fc ? T.fc : r.hi ? T.hi : T.bar; rr(ctx, x, y, w, h, 4); ctx.fill();
          ctx.textAlign = 'center'; ctx.fillStyle = T.muted; ctx.font = `350 24px ${FONT}`; ctx.fillText(r.l + (r.fc ? ' (F)' : ''), x + w / 2, top + bh);
          ctx.globalAlpha = a * ease((lt - 1.2) / 0.5); ctx.fillStyle = T.ink; ctx.font = `700 26px ${FONT}`; ctx.fillText(r.t, x + w / 2, y - 12); ctx.globalAlpha = a; ctx.textAlign = 'left'; });
      }
      lines('Source: ' + (c.src || ''), pad, H - 130, W - 2 * pad, 22, 350, T.muted, 1.35, 2);
    } else {
      lines('Explore the data', pad, 420, W - 2 * pad, 96, 900, T.ink, 1.06, 1, 'oblique ');
      lines('Every figure, its source and the full reports are in the OC Vibe Insights app.', pad, 520, W - 2 * pad - 200, 40, 350, T.muted, 1.3, 2);
      ctx.fillStyle = T.ink; ctx.font = `700 34px ${FONT}`; ctx.fillText(PREP, pad, 720); ctx.fillStyle = T.kick; ctx.fillText(CONTACT, pad, 772);
    }
    ctx.restore();
    // progress
    ctx.fillStyle = T.grid; ctx.fillRect(pad, H - 70, W - 2 * pad, 6); ctx.fillStyle = T.kick; ctx.fillRect(pad, H - 70, (W - 2 * pad) * Math.min(1, t / sc.dur), 6);
  }
  function rr(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
  function motionShell() {
    return `<div class="mk-mot"><canvas id="mkCanvas" width="1920" height="1080" role="img" aria-label="Animated video preview"></canvas>
      <div class="mk-mctl"><button type="button" class="ctl accent" id="mkPlay">Play</button><button type="button" class="ctl" id="mkRestart">Restart</button><label class="sr" for="mkScrub">Position</label><input type="range" id="mkScrub" min="0" max="1000" value="0"><span id="mkTime">0:00</span></div>
      <ol class="mk-scenes" id="mkScenes"></ol></div><p class="mk-cap" id="mkMcap"></p>`;
  }
  function motionPlayer(cv, st, interactive) {
    const ctx = cv.getContext('2d'), sc = motionScenes(st), reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let t = reduce ? Math.min(2.4, sc.dur) : 0, raf = 0, last = 0, playing = false;
    const mmss = x => `${Math.floor(x / 60)}:${String(Math.floor(x % 60)).padStart(2, '0')}`;
    const paint = () => { drawFrame(ctx, st, sc, t); if (interactive) { $('mkScrub').value = Math.round(t / sc.dur * 1000); $('mkTime').textContent = `${mmss(t)} of ${mmss(sc.dur)}`; } };
    const loop = ts => { if (!playing) return; if (last) t += (ts - last) / 1000; last = ts; if (t >= sc.dur) { t = sc.dur - 0.001; playing = false; setBtn(); } paint(); if (playing) raf = requestAnimationFrame(loop); };
    const setBtn = () => { if (interactive) $('mkPlay').textContent = playing ? 'Pause' : 'Play'; };
    const play = () => { if (t >= sc.dur - 0.01) t = 0; playing = true; last = 0; setBtn(); raf = requestAnimationFrame(loop); };
    const pause = () => { playing = false; cancelAnimationFrame(raf); setBtn(); };
    if (interactive) {
      $('mkPlay').onclick = () => playing ? pause() : play();
      $('mkRestart').onclick = () => { t = 0; paint(); if (!reduce) play(); };
      $('mkScrub').oninput = e => { pause(); t = +e.target.value / 1000 * sc.dur; paint(); };
      $('mkScenes').innerHTML = sc.scenes.map((s, i) => `<li><button type="button" class="chip" data-t="${s.t0 + Math.min(1.6, s.d / 2)}">${i + 1}. ${esc(s.k === 'intro' ? 'Title' : s.k === 'outro' ? 'Closing' : s.k === 'stat' ? s.m.value + ' ' + s.m.label : s.c.title)}</button></li>`).join('');
      $('mkScenes').onclick = e => { const b = e.target.closest('[data-t]'); if (b) { pause(); t = +b.dataset.t; paint(); } };
      $('mkMcap').textContent = `1920 × 1080 · ${sc.scenes.length} scenes · ${mmss(sc.dur)} · ${THEMES[st.theme].name} colors${reduce ? ' · motion is paused because your device asks for reduced motion; press Play to watch' : ''}`;
    }
    const lg = getLogo(); const go = () => { paint(); if (interactive && !reduce) play(); };
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => lg && !lg.complete ? (lg.onload = go) : go());
    return { stop: pause, sc };
  }
  function recordVideo(st, onProgress) {
    return new Promise((res, rej) => {
      if (typeof MediaRecorder === 'undefined' || !HTMLCanvasElement.prototype.captureStream) return rej(Object.assign(new Error('unavailable'), { code: 'novideo' }));
      const cv = document.createElement('canvas'); cv.width = 1920; cv.height = 1080; const ctx = cv.getContext('2d'), sc = motionScenes(st);
      const type = ['video/mp4;codecs=avc1', 'video/webm;codecs=vp9', 'video/webm;codecs=vp8', 'video/webm'].find(x => MediaRecorder.isTypeSupported(x));
      if (!type) return rej(Object.assign(new Error('unavailable'), { code: 'novideo' }));
      const stream = cv.captureStream(30), rec = new MediaRecorder(stream, { mimeType: type, videoBitsPerSecond: 6e6 }), parts = [];
      rec.ondataavailable = e => e.data && e.data.size && parts.push(e.data);
      rec.onstop = () => res({ blob: new Blob(parts, { type: type.split(';')[0] }), ext: /mp4/.test(type) ? 'mp4' : 'webm' });
      rec.onerror = rej;
      drawFrame(ctx, st, sc, 0); rec.start(500);
      const t0 = performance.now();
      const tick = () => { const t = (performance.now() - t0) / 1000; drawFrame(ctx, st, sc, Math.min(t, sc.dur - 0.001)); onProgress && onProgress(t, sc.dur); if (t < sc.dur + 0.3) setTimeout(tick, 1000 / 30); else rec.stop(); };
      tick();
    });
  }

  /* ---------- saving: one Save button for every kind ---------- */
  async function save(btn) {
    if (!pagesOK()) { toast('Choose at least one section first.'); return; }
    const t = ST.tool, f = fmtOf(), ids = ST.pages.slice(), all = ids.length === EXP_PAGES.length;
    if (t === 'link') { const u = shareUrl(ids), ok = await copyText(u, $('xpLink')); toast(ok ? 'Link copied: ' + u : 'Copy the link from the box.'); if (ok) close(); return; }
    const lab = btn.textContent; btn.disabled = true; btn.textContent = 'Preparing…';
    const suffix = all ? '' : '-' + (ids.length === 1 ? ids[0].replace('p-', '') : 'selected');
    try {
      if (t === 'report' && f === 'pptx') {
        const deck = b64Blob(ATTACH.deck, 'application/vnd.openxmlformats-officedocument.presentationml.presentation');
        if (all) await saveBlob(deck, 'OC_Vibe_Insights.pptx');
        else { if (typeof JSZip === 'undefined' || typeof pptxSubset === 'undefined') throw Object.assign(new Error('unavailable'), { code: 'unavailable' }); await saveBlob(await pptxSubset(JSZip, await deck.arrayBuffer(), deckSections(ids)), `OC_Vibe_Insights${suffix}.pptx`); }
      } else if (t === 'report') await saveBlob(await buildPdf(ids, all), `OC_Vibe_Insights${suffix}.pdf`);
      else if (t === 'data' && f === 'xlsx') await saveBlob(await xlsxFor(ids), `OC_Vibe_Insights_data${suffix}.xlsx`);
      else if (t === 'data') await saveBlob(new Blob(['﻿' + csvFor(ids).join('\r\n')], { type: 'text/csv' }), `OC_Vibe_Insights_data${suffix}.csv`);
      else await makeFile(t, f, btn);
      toast('Saved. It reflects your current choices.');
    } catch (err) { if (err && err.code === 'novideo') toast('This browser cannot record video. Save a still image, or try Chrome, Edge or Safari.'); else { console.error(err); dlError(err, 'Export'); } }
    finally { btn.disabled = false; btn.textContent = lab; syncControls(); }
  }
  async function makeFile(tool, fmt, btn, st = ST) {
    await (document.fonts ? document.fonts.ready : null);
    const name = slug(st);
    if (tool === 'doc') {
      if (fmt === 'docx') await saveBlob(await buildDocx(st), name + '_brief.docx');
      else if (fmt === 'md') await saveBlob(new Blob([docMd(st)], { type: 'text/markdown' }), name + '_brief.md');
      else await saveBlob(new Blob([pageHtml(titleOf(st), `<div class="mk-paper">${docHtml(st)}</div>`, DOC_CSS)], { type: 'text/html' }), name + '_brief.html');
    } else if (tool === 'slides') await saveBlob(await buildPptx(st), name + '_slides.pptx');
    else if (tool === 'design') {
      const d = designSvg(st, true), base = `${name}_${st.fmt}_${st.theme}`;
      if (fmt === 'svg') await saveBlob(new Blob([d.svg], { type: 'image/svg+xml' }), base + '.svg');
      else if (fmt === 'pdf') await saveBlob(await designPdf(st), base + '.pdf');
      else await saveBlob(await svgToPng(d.svg, d.w, d.h, st.fmt === 'letter' ? 2 : 1), base + '.png');
    } else if (tool === 'motion') {
      if (fmt === 'png') { const cv = document.createElement('canvas'); cv.width = 1920; cv.height = 1080; const sc = motionScenes(st); drawFrame(cv.getContext('2d'), st, sc, Math.min(2.4, sc.dur)); await saveBlob(await new Promise(r => cv.toBlob(r, 'image/png')), name + '_still.png'); }
      else { const v = await recordVideo(st, (t, d) => { if (btn) btn.textContent = `Recording ${Math.min(100, Math.round(t / d * 100))}%…`; }); await saveBlob(v.blob, name + '_motion.' + v.ext); }
    }
  }

  /* old links to the Make page open the Export panel */
  const h0 = (location.hash || '').slice(1), m0 = h0.match(/^(make|export)(?:\/(\w+))?/);
  if (m0) { const tl = m0[2] === 'dash' ? 'doc' : m0[2]; setTimeout(() => open(TOOL[tl] ? tl : null), 0); }
})();
