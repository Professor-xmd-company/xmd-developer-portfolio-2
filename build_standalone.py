"""Build a fully self-contained standalone.html (no external asset requests)."""
from PIL import Image  # noqa: F401  (keeps the build env aligned with generate_assets.py)
import base64, json, os

ROOT = os.path.dirname(os.path.abspath(__file__))


def read(name):
    return open(os.path.join(ROOT, name), encoding='utf-8').read()


html = read('index.html')
css = read('styles.css')
wave = read('wave.js')
script = read('script.js')

names = [
    'bg-desktop.png', 'bg-mobile-web.png',
    'wave-glow-desktop.png', 'wave-glow-mobile-web.png',
    'portrait-desktop.png', 'portrait-mobile.png',
    'overlay-desktop.png', 'overlay-mobile-web.png',
    'XMD-CV.pdf', 'favicon.svg'
]


def mime(name):
    if name.endswith('.png'):
        return 'image/png'
    if name.endswith('.pdf'):
        return 'application/pdf'
    if name.endswith('.svg'):
        return 'image/svg+xml'
    return 'application/octet-stream'


asset_data = {}
for name in names:
    path = os.path.join(ROOT, 'assets', name)
    with open(path, 'rb') as f:
        asset_data[name] = 'data:%s;base64,%s' % (
            mime(name), base64.b64encode(f.read()).decode('ascii'))

for name in names:
    script = script.replace("'assets/%s'" % name, 'ASSET_DATA[%s]' % json.dumps(name))

# Initial desktop image sources.
initial = {
    'bg': 'bg-desktop.png',
    'waveGlow': 'wave-glow-desktop.png',
    'portrait': 'portrait-desktop.png',
    'overlay': 'overlay-desktop.png'
}
import re
for element_id, name in initial.items():
    html = re.sub(
        r'(<img id="%s"[^>]*?src=")[^"]+(")' % re.escape(element_id),
        lambda m, n=name: m.group(1) + asset_data[n] + m.group(2),
        html)

html = html.replace(
    '<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">',
    '<link rel="icon" href="%s" type="image/svg+xml">' % asset_data['favicon.svg'])
html = html.replace('<link rel="stylesheet" href="styles.css">', '<style>\n%s\n</style>' % css)
html = html.replace('<script src="wave.js"></script>', '<script>\n%s\n</script>' % wave)
inline = 'const ASSET_DATA=%s;\n%s' % (
    json.dumps(asset_data, separators=(',', ':')), script)
html = html.replace('<script src="script.js"></script>', '<script>\n%s\n</script>' % inline)
html = html.replace('href="assets/XMD-CV.pdf"', 'href="%s"' % asset_data['XMD-CV.pdf'])
html = html.replace('<title>XMD / Developer — Portfolio</title>',
                    '<title>XMD / Developer — Portfolio (standalone)</title>')

out = os.path.join(ROOT, 'standalone.html')
open(out, 'w', encoding='utf-8').write(html)
print('standalone.html', os.path.getsize(out), 'bytes')
