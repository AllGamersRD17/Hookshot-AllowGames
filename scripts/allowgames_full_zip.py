"""(Allow Games) The whole Hookshot Builder in one zip, from a release's hookshot-setup.txt and its parts.

    python -I scripts/allowgames_full_zip.py <dist folder> <out zip>

The setup (HookshotBuilder.exe) downloads the parts a hookshot-setup.txt lists and unpacks them; this does the same here, once,
so the Allow Games Edition's release also has HookshotBuilder.zip: extract it, run HookshotBuilder\\HookshotBuilder.exe, as the
edition's readme says. A part made by this release is taken from the dist folder (it is not uploaded yet); the others (Python,
emsdk, CPM, wgpu-native, llvm-mingw) are downloaded from the URL in their line, and checked against its SHA-256. No game data.
"""
import hashlib
import io
import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile


def fetch(url, dist):
    local = os.path.join(dist, url.rsplit("/", 1)[-1])
    if os.path.isfile(local):
        with open(local, "rb") as f:
            return f.read()
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                return r.read()
        except Exception as e:   # (GitHub's download service now and then answers 5xx: tried again)
            print("  %s: %s, again" % (url, e), flush=True)
    sys.exit("could not download %s" % url)


def main():
    dist, out = sys.argv[1], os.path.abspath(sys.argv[2])
    with open(os.path.join(dist, "hookshot-setup.txt"), encoding="utf-8") as f:
        lines = f.read().splitlines()
    work = tempfile.mkdtemp()
    try:
        for line in lines:
            w = line.split()
            if not w or w[0] != "part":
                continue
            sha, size, dest, strip, rename, url = w[1], int(w[2]), w[3], w[4], w[5], w[6]
            data = fetch(url, dist)
            if len(data) != size or hashlib.sha256(data).hexdigest() != sha:
                sys.exit("%s: not the part the list names (size or SHA-256)" % url)
            print("%-60s %5d MB" % (url.rsplit("/", 1)[-1], size >> 20), flush=True)
            target = os.path.join(work, dest)
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for info in z.infolist():
                    name = info.filename
                    if strip != "-":   # (llvm-mingw's own top folder, named as the setup names it)
                        if not name.startswith(strip + "/"):
                            continue
                        name = (rename if rename != "-" else strip) + name[len(strip):]
                    path = os.path.join(target, *name.split("/"))
                    if info.is_dir():
                        os.makedirs(path, exist_ok=True)
                        continue
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with z.open(info) as src, open(path, "wb") as dst:
                        shutil.copyfileobj(src, dst)
        root = os.path.join(work, "HookshotBuilder")
        if not os.path.isfile(os.path.join(root, "HookshotBuilder.exe")):
            sys.exit("no HookshotBuilder\\HookshotBuilder.exe after the parts")
        bad = [n for d, _, fs in os.walk(root) for n in fs
               if n.lower().endswith((".nup", ".keys")) or n.lower() in ("hookshot.exe", "image.bin")]
        if bad:
            sys.exit("game files in the package: %s" % bad[:5])
        if os.path.exists(out):
            os.remove(out)
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for d, ds, fs in os.walk(root):
                ds.sort()
                for n in sorted(fs):
                    p = os.path.join(d, n)
                    z.write(p, os.path.relpath(p, work).replace(os.sep, "/"))
        print("%s: %d MB" % (out, os.path.getsize(out) >> 20))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
