"""Copy the built dashboard and deck into public/ for Vercel.

The pipeline writes pipeline/oc-vibe-insights.html as a page body (the claude.ai artifact adds the
document skeleton when it publishes). This script adds the skeleton so the same page works as a
standalone site, and copies the deck so it can be downloaded directly.
Run from the repository root:  python3 scripts/make_public.py
"""
import os, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P, OUT = os.path.join(ROOT, "pipeline"), os.path.join(ROOT, "public")
os.makedirs(OUT, exist_ok=True)
body = open(os.path.join(P, "oc-vibe-insights.html"), encoding="utf-8").read()
body = body.replace('<meta charset="utf-8">\n', "", 1)   # the head below declares it
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="robots" content="noindex, nofollow">\n</head>\n<body>\n')
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(head + body + "\n</body>\n</html>\n")
for f in ("OC_Vibe_Insights.pptx", "OC_Vibe_Insights.pdf", "OC_Vibe_Questions_Answered.pptx"):
    shutil.copyfile(os.path.join(P, f), os.path.join(OUT, f))
print("public/index.html, public/OC_Vibe_Insights.pptx and public/OC_Vibe_Insights.pdf written")
