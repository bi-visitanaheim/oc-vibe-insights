"""PDF export source (Oct. 14, 2026): render the full deck to PDF and map each deck section to its pages.

The dashboard's Export > PDF cuts this PDF to the chosen sections in the browser (pdf_subset.js with pdf-lib), the same
way Export > PowerPoint cuts the deck, so PDF pages carry the deck's layout and spacing. Requires LibreOffice (soffice)
and poppler (pdfinfo). Run after the deck is built: writes OC_Vibe_Insights.pdf and deck_pages.json."""
import json, os, re, subprocess, sys, zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
PPTX, PDF, OUT = (os.path.join(BASE, f) for f in ("OC_Vibe_Insights.pptx", "OC_Vibe_Insights.pdf", "deck_pages.json"))

z = zipfile.ZipFile(PPTX)
pres = z.read("ppt/presentation.xml").decode()
rels = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', z.read("ppt/_rels/presentation.xml.rels").decode()))
order = re.findall(r'<p:sldId id="(\d+)" r:id="(rId\d+)"/>', pres)
idx = {sid: i for i, (sid, _) in enumerate(order)}
sections = []
for name, body in re.findall(r'<p14:section name="([^"]*)"[^>]*>\s*<p14:sldIdLst>([\s\S]*?)</p14:sldIdLst>', pres):
    sections.append(dict(name=name, pages=sorted(idx[s] for s in re.findall(r'id="(\d+)"', body))))
numbered = []   # slides on the content master carry a slide number at lower right
for _, rid in order:
    srels = z.read("ppt/" + re.sub(r"slides/(slide\d+\.xml)", r"slides/_rels/\1.rels", rels[rid])).decode()
    lay = re.search(r'Target="\.\./slideLayouts/(slideLayout\d+\.xml)"', srels).group(1)
    lx = z.read("ppt/slideLayouts/" + lay).decode()
    numbered.append('type="sldNum"' in lx)

subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", BASE, PPTX], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
info = subprocess.run(["pdfinfo", PDF], capture_output=True, text=True, check=True).stdout
n_pdf = int(re.search(r"Pages:\s+(\d+)", info).group(1))
size = re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info)
covered = sorted(p for s in sections for p in s["pages"])
if n_pdf != len(order) or covered != list(range(len(order))):
    sys.exit(f"deck_pdf: {n_pdf} PDF pages for {len(order)} slides; section pages cover {len(covered)}")
json.dump(dict(n=n_pdf, w=float(size.group(1)), h=float(size.group(2)), sections=sections, numbered=numbered,
               num_box=dict(right=(13.333 - 0.6) / 13.333, bottom=(7.5 - 7.32) / 7.5, h=0.3 / 7.5, w=1.6 / 13.333)),
          open(OUT, "w"))
print(f"deck_pdf: {n_pdf} pages, {len(sections)} sections, {os.path.getsize(PDF) / 1e6:.1f} MB")
