
/* ===== OC Vibe edition ===== */
const sp = sec('p-spend'), im = sec('p-impact'), nt = sec('p-night'), tr = sec('p-transport'), wv = sec('p-d5'), md = sec('p-media'), ht = sec('p-hotel'), lo = sec('p-larc');
const n0 = v => Math.round(v).toLocaleString('en-US');
const tbl = (s, t, x, y, w, o = {}) => {
  const ci = t.cols.findIndex(c => c[0] === "How it's calculated");
  if (ci >= 0 && o.colW && o.colW.length === t.cols.length - 1) {
    const cw = w * 0.36, sc = (w - cw) / o.colW.reduce((a, b) => a + b, 0);
    o = Object.assign({}, o, { colW: [...o.colW.map(v => v * sc), cw], fs: Math.min(o.fs || 10.5, 8.5), rowH: Math.max(o.rowH || 0.32, 0.36) });
  }
  return table(s, t.cols, t.rows, x, y, w, Object.assign({ hi: t.hi }, o));
};
const htCal = ht.tables.find(t => t.title.startsWith('When Anaheim hotels have room')); ht.tables = ht.tables.filter(t => t !== htCal);
const loFacts = lo.tables.find(t => t.title === 'OC Vibe in recent public sources');
/* What it means for OC Vibe: one slide per section (OC Vibe as a whole; enhancements and needs) */
function ocvSlide(id) {
  const x = sec(id); if (!x || !x.for_ocv) return;
  const t = content(x.tab, 'What it means for OC Vibe: ' + x.tab, 'What this insight enhances for OC Vibe, and what OC Vibe needs to act on it', '');
  t.addShape(pres.shapes.RECTANGLE, { x: M, y: 1.55, w: W - 2 * M, h: 1.0, fill: { color: H.e4 }, line: { color: H.e4 } });
  t.addText('KEY INSIGHT', ft({ x: M + 0.15, y: 1.6, w: 2, h: 0.22, fontSize: 9, bold: true, color: H.e3, charSpacing: 1 }));
  rich(t, x.ans, { x: M + 0.15, y: 1.82, w: W - 2 * M - 0.3, h: 0.7, fontSize: 11 });
  const cw = (W - 2 * M - 0.3) / 2;
  [['WHAT IT ENHANCES', x.for_ocv.enhance], ['WHAT OC VIBE NEEDS', x.for_ocv.need]].forEach(([h, items], j) => {
    const bx = M + j * (cw + 0.3);
    t.addShape(pres.shapes.RECTANGLE, { x: bx, y: 2.7, w: cw, h: 0.05, fill: { color: j ? H.e3 : H.e1 }, line: { color: j ? H.e3 : H.e1 } });
    t.addText(h, ft({ x: bx, y: 2.8, w: cw, h: 0.28, fontSize: 10, bold: true, color: H.e3, charSpacing: 1 }));
    bullets(t, items.map(i => i.tag + ': ' + i.text + (i.calc ? ' [Calculation: ' + i.calc + ']' : '')), bx, 3.12, cw, 3.35, items.some(i => i.calc) ? 8 : (items.length > 3 ? 9.5 : 10.5));
  });
  const srcs = [...new Set([x.ans_src, ...x.for_ocv.enhance.map(i => i.src), ...x.for_ocv.need.map(i => i.src)].join('; ').split('; '))];
  source(t, srcs.join('; '));
}

/* Newsroom structure (Oct. 13, 2026): each section opens with a news report (dateline, lede, nut graph, by the numbers)
   and a details slide of six announcement-style data cards, then its analysis slides. Facts only; no opinion. */
function newsSlides(id) {
  KIND = '';
  const x = sec(id); if (!x || !x.details) { KIND = 'Analysis'; return; }
  const prev = D.sections[D.sections.indexOf(x) - 1];
  let t = content(x.tab, x.head, 'News report · ' + x.tab + ' · ' + x.period, (prev && prev.next ? 'Why this section follows ' + prev.tab + ': ' + prev.next.bridge + '\n\n' : '') + x.notes.join('\n'));
  const lw = 7.75;
  t.addText('THE LEDE', ft({ x: M, y: 1.62, w: lw, h: 0.25, fontSize: 10, bold: true, color: H.e3, charSpacing: 1 }));
  t.addText([{ text: x.dateline + ' ', options: { bold: true, color: H.e3 } }, ...runs(x.ans)], ft({ x: M, y: 1.9, w: lw, h: 2.15, fontSize: 13.5, color: H.dark, valign: 'top' }));
  t.addShape(pres.shapes.RECTANGLE, { x: M, y: 4.18, w: lw, h: 0.05, fill: { color: H.e3 }, line: { color: H.e3 } });
  t.addText('WHY IT MATTERS', ft({ x: M, y: 4.3, w: lw, h: 0.25, fontSize: 10, bold: true, color: H.e3, charSpacing: 1 }));
  rich(t, x.nut, { x: M, y: 4.58, w: lw, h: 1.85, fontSize: 12.5 });
  const cx = M + lw + 0.4, cw = W - M - cx;
  t.addText('BY THE NUMBERS', ft({ x: cx, y: 1.62, w: cw, h: 0.25, fontSize: 10, bold: true, color: H.e3, charSpacing: 1 }));
  x.cards.slice(0, 3).forEach(([k, l, v, sub, src], i) => {
    const y = 1.92 + i * 1.5;
    t.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx, y, w: cw, h: 1.4, fill: { color: H.white }, line: { color: H.e4, width: 1 }, rectRadius: 0.06, objectName: 'news-stat-' + i });
    t.addText(k.toUpperCase(), ft({ x: cx + 0.15, y: y + 0.08, w: cw - 0.3, h: 0.22, fontSize: 8.5, bold: true, color: H.e3, charSpacing: 1, fit: 'shrink' }));
    t.addText(v, ft({ x: cx + 0.15, y: y + 0.3, w: cw - 0.3, h: 0.45, fontSize: 22, bold: true, italic: true, color: H.e3 }));
    t.addText(l, ft({ x: cx + 0.15, y: y + 0.76, w: cw - 0.3, h: 0.3, fontSize: 10.5, bold: true, color: H.dark, fit: 'shrink' }));
    t.addText('Source: ' + src, ft({ x: cx + 0.15, y: y + 1.06, w: cw - 0.3, h: 0.28, fontSize: 7.5, color: H.dark, fit: 'shrink' }));
  });
  source(t, x.ans_src);
  t = content(x.tab, 'The details: ' + x.tab, 'News report · who, what, when, where, why and how, each with its figure, source and date', '');
  const gw = (W - 2 * M - 0.36) / 3, ch = 2.38;
  x.details.forEach((d, i) => {
    const px = M + (i % 3) * (gw + 0.18), py = 1.55 + Math.floor(i / 3) * (ch + 0.1);
    t.addShape(pres.shapes.RECTANGLE, { x: px, y: py, w: gw, h: ch, fill: { color: H.white }, line: { color: H.e4, width: 1 }, objectName: 'detail-card-' + i });
    t.addShape(pres.shapes.RECTANGLE, { x: px, y: py, w: gw, h: 0.07, fill: { color: H.e1 }, line: { color: H.e1 } });
    t.addText(d.k.toUpperCase(), ft({ x: px + 0.15, y: py + 0.14, w: gw - 0.3, h: 0.22, fontSize: 9, bold: true, color: H.e3, charSpacing: 1.5 }));
    t.addText(d.fig, ft({ x: px + 0.15, y: py + 0.36, w: gw - 0.3, h: 0.48, fontSize: 22, bold: true, italic: true, color: H.e3, fit: 'shrink' }));
    t.addText(d.fig_l, ft({ x: px + 0.15, y: py + 0.84, w: gw - 0.3, h: 0.38, fontSize: 10, bold: true, color: H.dark, fit: 'shrink', valign: 'top' }));
    rich(t, d.text, { x: px + 0.15, y: py + 1.24, w: gw - 0.3, h: ch - 1.58, fontSize: 9.5, fit: 'shrink' });
    t.addText('Source: ' + d.src, ft({ x: px + 0.15, y: py + ch - 0.33, w: gw - 0.3, h: 0.28, fontSize: 7, color: H.dark, valign: 'bottom', fit: 'shrink' }));
  });
  source(t, x.w5h.src);
  infoSlide(id);
  KIND = 'Analysis';
  mapSlides(id);
}

/* Data infographics (Oct. 13, 2026): one "At a glance" slide per section, drawn with native shapes (editable, no images) */
function igDraw(t, g, X, Y, Wd, Hd) {
  t.addText(g.title, ft({ x: X, y: Y, w: Wd, h: 0.36, fontSize: 15, bold: true, italic: true, color: H.e3, fit: 'shrink' }));
  if (g.sub) t.addText(g.sub, ft({ x: X, y: Y + 0.36, w: Wd, h: 0.26, fontSize: 9.5, color: H.dark, fit: 'shrink' }));
  const y0 = Y + 0.72, h0 = Hd - 0.72;
  const R = pres.shapes.RECTANGLE;
  if (g.kind === 'chain') {
    const n = g.steps.length, lw = 0.95, bw = (Wd - lw * (n - 1)) / n;
    g.steps.forEach((st, i) => {
      const bx = X + i * (bw + lw);
      t.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: bx, y: y0, w: bw, h: 2.2, fill: { color: H.light }, line: { color: H.e4, width: 1 }, rectRadius: 0.06 });
      t.addShape(R, { x: bx, y: y0, w: bw, h: 0.07, fill: { color: H.e3 }, line: { color: H.e3, width: 0 } });
      t.addText(st.v, ft({ x: bx + 0.12, y: y0 + 0.3, w: bw - 0.24, h: 0.75, fontSize: 25, bold: true, italic: true, color: H.e3, fit: 'shrink' }));
      t.addText(st.l, ft({ x: bx + 0.12, y: y0 + 1.1, w: bw - 0.24, h: 1.0, fontSize: 12, bold: true, color: H.dark, valign: 'top', fit: 'shrink' }));
      if (i < n - 1) {
        t.addShape(pres.shapes.LINE, { x: bx + bw + 0.08, y: y0 + 0.75, w: lw - 0.16, h: 0, line: { color: H.e1, width: 3, endArrowType: 'triangle' } });
        t.addText(g.links[i], ft({ x: bx + bw + 0.02, y: y0 + 0.88, w: lw - 0.04, h: 1.2, fontSize: 8.5, color: H.dark, align: 'center', valign: 'top', fit: 'shrink' }));
      }
    });
  } else if (g.kind === 'waffle') {
    const n = g.items.length, cw = Wd / n, cell = Math.min(0.24, (cw - 0.6) / 10), gap = cell * 0.14;
    g.items.forEach((it, j) => {
      const gx = X + j * cw, k0 = Math.round(it.pct);
      for (let k = 0; k < 100; k++) t.addShape(R, { x: gx + (k % 10) * (cell + gap), y: y0 + Math.floor(k / 10) * (cell + gap), w: cell, h: cell, fill: { color: k < k0 ? H.e1 : 'E3E2DA' }, line: { color: k < k0 ? H.e1 : 'E3E2DA', width: 0 } });
      const ty = y0 + 10 * (cell + gap) + 0.08;
      t.addText(it.pct.toFixed(1) + '%', ft({ x: gx, y: ty, w: cw - 0.2, h: 0.4, fontSize: 20, bold: true, italic: true, color: H.e3 }));
      t.addText(it.l + ' (' + k0 + ' of every 100)', ft({ x: gx, y: ty + 0.4, w: cw - 0.3, h: 0.5, fontSize: 10, bold: true, color: H.dark, valign: 'top', fit: 'shrink' }));
    });
  } else if (g.kind === 'receipt') {
    const rw = Wd * 0.56, lh = 0.6;
    t.addShape(R, { x: X, y: y0, w: rw, h: lh * g.lines.length + 0.85, fill: { color: H.white }, line: { color: H.e4, width: 1 } });
    g.lines.forEach((ln, i) => {
      const ly = y0 + 0.1 + i * lh;
      t.addText(ln.l, ft({ x: X + 0.15, y: ly, w: rw - 1.4, h: 0.26, fontSize: 11, bold: true, color: H.dark }));
      t.addText(ln.v, ft({ x: X + rw - 1.25, y: ly, w: 1.1, h: 0.26, fontSize: 12.5, bold: true, color: H.e3, align: 'right' }));
      t.addShape(R, { x: X + 0.15, y: ly + 0.3, w: (rw - 0.3) * ln.pct / 100, h: 0.07, fill: { color: H.e1 }, line: { color: H.e1, width: 0 } });
      t.addText(ln.calc + ' · ' + ln.pct + '% of spending', ft({ x: X + 0.15, y: ly + 0.38, w: rw - 0.3, h: 0.2, fontSize: 7.5, color: H.dark }));
    });
    const ty = y0 + 0.1 + g.lines.length * lh;
    t.addShape(pres.shapes.LINE, { x: X + 0.15, y: ty, w: rw - 0.3, h: 0, line: { color: H.dark, width: 1.5 } });
    t.addText(g.total.l.toUpperCase(), ft({ x: X + 0.15, y: ty + 0.08, w: rw - 1.6, h: 0.3, fontSize: 11, bold: true, color: H.dark }));
    t.addText(g.total.v, ft({ x: X + rw - 1.45, y: ty + 0.05, w: 1.3, h: 0.36, fontSize: 18, bold: true, italic: true, color: H.e3, align: 'right' }));
    t.addText(g.total.calc, ft({ x: X + 0.15, y: ty + 0.42, w: rw - 0.3, h: 0.3, fontSize: 7.5, color: H.dark, fit: 'shrink' }));
    const mx = X + rw + 0.4, mw = Wd - rw - 0.4, cols = ['125C60', '43A3A3', '77C7C9', 'B4D9E3', 'C9C6B8'];
    t.addText('Every $1 of visitor spending', ft({ x: mx, y: y0, w: mw, h: 0.3, fontSize: 12, bold: true, color: H.e3 }));
    let sx = mx; g.lines.forEach((ln, i) => { const sw = mw * ln.pct / 100; t.addShape(R, { x: sx, y: y0 + 0.4, w: sw, h: 0.45, fill: { color: cols[i] }, line: { color: H.white, width: 0.5 } }); sx += sw; });
    g.lines.forEach((ln, i) => {
      const ly = y0 + 1.05 + i * 0.42;
      t.addShape(R, { x: mx, y: ly + 0.08, w: 0.16, h: 0.16, fill: { color: cols[i] }, line: { color: cols[i], width: 0 } });
      t.addText([{ text: Math.round(ln.pct) + '¢  ', options: { bold: true, italic: true, color: H.e3, fontSize: 14 } }, { text: ln.l + ' (' + ln.pct + '%)', options: { color: H.dark, fontSize: 10.5 } }], ft({ x: mx + 0.25, y: ly, w: mw - 0.25, h: 0.34 }));
    });
  } else if (g.kind === 'people') {
    const full = Math.floor(g.pct / 10), part = (g.pct % 10) / 10, iw = 0.62;
    for (let k = 0; k < 10; k++) {
      const px = X + k * (iw + 0.18), on = k < full, f = k === full ? part : (on ? 1 : 0);
      t.addShape(pres.shapes.OVAL, { x: px + iw * 0.25, y: y0, w: iw * 0.5, h: iw * 0.5, fill: { color: on || f >= 0.5 ? H.e1 : H.e4 }, line: { color: H.white, width: 0 } });
      t.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: px, y: y0 + iw * 0.58, w: iw, h: iw * 1.6, fill: { color: H.e4 }, line: { color: H.white, width: 0 }, rectRadius: 0.12 });
      if (f > 0) t.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: px, y: y0 + iw * 0.58, w: iw * f, h: iw * 1.6, fill: { color: H.e1 }, line: { color: H.white, width: 0 }, rectRadius: f < 1 ? 0.02 : 0.12 });
    }
    t.addText(g.v, ft({ x: X + 8.2, y: y0, w: Wd - 8.2, h: 0.7, fontSize: 36, bold: true, italic: true, color: H.e3 }));
    t.addText(g.l, ft({ x: X + 8.2, y: y0 + 0.75, w: Wd - 8.2, h: 0.8, fontSize: 12, bold: true, color: H.dark, valign: 'top' }));
  } else if (g.kind === 'towers') {
    const n = g.nights.length, cw = Wd / n, th = Math.min(2.4, h0 - 0.8);
    g.nights.forEach((nt, i) => {
      const cx = X + i * cw + cw * 0.15, w = cw * 0.7;
      t.addShape(R, { x: cx, y: y0, w, h: th, fill: { color: H.light }, line: { color: H.e4, width: 1 } });
      const fh = th * nt.v / 100; t.addShape(R, { x: cx, y: y0 + th - fh, w, h: fh, fill: { color: nt.hi ? H.e1 : H.e4 }, line: { color: nt.hi ? H.e1 : H.e4, width: 0 } });
      t.addText(nt.v + '%', ft({ x: X + i * cw, y: y0 + th + 0.05, w: cw, h: 0.3, fontSize: 11, bold: true, color: H.dark, align: 'center' }));
      t.addText(nt.l.toUpperCase(), ft({ x: X + i * cw, y: y0 + th + 0.33, w: cw, h: 0.25, fontSize: 9, bold: true, color: H.dark, align: 'center' }));
    });
  } else if (g.kind === 'share') {
    t.addShape(R, { x: X, y: y0 + 0.1, w: Wd, h: 0.8, fill: { color: H.e4 }, line: { color: H.e4, width: 0 } });
    t.addShape(R, { x: X, y: y0 + 0.1, w: Math.max(0.04, Wd * g.pct / 100), h: 0.8, fill: { color: H.e3 }, line: { color: H.e3, width: 0 } });
    t.addText([{ text: g.part.v + ' ', options: { bold: true, italic: true, fontSize: 18, color: H.e3 } }, { text: g.part.l + ' (' + g.pct + '%)', options: { fontSize: 11, color: H.dark } }], ft({ x: X, y: y0 + 1.05, w: Wd / 2, h: 0.5 }));
    t.addText([{ text: g.whole.v + ' ', options: { bold: true, italic: true, fontSize: 18, color: H.e3 } }, { text: g.whole.l, options: { fontSize: 11, color: H.dark } }], ft({ x: X + Wd / 2, y: y0 + 1.05, w: Wd / 2, h: 0.5, align: 'right' }));
    t.addText('Calculation: ' + g.calc, ft({ x: X, y: y0 + 1.6, w: Wd, h: 0.3, fontSize: 9.5, color: H.dark }));
  } else if (g.kind === 'board') {
    const bh = 0.45 * (g.rows.length + 2) + 0.1, mxn = Math.max(...g.rows.map(r => r.n));
    t.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: X, y: y0, w: Wd, h: bh, fill: { color: H.e3 }, line: { color: H.e3, width: 0 }, rectRadius: 0.06 });
    ['ROUTE', 'CORRIDOR', 'WEEKDAY TRIPS'].forEach((hh, i) => t.addText(hh, ft({ x: X + [0.2, 1.2, Wd * 0.62][i], y: y0 + 0.1, w: 3, h: 0.3, fontSize: 9, bold: true, color: H.white, charSpacing: 1 })));
    [...g.rows, { r: 'All', d: g.total.l + ' (' + g.total.calc + ')', n: g.total.n, tot: true }].forEach((r, i) => {
      const ry = y0 + 0.5 + i * 0.45;
      t.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: X + 0.2, y: ry, w: 0.75, h: 0.34, fill: { color: r.tot ? H.white : H.e1 }, line: { color: H.white, width: 0 }, rectRadius: 0.04 });
      t.addText(r.r, ft({ x: X + 0.2, y: ry, w: 0.75, h: 0.34, fontSize: 13, bold: true, color: r.tot ? H.e3 : H.white, align: 'center', valign: 'middle' }));
      t.addText(r.d, ft({ x: X + 1.2, y: ry, w: Wd * 0.62 - 1.3, h: 0.34, fontSize: 11, color: H.white, valign: 'middle', fit: 'shrink' }));
      if (!r.tot) { t.addShape(R, { x: X + Wd * 0.62, y: ry + 0.12, w: (Wd * 0.3) * r.n / mxn, h: 0.1, fill: { color: H.e4 }, line: { color: H.e4, width: 0 } }); }
      t.addText(String(r.n), ft({ x: X + Wd - 0.9, y: ry, w: 0.75, h: 0.34, fontSize: 14, bold: true, color: H.white, align: 'right', valign: 'middle' }));
    });
    const ew = (Wd - 0.4) / g.extra.length;
    g.extra.forEach((e, i) => {
      const ex = X + i * (ew + 0.2), ey = y0 + bh + 0.15;
      t.addShape(R, { x: ex, y: ey, w: ew, h: 0.85, fill: { color: H.white }, line: { color: H.e4, width: 1 } });
      t.addText(e.v, ft({ x: ex + 0.12, y: ey + 0.05, w: ew - 0.24, h: 0.4, fontSize: 18, bold: true, italic: true, color: H.e3 }));
      t.addText(e.l, ft({ x: ex + 0.12, y: ey + 0.45, w: ew - 0.24, h: 0.35, fontSize: 9.5, color: H.dark, fit: 'shrink' }));
    });
  } else if (g.kind === 'funnel') {
    g.stages.forEach((st, i) => {
      const w = i ? Wd * 0.5 : Wd * 0.9, fx = X + (Wd - w) / 2, fy = y0 + i * 1.0;
      t.addShape(pres.shapes.TRAPEZOID, { x: fx, y: fy, w, h: 0.9, fill: { color: i ? H.e1 : H.e4 }, line: { color: H.white, width: 0 }, flipV: true });
      t.addText(st.v, ft({ x: fx, y: fy + 0.08, w, h: 0.45, fontSize: 22, bold: true, italic: true, color: H.dark, align: 'center' }));
      t.addText(st.l, ft({ x: fx, y: fy + 0.52, w, h: 0.3, fontSize: 10, bold: true, color: H.dark, align: 'center' }));
    });
    const rw = (Wd - 0.3) / g.rates.length;
    g.rates.forEach((r, i) => {
      const rx = X + i * (rw + 0.3), ry = y0 + 2.15;
      t.addShape(R, { x: rx, y: ry, w: rw, h: 0.05, fill: { color: H.e3 }, line: { color: H.e3, width: 0 } });
      t.addText(r.v, ft({ x: rx, y: ry + 0.1, w: rw, h: 0.42, fontSize: 20, bold: true, italic: true, color: H.e3 }));
      t.addText(r.l, ft({ x: rx, y: ry + 0.52, w: rw, h: 0.28, fontSize: 10.5, bold: true, color: H.dark }));
      t.addText(r.calc, ft({ x: rx, y: ry + 0.8, w: rw, h: 0.26, fontSize: 9, color: H.dark }));
    });
  } else if (g.kind === 'versus') {
    const mxv = Math.max(...g.rows.flatMap(r => [r.a, r.b])), lw = 3.0, bwid = Wd - lw - 0.2;
    g.rows.forEach((r, i) => {
      const ry = y0 + i * 1.15;
      t.addText(r.l, ft({ x: X, y: ry, w: lw, h: 0.9, fontSize: 12, bold: true, color: H.dark, valign: 'middle' }));
      [[r.la, r.a, H.e1], [r.lb, r.b, H.e4]].forEach(([lab, v, col], j) => {
        const by = ry + 0.05 + j * 0.42;
        t.addShape(R, { x: X + lw + 0.2, y: by, w: bwid, h: 0.36, fill: { color: H.light }, line: { color: H.light, width: 0 } });
        t.addShape(R, { x: X + lw + 0.2, y: by, w: bwid * v / mxv, h: 0.36, fill: { color: col }, line: { color: col, width: 0 } });
        t.addText([{ text: lab + ' ', options: { color: H.dark, fontSize: 10.5 } }, { text: '+' + v + '%', options: { color: H.dark, fontSize: 11, bold: true } }], ft({ x: X + lw + 0.3, y: by, w: bwid - 0.2, h: 0.36, valign: 'middle' }));
      });
    });
  }
}
function infoSlide(id) {
  const x = sec(id); if (!x || !(x.info || []).length) return;
  const t = content(x.tab, 'At a glance: ' + x.tab, 'News report · data infographic' + (x.info.length > 1 ? 's' : '') + ' · every figure from this section, with its source and date', '');
  const n = x.info.length, gw = (W - 2 * M - 0.4 * (n - 1)) / n;
  x.info.forEach((g, i) => igDraw(t, g, M + i * (gw + 0.4), 1.55, gw, 4.9));
  const used = { chain: 3.0, people: 2.0, share: 2.6, towers: 3.6, waffle: 4.2, receipt: 4.9, board: 4.3, funnel: 4.15, versus: 3.9 };
  const top = 1.55 + Math.max(...x.info.map(g => used[g.kind] || 4.9)) + 0.25;
  if (x.nut && 6.45 - top > 0.9) {
    t.addShape(pres.shapes.RECTANGLE, { x: M, y: top, w: W - 2 * M, h: 0.05, fill: { color: H.e3 }, line: { color: H.e3, width: 0 } });
    t.addText('WHY IT MATTERS', ft({ x: M, y: top + 0.1, w: 3, h: 0.25, fontSize: 10, bold: true, color: H.e3, charSpacing: 1 }));
    rich(t, x.nut, { x: M, y: top + 0.38, w: W - 2 * M, h: Math.min(1.6, 6.45 - top - 0.4), fontSize: 12.5 });
  }
  source(t, [...new Set(x.info.map(g => g.src))].join('; '));
}

/* Maps (Oct. 13, 2026): one slide per map, rendered from the same map renderer as the dashboard (maps_render.js) */
function mapSlides(id) {
  const x = sec(id); if (!x || !(x.maps || []).length) return;
  x.maps.forEach((m, i) => {
    const file = `map_${id}_${i}.png`; if (!require('fs').existsSync(file)) return;
    const t = content(x.tab, m.title, m.sub, '');
    const ar = m.kind === 'world' ? 960 / 470 : 960 / 600, iw = Math.min(8.7, 4.85 * ar), ih = iw / ar;
    t.addImage({ path: file, x: M, y: 1.55, w: iw, h: ih, altText: m.title + ': ' + [...m.points].sort((a, b) => b.v - a.v).slice(0, 8).map(p => p.name + ' ' + p.t).join(', ') });
    const lx = M + iw + 0.3, lw = W - M - lx; let ly = 1.55;
    if (m.bins) {
      t.addText('STATES', ft({ x: lx, y: ly, w: lw, h: 0.25, fontSize: 9.5, bold: true, color: H.e3, charSpacing: 1 })); ly += 0.3;
      [...m.bins.map((bn, k) => [['125C60', '43A3A3', 'B4D9E3'][k], bn[1]]), ['E9EBE4', m.other]].forEach(([c, l]) => {
        t.addShape(pres.shapes.RECTANGLE, { x: lx, y: ly + 0.04, w: 0.18, h: 0.18, fill: { color: c }, line: { color: 'C9C6B8', width: 0.5 } });
        t.addText(l, ft({ x: lx + 0.28, y: ly, w: lw - 0.3, h: 0.26, fontSize: 10, color: H.dark })); ly += 0.3; });
      ly += 0.15;
    }
    t.addText((m.kind === 'world' ? 'COUNTRIES' : 'METRO AREAS') + ' (CIRCLES)', ft({ x: lx, y: ly, w: lw, h: 0.25, fontSize: 9.5, bold: true, color: H.e3, charSpacing: 1 })); ly += 0.32;
    const fmt = p => m.unit === 'money' ? '$' + (p.v >= 1 ? p.v.toFixed(1) + 'M' : Math.round(p.v * 1000) + 'K') : p.t;
    [...m.points].sort((a, b) => b.v - a.v).slice(0, 8).forEach((p, k) => {
      t.addText([{ text: fmt(p) + '  ', options: { bold: true, color: H.e3, fontSize: 12 } }, { text: p.name, options: { color: H.dark, fontSize: 10 } }], ft({ x: lx, y: ly, w: lw, h: 0.3, fit: 'shrink' })); ly += 0.33; });
    source(t, m.src + '. Map: U.S. Census Bureau boundaries (us-atlas); Natural Earth 1:110m (world-atlas); circles at each metro\'s principal city or country\'s center.');
  });
}
/* Key takeaways (Oct. 13, 2026): one bold headline number per section */
function keyTakeawaysSlide() {
  const secs = D.sections.filter(x => x.id !== 'p-appx'); if (!secs.length) return;
  const t = content('Introduction', 'Key takeaways', 'The headline number from each section, with its period', '');
  const cols = 3, gw = (W - 2 * M - 0.36) / cols, ch = 1.55;
  secs.forEach((x, i) => {
    const cx = M + (i % cols) * (gw + 0.18), cy = 1.5 + Math.floor(i / cols) * (ch + 0.1);
    t.addShape(pres.shapes.RECTANGLE, { x: cx, y: cy, w: gw, h: ch, fill: { color: H.white }, line: { color: H.e4, width: 1 } });
    t.addShape(pres.shapes.RECTANGLE, { x: cx, y: cy, w: gw, h: 0.06, fill: { color: H.e1 }, line: { color: H.e1, width: 0 } });
    t.addText(x.tab.toUpperCase(), ft({ x: cx + 0.12, y: cy + 0.1, w: gw - 0.24, h: 0.22, fontSize: 8.5, bold: true, color: H.e3, charSpacing: 1 }));
    t.addText(x.hv, ft({ x: cx + 0.12, y: cy + 0.32, w: 1.9, h: 0.5, fontSize: 24, bold: true, italic: true, color: H.e3, fit: 'shrink' }));
    t.addText(x.hl, ft({ x: cx + 2.05, y: cy + 0.34, w: gw - 2.15, h: 0.48, fontSize: 9.5, bold: true, color: H.dark, valign: 'middle', fit: 'shrink' }));
    rich(t, x.head, { x: cx + 0.12, y: cy + 0.86, w: gw - 0.24, h: 0.62, fontSize: 10, fit: 'shrink' });
  });
  source(t, 'Each figure with its source and period on its section slides. Visit Anaheim Business Intelligence (Oct. 13, 2026).');
}

/* How the key insight is calculated: step table per section (calculated steps and reported inputs) */
function calcSlide(id, title) {
  const x = sec(id); if (!x || !x.calc_steps || !x.calc_steps.some(r => r[1] !== 'Reported')) return;
  const t = content(x.tab, title || ('How the numbers are calculated: ' + x.tab), 'Each step with its calculation, result and source', '');
  const rows = x.calc_steps.map(r => [r[0], r[1] === 'Reported' ? 'Reported by source' : r[1], r[2], r[3]]);
  const n = rows.length, rh = Math.min(0.42, 4.7 / (n + 1));
  table(t, [['Step', 0], ['Calculation', 0], ['Result', 1], ['Source', 0]], rows, M, 1.55, W - 2 * M, { colW: [2.5, 5.6, 1.4, 2.63], rowH: rh, fs: n > 8 ? 8.5 : 9.5, hi: rows.findIndex(r => /^7\./.test(r[0])) });
  source(t, [...new Set(rows.map(r => r[3]))].join('; '));
}
function wfSlide() {
  const x = sec('p-ocv'), wf = (x.feature || []).find(c => c.kind === 'wf'), rg = (x.feature || []).find(c => c.kind === 'range'); if (!wf) return;
  const t = content('OC Vibe impact', wf.title, wf.sub, '');
  let run = 0; const base = [], val = [];
  wf.steps.forEach(st => { if (st.total) { base.push(0); val.push(st.v); } else { base.push(run); val.push(st.v); run += st.v; } });
  t.addChart(pres.charts.BAR, [{ name: 'Base', labels: wf.steps.map(st => st.l + '\n' + st.t + '\n' + (st.note || '')), values: base }, { name: 'Value', labels: wf.steps.map(st => st.l + '\n' + st.t + '\n' + (st.note || '')), values: val }],
    { x: M, y: 1.6, w: 6.6, h: 4.6, barDir: 'col', barGrouping: 'stacked', chartColors: ['FFFFFF', H.e1], valAxisHidden: true, valGridLine: { style: 'none' },
      catAxisLabelColor: H.dark, catAxisLabelFontSize: 10, catAxisLabelFontFace: 'Proxima Nova', showLegend: false, barGapWidthPct: 60,
      showValue: false, objectName: 'waterfall' });
  if (rg) {
    t.addText(rg.title, ft({ x: 7.5, y: 1.6, w: W - M - 7.5, h: 0.6, fontSize: 13, bold: true, color: H.e3 }));
    const rows = rg.marks.map(mk => [mk.l.split(' $')[0], '$' + mk.l.split(' $')[1]]).concat([['90% range (5th–95th percentile)', '$' + Math.round(rg.lo) + 'M–$' + Math.round(rg.hi) + 'M']]);
    table(t, [['Case', 0], ['New visitor spending', 1]], rows, 7.5, 2.3, W - M - 7.5, { colW: [2.9, W - M - 7.5 - 2.9], rowH: 0.42, fs: 10.5, hi: 1 });
    rich(t, 'The range comes from 200,000 simulations that vary each assumption between its conservative and optimistic values.', { x: 7.5, y: 4.9, w: W - M - 7.5, h: 0.9, fontSize: 10.5 });
  }
  source(t, wf.src + '; Tourism Economics (2025).');
}
function lineSlide(id, kindTitle) {
  const x = sec(id), ln = (x.feature || []).find(c => c.kind === 'line'); if (!ln) return;
  const t = content(x.tab, ln.title, ln.sub, '');
  t.addChart(pres.charts.LINE, ln.series.map(sr => ({ name: sr.name, labels: ln.x, values: sr.v })), { x: M, y: 1.6, w: W - 2 * M, h: 4.7, chartColors: ln.series.map(sr => sr.focal ? H.e1 : H.e2),
    lineSize: 3, lineDataSymbol: 'circle', lineDataSymbolSize: 6, catAxisLabelColor: H.dark, catAxisLabelFontSize: 10, valAxisLabelColor: H.dark, valAxisLabelFontSize: 10,
    valGridLine: { color: 'D9D9D9', size: 0.5 }, catGridLine: { style: 'none' }, valAxisLabelFormatCode: (ln.yfmt && ln.yfmt.suf === '%') ? '0"%"' : '0"M"', showLegend: ln.series.length > 1, legendPos: 'b', legendFontSize: 10,
    showValue: true, dataLabelPosition: 't', dataLabelFontSize: 9, dataLabelColor: H.dark, dataLabelFormatCode: (ln.yfmt && ln.yfmt.suf === '%') ? '+0"%"' : '0.0"M"', objectName: 'line' });
  source(t, ln.src + '.');
}

/* Title */
pres.addSection({ title: 'Introduction' });
let s = pres.addSlide({ masterName: 'VA Title', sectionTitle: 'Introduction' });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 0.7, w: 3.0, h: 3.0 / LOGO_AR + 0.3, fill: { color: H.light }, line: { color: H.light }, rectRadius: 0.1, objectName: 'logo-plate' });
s.addImage({ data: LOGO, x: M + 0.15, y: 0.85, w: 2.7, h: 2.7 / LOGO_AR, altText: 'Visit Anaheim' });
s.addText('Visitor insights for OC Vibe', { placeholder: 'title' });
s.addText('How Anaheim visitors spend, stay, travel and choose where to go, and what the market outlook means for OC Vibe. Anaheim, Orange County and U.S. data through September 2026.', { placeholder: 'sub' });
s.addText('Prepared by Visit Anaheim Business Intelligence · October 2026 · Updated quarterly; next update ' + D.schedule.next, ft({ x: M, y: 6.6, w: 11, h: 0.4, fontSize: 12, color: H.white }));
s.addNotes('Prepared by Visit Anaheim Business Intelligence for OC Vibe (BIREPORTS-966).');

/* Main announcement (mirrors the dashboard overview) and summary of findings */
s = content('Introduction', D.main.head, 'Main announcement · Visit Anaheim Business Intelligence · data through Sept. 2026', D.main.srcs.join('; '));
rich(s, D.main.dek, { x: M, y: 1.5, w: W - 2 * M, h: 0.5, fontSize: 13, bold: true });
kpis(s, D.main.stats.slice(0, 4).map(([v, l, src]) => [src, l, v, '']), M, 2.1, W - 2 * M, 1.35, 24);
paras(s, ['ANAHEIM, Calif. (Oct. 13, 2026): ' + D.main.lede, ...D.main.paras.slice(0, 2)], M, 3.6, W - 2 * M, 2.9, 11);
source(s, D.main.srcs.join('; ') + '.');
s = content('Introduction', 'Main announcement (continued)', 'Groups, access and what the report covers', '');
paras(s, D.main.paras.slice(2), M, 1.6, W - 2 * M, 4.8, 13);
source(s, D.main.srcs.join('; ') + '.');
s = content('Introduction', 'Summary of findings', 'Each finding with its source and date', '');
bullets(s, D.takeaways, M, 1.55, W - 2 * M, 5.0, 10);
source(s, 'Sources and dates are shown with each finding; full source register on the Sources slides.');
keyTakeawaysSlide();
s = content('Introduction', 'How this report reads', 'Each section is a news report (lede, why it matters, the details) followed by analysis · sections in reading order', '');
table(s, [['Section', 0], ['The question it answers', 0], ['Why the next section follows', 0]], D.sections.filter(x => x.id !== 'p-appx').map(x => [x.tab, x.q, x.next ? x.next.tab + ': ' + x.next.bridge : '']), M, 1.55, W - 2 * M, { colW: [2.0, 4.1, 6.03], rowH: 0.5, fs: 8.5, hi: -1 });
source(s, 'Visit Anaheim Business Intelligence (Oct. 13, 2026). Facts only; no editorial or opinion content.');
/* Update schedule (Oct. 14, 2026): who, what, when, where, why and how of the quarterly update */
{ const U = D.schedule;
  s = content('Introduction', 'How this report is updated', U.line, U.lede);
  rich(s, U.lede, { x: M, y: 1.45, w: W - 2 * M, h: 0.62, fontSize: 12 });
  const gw = (W - 2 * M - 0.36) / 3, ch = 2.1;
  U.details.forEach((d, i) => {
    const px = M + (i % 3) * (gw + 0.18), py = 2.15 + Math.floor(i / 3) * (ch + 0.1);
    s.addShape(pres.shapes.RECTANGLE, { x: px, y: py, w: gw, h: ch, fill: { color: H.white }, line: { color: H.e4, width: 1 }, objectName: 'update-card-' + i });
    s.addShape(pres.shapes.RECTANGLE, { x: px, y: py, w: gw, h: 0.07, fill: { color: H.e1 }, line: { color: H.e1 } });
    s.addText(d.k.toUpperCase(), ft({ x: px + 0.15, y: py + 0.13, w: gw - 0.3, h: 0.22, fontSize: 9, bold: true, color: H.e3, charSpacing: 1.5 }));
    s.addText(d.fig, ft({ x: px + 0.15, y: py + 0.34, w: gw - 0.3, h: 0.42, fontSize: 20, bold: true, italic: true, color: H.e3, fit: 'shrink' }));
    s.addText(d.fig_l, ft({ x: px + 0.15, y: py + 0.76, w: gw - 0.3, h: 0.28, fontSize: 10, bold: true, color: H.dark, fit: 'shrink' }));
    rich(s, d.text, { x: px + 0.15, y: py + 1.05, w: gw - 0.3, h: ch - 1.35, fontSize: 9, fit: 'shrink' });
    s.addText('Source: ' + d.src, ft({ x: px + 0.15, y: py + ch - 0.3, w: gw - 0.3, h: 0.26, fontSize: 7, color: H.dark, valign: 'bottom', fit: 'shrink' }));
  });
  source(s, U.src + '. Contact: ' + U.contact + '.'); }

/* Questions answered (Oct. 14, 2026): the four core questions for Anaheim, Orange County and the U.S. */
pres.addSection({ title: 'Questions answered' });
qaCoreSlide('Questions answered');
AQ.core.forEach(id => { qaSlide('Questions answered', QS[id]); qaDetailSlide('Questions answered', QS[id]); });
qaIndexSlide('Questions answered');

/* 0. Anaheim and OC Vibe today (measured data only; no estimates) */
pres.addSection({ title: 'Anaheim and OC Vibe today' });
newsSlides('p-ocv');
const oi = sec('p-ocv'), ot = oi.tables, otT = t => ot.find(x => x.title.startsWith(t));
s = content('Anaheim and OC Vibe today', "Anaheim's visitor economy: 2025 results and 2026 forecast", 'City of Anaheim only · 2025 measured (Tourism Economics, published 2026) · 2026 = Tourism Economics forecast (Sept. 2026)', oi.notes.join('\n'));
kpis(s, oi.cards.map(c => c.slice(0, 4)), M, 1.55, W - 2 * M, 1.6, 22);
tbl(s, otT("Anaheim's visitor economy"), M, 3.3, W - 2 * M, { colW: [2.3, 1.55, 1.55, 1.0, 5.73], rowH: 0.36, fs: 10 });
source(s, 'Tourism Economics, Economic Impact of Visitors (calendar 2025; published 2026); Tourism Economics, Anaheim Travel Forecast (Sept. 2026); Datafy (calendar 2024). City of Anaheim totals; not allocated to OC Vibe.');

function w5hSlide(section, sc, title) {
  const w = sc.w5h; if (!w) return;
  const t = content(section, title, 'The essentials: who, what, when, where, why and how', '');
  const keys = ['who', 'what', 'when', 'where', 'why', 'how'], cw = (W - 2 * M - 0.36) / 3, ch = 2.25;
  keys.forEach((k, i) => {
    const x = M + (i % 3) * (cw + 0.18), y = 1.6 + Math.floor(i / 3) * (ch + 0.15);
    t.addShape(pres.shapes.RECTANGLE, { x, y, w: cw, h: 0.05, fill: { color: H.e1 }, line: { color: H.e1 } });
    t.addText(k.toUpperCase(), ft({ x, y: y + 0.12, w: cw, h: 0.3, fontSize: 11, bold: true, color: H.e3, charSpacing: 1 }));
    rich(t, w[k], { x, y: y + 0.45, w: cw, h: ch - 0.5, fontSize: 12 });
  });
  source(t, w.src);
}

s = content('Anaheim and OC Vibe today', 'The OC Vibe area today, before the new venues open', 'Measured or published figures only · each with its period and source', '');
tbl(s, otT('The OC Vibe area today'), M, 1.55, W - 2 * M, { colW: [4.3, 2.8, 2.1, 2.93], rowH: 0.37, fs: 10 });
source(s, otT('The OC Vibe area today').src + '.');

const mix = otT('Where Anaheim visitor spending goes');
s = content('Anaheim and OC Vibe today', 'Where Anaheim visitor spending goes, by category', 'City of Anaheim, calendar 2025 · Tourism Economics (published 2026) · each share with its calculation', '');
tbl(s, mix, M, 1.6, 7.6, { colW: [2.2, 1.1, 0.9, 3.4], rowH: 0.5, fs: 10 });
hbar(s, 'Share of visitor spending, 2025', mix.rows.slice(0, 5).map(r => r[0]), mix.rows.slice(0, 5).map(r => parseFloat(r[2])), 8.5, 1.6, W - M - 8.5, 4.4, '0.0"%"', 0);
source(s, mix.src + '.');

const kT = otT('Measures OC Vibe can build on');
s = content('Anaheim and OC Vibe today', 'Measures OC Vibe can build on, with today\'s baselines', 'Measured baselines; OC Vibe adds its own results once its venues open', '');
tbl(s, { ...kT, rows: kT.rows.slice(0, 8) }, M, 1.6, W - 2 * M, { colW: [1.3, 3.6, 2.9, 2.6, 1.73], rowH: 0.42, fs: 9.5 });
source(s, kT.src + ' Continued on next slide.');
s = content('Anaheim and OC Vibe today', 'Measures OC Vibe can build on (continued)', 'New markets, spending and access', '');
tbl(s, { ...kT, rows: kT.rows.slice(8) }, M, 1.6, W - 2 * M, { colW: [1.3, 3.6, 2.9, 2.6, 1.73], rowH: 0.42, fs: 9.5 });
source(s, kT.src + '.');

s = content('Anaheim and OC Vibe today', "Figures OC Vibe's developers and others have published", 'Shown as published; not produced or checked by Visit Anaheim BI', '');
tbl(s, otT('Figures OC Vibe'), M, 1.6, W - 2 * M, { colW: [3.2, 5.4, 3.53], rowH: 0.6, fs: 10.5 });
source(s, otT('Figures OC Vibe').src + '.');

/* 1. Visitor spending */
calcSlide('p-ocv', 'How the numbers are calculated: Anaheim and OC Vibe today');
ocvSlide('p-ocv');

/* Orange County tourism statistics (Oct. 19, 2026): the five questions from Entertainment + Culture Advisors */
pres.addSection({ title: 'Orange County tourism' });
newsSlides('p-octour');
{
  const oc = sec('p-octour'), oT = t => oc.tables.find(x => x.title.startsWith(t)), TAB = 'Orange County tourism';
  const fq = oT('The five questions');
  s = content(TAB, 'The five questions and where each is answered', 'Sent by Entertainment + Culture Advisors for OCVIBE, Oct. 19, 2026 · every gap paired with a solution', oc.notes.join('\n'));
  table(s, fq.cols, fq.rows, M, 1.55, W - 2 * M, { colW: [1.4, 3.0, 3.8, 1.7, 2.233], rowH: 0.78, fs: 8, hi: -1 });
  source(s, fq.src);
  const v = oT('1. Visitor arrivals');
  s = content(TAB, 'Question 1. Visitor arrivals to Orange County, 2009–2026', 'Millions · CIC Research 2009–2019 and Tourism Economics 2021–2025 are separate methods', '');
  const keep = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026 YTD'];
  const vr = v.rows.filter(r => keep.includes(r[0]));
  table(s, v.cols, vr, M, 1.55, W - 2 * M, { colW: [1.0, 1.3, 1.1, 1.1, 1.5, 6.133], rowH: 0.36, fs: 9.5, hi: vr.findIndex(r => r[0] === '2025') });
  source(s, v.src + '. 2009–2014 in the dashboard.');
  const sp = oT('1b.');
  s = content(TAB, 'Question 1. Orange County visitor spending, including 2020', 'Dean Runyan Associates for Visit California · $ millions · spending, not visitor counts', '');
  table(s, sp.cols, sp.rows, M, 1.55, 8.0, { colW: [1.2, 1.8, 1.6, 1.6, 1.8], rowH: 0.42, fs: 11, hi: 6 });
  rich(s, 'Orange County visitor spending in 2020 fell to 46.7% of its 2019 level and passed 2019 in 2022. In 2025p it was 21.5% above 2019. Tourism Economics and CIC do not publish 2020 county visitor counts; this series fills the year.', { x: M + 8.3, y: 1.55, w: W - 2 * M - 8.3, h: 3.5, fontSize: 12 });
  source(s, sp.src);
  const o1 = oT('2. Where'), o2 = oT('2b.');
  s = content(TAB, 'Question 2. Where visitors come from', 'Orange County 2019 (CIC) · Anaheim and Garden Grove 2023–2026 (Azira) · LA metro includes Orange County', '');
  table(s, o1.cols, o1.rows, M, 1.55, 7.4, { colW: [2.1, 1.3, 3.0, 1.0], rowH: 0.36, fs: 9, hi: 0 });
  table(s, o2.cols, o2.rows, M + 7.6, 1.55, W - 2 * M - 7.6, { colW: [1.2, 0.9, 1.3, 1.133], rowH: 0.42, fs: 8.5, hi: 0 });
  rich(s, 'No ZIP codes in Azira: the metro area cannot be split into Anaheim and outside Anaheim. Solution: a custom Symphony pull or a new visitor survey.', { x: M + 7.6, y: 4.6, w: W - 2 * M - 7.6, h: 1.6, fontSize: 10.5 });
  source(s, o1.src + '; ' + o2.src);
  const se = oT('3. Seasonality'), ad = oT('3b.');
  s = content(TAB, 'Question 3. Seasonality: Orange County hotel occupancy by month', 'CoStar, % of rooms sold · no monthly county visitor counts are published, so hotel occupancy is the measure', '');
  table(s, se.cols, se.rows.filter(r => !['2020', '2021'].includes(r[0])), M, 1.55, W - 2 * M, { colW: [1.333].concat(Array(12).fill(0.9)), rowH: 0.34, fs: 9.5, hi: 6 });
  table(s, ad.cols, ad.rows.filter(r => ['2019', '2025', '2026', '2023-25 avg.'].includes(r[0])), M, 4.45, W - 2 * M, { colW: [1.333].concat(Array(12).fill(0.9)), rowH: 0.34, fs: 9.5, hi: 3 });
  source(s, se.src + '. Lower table: average daily rate. 2020–2021 in the dashboard.');
  const pf = oT('4. Visitor profile'), pr = oT('4b.');
  s = content(TAB, 'Question 4. Visitor profile: purpose, party size, children and stay', 'CIC Research, Orange County visitors by type of stay, 2019 · the latest county visitor profile', '');
  table(s, pf.cols, pf.rows, M, 1.55, W - 2 * M, { colW: [4.133, 1.6, 1.6, 1.6, 1.6, 1.6], rowH: 0.32, fs: 9.5, hi: -1 });
  source(s, pf.src);
  s = content(TAB, 'Question 4. More recent visitor indicators', 'Each row names its geography and period · none is a full Orange County profile', '');
  table(s, pr.cols, pr.rows, M, 1.55, W - 2 * M, { colW: [2.8, 2.6, 3.4, 3.333], rowH: 0.55, fs: 9.5, hi: -1 });
  source(s, pr.src);
  const ht5 = oT('5. Orange County hotel');
  s = content(TAB, 'Question 5. Orange County hotel inventory, occupancy and ADR', 'CoStar · 2026 is Jan.–Aug. · revenue per available room = occupancy x ADR', '');
  table(s, ht5.cols, ht5.rows, M, 1.55, W - 2 * M, { colW: [1.6, 2.3, 2.0, 1.7, 1.8, 2.733], rowH: 0.4, fs: 10.5, hi: 7 });
  source(s, ht5.src);
  const cc = oT('Compare and contrast');
  s = content(TAB, 'Compare and contrast: how the visitor sources differ', 'Why figures differ by source, and which to use', '');
  table(s, cc.cols, cc.rows, M, 1.55, W - 2 * M, { colW: [1.7, 2.0, 1.9, 2.0, 2.4, 2.133], rowH: 0.7, fs: 9.5, hi: -1 });
  source(s, cc.src);
}
calcSlide('p-octour');
ocvSlide('p-octour');

pres.addSection({ title: 'Who visits' });
newsSlides('p-d5');
s = content('Who visits', 'District 5 profile: income, busiest day and the places visitors also go', 'Symphony | Azira POI analysis, District 5 · Jan. 1–May 31, 2026', wv.notes.join('\n'));
kpis(s, [['District 5', 'Stay overnight', '85.8%', 'New visitors 43.8%'], ['District 5', 'Median household income', '$85.7K', 'All Anaheim/GG visitors $79.9K'], ['District 5', 'Busiest day', 'Saturday', '15.9% of visits']], M, 1.6, 6.2, 1.75, 24);
tbl(s, wv.tables[0], M, 3.6, 6.2, { colW: [4.4, 1.8], rowH: 0.26, fs: 9.5 });
hbar(s, 'Also visited (share of District 5 visitors)', D.d5_poi.slice(0, 8).map(p => p[0]), D.d5_poi.slice(0, 8).map(p => p[1] / 100), 7.1, 1.6, 5.6, 4.8, '0.0%');
source(s, 'Symphony | Tourism Economics, Azira POI Analysis (District 5); U.S. Census Bureau (income)');

s = content('Who visits', 'OC Vibe already appears in 5.2% of Anaheim visitor days', 'Datafy Anaheim visitor report · calendar 2024 · visitors traveling 50+ miles', '');
hbar(s, 'Share of Anaheim visitor days including each cluster', D.datafy.clusters.map(c => c[0]), D.datafy.clusters.map(c => c[1] / 100), M, 1.6, 6.4, 4.8, '0.0%', 5);
tbl(s, wv.tables[2], 7.4, 1.6, 5.3, { colW: [3.6, 1.7], rowH: 0.4 });
s.addText('A visitor day can include several clusters, so shares do not sum to 100%.', ft({ x: 7.4, y: 5.0, w: 5.3, h: 0.5, fontSize: 10.5, color: H.dark }));
source(s, 'Datafy, Anaheim visitor report (Jan. 1–Dec. 31, 2024)');

s = content('Who visits', 'Visitor card spending rose 8.1% in August 2026, with growing fly-in markets', 'Visa Destination Insights via Symphony · August 2026 vs. August 2025', wv.ocv.slice(-2).join('\n'));
const wvn = wv.tables.length, spn = sp.tables.length;
tbl(s, sp.tables[spn - 1], M, 1.6, 6.0, { colW: [2.1, 1.3, 1.3, 1.3], rowH: 0.34, fs: 10 });
tbl(s, wv.tables[wvn - 2], 6.9, 1.6, W - M - 6.9, { colW: [3.3, 1.2, 1.33], rowH: 0.27, fs: 9 });
tbl(s, { ...wv.tables[wvn - 1], rows: wv.tables[wvn - 1].rows.slice(0, 6) }, M, 3.85, 6.0, { colW: [3.2, 1.4, 1.4], rowH: 0.3, fs: 9.5 });
source(s, 'Visa Destination Insights (reported Visa card data) via Symphony | Tourism Economics, Visitor Type and International Card Activity, Aug. 2026 (exported Oct. 12, 2026).');

/* 6. Marketing reach */
ocvSlide('p-d5');

pres.addSection({ title: 'Visitor spending' });
newsSlides('p-spend');
s = content('Visitor spending', `Each Anaheim visitor is forecast to spend $${D.ana_pv[9]} by 2028, up from $${D.ana_pv[0]} in 2019`, 'Average visitor spending · Tourism Economics Anaheim and Garden Grove Travel Forecast, Sept. 2026', sp.notes.join('\n'));
kpis(s, sp.cards.map(c => c.slice(0, 4)), M, 1.6, W - 2 * M, 1.6);
s.addText('Spending per visitor, Anaheim (2026–2028 forecast)', ft({ x: M, y: 3.4, w: 7.2, h: 0.35, fontSize: 13, bold: true, color: H.e3 }));
s.addChart(pres.charts.BAR, [{ name: 'Actual', labels: D.years.map(String), values: D.ana_pv.map((v, i) => D.years[i] <= 2025 ? v : 0) },
                             { name: 'Forecast', labels: D.years.map(String), values: D.ana_pv.map((v, i) => D.years[i] > 2025 ? v : 0) }],
  { x: M, y: 3.75, w: 7.2, h: 2.75, barDir: 'col', barGrouping: 'stacked', chartColors: [H.e1, H.e4], showValue: true, dataLabelPosition: 'inEnd', dataLabelFormatCode: '$0;;;',
    dataLabelColor: H.dark, dataLabelFontSize: 10, dataLabelFontBold: true, valAxisHidden: true, valGridLine: { style: 'none' }, catAxisLabelColor: H.dark, catAxisLabelFontSize: 10,
    showLegend: true, legendPos: 'b', legendFontSize: 10, legendColor: H.dark, barGapWidthPct: 35, objectName: 'chart-pv' });
tbl(s, sp.tables[2], 8.1, 3.45, 4.6, { colW: [1.2, 0.8, 0.85, 0.85, 0.9], fs: 9.5, rowH: 0.42 });
bullets(s, ['Spending is forecast to grow 3.9% a year to 2028, three times faster than visits (1.3%).', 'Overnight visits are growing fastest (+4.5% in Q2 2026).'], 8.1, 5.3, 4.6, 1.2, 11);
source(s, 'Tourism Economics, Travel Forecast (Sept. 2026) and Economic Impact of Visitors 2025. Per-visitor values are BI calculations from rounded totals (approximate).');

s = content('Visitor spending', 'Q2 2026: visitors spent $1.76 billion in Anaheim, up 7.8%', 'Quarterly results · Tourism Economics Q2 2026 measurement', '');
tbl(s, sp.tables[1], M, 1.6, 5.6, { colW: [1.4, 1.3, 1.5, 1.4], rowH: 0.4 });
tbl(s, sp.tables[0], 6.5, 1.6, 6.2, { colW: [0.85, 0.85, 1.35, 1.1, 0.95, 1.1], rowH: 0.36, fs: 10 });
bullets(s, ['Visits rose 2.8% to 6.74 million; overnight visits +4.5%, day visits +2.1%.', 'Hotel rates were nearly 9% above Q2 2025.', 'First half 2026: 13.1 million visitors spent $3.5 billion (+3.1% and +7.5%).',
            'Garden Grove Q2: 831,000 visitors (+3.4%) spent $200.4 million (+7.1%).'], M, 4.75, 5.6, 1.8, 11.5);
source(s, 'Tourism Economics, Anaheim and Garden Grove Travel Forecast (published Sept. 2026; data through Aug. 31, 2026)');

/* 2. Jobs and economy */
calcSlide('p-spend');
ocvSlide('p-spend');

pres.addSection({ title: 'Jobs and economy' });
newsSlides('p-impact');
s = content('Jobs and economy', 'Visitors support 67,817 Anaheim jobs; food and beverage is a growing share of tourism work', 'Regional economic impact · Anaheim, Garden Grove and Orange County, 2025', im.notes.join('\n'));
tbl(s, im.tables[0], M, 1.6, W - 2 * M, { colW: [1.6, 1.45, 1.6, 1.4, 1.3, 1.45, 1.5, 1.83], rowH: 0.42, fs: 10.5 });
hbar(s, 'Food and beverage share of visitor-supported jobs', Object.keys(EI), Object.values(EI).map(e => e.fb_job_share / 100), M, 3.55, 5.8, 2.9, '0.0%');
tbl(s, im.tables[1], 6.7, 3.6, 6.0, { colW: [1.8, 1.4, 1.4, 1.4], rowH: 0.36, fs: 10.5 });
source(s, 'Tourism Economics, Economic Impact of Visitors 2025 (Anaheim, Garden Grove, Orange County). Shares are BI calculations.');

/* 3. One more night */
ocvSlide('p-impact');

pres.addSection({ title: 'Hotel market' });
newsSlides('p-hotel');
s = content('Hotel market', `Resort-area hotels fill ${ht.cards[0][2]} of rooms, the highest in Orange County`, 'CoStar hotel performance · trailing 12 months and 2026 year to date through Aug. 2026', ht.notes.join('\n'));
kpis(s, ht.cards.map(c => c.slice(0, 4)), M, 1.6, W - 2 * M, 1.6, 26);
tbl(s, ht.tables[0], M, 3.45, 7.6, { colW: [2.4, 0.9, 1.0, 1.1, 1.1, 1.1], rowH: 0.36, fs: 9.5 });
hbar(s, 'Revenue per available room, past 12 months', ht.charts[0].rows.map(r => r.l), ht.charts[0].rows.map(r => r.v), 8.45, 3.4, 4.25, 3.1, '$0', ht.charts[0].rows.findIndex(r => r.hi));
source(s, 'CoStar Group, Orange County Hospitality Market and Disneyland Hospitality Submarket reports (pulled Oct. 12, 2026). © 2026 CoStar Group, licensed to Visit Anaheim.');

s = content('Hotel market', `Only ${D.sections.find(x => x.id === 'p-hotel').tables[2].rows.reduce((a, r) => a + Number(r[2]), 0)} hotel rooms are under construction countywide, which leaves room for OC Vibe's hotels`, 'CoStar construction, hotel investment and Orange County economy', '');
s.addText('Disneyland submarket by year', ft({ x: M, y: 1.6, w: 6.2, h: 0.3, fontSize: 12, bold: true, color: H.e3 }));
tbl(s, ht.tables[1], M, 1.95, 6.2, { colW: [1.9, 1.0, 1.15, 1.15, 1.0], rowH: 0.3, fs: 9.5 });
s.addText('Under construction in Orange County', ft({ x: M, y: 4.25, w: 6.2, h: 0.3, fontSize: 12, bold: true, color: H.e3 }));
tbl(s, { ...ht.tables[2], rows: ht.tables[2].rows.map(r => [r[0].replace(' (mixed-use, with dining and retail)', ' (mixed-use)'), ...r.slice(1)]) }, M, 4.6, 6.2, { colW: [2.7, 1.5, 0.7, 1.3], rowH: 0.3, fs: 9.5 });
s.addText('Orange County economy', ft({ x: 7.1, y: 1.6, w: 5.6, h: 0.3, fontSize: 12, bold: true, color: H.e3 }));
tbl(s, { ...ht.tables[4], rows: ht.tables[4].rows.map(r => [r[0].replace('Leisure and hospitality', 'Leisure & hospitality').replace(' concentration (U.S. = 1.0)', ' concentration').replace(', 5-year forecast (a year)', ' forecast, per year'), ...r.slice(1)]) }, 7.1, 1.95, 5.6, { colW: [3.2, 1.3, 1.1], rowH: 0.3, fs: 9.5 });
s.addText([{ text: 'Investment: ', options: { bold: true, color: H.e3 } }, { text: `hotel sales slowed with higher borrowing costs ($${D.costar_sales} in the past 12 months vs. a $311M three-year average). Market cap rate 7.2% in the Disneyland submarket. CoStar notes the OC Vibe district could create opportunities for future hotel investment.`, options: { color: H.dark } }],
  ft({ x: 7.1, y: 5.2, w: 5.6, h: 1.2, fontSize: 10.5, valign: 'top' }));
source(s, 'CoStar Group, Orange County Hospitality Market, Disneyland Submarket and Capital Markets reports (Oct. 12, 2026); Oxford Economics via CoStar. © 2026 CoStar Group.');

s = content('Hotel market', 'Sunday and Monday nights are where OC Vibe can add the most hotel stays', 'STR, Visit Anaheim hotels, Jan. 1–Oct. 3, 2026 · CoStar submarkets by month, 2026', ht.ocv.slice(-2).join('\n'));
const hn = ht.tables.length, hc = ht.charts[ht.charts.length - 1];
hbar(s, hc.title, hc.rows.map(r => r.l), hc.rows.map(r => r.v / 100), M, 1.55, 5.6, 3.1, '0.0%', 0);
tbl(s, ht.tables[hn - 2], M, 4.75, 5.6, { colW: [2.3, 1.1, 1.1, 1.1], rowH: 0.26, fs: 9 });
tbl(s, ht.tables[hn - 1], 6.5, 1.6, W - M - 6.5, { colW: [0.8, 1.15, 0.95, 1.1, 0.95, 1.28], rowH: 0.34, fs: 9 });
rich(s, ht.ocv[ht.ocv.length - 2], { x: 6.5, y: 4.85, w: W - M - 6.5, h: 1.5, fontSize: 10.5 });
source(s, 'STR daily data, Visit Anaheim hotel sets (Jan. 1–Oct. 3, 2026; provided Oct. 12, 2026); CoStar submarket export (Jan.–Aug. 2026).');

/* 8. OC Vibe outlook */
if (htCal) {
  s = content('Hotel market', 'When Anaheim hotels have room: a 2026 calendar for events and programming', 'Visit Anaheim hotel set (Anaheim+), Jan.–Sept. 2026 · weeknights = Sunday–Thursday nights', '');
  tbl(s, htCal, M, 1.6, W - 2 * M, { colW: [1.3, 1.5, 1.6, 2.0, 2.2, 1.6, 1.93], rowH: 0.42, fs: 10.5 });
  source(s, htCal.src + '.');
}
calcSlide('p-hotel');
ocvSlide('p-hotel');

pres.addSection({ title: 'One more night' });
newsSlides('p-night');
s = content('One more night', 'One more night by scenario: lodging and total visitor spending', 'Extra Night study · scenario estimates based on 2025 data', nt.notes.join('\n'));
hbar(s, 'Added spending by scenario ($ billions, estimates)', nt.charts[0].rows.map(r => r.l), nt.charts[0].rows.map(r => r.v), M, 1.6, 5.9, 3.0, '$0.00"B"');
tbl(s, nt.tables[0], 6.8, 1.6, 5.9, { colW: [2.6, 1.15, 2.15], rowH: 0.33, fs: 9.5 });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 4.85, w: 5.9, h: 1.55, fill: { color: H.light }, line: { color: H.e3, width: 1 }, rectRadius: 0.06, objectName: 'callout' });
s.addText([{ text: 'Why it matters for OC Vibe: ', options: { bold: true, color: H.e3 } },
           { text: 'evening events at Honda Center and the new concert hall, plus 550 planned hotel rooms, are the draws that turn day trips into overnight stays.', options: { color: H.dark } }],
  ft({ x: M + 0.2, y: 5.0, w: 5.5, h: 1.3, fontSize: 12, valign: 'top' }));
source(s, 'Visit Anaheim BI, Extra Night study (Tourism Economics 2025 spending; Azira length of stay). Estimates hold spending per day constant.');

s = content('One more night', 'Group business booked with TID incentives peaks at 30 events in 2026', 'Tourism Improvement District incentive bookings by event year · Simpleview', 'Room nights and attendees as booked; 2026 onward are future events on the books.');
tbl(s, nt.tables[1], M, 1.6, 6.4, { colW: [1.4, 1.2, 1.9, 1.9], rowH: 0.33 });
hbar(s, 'Room nights by event year (thousands)', D.tid.map(t => String(t[0])), D.tid.map(t => t[2] / 1000), 7.4, 1.6, 5.3, 4.8, '0', 4);
source(s, 'Simpleview, TID incentive buydowns (Extra Night study)');

/* 4. Getting here */
calcSlide('p-night');
ocvSlide('p-night');

pres.addSection({ title: 'Getting here' });
newsSlides('p-transport');
s = content('Getting here', 'OC Vibe sits beside one of the busiest corridors in Orange County', 'Weekday average daily traffic · OCTA 2026 Traffic Flow Map (published Aug. 2026)', tr.notes.join('\n'));
tbl(s, tr.tables[0], M, 1.6, 6.6, { colW: [3.9, 1.3, 1.4], rowH: 0.36, fs: 10.5 });
s.addImage({ data: D.adtimg, x: 7.5, y: 1.55, w: 5.2, h: 5.2 * 910 / 1050, altText: 'Excerpt of the OCTA 2026 Traffic Flow Map around SR-57, Katella Ave and ARTIC' });
s.addText('Freeway volumes are Caltrans 2024 counts; Katella Ave beside OC Vibe was last counted in 2021. New counts before the 2027 openings would set a baseline.', ft({ x: M, y: 5.6, w: 6.6, h: 0.8, fontSize: 10.5, color: H.dark }));
source(s, 'Orange County Transportation Authority, 2026 Traffic Flow Map (thousands of vehicles per weekday; Roman numerals = years before 2026 the count was taken)');

s = content('Getting here', 'ARTIC sees 277 weekday bus trips and a 14-minute one-seat ride to the resort', 'OCTA bus service at ARTIC · schedules Aug. 9–Nov. 7, 2026', '');
kpis(s, [['Weekday', 'Bus trips stopping at ARTIC', String(D.transit.wk), 'Routes 50, 53 and 553 · one every 3–4 min at peak'], ['To the resort', 'One-seat weekday trips', String(D.transit.resort_trips_wk), 'About 13 min (Route 50), 15 min (Route 553)'],
         ['After 10 p.m.', 'Weekday departures', '11', '16 buses stop after 10 p.m.; 5 end there · last at 1:38 a.m.']], M, 1.6, W - 2 * M, 1.6);
tbl(s, tr.tables[1], M, 3.45, 6.0, { colW: [0.8, 2.8, 0.8, 0.8, 0.8], rowH: 0.36, fs: 10 });
tbl(s, tr.tables[2], 6.8, 3.45, 5.9, { colW: [2.0, 2.2, 1.7], rowH: 0.5, fs: 8.5 });
source(s, 'OCTA bus schedules (GTFS), Visit Anaheim BI analysis; LARC Market Intelligence Report (Sept. 2026). Bus data excludes Metrolink and Amtrak, which also serve ARTIC.');

s = content('Getting here', 'Most visitors drive, and driving costs are up a third since 2019', 'Commute patterns and transportation cost trends · U.S. Bureau of Transportation Statistics; Azira', '');
kpis(s, [['Visitor origin', 'Domestic trips from within 50 miles', tr.cards[2][2], 'Anaheim and Garden Grove, Aug. 2026'], ['Orange County workers', 'Drive alone to work', `${(D.bts.modes[0][1] / D.bts.workers * 100).toFixed(1)}%`, `Public transportation ${(D.bts.modes[4][1] / D.bts.workers * 100).toFixed(1)}%`],
         ['U.S. car cost per mile', '2024 average', `$${D.auto['2024'].toFixed(2)}`, `▲ +${((D.auto['2024'] / D.auto['2019'] - 1) * 100).toFixed(0)}% vs. 2019`]], M, 1.6, W - 2 * M, 1.6);
tbl(s, tr.tables[3], M, 3.45, 5.4, { colW: [2.6, 1.5, 1.3], rowH: 0.36 });
tbl(s, tr.tables[4], 6.2, 3.45, 6.5, { colW: [0.8, 1.6, 1.4, 1.3, 1.4], rowH: 0.34, fs: 10 });
source(s, 'U.S. BTS County Transportation Profile (Orange County) and Transportation Economic Trends; Azira via Symphony. Shares are BI calculations.');

s = content('Getting here', 'Rail already brings visitors to OC Vibe\'s front door at ARTIC', 'Amtrak at Anaheim (ANA), 2018–2024 · Metrolink lines serving Anaheim, Oct.–Dec. 2025', tr.ocv.slice(-2).join('\n'));
const trR = tr.tables.findIndex(t => t.title === 'Rail service into ARTIC') + 1;
tbl(s, tr.tables[trR - 2], M, 1.6, 4.4, { colW: [1.2, 1.9, 1.3], rowH: 0.36, fs: 10.5 });
tbl(s, tr.tables[trR - 1], 5.2, 1.6, W - M - 5.2, { colW: [2.6, 1.25, 3.68], rowH: 0.46, fs: 9.5 });
rich(s, tr.ocv[tr.ocv.length - 2], { x: M, y: 4.75, w: 4.4, h: 1.6, fontSize: 10.5 });
source(s, 'Rail Passengers Association, Amtrak ANA fact sheet (Oct. 27, 2025; 2018–2024 data); Metrolink Fact Sheet FY2025-26 Q2 (Oct.–Dec. 2025).');

const tft = tr.tables.find(t => t.title.startsWith('Orange County transit operators')), tfr = tr.tables.find(t => t.title.startsWith('Orange County transit revenues'));
const tfp = tr.tables.find(t => t.title.startsWith('Orange County transit passengers'));
if (tfp) {
  s = content('Getting here', 'Transit ridership fell 38% from 2007 to 2017 while the bus fleet grew', 'Orange County transit passengers and vehicles · all operators · data ends in 2017', '');
  tbl(s, tfp, M, 1.55, 7.7, { colW: [0.7, 1.25, 1.0, 1.25, 1.1, 1.0, 1.4], rowH: 0.29, fs: 9 });
  rich(s, tr.notes[tr.notes.length - 2], { x: M + 8.0, y: 1.55, w: W - 2 * M - 8.0, h: 4.9, fontSize: 10.5 });
  source(s, tfp.src + '. Expenses per passenger is a BI calculation.');
}
if (tft && tfr) {
  s = content('Getting here', 'Orange County transit: fewer staff and rising costs, 2003–2017', 'OCTA, OCTA specialized service and Laguna Beach · nominal dollars · data ends in 2017', '');
  const pick7 = t => t.rows.filter(r => ['2017', '2015', '2013', '2011', '2010', '2009', '2007', '2005', '2003'].includes(r[0]));
  table(s, tft.cols, pick7(tft), M, 1.55, 7.7, { colW: [0.6, 0.95, 1.15, 1.15, 1.35, 1.1, 1.4], rowH: 0.3, fs: 8.5, hi: 0 });
  table(s, tfr.cols, pick7(tfr).slice(0, 5), M, 4.6, 7.7, { colW: [0.6, 1.2, 1.2, 1.6, 1.4, 1.7], rowH: 0.27, fs: 8.5, hi: 0 });
  rich(s, tr.notes[tr.notes.length - 1], { x: M + 8.0, y: 1.55, w: W - 2 * M - 8.0, h: 4.9, fontSize: 10 });
  source(s, tft.src + '. Selected years shown; all years in the dashboard. * 2006 total includes a Laguna Beach reporting outlier.');
}

lineSlide('p-transport');
calcSlide('p-transport');
ocvSlide('p-transport');

/* 5. Who visits */
pres.addSection({ title: 'Marketing reach' });
newsSlides('p-media');
s = content('Marketing reach', 'Which placements turn impressions into visits', 'Symphony | Azira media attribution · ad exposures Jan. 1–Aug. 31, 2026', md.notes.join('\n'));
kpis(s, md.cards.map(c => c.slice(0, 4)), M, 1.6, W - 2 * M, 1.6);
tbl(s, { ...md.tables[0], rows: md.tables[0].rows.map(r => [r[0].replace('Fall/Winter 2025–26 Domestic', 'Fall/Winter 25–26'), ...r.slice(1)]) }, M, 3.4, 7.4, { colW: [1.9, 1.9, 1.3, 1.1, 1.2], rowH: 0.27, fs: 10 });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 8.3, y: 3.4, w: 4.4, h: 2.4, fill: { color: H.light }, line: { color: H.e3, width: 1 }, rectRadius: 0.06, objectName: 'callout' });
s.addText([{ text: 'Opportunity for OC Vibe: ', options: { bold: true, color: H.e3 } }, { text: 'luxury and travel-planning placements convert best (up to 34.4 visits per 1,000 impressions). OC Vibe events and dining can be featured in this content.', options: { color: H.dark } }],
  ft({ x: 8.5, y: 3.55, w: 4.0, h: 2.1, fontSize: 12, valign: 'top' }));
source(s, 'Symphony | Tourism Economics, Azira Media Attribution (first visit at least three days after exposure)');

/* 7. Hotel market (CoStar) */
calcSlide('p-media');
ocvSlide('p-media');

pres.addSection({ title: 'Market outlook' });
newsSlides('p-larc');
s = content('Market outlook', 'OC Vibe: first buildings are up; market hall and plaza open in 2027', 'OC Vibe and nearby developments as reported in LARC market reports, June–Sept. 2026', lo.notes.join('\n'));
tbl(s, lo.tables[0], M, 1.6, 7.3, { colW: [1.7, 5.6], rowH: 0.48, fs: 10 });
tbl(s, lo.tables[2], 8.2, 1.6, 4.5, { colW: [2.5, 0.6, 1.4], rowH: 0.42, fs: 9 });
source(s, 'Lodging Analytics Research & Consulting (LARC), Anaheim Market Intelligence Reports (June, July and Sept. 2026)');

s = content('Market outlook', 'Hotel demand and conventions are strong; costs are the main headwind', 'LARC market outlook · Anaheim vs. U.S. · forecasts to 2030', '');
hbar(s, 'Revenue per available room, change vs. last year', lo.charts[0].rows.map(r => r.l), lo.charts[0].rows.map(r => r.v / 100), M, 1.6, 5.4, 2.9, '+0.0%');
tbl(s, lo.tables[1], 6.3, 1.6, 6.4, { colW: [1.1, 1.2, 1.5, 1.5, 1.1], rowH: 0.34, fs: 10 });
bullets(s, ['Conventions: room nights on the books +12% for 2026 and +17% for 2027 (Sept. 2026).', 'Events: 2028 Olympics cycling and volleyball in Anaheim; the 2026 World Cup boost turns into a tough comparison in Q2–Q3 2027.',
            `Inflation: Anaheim prices forecast +${D.cpi.cagr3}% a year (3 yrs), above the U.S.; hotel labor costs about +6% a year.`, 'Risks: gas prices and airfares (Iran conflict), possible federal shutdown, slower U.S. job growth.'], M, 4.75, W - 2 * M, 1.75, 11.5);
source(s, 'LARC, Anaheim Market Intelligence Report, Sept. 2026 (Moody\'s Analytics economic inputs). F = forecast.');

/* Checks and confidence */
if (loFacts) {
  s = content('Market outlook', 'OC Vibe in recent public sources', 'Phasing, venues and events as reported · figures differ by source', '');
  tbl(s, loFacts, M, 1.6, W - 2 * M, { colW: [2.0, 6.6, 3.53], rowH: 0.55, fs: 10.5 });
  source(s, 'Orange County Business Journal (June 1, 2026); OCVIBE concert hall release, PR Newswire (Mar. 12, 2026); BizBash (Sept. 16, 2026); LARC (Sept. 2026).');
}
lineSlide('p-larc');
ocvSlide('p-larc');

KIND = '';
/* Compare and contrast */
pres.addSection({ title: 'Compare and contrast' });
const ccSecs = D.sections.filter(x => x.cc);
for (let i = 0; i < ccSecs.length; i += 2) {
  s = content('Compare and contrast', 'Growth, opportunities, quick wins, hurdles, pitfalls and explanations' + (i ? ' (continued)' : ''), 'Every hurdle and pitfall comes with a solution · sources and dates in the dashboard', '');
  ccSecs.slice(i, i + 2).forEach((x, j) => {
    const bx = M + j * ((W - 2 * M) / 2 + 0.1), bw = (W - 2 * M) / 2 - 0.1;
    s.addText(x.tab, ft({ x: bx, y: 1.5, w: bw, h: 0.32, fontSize: 13, bold: true, color: H.e3 }));
    table(s, [['Type', 0], ['Point', 0], ['Solution', 0]], x.cc.map(c => [c.type, c.point, c.solution || 'None needed']), bx, 1.85, bw, { colW: [0.95, 3.25, bw - 4.2], rowH: 0.5, fs: 7.5, hi: -1, rich: true });
  });
  source(s, ccSecs.slice(i, i + 2).map(x => x.tab + ': ' + [...new Set(x.cc.map(c => c.src))].slice(0, 2).join('; ')).join(' | '));
}

/* Recommendations */
/* Reports and data library (Oct. 14, 2026) */
pres.addSection({ title: 'Reports and data library' });
libSlides('Reports and data library');

pres.addSection({ title: 'Next steps' });
s = content('Next steps', 'How Visit Anaheim data can help OC Vibe succeed', 'Recommendations from Visit Anaheim BI · for discussion', '');
table(s, [['What to do', 0], ['Who', 0], ['When', 0], ['Why', 0], ['How we\'ll measure it', 0]], D.recs_t, M, 1.5, W - 2 * M, { colW: [2.9, 2.2, 1.8, 3.0, 2.23], rowH: 0.58, fs: 9, hi: -1, rich: true });
s.addText('Visit Anaheim can refresh these measures quarterly and add OC Vibe-specific tracking (visitation, spending, length of stay) as venues open.', ft({ x: M, y: 6.1, w: W - 2 * M, h: 0.4, fontSize: 11.5, bold: true, color: H.e3 }));
source(s, 'Visit Anaheim Business Intelligence');

/* Sources */
s = content('Next steps', 'Sources and notes', 'Every source with period covered, date published or pulled, and how BI checked it', '');
const RC = [['Source', 0], ['Document', 0], ['Period covered', 0], ['Published or pulled', 0], ['How it was checked', 0]];
const rr = D.register.map(r => [r[0], r[1], r[2], r[3], r[5]]);
for (let i = 0; i < rr.length; i += 8) {
  if (i > 0) s = content('Next steps', 'Sources and notes (continued)', 'Source register, continued', '');
  table(s, RC, rr.slice(i, i + 8), M, 1.55, W - 2 * M, { colW: [2.0, 3.3, 2.1, 2.1, 2.63], rowH: 0.52, fs: 8.5, hi: -1 });
  source(s, 'Visit Anaheim Business Intelligence source register, Oct. 12, 2026' + (i + 8 < rr.length ? ' (continued on next slide).' : '.'));
}
s = content('Next steps', 'About the data', 'Limits and differences between sources to keep in mind', '');
bullets(s, D.dq.slice(0, 8), M, 1.6, W - 2 * M, 4.9, 11.5);
s = content('Next steps', 'About the data (continued)', 'Limits and differences between sources to keep in mind', '');
bullets(s, D.dq.slice(8), M, 1.6, W - 2 * M, 4.9, 11.5);
{ const U = D.schedule;
  s = content('Next steps', U.table.title, U.line, '');
  table(s, U.table.cols, U.table.rows, M, 1.5, W - 2 * M, { colW: [3.4, 2.6, 2.75, 3.38], rowH: 0.48, fs: 9, hi: -1 });
  source(s, U.table.src + '.');
  s = content('Next steps', U.planned.title, 'Planned for a more complete view of OC Vibe visitors · not in this edition', '');
  table(s, U.planned.cols, U.planned.rows, M, 1.6, W - 2 * M, { colW: [2.7, 2.9, 3.83, 2.7], rowH: 0.85, fs: 10.5, hi: -1 });
  rich(s, 'No figures from these sources appear until the data is received, checked and cleared for sharing. Each is added at the next quarterly update after it arrives. Ticketing and foot-traffic data are licensed or partner data: the report would show summaries only.', { x: M, y: 4.5, w: W - 2 * M, h: 0.9, fontSize: 12 });
  source(s, U.planned.src + '.'); }

/* Appendix */
pres.addSection({ title: 'Appendix' });
const ap = sec('p-appx');
s = content('Appendix', 'Formulas, with the 2025 inputs worked through', 'Each formula with its 2025 inputs · Visit Anaheim BI, Oct. 13, 2026', '');
table(s, ap.tables[0].cols, ap.tables[0].rows.slice(0, 10), M, 1.5, W - 2 * M, { colW: [2.6, 4.6, 4.93], rowH: 0.45, fs: 9.5, hi: 7 });
source(s, ap.tables[0].src);
if (ap.tables[0].rows.length > 10) {   // only when there are more than 10 formulas (Oct. 14, 2026: no empty continuation slide)
  s = content('Appendix', 'Formulas (continued)', 'Each formula with its 2025 inputs · Visit Anaheim BI, Oct. 13, 2026', '');
  table(s, ap.tables[0].cols, ap.tables[0].rows.slice(10), M, 1.5, W - 2 * M, { colW: [2.6, 4.6, 4.93], rowH: 0.45, fs: 9.5, hi: -1 });
  source(s, ap.tables[0].src);
}
for (let i = 0; i < ap.tables[1].rows.length; i += 15) {
  s = content('Appendix', 'Glossary' + (i ? ' (continued)' : ''), 'Terms used in this report', '');
  table(s, ap.tables[1].cols, ap.tables[1].rows.slice(i, i + 15), M, 1.5, W - 2 * M, { colW: [3.0, 9.13], rowH: 0.31, fs: 9.5, hi: -1 });
  source(s, ap.tables[1].src);
}
for (let i = 0; i < ap.tables[2].rows.length; i += 8) {   // 8 methods per slide so long rows never run into the footer
  s = content('Appendix', 'Methods' + (i ? ' (continued)' : ''), 'How each type of number was produced', '');
  table(s, ap.tables[2].cols, ap.tables[2].rows.slice(i, i + 8), M, 1.5, W - 2 * M, { colW: [2.4, 6.6, 3.13], rowH: 0.5, fs: 9.5, hi: -1 });
  source(s, ap.tables[2].src);
}

(async () => {
  await pres.writeFile({ fileName: 'OC_Vibe_Insights.pptx', compression: true });
  await applyTheme('OC_Vibe_Insights.pptx', THEME);
  console.log('written');
})();
