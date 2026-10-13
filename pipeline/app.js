/* OC Vibe Insights — built on the BI Pulse dashboard template (nav, sidebar, BI Pulse Summary, full screen, PDF export). */
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
function renderSection(s) {
  const [t0, ...tRest] = s.tables;
  const more = [...(s.more_charts || s.charts).map(c => `<div>${chartHtml(c)}</div>`), ...tRest.map((t,i) => `<div class="tbl${t.wide?' wide':''}" id="${s.id}-t${i+1}">${tableHtml(t, s.id+'-t'+(i+1))}</div>`)];
  const nNarrow = more.filter(h => !h.startsWith('<div class="tbl wide"')).length;
  if (more.length && nNarrow % 2 === 1 && !more[more.length-1].startsWith('<div class="tbl wide"')) more[more.length-1] = more[more.length-1].replace(/^<div( class="tbl")?/, m => m.includes('class') ? '<div class="tbl wide"' : '<div class="wide"');
  const calcLine = t => t ? `<span class="calc-line"><b>Calculation:</b> ${esc(t)}</span>` : '';
  const stats = s.cards.map(([k,l,v,sub,src], i) => `<div class="art-stat reveal"><span class="as-k">${esc(k)}</span><b class="as-v">${esc(v)}</b><span class="as-l">${esc(l)}</span><span class="as-p">${emph(sub)}</span>${calcLine((s.card_calc||[])[i])}<span class="src-inline">Source: ${esc(src)}</span></div>`).join('');
  const steps = s.calc_steps ? `<div class="calc-steps reveal" id="${s.id}-calc"><h3>How the key insight is calculated</h3><div class="scroll" tabindex="0" aria-label="How the key insight is calculated"><table><thead><tr><th scope="col">Step</th><th scope="col">Calculation</th><th scope="col" class="n">Result</th><th scope="col">Source</th></tr></thead><tbody>${s.calc_steps.map(([a,b,c2,d]) => `<tr${/^\d+\. New visitor spending|^7\./.test(a) ? ' class="hi"' : ''}><th scope="row">${esc(a)}</th><td>${b === 'Reported' ? '<span class="muted">Reported by source</span>' : esc(b)}</td><td class="n"><b>${esc(c2)}</b></td><td class="src-cell">${esc(d)}</td></tr>`).join('')}</tbody></table></div></div>` : '';
  const feat = (s.feature || []).length ? `<div class="feat${s.feature.length === 1 ? ' one' : ''}" id="${s.id}-charts">${s.feature.map(c => `<div class="reveal">${chartHtml(c)}</div>`).join('')}</div>` : '';
  const W = s.w5h ? ['who','what','when','where','why','how'].map(k => `<p class="w5h-p"><b class="w5h-k">${k[0].toUpperCase()+k.slice(1)}.</b> ${emph(s.w5h[k])}</p>`).join('') + `<p class="src-inline">Sources: ${esc(s.w5h.src)}</p>` : '';
  const item = x => `<li><span class="otag">${esc(x.tag)}</span> ${emph(x.text)}${calcLine(x.calc)}<span class="src-inline">Source: ${esc(x.src)}</span></li>`;
  const F = s.for_ocv ? `<div class="ocv-whole reveal" id="${s.id}-ocv"><h3>What it means for OC Vibe</h3><div class="ow-grid">
      <div class="ow-col"><h4>What it enhances</h4><ul>${s.for_ocv.enhance.map(item).join('')}</ul></div>
      <div class="ow-col"><h4>What OC Vibe needs</h4><ul>${s.for_ocv.need.map(item).join('')}</ul></div></div></div>` : '';
  const CC = s.cc ? `<div class="cc-box reveal" id="${s.id}-cc"><h3>Compare and contrast</h3><div class="scroll" tabindex="0" aria-label="Compare and contrast"><table class="cc-t2"><thead><tr><th scope="col">Type</th><th scope="col">Point</th><th scope="col">Solution</th><th scope="col">Source and date</th></tr></thead><tbody>${s.cc.map(c => `<tr class="cc-${c.type.toLowerCase().replace(/\s+/g,'-')}"><th scope="row"><span class="cc-t">${esc(c.type)}</span></th><td>${emph(c.point)}${calcLine(c.calc)}</td><td>${c.solution ? emph(c.solution) : '<span class="muted">—</span>'}</td><td class="src-cell">${esc(c.src)}</td></tr>`).join('')}</tbody></table></div></div>` : '';
  const nMore = more.length + 1;
  return `<section class="page art" id="${s.id}" data-title="${esc(s.tab)}">
    <header class="art-h reveal">
      <span class="art-kick">${esc(s.tab)}</span>
      <h2 class="art-head">${esc(s.head || s.q)}</h2>
      ${s.dek ? `<p class="art-dek">${esc(s.dek)}</p>` : ''}
      <p class="art-q"><b>The question:</b> ${esc(s.q)}</p>
      <p class="art-by">Visit Anaheim Business Intelligence · ${esc(DATA.prepared)} · <span class="badge">${esc(s.period)}</span></p>
    </header>
    <div class="art-grid">
      <div class="art-body">
        <div class="answer art-lede reveal" id="ans-${s.id}"><div class="answer-t"><span class="answer-l">Key insight</span><p>${emph(s.ans)}</p>${s.ans_src ? `<span class="src-inline">Source: ${esc(s.ans_src)}</span>` : ''}</div><div class="answer-key" aria-label="Key number"><span class="ak-v">${esc(s.hv)}</span><span class="ak-l">${esc(s.hl)}</span></div></div>
        ${steps}
        ${W ? `<div class="art-w5h reveal" id="${s.id}-w5h"><h3>The details</h3>${W}</div>` : ''}
      </div>
      <aside class="art-side" aria-label="By the numbers"><h3>By the numbers</h3>${stats}</aside>
    </div>
    ${feat}
    <figure class="art-fig tbl reveal" id="${s.id}-t0">${tableHtml(t0, s.id+'-t0')}</figure>
    ${F}
    ${CC}
    ${s.id==='p-ocv' ? '<div class="calc-box" id="ocvCalc"></div>' : ''}
    <details class="more-d" id="${s.id}-more"><summary>More data and notes <span class="muted">(${nMore} items)</span></summary>
      <div class="sec-more">${more.join('')}</div>
      <div class="notes-box" id="${s.id}-notes"><h3>Notes and data quality</h3><ul>${s.notes.map(n => `<li>${emph(n)}</li>`).join('')}</ul></div>
    </details>
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

/* ---------- overview: questions and short answers ---------- */
$('qa').innerHTML = S.map(s => `<button type="button" class="qa-row" data-go="${s.id}"><span class="qa-b"><span class="qa-q">${esc(s.q)}</span><span class="qa-a">${emph(s.ans)}</span>${s.ans_src ? `<span class="src-inline">Source: ${esc(s.ans_src)}</span>` : ''}</span><span class="qa-v"><b>${esc(s.hv)}</b><small>${esc(s.hl)}</small></span><span class="qa-go" aria-hidden="true">›</span></button>`).join('');

/* ---------- sources page ---------- */
$('takeaways').innerHTML = DATA.takeaways.map(t => { const k = t.lastIndexOf(' (Source: '); let body = k > 0 ? t.slice(0,k) : t, src = k > 0 ? t.slice(k+10, -1) : ''; const c = body.indexOf(' (Calculation: '); let calc = ''; if (c > 0) { calc = body.slice(c+15, -1); body = body.slice(0, c); } return `<li>${emph(body)}${calc ? `<span class="calc-line"><b>Calculation:</b> ${esc(calc)}</span>` : ''}${src ? `<span class="src-inline">Source: ${esc(src)}</span>` : ''}</li>`; }).join('');
$('dqList').innerHTML = DQ.map(t => `<li>${emph(t)}</li>`).join('');
$('srcList').innerHTML = DATA.sources.map(([name, desc]) => `<li class="src-item"><h4>${esc(name)}</h4><p>${esc(desc)}</p></li>`).join('');
$('regTbl').innerHTML = tableHtml({title:'Sources used in this report', sub:`${DATA.register.length} sources`, cols:[['Source',0],['Document',0],['Period covered',0],['Published or pulled',0],['Used for',0],['How it was checked',0]], rows:DATA.register, hi:-1, full:true, src:'Visit Anaheim Business Intelligence, Oct. 12, 2026'}, 'reg');
$('recList').innerHTML = `<div class="scroll" tabindex="0" aria-label="Recommendations"><table><thead><tr><th scope="col">What to do</th><th scope="col">Who</th><th scope="col">When</th><th scope="col">Why</th><th scope="col">How we'll measure it</th></tr></thead><tbody>${RECS_T.map(r => `<tr><th scope="row">${esc(r[0])}</th><td>${esc(r[1])}</td><td>${esc(r[2])}</td><td>${emph(r[3])}</td><td>${esc(r[4])}</td></tr>`).join('')}</tbody></table></div>`;

/* ---------- BI Pulse Summary ---------- */
const LABEL = Object.fromEntries(S.map(s => [s.id, s.tab]));
const MAIN = DATA.main;
let ANN = null;
function renderAnn() {
  const lead = 'main', st = MAIN, today = new Date();   // the overview's main announcement (facts only)
  const prepared = `Prepared by Visit Anaheim Business Intelligence with data through Sept. 2026, ${DATA.prepared}.`;
  ANN = {st, lead, hl: 'OC Vibe market update', dateline: `ANAHEIM, Calif. (${apDate(today)}):`, prepared};
  const max = Math.max(...st.chart.rows.map(r => Math.abs(r[1])), 1e-9);
  const bars = st.chart.rows.map(([l,v,t,hi]) => `<div class="ann-bar${hi?' hi':''}${v<0?' neg':''}" data-tip="${esc(l)}: ${esc(t)}" tabindex="0"><span class="l">${esc(l)}</span><span class="t" aria-hidden="true"><span class="f" style="width:${Math.max(2, Math.abs(v)/max*100).toFixed(1)}%"></span></span><span class="v">${v>0?'▲':v<0?'▼':'▶'}&#8239;${esc(t.replace(/^\+/, '+'))}</span></div>`).join('');
  $('annPaper').innerHTML = `
    <div class="ann-mast"><span class="np">BI Pulse Summary</span><span class="e">Visit Anaheim Business Intelligence · Data through Sept. 2026 · Prepared for OC Vibe</span></div>
    <div class="ann-meta"><span class="over">For immediate release</span></div>
    <p class="ann-kick">Highlight: <b>${esc(ANN.hl)}</b></p>
    <h2 class="ann-h" id="annHead">${esc(st.head)}</h2>
    <p class="ann-dek">${esc(st.dek)}</p>
    <div class="ann-grid">
      <div class="ann-cols"><p class="lede"><span class="ann-dl">${ANN.dateline}</span> ${emph(st.lede)}</p>${st.paras.map(p => `<p>${emph(p)}</p>`).join('')}</div>
      <aside class="ann-side" aria-label="By the numbers">
        <div class="ann-box"><h3>By the numbers</h3>${st.stats.map(([v,l,src], i) => `<div class="ann-stat"><b>${esc(v)}</b><span>${esc(l)}</span>${(st.stat_calc||[])[i] ? `<small>Calculation: ${esc(st.stat_calc[i])}</small>` : ''}<small>Source: ${esc(src)}</small></div>`).join('')}</div>
        <figure class="ann-box ann-fig" style="margin:0" role="img" aria-label="${esc(st.chart.title)}: ${esc(st.chart.rows.map(r => r[0]+' '+r[2]).join(', '))}">
          <figcaption>${esc(st.chart.title)}</figcaption><div class="ann-bars">${bars}</div><p class="src">Source: ${esc(st.chart.src)}.</p>
        </figure>
      </aside>
    </div>
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
const SIDE = [['p-summary','Overview',[['qa','Questions and short answers']]], ...S.map(s => [s.id, s.tab, [['ans-'+s.id,'Key insight'],[s.id+'-calc','How it is calculated'],[s.id+'-charts','Charts'],[s.id+'-w5h','The details'],[s.id+'-t0','Main table'],[s.id+'-ocv','What it means for OC Vibe'],[s.id+'-cc','Compare and contrast'],[s.id+'-more','More data and notes']].filter(([id]) => id.endsWith('-calc') ? s.calc_steps : id.endsWith('-charts') ? (s.feature||[]).length : id.endsWith('-w5h') ? s.w5h : id.endsWith('-ocv') ? s.for_ocv : id.endsWith('-cc') ? s.cc : true)])];
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
$('prevBtn').onclick = () => goPage(CUR-1);
$('nextBtn').onclick = () => goPage(CUR+1);
function setView(long) { LONG = long; store.set('long', long); $('pages').classList.toggle('single', !long); $('vsOne').setAttribute('aria-pressed', !long); $('vsLong').setAttribute('aria-pressed', long); }
$('vsOne').onclick = () => { setView(false); goPage(CUR); };
$('vsLong').onclick = () => { setView(true); goPage(CUR); };
const io = new IntersectionObserver(es => { if (!LONG) return; es.forEach(en => { if (en.isIntersecting) { CUR = PAGES.indexOf(en.target.id); updateNav(); } }); }, {rootMargin:'-30% 0px -65% 0px'});
PAGES.forEach(id => io.observe($(id)));
$('toTop').onclick = () => window.scrollTo({top:0});
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
(function initExport(){
  const dlg = $('expDlg'), list = $('expList');
  list.innerHTML = PAGES.map(id => `<label class="exp-item"><input type="checkbox" value="${id}" checked> <span>${esc(pageTitle(id))}</span></label>`).join('');
  const boxes = () => [...list.querySelectorAll('input')];
  const sync = () => { const n = boxes().filter(b => b.checked).length; $('expGo').disabled = n===0; $('expCount').textContent = n===PAGES.length ? 'All sections selected' : `${n} of ${PAGES.length} selected`; };
  list.addEventListener('change', sync);
  $('expAll').onclick = () => { boxes().forEach(b => b.checked = true); sync(); };
  $('expNone').onclick = () => { boxes().forEach(b => b.checked = false); sync(); };
  $('expCur').onclick = () => { boxes().forEach(b => b.checked = b.value===PAGES[CUR]); sync(); };
  $('expCancel').onclick = () => dlg.close();
  dlg.addEventListener('click', e => { if (e.target===dlg) dlg.close(); });
  $('exportPdf').onclick = () => { sync(); if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open',''); };
  $('expGo').onclick = async () => {
    const ids = boxes().filter(b => b.checked).map(b => b.value), fmt = (dlg.querySelector('input[name="expFmt"]:checked')||{}).value || 'pdf';
    dlg.close();
    const btn = $('exportPdf'); btn.disabled = true; const label = btn.textContent;
    const all = ids.length===PAGES.length, suffix = all ? '' : '-' + (ids.length===1 ? ids[0].replace('p-','') : 'selected');
    try {
      if (fmt==='csv') {
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

/* ---------- OC Vibe staff inputs: live impact calculator (saved to the artifact's shared db when allowed) ---------- */
(function initCalc(){
  const host = $('ocvCalc'); if (!host) return;
  const MD = MODEL, F = [
    ['hall_cap','Concert hall seats','', 1, ''],
    ['hall_events','Concert hall events a year','', 1, ''],
    ['hall_fill','Concert hall seats filled','%', 1, ''],
    ['small_cap','Theater and club seats','', 1, ''],
    ['small_events','Theater and club events a year','', 1, ''],
    ['small_fill','Theater and club seats filled','%', 1, ''],
    ['other_att','Other new attendance a year (market hall, plazas, festivals)','', 1000, ''],
    ['net_new','Attendees who are net-new visitors to Anaheim','%', 1, ''],
    ['add_day','Anaheim visitors who add a day because of OC Vibe','%', 0.1, ''],
    ['rooms','Hotel rooms open','', 10, ''],
    ['occ','Hotel occupancy','%', 1, ''],
    ['adr','Hotel average nightly rate','$', 1, ''],
  ];
  const BASE = Object.fromEntries(F.map(f => [f[0], f[4]]));
  const ok = v => Number.isFinite(v), fmtM = v => ok(v) ? '$' + (v/1e6).toFixed(1) + 'M' : '—', fmtN = v => ok(v) ? Math.round(v).toLocaleString('en-US') : '—';
  function calc(x) {
    const part = (a, b, c) => [a, b, c].every(Number.isFinite) ? a*b*c/100 : 0, anyVenue = [x.hall_cap, x.small_cap, x.other_att].some(Number.isFinite);
    const attend = anyVenue ? part(x.hall_cap, x.hall_events, x.hall_fill) + part(x.small_cap, x.small_events, x.small_fill) + (Number.isFinite(x.other_att) ? x.other_att : 0) : NaN;
    const nv = attend*x.net_new/100, days = MD.visitors*x.add_day/100, sp1 = Number.isFinite(nv) ? nv*MD.pv : NaN, sp2 = Number.isFinite(days) ? days*MD.per_day : NaN;
    const spend = (Number.isFinite(sp1) || Number.isFinite(sp2)) ? (Number.isFinite(sp1) ? sp1 : 0) + (Number.isFinite(sp2) ? sp2 : 0) : NaN, rn = x.rooms*365*x.occ/100, rev = rn*x.adr;
    return [
      ['Attendance a year', fmtN(attend)], ['Net-new visitors', fmtN(nv)], ['Extra visitor days', fmtN(days)],
      ['New visitor spending', fmtM(spend)], ['Anaheim total economic impact', fmtM(spend*MD.mult_ana)], ['Anaheim jobs supported', fmtN(Math.round(spend/1e6*MD.jobs_ana/10)*10)],
      ['Anaheim state and local taxes', fmtM(spend*MD.tax_ana)], ['Orange County total economic impact', fmtM(spend*MD.mult_oc)],
      ['OC Vibe hotel room nights', fmtN(rn)],
      ['OC Vibe hotel room revenue', fmtM(rev)], ['Anaheim hotel tax (15%)', fmtM(rev*MD.tot)],
    ];
  }
  host.innerHTML = `<h3>Enter OC Vibe's own figures</h3>
    <p class="calc-sub">For OC Vibe staff: enter OC Vibe's own plans or results. Visit Anaheim supplies no assumptions here; results appear only from the figures you enter, converted with Tourism Economics 2025 ratios for Anaheim (jobs, impact, taxes). Saved figures are shared with everyone who can open this page.</p>
    <div class="calc-grid"><form class="calc-in" id="calcForm" autocomplete="off">${F.map(([k,l,u,st]) => `<label class="calc-f"><span>${esc(l)}</span><span class="calc-w">${u==='$'?'<i>$</i>':''}<input type="number" inputmode="decimal" min="0" step="${st}" name="${k}" id="cin-${k}">${u==='%'?'<i>%</i>':''}</span></label>`).join('')}
      <label class="calc-f calc-note"><span>Where these figures come from (optional)</span><input type="text" maxlength="300" name="note" id="cin-note" placeholder="For example: 2027 booking plan, Oct. 2026"></label>
      <div class="calc-acts"><button type="button" class="ctl accent" id="calcSave">Save for Visit Anaheim</button><button type="button" class="ctl" id="calcReset">Clear</button><button type="button" class="ctl" id="calcDl">Download (.csv)</button></div>
      <p class="calc-status" id="calcStatus" aria-live="polite"></p></form>
      <div class="calc-out"><div class="scroll" tabindex="0" aria-label="Calculated impact"><table><thead><tr><th scope="col">Measure</th><th scope="col" class="n">From OC Vibe's figures</th></tr></thead><tbody id="calcBody"></tbody></table></div>
      <p class="src">Method and ratios as in the scenario table above (Tourism Economics 2025 ratios; 2025 dollars; visitors only). Estimates, not forecasts.</p>
      <div id="calcHist"></div></div></div>`;
  const form = $('calcForm');
  const read = () => Object.fromEntries(F.map(([k]) => { const t = form.elements[k].value; return [k, t === '' ? NaN : Math.max(0, parseFloat(t))]; }));
  const fill = v => F.forEach(([k]) => form.elements[k].value = v[k] ?? BASE[k]);
  function render() { const o = calc(read()); $('calcBody').innerHTML = o.map(([l,v],i) => `<tr class="${i===3?'hirow':''}"><th scope="row">${esc(l)}</th><td class="n">${esc(v)}</td></tr>`).join(''); }
  fill(BASE); render();
  form.addEventListener('input', render);
  $('calcReset').onclick = () => { fill(BASE); form.elements.note.value = ''; render(); setStatus('Cleared. Nothing is saved until you choose Save.'); };
  $('calcDl').onclick = async () => {
    const v = read(), o = calc(v), q = s => '"' + String(s).replace(/"/g,'""') + '"';
    const lines = ['"OC Vibe impact: figures entered by OC Vibe staff"', '"Input","Value"', ...F.map(([k,l,u]) => [q(l + (u ? ' ('+u+')' : '')), q(v[k])].join(',')), [q('Note'), q(form.elements.note.value)].join(','), '', '"Measure","From OC Vibe\'s figures"', ...o.map(([l,x]) => [q(l), q(x)].join(',')), '', q('Prepared with the Visit Anaheim BI OC Vibe impact method, ' + apDate(new Date()) + '. Results come only from the figures entered above.')];
    try { await saveBlob(new Blob(['﻿' + lines.join('\r\n')], {type:'text/csv'}), 'OC_Vibe_impact_inputs.csv'); toast('Download ready.'); } catch (err) { dlError(err, 'Download'); }
  };
  function setStatus(t) { $('calcStatus').textContent = t; }
  let DB = null, U = null, canWrite = null, saving = false;
  async function names(ids) { try { return U ? await U.profiles(ids) : {}; } catch(_) { return {}; } }
  (async () => {
    const CL = (window.claude && typeof window.claude.use === 'function') ? window.claude : null;
    DB = CL ? await CL.use('db') : null; U = CL ? await CL.use('user') : null;
    if (!DB) { $('calcSave').hidden = true; setStatus('Saving is not available in this view. Use Download to send your figures to Visit Anaheim.'); return; }
    canWrite = U ? await U.can('data.write') : null;
    if (canWrite === false) { $('calcSave').hidden = true; setStatus('You can try figures here. To save them for Visit Anaheim, ask for edit access, or use Download.'); }
    DB.doc('ocvibe/inputs').onSnapshot(async snap => {
      if (!snap.exists) { setStatus(canWrite === false ? $('calcStatus').textContent : 'No OC Vibe figures saved yet. Enter figures to see results.'); return; }
      const d = snap.data(); if (snap.metadata.hasPendingWrites) return;
      fill(d.values || BASE); form.elements.note.value = d.note || ''; render();
      const ps = d.by ? await names([d.by]) : {}; const who = (ps[d.by] && ps[d.by].name) || 'Someone';
      setStatus(`Showing figures saved by ${who} on ${d.at ? apDate(new Date(d.at)) : 'an earlier date'}.`);
    }, () => setStatus('Saved figures could not be loaded. You can still enter and download figures.'));
    DB.collection('ocvibe_history').orderBy('at','desc').limit(8).onSnapshot(async qs => {
      if (qs.empty) { $('calcHist').innerHTML = ''; return; }
      const ids = [...new Set(qs.docs.map(d => d.data().by).filter(Boolean))], ps = await names(ids);
      $('calcHist').innerHTML = `<h4>Save history</h4><ul class="calc-hl">${qs.docs.map(d => { const x = d.data(); return `<li><b>${esc(apDate(new Date(x.at)))}</b> · <span data-n></span>${x.note ? ' · ' + esc(x.note) : ''}</li>`; }).join('')}</ul>`;
      [...$('calcHist').querySelectorAll('[data-n]')].forEach((el,i) => { const by = qs.docs[i].data().by; el.textContent = (ps[by] && ps[by].name) || 'Someone'; });
    }, () => {});
  })();
  $('calcSave').onclick = async () => {
    if (!DB || saving) return; saving = true; $('calcSave').disabled = true;
    const rec = { values: read(), note: form.elements.note.value.slice(0, 300), at: new Date().toISOString(), by: U ? await U.id() : null };
    try { await DB.doc('ocvibe/inputs').set(rec); await DB.collection('ocvibe_history').add(rec); setStatus('Saved. Visit Anaheim BI can now see these figures.'); toast('Figures saved.'); }
    catch (e) { if (e && e.code === 'invalid_argument') { $('calcSave').hidden = true; setStatus('Your access level cannot save figures here. Use Download and send the file to Visit Anaheim BI.'); } else setStatus('The figures could not be saved. Try again, or use Download.'); }
    finally { saving = false; $('calcSave').disabled = false; }
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
  const io2 = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io2.unobserve(e.target); } }), {rootMargin:'0px 0px -6% 0px'});
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
