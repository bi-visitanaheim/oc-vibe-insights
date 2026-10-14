/* PDF export (Oct. 14, 2026): build a PDF holding only the chosen sections from the full OC Vibe Insights deck PDF,
   the same cut as the PowerPoint export. Works in the browser (window.PDFLib) and in Node (require('pdf-lib')).
   The title page is always kept. Pages are renumbered "n of N" over the deck's slide number so the cut reads in order. */
async function pdfSubset(PDFLib, data, keepNames, MAP) {
  const keep = new Set(keepNames);
  const pages = [0];
  MAP.sections.forEach(s => { if (keep.has(s.name)) s.pages.forEach(p => { if (!pages.includes(p)) pages.push(p); }); });
  pages.sort((a, b) => a - b);
  const src = await PDFLib.PDFDocument.load(data);
  const out = await PDFLib.PDFDocument.create();
  out.setTitle('OC Vibe Insights: ' + keepNames.join(', '));
  out.setAuthor('Visit Anaheim Business Intelligence'); out.setCreator('OC Vibe Insights'); out.setProducer('Visit Anaheim BI');
  const copied = await out.copyPages(src, pages);
  const font = await out.embedFont(PDFLib.StandardFonts.Helvetica);
  const ink = PDFLib.rgb(0x23 / 255, 0x1F / 255, 0x20 / 255), white = PDFLib.rgb(1, 1, 1), N = pages.length;
  copied.forEach((pg, i) => {
    out.addPage(pg);
    if (!MAP.numbered[pages[i]]) return;
    const { width, height } = pg.getSize(), b = MAP.num_box;
    const right = width * b.right, bottom = height * b.bottom, h = height * b.h, w = width * b.w;
    pg.drawRectangle({ x: right - w, y: bottom - 1, width: w + 2, height: h + 2, color: white });
    const label = `${i + 1} of ${N}`, size = 9 * width / 960;
    pg.drawText(label, { x: right - font.widthOfTextAtSize(label, size), y: bottom + h - size - 2, size, font, color: ink });
  });
  const bytes = await out.save();
  return typeof window === 'undefined' ? bytes : new Blob([bytes], { type: 'application/pdf' });
}
if (typeof module !== 'undefined') module.exports = { pdfSubset };
