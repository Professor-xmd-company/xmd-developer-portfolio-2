from PIL import Image
import numpy as np, cv2, os

ROOT = os.path.dirname(os.path.abspath(__file__))
UP = '/home/user/uploads'
OUT = os.path.join(ROOT, 'assets')
os.makedirs(OUT, exist_ok=True)

DESKTOP_REF = os.path.join(UP, 'file_000000005db08211b2da00fa115ebcd9.png')
MOBILE_REF  = os.path.join(UP, 'file_00000000524882119afd50bf0ad3a936.png')
PORTRAIT    = os.path.join(UP, 'file_00000000d9348211ac6688373dab7388.png')

# ---------- low-frequency background field (visible only through the wave / portrait holes) ----------
def background_field(path, out_name, cell=48):
    im = cv2.imread(path, cv2.IMREAD_COLOR)
    H,W = im.shape[:2]
    gh, gw = (H+cell-1)//cell, (W+cell-1)//cell
    small = np.zeros((gh,gw,3), np.uint8)
    for j in range(gh):
        for i in range(gw):
            p = im[j*cell:min((j+1)*cell,H), i*cell:min((i+1)*cell,W)].reshape(-1,3)
            lum = p.mean(1)
            sel = p[lum <= np.percentile(lum, 35)]
            small[j,i] = np.median(sel, axis=0)
    out = cv2.resize(small, (W,H), interpolation=cv2.INTER_CUBIC)
    out = cv2.GaussianBlur(out, (0,0), sigmaX=cell*.45, sigmaY=cell*.45)
    cv2.imwrite(os.path.join(OUT,out_name), out)
    return out

bg_d = background_field(DESKTOP_REF, 'bg-desktop.png')
bg_m = background_field(MOBILE_REF, 'bg-mobile.png')

# ---------- supplied portrait mapped exactly into each reference composition ----------
def make_portrait(ref_path, M, center, S, radius, out_name):
    src = cv2.imread(PORTRAIT, cv2.IMREAD_COLOR)[:,:,:3]
    ref = cv2.imread(ref_path, cv2.IMREAD_COLOR)
    x0, y0 = center[0]-S/2, center[1]-S/2
    Mc = M.copy().astype(np.float32)
    Mc[:,2] -= np.array([x0,y0], np.float32)
    warp = cv2.warpAffine(src, Mc, (S,S), flags=cv2.INTER_LANCZOS4,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))
    rc = ref[int(y0):int(y0)+S, int(x0):int(x0)+S]
    Y,X = np.mgrid[0:S,0:S]
    c = (S-1)/2
    r = np.hypot(X-c, Y-c)
    # low-frequency colour match to the screenshot while keeping high-frequency detail from supplied photo
    valid = (r < radius-7).astype(np.float32)
    diff = (rc.astype(np.float32)-warp.astype(np.float32))*valid[...,None]
    num = cv2.GaussianBlur(diff, (0,0), 18)
    den = cv2.GaussianBlur(valid, (0,0), 18) + 1e-6
    corrected = np.clip(warp.astype(np.float32) + num/den[...,None], 0, 255).astype(np.uint8)
    alpha = np.clip((radius-r)/1.4, 0, 1)
    rgba = np.dstack([corrected, (alpha*255).astype(np.uint8)])
    cv2.imwrite(os.path.join(OUT,out_name), rgba)

# affine fits from supplied portrait -> reference coordinates (SIFT verified against face landmarks)
M_desktop = np.array([[0.365020388,-0.004859858,661.599024],
                      [0.004859858,0.365020388, 55.767940]], np.float32)
M_mobile  = np.array([[0.338952382,-0.005955891,408.415452],
                      [0.005955891,0.338952382,142.765859]], np.float32)
make_portrait(DESKTOP_REF, M_desktop, (968.5,251.5), 360, 145, 'portrait-desktop.png')
make_portrait(MOBILE_REF,  M_mobile,  (694.5,323.5), 340, 138, 'portrait-mobile.png')

# ---------- exact screenshot overlays with holes for live wave canvas + supplied portrait ----------
def rect(mask, box, value=1):
    x1,y1,x2,y2 = box
    mask[y1:y2, x1:x2] = value

def make_overlay(ref_path, bg, out_name, cfg):
    S = cv2.imread(ref_path, cv2.IMREAD_COLOR)
    H,W = S.shape[:2]
    Y,X = np.mgrid[0:H,0:W]
    mask = np.ones((H,W), np.float32)
    # portrait interior hole
    r = np.hypot(X-cfg['center'][0], Y-cfg['center'][1])
    mask[r < cfg['hole_radius']] = 0
    # wave hole
    y1,y2 = cfg['wave_hole']
    mask[y1:y2,:] = 0
    # preserve all foreground UI that overlaps either hole
    for box in cfg['preserve']:
        rect(mask, box, 1)
    # preserve the neon ring outside the portrait hole
    mask[r >= cfg['hole_radius']+1] = 1
    # preserve everything below the wave (cards and footer)
    mask[y2:,:] = 1
    # feather hole boundaries, then re-assert crisp UI/card/ring areas
    soft = cv2.GaussianBlur(mask, (0,0), 1.15)
    soft[r >= cfg['hole_radius']+1] = 1
    soft[y2:,:] = 1
    for box in cfg['preserve']:
        rect(soft, box, 1)
    soft = np.clip(soft, 0, 1)
    rgba = np.dstack([S, (soft*255).astype(np.uint8)])
    cv2.imwrite(os.path.join(OUT,out_name), rgba)

    # positive low-frequency wave glow, stripped of stars, for the live wave area
    gy1,gy2 = cfg['glow_band']
    blur = cv2.GaussianBlur(S[gy1:gy2].astype(np.float32), (0,0), 22)
    base = cv2.GaussianBlur(bg[gy1:gy2].astype(np.float32), (0,0), 22)
    glow = np.clip(blur-base, 0, 255)
    full = np.zeros((H,W,3), np.float32)
    full[gy1:gy2] = glow
    alpha = np.zeros((H,W), np.float32)
    alpha[gy1:gy2] = np.clip(glow.max(2)/26.0, 0, 1)
    glow_rgba = np.dstack([np.clip(full,0,255).astype(np.uint8), (alpha*255).astype(np.uint8)])
    cv2.imwrite(os.path.join(OUT,out_name.replace('overlay-','wave-glow-')), glow_rgba)

make_overlay(DESKTOP_REF, bg_d, 'overlay-desktop.png', {
    'center':(968.5,251.5), 'hole_radius':145,
    'wave_hole':(230,445),
    'glow_band':(215,445),
    'preserve':[
        (196,136,668,248),   # headline, including the line that crosses the wave
        (196,262,605,311),   # intro paragraph
        (196,324,534,367),   # CTA buttons
        (202,386,358,414),   # social icons
        (742,246,876,295),   # Frontend Developer floating card
        (1124,127,1283,218), # Building clean code floating card
    ]
})

make_overlay(MOBILE_REF, bg_m, 'overlay-mobile.png', {
    'center':(694.5,323.5), 'hole_radius':138,
    'wave_hole':(530,635),
    'glow_band':(500,635),
    'preserve':[
        (150,198,585,412),   # hero copy/badge/buttons
        (150,438,585,490),   # CTA buttons
        (154,505,395,556),   # social icons
        (748,190,905,278),   # Turning ideas floating card
    ]
})

# ---------- small representative image assets, kept for inspection / reuse ----------
def save_crop(ref, box, name):
    Image.open(ref).crop(box).save(os.path.join(OUT,name))

save_crop(DESKTOP_REF, (93,445,1445,710), 'about-card-desktop.png')
save_crop(DESKTOP_REF, (93,719,852,941),  'skills-card-desktop.png')
save_crop(DESKTOP_REF, (880,719,1445,941),'projects-card-desktop.png')
save_crop(DESKTOP_REF, (93,941,1445,1024),'footer-desktop.png')
save_crop(MOBILE_REF,  (116,635,853,945),  'about-card-mobile.png')
save_crop(MOBILE_REF,  (116,1238,853,1502),'projects-card-mobile.png')

# ---------- real-website mobile stage (no phone chrome, full-screen ratio) ----------
import subprocess, sys
subprocess.run([sys.executable, os.path.join(ROOT, 'make_mobile_web_assets.py')], check=True)

print('generated:', len(os.listdir(OUT)), 'files')
for f in sorted(os.listdir(OUT)):
    print(' ', f, os.path.getsize(os.path.join(OUT,f)))
