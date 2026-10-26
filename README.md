# XMD / Developer — pixel-accurate portfolio replica

A responsive, single-page recreation of the supplied desktop (`1536 × 1024`) portfolio artwork. The phone layout is a real full-screen web stage (`816 × 1766`, matching modern phone ratios): the fake device status bar, signal/Wi-Fi/battery icons, home indicator and device side margins have been removed, while every portfolio component stays unchanged.

## What is included

- `standalone.html` — fully self-contained version with all CSS, JavaScript, images, fonts and the CV embedded as data URIs. Open this file directly in the workspace viewer.
- `index.html` — source entry point with external CSS/JS/assets; semantic portfolio content, the fixed design stage, and the transparent interaction layer.
- `styles.css` — stage scaling, exact layer stacking, focus/hover states.
- `script.js` — desktop/mobile switching, exact canvas placement, and interactive hotspots.
- `wave.js` — the palette, 551-star data array, and renderer copied from your `Star Wave.html`.
- `assets/` — generated pixel-locked layers:
  - `bg-desktop.png`, `bg-mobile.png`, `bg-mobile-web.png` — low-frequency background fields.
  - `wave-glow-desktop.png`, `wave-glow-mobile.png`, `wave-glow-mobile-web.png` — exact blurred wave glow with stars removed.
  - `portrait-desktop.png`, `portrait-mobile.png` — your supplied portrait warped into the exact circle used by each design, with low-frequency colour matched to the reference.
  - `overlay-desktop.png`, `overlay-mobile.png`, `overlay-mobile-web.png` — transparent composites of the reference artwork. They contain precise cut-outs so the live wave canvas and supplied portrait remain visible. The `*-mobile-web.png` layers have all phone chrome removed.
  - `XMD-CV.pdf` — a placeholder CV for the Download CV button.
  - `favicon.svg` — XMD sparkle.
- `generate_assets.py` — rebuilds every generated asset from the four uploaded source files, then calls the mobile-web stage builder.
- `make_mobile_web_assets.py` — removes the phone status bar/home indicator and builds the full-screen mobile stage.
- `build_standalone.py` — rebuilds the self-contained `standalone.html`.
- `preview_composite.py` — builds offline reference-vs-result comparisons.
- `reference/` — a copy of the supplied Star Wave source.

## Run locally

```bash
cd /home/user/xmd-portfolio
python -m http.server 8000 --bind 0.0.0.0
```

Open `http://localhost:8000/`.

Force a specific layout while checking pixels:

- `http://localhost:8000/?view=desktop`
- `http://localhost:8000/?view=mobile`

Without a query parameter, the page automatically uses the desktop design on landscape windows and the mobile design on narrow/portrait windows.

## Customisation notes

- Replace the placeholder social URLs and `hello@xmd.dev` in `script.js` / `index.html`.
- Replace `assets/XMD-CV.pdf` with the real CV; the button already uses `download`.
- If you edit the source screenshots or portrait, run `python generate_assets.py` to rebuild the pixel-locked layers.
- The visible typography, cards, icons, borders, gradients and project thumbnails are preserved as artwork-derived layers so the supplied colours remain exact. The hidden semantic HTML keeps the page readable and navigable for assistive technology.


## Live deployment

- GitHub: https://github.com/Professor-xmd-company/xmd-developer-portfolio-2
- Vercel: https://xmd-developer-portfolio-2.vercel.app
- Force desktop: https://xmd-developer-portfolio-2.vercel.app/?view=desktop
- Force mobile: https://xmd-developer-portfolio-2.vercel.app/?view=mobile
