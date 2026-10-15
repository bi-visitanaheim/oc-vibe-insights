"""Prepare files for the claude.ai artifact (Oct. 14, 2026). Artifacts serve PDF and CSV directly but not Office or zip files,
so those are written as <name>.json ({"b64", "type"}) for the page's Download button (downloads capability).
Writes build_artifact/ and prints the Artifact `files` maps, split into publishes under 55 MB."""
import base64, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline'))
import library as L
OUT = os.path.join(ROOT, 'build_artifact'); os.makedirs(OUT, exist_ok=True)
CT = {'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'zip': 'application/zip'}
items = []
for f in L.FILES:
    src = os.path.join(ROOT, 'pipeline', f['file']) if f['topic'] == 'report' else os.path.join(ROOT, 'public', 'library', f['file'])
    pub = f['file'] if f['topic'] == 'report' else 'library/' + f['file']
    ext = f['file'].rsplit('.', 1)[1]
    if ext in CT:
        out = os.path.join(OUT, f['file'] + '.json')
        json.dump({'b64': base64.b64encode(open(src, 'rb').read()).decode(), 'type': CT[ext]}, open(out, 'w'))
        items.append((pub + '.json', out))
    else:
        items.append((pub, src))
items.sort(key=lambda x: -os.path.getsize(x[1]))
batches, cur, size = [], {}, 9e6   # first batch also carries the page (~9 MB)
for pub, src in items:
    s = os.path.getsize(src)
    if size + s > 55e6: batches.append(cur); cur, size = {}, 0
    cur[pub] = os.path.relpath(src, ROOT); size += s
batches.append(cur)
for i, b in enumerate(batches):
    json.dump(b, open(os.path.join(OUT, f'batch{i}.json'), 'w'))
    print(i, len(b), round(sum(os.path.getsize(os.path.join(ROOT, v)) for v in b.values()) / 1e6, 1), 'MB')
