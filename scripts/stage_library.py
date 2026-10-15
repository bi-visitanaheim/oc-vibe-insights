"""Copy the original source files into public/library under stable, readable names (Oct. 14, 2026).

Usage: python3 scripts/stage_library.py <folder with the original files>
Visit Anaheim-owned Office files get neutral document properties (no personal names); the TID workbook's
working-sheet names are made neutral. File contents are otherwise unchanged. The mapping lives in pipeline/library.py."""
import os, re, shutil, sys, zipfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
import library as L

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public', 'library')
os.makedirs(OUT, exist_ok=True)
SHEETS = {'for nancy': 'Summary figures', 'Cindy TE MATH': 'TE inputs check'}

def scrub(src, dst, rename_sheets=False, owner='Visit Anaheim Business Intelligence'):
    zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
    for it in zin.infolist():
        b = zin.read(it.filename)
        if it.filename == 'docProps/core.xml':
            t = b.decode('utf-8')
            t = re.sub(r'<dc:creator>[^<]*</dc:creator>', f'<dc:creator>{owner}</dc:creator>', t)
            t = re.sub(r'<cp:lastModifiedBy>[^<]*</cp:lastModifiedBy>', f'<cp:lastModifiedBy>{owner}</cp:lastModifiedBy>', t)
            b = t.encode('utf-8')
        elif it.filename == 'xl/workbook.xml':
            t = b.decode('utf-8')
            t = re.sub(r'<mc:AlternateContent[^>]*>\s*<mc:Choice Requires="x15">\s*<x15ac:absPath[^>]*/>\s*</mc:Choice>\s*</mc:AlternateContent>', '', t)
            t = re.sub(r'<x15ac:absPath[^>]*/>', '', t)
            if rename_sheets:
                for a, z in SHEETS.items():
                    t = t.replace(f'name="{a}"', f'name="{z}"').replace(f"'{a}'!", f"'{z}'!").replace(f'{a}!', f"'{z}'!")
            b = t.encode('utf-8')
        elif it.filename.startswith('ppt/changesInfos/') or it.filename.startswith('ppt/authors') or it.filename.startswith('ppt/commentAuthors'):
            b = re.sub(rb'name="[^"]*"', b'name="Visit Anaheim BI"', b)
        elif it.filename in ('xl/persons/person.xml',):
            b = re.sub(rb'displayName="[^"]*"', b'displayName="Visit Anaheim BI"', b)
        elif rename_sheets and it.filename.startswith('xl/') and it.filename.endswith('.xml'):
            t = b.decode('utf-8')
            for a, z in SHEETS.items():
                t = t.replace(f'name="{a}"', f'name="{z}"').replace(f"'{a}'!", f"'{z}'!").replace(f'{a}!', f"'{z}'!")
            b = t.encode('utf-8')
        elif it.filename == 'docProps/app.xml' and rename_sheets:
            t = b.decode('utf-8')
            for a, z in SHEETS.items(): t = t.replace(f'>{a}<', f'>{z}<')
            b = t.encode('utf-8')
        zout.writestr(it, b)
    zout.close()

for f in L.FILES:
    if not f.get('orig'): continue
    src, dst = os.path.join(SRC, f['orig']), os.path.join(OUT, f['file'])
    if f['file'].endswith(('.xlsx', '.pptx', '.docx')):   # Office files: neutral document properties and revision names
        own = 'Visit Anaheim Business Intelligence' if f['publisher'].startswith('Visit Anaheim') else ''
        scrub(src, dst, rename_sheets=f.get('rename_sheets', False), owner=own)
    elif f['file'].endswith('.pdf'):   # PDFs: content unchanged; author field set to the publishing organization
        import pikepdf
        org = 'Tourism Economics' if f['publisher'].startswith('Tourism Economics') else 'Lodging Analytics Research & Consulting (LARC)' if 'LARC' in f['publisher'] else None
        if org:
            with pikepdf.open(src) as pdf:
                pdf.docinfo['/Author'] = org
                with pdf.open_metadata(set_pikepdf_as_editor=False) as meta:
                    if 'dc:creator' in meta: meta['dc:creator'] = [org]
                pdf.save(dst)
        else:
            shutil.copy2(src, dst)
    else: shutil.copy2(src, dst)
    print(f"{f['file']:<52} {os.path.getsize(dst)/1e6:6.2f} MB")
