/* ---------- OC Vibe staff inputs: live impact calculator (saved to the artifact's shared db when allowed) ---------- */
(function initCalc(){
  const host = $('ocvCalc'); if (!host) return;
  const MD = MODEL, F = [
    ['hall_events','Concert hall events a year','', 1, MD.base.hall_events],
    ['hall_fill','Concert hall seats filled','%', 1, MD.base.hall_fill],
    ['small_events','Theater and club events a year','', 1, MD.base.small_events],
    ['small_fill','Theater and club seats filled','%', 1, MD.base.small_fill],
    ['other_att','Other new attendance a year (market hall, plazas, festivals)','', 1000, 0],
    ['net_new','Attendees who are net-new visitors to Anaheim','%', 1, MD.base.net_new],
    ['add_day','Anaheim visitors who add a day because of OC Vibe','%', 0.1, MD.base.add_day],
    ['rooms','Hotel rooms open','', 10, MD.base.rooms],
    ['occ','Hotel occupancy','%', 1, MD.base.occ],
    ['adr','Hotel average nightly rate','$', 1, MD.base.adr],
  ];
  const BASE = Object.fromEntries(F.map(f => [f[0], f[4]]));
  const fmtM = v => '$' + (v/1e6).toFixed(1) + 'M', fmtN = v => Math.round(v).toLocaleString('en-US');
  function calc(x) {
    const attend = MD.hall_cap*x.hall_events*x.hall_fill/100 + MD.small_cap*x.small_events*x.small_fill/100 + (+x.other_att||0);
    const nv = attend*x.net_new/100, days = MD.visitors*x.add_day/100;
    const spend = nv*MD.pv + days*MD.per_day, rn = x.rooms*365*x.occ/100, rev = rn*x.adr;
    return [
      ['Attendance a year', fmtN(attend)], ['Net-new visitors', fmtN(nv)], ['Extra visitor days', fmtN(days)],
      ['New visitor spending', fmtM(spend)], ['Anaheim total economic impact', fmtM(spend*MD.mult_ana)], ['Anaheim jobs supported', fmtN(spend/1e6*MD.jobs_ana)],
      ['Anaheim state and local taxes', fmtM(spend*MD.tax_ana)], ['Orange County total economic impact', fmtM(spend*MD.mult_oc)],
      ['California: new out-of-state visitor spending', fmtM(spend*MD.out_of_state)], ['OC Vibe hotel room nights', fmtN(rn)],
      ['OC Vibe hotel room revenue', fmtM(rev)], ['Anaheim hotel tax (15%)', fmtM(rev*MD.tot)],
    ];
  }
  host.innerHTML = `<h3>Enter OC Vibe's own figures</h3>
    <p class="calc-sub">OC Vibe staff can replace Visit Anaheim's assumptions with their own plans. Results update as you type and are compared with the BI base case. Saved figures are shared with everyone who can open this page.</p>
    <div class="calc-grid"><form class="calc-in" id="calcForm" autocomplete="off">${F.map(([k,l,u,st]) => `<label class="calc-f"><span>${esc(l)}</span><span class="calc-w">${u==='$'?'<i>$</i>':''}<input type="number" inputmode="decimal" min="0" step="${st}" name="${k}" id="cin-${k}">${u==='%'?'<i>%</i>':''}</span></label>`).join('')}
      <label class="calc-f calc-note"><span>Where these figures come from (optional)</span><input type="text" maxlength="300" name="note" id="cin-note" placeholder="For example: 2027 booking plan, Oct. 2026"></label>
      <div class="calc-acts"><button type="button" class="ctl accent" id="calcSave">Save for Visit Anaheim</button><button type="button" class="ctl" id="calcReset">Reset to BI base case</button><button type="button" class="ctl" id="calcDl">Download (.csv)</button></div>
      <p class="calc-status" id="calcStatus" aria-live="polite"></p></form>
      <div class="calc-out"><div class="scroll" tabindex="0" aria-label="Calculated impact"><table><thead><tr><th scope="col">Measure</th><th scope="col" class="n">OC Vibe figures</th><th scope="col" class="n">BI base case</th></tr></thead><tbody id="calcBody"></tbody></table></div>
      <p class="src">Method and ratios as in the scenario table above (Tourism Economics 2025 ratios; 2025 dollars; visitors only). Estimates, not forecasts.</p>
      <div id="calcHist"></div></div></div>`;
  const form = $('calcForm'), baseOut = calc(BASE);
  const read = () => Object.fromEntries(F.map(([k]) => [k, Math.max(0, parseFloat(form.elements[k].value) || 0)]));
  const fill = v => F.forEach(([k]) => form.elements[k].value = v[k] ?? BASE[k]);
  function render() { const o = calc(read()); $('calcBody').innerHTML = o.map(([l,v],i) => `<tr class="${i===3?'hirow':''}"><th scope="row">${esc(l)}</th><td class="n">${esc(v)}</td><td class="n">${esc(baseOut[i][1])}</td></tr>`).join(''); }
  fill(BASE); render();
  form.addEventListener('input', render);
  $('calcReset').onclick = () => { fill(BASE); form.elements.note.value = ''; render(); setStatus('Reset to the BI base case. Nothing is saved until you choose Save.'); };
  $('calcDl').onclick = async () => {
    const v = read(), o = calc(v), q = s => '"' + String(s).replace(/"/g,'""') + '"';
    const lines = ['"OC Vibe impact: figures entered by OC Vibe staff"', '"Input","Value"', ...F.map(([k,l,u]) => [q(l + (u ? ' ('+u+')' : '')), q(v[k])].join(',')), [q('Note'), q(form.elements.note.value)].join(','), '', '"Measure","OC Vibe figures","BI base case"', ...o.map(([l,x],i) => [q(l), q(x), q(baseOut[i][1])].join(',')), '', q('Prepared with the Visit Anaheim BI OC Vibe impact method, ' + apDate(new Date()) + '. Estimates, not forecasts.')];
    try { await saveBlob(new Blob(['﻿' + lines.join('\r\n')], {type:'text/csv'}), 'OC_Vibe_impact_inputs.csv'); toast('Download ready.'); } catch (err) { dlError(err, 'Download'); }
  };
  function setStatus(t) { $('calcStatus').textContent = t; }
  let DB = null, U = null, canWrite = null, saving = false;
  async function names(ids) { try { return U ? await U.profiles(ids) : {}; } catch(_) { return {}; } }
  (async () => {
    DB = await claude.use('db'); U = await claude.use('user');
    if (!DB) { $('calcSave').hidden = true; setStatus('Saving is not available in this view. Use Download to send your figures to Visit Anaheim.'); return; }
    canWrite = U ? await U.can('data.write') : null;
    if (canWrite === false) { $('calcSave').hidden = true; setStatus('You can try figures here. To save them for Visit Anaheim, ask for edit access, or use Download.'); }
    DB.doc('ocvibe/inputs').onSnapshot(async snap => {
      if (!snap.exists) { setStatus(canWrite === false ? $('calcStatus').textContent : 'No OC Vibe figures saved yet. The BI base case is shown.'); return; }
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
