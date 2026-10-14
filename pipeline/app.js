/* OC Vibe Insights: built on the BI Pulse dashboard template (nav, sidebar, BI Pulse Summary, full screen, PDF export). */
const store = { get(k){ try { return JSON.parse(localStorage.getItem('va-ocvibe-'+k)); } catch(_) { return null; } }, set(k,v){ try { localStorage.setItem('va-ocvibe-'+k, JSON.stringify(v)); } catch(_) {} } };
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
/* Emphasis: bold key metrics (money, percentages, large counts, scaled values) inside prose */
const KV_RX = /(?:[▲▼]\s?)?[+−-]?\$?\d[\d,]*(?:\.\d+)?(?:\s?(?:[MBK](?![a-z])|million|billion|%|percentage points|points|pts|days?|nights|room nights|jobs|visitors|vehicles|rooms|seats))?(?:\s?(?:–|-|to)\s?\$?\d[\d,]*(?:\.\d+)?(?:[MBK](?![a-z])|%| million| billion)?)?/g;
function kvKeep(m) {
  const t = m.trim().replace(/^[▲▼]\s?/, '');
  if (/^[−-]\d+$/.test(t)) return false;
  if (/^(19|20)\d\d\s/.test(t)) return false;                    // '2025 visitors'                         // e.g. SR-57, I-5
  if (/^(19|20)\d\d$/.test(t)) return false;                      // years
  if (/^(19|20)\d\d[–-](19|20)?\d\d$/.test(t)) return false;      // year ranges
  return /[$%]|\d,\d|\d\.\d|[MBK]$|million|billion|points|pts|days?|nights|jobs|visitors|vehicles|rooms|seats/.test(t);
}
const emph = raw => esc(raw).replace(KV_RX, (m, off, str) => {
  if (!kvKeep(m)) return m;
  const prev = str.slice(Math.max(0, off - 10), off);
  if (/(Route |Q|SR-|I-|No\. |District |Line |Phase |Lot |Dock )$/.test(prev) || /[A-Za-z]$/.test(prev)) return m;
  const lead = m.match(/^\s*/)[0]; return `${lead}<b class="kv">${m.slice(lead.length)}</b>`;
});

const glyph = v => v>0?'▲':v<0?'▼':'▶';
const dcell = c => (c && typeof c === 'object') ? `<span class="${c.d>0?'fav':c.d<0?'unf':''}">${glyph(c.d)} ${esc(c.t)}</span>` : esc(c);
const stripTags = h => String(h).replace(/<[^>]+>/g,'');
const AP_MON = ['Jan.','Feb.','March','April','May','June','July','Aug.','Sept.','Oct.','Nov.','Dec.'];
const apDate = d => `${AP_MON[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
const S = DATA.sections;

/* ---------- section pages ---------- */
function tableHtml(t, key) {
  const th = t.cols.map(([l,n]) => `<th scope="col" class="${n?'n':''}">${esc(l)}</th>`).join('');
  const LIM = 8, many = !t.full && t.rows.length > LIM + 2, open = FULL.has(key);
  const rows = many && !open ? t.rows.slice(0, LIM) : t.rows;
  const tb = rows.map((r,i) => `<tr class="${i===t.hi?'hirow':''}">` + r.map((c,j) => j===0 ? `<th scope="row">${dcell(c)}</th>` : `<td class="${t.cols[j][1]?'n':''}">${dcell(c)}</td>`).join('') + '</tr>').join('');
  const btn = many ? `<div class="more"><button type="button" class="nbtn more-b" data-key="${key}" aria-expanded="${open}">${open?'Show fewer':`Show full list (${t.rows.length})`}</button></div>` : '';
  return `<div class="tbl-cap"><b>${esc(t.title)}</b>${t.sub?`<span>${esc(t.sub)}</span>`:''}</div>
    <div class="scroll" tabindex="0" aria-label="${esc(t.title)}"><table><thead><tr>${th}</tr></thead><tbody>${tb}</tbody></table></div>${btn}
    <p class="src">Source: ${esc(t.src)}</p>`;
}
const FULL = new Set();
const fmtY = (v, f) => (f && f.pre || '') + (+v).toFixed(f && f.dec != null ? f.dec : 1) + (f && f.suf || '');
function svgLine(c) {
  const W = 640, H = 260, L = 46, R = 104, T = 16, Bm = 30, all = c.series.flatMap(x => x.v);
  const lo0 = c.ymin != null ? c.ymin : Math.min(0, ...all), raw = (Math.max(...all) - lo0) / 4, mag = Math.pow(10, Math.floor(Math.log10(raw || 1))), stp = [1, 2, 2.5, 5, 10].map(k => k * mag).find(k => k >= raw) || raw;
  const lo = Math.floor(lo0 / stp) * stp, hi = Math.ceil(Math.max(...all) / stp) * stp + (Math.max(...all) % stp === 0 ? stp * 0.25 : 0), X = i => L + i * (W - L - R) / Math.max(1, c.x.length - 1), Y = v => T + (H - T - Bm) * (1 - (v - lo) / (hi - lo || 1));
  const ticks = []; for (let t = lo; t <= hi + 1e-9; t += stp) ticks.push(t);
  const tf = Object.assign({}, c.yfmt, {dec: stp >= 1 ? 0 : 1});
  const grid = ticks.map(t => `<line x1="${L}" x2="${W - R}" y1="${Y(t).toFixed(1)}" y2="${Y(t).toFixed(1)}" class="gl"/><text x="${L - 6}" y="${(Y(t) + 4).toFixed(1)}" class="ax" text-anchor="end">${esc(t === 0 ? '0' : fmtY(t, tf))}</text>`).join('');
  const step = Math.ceil(c.x.length / 8), xl = c.x.map((x, i) => i % step === 0 || i === c.x.length - 1 ? `<text x="${X(i).toFixed(1)}" y="${H - 8}" class="ax" text-anchor="middle">${esc(x)}</text>` : '').join('');
  const ser = c.series.map(sr => {
    const pts = sr.v.map((v, i) => `${X(i).toFixed(1)},${Y(v).toFixed(1)}`).join(' '), last = sr.v.length - 1;
    const area = sr.focal ? `<polygon class="ar" points="${X(0).toFixed(1)},${Y(lo).toFixed(1)} ${pts} ${X(last).toFixed(1)},${Y(lo).toFixed(1)}"/>` : '';
    return `${area}<polyline class="${sr.focal ? 'ln f' : 'ln o'}" points="${pts}"/>${sr.v.map((v, i) => `<circle class="${sr.focal ? 'pt f' : 'pt o'}" cx="${X(i).toFixed(1)}" cy="${Y(v).toFixed(1)}" r="${sr.focal ? 3.5 : 2.5}"/><circle class="hit" cx="${X(i).toFixed(1)}" cy="${Y(v).toFixed(1)}" r="11" data-tip="${esc(sr.name)}, ${esc(c.x[i])}: ${esc(fmtY(v, c.yfmt))}" tabindex="0"/>`).join('')}<text x="${(X(last) + 8).toFixed(1)}" y="${(Y(sr.v[last]) + 4).toFixed(1)}" class="${sr.focal ? 'dl f' : 'dl'}">${esc(sr.name)} ${esc(fmtY(sr.v[last], c.yfmt))}</text>`;
  }).join('');
  return `<svg class="vz" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet" focusable="false">${grid}${xl}${ser}</svg>`;
}
function svgWf(c) {
  const W = 640, H = 250, L = 16, R = 16, T = 24, Bm = 52, n = c.steps.length, bw = (W - L - R) / n * 0.56, gap = (W - L - R) / n;
  const max = Math.max(...c.steps.map(s => s.v)), Y = v => T + (H - T - Bm) * (1 - v / max);
  let run = 0;
  const bars = c.steps.map((s, i) => {
    const x = L + i * gap + (gap - bw) / 2, y0 = s.total ? 0 : run, y1 = s.total ? s.v : run + s.v; if (!s.total) run += s.v;
    const top = Y(y1), h = Y(y0) - Y(y1);
    const con = i < n - 1 ? `<line class="wfc" x1="${(x + bw).toFixed(1)}" x2="${(x + gap).toFixed(1)}" y1="${top.toFixed(1)}" y2="${top.toFixed(1)}"/>` : '';
    return `<rect data-tip="${esc(s.l)}: ${esc(s.t)}${s.note ? ' (' + esc(s.note) + ')' : ''}" tabindex="0" class="${s.total ? 'wft' : (i ? 'wf2' : 'wf1')}" x="${x.toFixed(1)}" y="${top.toFixed(1)}" width="${bw.toFixed(1)}" height="${Math.max(1, h).toFixed(1)}" rx="3"><title>${esc(s.l)}: ${esc(s.t)}</title></rect>${con}
      <text x="${(x + bw / 2).toFixed(1)}" y="${(top - 7).toFixed(1)}" class="dl f" text-anchor="middle">${esc(s.t)}</text>
      <text x="${(x + bw / 2).toFixed(1)}" y="${H - 32}" class="ax b" text-anchor="middle">${esc(s.l)}</text><text x="${(x + bw / 2).toFixed(1)}" y="${H - 16}" class="ax" text-anchor="middle">${esc(s.note || '')}</text>`;
  }).join('');
  return `<svg class="vz" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet" focusable="false"><line class="gl" x1="${L}" x2="${W - R}" y1="${Y(0)}" y2="${Y(0)}"/>${bars}</svg>`;
}
function svgRange(c) {
  const W = 640, H = 150, L = 20, R = 20, X = v => L + (W - L - R) * (v - c.min) / (c.max - c.min), y = 62;
  const ticks = [0, 50, 100, 150, 200].filter(t => t >= c.min && t <= c.max).map(t => `<line class="gl" x1="${X(t)}" x2="${X(t)}" y1="${y - 26}" y2="${y + 26}"/><text class="ax" x="${X(t)}" y="${y + 44}" text-anchor="middle">$${t}M</text>`).join('');
  const marks = c.marks.map((mk, i) => `<line data-tip="${esc(mk.l)}" tabindex="0" class="${mk.k === 'base' ? 'rmb' : mk.k === 'mid' ? 'rmm' : 'rme'}" x1="${X(mk.v).toFixed(1)}" x2="${X(mk.v).toFixed(1)}" y1="${y - 22}" y2="${y + 22}"/><text class="${mk.k === 'base' ? 'dl f' : 'ax'}" x="${X(mk.v).toFixed(1)}" y="${i % 2 ? y + 62 : y - 30}" text-anchor="${mk.v < 30 ? 'start' : mk.v > 170 ? 'end' : 'middle'}">${esc(mk.l)}</text>`).join('');
  return `<svg class="vz" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet" focusable="false">${ticks}<rect class="rb" data-tip="90% of simulations: $${Math.round(c.lo)}M–$${Math.round(c.hi)}M" tabindex="0" x="${X(c.lo).toFixed(1)}" y="${y - 14}" width="${(X(c.hi) - X(c.lo)).toFixed(1)}" height="28" rx="4"/><text class="ax b" x="${((X(c.lo) + X(c.hi)) / 2).toFixed(1)}" y="${y + 4}" text-anchor="middle">90% of simulations</text>${marks}</svg>`;
}
function heatHtml(c) {
  const cls = v => v >= 85 ? 'h5' : v >= 80 ? 'h4' : v >= 75 ? 'h3' : v >= 70 ? 'h2' : 'h1';
  return `<div class="scroll" tabindex="0" aria-label="${esc(c.title)}"><table class="heat"><thead><tr><th scope="col">Month</th>${c.cols.map(h => `<th scope="col">${esc(h)}</th>`).join('')}<th scope="col">Peak nights and groups</th></tr></thead><tbody>${c.rows.map(r => `<tr><th scope="row">${esc(r.l)}</th>${r.cells.map((v, j) => `<td class="${cls(v)}" data-tip="${esc(r.l)}, ${esc(c.cols[j])}: ${(+v).toFixed(1)}% occupancy${r.extra ? ' · ' + esc(r.extra) : ''}">${(+v).toFixed(1)}%</td>`).join('')}<td class="hx">${esc(r.extra || '')}</td></tr>`).join('')}</tbody></table></div>
    <div class="legend heat-lg"><span><i class="h1"></i>Under 70%</span><span><i class="h2"></i>70–75%</span><span><i class="h3"></i>75–80%</span><span><i class="h4"></i>80–85%</span><span><i class="h5"></i>85%+</span></div>`;
}
function chartHtml(c) {
  let body = '';
  if (c.kind === 'line' || c.kind === 'wf' || c.kind === 'range' || c.kind === 'heat') {
    const aria = c.kind === 'line' ? `${c.title}. ` + c.series.map(sr => `${sr.name}: ` + sr.v.map((v, i) => `${c.x[i]} ${fmtY(v, c.yfmt)}`).join(', ')).join('; ')
      : c.kind === 'wf' ? `${c.title}. ` + c.steps.map(s => `${s.l} ${s.t}`).join(', ')
      : c.kind === 'range' ? `${c.title}. ` + c.marks.map(m => m.l).join(', ') : `${c.title}`;
    body = c.kind === 'line' ? svgLine(c) : c.kind === 'wf' ? svgWf(c) : c.kind === 'range' ? svgRange(c) : heatHtml(c);
    const leg = c.kind === 'line' && c.series.length > 1 ? `<div class="legend">${c.series.map(sr => `<span><i class="${sr.focal ? 'lf' : 'lo'}"></i>${esc(sr.name)}</span>`).join('')}</div>` : '';
    return `<figure class="chartf"${c.kind === 'heat' ? '' : ` role="img" aria-label="${esc(aria)}"`}><h3>${esc(c.title)}</h3><p class="csub2">${esc(c.sub)}</p>${body}${leg}<p class="src">Source: ${esc(c.src)}</p></figure>`;
  }
  const aria = c.rows ? `${c.title}: ` + c.rows.map(r => `${r.l} ${r.t}`).join(', ') : c.title;
  if (c.kind === 'img') {
    return `<figure class="chartf"><h3>${esc(c.title)}</h3><p class="csub2">${esc(c.sub)}</p><img src="${IMGS[c.img]}" alt="${esc(c.title)}" style="width:100%;height:auto;border-radius:4px;border:1px solid var(--border-subtle)"><p class="src">Source: ${esc(c.src)}</p></figure>`;
  }
  if (c.kind === 'cols') {
    const max = Math.max(...c.rows.map(r => r.v));
    body = `<div class="vcols">${c.rows.map(r => `<div class="vcol${r.fc?' fc':''}${r.hi?' hi':''}" data-tip="${esc(r.l)}: ${esc(r.t)}${r.fc?' (forecast)':''}" tabindex="0" role="img" aria-label="${esc(r.l)}: ${esc(r.t)}${r.fc?' (forecast)':''}"><span class="bv">${esc(r.t)}</span><span class="b" style="height:${(r.v/max*82).toFixed(1)}%"></span></div>`).join('')}</div>
      <div class="vlabs" aria-hidden="true">${c.rows.map(r => `<span>${esc(r.l)}</span>`).join('')}</div>
      <div class="legend"><span><i class="a"></i>Actual</span><span><i class="h"></i>Latest full year (2025)</span><span><i class="f"></i>Forecast</span></div>`;
  } else {
    const max = Math.max(...c.rows.map(r => Math.abs(r.v)), 1e-9);
    body = `<div class="hbars">${c.rows.map(r => `<span class="l">${esc(r.l)}</span><span class="t" data-tip="${esc(r.l)}: ${esc(r.t)}" tabindex="0" role="img" aria-label="${esc(r.l)}: ${esc(r.t)}"><span class="f${r.hi?' hi':''}" style="width:${Math.max(1.5, Math.abs(r.v)/max*100).toFixed(1)}%"></span></span><span class="v">${esc(r.t)}</span>`).join('')}</div>`;
  }
  return `<figure class="chartf" role="img" aria-label="${esc(aria)}"><h3>${esc(c.title)}</h3><p class="csub2">${esc(c.sub)}</p>${body}<p class="src">Source: ${esc(c.src)}</p></figure>`;
}

/* ---------- data infographics (Oct. 13, 2026): count-up numbers, growing bars, filling waffles; final values in markup ---------- */
function cnt(o, txt) {   // number that counts up on entrance; markup holds the final text
  if (!o || o.n == null) return esc(txt);
  return `<span class="cu" data-n="${o.n}" data-pre="${esc(o.pre||'')}" data-suf="${esc(o.suf||'')}" data-dec="${o.dec != null ? o.dec : (String(o.n).includes('.') ? String(o.n).split('.')[1].length : 0)}">${esc(txt)}</span>`;
}
function infoHtml(g, sid, i) {
  const head = `<header class="ig-h"><h4>${esc(g.title)}</h4>${g.sub ? `<p>${esc(g.sub)}</p>` : ''}</header>`;
  const foot = `<p class="ig-src">Source: ${esc(g.src)}</p>`;
  let body = '', label = g.title;
  if (g.kind === 'chain') {
    body = `<ol class="ig-chain">${g.steps.map((st, k) => `<li class="ch-step" style="--i:${k}"><b class="ch-v">${cnt(st, st.v)}</b><span class="ch-l">${esc(st.l)}</span></li>${k < g.links.length ? `<li class="ch-link" style="--i:${k}"><span class="ch-arrow" aria-hidden="true"></span><span class="ch-t">${esc(g.links[k])}</span></li>` : ''}`).join('')}</ol>`;
    label += ': ' + g.steps.map(st => st.v + ' ' + st.l).join(', ');
  } else if (g.kind === 'waffle') {
    body = `<div class="ig-waffles">${g.items.map(it => { const n = Math.round(it.pct); return `<figure class="wf"><div class="wf-grid" role="img" aria-label="${n} of 100 (${it.pct}%) ${esc(it.l)}">${Array.from({length:100}, (_, k) => `<span class="${k < n ? 'on' : ''}" style="--i:${k}"></span>`).join('')}</div><figcaption><b>${cnt({n:it.pct, suf:'%', dec:1}, it.pct.toFixed(1)+'%')}</b> ${esc(it.l)}<small>${n} of every 100 · Source: ${esc(it.src)}</small></figcaption></figure>`; }).join('')}</div>`;
  } else if (g.kind === 'receipt') {
    body = `<div class="ig-receipt"><div class="rc-paper"><p class="rc-h">Anaheim · average visitor · 2025</p>${g.lines.map((ln, k) => `<div class="rc-ln" style="--i:${k}" data-tip="${esc(ln.l)}: ${esc(ln.v)} (${esc(ln.calc)}; ${ln.pct}% of spending)" tabindex="0"><span class="rc-l">${esc(ln.l)}</span><span class="rc-dots" aria-hidden="true"></span><b>${cnt(ln, ln.v)}</b><span class="rc-bar" aria-hidden="true"><span class="grow" style="width:${ln.pct}%"></span></span><small>${esc(ln.calc)} · ${ln.pct}% of spending</small></div>`).join('')}<div class="rc-tot"><span>${esc(g.total.l)}</span><b>${esc(g.total.v)}</b><small>${esc(g.total.calc)}</small></div></div>
      <div class="rc-mix"><p class="rc-mh">Every $1 of visitor spending</p><div class="rc-stack" role="img" aria-label="${esc(g.lines.map(ln => ln.l + ' ' + ln.pct + '%').join(', '))}">${g.lines.map((ln, k) => `<span class="rc-seg s${k}" style="width:${ln.pct}%;--i:${k}" data-tip="${esc(ln.l)}: ${ln.pct}% (${(ln.pct).toFixed(1)} cents of each $1)" tabindex="0"></span>`).join('')}</div>
      <ul class="rc-leg">${g.lines.map((ln, k) => `<li><span class="sw s${k}" aria-hidden="true"></span><b>${Math.round(ln.pct)}¢</b> ${esc(ln.l)} <small>(${ln.pct}%)</small></li>`).join('')}</ul></div></div>`;
    label += ': ' + g.lines.map(ln => ln.l + ' ' + ln.v).join(', ') + '; ' + g.total.l + ' ' + g.total.v;
  } else if (g.kind === 'people') {
    const full = Math.floor(g.pct / 10), part = (g.pct % 10) / 10;
    const icon = f => `<span class="pp" style="--f:${f}"><svg viewBox="0 0 24 48" aria-hidden="true"><circle cx="12" cy="7" r="6"/><path d="M3 18a9 9 0 0 1 18 0v14h-4v15h-10V32H3z"/></svg></span>`;
    body = `<div class="ig-people"><div class="pp-row" role="img" aria-label="${esc(g.v)} ${esc(g.l)}">${Array.from({length:10}, (_, k) => icon(k < full ? 1 : k === full ? part : 0)).join('')}</div><p class="pp-cap"><b>${cnt({n:g.pct, suf:'%', dec:1}, g.v)}</b> ${esc(g.l)}</p></div>`;
  } else if (g.kind === 'towers') {
    body = `<div class="ig-towers">${g.nights.map((nt, k) => `<div class="tw${nt.hi ? ' hi' : ''}" style="--i:${k}" data-tip="${esc(nt.l)}: ${nt.v}% occupied" tabindex="0"><div class="tw-b"><span class="grow-y" style="height:${nt.v}%"></span></div><b>${nt.v}%</b><span>${esc(nt.l)}</span></div>`).join('')}</div>`;
    label += ': ' + g.nights.map(nt => nt.l + ' ' + nt.v + '%').join(', ');
  } else if (g.kind === 'share') {
    body = `<div class="ig-share"><div class="sh-bar" data-tip="${esc(g.part.v)} ${esc(g.part.l)} of ${esc(g.whole.v)}: ${g.pct}%" tabindex="0"><span class="grow" style="width:${Math.max(g.pct, 0.8)}%"></span></div><div class="sh-leg"><span><b>${cnt(g.part, g.part.v)}</b> ${esc(g.part.l)} (${g.pct}%)</span><span><b>${cnt(g.whole, g.whole.v)}</b> ${esc(g.whole.l)}</span></div><p class="ig-calc">Calculation: ${esc(g.calc)}</p></div>`;
    label += `: ${g.part.v} ${g.part.l} of ${g.whole.v} ${g.whole.l}, ${g.pct}%`;
  } else if (g.kind === 'board') {
    const mx = Math.max(...g.rows.map(r => r.n));
    body = `<div class="ig-board"><div class="bd-h"><span>Route</span><span>Corridor</span><span>Weekday trips</span></div>${g.rows.map((r, k) => `<div class="bd-r" style="--i:${k}"><span class="bd-route">${esc(r.r)}</span><span class="bd-d">${esc(r.d)}</span><span class="bd-n"><span class="bd-bar"><span class="grow" style="width:${r.n / mx * 100}%"></span></span><b>${cnt({n:r.n}, String(r.n))}</b></span></div>`).join('')}<div class="bd-r bd-t"><span class="bd-route">All</span><span class="bd-d">${esc(g.total.l)} (${esc(g.total.calc)})</span><span class="bd-n"><b>${cnt({n:g.total.n}, String(g.total.n))}</b></span></div></div><div class="ig-extra">${g.extra.map(x => `<div><b>${esc(x.v)}</b><span>${esc(x.l)}</span></div>`).join('')}</div>`;
    label += ': ' + g.rows.map(r => 'Route ' + r.r + ' ' + r.n).join(', ') + ', total ' + g.total.n;
  } else if (g.kind === 'funnel') {
    body = `<div class="ig-funnel">${g.stages.map((st, k) => `<div class="fn-s" style="--w:${k ? 46 : 100}%;--i:${k}"><b>${cnt(st, st.v)}</b><span>${esc(st.l)}</span></div>`).join('')}<div class="fn-rates">${g.rates.map(r => `<div><b>${esc(r.v)}</b><span>${esc(r.l)}</span><small>${esc(r.calc)}</small></div>`).join('')}</div></div>`;
    label += ': ' + g.stages.map(st => st.v + ' ' + st.l).join(' to ');
  } else if (g.kind === 'versus') {
    const mx = Math.max(...g.rows.flatMap(r => [r.a, r.b]));
    body = `<div class="ig-vs">${g.rows.map((r, k) => `<div class="vs-r" style="--i:${k}"><span class="vs-l">${esc(r.l)}</span><div class="vs-bars"><div class="vs-b a" data-tip="${esc(r.la)}: +${r.a}%" tabindex="0"><span class="grow" style="width:${r.a / mx * 100}%"></span><em>${esc(r.la)} <b>+${r.a}%</b></em></div><div class="vs-b b" data-tip="${esc(r.lb)}: +${r.b}%" tabindex="0"><span class="grow" style="width:${r.b / mx * 100}%"></span><em>${esc(r.lb)} <b>+${r.b}%</b></em></div></div></div>`).join('')}</div>`;
    label += ': ' + g.rows.map(r => `${r.l}: ${r.la} +${r.a}%, ${r.lb} +${r.b}%`).join('; ');
  }
  return `<figure class="ig igk-${g.kind} reveal" id="${sid}-ig${i}" aria-label="${esc(label)}">${head}${body}${foot}</figure>`;
}
function countUp(root) {
  root.querySelectorAll('.cu').forEach(el => {
    const n = +el.dataset.n, dec = +el.dataset.dec || 0, pre = el.dataset.pre || '', suf = el.dataset.suf || '', final = el.textContent, t0 = performance.now(), D = 1100;
    const fmt = v => pre + v.toLocaleString('en-US', {minimumFractionDigits: dec, maximumFractionDigits: dec}) + suf;
    const step = t => { const p = Math.min(1, (t - t0) / D), e = 1 - Math.pow(1 - p, 3); el.textContent = p < 1 ? fmt(n * e) : final; if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  });
}

function renderSection(s) {
  const [t0, ...tRest] = s.tables;
  const more = [...(s.more_charts || s.charts).map(c => `<div>${chartHtml(c)}</div>`), ...tRest.map((t,i) => `<div class="tbl${t.wide?' wide':''}" id="${s.id}-t${i+1}">${tableHtml(t, s.id+'-t'+(i+1))}</div>`)];
  const nNarrow = more.filter(h => !h.startsWith('<div class="tbl wide"')).length;
  if (more.length && nNarrow % 2 === 1 && !more[more.length-1].startsWith('<div class="tbl wide"')) more[more.length-1] = more[more.length-1].replace(/^<div( class="tbl")?/, m => m.includes('class') ? '<div class="tbl wide"' : '<div class="wide"');
  const calcLine = t => t ? `<span class="calc-line"><b>Calculation:</b> ${esc(t)}</span>` : '';
  const stats = s.cards.map(([k,l,v,sub,src], i) => `<div class="art-stat reveal"><span class="as-k">${esc(k)}</span><b class="as-v">${esc(v)}</b><span class="as-l">${esc(l)}</span><span class="as-p">${emph(sub)}</span>${calcLine((s.card_calc||[])[i])}<span class="src-inline">Source: ${esc(src)}</span></div>`).join('');
  const steps = s.calc_steps ? `<div class="calc-steps reveal" id="${s.id}-calc"><h3>How the key insight is calculated</h3><div class="scroll" tabindex="0" aria-label="How the key insight is calculated"><table><thead><tr><th scope="col">Step</th><th scope="col">Calculation</th><th scope="col" class="n">Result</th><th scope="col">Source</th></tr></thead><tbody>${s.calc_steps.map(([a,b,c2,d]) => `<tr${/^\d+\. New visitor spending|^7\./.test(a) ? ' class="hi"' : ''}><th scope="row">${esc(a)}</th><td>${b === 'Reported' ? '<span class="muted">Reported by source</span>' : esc(b)}</td><td class="n"><b>${esc(c2)}</b></td><td class="src-cell">${esc(d)}</td></tr>`).join('')}</tbody></table></div></div>` : '';
  const feat = (s.feature || []).length ? `<div class="feat${s.feature.length === 1 ? ' one' : ''}" id="${s.id}-charts">${s.feature.map(c => `<div class="reveal">${chartHtml(c)}</div>`).join('')}</div>` : '';
  const W = (s.details || []).length ? `<div class="dgrid">${s.details.map(d => `<article class="dcard reveal"><span class="dk">${esc(d.k)}</span><b class="dfig">${esc(d.fig)}</b><span class="dfl">${esc(d.fig_l)}</span><p>${emph(d.text)}</p><span class="src-inline">Source: ${esc(d.src)}</span></article>`).join('')}</div>`
    : s.w5h ? ['who','what','when','where','why','how'].map(k => `<p class="w5h-p"><b class="w5h-k">${k[0].toUpperCase()+k.slice(1)}.</b> ${emph(s.w5h[k])}</p>`).join('') + `<p class="src-inline">Sources: ${esc(s.w5h.src)}</p>` : '';
  const NX = s.next ? `<nav class="upnext reveal" aria-label="Next section"><span class="un-k">Up next · section ${S.indexOf(s) + 2} of ${S.length + 1}</span><button type="button" class="un-b" data-go="${s.next.id}">${esc(s.next.tab)} <span aria-hidden="true">→</span></button>${s.next.bridge ? `<p>${emph(s.next.bridge)}</p>` : ''}</nav>` : '';
  const isNews = s.kind === 'News report';
  const item = x => `<li><span class="otag">${esc(x.tag)}</span> ${emph(x.text)}${calcLine(x.calc)}<span class="src-inline">Source: ${esc(x.src)}</span></li>`;
  const F = s.for_ocv ? `<div class="ocv-whole reveal" id="${s.id}-ocv"><h3>What it means for OC Vibe</h3><div class="ow-grid">
      <div class="ow-col"><h4>What it enhances</h4><ul>${s.for_ocv.enhance.map(item).join('')}</ul></div>
      <div class="ow-col"><h4>What OC Vibe needs</h4><ul>${s.for_ocv.need.map(item).join('')}</ul></div></div></div>` : '';
  const CC = s.cc ? `<div class="cc-box reveal" id="${s.id}-cc"><h3>Compare and contrast</h3><div class="scroll" tabindex="0" aria-label="Compare and contrast"><table class="cc-t2"><thead><tr><th scope="col">Type</th><th scope="col">Point</th><th scope="col">Solution</th><th scope="col">Source and date</th></tr></thead><tbody>${s.cc.map(c => `<tr class="cc-${c.type.toLowerCase().replace(/\s+/g,'-')}"><th scope="row"><span class="cc-t">${esc(c.type)}</span></th><td>${emph(c.point)}${calcLine(c.calc)}</td><td>${c.solution ? emph(c.solution) : '<span class="muted">None needed</span>'}</td><td class="src-cell">${esc(c.src)}</td></tr>`).join('')}</tbody></table></div></div>` : '';
  const nMore = more.length + 1;
  return `<section class="page art${isNews ? ' news' : ''}" id="${s.id}" data-title="${esc(s.tab)}">
    <header class="art-h reveal">
      <span class="art-kick">${isNews ? '<span class="kind">News report</span> · ' : (s.kind ? `<span class="kind">${esc(s.kind)}</span> · ` : '')}${esc(s.tab)}</span>
      <h2 class="art-head">${esc(s.head || s.q)}</h2>
      ${s.dek ? `<p class="art-dek">${esc(s.dek)}</p>` : ''}
      <p class="art-by">By Visit Anaheim Business Intelligence · ${esc(DATA.prepared)} · <span class="badge">${esc(s.period)}</span></p>
    </header>
    <div class="art-lede-wrap">
      <div class="answer art-lede reveal" id="ans-${s.id}"><div class="answer-t"><span class="answer-l">${isNews ? 'The lede' : 'Key insight'}</span><p>${s.dateline ? `<span class="dline">${esc(s.dateline)}</span> ` : ''}${emph(s.ans)}</p>${s.ans_src ? `<span class="src-inline">Source: ${esc(s.ans_src)}</span>` : ''}</div><div class="answer-key" aria-label="Key number"><span class="ak-v">${esc(s.hv)}</span><span class="ak-l">${esc(s.hl)}</span></div></div>
      ${s.nut ? `<div class="nut reveal" id="${s.id}-nut"><span class="nut-l">Why it matters</span><p>${emph(s.nut)}</p></div>` : ''}
    </div>
    ${(s.info || []).length ? `<div class="ig-wrap${s.info.length > 1 ? ' two' : ''}" id="${s.id}-ig"><h3 class="ig-k">At a glance</h3>${s.info.map((g, i) => infoHtml(g, s.id, i)).join('')}</div>` : ''}
    <section class="art-nums reveal" aria-label="By the numbers"><h3>By the numbers</h3><div class="nums">${stats}</div></section>
    ${steps}
    ${W ? `<div class="art-w5h reveal" id="${s.id}-w5h"><h3>The details</h3><p class="d-sub">Who, what, when, where, why and how, each with its figure, source and date.</p>${W}</div>` : ''}
    ${isNews ? `<div class="an-band reveal" id="${s.id}-analysis"><span class="kind">Analysis</span><h3>What the data shows</h3><p><b>The question:</b> ${esc(s.q)}</p></div>` : `<p class="art-q"><b>The question:</b> ${esc(s.q)}</p>`}
    ${(s.maps || []).length ? `<div class="mp-wrapall" id="${s.id}-maps">${s.maps.map((m, i) => `<figure class="mp reveal" id="${s.id}-map${i}"><header class="ig-h"><h4>${esc(m.title)}</h4><p>${esc(m.sub)}</p></header><div class="mp-grid"><div class="mp-canvas">${mapSvg(MAPGEO, m)}</div>${mapLegend(m)}</div><p class="ig-src">Source: ${esc(m.src)}. Map: ${esc(MAPGEO.src)}; circles placed at each metro's principal city or each country's center.</p></figure>`).join('')}</div>` : ''}
    ${feat}
    <figure class="art-fig tbl reveal" id="${s.id}-t0">${tableHtml(t0, s.id+'-t0')}</figure>
    ${F}
    ${CC}
    <details class="more-d" id="${s.id}-more"><summary><span class="md-ic" aria-hidden="true">+</span><span class="md-t"><b>More data and notes</b><span class="md-s">${nMore} more charts and tables, plus the notes and data-quality caveats behind this section. Don't skip these before you quote a number.</span></span><span class="md-btn"><span class="md-open">Show</span><span class="md-close">Hide</span></span></summary>
      <div class="sec-more">${more.join('')}</div>
      <div class="notes-box" id="${s.id}-notes"><h3>Notes and data quality</h3><ul>${s.notes.map(n => `<li>${emph(n)}</li>`).join('')}</ul></div>
    </details>
    ${NX}
  </section>`;
}
function wireMore(root) {
  root.querySelectorAll('.more-b').forEach(b => b.onclick = () => {
    const key = b.dataset.key, [sid, ti] = [key.split('-t')[0], +key.split('-t')[1]];
    FULL.has(key) ? FULL.delete(key) : FULL.add(key);
    const s = S.find(x => x.id === sid); $(key).innerHTML = tableHtml(s.tables[ti], key); wireMore($(key)); $(key).querySelector('.more-b').focus();
  });
}
$('secHost').outerHTML = S.map(renderSection).join('');
wireMore(document);

/* ---------- overview: key takeaways (one bold metric per section) ---------- */
$('keyTk').innerHTML = S.filter(s => s.id !== 'p-appx').map((s, i) => `<button type="button" class="kt reveal" data-go="${s.id}" style="--i:${i}"><span class="kt-k">${esc(s.tab)}</span><b class="kt-v">${esc(s.hv)}</b><span class="kt-l">${esc(s.hl)}</span><span class="kt-h">${emph(s.head)}</span><span class="kt-s">${esc(s.period)}</span><span class="kt-go">Read the section <span aria-hidden="true">→</span></span></button>`).join('');
/* ---------- overview: questions and short answers ---------- */
$('qa').innerHTML = S.map(s => `<button type="button" class="qa-row" data-go="${s.id}"><span class="qa-b"><span class="qa-q">${esc(s.q)}</span><span class="qa-a">${emph(s.ans)}</span>${s.ans_src ? `<span class="src-inline">Source: ${esc(s.ans_src)}</span>` : ''}</span><span class="qa-v"><b>${esc(s.hv)}</b><small>${esc(s.hl)}</small></span><span class="qa-go" aria-hidden="true">›</span></button>`).join('');

/* ---------- sources page ---------- */
$('takeaways').innerHTML = DATA.takeaways.map(t => { const k = t.lastIndexOf(' (Source: '); let body = k > 0 ? t.slice(0,k) : t, src = k > 0 ? t.slice(k+10, -1) : ''; const c = body.indexOf(' (Calculation: '); let calc = ''; if (c > 0) { calc = body.slice(c+15, -1); body = body.slice(0, c); } return `<li>${emph(body)}${calc ? `<span class="calc-line"><b>Calculation:</b> ${esc(calc)}</span>` : ''}${src ? `<span class="src-inline">Source: ${esc(src)}</span>` : ''}</li>`; }).join('');
$('dqList').innerHTML = DQ.map(t => `<li>${emph(t)}</li>`).join('');
/* Update schedule and planned sources (Oct. 14, 2026) */
{ const U = DATA.schedule;
  $('updLede').innerHTML = emph(U.lede);
  $('updCards').innerHTML = `<div class="dgrid">${U.details.map(d => `<article class="dcard reveal"><span class="dk">${esc(d.k)}</span><b class="dfig">${esc(d.fig)}</b><span class="dfl">${esc(d.fig_l)}</span><p>${emph(d.text)}</p><span class="src-inline">Source: ${esc(d.src)}</span></article>`).join('')}</div>`;
  $('updTable').innerHTML = tableHtml(Object.assign({ full: true, hi: -1 }, U.table), 'upd-t');
  $('updPlanned').innerHTML = tableHtml(Object.assign({ full: true, hi: -1, sub: 'No figures from these sources appear until the data is received, checked and cleared for sharing. Each is added at the next quarterly update after it arrives.' }, U.planned), 'upd-p'); }
$('srcList').innerHTML = DATA.sources.map(([name, desc]) => `<li class="src-item"><h4>${esc(name)}</h4><p>${esc(desc)}</p></li>`).join('');
$('regTbl').innerHTML = tableHtml({title:'Sources used in this report', sub:`${DATA.register.length} sources`, cols:[['Source',0],['Document',0],['Period covered',0],['Published or pulled',0],['Used for',0],['How it was checked',0]], rows:DATA.register, hi:-1, full:true, src:'Visit Anaheim Business Intelligence, Oct. 12, 2026'}, 'reg');
$('recList').innerHTML = `<div class="scroll" tabindex="0" aria-label="Recommendations"><table><thead><tr><th scope="col">What to do</th><th scope="col">Who</th><th scope="col">When</th><th scope="col">Why</th><th scope="col">How we'll measure it</th></tr></thead><tbody>${RECS_T.map(r => `<tr><th scope="row">${esc(r[0])}</th><td>${esc(r[1])}</td><td>${esc(r[2])}</td><td>${emph(r[3])}</td><td>${esc(r[4])}</td></tr>`).join('')}</tbody></table></div>`;

/* ---------- BI Pulse Summary ---------- */
const LABEL = Object.fromEntries(S.map(s => [s.id, s.tab]));
const MAIN = DATA.main;
let ANN = null;
function renderAnn() {
  const lead = 'main', st = MAIN, today = new Date();   // the overview's main announcement (facts only)
  const prepared = `Prepared by Visit Anaheim Business Intelligence with data through Sept. 2026, ${DATA.prepared}. Updated quarterly; next scheduled update ${DATA.schedule.next}.`;
  ANN = {st, lead, hl: 'OC Vibe market update', dateline: `ANAHEIM, Calif. (${apDate(today)}):`, prepared};
  const max = Math.max(...st.chart.rows.map(r => Math.abs(r[1])), 1e-9);
  const bars = st.chart.rows.map(([l,v,t,hi]) => `<div class="ann-bar${hi?' hi':''}${v<0?' neg':''}" data-tip="${esc(l)}: ${esc(t)}" tabindex="0"><span class="l">${esc(l)}</span><span class="t" aria-hidden="true"><span class="f" style="width:${Math.max(2, Math.abs(v)/max*100).toFixed(1)}%"></span></span><span class="v">${v>0?'▲':v<0?'▼':'▶'}&#8239;${esc(t.replace(/^\+/, '+'))}</span></div>`).join('');
  $('annPaper').innerHTML = `
    <div class="ann-mast"><span class="np">BI Pulse Summary</span><span class="e">Visit Anaheim Business Intelligence · Data through Sept. 2026 · Prepared for OC Vibe</span></div>
    <div class="ann-meta"><span class="over">For immediate release</span></div>
    <p class="ann-kick">Highlight: <b>${esc(ANN.hl)}</b></p>
    <h2 class="ann-h" id="annHead">${esc(st.head)}</h2>
    <p class="ann-dek">${esc(st.dek)}</p>
    <section class="ann-nums" aria-label="By the numbers"><h3>By the numbers</h3><div class="ann-strip">${st.stats.map(([v,l,src], i) => `<div class="ann-stat"><b>${esc(v)}</b><span>${esc(l)}</span>${(st.stat_calc||[])[i] ? `<small>Calculation: ${esc(st.stat_calc[i])}</small>` : ''}<small>Source: ${esc(src)}</small></div>`).join('')}</div></section>
    <div class="ann-cols"><p class="lede"><span class="ann-dl">${ANN.dateline}</span> ${emph(st.lede)}</p>${st.paras.map(p => `<p>${emph(p)}</p>`).join('')}</div>
    <figure class="ann-box ann-fig ann-wide" role="img" aria-label="${esc(st.chart.title)}: ${esc(st.chart.rows.map(r => r[0]+' '+r[2]).join(', '))}">
      <figcaption>${esc(st.chart.title)}</figcaption><div class="ann-bars">${bars}</div><p class="src">Source: ${esc(st.chart.src)}.</p>
    </figure>
    <div class="ann-foot"><p><b>About the data:</b> ${esc(st.srcs.join('; '))}. ${esc(prepared)}</p><p class="ann-end">###</p></div>`;
}
function annText() {
  if (!ANN) return '';
  const {st, dateline, prepared, hl} = ANN;
  const out = ['BI PULSE SUMMARY', 'Visit Anaheim Business Intelligence · Data through Sept. 2026', '', 'FOR IMMEDIATE RELEASE', '', `Highlight: ${hl}`, st.head, st.dek, '', `${dateline} ${st.lede}`, ''];
  st.paras.forEach(p => out.push(p, ''));
  out.push('By the numbers'); st.stats.forEach(([v,l,src]) => out.push(`- ${v}: ${l} (Source: ${src})`));
  out.push('', `About the data: ${st.srcs.join('; ')}. ${prepared}`, '', '###');
  return out.join('\n');
}
function annHtml() {
  if (!ANN) return '';
  const {st, dateline, prepared, hl} = ANN;
  const ff = "font-family:'Sharp Sans Disp No2','Proxima Nova',Arial,sans-serif;color:#231F20;";
  const P = (t, x='') => `<p style="${ff}font-size:11pt;line-height:1.45;margin:0 0 10pt;${x}">${t}</p>`;
  return `<div style="${ff}"><p style="${ff}font-size:20pt;font-weight:900;font-style:italic;color:#125C60;margin:6pt 0 2pt">BI Pulse Summary</p>` +
    P('Visit Anaheim Business Intelligence · Data through Sept. 2026', 'font-size:9pt;') + P('<b>FOR IMMEDIATE RELEASE</b>', 'font-size:9pt;letter-spacing:.06em;') +
    P(`<b>HIGHLIGHT: ${esc(hl.toUpperCase())}</b>`, 'font-size:9pt;letter-spacing:.1em;color:#125C60;margin:10pt 0 0;') +
    `<h1 style="${ff}font-size:22pt;line-height:1.1;font-weight:900;font-style:italic;color:#125C60;margin:12pt 0 6pt">${esc(st.head)}</h1>` +
    `<h2 style="${ff}font-size:13pt;font-weight:700;margin:0 0 12pt">${esc(st.dek)}</h2>` + P(`<b>${dateline}</b> ${emph(st.lede).replace(/<b class="kv">/g,'<b>')}`) + st.paras.map(p => P(emph(p).replace(/<b class="kv">/g,'<b>'))).join('') +
    `<p style="${ff}font-size:10pt;font-weight:700;letter-spacing:.1em;margin:12pt 0 4pt">BY THE NUMBERS</p><ul style="${ff}font-size:11pt;margin:0 0 10pt">${st.stats.map(([v,l,src]) => `<li><b>${esc(v)}</b>: ${esc(l)} (Source: ${esc(src)})</li>`).join('')}</ul>` +
    P(`<i>About the data: ${esc(st.srcs.join('; '))}. ${esc(prepared)}</i>`, 'font-size:9pt;') + P('###', 'text-align:center;') + '</div>';
}
async function annCopy() {
  const rich = true;
  const txt = annText(), html = annHtml();
  try {
    if (rich && window.ClipboardItem && navigator.clipboard && navigator.clipboard.write) {
      await navigator.clipboard.write([new ClipboardItem({'text/html': new Blob([html], {type:'text/html'}), 'text/plain': new Blob([txt], {type:'text/plain'})})]);
    } else if (navigator.clipboard && navigator.clipboard.writeText) { await navigator.clipboard.writeText(txt); }
    else throw new Error('no clipboard');
    toast('Summary copied. It keeps its formatting in Word or Outlook and pastes as plain text elsewhere.');
  } catch (_) {
    const ok = (() => { try {
      const box = document.createElement(rich ? 'div' : 'textarea');
      if (rich) { box.contentEditable = 'true'; box.innerHTML = html; } else box.value = txt;
      box.style.cssText = 'position:fixed;left:-9999px;top:0;opacity:0'; document.body.appendChild(box);
      if (rich) { const r = document.createRange(); r.selectNodeContents(box); const sl = getSelection(); sl.removeAllRanges(); sl.addRange(r); } else box.select();
      const res = document.execCommand('copy'); box.remove(); getSelection().removeAllRanges(); return res; } catch(e) { return false; } })();
    toast(ok ? 'Summary copied.' : 'Copy is blocked here. Select the summary text and copy it manually.');
  }
}
$('annCopy').onclick = () => annCopy();
renderAnn();

/* ---------- full screen ---------- */
const fsEl = () => document.fullscreenElement || document.webkitFullscreenElement;
function fsSync() {
  const on = !!fsEl() || $('app').classList.contains('fs-fallback');
  $('app').classList.toggle('fs-on', on); $('fsBtn').textContent = on ? 'Exit full screen' : 'Full screen'; $('fsBtn').setAttribute('aria-pressed', on);
}
$('fsBtn').onclick = async () => {
  const app = $('app');
  if (fsEl()) { try { await (document.exitFullscreen || document.webkitExitFullscreen).call(document); } catch(_){} return fsSync(); }
  if (app.classList.contains('fs-fallback')) { app.classList.remove('fs-fallback'); return fsSync(); }
  const root = document.documentElement, req = root.requestFullscreen || root.webkitRequestFullscreen;
  try { if (!req) throw 0; await req.call(root); } catch(_) { app.classList.add('fs-fallback'); app.scrollTop = 0; }
  fsSync();
};
document.addEventListener('fullscreenchange', fsSync);
document.addEventListener('webkitfullscreenchange', fsSync);
document.addEventListener('keydown', e => { if (e.key==='Escape' && $('app').classList.contains('fs-fallback')) { $('app').classList.remove('fs-fallback'); fsSync(); } });

/* ---------- pages, sidebar, section tabs ---------- */
const PAGES = ['p-summary', ...S.map(s => s.id), 'p-notes'];
const SIDE = [['p-summary','Overview',[['qa','Questions and short answers']]], ...S.map(s => [s.id, s.tab, [['ans-'+s.id, s.kind === 'News report' ? 'The lede' : 'Key insight'],[s.id+'-nut','Why it matters'],[s.id+'-ig','At a glance'],[s.id+'-calc','How it is calculated'],[s.id+'-w5h','The details'],[s.id+'-analysis','Analysis'],[s.id+'-maps','Maps'],[s.id+'-charts','Charts'],[s.id+'-t0','Main table'],[s.id+'-ocv','What it means for OC Vibe'],[s.id+'-cc','Compare and contrast'],[s.id+'-more','More data and notes']].filter(([id]) => id.endsWith('-calc') ? s.calc_steps : id.endsWith('-charts') ? (s.feature||[]).length : id.endsWith('-w5h') ? s.w5h : id.endsWith('-nut') ? s.nut : id.endsWith('-ig') ? (s.info||[]).length : id.endsWith('-analysis') ? s.kind === 'News report' : id.endsWith('-maps') ? (s.maps||[]).length : id.endsWith('-ocv') ? s.for_ocv : id.endsWith('-cc') ? s.cc : true)])];
$('sideList').innerHTML = SIDE.map(([id,t,subs]) => `<li><button type="button" class="top" data-go="${id}">${esc(t)}</button><div class="subs">${subs.map(([sid,st]) => `<button type="button" class="sub" data-go="${id}" data-target="${sid}">${esc(st)}</button>`).join('')}</div></li>`).join('');
$('secPills').innerHTML = [...SIDE, ['p-notes','Sources']].map(([id,t]) => `<button type="button" class="tab" data-go="${id}">${esc(t)}</button>`).join('');
document.querySelectorAll('[data-go]').forEach(b => b.onclick = () => { goPage(PAGES.indexOf(b.dataset.go), b.dataset.target); if (matchMedia('(max-width:900px)').matches && b.closest('.side')) setSide(false); });
let CUR = 0, LONG = store.get('long') === true;
function goPage(i, target) {
  if (i<0 || i>=PAGES.length) return;
  CUR = i; document.querySelectorAll('.page').forEach((p,k) => p.classList.toggle('cur', k===i)); updateNav();
  const el = target ? $(target) : $(PAGES[i]);
  if (el && el.closest && el.closest('details')) el.closest('details').open = true;
  if (LONG || target) el.scrollIntoView({block:'start'}); else $('main').scrollIntoView({block:'start'});
  try { history.replaceState(null,'','#'+PAGES[i].slice(2)); } catch(_){}
}
function updateNav() {
  const i = CUR, pg = $(PAGES[i]), last = PAGES.length-2, isRef = i===PAGES.length-1;
  $('pgNum').textContent = isRef ? 'Reference' : `Page ${i+1} of ${last+1}`; $('pgTitle').textContent = pg.dataset.title;
  $('prevBtn').disabled = i===0; $('nextBtn').disabled = i>=PAGES.length-1;
  document.querySelectorAll('.side .top, #secPills .tab').forEach(b => b.setAttribute('aria-current', b.dataset.go===PAGES[i]));
  const pc = $('secPills'), cp = pc.querySelector('[aria-current="true"]'); if (cp && pc.scrollWidth > pc.clientWidth) pc.scrollLeft = cp.offsetLeft - (pc.clientWidth - cp.offsetWidth)/2;
}
window.addEventListener('hashchange', () => { const i = PAGES.indexOf('p-' + (location.hash||'').slice(1)); if (i >= 0 && i !== CUR) goPage(i); });
$('prevBtn').onclick = () => goPage(CUR-1);
$('nextBtn').onclick = () => goPage(CUR+1);
function setView(long) { LONG = long; store.set('long', long); $('pages').classList.toggle('single', !long); $('vsOne').setAttribute('aria-pressed', !long); $('vsLong').setAttribute('aria-pressed', long); }
$('vsOne').onclick = () => { setView(false); goPage(CUR); };
$('vsLong').onclick = () => { setView(true); goPage(CUR); };
const io = new IntersectionObserver(es => { if (!LONG) return; es.forEach(en => { if (en.isIntersecting) { CUR = PAGES.indexOf(en.target.id); updateNav(); } }); }, {rootMargin:'-30% 0px -65% 0px'});
PAGES.forEach(id => io.observe($(id)));
$('toTop').onclick = () => window.scrollTo({top:0});
function setNavH() { const n = document.querySelector('.secnav'); document.documentElement.style.setProperty('--navh', ((n ? n.offsetHeight : 0) + 14) + 'px'); }
setNavH(); window.addEventListener('resize', setNavH, {passive:true});
window.addEventListener('scroll', () => { $('toTop').hidden = window.scrollY < 700; }, {passive:true});
function setSide(open) {
  $('layout').classList.toggle('closed', !open); $('sideToggle').textContent = open ? '‹' : '›';
  $('sideToggle').setAttribute('aria-expanded', open); $('sideToggle').setAttribute('aria-label', open ? 'Close section menu' : 'Open section menu'); store.set('side', open);
}
$('sideToggle').onclick = () => setSide($('layout').classList.contains('closed'));
$('collapseAll').onclick = () => { const c = $('side').classList.toggle('collapsed'); $('collapseAll').textContent = c ? 'Show details' : 'Hide details'; $('collapseAll').setAttribute('aria-expanded', !c); };

/* ---------- downloads (attachments) ---------- */
function toast(msg){ const t=$('toast'); t.textContent=msg; t.hidden=false; clearTimeout(toast._t); toast._t=setTimeout(()=>t.hidden=true, 4500); }
let DL = null;
(async () => { try { DL = window.claude && window.claude.use ? await window.claude.use('downloads') : null; } catch(_) { DL = null; } })();
async function saveBlob(blob, filename) {
  if (!DL && window.claude && window.claude.use) { try { DL = await window.claude.use('downloads'); } catch(_){} }
  if (DL) { await DL.save({filename, data: blob}); return; }
  if (window.claude && window.claude.use) throw Object.assign(new Error('unavailable'), {code:'unavailable'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = filename; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
}
function dlError(err, what) {
  const code = err && err.code;
  if (code==='declined') toast(`${what} cancelled.`);
  else if (code==='rate_limited') toast('A save prompt is already open. Try again in a moment.');
  else if (code==='unavailable') toast('Downloads are not available in this view.');
  else toast(`The ${what.toLowerCase()} could not be completed. Try again, or contact the BI team.`);
}
function b64Blob(b64, type){ const bin = atob(b64), u8 = new Uint8Array(bin.length); for (let i=0;i<bin.length;i++) u8[i] = bin.charCodeAt(i); return new Blob([u8], {type}); }
$('dlDeck').onclick = async () => { const b=$('dlDeck'); b.disabled = true;
  try { await saveBlob(b64Blob(ATTACH.deck, 'application/vnd.openxmlformats-officedocument.presentationml.presentation'), 'OC_Vibe_Insights.pptx'); toast('Download ready.'); } catch (err) { dlError(err, 'Download'); } finally { b.disabled = false; } };
$('dlCsv').onclick = async () => { const b=$('dlCsv'); b.disabled = true;
  const q = v => '"' + String(v && typeof v === 'object' ? v.t : v).replace(/"/g,'""') + '"';
  const lines = [];
  S.forEach(sec => sec.tables.forEach(t => { lines.push(q(sec.tab + ': ' + t.title)); lines.push(t.cols.map(c => q(c[0])).join(',')); t.rows.forEach(r => lines.push(r.map(q).join(','))); lines.push(q('Source: ' + t.src)); lines.push(''); }));
  try { await saveBlob(new Blob(['\ufeff' + lines.join('\r\n')], {type:'text/csv'}), 'OC_Vibe_Insights_data.csv'); toast('Download ready.'); } catch (err) { dlError(err, 'Download'); } finally { b.disabled = false; } };

/* ---------- export to PDF ---------- */
function loadScript(src){ return new Promise((res,rej) => { if (document.querySelector(`script[src="${src}"]`)) return res(); const s=document.createElement('script'); s.src=src; s.onload=res; s.onerror=()=>rej(new Error('load')); document.head.appendChild(s); }); }
const nextFrame = () => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
async function buildPdf(ids) {
  ids = ids && ids.length ? ids : PAGES;
  await loadScript('https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js');
  await loadScript('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js');
  const root = document.documentElement, app = $('app'), prevTheme = root.getAttribute('data-theme'), wasLong = LONG, scrollY = window.scrollY;
  root.setAttribute('data-theme','light'); app.classList.add('exporting'); setView(true);
  const closedD = [...document.querySelectorAll('details.more-d:not([open])')]; closedD.forEach(d => d.open = true); document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
  const st = document.createElement('style'); st.textContent = '.exporting{width:860px}.exporting .grid2,.exporting .sec-more{grid-template-columns:minmax(0,1fr)!important}.exporting .page{break-inside:auto}';
  document.head.appendChild(st);
  await document.fonts.ready; await nextFrame();
  try {
    const { jsPDF } = window.jspdf; const pdf = new jsPDF({unit:'pt', format:'letter', orientation:'portrait'});
    const PW=612, PH=792, M=54, CW=PW-2*M, CH=PH-2*M-24, GAP=12; let y=M;
    const blocks = [{el:$('band'), newPage:false}];
    const expand = el => el.tagName === 'SUMMARY' ? [] : (['grid2','stack','qbody','qside','ann','ann-paper','ann-grid','sec-more','art-grid','art-body','more-d'].some(c => el.classList.contains(c))) ? [...el.children].flatMap(expand) : [el];
    ids.forEach((id,pi) => [...$(id).children].flatMap(expand).forEach((ch,ci) => { if (ch.offsetHeight>0) blocks.push({el:ch, newPage: pi>0 && ci===0}); }));
    for (const blk of blocks) {
      const cv = await html2canvas(blk.el, {scale:1.6, backgroundColor:'#FFFFFF', logging:false});
      const ratio = CW / cv.width, hPt = cv.height * ratio;
      if (blk.newPage || (y > M && y + Math.min(hPt, CH) > M + CH)) { pdf.addPage(); y = M; }
      if (hPt > CH && hPt <= CH*1.15) { if (y > M) { pdf.addPage(); y = M; } const wPt = CW*CH/hPt; pdf.addImage(cv.toDataURL('image/jpeg', 0.85), 'JPEG', M+(CW-wPt)/2, y, wPt, CH); y += CH + GAP; continue; }
      let offPx = 0;
      while (offPx < cv.height) {
        const slicePx = Math.min(cv.height-offPx, Math.floor((M+CH-y)/ratio));
        const part = document.createElement('canvas'); part.width = cv.width; part.height = slicePx;
        part.getContext('2d').drawImage(cv, 0, offPx, cv.width, slicePx, 0, 0, cv.width, slicePx);
        pdf.addImage(part.toDataURL('image/jpeg', 0.85), 'JPEG', M, y, CW, slicePx*ratio);
        offPx += slicePx; y += slicePx*ratio + GAP;
        if (offPx < cv.height) { pdf.addPage(); y = M; }
      }
    }
    const total = pdf.getNumberOfPages();
    for (let i=1;i<=total;i++) {
      pdf.setPage(i);
      const fc = document.createElement('canvas'); fc.width = CW*3; fc.height = 42; const g = fc.getContext('2d');
      g.fillStyle='#FFFFFF'; g.fillRect(0,0,fc.width,fc.height); g.fillStyle='#43A3A3'; g.fillRect(0,0,fc.width,3);
      g.fillStyle='#231F20'; g.font='350 26px "Sharp Sans Disp No2", sans-serif'; g.textBaseline='bottom';
      g.fillText('Visit Anaheim | visitanaheim.org', 0, 40);
      const rt = `OC Vibe Insights · Data through Sept. 2026  ·  Page ${i} of ${total}`; g.fillText(rt, fc.width - g.measureText(rt).width, 40);
      pdf.addImage(fc.toDataURL('image/png'), 'PNG', M, PH-M+6, CW, 14);
    }
    return pdf.output('blob');
  } finally {
    closedD.forEach(d => d.open = false);
    st.remove(); app.classList.remove('exporting');
    if (prevTheme===null) root.removeAttribute('data-theme'); else root.setAttribute('data-theme', prevTheme);
    setView(wasLong); goPage(CUR); window.scrollTo(0, scrollY);
  }
}
/* ---------- export chooser: pick sections and format ---------- */
const pageTitle = id => id==='p-summary' ? 'Overview (BI Pulse summary)' : id==='p-notes' ? 'Sources, recommendations and notes' : (S.find(x => x.id===id)||{}).tab || id;
function csvFor(ids) {
  const q = v => '"' + String(v && typeof v === 'object' ? v.t : v).replace(/"/g,'""') + '"';
  const lines = [];
  S.filter(sec => ids.includes(sec.id)).forEach(sec => sec.tables.forEach(t => { lines.push(q(sec.tab + ': ' + t.title)); lines.push(t.cols.map(c => q(c[0])).join(',')); t.rows.forEach(r => lines.push(r.map(q).join(','))); lines.push(q('Source: ' + t.src)); lines.push(''); }));
  return lines;
}

/* Excel export (Oct. 13, 2026): a real .xlsx built with JSZip; one sheet per section, every table with its source; numbers stay numbers */
async function xlsxFor(ids) {
  const z = new JSZip(), xe = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])).replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, '');
  const cv = v => v && typeof v === 'object' ? v.t : v;
  const sheets = [{ name: 'About', rows: [[{ v: 'OC Vibe Insights: data tables', s: 1 }], [`Visit Anaheim Business Intelligence · prepared ${DATA.prepared} · data through Sept. 2026`], ['Contact: bi@visitanaheim.org'], [DATA.schedule.line], [],
    ['Each sheet is one section. Every table is followed by its source and period. Values marked F are forecasts.'], ['CoStar, STR and Visa are licensed data: share summaries outside Visit Anaheim, not raw exports.']] }];
  const used = new Set(['About']);
  S.filter(sec => ids.includes(sec.id)).forEach(sec => {
    const rows = [[{ v: sec.tab, s: 1 }], [sec.head || ''], []];
    sec.tables.forEach(t => { rows.push([{ v: t.title, s: 2 }]); rows.push(t.cols.map(c => ({ v: c[0], s: 3 }))); t.rows.forEach(r => rows.push(r.map(cv))); rows.push([{ v: 'Source: ' + t.src, s: 4 }]); rows.push([]); });
    let nm = sec.tab.replace(/[\\/?*[\]:]/g, ' ').slice(0, 31); while (used.has(nm)) nm = nm.slice(0, 29) + '_' + used.size; used.add(nm);
    sheets.push({ name: nm, rows });
  });
  const col = i => { let s = ''; i++; while (i) { const m = (i - 1) % 26; s = String.fromCharCode(65 + m) + s; i = Math.floor((i - 1) / 26); } return s; };
  const cell = (v, r, c) => {
    const ref = col(c) + (r + 1); let s = 0;
    if (v && typeof v === 'object' && 'v' in v) { s = v.s; v = v.v; }
    const t = String(v == null ? '' : v).trim().replace(/−/g, '-');
    if (!s && /^-?\d{1,3}(,\d{3})*(\.\d+)?$|^-?\d+(\.\d+)?$/.test(t) && !/^(19|20)\d\d$/.test(t)) return `<c r="${ref}"><v>${t.replace(/,/g, '')}</v></c>`;
    if (!s && /^[+-]?\d+(\.\d+)?%$/.test(t)) return `<c r="${ref}" s="5"><v>${parseFloat(t) / 100}</v></c>`;
    if (!s && /^-?\$\d{1,3}(,\d{3})*(\.\d+)?$|^-?\$\d+(\.\d+)?$/.test(t)) return `<c r="${ref}" s="6"><v>${t.replace(/[$,]/g, '')}</v></c>`;
    return t ? `<c r="${ref}" t="inlineStr"${s ? ` s="${s}"` : ''}><is><t xml:space="preserve">${xe(t)}</t></is></c>` : '';
  };
  sheets.forEach((sh, k) => {
    const data = sh.rows.map((r, i) => `<row r="${i + 1}">${r.map((v, j) => cell(v, i, j)).join('')}</row>`).join('');
    z.file(`xl/worksheets/sheet${k + 1}.xml`, `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetViews><sheetView workbookViewId="0" showGridLines="0"/></sheetViews><cols><col min="1" max="1" width="48" customWidth="1"/><col min="2" max="12" width="20" customWidth="1"/></cols><sheetData>${data}</sheetData></worksheet>`);
  });
  z.file('[Content_Types].xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>${sheets.map((_, k) => `<Override PartName="/xl/worksheets/sheet${k + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>`).join('')}</Types>`);
  z.file('_rels/.rels', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>`);
  z.file('xl/workbook.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>${sheets.map((sh, k) => `<sheet name="${xe(sh.name)}" sheetId="${k + 1}" r:id="rId${k + 1}"/>`).join('')}</sheets></workbook>`);
  z.file('xl/_rels/workbook.xml.rels', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">${sheets.map((_, k) => `<Relationship Id="rId${k + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet${k + 1}.xml"/>`).join('')}<Relationship Id="rId${sheets.length + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>`);
  z.file('xl/styles.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><numFmts count="2"><numFmt numFmtId="164" formatCode="0.0%"/><numFmt numFmtId="165" formatCode="&quot;$&quot;#,##0.##"/></numFmts><fonts count="5"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="15"/><color rgb="FF125C60"/><name val="Calibri"/></font><font><b/><sz val="12"/><color rgb="FF125C60"/><name val="Calibri"/></font><font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font><font><i/><sz val="9"/><color rgb="FF555555"/><name val="Calibri"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF125C60"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="7"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/><xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1"/><xf numFmtId="0" fontId="3" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/><xf numFmtId="0" fontId="4" fillId="0" borderId="0" xfId="0" applyFont="1"/><xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/><xf numFmtId="165" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>`);
  return z.generateAsync({ type: 'blob', compression: 'DEFLATE', mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
}
const PUBLIC_URL = 'https://oc-vibe-insights.vercel.app/';
const shareUrl = ids => PUBLIC_URL + (ids.length === 1 && ids[0] !== 'p-summary' ? '#' + ids[0].replace('p-', '') : '');
async function copyText(t, input) {
  try { await navigator.clipboard.writeText(t); return true; } catch (_) {}
  try { input.focus(); input.select(); return document.execCommand('copy'); } catch (_) { return false; }
}
(function initExport(){
  const dlg = $('expDlg'), list = $('expList');
  list.innerHTML = PAGES.map(id => `<label class="exp-item"><input type="checkbox" value="${id}" checked> <span>${esc(pageTitle(id))}</span></label>`).join('');
  const boxes = () => [...list.querySelectorAll('input')];
  const fmtNow = () => (dlg.querySelector('input[name="expFmt"]:checked')||{}).value || 'pdf';
  const sync = () => { const n = boxes().filter(b => b.checked).length, f = fmtNow(); $('expGo').disabled = n===0; $('expCount').textContent = n===PAGES.length ? 'All sections selected' : `${n} of ${PAGES.length} selected`;
    $('expLinkBox').hidden = f !== 'link'; $('expShare').hidden = f !== 'link' || !navigator.share; $('expGo').textContent = f === 'link' ? 'Copy link' : 'Export';
    $('expLink').value = shareUrl(boxes().filter(b => b.checked).map(b => b.value)); };
  dlg.querySelectorAll('input[name="expFmt"]').forEach(r => r.addEventListener('change', sync));
  $('expShare').onclick = async () => { try { await navigator.share({ title: 'OC Vibe Insights', url: $('expLink').value }); dlg.close(); } catch (_) {} };
  list.addEventListener('change', sync);
  $('expAll').onclick = () => { boxes().forEach(b => b.checked = true); sync(); };
  $('expNone').onclick = () => { boxes().forEach(b => b.checked = false); sync(); };
  $('expCur').onclick = () => { boxes().forEach(b => b.checked = b.value===PAGES[CUR]); sync(); };
  $('expCancel').onclick = () => dlg.close();
  dlg.addEventListener('click', e => { if (e.target===dlg) dlg.close(); });
  $('exportPdf').onclick = () => { sync(); if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open',''); };
  $('expGo').onclick = async () => {
    const ids = boxes().filter(b => b.checked).map(b => b.value), fmt = fmtNow();
    if (fmt === 'link') { const ok = await copyText($('expLink').value, $('expLink')); toast(ok ? 'Link copied: ' + $('expLink').value : 'Copy the link from the box above.'); if (ok) dlg.close(); return; }
    dlg.close();
    const btn = $('exportPdf'); btn.disabled = true; const label = btn.textContent;
    const all = ids.length===PAGES.length, suffix = all ? '' : '-' + (ids.length===1 ? ids[0].replace('p-','') : 'selected');
    try {
      if (fmt==='pptx') {
        btn.textContent = 'Preparing PowerPoint…';
        const deck = b64Blob(ATTACH.deck, 'application/vnd.openxmlformats-officedocument.presentationml.presentation');
        if (all) { await saveBlob(deck, 'OC_Vibe_Insights.pptx'); toast('PowerPoint ready.'); return; }
        const content = S.filter(x => x.id !== 'p-appx');
        const names = ids.map(id => id==='p-summary' ? 'Introduction' : id==='p-notes' ? 'Next steps' : id==='p-appx' ? 'Appendix' : (S.find(x => x.id===id)||{}).tab).filter(Boolean);
        if (content.every(x => ids.includes(x.id))) names.push('Compare and contrast');
        if (typeof JSZip === 'undefined' || typeof pptxSubset === 'undefined') throw Object.assign(new Error('unavailable'), {code:'unavailable'});
        const blob = await pptxSubset(JSZip, await deck.arrayBuffer(), names);
        await saveBlob(blob, `OC_Vibe_Insights${suffix}.pptx`); toast('PowerPoint ready: the title slide plus the chosen sections.');
      } else if (fmt==='xlsx') {
        if (!S.some(sec => ids.includes(sec.id))) { toast('The selected sections have no data tables. Choose a content section.'); return; }
        btn.textContent = 'Preparing Excel…';
        await saveBlob(await xlsxFor(ids), `OC_Vibe_Insights_data${suffix}.xlsx`); toast('Excel workbook ready.');
      } else if (fmt==='csv') {
        const lines = csvFor(ids);
        if (!lines.length) { toast('The selected sections have no data tables. Choose a content section or export a PDF.'); return; }
        btn.textContent = 'Preparing CSV…';
        await saveBlob(new Blob(['﻿' + lines.join('\r\n')], {type:'text/csv'}), `OC_Vibe_Insights_data${suffix}.csv`); toast('CSV ready.');
      } else {
        btn.textContent = 'Preparing PDF…';
        const ordered = PAGES.filter(id => ids.includes(id));
        const blob = await buildPdf(ordered); await saveBlob(blob, `Visit-Anaheim-OC-Vibe-Insights${suffix}.pdf`); toast('PDF ready.');
      }
    } catch (err) { dlError(err, 'Export'); }
    finally { btn.disabled = false; btn.textContent = label; }
  };
})();

/* ---------- init ---------- */
setView(LONG && !matchMedia('(max-width:640px)').matches);
setSide(matchMedia('(max-width:900px)').matches ? false : store.get('side') === true);
const h = (location.hash||'').slice(1), hi = PAGES.indexOf('p-'+h);
CUR = hi>=0 ? hi : 0;
document.querySelectorAll('.page').forEach((p,k) => p.classList.toggle('cur', k===CUR)); updateNav();
/* open collapsed detail for print and PDF export, then restore */
let _closed = [];
window.addEventListener('beforeprint', () => { _closed = [...document.querySelectorAll('details.more-d:not([open])')]; _closed.forEach(d => d.open = true); });
window.addEventListener('afterprint', () => { _closed.forEach(d => d.open = false); _closed = []; });
/* entrance motion (VA Branded: fade and 12px rise, once; off under reduced motion; content shows without scripts) */
(function(){
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.documentElement.classList.add('js-anim');
  const io2 = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); if (e.target.classList.contains('ig')) countUp(e.target); io2.unobserve(e.target); } }), {rootMargin:'0px 0px -6% 0px'});
  document.querySelectorAll('.reveal').forEach(el => io2.observe(el));
  window.addEventListener('beforeprint', () => document.querySelectorAll('.reveal').forEach(el => el.classList.add('in')));
})();
/* value tooltips: hovering or focusing any chart mark shows its value and highlights it */
(function(){
  const tip = document.createElement('div'); tip.id = 'vtip'; tip.setAttribute('role', 'tooltip'); tip.hidden = true; document.body.appendChild(tip);
  let hot = null;
  const place = (x, y) => { const r = tip.getBoundingClientRect(), W = window.innerWidth; let left = x + 14, top = y - r.height - 12; if (left + r.width > W - 8) left = x - r.width - 14; if (left < 8) left = 8; if (top < 8) top = y + 18; tip.style.left = left + 'px'; tip.style.top = top + 'px'; };
  const show = (el, x, y) => {
    if (hot && hot !== el) { hot.classList.remove('is-hot'); const f0 = hot.closest('figure, .ann-bars, table.heat'); if (f0) f0.classList.remove('hovering'); }
    hot = el; el.classList.add('is-hot'); const f = el.closest('figure, .ann-bars, table.heat'); if (f) f.classList.add('hovering');
    tip.textContent = el.getAttribute('data-tip'); tip.hidden = false; place(x, y);
  };
  const hide = () => { tip.hidden = true; if (hot) { hot.classList.remove('is-hot'); const f = hot.closest('figure, .ann-bars, table.heat'); if (f) f.classList.remove('hovering'); hot = null; } };
  document.addEventListener('pointerover', e => { const el = e.target.closest && e.target.closest('[data-tip]'); if (el) show(el, e.clientX, e.clientY); });
  document.addEventListener('pointermove', e => { if (hot && !tip.hidden) place(e.clientX, e.clientY); });
  document.addEventListener('pointerout', e => { const el = e.target.closest && e.target.closest('[data-tip]'); if (el && !(e.relatedTarget && el.contains(e.relatedTarget))) hide(); });
  document.addEventListener('focusin', e => { const el = e.target.closest && e.target.closest('[data-tip]'); if (el) { const r = el.getBoundingClientRect(); show(el, r.left + r.width / 2, r.top); } });
  document.addEventListener('focusout', e => { if (e.target.closest && e.target.closest('[data-tip]')) hide(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') hide(); });
  window.addEventListener('scroll', () => { if (!hot) return; if (document.activeElement === hot) { const r = hot.getBoundingClientRect(); place(r.left + r.width / 2, r.top); } else hide(); }, {passive: true});
})();
