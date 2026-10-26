"""Create the real-website mobile artwork.

- removes the fake phone status bar and home indicator from the overlay;
- crops away the device side margins (x = 90..906);
- inserts low-detail background rows at four natural gaps so the design has a
  816 x 1766 ratio (matching a real 390 x 844 / 414 x 896 phone viewport)
  without stretching any component;
- produces a transformed reference target for visual QA.
"""
from PIL import Image
import numpy as np, cv2, os

ROOT = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(ROOT, 'assets')
Q = os.path.join(ROOT, 'qa')
os.makedirs(Q, exist_ok=True)

X0, X1 = 90, 906
H0 = 1536
INSERTS = {130: 50, 945: 60, 1200: 60, 1502: 60}
H1 = H0 + sum(INSERTS.values())  # 1766


def row_indices():
    idx = []
    for y in range(H0):
        if y in INSERTS:
            # repeat the preceding low-detail row; this adds empty space only
            idx.extend([max(0, y - 1)] * INSERTS[y])
        idx.append(y)
    return np.asarray(idx, dtype=np.int32)


IDX = row_indices()


def transform(arr, crop=True, remove_chrome=False, backdrop=None):
    if crop:
        arr = arr[:, X0:X1]
    if remove_chrome and arr.ndim == 3 and arr.shape[2] == 4:
        arr = arr.copy()
        chrome = np.zeros((H0,), dtype=bool)
        chrome[0:60] = True          # 9:41, signal, Wi-Fi, battery
        chrome[1515:1536] = True    # white home indicator + antialiasing
        arr[chrome, :, 3] = 0
        if backdrop is not None:
            bd = backdrop[:, X0:X1] if backdrop.shape[1] != arr.shape[1] else backdrop
            # Give fully transparent pixels the real dark backdrop colour so
            # browser image scaling cannot bleed white device-chrome pixels.
            arr[chrome, :, :3] = bd[chrome]
            transparent = arr[:, :, 3] < 8
            arr[transparent, :3] = bd[transparent]
    return arr[IDX].copy()


def load_rgba(name):
    return cv2.imread(os.path.join(A, name), cv2.IMREAD_UNCHANGED)


def save(name, arr):
    cv2.imwrite(os.path.join(A, name), arr)


# Full-stage layers.
bg = cv2.imread(os.path.join(A, 'bg-mobile.png'), cv2.IMREAD_COLOR)
glow = load_rgba('wave-glow-mobile.png')
overlay = load_rgba('overlay-mobile.png')
save('bg-mobile-web.png', transform(bg))
save('wave-glow-mobile-web.png', transform(glow))
save('overlay-mobile-web.png', transform(overlay, remove_chrome=True, backdrop=bg))

# The supplied portrait crop is unchanged, only its stage position changes.
# A transformed reference target: original screenshot with device chrome
# replaced by the clean background field, then the same crop / row insertion.
ref = cv2.imread('/home/user/uploads/file_00000000524882119afd50bf0ad3a936.png', cv2.IMREAD_COLOR)
ref[:60] = bg[:60]
ref[1515:1536] = bg[1515:1536]
target = transform(ref)
cv2.imwrite(os.path.join(Q, 'reference-mobile-web-target.png'), target)

print('mobile web assets:', 816, 'x', H1)
for n in ['bg-mobile-web.png', 'wave-glow-mobile-web.png', 'overlay-mobile-web.png']:
    print(' ', n, os.path.getsize(os.path.join(A, n)))
print(' target:', os.path.getsize(os.path.join(Q, 'reference-mobile-web-target.png')))
