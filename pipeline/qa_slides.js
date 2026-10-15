/* Questions answered and Reports and data library slides (Oct. 14, 2026).
   Shared by the full deck (deck.js = deck_head + qa_slides + deck_body) and the focused deck
   (qa_deck.js = deck_head + qa_slides + qa_body). Uses deck_head helpers: pres, content, source, table, hbar, rich, paras, kpis, ft, H, W, M. */
const AQ = D.ask, LB = D.lib;
const QS = Object.fromEntries(AQ.items.map(q => [q.id, q]));
const FILES = Object.fromEntries(LB.files.map(f => [f.id, f]));
const SEC_T = Object.fromEntries([['p-ask', 'Questions answered'], ['p-library', 'Reports and data library'], ['p-notes', 'Sources'], ...D.sections.map(s => [s.id, s.tab])]);
const uniq = a => [...new Set(a)];

function noteBox(s, title, text, x, y, w, h) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: H.light }, line: { color: H.e4, width: 0.75 }, objectName: 'note-' + title });
  s.addText(title.toUpperCase(), ft({ x: x + 0.12, y: y + 0.08, w: w - 0.24, h: 0.22, fontSize: 8.5, bold: true, color: H.e3, charSpacing: 1 }));
  rich(s, text, { x: x + 0.12, y: y + 0.32, w: w - 0.24, h: h - 0.4, fontSize: 9, fit: 'shrink' });
}
function qaChart(s, v, x, y, w, h) {
  if (!v) return;
  if (v.kind === 'stack') {
    const cats = uniq(v.rows.flatMap(r => r.parts.map(p => p[0])));
    const data = cats.map(c => ({ name: c, labels: v.rows.map(r => r.l), values: v.rows.map(r => { const p = r.parts.find(p => p[0] === c); return p ? p[1] : 0; }) }));
    s.addText(v.title, ft({ x, y, w, h: 0.35, fontSize: 12, bold: true, color: H.e3, objectName: 'chart-title' }));
    s.addChart(pres.charts.BAR, data, { x, y: y + 0.38, w, h: h - 0.38, barDir: 'bar', barGrouping: 'stacked', chartColors: ['125C60', '43A3A3', '77C7C9', 'B4D9E3', 'E8E6DC'],
      catAxisOrientation: 'maxMin', catAxisLabelFontSize: 9.5, catAxisLabelFontFace: 'Proxima Nova', catAxisLabelColor: H.dark, valAxisHidden: true, valAxisMaxVal: 100,
      valGridLine: { style: 'none' }, showValue: true, dataLabelFormatCode: '0"%"', dataLabelFontSize: 8, dataLabelColor: H.dark, dataLabelFontFace: 'Proxima Nova',
      showLegend: true, legendPos: 'b', legendFontSize: 8.5, legendFontFace: 'Proxima Nova', barGapWidthPct: 40, objectName: 'chart' });
    return;
  }
  const rows = v.rows, hi = rows.findIndex(r => r.hi);
  const pct = (v.unit === '%');
  hbar(s, v.title, rows.map(r => r.l), rows.map(r => r.v), x, y, w, h, v.fmt || (pct ? '0.0"%"' : (Math.max(...rows.map(r => r.v)) < 20 ? '0.00' : '#,##0')), hi < 0 ? 0 : hi);
}
function qaSlide(section, q, kicker) {
  const s = content(section, q.q, (kicker || q.topic) + ' · Anaheim, Orange County and U.S.', q.a);
  rich(s, q.a, { x: M, y: 1.5, w: 7.25, h: 0.95, fontSize: 12, fit: 'shrink' });
  table(s, [['Geography', 0], ['Value', 0], ['Detail', 0]], q.geo.map(g => [g[0], g[1], g[2]]), M, 2.55, 7.25, { colW: [1.75, 1.75, 3.75], rowH: 0.42, fs: 8.5, hi: 0 });
  const xr = M + 7.5, wr = W - M - xr;
  if (q.viz) { qaChart(s, q.viz, xr, 1.45, wr, 2.75); noteBox(s, 'How it is calculated', q.how, xr, 4.3, wr, 1.08); if (q.caveat) noteBox(s, 'Keep in mind', q.caveat, xr, 5.45, wr, 1.0); }
  else { noteBox(s, 'How it is calculated', q.how, xr, 1.5, wr, 2.2); if (q.caveat) noteBox(s, 'Keep in mind', q.caveat, xr, 3.85, wr, 2.0); }
  const files = (q.files || []).map(id => FILES[id]).filter(Boolean).map(f => f.title);
  source(s, uniq(q.geo.map(g => g[3])).join('; ') + (files.length ? '. Files in the app library: ' + files.join('; ') : '') + '.');
  return s;
}
function qaDetailSlide(section, q) {
  // a second slide for each core question: the full table behind it
  const pick = { 'avg-spend': ['p-spend', 'Average spend'], 'transport-impact': ['p-transport', 'Economic impact of visitor transportation'], 'night-value': ['p-night', 'How the one-more-night'], 'd5-who': ['p-d5', 'Where District 5 visitors come from'] }[q.id];
  if (!pick) return;
  const sc = D.sections.find(x => x.id === pick[0]); const t = sc && sc.tables.find(t => t.title.startsWith(pick[1]));
  if (!t) return;
  const s = content(section, t.title, 'The detail behind: ' + q.q, t.sub || '');
  const n = t.cols.length, cw = (W - 2 * M);
  const colW = n === 3 ? [3.6, 2.4, cw - 6.0] : n === 4 ? [2.6, 2.2, 5.6, cw - 10.4] : t.cols.map(() => cw / n);
  table(s, t.cols, t.rows.slice(0, 11), M, 1.55, cw, { colW, rowH: 0.3, fs: 9.5, hi: t.hi === undefined ? 0 : t.hi });
  noteBox(s, 'How it is calculated', q.how, M, 5.45, cw / 2 - 0.1, 1.0);
  noteBox(s, 'Keep in mind', q.caveat || 'See the About the data slides.', M + cw / 2 + 0.1, 5.45, cw / 2 - 0.1, 1.0);
  source(s, t.src + '.');
}
function qaCoreSlide(section) {
  const s = content(section, 'Questions answered: the four core questions', 'Anaheim, Orange County and U.S. · each answer has a summary, a visual, the method and the files to read more', '');
  kpis(s, AQ.core.map(id => QS[id]).map(q => [q.topic, q.key_l, q.key, q.q]), M, 1.6, W - 2 * M, 2.4, 26);
  const rows = AQ.core.map(id => QS[id]).map(q => [q.q, q.a]);
  table(s, [['Question', 0], ['Short answer', 0]], rows, M, 4.15, W - 2 * M, { colW: [3.4, W - 2 * M - 3.4], rowH: 0.5, fs: 9, hi: -1, rich: true });
  source(s, 'Visit Anaheim Business Intelligence (Oct. 14, 2026); sources on each question slide.');
}
function qaIndexSlide(section) {
  const s = content(section, 'Every question answered in this report', 'Find the slide or open the app: Questions answered', '');
  const rows = AQ.order.flatMap(t => AQ.items.filter(q => q.topic === t).map(q => [t, q.q, q.key + ' ' + q.key_l]));
  table(s, [['Topic', 0], ['Question', 0], ['Headline answer', 0]], rows, M, 1.5, W - 2 * M, { colW: [2.2, 5.0, W - 2 * M - 7.2], rowH: 0.23, fs: 8, hi: -1 });
  source(s, 'Visit Anaheim Business Intelligence (Oct. 14, 2026).');
}
function libSlides(section) {
  const byTopic = LB.topics.map(([k, t]) => [t, LB.files.filter(f => f.topic === k)]).filter(x => x[1].length);
  const rows = byTopic.flatMap(([t, fs]) => fs.map(f => [t.split(' (')[0], f.title, f.publisher.split(' for ')[0], f.period, f.published, f.ext]));
  const per = 13;
  for (let i = 0; i < rows.length; i += per) {
    const s = content(section, 'Reports and data library' + (i ? ' (continued)' : ''), `${LB.files.length} files used to build this report · open or download each one in the app (Reports and data library)`, '');
    table(s, [['Topic', 0], ['File', 0], ['Publisher', 0], ['Covers', 0], ['Published', 0], ['Type', 0]], rows.slice(i, i + per), M, 1.5, W - 2 * M,
      { colW: [1.9, 4.3, 2.4, 1.75, 1.2, W - 2 * M - 11.55], rowH: 0.36, fs: 8, hi: -1 });
    source(s, 'Visit Anaheim Business Intelligence, Reports and data library (Oct. 14, 2026). Files as received from each publisher.');
  }
  const s = content(section, 'Public sources used (links)', 'Published by others and linked rather than hosted', '');
  table(s, [['Source', 0], ['What it is used for', 0], ['Link', 0]], LB.links.map(l => [l[0], l[2], l[1]]), M, 1.5, W - 2 * M, { colW: [4.2, 4.4, W - 2 * M - 8.6], rowH: 0.6, fs: 8.5, hi: -1 });
  source(s, 'Accessed dates as listed.');
}
