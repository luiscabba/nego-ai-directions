"""Build the site (public/index.html) from the Glass Console Final artboard.

Usage: python3 build.py   (needs `npm i` once for morphdom)
"""
import re, pathlib, shutil
ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "public"
SRC = ROOT / "canvas" / "P5.dc.html"

def main():
    (OUT / "vendor").mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "node_modules/morphdom/dist/morphdom-umd.min.js", OUT / "vendor/")
    s = SRC.read_text()
    xdc = re.search(r"<x-dc>(.*)</x-dc>", s, re.S).group(1)
    helmet = re.search(r"<helmet>(.*?)</helmet>", xdc, re.S).group(1).strip()
    body = re.sub(r"<helmet>.*?</helmet>", "", xdc, flags=re.S).strip()
    logic = re.search(r'<script type="text/x-dc"[^>]*>(.*?)</script>', s, re.S).group(1)
    (OUT / "index.html").write_text(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nego AI</title>
{helmet}
</head>
<body>
<div id="app"></div>
<template id="tpl">{body}</template>
<script id="logic" type="text/plain">{logic.replace("</script", "<\\\\/script")}</script>
<script src="vendor/morphdom-umd.min.js"></script>
<script src="dc-runtime.js"></script>
<script>
window.__NEGO_SITE = true;
DCRuntime.mount(document.getElementById('app'), document.getElementById('tpl'), document.getElementById('logic').textContent);
</script>
</body>
</html>
""")
    print("built public/index.html")

main()
