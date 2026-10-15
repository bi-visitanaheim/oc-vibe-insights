"""Re-zip Office files with DEFLATE (the theme step can write them uncompressed); content and order unchanged."""
import sys, zipfile, os, shutil
for path in sys.argv[1:]:
    tmp = path + '.tmp'
    with zipfile.ZipFile(path) as src, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as dst:
        for info in src.infolist():
            if info.is_dir():
                continue
            zi = zipfile.ZipInfo(info.filename, info.date_time); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = info.external_attr
            dst.writestr(zi, src.read(info.filename))
    before = os.path.getsize(path); shutil.move(tmp, path); print(f'{path}: {before:,} -> {os.path.getsize(path):,} bytes')
