# QA report — final full-screen portfolio

## 1. Original reference artwork (unchanged desktop)

| View | Reference | Browser render | Mean absolute RGB error | Pixels within 20/255 |
|---|---|---|---:|---:|
| Desktop | 1536 × 1024 | `qa/desktop-after-mobile-change.png` | **0.4392 / 255** | **98.75%** |
| Original mobile mockup | 1024 × 1536 | `qa/browser-mobile.png` | **0.3981 / 255** | **98.89%** |

The desktop layout was not changed by the final phone adjustment. The original mobile mockup comparison remains in `qa/browser-comparison-mobile.png` as proof that the design components were preserved.

## 2. Final real-phone layout

The fake phone chrome was removed: **9:41, signal, Wi-Fi, battery, home indicator and device side margins**. The mobile stage is now `816 × 1766`, derived from the original content area (`x 90..906`) plus extra dark rows inserted only in natural gaps. No component was stretched.

| Phone viewport | Stage rect | Target MAE | p95 error | Pixels >20/255 |
|---|---|---:|---:|---:|
| 390 × 844 | fills `389.98 × 844` | **2.693 / 255** | 15 | 4.90% |
| 414 × 896 | fills `414 × 896` | **2.102 / 255** | 11 | 3.59% |

The target is `qa/reference-mobile-web-target.png`: the original screenshot with the same chrome removal, crop and row insertion. The slightly higher MAE versus the old mockup is expected because the live wave canvas and supplied portrait are composited over a re-spaced dark background; all cards, typography, icons, colours, badges and thumbnails remain from the reference artwork.

Chrome-removal checks on the 390 × 844 render:

- top 30 px maximum channel value: **54** — no white status-bar text/icons;
- bottom 20 px maximum channel value: **64**, bright pixels >200: **0** — no home indicator;
- horizontal stage coverage: **389.98 / 390 px**;
- vertical stage coverage: **844 / 844 px**.

## 3. Browser checks

- Chromium console: **0 errors, 0 warnings**.
- Failed resources: **0**.
- Desktop interactive hotspots: **21**.
- Mobile interactive hotspots: **13**.
- `?view=desktop` and `?view=mobile` both render correctly.
- `standalone.html` was rebuilt with the new mobile-web assets and re-tested (0 errors / 0 warnings, no external resource requests).
- Automatic layout selection was verified at 390 × 844 and 414 × 896; both choose the full-screen mobile design.

## 4. Evidence files

- `qa/mobile-web-390-final.png` — final 390 × 844 phone render.
- `qa/mobile-web-414-final.png` — final 414 × 896 phone render.
- `qa/mobile-web-comparison-final.png` — transformed target vs final render, side by side.
- `qa/mobile-web-diff-final.png` — 4× amplified difference map.
- `qa/top-crop-final.png`, `qa/bottom-crop-final.png` — proof that device chrome is gone.
- `qa/reference-mobile-web-target.png` — transformed reference target.
- `qa/desktop-after-mobile-change.png` — unchanged desktop render after mobile work.
- `qa/browser-comparison-desktop.png`, `qa/browser-comparison-mobile.png` — original side-by-side comparisons.

## 5. Live deployment

- GitHub repo: **https://github.com/Professor-xmd-company/xmd-developer-portfolio-2**
- Vercel live: **https://xmd-developer-portfolio-2.vercel.app**
- Deployment URL: `https://xmd-developer-portfolio-2-jo8of8qky.vercel.app`

HTTP checks after deployment:

| Check | Result |
|---|---|
| `/` | **HTTP 200** |
| `/?view=mobile` | **HTTP 200** |
| `/?view=desktop` | **HTTP 200** |
| `/standalone.html` | **HTTP 200** |
| `/assets/overlay-mobile-web.png` | **HTTP 200** |
| GitHub repo page | **HTTP 200** |

Live Chromium checks: 0 console errors, 0 warnings, 0 failed resources, 13 mobile hotspots, mobile stage covers `389.98 × 844` of a `390 × 844` viewport, and the live mobile/desktop screenshots are pixel-identical to the local renders (MAE 0.0).

- `qa/live-mobile-390.png` — live phone render.
- `qa/live-desktop.png` — live desktop render.
- `qa/DEPLOY-RESULT.md` — deployment verification record.
