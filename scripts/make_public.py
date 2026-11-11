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
# Overview motion clip as a GIF (Nov. 11, 2026): rebuilt from assets/ocv_motion.mp4 whenever the MP4 is newer,
# so replacing the MP4 at a data refresh also refreshes the Download GIF button. Falls back to the stored GIF.
import subprocess
A = os.path.join(P, "assets"); mp4, gif = os.path.join(A, "ocv_motion.mp4"), os.path.join(A, "ocv_motion.gif")
if shutil.which("ffmpeg") and (not os.path.exists(gif) or os.path.getmtime(mp4) > os.path.getmtime(gif)):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vf",
        "split[a][b];[a]palettegen=max_colors=256:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
        "-loop", "0", gif], check=True)
    print("assets/ocv_motion.gif rebuilt from ocv_motion.mp4")
elif os.path.getmtime(mp4) > os.path.getmtime(gif):
    print("WARNING: ocv_motion.mp4 is newer than ocv_motion.gif and ffmpeg is not installed; the Download GIF button is out of date")
shutil.copyfile(gif, os.path.join(OUT, "ocv_motion.gif"))
print("public/index.html, public/OC_Vibe_Insights.pptx and public/OC_Vibe_Insights.pdf written")
