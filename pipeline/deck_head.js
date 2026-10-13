const pptxgen = require('pptxgenjs');
// Theme step: uses the pptx skill's apply_theme.js (available in Claude sessions; not redistributed here).
// Set PPTX_THEME_SCRIPT to its path to apply the theme; without it the deck is written unthemed and a warning is shown.
let applyTheme = async () => console.warn('PPTX_THEME_SCRIPT not set: deck written without the theme step.');
try { if (process.env.PPTX_THEME_SCRIPT) ({ applyTheme } = require(process.env.PPTX_THEME_SCRIPT)); } catch (e) { console.warn('Theme script not loaded:', e.message); }
const D = require('./deck_data.json');

const THEME = { name: 'Visit Anaheim Escapism', headFontFace: 'Proxima Nova', bodyFontFace: 'Proxima Nova',
  colors: { dk1: '231F20', lt1: 'FFFFFF', dk2: '125C60', lt2: 'F9F9F2', accent1: '43A3A3', accent2: '77C7C9', accent3: 'B4D9E3', accent4: '125C60', accent5: 'A10009', accent6: 'FF000C', hlink: '125C60', folHlink: '125C60' } };
const H = { dark: '231F20', light: 'F9F9F2', e1: '43A3A3', e2: '77C7C9', e3: '125C60', e4: 'B4D9E3', white: 'FFFFFF', p3: 'A10009' };

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';            // 13.333 x 7.5 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = 'OC Vibe Insights'; pres.author = 'Visit Anaheim Business Intelligence'; pres.company = 'Visit Anaheim';
const C = pres.SchemeColor;
const W = 13.333, M = 0.6;
const LOGO = D.logo.replace(/^data:/, '');   // "image/png;base64,..."
const LOGO_AR = 600 / 219;

pres.defineSlideMaster({ title: 'VA Title', background: { color: H.e3 },
  objects: [{ placeholder: { options: { name: 'title', type: 'title', x: M, y: 2.55, w: 9.5, h: 1.5, fontSize: 44, bold: true, italic: true, color: H.white, valign: 'top', align: 'left', margin: 0 }, text: '' } },
            { placeholder: { options: { name: 'sub', type: 'body', x: M, y: 4.15, w: 9.5, h: 1.2, fontSize: 18, color: H.white, valign: 'top', align: 'left', margin: 0 }, text: '' } }] });
pres.defineSlideMaster({ title: 'VA Section', background: { color: H.e3 },
  objects: [{ placeholder: { options: { name: 'title', type: 'title', x: M, y: 2.9, w: 11, h: 1.2, fontSize: 36, bold: true, italic: true, color: H.white, margin: 0 }, text: '' } }] });
pres.defineSlideMaster({ title: 'VA Content', background: { color: H.white },
  objects: [
    { image: { x: W - M - 1.6, y: 0.3, w: 1.6, h: 1.6 / LOGO_AR, data: LOGO } },
    { line: { x: M, y: 7.0, w: W - 2 * M, h: 0, line: { color: H.e1, width: 1 } } },
    { text: { text: 'Visit Anaheim | visitanaheim.org', options: { x: M, y: 7.02, w: 6, h: 0.3, fontSize: 9, color: H.dark, margin: 0 } } },
    { placeholder: { options: { name: 'title', type: 'title', x: M, y: 0.3, w: W - 2 * M - 2.0, h: 0.85, fontSize: 22, bold: true, color: H.e3, valign: 'top', align: 'left', margin: 0 }, text: '' } },
    { placeholder: { options: { name: 'kicker', type: 'body', x: M, y: 1.2, w: W - 2 * M - 2.0, h: 0.3, fontSize: 12, color: H.dark, align: 'left', margin: 0 }, text: '' } }],
  slideNumber: { x: W - M - 0.6, y: 7.02, w: 0.6, h: 0.3, fontSize: 9, color: H.dark, align: 'right' } });

const ft = (o) => Object.assign({ isTextBox: true, margin: 0, fontFace: 'Proxima Nova' }, o);
function content(section, title, kicker, notes) {
  const s = pres.addSlide({ masterName: 'VA Content', sectionTitle: section });
  s.addText(title, { placeholder: 'title' });
  if (kicker) s.addText(kicker, { placeholder: 'kicker' });
  if (notes) s.addNotes(notes);
  return s;
}
function source(s, txt) { s.addText('Source: ' + txt, ft({ x: M, y: 6.55, w: W - 2 * M, h: 0.4, fontSize: 9, color: H.dark, valign: 'bottom', objectName: 'source' })); }
function kpis(s, cards, x, y, w, h, vfs = 28) {
  const gap = 0.18, cw = (w - gap * (cards.length - 1)) / cards.length;
  cards.forEach(([k, l, v, sub], i) => {
    const cx = x + i * (cw + gap);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx, y, w: cw, h, fill: { color: H.white }, line: { color: H.e4, width: 1 }, rectRadius: 0.08, objectName: 'kpi-card-' + i });
    s.addText(k.toUpperCase(), ft({ x: cx + 0.18, y: y + 0.14, w: cw - 0.36, h: 0.25, fontSize: 9, bold: true, color: H.e3, charSpacing: 1 }));
    s.addText(l, ft({ x: cx + 0.18, y: y + 0.38, w: cw - 0.36, h: 0.3, fontSize: 10.5, bold: true, color: H.dark, fit: 'shrink' }));
    s.addText(v, ft({ x: cx + 0.18, y: y + 0.68, w: cw - 0.36, h: 0.6, fontSize: vfs, bold: true, color: H.e3 }));
    s.addText(sub, ft({ x: cx + 0.18, y: y + 1.28, w: cw - 0.36, h: h - 1.38, fontSize: 10, color: H.dark, valign: 'top' }));
  });
}
function table(s, cols, rows, x, y, w, opts = {}) {
  const hdr = cols.map(([l, n]) => ({ text: l, options: { bold: true, color: H.white, fill: { color: H.e3 }, align: n ? 'right' : 'left', fontSize: opts.fs || 10.5 } }));
  const body = rows.map((r, i) => r.map((c, j) => {
    const isObj = c && typeof c === 'object';
    const txt = isObj ? (c.d > 0 ? '▲ ' : c.d < 0 ? '▼ ' : '▶ ') + c.t : String(c);
    return { text: (opts.rich && !isObj && j > 0) ? runs(txt, { fontSize: opts.fs || 10.5 }) : txt, options: { align: cols[j][1] ? 'right' : 'left', bold: i === opts.hi || j === 0, fontSize: opts.fs || 10.5,
      color: isObj && c.d < 0 ? H.p3 : H.dark, fill: { color: i === opts.hi ? H.e4 : (i % 2 ? H.light : H.white) } } };
  }));
  s.addTable([hdr, ...body], { x, y, w, colW: opts.colW, fontFace: 'Proxima Nova', border: { type: 'solid', pt: 0.5, color: H.e4 }, rowH: opts.rowH || 0.32, margin: [0.04, 0.08, 0.04, 0.08], valign: 'middle' });
}
function hbar(s, title, labels, values, x, y, w, h, fmt, hiIdx = 0) {
  s.addText(title, ft({ x, y, w, h: 0.35, fontSize: 13, bold: true, color: H.e3, objectName: 'chart-title' }));
  const colors = values.map((_, i) => i === hiIdx ? H.e1 : H.e4);
  s.addChart(pres.charts.BAR, [{ name: title, labels, values }], { x, y: y + 0.4, w, h: h - 0.4, barDir: 'bar', chartColors: colors, invertedColors: colors,
    catAxisOrientation: 'maxMin', catAxisLabelColor: H.dark, catAxisLabelFontSize: 10, catAxisLabelFontFace: 'Proxima Nova', valAxisHidden: true,
    valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: fmt, dataLabelColor: H.dark,
    dataLabelFontSize: 10, dataLabelFontBold: true, dataLabelFontFace: 'Proxima Nova', barGapWidthPct: 45, showLegend: false, objectName: 'chart' });
}
/* Split text into runs, bolding key metrics (money, %, large counts, scaled values) in teal */
const KV_RX = /(?:[▲▼]\s?)?[+−-]?\$?\d[\d,]*(?:\.\d+)?(?:\s?(?:[MBK](?![a-z])|million|billion|%|percentage points|points|pts|days?|nights|room nights|jobs|visitors|vehicles|rooms|seats))?(?:\s?(?:–|-|to)\s?\$?\d[\d,]*(?:\.\d+)?(?:[MBK](?![a-z])|%| million| billion)?)?/g;
function kvKeep(m, prev) {
  const t = m.trim().replace(/^[▲▼]\s?/, '');
  if (/^(19|20)\d\d\s/.test(t)) return false;
  if (/^[−-]\d+$/.test(t) || /^(19|20)\d\d$/.test(t) || /^(19|20)\d\d[–-](19|20)?\d\d$/.test(t)) return false;
  if (/(Route |Q|SR-|I-|No\. |District |Line |Phase |Lot |Dock )$/.test(prev) || /[A-Za-z]$/.test(prev)) return false;
  return /[$%]|\d,\d|\d\.\d|[MBK]$|million|billion|points|pts|days?|nights|jobs|visitors|vehicles|rooms|seats/.test(t);
}
function runs(text, base = {}) {
  const out = []; let last = 0; text = String(text);
  text.replace(KV_RX, (m, off) => {
    if (!m.trim() || !kvKeep(m, text.slice(Math.max(0, off - 10), off))) return m;
    const lead = m.match(/^\s*/)[0].length;
    if (off + lead > last) out.push({ text: text.slice(last, off + lead), options: { ...base } });
    out.push({ text: m.slice(lead), options: { ...base, bold: true, color: H.e3 } }); last = off + m.length; return m;
  });
  if (last < text.length) out.push({ text: text.slice(last), options: { ...base } });
  return out.length ? out : [{ text, options: { ...base } }];
}
function bullets(s, items, x, y, w, h, fs = 13) {
  const arr = [];
  items.forEach((t, i) => {
    const r = runs(t);
    r.forEach(x => { x.options = { ...x.options, align: 'left', bullet: { indent: 14 }, paraSpaceAfter: 6 }; });
    if (i < items.length - 1) r[r.length - 1].options.breakLine = true;
    arr.push(...r);
  });
  s.addText(arr, ft({ x, y, w, h, fontSize: fs, color: H.dark, valign: 'top' }));
}
function paras(s, items, x, y, w, h, fs = 12) {
  const arr = [];
  items.forEach((t, i) => { const r = runs(t); r.forEach(q => { q.options = { ...q.options, align: 'left', paraSpaceAfter: 8 }; }); if (i < items.length - 1) r[r.length - 1].options.breakLine = true; arr.push(...r); });
  s.addText(arr, ft({ x, y, w, h, fontSize: fs, color: H.dark, valign: 'top' }));
}
function rich(s, text, o) { s.addText(runs(text), ft(Object.assign({ color: H.dark, valign: 'top' }, o))); }
const sec = id => D.sections.find(s => s.id === id);
const EI = D.ei, N = D.N;

