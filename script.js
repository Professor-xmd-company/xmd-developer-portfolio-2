/* XMD Portfolio — pixel-locked responsive stage + live Star Wave canvas.
   Visible artwork layers are generated from the supplied screenshots.
   The profile photo is warped from the supplied standalone portrait into the
   exact circle used by both compositions. */

const MODES = {
  desktop: {
    width: 1536,
    height: 1024,
    assets: {
      bg: 'assets/bg-desktop.png',
      glow: 'assets/wave-glow-desktop.png',
      portrait: 'assets/portrait-desktop.png',
      overlay: 'assets/overlay-desktop.png'
    },
    canvas: { left: 0, top: 134, width: 1536 },
    portrait: { left: 788, top: 71, size: 360 }
  },
  mobile: {
    width: 816,
    height: 1766,
    assets: {
      bg: 'assets/bg-mobile-web.png',
      glow: 'assets/wave-glow-mobile-web.png',
      portrait: 'assets/portrait-mobile.png',
      overlay: 'assets/overlay-mobile-web.png'
    },
    canvas: { left: 0, top: 480, width: 816 },
    portrait: { left: 434.5, top: 203.5, size: 340 }
  }
};

/* The real-phone mobile stage is the original artwork cropped to the content
   area (x 90..906) with extra background rows inserted in natural gaps.
   Hotspots are mapped through the same transformation, so no component moves
   relative to its artwork. */
const MOBILE_X_CROP = 90;
const MOBILE_ROW_INSERTS = [
  { at: 130, count: 50 },
  { at: 945, count: 60 },
  { at: 1200, count: 60 },
  { at: 1502, count: 60 }
];

function mobileY(y) {
  let out = y;
  for (const row of MOBILE_ROW_INSERTS) if (y >= row.at) out += row.count;
  return out;
}

function mobileRect(item) {
  const x = item.x - MOBILE_X_CROP;
  const y = mobileY(item.y);
  return { x, y, w: item.w, h: mobileY(item.y + item.h) - y };
}

const SOCIAL = {
  github: 'https://github.com/',
  x: 'https://x.com/',
  linkedin: 'https://www.linkedin.com/',
  email: 'mailto:hello@xmd.dev'
};

const LINK_SETS = {
  desktop: [
    { label: 'Home', href: '#home', x: 580, y: 22, w: 48, h: 26, r: 8 },
    { label: 'About', href: '#about', x: 650, y: 22, w: 56, h: 26, r: 8 },
    { label: 'Projects', href: '#projects', x: 738, y: 22, w: 78, h: 26, r: 8 },
    { label: 'Skills', href: '#skills', x: 838, y: 22, w: 58, h: 26, r: 8 },
    { label: 'Contact', href: '#contact', x: 910, y: 22, w: 74, h: 26, r: 8 },
    { label: "Let's talk", href: 'mailto:hello@xmd.dev', x: 1342, y: 15, w: 112, h: 39, r: 20 },

    { label: 'View My Projects', href: '#projects', x: 198, y: 325, w: 164, h: 41, r: 21 },
    { label: 'Download CV', href: 'assets/XMD-CV.pdf', download: 'XMD-CV.pdf', x: 370, y: 325, w: 162, h: 41, r: 21 },

    { label: 'GitHub', href: SOCIAL.github, external: true, x: 202, y: 386, w: 27, h: 27, r: 50 },
    { label: 'X', href: SOCIAL.x, external: true, x: 234, y: 386, w: 27, h: 27, r: 50 },
    { label: 'LinkedIn', href: SOCIAL.linkedin, external: true, x: 266, y: 386, w: 27, h: 27, r: 50 },
    { label: 'Email', href: SOCIAL.email, x: 298, y: 386, w: 27, h: 27, r: 50 },

    { label: 'View All Skills', href: '#skills', x: 760, y: 752, w: 72, h: 30, r: 8 },
    { label: 'View All Projects', href: '#projects', x: 1349, y: 758, w: 84, h: 30, r: 8 },

    { label: 'LaunchShield project', href: '#launchshield', x: 910, y: 801, w: 171, h: 136, r: 14 },
    { label: 'XMD Computer project', href: '#xmd-computer', x: 1096, y: 801, w: 172, h: 136, r: 14 },
    { label: 'Personal Portfolio project', href: '#personal-portfolio', x: 1281, y: 801, w: 164, h: 136, r: 14 },

    { label: 'Footer GitHub', href: SOCIAL.github, external: true, x: 1343, y: 970, w: 22, h: 24, r: 50 },
    { label: 'Footer X', href: SOCIAL.x, external: true, x: 1367, y: 970, w: 22, h: 24, r: 50 },
    { label: 'Footer LinkedIn', href: SOCIAL.linkedin, external: true, x: 1391, y: 970, w: 22, h: 24, r: 50 },
    { label: 'Footer Email', href: SOCIAL.email, x: 1415, y: 970, w: 22, h: 24, r: 50 }
  ],
  mobile: [
    { label: "Let's talk", href: 'mailto:hello@xmd.dev', x: 648, y: 61, w: 186, h: 53, r: 28 },
    { label: 'Open menu', href: '#home', x: 854, y: 60, w: 50, h: 54, r: 10 },

    { label: 'View My Projects', href: '#projects', x: 158, y: 437, w: 214, h: 50, r: 25 },
    { label: 'Download CV', href: 'assets/XMD-CV.pdf', download: 'XMD-CV.pdf', x: 387, y: 437, w: 186, h: 50, r: 25 },

    { label: 'GitHub', href: SOCIAL.github, external: true, x: 160, y: 512, w: 34, h: 34, r: 50 },
    { label: 'X', href: SOCIAL.x, external: true, x: 211, y: 512, w: 34, h: 34, r: 50 },
    { label: 'LinkedIn', href: SOCIAL.linkedin, external: true, x: 262, y: 512, w: 34, h: 34, r: 50 },
    { label: 'Email', href: SOCIAL.email, x: 313, y: 512, w: 34, h: 34, r: 50 },

    { label: 'View All Skills', href: '#skills', x: 718, y: 997, w: 151, h: 47, r: 24 },
    { label: 'View All Projects', href: '#projects', x: 718, y: 1260, w: 151, h: 47, r: 24 },

    { label: 'LaunchShield project', href: '#launchshield', x: 154, y: 1340, w: 238, h: 158, r: 15 },
    { label: 'XMD Computer project', href: '#xmd-computer', x: 405, y: 1340, w: 238, h: 158, r: 15 },
    { label: 'Personal Portfolio project', href: '#personal-portfolio', x: 655, y: 1340, w: 238, h: 158, r: 15 }
  ]
};

const stage = document.getElementById('stage');
const bg = document.getElementById('bg');
const glow = document.getElementById('waveGlow');
const canvas = document.getElementById('wave');
const portrait = document.getElementById('portrait');
const overlay = document.getElementById('overlay');
const links = document.getElementById('links');
const forcedView = new URLSearchParams(location.search).get('view');
let currentMode = null;

function detectMode() {
  if (forcedView === 'desktop' || forcedView === 'mobile') return forcedView;
  const isNarrow = window.innerWidth < 900;
  const isPortrait = window.innerHeight > window.innerWidth;
  return (isNarrow || isPortrait) ? 'mobile' : 'desktop';
}

function setImage(el, src) {
  if (el.getAttribute('src') !== src) el.setAttribute('src', src);
}

function renderLinks(mode) {
  links.replaceChildren();
  const frag = document.createDocumentFragment();
  LINK_SETS[mode].forEach((item, i) => {
    const a = document.createElement('a');
    a.href = item.href;
    a.textContent = item.label;
    a.setAttribute('aria-label', item.label);
    a.title = item.label;
    a.dataset.hotspot = `${mode}-${i}`;
    const rect = mode === 'mobile' ? mobileRect(item) : item;
    a.style.left = `${rect.x}px`;
    a.style.top = `${rect.y}px`;
    a.style.width = `${rect.w}px`;
    a.style.height = `${rect.h}px`;
    a.style.borderRadius = `${item.r ?? 10}px`;
    if (item.external) {
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
    }
    if (item.download) a.download = item.download;
    frag.appendChild(a);
  });
  links.appendChild(frag);
}

function drawWave(mode) {
  const cfg = MODES[mode].canvas;
  const cssHeight = cfg.width * 150 / 784;
  canvas.style.left = `${cfg.left}px`;
  canvas.style.top = `${cfg.top}px`;
  canvas.style.width = `${cfg.width}px`;
  canvas.style.height = `${cssHeight}px`;
  // drawStarWave is supplied verbatim in wave.js from the user's Star Wave.html
  drawStarWave(canvas);
}

function setMode(mode) {
  const cfg = MODES[mode];
  currentMode = mode;
  stage.dataset.mode = mode;
  document.documentElement.dataset.view = mode;
  document.body.dataset.view = mode;
  stage.style.width = `${cfg.width}px`;
  stage.style.height = `${cfg.height}px`;

  setImage(bg, cfg.assets.bg);
  setImage(glow, cfg.assets.glow);
  setImage(portrait, cfg.assets.portrait);
  setImage(overlay, cfg.assets.overlay);

  portrait.style.left = `${cfg.portrait.left}px`;
  portrait.style.top = `${cfg.portrait.top}px`;
  portrait.style.width = `${cfg.portrait.size}px`;
  portrait.style.height = `${cfg.portrait.size}px`;

  renderLinks(mode);
  drawWave(mode);
  console.info(`[XMD] ${mode} design · ${cfg.width}×${cfg.height}`);
}

function applyScale() {
  if (!currentMode) return;
  const cfg = MODES[currentMode];
  const scale = Math.min(window.innerWidth / cfg.width, window.innerHeight / cfg.height);
  stage.style.setProperty('--s', String(scale));
}

function update() {
  const mode = detectMode();
  if (mode !== currentMode) setMode(mode);
  else drawWave(mode);
  applyScale();
}

let resizeFrame = 0;
window.addEventListener('resize', () => {
  cancelAnimationFrame(resizeFrame);
  resizeFrame = requestAnimationFrame(update);
});
window.addEventListener('orientationchange', update);

update();
