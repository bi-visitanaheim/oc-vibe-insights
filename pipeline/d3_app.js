/* D3 v7.9.0 visuals (Oct. 14, 2026): deterministic SVG (fixed viewBox, sorted data, no randomness, no transitions).
   Colors come from CSS classes, so light and dark mode need no redraw. Values use the shared value tooltip ([data-tip]). */
(function () {
  if (typeof d3 === 'undefined' || !DATA.ask) return;
  const GEO_ORDER = ['Anaheim', 'Garden Grove', 'Orange County', 'California', 'U.S.'];
  const gcls = g => 'g-' + g.toLowerCase().replace(/[^a-z]+/g, '');
  // on phones the SVG keeps a readable minimum width inside a swipeable frame
  const wrapSvg = n => { const w = document.createElement('div'); w.className = 'd3s'; w.setAttribute('tabindex', '0'); w.setAttribute('aria-label', 'Chart. Swipe sideways on small screens to see all of it.'); w.appendChild(n); return w; };
  const fmt = (u, v) => u === '$' ? '$' + d3.format(',.0f')(v) : d3.format('.1f')(v) + '%';

  /* ---------- dot matrix: how Anaheim compares ---------- */
  function dotMatrix(host) {
    const C = DATA.ask.compare; if (!C || !host || document.getElementById('d3-compare')) return;
    const fig = document.createElement('figure'); fig.className = 'ig d3f'; fig.id = 'd3-compare';
    const rows = C.rows.map(r => Object.assign({}, r, { pts: r.pts.slice().sort((a, b) => GEO_ORDER.indexOf(a[0]) - GEO_ORDER.indexOf(b[0])) }));
    const W = 960, L = 300, R = 40, rowH = 78, T = 46, H = T + rows.length * rowH + 8;
    const svg = d3.create('svg').attr('class', 'vz d3vz').attr('viewBox', `0 0 ${W} ${H}`).attr('preserveAspectRatio', 'xMidYMid meet').attr('role', 'img')
      .attr('aria-label', C.title + '. ' + rows.map(r => r.m + ': ' + r.pts.map(p => p[0] + ' ' + fmt(r.unit, p[1])).join(', ')).join('; '));
    const geos = GEO_ORDER.filter(g => rows.some(r => r.pts.some(p => p[0] === g)));
    const lg = svg.append('g').attr('class', 'd3-leg').attr('transform', `translate(${L},18)`);
    geos.forEach((g, i) => { const x = i * 128; lg.append('circle').attr('class', 'dot ' + gcls(g)).attr('cx', x + 6).attr('cy', 0).attr('r', 6); lg.append('text').attr('class', 'lbl').attr('x', x + 16).attr('y', 4).text(g); });
    rows.forEach((r, i) => {
      const y = T + i * rowH + rowH / 2, max = d3.max(r.pts, p => p[1]);
      const x = d3.scaleLinear().domain([0, max * 1.1]).nice(4).range([L, W - R]);
      const g = svg.append('g').attr('class', 'd3-row').attr('data-ask-open', r.q).attr('tabindex', 0).attr('role', 'button').attr('aria-label', `${r.m}. Open the full answer.`);
      g.append('rect').attr('class', 'rowbg').attr('x', 0).attr('y', y - rowH / 2 + 4).attr('width', W).attr('height', rowH - 8).attr('rx', 6);
      g.append('text').attr('class', 'm').attr('x', 12).attr('y', y - 4).text(r.m.replace(/ \(.*\)$/, ''));
      g.append('text').attr('class', 'mu').attr('x', 12).attr('y', y + 14).text((r.m.match(/\(([^)]*)\)$/) || [, ''])[1] + ' · open the answer →');
      g.append('line').attr('class', 'axl').attr('x1', x.range()[0]).attr('x2', x.range()[1]).attr('y1', y).attr('y2', y);
      x.ticks(4).forEach(t => { g.append('line').attr('class', 'tk').attr('x1', x(t)).attr('x2', x(t)).attr('y1', y - 4).attr('y2', y + 4); g.append('text').attr('class', 'tkl').attr('x', x(t)).attr('y', y + 22).attr('text-anchor', 'middle').text(r.unit === '$' ? '$' + t : t + '%'); });
      // value labels: alternate above/below when dots are within 46px, deterministic by sorted x
      const placed = r.pts.map(p => ({ g: p[0], v: p[1], px: x(p[1]) })).sort((a, b) => a.px - b.px || GEO_ORDER.indexOf(a.g) - GEO_ORDER.indexOf(b.g));
      let lastUp = -1e9, lastDn = -1e9;
      placed.forEach(p => { const up = p.px - lastUp >= 46 || p.px - lastDn < 46; p.dy = up ? -12 : 30; if (up) lastUp = p.px; else lastDn = p.px; });
      placed.forEach(p => {
        g.append('circle').attr('class', 'dot ' + gcls(p.g)).attr('cx', p.px).attr('cy', y).attr('r', p.g === 'Anaheim' ? 9 : 7)
          .attr('data-tip', `${p.g}: ${fmt(r.unit, p.v)} (${r.m})`).attr('tabindex', 0);
        g.append('text').attr('class', 'val ' + (p.g === 'Anaheim' ? 'hi' : '')).attr('x', p.px).attr('y', y + p.dy).attr('text-anchor', 'middle').text(fmt(r.unit, p.v));
      });
    });
    fig.innerHTML = `<header class="ig-h"><h4>${esc(C.title)}</h4><p>Each row has its own scale. Select a row to open the full answer. ${esc(C.notes)}</p></header>`;
    fig.appendChild(wrapSvg(svg.node()));
    fig.insertAdjacentHTML('beforeend', `<p class="ig-src">Source: ${esc(C.src)}</p>`);
    host.parentNode.insertBefore(fig, host.nextSibling);
    fig.addEventListener('keydown', e => { const row = e.target.closest && e.target.closest('.d3-row'); if (row && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); row.dispatchEvent(new MouseEvent('click', { bubbles: true })); } });
  }

  /* ---------- treemaps: where visitor spending goes ---------- */
  function treemaps(host) {
    const M = DATA.ask.mix; if (!M || !host || document.getElementById('d3-mix')) return;
    const CATS = ['Recreation', 'Lodging', 'Retail', 'Food and beverage', 'Transportation'];
    const fig = document.createElement('figure'); fig.className = 'ig d3f'; fig.id = 'd3-mix';
    const W = 960, H = 420, gap = 28, w = (W - gap) / 2, top = 34;
    const svg = d3.create('svg').attr('class', 'vz d3vz').attr('viewBox', `0 0 ${W} ${H + top + 36}`).attr('preserveAspectRatio', 'xMidYMid meet').attr('role', 'img')
      .attr('aria-label', M.title + '. ' + M.geos.map(g => g.g + ': ' + g.parts.map(p => `${p[0]} $${d3.format(',.0f')(p[1])}M (${(p[1] / g.total * 100).toFixed(1)}%)`).join(', ')).join('; '));
    M.geos.forEach((G, gi) => {
      const ox = gi * (w + gap);
      const root = d3.hierarchy({ children: G.parts.map(p => ({ n: p[0], v: p[1] })).sort((a, b) => CATS.indexOf(a.n) - CATS.indexOf(b.n)) }).sum(d => d.v || 0).sort((a, b) => b.value - a.value || CATS.indexOf(a.data.n) - CATS.indexOf(b.data.n));
      d3.treemap().tile(d3.treemapSquarify.ratio(1.4)).size([w, H]).paddingInner(3).round(true)(root);
      const g = svg.append('g').attr('transform', `translate(${ox},${top})`);
      svg.append('text').attr('class', 'tmh').attr('x', ox).attr('y', 20).text(`${G.g} · $${(G.total / 1000).toFixed(2)}B total`);
      root.leaves().forEach(l => {
        const pct = l.data.v / G.total * 100, cw = l.x1 - l.x0, ch = l.y1 - l.y0;
        const cell = g.append('g').attr('transform', `translate(${l.x0},${l.y0})`);
        cell.append('rect').attr('class', 'tm c' + CATS.indexOf(l.data.n)).attr('width', cw).attr('height', ch).attr('rx', 4)
          .attr('data-tip', `${G.g}, ${l.data.n}: $${d3.format(',.0f')(l.data.v)}M (${pct.toFixed(1)}% of $${d3.format(',.0f')(G.total)}M)`).attr('tabindex', 0);
        if (cw > 70 && ch > 44) {
          cell.append('text').attr('class', 'tml c' + CATS.indexOf(l.data.n)).attr('x', 10).attr('y', 22).text(l.data.n);
          cell.append('text').attr('class', 'tmv c' + CATS.indexOf(l.data.n)).attr('x', 10).attr('y', 44).text(`$${l.data.v >= 1000 ? (l.data.v / 1000).toFixed(2) + 'B' : d3.format(',.0f')(l.data.v) + 'M'} · ${pct.toFixed(1)}%`);
        } else if (cw > 40 && ch > 20) {
          cell.append('text').attr('class', 'tmv c' + CATS.indexOf(l.data.n)).attr('x', 6).attr('y', 16).text(pct.toFixed(1) + '%');
        }
      });
    });
    const lg = svg.append('g').attr('transform', `translate(0,${H + top + 22})`);
    CATS.forEach((c, i) => { lg.append('rect').attr('class', 'tm c' + i).attr('x', i * 170).attr('y', -10).attr('width', 12).attr('height', 12).attr('rx', 2); lg.append('text').attr('class', 'lbl').attr('x', i * 170 + 18).attr('y', 0).text(c); });
    fig.innerHTML = `<header class="ig-h"><h4>${esc(M.title)}</h4><p>Each rectangle's area is its share of the area's visitor spending in 2025. Hover over or tab to a rectangle for its value.</p></header>`;
    fig.appendChild(wrapSvg(svg.node()));
    fig.insertAdjacentHTML('beforeend', `<p class="ig-calc">Share = category spending ÷ total visitor spending (Anaheim $6.832B; Orange County $17.993B). Transportation is ground travel and gasoline bought locally, plus the local share of air travel where an airport exists.</p><p class="ig-src">Source: ${esc(M.src)}</p>`);
    host.appendChild(fig);
  }

  const start = () => {
    dotMatrix(document.getElementById('askCoreGrid'));
    treemaps(document.getElementById('p-spend-ig') || document.getElementById('p-impact-ig'));
  };
  start();
})();
