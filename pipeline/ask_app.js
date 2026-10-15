/* Questions answered and Reports and data library (Oct. 14, 2026).
   Runs after app.js and reuses its helpers ($, esc, emph, chartHtml, saveBlob, toast, dlError, goPage, PAGES). */
(function () {
  const AQ = DATA.ask, LB = DATA.lib;
  const FILES = Object.fromEntries(LB.files.map(f => [f.id, f]));
  const QS = Object.fromEntries(AQ.items.map(q => [q.id, q]));
  const SEC_T = Object.fromEntries([['p-summary', 'Overview'], ['p-ask', 'Questions answered'], ['p-library', 'Reports and data library'], ['p-notes', 'Sources'], ...S.map(s => [s.id, s.tab])]);
  const fileHref = f => f.topic === 'report' ? f.file : 'library/' + f.file;
  const mb = b => b == null ? '' : b >= 1e6 ? (b / 1e6).toFixed(1) + ' MB' : Math.max(1, Math.round(b / 1e3)) + ' KB';
  const go = (id, target) => { const i = PAGES.indexOf(id); if (i >= 0) goPage(i, target); };

  /* ---------- visuals ---------- */
  function vizHtml(v) {
    if (!v) return '';
    if (v.kind === 'stack') {
      const cats = [...new Set(v.rows.flatMap(r => r.parts.map(p => p[0])))];
      const ci = c => cats.indexOf(c) % 5;
      const rows = v.rows.map(r => `<div class="row"><span class="l" style="font-size:13px;font-weight:700">${esc(r.l)}</span><div class="bar" role="img" aria-label="${esc(r.l)}: ${esc(r.parts.map(p => p[0] + ' ' + p[1] + '%').join(', '))}">${r.parts.map(p => `<span class="seg c${ci(p[0])}" style="width:${p[1]}%" data-tip="${esc(r.l)}, ${esc(p[0])}: ${p[1]}%" tabindex="0">${p[1] >= 9 ? p[1] + '%' : ''}</span>`).join('')}</div></div>`).join('');
      const key = `<div class="key">${cats.map(c => `<span><i class="seg c${ci(c)}" style="display:inline-block"></i>${esc(c)}</span>`).join('')}</div>`;
      const id = G2Q.push({ kind: 'stack', title: v.title, rows: v.rows }) - 1;
      return `<figure class="chartf" role="img" aria-label="${esc(v.title + ': ' + v.rows.map(r => r.l + ' ' + r.parts.map(p => p[0] + ' ' + p[1] + '%').join(', ')).join('; '))}"><h3>${esc(v.title)}</h3><div class="g2c" data-g2="${id}" style="--g2h:${v.rows.length * 56 + 70}px"><div class="stackv">${rows}${key}</div></div></figure>`;
    }
    return chartHtml({ kind: 'bars', title: v.title, sub: '', unit: v.unit || '', rows: v.rows.map(r => ({ l: r.l, v: r.v, t: r.t, hi: !!r.hi })), src: '' }).replace(/<p class="src">Source: <\/p>/, '');
  }

  /* ---------- Questions answered ---------- */
  const fileBtns = ids => ids.map(id => FILES[id]).filter(Boolean).map(f => ['PDF', 'CSV'].includes(f.ext)
    ? `<a class="fbtn" href="${esc(fileHref(f))}" target="_blank" rel="noopener" title="${esc(f.publisher)} · ${esc(f.period)}">${esc(f.title)} <span aria-hidden="true">↗</span></a>`
    : `<button type="button" class="fbtn" data-lib-go="${f.id}" title="${esc(f.publisher)} · ${esc(f.period)}">${esc(f.title)} (${esc(f.ext)})</button>`).join('');
  const linkBtns = idx => (idx || []).map(i => LB.links[i]).filter(Boolean).map(l =>
    `<a class="fbtn" href="${esc(l[1])}" target="_blank" rel="noopener">${esc(l[0].split(':')[0])} <span aria-hidden="true">↗</span></a>`).join('');
  function itemHtml(q) {
    const geo = `<table class="ask-geo"><thead><tr><th scope="col">Geography</th><th scope="col">Value</th><th scope="col">Detail and source</th></tr></thead><tbody>${q.geo.map(g =>
      `<tr><th scope="row">${esc(g[0])}</th><td class="v">${esc(g[1])}</td><td>${emph(g[2])}<span class="s">Source: ${esc(g[3])}</span></td></tr>`).join('')}</tbody></table>`;
    return `<details class="ask-item" id="q-${q.id}" data-topic="${esc(q.topic)}">
      <summary><span><span class="ask-q">${esc(q.q)}</span><span class="ask-a t8x" data-t8="${esc(q.a)}">${emph(q.a)}</span></span>
        <span class="ask-v"><b>${esc(q.key)}</b><small>${esc(q.key_l)}</small></span><span class="ask-tog" aria-hidden="true">›</span></summary>
      <div class="ask-body">
        <div class="ask-grid"><div class="ask-geo-w" tabindex="0" aria-label="Figures by geography">${geo}</div><div>${vizHtml(q.viz)}</div></div>
        <div class="ask-notes"><div class="ask-note"><h4>How it is calculated</h4>${emph(q.how)}</div>${q.caveat ? `<div class="ask-note"><h4>Keep in mind</h4>${emph(q.caveat)}</div>` : ''}</div>
        <div class="ask-files">${q.files.length ? `<span class="lbl">Read the files</span>${fileBtns(q.files)}` : ''}${(q.links || []).length ? `<span class="lbl">Public sources</span>${linkBtns(q.links)}` : ''}
          <button type="button" class="fbtn go" data-ask-go="${esc(q.go)}">Go deeper: ${esc(SEC_T[q.go] || 'section')} <span aria-hidden="true">→</span></button></div>
      </div></details>`;
  }
  $('askCoreGrid').innerHTML = AQ.core.map(id => QS[id]).map(q =>
    `<button type="button" class="ask-k" data-ask-open="${q.id}"><span class="kk">${esc(q.topic)}</span><b class="kv">${esc(q.key)}</b><span class="kl">${esc(q.key_l)}</span><span class="kq">${esc(q.q)}</span></button>`).join('');
  $('askList').innerHTML = AQ.order.map(t => {
    const items = AQ.items.filter(q => q.topic === t);
    return items.length ? `<div class="ask-group" data-topic="${esc(t)}"><h4 class="ask-topic">${esc(t)}</h4><div class="ask-list">${items.map(itemHtml).join('')}</div></div>` : '';
  }).join('');
  let askTopic = '';
  $('askTopics').innerHTML = ['All', ...AQ.order].map(t => `<button type="button" class="chip" data-t="${t === 'All' ? '' : esc(t)}" aria-pressed="${t === 'All'}">${esc(t)}</button>`).join('');
  function askFilter() {
    const term = $('askQ').value.trim().toLowerCase(); let n = 0;
    document.querySelectorAll('#askList details.ask-item').forEach(d => {
      const q = QS[d.id.slice(2)], hay = (q.q + ' ' + q.a + ' ' + q.topic + ' ' + q.geo.map(g => g.join(' ')).join(' ')).toLowerCase();
      const ok = (!askTopic || q.topic === askTopic) && (!term || term.split(/\s+/).every(w => hay.includes(w)));
      d.hidden = !ok; if (ok) n++; if (ok && term) d.open = true;
    });
    document.querySelectorAll('#askList .ask-group').forEach(g => g.hidden = ![...g.querySelectorAll('details')].some(d => !d.hidden));
    $('askCount').textContent = `${n} question${n === 1 ? '' : 's'} shown`;
  }
  $('askQ').addEventListener('input', askFilter);
  $('askTopics').addEventListener('click', e => { const b = e.target.closest('.chip'); if (!b) return; askTopic = b.dataset.t;
    $('askTopics').querySelectorAll('.chip').forEach(c => c.setAttribute('aria-pressed', c === b)); askFilter(); });

  /* ---------- Reports and data library ---------- */
  const extCls = e => e === 'PDF' ? '' : e === 'CSV' ? ' c' : e === 'ZIP' ? ' z' : ' x';
  const hosted = LB.files.filter(f => f.topic !== 'report');
  const totalB = LB.files.reduce((a, f) => a + (f.bytes || 0), 0);
  $('libBadge').textContent = `${LB.files.length} files · ${(totalB / 1e6).toFixed(0)} MB · as of ${LB.asof}`;
  const pubs = new Set(hosted.map(f => f.publisher.split(' for ')[0].split(' (')[0].split(' via ')[0]));
  $('libSum').innerHTML = [
    [String(hosted.length), 'source files', 'Reports and data as received from each publisher'],
    [String(LB.files.filter(f => f.kind === 'Report' || f.kind === 'Study').length), 'reports and studies', 'Tourism Economics, LARC, CoStar and Visit Anaheim'],
    [String(AQ.items.length), 'questions answered', 'Each question links to the files that answer it']
  ].map(([v, l, d]) => `<article class="dcard"><span class="dk">Library</span><b class="dfig">${v}</b><span class="dfl">${l}</span><p>${esc(d)}</p></article>`).join('');
  function fileHtml(f) {
    const qs = (f.answers || []).map(id => QS[id]).filter(Boolean);
    const secs = (f.used_in || []).filter(id => SEC_T[id]);
    return `<article class="lib-file" id="f-${f.id}" data-topic="${f.topic}">
      <span class="ext${extCls(f.ext)}">${esc(f.ext)}</span>
      <div><h4>${esc(f.title)}</h4>
        <div class="meta">${esc(f.publisher)} · ${esc(f.kind)} · Covers ${esc(f.period)} · Published ${esc(f.published)}${f.pages ? ` · ${f.pages} page${f.pages > 1 ? 's' : ''}` : ''}${f.bytes ? ` · ${mb(f.bytes)}` : ''}</div>
        <p>${emph(f.summary)}</p>${f.note ? `<p class="note">${esc(f.note)}</p>` : ''}
        <details class="lib-more"><summary>${[qs.length ? `Answers ${qs.length} question${qs.length > 1 ? 's' : ''}` : '', `used in ${secs.length} section${secs.length > 1 ? 's' : ''}`, 'geography'].filter(Boolean).join(' · ')}</summary>
        ${qs.length ? `<div class="tags"><b>Answers</b>${qs.map(q => `<button type="button" class="tag ltag" data-ask-open="${q.id}">${esc(q.q)}</button>`).join('')}</div>` : ''}
        ${secs.length ? `<div class="tags"><b>Used in</b>${secs.map(id => `<button type="button" class="tag ltag" data-ask-go="${id}">${esc(SEC_T[id])}</button>`).join('')}</div>` : ''}
        <div class="tags"><b>Geography</b>${f.geo.map(g => `<span>${esc(g)}</span>`).join(' · ')}</div></details></div>
      <div class="acts">${['PDF', 'CSV'].includes(f.ext) ? `<a class="fbtn" href="${esc(fileHref(f))}" target="_blank" rel="noopener">Open <span aria-hidden="true">↗</span></a>` : ''}<button type="button" class="fbtn go" data-dl="${f.id}">Download</button></div>
    </article>`;
  }
  $('libFiles').innerHTML = LB.topics.map(([k, t, d]) => {
    const fs = LB.files.filter(f => f.topic === k);
    return fs.length ? `<section class="lib-group" data-topic="${k}"><h3>${esc(t)} <span class="badge">${fs.length}</span></h3><p>${esc(d)}</p><div class="lib-list">${fs.map(fileHtml).join('')}</div></section>` : '';
  }).join('') + `<div class="lib-empty" id="libEmpty" hidden>No files match. Clear the search or choose another topic.</div>`;
  $('libLinkList').innerHTML = LB.links.map(([t, u, d]) => `<li><a href="${esc(u)}" target="_blank" rel="noopener">${esc(t)} <span aria-hidden="true" style="display:inline">↗</span></a><span>${esc(d)}</span></li>`).join('');
  let libTopic = '';
  $('libTopics').innerHTML = [['', 'All'], ...LB.topics.map(([k, t]) => [k, t.split(' (')[0]])].map(([k, t]) => `<button type="button" class="chip" data-t="${k}" aria-pressed="${!k}">${esc(t)}</button>`).join('');
  function libFilter() {
    const term = $('libQ').value.trim().toLowerCase(); let n = 0;
    document.querySelectorAll('#libFiles .lib-file').forEach(el => {
      const f = FILES[el.id.slice(2)], hay = [f.title, f.publisher, f.summary, f.period, f.published, f.kind, f.ext, f.geo.join(' '), f.note, (f.answers || []).map(id => QS[id] ? QS[id].q : '').join(' ')].join(' ').toLowerCase();
      const ok = (!libTopic || f.topic === libTopic) && (!term || term.split(/\s+/).every(w => hay.includes(w)));
      el.hidden = !ok; if (ok) n++;
    });
    document.querySelectorAll('#libFiles .lib-group').forEach(g => g.hidden = ![...g.querySelectorAll('.lib-file')].some(e => !e.hidden));
    $('libEmpty').hidden = n > 0; $('libCount').textContent = `${n} file${n === 1 ? '' : 's'} shown`;
  }
  $('libQ').addEventListener('input', libFilter);
  $('libTopics').addEventListener('click', e => { const b = e.target.closest('.chip'); if (!b) return; libTopic = b.dataset.t;
    $('libTopics').querySelectorAll('.chip').forEach(c => c.setAttribute('aria-pressed', c === b)); libFilter(); });

  /* ---------- shared actions ---------- */
  document.addEventListener('click', async e => {
    const o = e.target.closest('[data-ask-open]'), g = e.target.closest('[data-ask-go]'), d = e.target.closest('[data-dl]');
    if (o) { const det = $('q-' + o.dataset.askOpen); if (det) { det.hidden = false; det.open = true; } go('p-ask', 'q-' + o.dataset.askOpen); }
    else if (g) go(g.dataset.askGo);
    else if (e.target.closest('[data-lib-go]')) { const id = e.target.closest('[data-lib-go]').dataset.libGo; go('p-library', 'f-' + id); }
    else if (d) {
      const f = FILES[d.dataset.dl]; d.disabled = true;
      try {
        let blob;
        if (f.id === 'ocv-deck') blob = b64Blob(ATTACH.deck, 'application/vnd.openxmlformats-officedocument.presentationml.presentation');
        else if (f.id === 'ocv-report') blob = b64Blob(ATTACH.pdf, 'application/pdf');
        else {
          let r = null; try { r = await fetch(fileHref(f)); } catch (_) { r = null; }
          if (r && r.ok && !/text\/html/.test(r.headers.get('content-type') || '')) blob = await r.blob();
          else {   // claude.ai artifact: Office and zip files are published as base64 JSON next to the page
            const j = await fetch(fileHref(f) + '.json'); if (!j.ok) throw new Error('fetch');
            const o = await j.json(); blob = b64Blob(o.b64, o.type);
          }
        }
        await saveBlob(blob, f.file); toast('Download ready.');
      } catch (err) { dlError(err, 'Download'); } finally { d.disabled = false; }
    }
  });
  /* deep links: #ask/<id> and #library/<id> */
  function deep() {
    const h = (location.hash || '').slice(1), [k, id] = h.split('/');
    if (k === 'ask' && id && QS[id]) { const det = $('q-' + id); det.open = true; go('p-ask', 'q-' + id); }
    else if (k === 'library' && id && FILES[id]) go('p-library', 'f-' + id);
  }
  window.addEventListener('hashchange', deep); deep();
  askFilter(); libFilter();
  /* floating "Next" pill: shows once the reader is into a section's data and hides when the Up next band is on screen */
  const pill = $('nextPill'); let bandVisible = false;
  const bandIo = new IntersectionObserver(es => { es.forEach(en => { if (en.target.closest('.page') === $(PAGES[CUR])) bandVisible = en.isIntersecting; }); syncPill(); });
  document.querySelectorAll('.upnext2').forEach(n => bandIo.observe(n));
  function syncPill() {
    const id = PAGES[CUR], sec = S.find(x => x.id === id), pg = $(id);
    if (!sec || !sec.next || !pg) { pill.hidden = true; return; }
    const top = pg.getBoundingClientRect().top, past = -top > Math.min(900, pg.offsetHeight * 0.25);
    pill.textContent = `Next: ${sec.next.tab} →`; pill.dataset.to = sec.next.id;
    pill.hidden = !(past && !bandVisible); if (!pill.hidden) $('toTop').style.bottom = '84px'; else $('toTop').style.bottom = '';
  }
  pill.onclick = () => go(pill.dataset.to);
  window.addEventListener('scroll', syncPill, { passive: true });
  document.addEventListener('click', () => setTimeout(syncPill, 60));
})();
