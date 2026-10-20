# Nego AI · Glass Console

Clickable Glass Console Final app for Nego AI (agent and team lead views).

- `public/` is the static site deployed on Vercel. `index.html` is the app.
- Add `?demo` to the URL, or press **D**, to play the 60-second demo run.
- `canvas/` holds the Claude Design canvas artboards; `P5.dc.html` is the app source.
- `video/` holds the HyperFrames source for the demo film.
- `python3 build.py` rebuilds `public/index.html` from `canvas/P5.dc.html` (needs `npm i`).
