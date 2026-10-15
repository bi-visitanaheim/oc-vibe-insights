/* AntV visual layer (Oct. 14, 2026)
   G2 v5 charts, T8 narrative text, AntV Infographic and X6 diagrams, all inlined (no network), in the VA Branded palette,
   redrawn for light and dark mode. Runs after app.js and ask_app.js; uses their helpers ($, esc, S, DATA, G2Q, KV_RX, kvKeep, go via PAGES/goPage). */
(function () {
  const VA = { DARK: '#231F20', LIGHT: '#F9F9F2', E1: '#43A3A3', E2: '#77C7C9', E3: '#125C60', E4: '#B4D9E3', P3: '#A10009', P2: '#FF7980' };
  const FONT = '"Sharp Sans Disp No2","Sharp Sans Display No. 2","Proxima Nova",system-ui,sans-serif';
  const isDark = () => { const t = document.documentElement.getAttribute('data-theme'); return t ? t === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches; };
  const P = () => isDark()
    ? { ink: VA.LIGHT, sub: '#D8D4CC', grid: '#4A4546', main: VA.E1, hi: VA.E4, fc: '#3E6E70', fcStroke: VA.E2, series: [VA.E4, VA.E1, VA.LIGHT, VA.E2], seq: ['#24403F', VA.E3, VA.E1, VA.E4], pos: VA.E2, neg: VA.P2, card: '#302C2D', line: '#5A5455' }
    : { ink: VA.DARK, sub: '#4A4546', grid: '#E3E1D8', main: VA.E1, hi: VA.E3, fc: VA.E4, fcStroke: VA.E3, series: [VA.E3, VA.E1, VA.DARK, VA.E2], seq: ['#E3F1F4', VA.E4, VA.E1, VA.E3], pos: VA.E3, neg: VA.P3, card: '#FFFFFF', line: '#B4D9E3' };
  const num = t => { const m = String(t).replace(/,/g, '').match(/-?\d+(\.\d+)?/); return m ? +m[0] : 0; };
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------- G2 charts ---------------- */
  const axisStyle = p => { const st = { labelFill: p.ink, labelFontFamily: FONT, labelFontSize: 12.5, labelFillOpacity: 1, labelOpacity: 1, titleFill: p.ink, titleFontFamily: FONT, lineStroke: p.grid, tickStroke: p.grid, gridStroke: p.grid, gridStrokeOpacity: 1 }; return Object.assign({ style: Object.assign({}, st) }, st); };
  const theme = () => ({ type: isDark() ? 'classicDark' : 'classic', view: { viewFill: 'transparent' } });
  const anim = reduced ? false : undefined;
  function spec(c) {
    const p = P(), ax = axisStyle(p);
    if (c.kind === 'bars') {
      const rows = c.rows.map((r, i) => ({ l: r.l, v: +r.v, t: r.t, k: r.hi ? 'Highlighted' : 'Other', i }));
      return { type: 'interval', theme: theme(), data: rows, animate: anim,
        encode: { x: 'l', y: 'v', color: 'k' }, coordinate: { transform: [{ type: 'transpose' }] },
        scale: { color: { domain: ['Highlighted', 'Other'], range: [p.hi, p.main] }, x: { paddingInner: 0.28 }, y: { nice: true } },
        style: { radius: 4 }, legend: false, paddingRight: 64,
        axis: { x: Object.assign({ title: false, line: false, tick: false, labelAutoWrap: true, labelAutoHide: false }, ax), y: false },
        labels: [{ text: 't', position: 'right', dx: 8, textAlign: 'start', fill: p.ink, fontWeight: 700, fontFamily: FONT, fontSize: 12.5, style: { textAlign: 'start', dx: 8, fill: p.ink } }],
        tooltip: { title: 'l', items: [{ field: 't', name: c.title ? 'Value' : 'Value' }] } };
    }
    if (c.kind === 'cols') {
      const rows = c.rows.map(r => ({ l: r.l, v: +r.v, t: r.t, k: r.hi ? 'Latest full year (2025)' : r.fc ? 'Forecast' : 'Actual' }));
      return { type: 'interval', theme: theme(), data: rows, animate: anim, encode: { x: 'l', y: 'v', color: 'k' },
        scale: { color: { domain: ['Actual', 'Latest full year (2025)', 'Forecast'], range: [p.main, p.hi, p.fc] }, x: { paddingInner: 0.25 }, y: { nice: true } },
        style: { radius: 4, stroke: d => d.k === 'Forecast' ? p.fcStroke : null, lineDash: d => d.k === 'Forecast' ? [4, 3] : null, lineWidth: d => d.k === 'Forecast' ? 1.5 : 0 },
        axis: { x: Object.assign({ title: false, tick: false }, ax), y: false },
        legend: { color: { position: 'bottom', itemLabelFill: p.ink, itemLabelFontFamily: FONT } },
        labels: [{ text: 't', position: 'top', dy: -6, textBaseline: 'bottom', fill: p.ink, fontWeight: 700, fontFamily: FONT, fontSize: 12, style: { textBaseline: 'bottom', dy: -6, fill: p.ink } }], paddingTop: 26,
        tooltip: { title: 'l', items: [{ field: 't', name: 'Value' }, { field: 'k', name: 'Type' }] } };
    }
    if (c.kind === 'line') {
      const f = c.yfmt || {}, fmt = v => (f.pre || '') + (+v).toFixed(f.dec != null ? f.dec : 1) + (f.suf || '');
      const data = c.series.flatMap(sr => sr.v.map((v, i) => ({ x: String(c.x[i]), v: +v, s: sr.name, t: fmt(v) })));
      const names = c.series.map(sr => sr.name), focal = c.series.filter(sr => sr.focal).map(sr => sr.name);
      const range = names.map((n, i) => focal.includes(n) ? p.series[0] : p.series[1 + (i % 3)]);
      return { type: 'view', theme: theme(), data, animate: anim,
        scale: { color: { domain: names, range }, y: { nice: true, zero: c.ymin === 0 }, x: { type: 'point', padding: 0.05 } },
        axis: { x: Object.assign({ title: false }, ax), y: Object.assign({ title: false, grid: true, labelFormatter: v => fmt(v) }, ax) },
        legend: names.length > 1 ? { color: { position: 'bottom', itemLabelFill: p.ink, itemLabelFontFamily: FONT } } : false,
        children: [
          { type: 'line', encode: { x: 'x', y: 'v', color: 's' }, style: { lineWidth: 2.5 }, tooltip: false },
          { type: 'point', encode: { x: 'x', y: 'v', color: 's', shape: 'circle' }, tooltip: { title: 'x', items: [{ field: 't', name: 'Value' }, { field: 's', name: 'Series' }] } },
          { type: 'text', data: names.map(n => { const sr = c.series.find(x => x.name === n), last = sr.v.length - 1; return { x: String(c.x[last]), v: sr.v[last], s: n, t: fmt(sr.v[last]) }; }),
            encode: { x: 'x', y: 'v', text: 't', color: 's' }, style: { dx: 8, textAlign: 'start', fontWeight: 800, fontFamily: FONT, fontSize: 12.5 }, tooltip: false }
        ], paddingRight: 56 };
    }
    if (c.kind === 'heat') {
      const data = c.rows.flatMap(r => r.cells.map((v, j) => ({ m: r.l, k: c.cols[j], v: +v, t: (+v).toFixed(1) + '%', extra: r.extra || '' })));
      return { type: 'cell', theme: theme(), data, animate: anim, encode: { x: 'k', y: 'm', color: 'v' },
        scale: { color: { type: 'linear', range: p.seq, domain: [60, 75, 85, 95] } },
        style: { inset: 2, radius: 3 }, axis: { x: Object.assign({ title: false, position: 'top', tick: false, line: false }, ax), y: Object.assign({ title: false, tick: false, line: false }, ax) },
        legend: { color: { position: 'bottom', length: 260, labelFill: p.ink, labelFontFamily: FONT, title: false } },
        labels: [{ text: 't', position: 'inside', fontWeight: 700, fontFamily: FONT, fontSize: 12.5, transform: [{ type: 'contrastReverse' }] }],
        tooltip: { title: d => d.m + ', ' + d.k, items: [{ field: 't', name: 'Occupancy' }, { field: 'extra', name: 'Peak nights and groups' }] } };
    }
    if (c.kind === 'stack') {
      const cats = [...new Set(c.rows.flatMap(r => r.parts.map(x => x[0])))];
      const data = c.rows.flatMap(r => cats.map(cat => { const x = r.parts.find(q => q[0] === cat); return x ? { g: r.l, cat, pct: +x[1], t: x[1] + '%' } : null; }).filter(Boolean));
      return { type: 'interval', theme: theme(), data, animate: anim, encode: { x: 'g', y: 'pct', color: 'cat' }, transform: [{ type: 'stackY' }],
        coordinate: { transform: [{ type: 'transpose' }] },
        scale: { color: { domain: cats, range: isDark() ? [VA.E4, VA.E1, '#3E6E70', VA.LIGHT, '#8A8580'] : [VA.E3, VA.E1, VA.E2, VA.E4, '#8A8580'] }, x: { paddingInner: 0.3 }, y: { domain: [0, 100] } },
        style: { radius: 2, stroke: p.card, lineWidth: 1 }, axis: { x: Object.assign({ title: false, tick: false, line: false }, ax), y: false },
        legend: { color: { position: 'bottom', itemLabelFill: p.ink, itemLabelFontFamily: FONT } },
        labels: [{ text: d => d.pct >= 8 ? d.t : '', position: 'inside', fontWeight: 700, fontFamily: FONT, fontSize: 11.5, transform: [{ type: 'contrastReverse' }] }],
        tooltip: { title: d => d.g, items: [{ field: 'cat', name: 'Category' }, { field: 't', name: 'Share' }] } };
    }
    return null;
  }
  const CHARTS = new Map();   // element -> G2 chart
  async function mount(el) {
    if (CHARTS.has(el) || typeof G2 === 'undefined') return;
    const c = el.dataset.g2 === 'ann' ? Object.assign({ kind: 'bars' }, ANN_SPEC) : G2Q[+el.dataset.g2];
    const sp = c && spec(c); if (!sp) return;
    const fallback = el.innerHTML;
    try {
      el.innerHTML = ''; el.classList.add('g2-on');
      const chart = new G2.Chart({ container: el, autoFit: true, height: parseInt(getComputedStyle(el).getPropertyValue('--g2h')) || 260 });
      chart.options(sp); CHARTS.set(el, { chart, c }); await chart.render();
    } catch (e) {
      el.classList.remove('g2-on'); el.innerHTML = fallback; CHARTS.delete(el);
      const d = el.parentElement && el.parentElement.querySelector('details.g2-data'); if (d) d.open = true;
    }
  }
  /* overview growth bars (BI Pulse Summary) */
  const ANN_SPEC = DATA.main && DATA.main.chart ? { title: DATA.main.chart.title, rows: DATA.main.chart.rows.map(([l, v, t, hi]) => ({ l, v, t: (v > 0 ? '▲ ' : v < 0 ? '▼ ' : '') + t, hi })) } : null;
  function annHook() {
    const box = document.querySelector('.ann-bars'); if (!box || !ANN_SPEC || box.dataset.g2) return;
    const h = Math.max(150, ANN_SPEC.rows.length * 34 + 36);
    const wrap = document.createElement('div'); wrap.className = 'g2c'; wrap.dataset.g2 = 'ann'; wrap.style.setProperty('--g2h', h + 'px');
    box.parentNode.insertBefore(wrap, box); wrap.appendChild(box); io.observe(wrap);
  }
  const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { io.unobserve(en.target); mount(en.target); } }), { rootMargin: '300px 0px' });
  function observeAll(root) { (root || document).querySelectorAll('.g2c').forEach(el => { if (!CHARTS.has(el)) io.observe(el); }); }

  /* ---------------- T8 narrative text ---------------- */
  const TIME_RX = /\b(?:Q[1-4] 20\d\d|(?:Jan|Feb|March|April|May|June|July|Aug|Sept|Oct|Nov|Dec)\.?(?:[–-](?:Jan|Feb|March|April|May|June|July|Aug|Sept|Oct|Nov|Dec)\.?)? (?:\d{1,2}, )?20\d\d|(?:19|20)\d\d)\b/g;
  function t8Syntax(text) {
    text = String(text).replace(/[\[\]]/g, '');
    const spans = [];
    text.replace(KV_RX, (m, off, str) => {
      if (!m.trim() || !kvKeep(m)) return m;
      const prev = str.slice(Math.max(0, off - 10), off);
      if (/(Route |Q|SR-|I-|No\. |District |Line |Phase |Lot |Dock )$/.test(prev) || /[A-Za-z]$/.test(prev)) return m;
      const lead = m.match(/^\s*/)[0].length; spans.push({ a: off + lead, b: off + m.length, kind: 'kv' }); return m;
    });
    text.replace(TIME_RX, (m, off) => { if (!spans.some(s => off < s.b && off + m.length > s.a)) spans.push({ a: off, b: off + m.length, kind: 'time' }); return m; });
    spans.sort((x, y) => x.a - y.a);
    let out = '', last = 0;
    for (const s of spans) {
      if (s.a < last) continue;
      const raw = text.slice(s.a, s.b), before = text.slice(Math.max(0, s.a - 14), s.a).toLowerCase();
      let ent;
      if (s.kind === 'time') ent = `[${raw}](time_desc)`;
      else if (/%/.test(raw) && (/^[▲+]/.test(raw) || /(up|rose|grew|gain(ed)?|increas\w*|higher|by)\s*$/.test(before))) ent = `[${raw.replace(/^▲\s?/, '')}](ratio_value, origin=${num(raw) / 100}, assessment="positive")`;
      else if (/%/.test(raw) && (/^[▼−-]/.test(raw) || /(down|fell|declin\w*|lower|dropp\w*)\s*$/.test(before))) ent = `[${raw.replace(/^▼\s?/, '')}](ratio_value, origin=${-Math.abs(num(raw)) / 100}, assessment="negative")`;
      else if (/%/.test(raw) && num(raw) <= 100 && !/[–-]/.test(raw.slice(1))) ent = `[${raw}](proportion, origin=${num(raw) / 100})`;
      else ent = `[${raw}](metric_value, origin=${num(raw)})`;
      out += text.slice(last, s.a) + ent; last = s.b;
    }
    return out + text.slice(last);
  }
  const T8S = new Map();
  function t8Theme() {
    const p = P();
    return [isDark() ? 'dark' : 'light', { fontFamily: FONT, fontSize: 16, lineHeight: 26, colorBase: p.ink, colorEntityBase: p.ink, colorMetricValue: isDark() ? VA.E4 : VA.E3, colorOtherValue: p.ink,
      colorPositive: p.pos, colorNegative: p.neg, colorDimensionValue: p.ink, colorMetricName: p.ink, colorConclusion: p.ink, colorProportionFill: isDark() ? VA.E2 : VA.E3, colorProportionShadow: isDark() ? '#4A4546' : VA.E4, colorLineStroke: VA.E1, colorLink: p.ink }];
  }
  function t8Render(el) {
    if (typeof T8 === 'undefined' || !el.dataset.t8) return;
    try {
      let host = T8S.get(el);
      if (!host) { host = { fb: el.innerHTML, t: null }; T8S.set(el, host); }
      el.innerHTML = ''; el.classList.add('t8-on');
      const t = new T8.Text(el), [mode, tok] = t8Theme(); t.theme(mode, tok).render(t8Syntax(el.dataset.t8)); host.t = t;
    } catch (e) { const h = T8S.get(el); if (h) el.innerHTML = h.fb; el.classList.remove('t8-on'); }
  }
  const t8io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { t8io.unobserve(en.target); t8Render(en.target); } }), { rootMargin: '400px 0px' });
  function observeT8(root) { (root || document).querySelectorAll('.t8x').forEach(el => { if (!T8S.has(el)) t8io.observe(el); }); }

  /* ---------------- AntV Infographic (icons from Material Design Icons, inlined) ---------------- */
  const icon = n => { const d = (window.MDI || {})[n]; return d ? 'data:image/svg+xml,' + encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="${d}"/></svg>`) : ''; };
  const IGS = [];   // {el, syntax()}
  function igTheme() {
    const p = P();
    return `theme${isDark() ? ' dark' : ''}
  palette
    - ${isDark() ? VA.E4 : VA.E3}
    - ${VA.E1}
    - ${isDark() ? VA.E2 : '#2E7F80'}
  base
    text
      font-family ${FONT.split(',')[0].replace(/"/g, '')}`;
  }
  function igRender(item) {
    if (typeof AntVInfographic === 'undefined') return;
    try {
      item.el.innerHTML = '';
      const ig = new AntVInfographic.Infographic({ container: item.el, width: '100%', height: '100%' });
      ig.render(item.syntax() + '\n' + igTheme()); item.ig = ig;
    } catch (e) { item.el.innerHTML = item.fallback || ''; }
  }
  function addIg(host, where, id, title, sub, src, h, syntax, fallback, calc) {
    if (!host || document.getElementById(id)) return;
    const fig = document.createElement('figure'); fig.className = 'ig ig-antv'; fig.id = id;
    fig.innerHTML = `<header class="ig-h"><h4>${esc(title)}</h4>${sub ? `<p>${esc(sub)}</p>` : ''}</header><div class="d3s x6s"><div class="igc" style="height:${h}px" role="img" aria-label="${esc(title + '. ' + (fallback || ''))}"></div></div>${calc ? `<p class="ig-calc">${esc(calc)}</p>` : ''}<p class="ig-src">Source: ${esc(src)}</p>`;
    where === 'before' ? host.parentNode.insertBefore(fig, host) : where === 'prepend' ? host.insertBefore(fig, host.firstChild) : host.appendChild(fig);
    const item = { el: fig.querySelector('.igc'), syntax, fallback: `<p class="ig-fb">${esc(fallback || '')}</p>` }; IGS.push(item);
    const o = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { o.disconnect(); igRender(item); } }), { rootMargin: '300px 0px' }); o.observe(item.el);
  }
  function buildInfographics() {
    // One more night: the method in five steps (values from the section's calculation table)
    const night = S.find(s => s.id === 'p-night');
    if (night) {
      const rows = Object.fromEntries(night.tables[0].rows.map(r => [r[0], r[1]]));
      const steps = [['Visitors, 2025', rows['Visitors, 2025'], 'Tourism Economics', 'account-group'],
        ['Weighted average stay', rows['Weighted average stay'], '93.2% × 1.9 days + 6.8% × 5.9 days', 'calendar-range'],
        ['Spending per visitor-day', rows['Spending per visitor-day'], '$6.83B ÷ (26.5M × 2.17)', 'cash-multiple'],
        ['One more night of lodging', rows['One more night of lodging'], '$1.72B lodging ÷ 2.17 days', 'bed'],
        ['Every visitor, all spending', rows['One more day, every visitor (upper bound)'], 'Upper bound: $6.83B ÷ 2.17', 'chart-line']].filter(s => s[1]);
      addIg($('p-night-ig') || $('p-night-s2'), 'append', 'p-night-antv', 'How the one-more-night value is built, in five steps', 'Each step uses 2025 Tourism Economics totals and Azira length of stay. The calculations are listed below the steps.',
        'Visit Anaheim BI, Extra Night study (2025 inputs; recalculated Oct. 12, 2026)', 330,
        () => `infographic list-row-horizontal-icon-arrow\ndata\n  lists\n${steps.map(s => `    - label ${s[1]}\n      desc ${s[0]}\n      icon ${icon(s[3])}`).join('\n')}`,
        steps.map(s => `${s[0]} ${s[1]} (${s[2]})`).join('; '), 'Calculations: ' + steps.map(s => `${s[0]} ${s[1]} = ${s[2]}`).join(' · '));
    }
    // How this report is updated: the quarterly timeline
    const U = DATA.schedule;
    if (U) addIg($('updCards'), 'before', 'upd-antv', 'The quarterly update cycle', 'Each edition is refreshed on the 15th of the month after Tourism Economics delivers its quarterly forecast.',
      'Visit Anaheim BI update schedule (Oct. 14, 2026)', 260,
      () => `infographic sequence-timeline-simple\ndata\n  sequences\n    - label Jan. 15\n      desc Q4 results and new forecast\n      icon ${icon('calendar-start')}\n    - label Apr. 15\n      desc Q1 results; annual impact reports arrive in spring\n      icon ${icon('calendar-check')}\n    - label July 15\n      desc Q2 results\n      icon ${icon('calendar-check')}\n    - label Oct. 15\n      desc Q3 results\n      icon ${icon('calendar-check')}\n  order asc`,
      'Jan. 15, Apr. 15, July 15 and Oct. 15');
    // Library: topics at a glance
    const LB = DATA.lib;
    if (LB) {
      const ic = { econ: 'finance', forecast: 'chart-timeline-variant', night: 'weather-night', visitors: 'account-group', media: 'bullhorn', hotels: 'bed', outlook: 'telescope', transport: 'bus', program: 'calendar-star', report: 'file-document-multiple' };
      const items = LB.topics.map(([k, t]) => [t.split(' (')[0], LB.files.filter(f => f.topic === k).length, ic[k] || 'folder']).filter(x => x[1]);
      addIg($('libFilesH'), 'before', 'lib-antv', 'What is in the library', `${LB.files.length} files in ${items.length} topics.`, 'Visit Anaheim BI, Reports and data library (Oct. 14, 2026)', 320,
        () => `infographic list-grid-badge-card\ndata\n  lists\n${items.map(([t, n, i]) => `    - label ${t}\n      desc ${n} file${n > 1 ? 's' : ''}\n      icon ${icon(i)}`).join('\n')}`,
        items.map(([t, n]) => `${t}: ${n}`).join('; '));
    }
  }

  /* ---------------- X6 diagrams ---------------- */
  const X6S = [];
  // keep diagrams readable on phones: at least 760px wide inside a swipeable frame
  const x6w = el => { const w = Math.max((el.parentNode && el.parentNode.clientWidth) || 900, 760); el.style.width = w + 'px'; return w; };
  const IMPACT = { 'Anaheim': [26.5, 6832, 1460, 2130, 10422, 67817, 3050, 970], 'Garden Grove': [3.24, 769.3, 127.7, 191.1, 1088.1, 6694, 263.2, 83.6], 'Orange County': [51.3, 17993, 6253, 6426, 30673, 178164, 7776, 3094] };
  const money = m => m >= 1000 ? '$' + (m / 1000).toFixed(2) + 'B' : '$' + (m >= 100 ? Math.round(m) : m.toFixed(1)) + 'M';
  function x6Impact(el, geo) {
    const p = P(), [vis, sp, ind, indc, tot, jobs, inc, tax] = IMPACT[geo];
    el.innerHTML = '';
    const g = new X6.Graph({ container: el, width: x6w(el), height: parseInt(el.style.height) || 300, background: { color: 'transparent' }, interacting: false, panning: false, mousewheel: false, grid: false });
    const node = (id, x, y, w, label, sub, strong) => g.addNode({ id, shape: 'rect', x, y, width: w, height: 64,
      attrs: { body: { fill: strong ? p.hi : p.card, stroke: strong ? p.hi : VA.E1, strokeWidth: 1.5, rx: 8, ry: 8 },
        label: { text: label + '\n' + sub, fill: strong ? (isDark() ? VA.DARK : '#FFFFFF') : p.ink, fontFamily: FONT, fontSize: 13, fontWeight: 700, lineHeight: 18 } } });
    const edge = (a, b, t) => g.addEdge({ source: a, target: b, router: { name: 'manhattan' }, connector: { name: 'rounded' },
      attrs: { line: { stroke: VA.E1, strokeWidth: 2, targetMarker: { name: 'block', width: 8, height: 6 } } },
      labels: t ? [{ attrs: { label: { text: t, fill: p.ink, fontFamily: FONT, fontSize: 11 }, body: { fill: p.card, stroke: 'none' } } }] : [] });
    node('v', 0, 108, 150, (vis + 'M').replace('.0M', 'M'), 'visitors', false);
    node('d', 210, 108, 170, money(sp), 'visitor spending (direct)', true);
    node('i', 440, 20, 180, money(ind), 'supplier purchases (indirect)', false);
    node('n', 440, 196, 180, money(indc), 'worker spending (induced)', false);
    node('t', 680, 108, 170, money(tot), 'total economic impact', true);
    node('j', 910, 20, 160, jobs.toLocaleString('en-US'), 'jobs supported', false);
    node('l', 910, 108, 160, money(inc), 'labor income', false);
    node('x', 910, 196, 160, money(tax), 'state and local taxes', false);
    edge('v', 'd', 'spend'); edge('d', 'i'); edge('d', 'n'); edge('d', 't'); edge('i', 't'); edge('n', 't'); edge('t', 'j'); edge('t', 'l'); edge('t', 'x');
    g.zoomToFit({ padding: 16, maxScale: 1 }); g.centerContent();
    return g;
  }
  function addImpactFlow() {
    const host = $('p-impact-ig') || $('p-impact-s2'); if (!host || $('p-impact-x6')) return;
    const fig = document.createElement('figure'); fig.className = 'ig ig-x6'; fig.id = 'p-impact-x6';
    fig.innerHTML = `<header class="ig-h"><h4>How visitor spending becomes economic impact, 2025</h4><p>Direct visitor spending, plus supplier purchases and worker spending, adds up to the total impact, which supports jobs, income and taxes. Choose a geography.</p></header>
      <div class="x6-geo" role="group" aria-label="Geography">${Object.keys(IMPACT).map((k, i) => `<button type="button" class="chip" aria-pressed="${i === 0}" data-geo="${k}">${k}</button>`).join('')}</div>
      <div class="d3s x6s"><div class="x6c" style="height:300px" role="img" aria-label=""></div></div>
      <p class="ig-calc">Total impact = direct + indirect + induced. Each geography is modeled on its own, so city totals are not added to the county.</p>
      <p class="ig-src">Source: Tourism Economics, Economic Impact of Visitors 2025 (Anaheim, Garden Grove, Orange County; pub. Apr.–May 2026)</p>`;
    host.appendChild(fig);
    const el = fig.querySelector('.x6c'); let geo = 'Anaheim';
    const draw = () => { try { const [vis, sp, ind, indc, tot, jobs, inc, tax] = IMPACT[geo]; el.setAttribute('aria-label', `${geo}: ${vis}M visitors; visitor spending ${money(sp)} plus indirect ${money(ind)} and induced ${money(indc)} equals total impact ${money(tot)}; ${jobs.toLocaleString('en-US')} jobs, ${money(inc)} labor income, ${money(tax)} state and local taxes.`); x6Impact(el, geo); } catch (e) { el.textContent = el.getAttribute('aria-label'); } };
    fig.querySelector('.x6-geo').addEventListener('click', e => { const b = e.target.closest('[data-geo]'); if (!b) return; geo = b.dataset.geo; fig.querySelectorAll('[data-geo]').forEach(x => x.setAttribute('aria-pressed', x === b)); draw(); });
    X6S.push(draw);
    const o = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { o.disconnect(); draw(); } })); o.observe(el);
  }
  function addLineage() {
    const LB = DATA.lib, reg = $('regTbl'); if (!LB || !reg || $('lineage-x6')) return;
    const pubOf = f => /Tourism Economics/.test(f.publisher) ? 'Tourism Economics' : /Visa/.test(f.publisher) ? 'Visa (Symphony)' : /Azira|Symphony/.test(f.publisher) ? 'Azira (Symphony)' : /LARC/.test(f.publisher) ? 'LARC' : /STR/.test(f.publisher) ? 'STR' : /CoStar/.test(f.publisher) ? 'CoStar' : /Datafy/.test(f.publisher) ? 'Datafy' : /OCTA|Metrolink|Rail|transit/.test(f.publisher) ? 'OCTA, rail and transit' : /Transportation Statistics/.test(f.publisher) ? 'U.S. BTS' : /Visit Anaheim/.test(f.publisher) ? 'Visit Anaheim BI' : null;
    const links = new Map();
    LB.files.forEach(f => { const pb = pubOf(f); if (!pb) return; (f.used_in || []).filter(id => S.find(s => s.id === id)).forEach(id => links.set(pb + '|' + id, [pb, id])); });
    const pubs = [...new Set([...links.values()].map(v => v[0]))], secs = S.filter(s => [...links.values()].some(v => v[1] === s.id));
    const box = reg.closest('.box'); const fig = document.createElement('figure'); fig.className = 'ig ig-x6'; fig.id = 'lineage-x6';
    const H = Math.max(pubs.length, secs.length) * 46 + 20;
    fig.innerHTML = `<header class="ig-h"><h4>Data lineage: which source feeds which section</h4><p>Hover over or tab to a source or section to highlight its links. Built from the Reports and data library.</p></header><div class="d3s x6s"><div class="x6c" style="height:${H}px" role="img" aria-label="${esc([...links.values()].map(([a, b]) => a + ' to ' + (S.find(s => s.id === b) || {}).tab).join('; '))}"></div></div><p class="ig-src">Source: Visit Anaheim BI, Reports and data library and source register (Oct. 14, 2026)</p>`;
    box.parentNode.insertBefore(fig, box);
    const el = fig.querySelector('.x6c');
    const draw = () => {
      try {
        const p = P(); el.innerHTML = '';
        const g = new X6.Graph({ container: el, width: x6w(el), height: parseInt(el.style.height) || 400, background: { color: 'transparent' }, interacting: false, panning: false, mousewheel: false });
        pubs.forEach((pb, i) => g.addNode({ id: 'p:' + pb, shape: 'rect', x: 0, y: 10 + i * 46, width: 210, height: 34, attrs: { body: { fill: p.hi, stroke: p.hi, rx: 6, ry: 6 }, label: { text: pb, fill: isDark() ? VA.DARK : '#FFFFFF', fontFamily: FONT, fontSize: 12.5, fontWeight: 700 } } }));
        secs.forEach((s, i) => g.addNode({ id: 's:' + s.id, shape: 'rect', x: 560, y: 10 + i * 46 * (pubs.length / Math.max(secs.length, 1)), width: 220, height: 34, attrs: { body: { fill: p.card, stroke: VA.E1, strokeWidth: 1.5, rx: 6, ry: 6 }, label: { text: s.tab, fill: p.ink, fontFamily: FONT, fontSize: 12.5, fontWeight: 700 } } }));
        [...links.values()].forEach(([a, b]) => g.addEdge({ source: 'p:' + a, target: 's:' + b, connector: { name: 'smooth' }, attrs: { line: { stroke: isDark() ? '#6F9C9D' : VA.E2, strokeWidth: 1.2, targetMarker: null } } }));
        const hl = (n, on) => g.getConnectedEdges(n).forEach(ed => ed.attr('line/stroke', on ? (isDark() ? VA.E4 : VA.E3) : (isDark() ? '#6F9C9D' : VA.E2)) || ed.attr('line/strokeWidth', on ? 2.6 : 1.2));
        g.on('node:mouseenter', ({ node }) => hl(node, true)); g.on('node:mouseleave', ({ node }) => hl(node, false));
        g.zoomToFit({ padding: 10, maxScale: 1 }); g.centerContent();
      } catch (e) { el.textContent = el.getAttribute('aria-label'); }
    };
    X6S.push(draw);
    const o = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { o.disconnect(); draw(); } })); o.observe(el);
  }

  /* ---------------- theme changes: redraw everything that is on screen ---------------- */
  function redraw() {
    CHARTS.forEach(({ chart, c }) => { try { chart.options(spec(c)); chart.render(); } catch (e) {} });
    T8S.forEach((h, el) => t8Render(el));
    IGS.forEach(it => { if (it.ig) igRender(it); });
    X6S.forEach(d => d());
  }
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', redraw);
  let rz; window.addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(() => X6S.forEach(d => d()), 250); }, { passive: true });
  new MutationObserver(redraw).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  window.addEventListener('beforeprint', () => document.querySelectorAll('.g2c').forEach(el => mount(el)));

  const start = () => { annHook(); observeAll(); observeT8(); buildInfographics(); addImpactFlow(); addLineage(); };
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(start, start);
})();
