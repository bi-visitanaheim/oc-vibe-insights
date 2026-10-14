/* Render the report's maps to PNG for the deck (same renderer as the page). Run after export_deck.py. */
const { chromium } = require('playwright'); const fs = require('fs');
const { mapSvg } = require('./map_svg.js');
const GEO = JSON.parse(fs.readFileSync('maps_geo.json', 'utf8')), D = JSON.parse(fs.readFileSync('deck_data.json', 'utf8'));
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1.5 });
  for (const s of D.sections) for (const [i, m] of (s.maps || []).entries()) {
    const g = m.kind === 'world' ? GEO.world : GEO.us;
    await p.setContent(`<!doctype html><html><body style="margin:0;background:#FFFFFF"><div id="m" style="width:1600px;background:#F9F9F2">${mapSvg(GEO, m)}</div></body></html>`);
    const el = await p.$('#m'); await el.screenshot({ path: `map_${s.id}_${i}.png` }); console.log('map', s.id, i, g.w + 'x' + g.h);
  }
  await b.close();
})();
