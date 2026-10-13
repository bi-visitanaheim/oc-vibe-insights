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
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="robots" content="noindex, nofollow">\n</head>\n<body>\n')
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(head + body + "\n</body>\n</html>\n")
shutil.copyfile(os.path.join(P, "OC_Vibe_Insights.pptx"), os.path.join(OUT, "OC_Vibe_Insights.pptx"))
print("public/index.html and public/OC_Vibe_Insights.pptx written")
