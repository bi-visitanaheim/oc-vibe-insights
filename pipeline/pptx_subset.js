/* PowerPoint export (Oct. 13, 2026): build a deck holding only the chosen sections from the full OC Vibe Insights deck.
   Works in the browser and in Node. Takes a JSZip class, the full .pptx bytes and the deck section names to keep.
   Removed slides take their notes and charts with them; section list, relationships, content types and slide counts are
   rewritten so PowerPoint opens the file without a repair prompt. The title slide is always kept. */
async function pptxSubset(JSZip, data, keepNames) {
  const keep = new Set(keepNames);
  const z = await JSZip.loadAsync(data);
  const rd = p => z.file(p) ? z.file(p).async('string') : Promise.resolve('');
  let pres = await rd('ppt/presentation.xml'), prels = await rd('ppt/_rels/presentation.xml.rels'), ct = await rd('[Content_Types].xml');
  const secs = [...pres.matchAll(/<p14:section name="([^"]*)"[^>]*>\s*<p14:sldIdLst>([\s\S]*?)<\/p14:sldIdLst>\s*<\/p14:section>/g)]
    .map(m => ({ name: m[1], whole: m[0], ids: [...m[2].matchAll(/id="(\d+)"/g)].map(x => x[1]) }));
  const keepIds = new Set();
  secs.forEach((s, i) => { if (keep.has(s.name)) s.ids.forEach(id => keepIds.add(id)); if (i === 0 && s.ids.length) keepIds.add(s.ids[0]); });
  const dropPart = path => {
    z.remove(path);
    const rel = path.replace(/([^/]+)$/, '_rels/$1.rels'); if (z.file(rel)) z.remove(rel);
    ct = ct.replace(new RegExp('<Override PartName="/' + path.replace(/[.[\]]/g, '\\$&') + '"[^>]*/>'), '');
  };
  for (const m of [...pres.matchAll(/<p:sldId id="(\d+)" r:id="(rId\d+)"\/>/g)]) {
    if (keepIds.has(m[1])) continue;
    pres = pres.replace(m[0], '');
    const rel = prels.match(new RegExp('<Relationship Id="' + m[2] + '"[^>]*/>'));
    if (!rel) continue;
    prels = prels.replace(rel[0], '');
    const target = 'ppt/' + rel[0].match(/Target="([^"]+)"/)[1];
    dropPart(target);
  }
  // remove parts nothing references any more (charts, embedded workbooks, media, notes), repeating until stable
  const resolve = (relsPath, t) => {
    if (t.startsWith('/')) return t.slice(1);
    const base = relsPath.replace(/_rels\/[^/]+\.rels$/, '').split('/').filter(Boolean);
    for (const seg of t.split('/')) { if (seg === '..') base.pop(); else if (seg !== '.') base.push(seg); }
    return base.join('/');
  };
  for (let pass = 0; pass < 4; pass++) {
    const refs = new Set();
    for (const f of Object.keys(z.files).filter(f => f.endsWith('.rels'))) {
      const x = await rd(f);
      for (const m of x.matchAll(/Target="([^"]+)"/g)) if (!/TargetMode="External"/.test(m[0])) refs.add(resolve(f, m[1]));
    }
    const orphans = Object.keys(z.files).filter(f => /^ppt\/(charts|embeddings|media|notesSlides)\/[^/]+$/.test(f) && !refs.has(f));
    if (!orphans.length) break;
    orphans.forEach(dropPart);
  }
  secs.forEach(s => {
    const ids = s.ids.filter(id => keepIds.has(id));
    pres = pres.replace(s.whole, ids.length ? s.whole.replace(/<p14:sldIdLst>[\s\S]*?<\/p14:sldIdLst>/, '<p14:sldIdLst>' + ids.map(id => `<p14:sldId id="${id}"/>`).join('') + '</p14:sldIdLst>') : '');
  });
  const n = keepIds.size;
  let app = await rd('docProps/app.xml');
  if (app) {
    const notes = Object.keys(z.files).filter(f => /^ppt\/notesSlides\/notesSlide\d+\.xml$/.test(f)).length;
    app = app.replace(/<Slides>\d+<\/Slides>/, `<Slides>${n}</Slides>`).replace(/<Notes>\d+<\/Notes>/, `<Notes>${notes}</Notes>`)
      .replace(/(<vt:lpstr>Slide Titles<\/vt:lpstr><\/vt:variant>\s*<vt:variant><vt:i4>)\d+(<\/vt:i4>)/, `$1${n}$2`)
      .replace(/<TitlesOfParts>\s*<vt:vector size="\d+" baseType="lpstr">([\s\S]*?)<\/vt:vector>/, (all, inner) => {
        const fixed = [...inner.matchAll(/<vt:lpstr>([^<]*)<\/vt:lpstr>/g)].map(x => x[1]).filter(x => !/^Slide \d+$/.test(x));
        const items = [...fixed, ...Array.from({ length: n }, (_, i) => 'Slide ' + (i + 1))];
        return `<TitlesOfParts>\n\t\t<vt:vector size="${items.length}" baseType="lpstr">${items.map(x => `<vt:lpstr>${x}</vt:lpstr>`).join('')}</vt:vector>`;
      });
    z.file('docProps/app.xml', app);
  }
  z.file('ppt/presentation.xml', pres); z.file('ppt/_rels/presentation.xml.rels', prels); z.file('[Content_Types].xml', ct);
  return z.generateAsync({ type: typeof window === 'undefined' ? 'nodebuffer' : 'blob', compression: 'DEFLATE',
    mimeType: 'application/vnd.openxmlformats-officedocument.presentationml.presentation' });
}
if (typeof module !== 'undefined') module.exports = { pptxSubset };
