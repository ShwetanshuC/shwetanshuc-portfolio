/* ============================================================
   PORTFOLIO.JS — Interactions for Shwetanshu's personal site
   ============================================================ */

// Mark body as JS-enabled so CSS can activate reveal animations
document.documentElement.classList.add('js');

// Only flip on hover-driven effects (e.g. the home hero photo strip) once
// the cursor genuinely moves — otherwise :hover can apply the instant the
// page loads just because the cursor happens to already be resting there.
window.addEventListener('pointermove', () => {
  document.documentElement.classList.add('mouse-moved');
}, { once: true });

document.addEventListener('DOMContentLoaded', () => {
  // Loader goes first and is self-contained (own try/catch inside) so a
  // bug in any function below it can never leave the loader stuck on screen.
  initPageLoader();
  [initNav, initScrollReveal, initCounters, initBeforeAfterSliders, initOOS, initWipBadge].forEach(fn => {
    try { fn(); } catch (e) { console.error(e); }
  });
});

/* ---- WIP BADGE: strike a soft A major chord and show a note ---- */
function initWipBadge() {
  const badge = document.getElementById('wip-badge');
  const toast = document.getElementById('wip-toast');
  if (!badge || !toast) return;

  let audioCtx = null;
  let toastTimer = null;

  function playTuningForkChord() {
    // Must be created (or resumed) inside the gesture handler itself —
    // mobile Safari mutes any AudioContext set up outside a user gesture.
    if (!audioCtx) {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      if (!Ctx) return;
      audioCtx = new Ctx();
    }
    if (audioCtx.state === 'suspended') audioCtx.resume();

    const now = audioCtx.currentTime;
    // A major triad: A4, C#5, E5
    const notes = [440.0, 554.37, 659.25];

    notes.forEach((freq, i) => {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.value = freq;

      // Soft, slightly staggered strike with a natural tuning-fork decay.
      const start = now + i * 0.03;
      const peak = 0.09;
      gain.gain.setValueAtTime(0, start);
      gain.gain.linearRampToValueAtTime(peak, start + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.0001, start + 2.4);

      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(start);
      osc.stop(start + 2.5);
    });
  }

  function showToast() {
    clearTimeout(toastTimer);
    toast.classList.add('is-visible');
    toastTimer = setTimeout(() => toast.classList.remove('is-visible'), 4000);
  }

  badge.addEventListener('click', () => {
    playTuningForkChord();
    showToast();
  });
}

/* ---- PAGE LOADER: brief on-brand intro on the home page ---- */
function initPageLoader() {
  const loader = document.getElementById('page-loader');
  if (!loader) return;
  const MIN_VISIBLE_MS = 900;
  // Hard cap so a single slow/failed asset (e.g. one hero photo over a slow
  // connection) can never leave the loader stuck on screen forever.
  const MAX_WAIT_MS = 2500;
  const start = performance.now();
  let done = false;

  function finish() {
    if (done) return;
    done = true;
    const elapsed = performance.now() - start;
    const wait = Math.max(0, MIN_VISIBLE_MS - elapsed);
    setTimeout(() => {
      loader.classList.add('is-done');
      setTimeout(() => loader.remove(), 650);
    }, wait);
  }

  if (document.readyState === 'complete') finish();
  else window.addEventListener('load', finish, { once: true });
  setTimeout(finish, MAX_WAIT_MS);
}

/* ---- NAV: transparent on hero, solid on scroll ---- */
function initNav() {
  const nav = document.querySelector('.site-nav');
  if (!nav) return;
  const hero = document.querySelector('.hero-section, .home-hero');

  function updateNav() {
    const scrolled = window.scrollY > 40;
    nav.classList.toggle('scrolled', scrolled);
    if (hero) nav.classList.toggle('hero-nav', !scrolled || window.scrollY < 40);
  }

  if (hero) nav.classList.add('hero-nav');
  updateNav();
  window.addEventListener('scroll', updateNav, { passive: true });

  // Active link
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(a => {
    if (a.getAttribute('href') === currentPath) a.classList.add('active');
  });
}

/* ---- SCROLL REVEAL ---- */
function initScrollReveal() {
  const els = document.querySelectorAll('.reveal');
  if (!els.length) return;

  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  els.forEach(el => obs.observe(el));
}

/* ---- ANIMATED COUNTERS ---- */
function initCounters() {
  const counters = document.querySelectorAll('.stat-number[data-target]');
  if (!counters.length) return;

  function animateCounter(el) {
    const target = parseInt(el.dataset.target);
    const prefix = el.dataset.prefix || '';
    const suffix = el.dataset.suffix || '';
    const duration = 1800;
    const start = performance.now();

    function update(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = Math.floor(eased * target).toLocaleString('en-US');
      el.textContent = prefix + value + suffix;
      if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
  }

  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        animateCounter(e.target);
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(c => obs.observe(c));
}

/* ---- BEFORE/AFTER SLIDERS ---- */
function initBeforeAfterSliders() {
  document.querySelectorAll('.ba-slider-wrap').forEach(initSlider);
}

function initSlider(wrap) {
  const after = wrap.querySelector('.ba-after');
  const divider = wrap.querySelector('.ba-divider');
  const handle = wrap.querySelector('.ba-handle');
  if (!after || !divider || !handle) return;

  const DESIGN_WIDTH = 1440;
  let isDragging = false;

  function scaleIframes() {
    const w = wrap.offsetWidth;
    const h = wrap.offsetHeight;
    if (!w || !h) return;
    const scale = w / DESIGN_WIDTH;
    wrap.querySelectorAll('iframe').forEach(f => {
      f.style.width  = DESIGN_WIDTH + 'px';
      f.style.height = Math.round(h / scale) + 'px';
      f.style.transform = `scale(${scale})`;
      f.style.transformOrigin = '0 0';
    });
  }

  scaleIframes();
  window.addEventListener('resize', scaleIframes, { passive: true });

  /* A single init-time call plus a window resize listener leaves a gap:
     if `wrap`'s own size settles later than DOMContentLoaded for any
     reason (a font swap reflow, a grid recalculation from a stylesheet
     that finishes applying late, browser-specific timing), the iframes
     are scaled once against a size that's about to change and nothing
     ever re-triggers scaleIframes() to correct it — no window resize
     event fires just because one element's box changed. A ResizeObserver
     watches the wrap directly, so any future size change (including the
     very first real layout) re-runs the scale calculation automatically. */
  if (window.ResizeObserver) {
    var ro = new ResizeObserver(function () { scaleIframes(); });
    ro.observe(wrap);
  }

  const card = wrap.closest('.ba-card');
  const labelPanelBefore = card && card.querySelector('.ba-label-panel--before');

  function setPosition(x) {
    const rect = wrap.getBoundingClientRect();
    const pos = Math.max(0, Math.min(1, (x - rect.left) / rect.width));
    const pct = pos * 100;
    after.style.clipPath = `inset(0 0 0 ${pct}%)`;
    divider.style.left = pct + '%';
    handle.style.left = pct + '%';
    if (labelPanelBefore) labelPanelBefore.style.width = pct + '%';
  }

  // Initialize at 50%
  setPosition(wrap.getBoundingClientRect().left + wrap.getBoundingClientRect().width / 2);

  function lockIframes()   { wrap.querySelectorAll('iframe').forEach(f => f.style.pointerEvents = 'none'); }
  function unlockIframes() { wrap.querySelectorAll('iframe').forEach(f => f.style.pointerEvents = '');    }

  // Mac traffic-light dots
  const dotRed    = card && card.querySelector('.ba-mac-dot--red');
  const dotYellow = card && card.querySelector('.ba-mac-dot--yellow');
  const dotGreen  = card && card.querySelector('.ba-mac-dot--green');

  if (card && dotGreen) {
    // Green: enter fullscreen (main page only)
    dotGreen.addEventListener('click', () => {
      if (!document.fullscreenElement) card.requestFullscreen();
    });
    // Red: close / exit fullscreen
    if (dotRed) dotRed.addEventListener('click', () => {
      if (document.fullscreenElement === card) document.exitFullscreen();
    });
    // Yellow: minimize / exit fullscreen
    if (dotYellow) dotYellow.addEventListener('click', () => {
      if (document.fullscreenElement === card) document.exitFullscreen();
    });

    document.addEventListener('fullscreenchange', () => {
      setTimeout(scaleIframes, 60);
    });
  }

  // Drag triggers ONLY from the handle — iframes stay interactive otherwise
  handle.addEventListener('mousedown', (e) => {
    isDragging = true;
    lockIframes();
    setPosition(e.clientX);
    e.preventDefault();
  });
  window.addEventListener('mousemove', (e) => { if (isDragging) setPosition(e.clientX); });
  window.addEventListener('mouseup',   ()  => { if (isDragging) { isDragging = false; unlockIframes(); } });

  handle.addEventListener('touchstart', (e) => {
    isDragging = true;
    lockIframes();
    setPosition(e.touches[0].clientX);
  }, { passive: true });
  window.addEventListener('touchmove', (e) => { if (isDragging) setPosition(e.touches[0].clientX); }, { passive: true });
  window.addEventListener('touchend',  ()  => { if (isDragging) { isDragging = false; unlockIframes(); } });
}

/* ---- OUT-OF-STYLE SCATTER — hybrid scroll-teaser + autonomous burst ---- */
function initOOS() {
  const section = document.getElementById('oos-section');
  if (!section) return;

  const inner  = section.querySelector('.wd-oos-inner');
  const cards  = Array.from(section.querySelectorAll('.wd-si'));
  const center = section.querySelector('.wd-oos-center');

  const CW = 220, CH = 162;
  const COMMIT    = 0.40;   // scroll progress (0-1) at which burst fires
  const TEASER_N  = 8;      // cards that preview scroll-linked
  // Each teaser starts arriving at this scroll progress
  const TEASER_STARTS = [0.00, 0.04, 0.08, 0.12, 0.17, 0.21, 0.26, 0.30];
  const TEASER_WIN    = 0.095; // how much scroll progress each teaser uses to fly in
  // Max rate teasers can advance — caps fast-scroll so cards always animate visibly
  // 0.40 / 950 means full teaser phase takes ≥ ~950ms regardless of scroll speed
  const MAX_RATE = 0.40 / 950;

  // Shuffle card indices once so teasers aren't always the same cards
  const order     = [...Array(cards.length).keys()].sort(() => Math.random() - 0.5);
  const teaserIds = order.slice(0, TEASER_N);
  const burstIds  = order.slice(TEASER_N);

  let teasers          = null;
  let committed        = false;
  let looping          = false;
  let displayProgress  = 0;
  let lastFrameTime    = null;
  let releaseHandlers  = null; // scroll-lock handlers saved so resetScatter can remove them
  let virusStart       = null; // startAnimation() ref from initVirusPhase (set on first run)

  // Applies is-done and removes the 200vh scroll trap, with scroll compensation
  // to prevent a visual jump depending on where the section is in the viewport.
  function applyIsDone() {
    if (section.classList.contains('is-done')) return;
    const rect = section.getBoundingClientRect();
    if (rect.bottom < 0) {
      // Section above viewport — compensate so content below doesn't jump up.
      const prevScroll = window.scrollY;
      const prevHeight = section.offsetHeight;
      section.classList.add('is-done');
      const delta = prevHeight - section.offsetHeight;
      if (delta > 0) window.scrollTo({ top: prevScroll - delta, behavior: 'instant' });
    } else if (rect.top > window.innerHeight) {
      // Section below viewport — safe, no compensation needed.
      section.classList.add('is-done');
    } else {
      // Section is in view — align section top to viewport top before switching
      // sticky → relative so the inner doesn't visually shift.
      window.scrollTo({ top: window.scrollY + rect.top, behavior: 'instant' });
      section.classList.add('is-done');
    }
  }

  function makeFlight(card, W, H) {
    const fx   = 10 + Math.random() * (W - CW - 20);
    const fy   = 10 + Math.random() * (H - CH - 20);
    const r    = +((Math.random() - 0.5) * 12).toFixed(1);
    const edge = Math.floor(Math.random() * 4);
    const dist = 600 + Math.random() * 800;
    let tx, ty;
    switch (edge) {
      case 0: tx = -(fx + dist);               ty = (Math.random()-0.5)*H*1.6; break; // left
      case 1: tx =  (W - fx) + dist;           ty = (Math.random()-0.5)*H*1.6; break; // right
      case 2: tx = (Math.random()-0.5)*W*1.6;  ty = -(fy + dist);              break; // top
      default:tx = (Math.random()-0.5)*W*1.6;  ty =  (H - fy) + dist;          break; // bottom
    }
    card.style.setProperty('--r', r + 'deg');
    card.style.left   = fx + 'px';
    card.style.top    = fy + 'px';
    card.style.right  = 'auto';
    card.style.bottom = 'auto';
    return { tx, ty, r };
  }

  function initTeasers(W, H) {
    if (teasers) return;
    teasers = teaserIds.map((ci, i) => {
      const card   = cards[ci];
      const flight = makeFlight(card, W, H);
      card.style.opacity = '0';
      return { card, ...flight, s: TEASER_STARTS[i], e: TEASER_STARTS[i] + TEASER_WIN };
    });
  }

  function commitBurst(W, H) {
    if (committed) return;
    committed = true;
    const commitStart = performance.now();

    // Freeze the page so momentum/inertia can't carry the user past the section.
    // overflow:hidden on <html> is a compositor-level lock — no event-handler
    // fighting, no snap-back jank.
    document.documentElement.style.overflow = 'hidden';

    // Release on the next deliberate scroll, but ignore wheel events for a short
    // grace window — those are residual momentum from the same gesture that
    // triggered the lock and would otherwise immediately undo it.
    const lockTime = performance.now();
    const MOMENTUM_GRACE = 500; // ms to treat wheel events as residual momentum

    function releaseOnScroll(e) {
      const goingDown = e.type === 'wheel'
        ? e.deltaY > 0
        : ['ArrowDown', 'PageDown', 'End', ' '].includes(e.key);
      if (!goingDown) return;
      if (e.type === 'wheel' && performance.now() - lockTime < MOMENTUM_GRACE) return;
      document.documentElement.style.overflow = '';
      window.removeEventListener('wheel',   releaseOnScroll);
      window.removeEventListener('keydown', releaseOnScroll);
      applyIsDone();
    }
    releaseHandlers = releaseOnScroll;
    window.addEventListener('wheel',   releaseOnScroll, { passive: true });
    window.addEventListener('keydown', releaseOnScroll);

    // Snap teasers to their resting positions immediately
    if (teasers) {
      teasers.forEach(({ card, r }) => {
        card.style.opacity   = '1';
        card.style.transform = `translate(0px,0px) rotate(${r}deg) scale(1)`;
        card.getAnimations().forEach(a => a.cancel());
      });
    }

    // Burst remaining 16 cards in 4 waves ~200ms apart
    const burstDelay = [0,0,0,0, 200,200,200,200, 400,400,400,400, 600,600,600,600];
    const promises = burstIds.map((ci, pos) => {
      const card = cards[ci];
      const { tx, ty, r } = makeFlight(card, W, H);
      const delay = (burstDelay[pos] || 0) + Math.random() * 55;
      const dur   = 480 + Math.random() * 200;
      const anim  = card.animate([
        { transform: `translate(${tx}px,${ty}px) rotate(0deg) scale(0.5)`, opacity: 0 },
        { transform: `translate(0px,0px) rotate(${r}deg) scale(1)`,        opacity: 1 }
      ], { duration: dur, delay, easing: 'cubic-bezier(0.34,1.56,0.64,1)', fill: 'forwards' });
      return new Promise(res => { anim.onfinish = res; });
    });

    // Heading springs in after first two burst waves have started
    // Heading animation: 650ms delay + 680ms duration = fully visible at ~1330ms from commit
    setTimeout(() => center.classList.add('is-revealed'), 650);

    // Once every burst card lands: commit inline styles, hand off to CSS live-loop
    Promise.all(promises).then(() => {
      cards.forEach(card => {
        const r = card.style.getPropertyValue('--r') || '0deg';
        card.style.opacity   = '1';
        card.style.transform = `translate(0px,0px) rotate(${r}) scale(1)`;
        card.getAnimations().forEach(a => a.cancel());
      });
      setTimeout(() => {
        section.classList.add('is-settled');

        // Start virus phase shortly after cards settle.
        // On first run, initialize it and capture the startAnimation ref.
        // On replay, call startAnimation directly — no re-init needed.
        setTimeout(() => {
          if (virusStart) {
            virusStart();
          } else {
            virusStart = initVirusPhase(section, inner, center);
          }
        }, 300);

        // Release the scroll wall 1s after the heading has fully animated in.
        const HEADING_DONE_AT = 650 + 680; // ms from commitStart
        const elapsed = performance.now() - commitStart;
        const waitMore = Math.max(0, HEADING_DONE_AT - elapsed) + 1000;

        setTimeout(() => {
          window.removeEventListener('wheel',   releaseOnScroll);
          window.removeEventListener('keydown', releaseOnScroll);
          document.documentElement.style.overflow = '';
          applyIsDone();
        }, waitMore);
      }, 500);
    });
  }

  function getScrollProgress() {
    const rect  = section.getBoundingClientRect();
    const range = section.offsetHeight - window.innerHeight;
    if (range <= 0) return 0;
    return Math.max(0, Math.min(1, -rect.top / range));
  }

  function frame(timestamp) {
    const realProgress = getScrollProgress();
    const W = inner.clientWidth;
    const H = inner.clientHeight;

    // Advance displayProgress toward real progress, capped per elapsed ms
    const dt = lastFrameTime ? Math.min(timestamp - lastFrameTime, 50) : 16;
    lastFrameTime = timestamp;
    displayProgress = Math.min(realProgress, displayProgress + MAX_RATE * dt);

    if (!committed) {
      initTeasers(W, H);

      // Drive teasers with the rate-capped display progress
      teasers.forEach(({ card, tx, ty, r, s, e }) => {
        const t_raw = Math.max(0, Math.min(1, (displayProgress - s) / (e - s)));
        const t     = 1 - (1 - t_raw) * (1 - t_raw); // ease-out quad
        card.style.opacity   = String(t);
        card.style.transform = `translate(${tx * (1 - t)}px,${ty * (1 - t)}px) rotate(${r * t}deg) scale(${0.5 + t * 0.5})`;
      });

      // Burst fires on real scroll position so it triggers at the right scroll depth
      if (realProgress >= COMMIT) {
        commitBurst(W, H);
        looping = false;
        return;
      }
    }

    if (displayProgress < realProgress - 0.001) {
      requestAnimationFrame(frame);
    } else {
      looping = false;
      lastFrameTime = null;
    }
  }

  function scheduleFrame() {
    if (looping) return;
    looping = true;
    requestAnimationFrame(frame);
  }

  window.addEventListener('scroll', scheduleFrame, { passive: true });

  // Initial check for pre-scrolled state on page load
  scheduleFrame();

  // Full scatter reset — called by the replay button (via custom event) so that
  // the user has to scroll through the full 200vh trap again from a dark screen.
  function resetScatter() {
    // Tear down any lingering scroll-lock handlers
    if (releaseHandlers) {
      window.removeEventListener('wheel',   releaseHandlers);
      window.removeEventListener('keydown', releaseHandlers);
      releaseHandlers = null;
    }
    document.documentElement.style.overflow = '';

    // Strip all phase classes (restores 200vh trap, sticky inner, dark bg)
    section.classList.remove('is-done', 'is-settled', 'is-infecting');
    center.classList.remove('is-revealed', 'security-visible');

    // Snap .wd-oos-cta back to amber instantly — kills the 12s reverse transition
    const cta = section.querySelector('.wd-oos-cta');
    if (cta) {
      cta.style.transition = 'none';
      void cta.offsetWidth;
      cta.style.transition = '';
    }

    // Clear all card inline styles so they're invisible and unpositioned
    cards.forEach(card => {
      card.getAnimations().forEach(a => a.cancel());
      card.style.opacity   = '0';
      card.style.transform = '';
      card.style.left      = '';
      card.style.top       = '';
      card.style.right     = '';
      card.style.bottom    = '';
      card.style.removeProperty('--r');
    });

    // Reset scatter closure state — frame() / commitBurst() start from scratch
    teasers         = null;
    committed       = false;
    displayProgress = 0;
    looping         = false;
    lastFrameTime   = null;
  }

  section.addEventListener('oos:reset-scatter', resetScatter);
}

/* ---- OOS VIRUS PHASE ---- */
function initVirusPhase(section, inner, center) {
  const gameOver = section.querySelector('#oos-gameover');
  if (!gameOver) return;

  const VIRUS_SVG_SRC = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" shape-rendering="crispEdges">
    <rect x="14" y="0" width="4" height="6" fill="#ff2020"/>
    <rect x="14" y="26" width="4" height="6" fill="#ff2020"/>
    <rect x="0" y="14" width="6" height="4" fill="#ff2020"/>
    <rect x="26" y="14" width="6" height="4" fill="#ff2020"/>
    <rect x="4" y="4" width="4" height="4" fill="#ff2020"/>
    <rect x="24" y="4" width="4" height="4" fill="#ff2020"/>
    <rect x="4" y="24" width="4" height="4" fill="#ff2020"/>
    <rect x="24" y="24" width="4" height="4" fill="#ff2020"/>
    <rect x="10" y="6" width="12" height="2" fill="#ff2020"/>
    <rect x="8" y="8" width="16" height="2" fill="#ff2020"/>
    <rect x="6" y="10" width="20" height="12" fill="#ff2020"/>
    <rect x="8" y="22" width="16" height="2" fill="#ff2020"/>
    <rect x="10" y="24" width="12" height="2" fill="#ff2020"/>
    <rect x="10" y="12" width="4" height="4" fill="#1a0000"/>
    <rect x="18" y="12" width="4" height="4" fill="#1a0000"/>
    <rect x="11" y="13" width="1" height="1" fill="rgba(255,200,200,0.7)"/>
    <rect x="19" y="13" width="1" height="1" fill="rgba(255,200,200,0.7)"/>
    <rect x="11" y="18" width="2" height="3" fill="#1a0000"/>
    <rect x="19" y="18" width="2" height="3" fill="#1a0000"/>
    <rect x="12" y="20" width="8" height="1" fill="#1a0000"/>
  </svg>`;

  // Pre-rasterize the SVG to a GPU-resident ImageBitmap (or a plain canvas fallback).
  // drawImage from an ImageBitmap is a direct GPU blit — no per-frame SVG decode,
  // which was causing the JS thread to drop frames and produce visible stepping.
  const SPRITE_PX = 40;
  let sprite    = null;
  let imgReady  = false;

  const virusImg = new Image();
  virusImg.onload = () => {
    if (typeof createImageBitmap === 'function') {
      createImageBitmap(virusImg).then(bmp => { sprite = bmp; imgReady = true; });
    } else {
      const fc = document.createElement('canvas');
      fc.width = fc.height = SPRITE_PX;
      fc.getContext('2d').drawImage(virusImg, 0, 0, SPRITE_PX, SPRITE_PX);
      sprite = fc;
      imgReady = true;
    }
  };
  virusImg.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(VIRUS_SVG_SRC);

  // redDiv is always created/managed by startAnimation() to avoid DOM duplicates on replay
  let redDiv = null;

  const virusCanvas = document.createElement('canvas');
  virusCanvas.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;z-index:50;pointer-events:none;image-rendering:pixelated;';
  inner.appendChild(virusCanvas);
  const vCtx = virusCanvas.getContext('2d');
  vCtx.imageSmoothingEnabled = false;

  function syncCanvas() {
    virusCanvas.width  = inner.clientWidth;
    virusCanvas.height = inner.clientHeight;
  }
  syncCanvas();
  window.addEventListener('resize', syncCanvas, { passive: true });

  // Particle system
  const MAX    = 350;
  const pos    = new Float32Array(MAX * 2);
  const vel    = new Float32Array(MAX * 2);
  const sz     = new Uint8Array(MAX);
  const bornAt = new Float64Array(MAX);
  let   count  = 0;

  function addVirus(ts) {
    if (count >= MAX) return;
    const w = virusCanvas.width, h = virusCanvas.height;
    const s = 26 + (Math.random() * 14 | 0);
    let x, y;
    if (count < 15 || count % 28 === 0) {
      // First batch + every 28th: fully random so viruses spread across the whole canvas
      x = s + Math.random() * (w - s * 2);
      y = s + Math.random() * (h - s * 2);
    } else {
      // Uniform parent selection (not biased toward recent) + large random offset
      // so children disperse instead of clustering near the parent
      const parentIdx = Math.floor(Math.random() * count);
      const pi = parentIdx * 2;
      const ps = sz[parentIdx];
      const spread = 60 + Math.random() * 120;
      const spawnAng = Math.random() * Math.PI * 2;
      x = pos[pi] + ps / 2 + Math.cos(spawnAng) * spread - s / 2;
      y = pos[pi + 1] + ps / 2 + Math.sin(spawnAng) * spread - s / 2;
    }
    x = Math.max(0, Math.min(w - s, x));
    y = Math.max(0, Math.min(h - s, y));
    // Velocity in px/sec (×60 converts old px/frame values to px/sec at 60fps baseline)
    const spd = (0.45 + Math.random() * 1.55) * 60;
    const ang = Math.random() * Math.PI * 2;
    const i2  = count * 2;
    pos[i2] = x;  pos[i2 + 1] = y;
    vel[i2] = Math.cos(ang) * spd;  vel[i2 + 1] = Math.sin(ang) * spd;
    sz[count]     = s;
    bornAt[count] = ts;
    count++;
  }

  const TAKEOVER_AT = 14000; // cumulative ms before red flood

  let cumulativeMs  = 0;
  let takeoverMs    = 0;
  let loopActive    = false;
  let animId        = null;
  let phaseComplete = false;
  let shaking       = false;
  let tookover      = false;
  let gameOverShown  = false;
  let recoveredShown = false;
  let lastTs        = 0;
  let spawnAccum    = 0;
  let shakeX = 0, shakeY = 0, tgtX = 0, tgtY = 0, shakeFrame = 0;

  function tick(timestamp) {
    const dtMs = Math.min(timestamp - (lastTs || timestamp), 50);
    const dt   = dtMs / 1000;
    lastTs     = timestamp;
    cumulativeMs += dtMs;
    if (tookover) takeoverMs += dtMs;

    const elapsedS = cumulativeMs / 1000;
    const vw = virusCanvas.width, vh = virusCanvas.height;

    // ── Takeover trigger ───────────────────────────────────────
    if (!tookover && cumulativeMs >= TAKEOVER_AT) {
      tookover = true;

      shaking = false;
      inner.style.willChange = '';
      inner.style.transform  = '';

      // Flood red div to full opacity via CSS (compositor thread)
      redDiv.style.transition = 'opacity 1.8s ease-in';
      redDiv.style.opacity    = '1';

      // Loop keeps running so viruses stay in motion; stopped inside the setTimeout
      setTimeout(() => {
        loopActive = false;
        if (animId) { cancelAnimationFrame(animId); animId = null; }

        // Red is now fully opaque — canvas is hidden underneath, safe to remove
        virusCanvas.remove();

        // Fade red → black smoothly (background-color is CSS-animatable)
        redDiv.style.transition = 'background-color 1.2s ease';
        redDiv.style.background = '#000';

        // Once black, fade in GAME OVER overlay
        setTimeout(() => {
          gameOverShown = true;
          gameOver.removeAttribute('aria-hidden');
          gameOver.classList.add('is-active');

          // Remove redDiv after overlay's own 0.75 s fade completes
          setTimeout(() => { redDiv.remove(); }, 900);

          // Recovery
          if (!recoveredShown) {
            setTimeout(() => {
              recoveredShown = true;
              phaseComplete  = true;
              gameOver.classList.add('is-recovered');
              sectionObs.disconnect();
            }, 7500);
          }
        }, 1200);
      }, 1800);
    }

    // ── Spawn (stops at takeover) ──────────────────────────────
    if (!tookover && elapsedS >= 2 && count < MAX) {
      const rawRate = 0.4 * Math.exp(0.45 * (elapsedS - 2));
      spawnAccum += Math.min(rawRate, 80) * dt;
      const toAdd = Math.min(Math.floor(spawnAccum), 6, MAX - count);
      spawnAccum -= toAdd;
      for (let i = 0; i < toAdd; i++) addVirus(timestamp);
    }

    // ── Red div opacity — pure CSS property update, GPU-composited ─
    if (!tookover) {
      redDiv.style.opacity = (count / MAX * 0.3).toFixed(4);
    }

    // ── Smooth shake ───────────────────────────────────────────
    if (shaking) {
      shakeFrame++;
      if (shakeFrame % 5 === 0) {
        const amp = count < 25  ? 0 :
                    count < 100 ? (count - 25) / 75 * 2 :
                    count < 400 ? 2 + (count - 100) / 300 * 5 :
                    count < 900 ? 7 + (count - 400) / 500 * 5 : 12;
        tgtX = (Math.random() - 0.5) * amp * 2;
        tgtY = (Math.random() - 0.5) * amp;
      }
      shakeX += (tgtX - shakeX) * 0.28;
      shakeY += (tgtY - shakeY) * 0.28;
      inner.style.transform = `translate(${shakeX | 0}px,${shakeY | 0}px)`;
    }

    // ── Virus sprites ──────────────────────────────────────────
    vCtx.clearRect(0, 0, vw, vh);
    if (imgReady && count > 0) {
      // Fade viruses out as red floods in — they keep moving throughout
      const virusAlpha = tookover ? Math.max(0, 1 - takeoverMs / 1800) : 1;
      // Exponential surge toward takeover; continues accelerating as red floods in.
      const t = Math.min(cumulativeMs / TAKEOVER_AT, 1);
      const speedFactor = tookover
        ? Math.min(11 + (takeoverMs / 1800) * 6, 17)   // 11→17 during red flood
        : Math.min(1 + t * t * 10, 11);                 // 1→11 over 14 s
      const BIRTH_DUR   = 350;
      vCtx.globalAlpha = virusAlpha;
      for (let i = 0; i < count; i++) {
        const i2 = i * 2;
        let x  = pos[i2],   y  = pos[i2 + 1];
        let vx = vel[i2],   vy = vel[i2 + 1];
        const s = sz[i];
        x += vx * speedFactor * dt; y += vy * speedFactor * dt;
        if (x <= 0 || x + s >= vw) { vx = -vx; x = Math.max(0, Math.min(vw - s, x)); }
        if (y <= 0 || y + s >= vh) { vy = -vy; y = Math.max(0, Math.min(vh - s, y)); }
        pos[i2] = x;  pos[i2 + 1] = y;
        vel[i2] = vx; vel[i2 + 1] = vy;
        const age        = timestamp - bornAt[i];
        const t          = age < BIRTH_DUR ? age / BIRTH_DUR : 1;
        const birthScale = 1 - (1 - t) * (1 - t) * (1 - t);
        const drawS      = Math.max(1, (s * birthScale) | 0);
        const cx = x + s * 0.5, cy = y + s * 0.5;
        vCtx.drawImage(sprite, (cx - drawS * 0.5) | 0, (cy - drawS * 0.5) | 0, drawS, drawS);
      }
      vCtx.globalAlpha = 1;
    }

    if (loopActive) animId = requestAnimationFrame(tick);
  }

  // Pause rAF when section scrolls off-screen; resume when it comes back.
  // Uses cumulative time so phases fire on actual watch-time, not wall-clock.
  const sectionObs = new IntersectionObserver(entries => {
    const visible = entries[0].intersectionRatio >= 0.05;
    if (visible && !loopActive && !phaseComplete) {
      loopActive = true;
      lastTs     = 0;
      animId     = requestAnimationFrame(tick);
    } else if (!visible && loopActive) {
      loopActive = false;
      if (animId) { cancelAnimationFrame(animId); animId = null; }
    }
  }, { threshold: [0.05] });

  function startAnimation() {
    // Remove stale redDiv if somehow still in DOM, then create a fresh one
    if (redDiv && redDiv.parentNode) redDiv.remove();
    redDiv = document.createElement('div');
    redDiv.style.cssText = 'position:absolute;inset:0;z-index:49;pointer-events:none;background:rgb(140,0,0);opacity:0;will-change:opacity,background;';
    inner.appendChild(redDiv);

    // Re-attach virusCanvas (ref kept after DOM removal) and reset its styles
    virusCanvas.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;z-index:50;pointer-events:none;image-rendering:pixelated;opacity:1;transition:none;';
    inner.appendChild(virusCanvas);
    syncCanvas();

    // Reset particle system
    count = 0;
    spawnAccum = 0;

    // Reset timing
    cumulativeMs = 0;
    takeoverMs   = 0;
    lastTs       = 0;

    // Reset flags
    tookover       = false;
    gameOverShown  = false;
    recoveredShown = false;
    phaseComplete  = false;
    shaking        = true;
    shakeX = 0; shakeY = 0; tgtX = 0; tgtY = 0; shakeFrame = 0;
    inner.style.willChange = 'transform';

    // Reset colour state — strip infecting classes so CSS transitions replay from scratch
    section.classList.remove('is-infecting');
    center.classList.remove('security-visible');

    // Force a reflow so the browser treats the next add as a fresh transition start
    void section.offsetWidth;

    center.classList.add('security-visible');
    setTimeout(() => section.classList.add('is-infecting'), 800);

    loopActive = true;
    animId = requestAnimationFrame(tick);
    sectionObs.observe(section);
  }

  startAnimation();

  // Replay button — visible in the recovered state.
  // Dispatches 'oos:reset-scatter' so initOOS tears down scatter state, then
  // commitBurst will call startAnimation() again once the user re-scrolls through.
  const replayBtn = section.querySelector('#oos-replay');
  if (replayBtn) {
    replayBtn.addEventListener('click', () => {
      // Fade the overlay out smoothly
      gameOver.classList.remove('is-active', 'is-recovered');
      gameOver.setAttribute('aria-hidden', 'true');

      // Reset scatter (removes is-done/is-settled/is-infecting, clears cards, snaps CTA color)
      section.dispatchEvent(new CustomEvent('oos:reset-scatter'));

      // Scroll to section top while overlay is fading — user sees completely dark state
      setTimeout(() => {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 150);
    });
  }

  return startAnimation;
}
