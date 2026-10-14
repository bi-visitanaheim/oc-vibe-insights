/* Map renderer shared by the page (inlined) and the deck PNG renderer (Node). Oct. 13, 2026.
   GEO: maps_geo.json; m: a map spec from maps.py. Returns an SVG string; colors come from CSS classes (mp-*) so the
   page follows light and dark themes, with light defaults inlined for standalone rendering. */
function mapSvg(GEO, m) {
  const g = m.kind === 'world' ? GEO.world : GEO.us, key = m.kind === 'world' ? 'world' : 'us';
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmt = p => m.unit === 'money' ? '$' + (p.v >= 1 ? p.v.toFixed(1) + 'M' : Math.round(p.v * 1000) + 'K') : p.t;
  const sv = {}; (m.states || []).forEach(s => sv[s.name] = s);
  const bin = v => { for (let i = 0; i < (m.bins || []).length; i++) if (v >= m.bins[i][0]) return i; return (m.bins || []).length - 1; };
  const shapes = (g.states || g.countries).map(s => {
    const d = sv[s.name];
    return d ? `<path class="mp-st b${bin(d.v)}" d="${s.d}" data-tip="${esc(s.name)}: ${esc(d.t)}" tabindex="0"><title>${esc(s.name)}: ${esc(d.t)}</title></path>`
             : `<path class="mp-land" d="${s.d}"/>`;
  }).join('');
  const pts = (m.points || []).filter(p => GEO.pts[p.name] && GEO.pts[p.name][key]).sort((a, b) => b.v - a.v);
  const max = Math.max(...pts.map(p => p.v), 1e-9), R = m.kind === 'world' ? 30 : 34;
  const rad = v => Math.max(3.2, Math.sqrt(v / max) * R);
  const circles = pts.map((p, i) => { const [x, y] = GEO.pts[p.name][key];
    return `<circle class="mp-b" style="--i:${i}" cx="${x}" cy="${y}" r="${rad(p.v).toFixed(1)}" data-tip="${esc(p.name)}: ${esc(p.t)}" tabindex="0"><title>${esc(p.name)}: ${esc(p.t)}</title></circle>`; }).join('');
  const placed = [], labels = [];
  if (m.home && GEO.pts[m.home] && GEO.pts[m.home][key]) { const [hx, hy] = GEO.pts[m.home][key]; placed.push([hx - 70, hy + 6, hx - 6, hy + 24]); }
  const hit = (b) => placed.some(q => b[0] < q[2] && b[2] > q[0] && b[1] < q[3] && b[3] > q[1]);
  pts.forEach((p, i) => { const [x, y] = GEO.pts[p.name][key], r = rad(p.v);
    if (i > 6) return;
    const short = p.name.split('–')[0].replace(' (mainland)', ''), w = (short.length + fmt(p).length + 1) * 7.4 + 6;
    const tries = [[x + r + 4, y + 4, 'start'], [x - r - 4, y + 4, 'end'], [x - w / 2, y - r - 6, 'start'], [x - w / 2, y + r + 15, 'start']];
    const ok = tries.map(([lx, ly, an]) => { const x0 = an === 'end' ? lx - w : lx; return [lx, ly, an, [x0, ly - 13, x0 + w, ly + 4]]; })
      .find(t => t[3][0] >= 2 && t[3][2] <= g.w - 2 && t[3][1] >= 2 && t[3][3] <= g.h - 2 && !hit(t[3]));
    if (!ok) return;
    const [lx, ly, anchor, box] = ok; placed.push(box); const y_ = ly - 4;
    labels.push(`<text class="mp-lb" x="${lx.toFixed(1)}" y="${(y_ + 4).toFixed(1)}" text-anchor="${anchor}">${esc(short)} <tspan class="mp-lv">${esc(fmt(p))}</tspan></text>`); });
  let home = '';
  if (m.home && GEO.pts[m.home] && GEO.pts[m.home][key]) { const [x, y] = GEO.pts[m.home][key];
    home = `<g class="mp-home"><path d="M${x} ${y - 7}L${x + 7} ${y}L${x} ${y + 7}L${x - 7} ${y}Z"/><text x="${x - 10}" y="${y + 20}" text-anchor="end">Anaheim</text></g>`; }
  const label = m.title + ': ' + pts.slice(0, 8).map(p => p.name + ' ' + fmt(p)).join(', ') + ((m.states || []).length ? '; states: ' + m.states.map(s => s.name + ' ' + s.t).join(', ') : '');
  return `<svg class="mp-svg" viewBox="0 0 ${g.w} ${g.h}" role="img" aria-label="${esc(label)}" xmlns="http://www.w3.org/2000/svg">
<style>.mp-land{fill:var(--mp-land,#E9EBE4);stroke:var(--mp-line,#FFFFFF);stroke-width:.7}.mp-st{stroke:var(--mp-line,#FFFFFF);stroke-width:.7}.mp-st.b0{fill:var(--mp-b0,#125C60)}.mp-st.b1{fill:var(--mp-b1,#43A3A3)}.mp-st.b2{fill:var(--mp-b2,#B4D9E3)}
.mp-b{fill:#43A3A3;fill-opacity:.62;stroke:#125C60;stroke-width:1.2}.mp-lb{font:700 13px "Sharp Sans Disp No2","Proxima Nova",system-ui,sans-serif;fill:var(--mp-ink,#231F20);paint-order:stroke;stroke:var(--mp-halo,#FFFFFF);stroke-width:3.5px}
.mp-lv{font-weight:900;fill:var(--mp-val,#125C60)}.mp-home path{fill:#A10009;stroke:#FFFFFF;stroke-width:1.5}.mp-home text{font:800 12px system-ui,sans-serif;fill:#A10009;paint-order:stroke;stroke:var(--mp-halo,#FFFFFF);stroke-width:3px}</style>
<g>${shapes}</g><g>${circles}</g><g>${home}</g><g>${labels.join('')}</g></svg>`;
}
function mapLegend(m) {
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmt = p => m.unit === 'money' ? '$' + (p.v >= 1 ? p.v.toFixed(1) + 'M' : Math.round(p.v * 1000) + 'K') : p.t;
  const top = [...(m.points || [])].sort((a, b) => b.v - a.v).slice(0, 8);
  const bins = (m.bins || []).map((b, i) => `<li><span class="sw b${i}"></span>${esc(b[1])}</li>`).join('') + (m.bins ? `<li><span class="sw land"></span>${esc(m.other)}</li>` : '');
  return `<div class="mp-key">${m.bins ? `<p class="mp-kh">States</p><ul class="mp-bins">${bins}</ul>` : ''}<p class="mp-kh">${m.kind === 'world' ? 'Countries' : 'Metro areas'} (circles)</p>
<ol class="mp-top">${top.map(p => `<li><b>${esc(fmt(p))}</b> ${esc(p.name)}</li>`).join('')}</ol><p class="mp-note"><span class="mp-hk" aria-hidden="true"></span> Anaheim</p></div>`;
}
if (typeof module !== 'undefined') module.exports = { mapSvg, mapLegend };
