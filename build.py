"""Build standalone flow pages from the canvas .dc.html artboards.

Usage: python3 build.py <folder with F*.dc.html>
"""
import re, sys, pathlib, shutil, html

SRC = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(__file__).parent / "public"

FLOWS = [
    ("F2", "practice-path", "2", "Practice Path"),
    ("F3", "call-floor", "3", "Call Floor"),
    ("F4", "glass-path", "4", "Glass Path"),
    ("F5", "glass-console", "5", "Glass Console"),
    ("F6", "collection-slip", "8", "Collection Slip"),
    ("F7", "game-show", "9", "Game Show"),
]

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Nego AI</title>
{helmet}
<style>
.dc-switch{{position:fixed;left:16px;bottom:16px;z-index:50;display:flex;gap:4px;padding:5px;border-radius:99px;background:rgba(15,18,20,.82);backdrop-filter:blur(12px);font:600 12px/1 system-ui,sans-serif}}
.dc-switch a{{color:#E8ECEA;text-decoration:none;padding:8px 12px;border-radius:99px}}
.dc-switch a:hover{{background:rgba(255,255,255,.12)}}
.dc-switch a[aria-current]{{background:#E8ECEA;color:#111}}
</style>
</head>
<body>
<div id="app"></div>
<template id="tpl">{body}</template>
<script id="logic" type="text/plain">{logic}</script>
<nav class="dc-switch" aria-label="Directions">{nav}</nav>
<script src="../vendor/morphdom-umd.min.js"></script>
<script src="../dc-runtime.js"></script>
<script>
if (window.self !== window.top) document.querySelector('.dc-switch').hidden = true;
DCRuntime.mount(document.getElementById('app'), document.getElementById('tpl'), document.getElementById('logic').textContent);
</script>
</body>
</html>
"""

def main():
    (OUT / "flows").mkdir(parents=True, exist_ok=True)
    (OUT / "vendor").mkdir(exist_ok=True)
    shutil.copy(pathlib.Path(__file__).parent / "node_modules/morphdom/dist/morphdom-umd.min.js", OUT / "vendor/")
    for fid, slug, num, name in FLOWS:
        s = (SRC / f"{fid}.dc.html").read_text()
        xdc = re.search(r"<x-dc>(.*)</x-dc>", s, re.S).group(1)
        helmet = re.search(r"<helmet>(.*?)</helmet>", xdc, re.S).group(1).strip()
        body = re.sub(r"<helmet>.*?</helmet>", "", xdc, flags=re.S).strip()
        logic = re.search(r"<script type=\"text/x-dc\"[^>]*>(.*?)</script>", s, re.S).group(1)
        nav = '<a href="../">All</a>' + "".join(
            f'<a href="{sl}.html"{" aria-current=\"page\"" if sl == slug else ""}>{n}</a>' for _, sl, n, _ in FLOWS)
        (OUT / "flows" / f"{slug}.html").write_text(
            PAGE.format(title=f"{num} {name}", helmet=helmet, body=body, logic=logic.replace("</script", "<\\/script"), nav=nav))
        print("built", slug)

main()
