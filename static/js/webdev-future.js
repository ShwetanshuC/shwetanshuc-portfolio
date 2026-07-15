/* ============================================================
   WEBDEV-FUTURE.JS — /web-development/ only.
   Mounts the real Paper Shaders "Dot Orbit" shader (vendored vanilla
   build, no bundler) and masks it to the hero title, so the title is
   literally made of the orbiting dots. Falls back to plain static
   text with no shader for prefers-reduced-motion / WebGL failures.
   ============================================================ */

import { ShaderMount } from '../vendor/paper-shaders/shader-mount.js';
import { dotOrbitFragmentShader } from '../vendor/paper-shaders/shaders/dot-orbit.js';
import { metaballsFragmentShader } from '../vendor/paper-shaders/shaders/metaballs.js';
import { getShaderNoiseTexture } from '../vendor/paper-shaders/get-shader-noise-texture.js';

(function () {
  'use strict';

  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function initDotTitle() {
    var wrap = document.getElementById('wf-title-wrap');
    var host = document.getElementById('wf-title-shader');
    var fallback = document.getElementById('wf-title-fallback');
    var lines = host ? Array.prototype.slice.call(host.querySelectorAll('.wf-title-line')) : [];
    if (!wrap || !host || !lines.length) return;

    /* Below this width there isn't enough room for the dot grid to
       resolve legible letterforms — fall back to plain clean text
       rather than render an illegible smear. */
    var NARROW_VIEWPORT = 700;

    if (reduceMotion || window.innerWidth < NARROW_VIEWPORT) {
      wrap.classList.add('is-static');
      return;
    }

    var gl = document.createElement('canvas').getContext('webgl2');
    if (!gl) {
      wrap.classList.add('is-static');
      return;
    }

    /* Brighter champagne gold — high contrast against black at every
       stop (no stop drops below ~72% luminance), matching the "text
       should stand out, not blend in" direction. */
    var baseUniforms = {
      u_colorBack: [0, 0, 0, 0],
      u_colors: [
        [0.949, 0.894, 0.796, 1],
        [0.910, 0.835, 0.718, 1],
        [0.851, 0.714, 0.451, 1],
      ],
      u_colorsCount: 3,
      u_stepsPerColor: 4,
      u_fit: 2,
      /* Denser grid than the previous pass: individually smaller dots
         but far more of them per letter, so strokes read as continuous
         shapes up close instead of breaking into isolated circles. */
      u_scale: 0.105,
      u_rotation: 0,
      u_offsetX: 0,
      u_offsetY: 0,
      u_originX: 0.5,
      u_originY: 0.5,
      u_worldWidth: 0,
      u_worldHeight: 0,
    };

    /* Entrance: the dots start loosely scattered and ease into a calm,
       tightly-held resting formation — the title settles out of a soft
       haze rather than snapping into place. Rest state keeps spreading
       low so the idle motion reads as a slow, elegant drift rather than
       something that fights the letterforms for legibility. */
    var SETTLE = { u_size: 1, u_sizeRange: 0, u_spreading: 0.18 };
    var SCATTER = { u_size: 0.35, u_sizeRange: 0.6, u_spreading: 1 };

    var uniforms = Object.assign({}, baseUniforms, SCATTER);

    var mount = null;
    try {
      mount = new ShaderMount(host, dotOrbitFragmentShader, uniforms, undefined, 0.55);
    } catch (e) {
      console.error(e);
      fallback.style.display = 'block';
      wrap.classList.add('is-static');
      return;
    }

    function easeOutExpo(t) { return t === 1 ? 1 : 1 - Math.pow(2, -10 * t); }

    /* Every dot in the title orbits on the same shared clock, so once
       formed they all drift in near-unison — a synchronized shimmer
       that fights reading rather than adding life. The fix isn't a
       softer wobble, it's to stop: the dots fly in and settle once,
       then the shader freezes on that resting frame. The title reads
       like a fixed halftone portrait, not a screen you have to track. */
    function playSettleAnimation() {
      var duration = 950;
      var start = null;
      function step(now) {
        if (start === null) start = now;
        var t = Math.min(1, (now - start) / duration);
        var e = easeOutExpo(t);
        mount.setUniforms({
          u_size: SCATTER.u_size + (SETTLE.u_size - SCATTER.u_size) * e,
          u_sizeRange: SCATTER.u_sizeRange + (SETTLE.u_sizeRange - SCATTER.u_sizeRange) * e,
          u_spreading: SCATTER.u_spreading + (SETTLE.u_spreading - SCATTER.u_spreading) * e,
        });
        if (t < 1) {
          requestAnimationFrame(step);
        } else {
          mount.setSpeed(0);
        }
      }
      requestAnimationFrame(step);
    }

    function buildMask() {
      if (window.innerWidth < NARROW_VIEWPORT) {
        wrap.classList.add('is-static');
        wrap.classList.remove('is-ready');
        return;
      }
      wrap.classList.remove('is-static');
      var rect = wrap.getBoundingClientRect();
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = Math.max(1, Math.round(rect.width * dpr));
      var h = Math.max(1, Math.round(rect.height * dpr));
      var c = document.createElement('canvas');
      c.width = w;
      c.height = h;
      var ctx = c.getContext('2d');
      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = '#fff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      lines.forEach(function (line) {
        var lr = line.getBoundingClientRect();
        var cs = getComputedStyle(line);
        var cx = (lr.left - rect.left + lr.width / 2) * dpr;
        var cy = (lr.top - rect.top + lr.height / 2) * dpr;
        var fontSize = parseFloat(cs.fontSize) * dpr;
        ctx.font = cs.fontWeight + ' ' + fontSize + 'px ' + cs.fontFamily;

        /* Canvas 2D text metrics don't always match the CSS-rendered
           box exactly (font-loading race, sub-pixel rounding). If the
           measured glyph run would exceed the canvas, shrink the font
           just enough to fit rather than let it clip at the edges. */
        var measured = ctx.measureText(line.textContent).width;
        var available = w * 0.99;
        if (measured > available) {
          fontSize *= available / measured;
          ctx.font = cs.fontWeight + ' ' + fontSize + 'px ' + cs.fontFamily;
        }
        ctx.fillText(line.textContent, cx, cy);
      });

      var url = c.toDataURL('image/png');
      host.style.webkitMaskImage = 'url(' + url + ')';
      host.style.maskImage = 'url(' + url + ')';
      host.style.webkitMaskRepeat = 'no-repeat';
      host.style.maskRepeat = 'no-repeat';
      host.style.webkitMaskSize = '100% 100%';
      host.style.maskSize = '100% 100%';
    }

    var raf = null;
    function scheduleMask() {
      if (raf) cancelAnimationFrame(raf);
      raf = requestAnimationFrame(buildMask);
    }

    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(scheduleMask);
    } else {
      scheduleMask();
    }
    window.addEventListener('resize', scheduleMask);

    /* No idle-motion resume on scroll/tab-visibility here on purpose:
       once the entrance settles, playSettleAnimation() sets speed to 0
       and the shader stops rendering entirely (see shader-mount.js) —
       a frozen frame costs nothing to keep on screen, so there's
       nothing to pause. */

    requestAnimationFrame(function () {
      wrap.classList.add('is-ready');
      playSettleAnimation();
    });
  }

  /* Subtle cursor parallax on the hero content — the hero shifts a few
     px opposite the pointer, spring-damped via a CSS transition rather
     than a physics loop. Desktop pointers only. */
  function initHeroParallax() {
    if (reduceMotion) return;
    var content = document.querySelector('.wf-hero-content');
    var hero = document.querySelector('.wf-hero');
    if (!content || !hero || !window.matchMedia('(pointer: fine)').matches) return;

    var raf = null;
    hero.addEventListener('pointermove', function (e) {
      if (raf) return;
      raf = requestAnimationFrame(function () {
        var rect = hero.getBoundingClientRect();
        var px = (e.clientX - rect.left) / rect.width - 0.5;
        var py = (e.clientY - rect.top) / rect.height - 0.5;
        content.style.transform = 'translate(' + (px * -14).toFixed(1) + 'px, ' + (py * -10).toFixed(1) + 'px)';
        raf = null;
      });
    });
    hero.addEventListener('pointerleave', function () {
      content.style.transform = '';
    });
  }

  function initFadeIns() {
    var els = document.querySelectorAll('.wf-fade');
    if (reduceMotion) {
      els.forEach(function (el) { el.classList.add('visible'); });
      return;
    }
    els.forEach(function (el, i) {
      setTimeout(function () { el.classList.add('visible'); }, 120 * i);
    });
  }

  /* "Made for [word]" — cycles through what a site could be built for,
     opening at a readable pace, blurring fast through the middle, then
     decelerating slowly to a landing on "you" (red). Runs once, when
     scrolled into view. "Made for" never moves: the word's box is
     fixed to the widest word in the pool before the cycle starts. */
  function initMadeForCycle() {
    var word = document.getElementById('madefor-word');
    var trigger = word && word.closest('.wf-madefor-trigger');
    if (!word || !trigger) return;

    var POOL = [
      'sales', 'inventory', 'restaurants', 'boutiques', 'musicians',
      'studios', 'clinics', 'gyms', 'portfolios', 'creators',
      'nonprofits', 'salons', 'photographers', 'architects', 'bakeries',
      'florists', 'consultants', 'coaches', 'artists', 'schools',
      'farms', 'cafes', 'breweries', 'designers', 'freelancers',
      'contractors', 'therapists', 'realtors', 'clubs', 'venues'
    ];

    function lockWordWidth() {
      var probe = document.createElement('span');
      var cs = getComputedStyle(word);
      probe.style.cssText = 'position:absolute; visibility:hidden; white-space:nowrap; left:-9999px; top:-9999px;'
        + 'font-family:' + cs.fontFamily + ';'
        + 'font-weight:' + cs.fontWeight + ';'
        + 'font-size:' + cs.fontSize + ';'
        + 'letter-spacing:' + cs.letterSpacing + ';';
      document.body.appendChild(probe);
      var max = 0;
      POOL.concat(['you']).forEach(function (w) {
        probe.textContent = w;
        max = Math.max(max, probe.getBoundingClientRect().width);
      });
      document.body.removeChild(probe);
      trigger.style.setProperty('--madefor-word-w', Math.ceil(max) + 'px');
    }

    lockWordWidth();
    var resizeRaf = null;
    window.addEventListener('resize', function () {
      if (resizeRaf) cancelAnimationFrame(resizeRaf);
      resizeRaf = requestAnimationFrame(lockWordWidth);
    });

    if (reduceMotion) {
      word.textContent = 'you';
      word.classList.add('is-final');
      return;
    }

    function shuffled(arr) {
      var a = arr.slice();
      for (var i = a.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var t = a[i]; a[i] = a[j]; a[j] = t;
      }
      return a;
    }

    /* One continuous sinusoidal speed curve across the whole run —
       slow at the start, smoothly accelerating to a blur through the
       middle, smoothly decelerating back down — rather than three
       hard-coded phases stitched together. A discrete jump from a
       420ms opening delay straight to a 55ms blur delay is exactly
       the "speed randomly jumps" feeling to avoid; a sin() curve has
       no seam anywhere. "You" gets one extra deliberate beat on top
       of the curve's own slow tail, so the landing still reads as a
       full stop rather than just the curve's natural end. */
    var RUN_LENGTH = 26;
    var MIN_DELAY = 60;
    var MAX_DELAY = 620;
    /* Was a separate fixed FINAL_PAUSE (1500ms) tacked on after the
       curve — but the curve's own last step landed around MAX_DELAY
       (620ms), so jumping straight to 1500ms was a sudden two-and-a-
       half-times leap: the "abrupt stop before slowing down" you saw.
       Landing now belongs to the same continuous curve as everything
       else, just an asymmetric one: the first half eases in from
       MAX_DELAY down to MIN_DELAY (the buildup), the second half eases
       out from MIN_DELAY up to a much longer LANDING_MAX (the landing)
       — both halves meet at exactly MIN_DELAY at the midpoint, so
       there's no seam anywhere in the whole run, buildup or landing. */
    var LANDING_MAX = 1650;

    var pool = shuffled(POOL);
    var sequence = [];
    for (var w = 0; w < RUN_LENGTH; w++) {
      sequence.push(pool[w % pool.length]);
    }
    sequence.push('you');

    var delays = [];
    for (var d = 0; d < RUN_LENGTH; d++) {
      var t = d / (RUN_LENGTH - 1);
      var delay;
      if (t <= 0.5) {
        var u = t / 0.5;
        var speedFactor = Math.pow(Math.sin((Math.PI / 2) * u), 2);
        delay = MAX_DELAY - (MAX_DELAY - MIN_DELAY) * speedFactor;
      } else {
        var u2 = (t - 0.5) / 0.5;
        var growFactor = u2 * u2;
        delay = MIN_DELAY + (LANDING_MAX - MIN_DELAY) * growFactor;
      }
      delays.push(Math.round(delay));
    }

    var played = false;
    function playCycle() {
      if (played) return;
      played = true;
      var i = 0;
      function step() {
        word.textContent = sequence[i];
        if (i === sequence.length - 1) {
          word.classList.add('is-final');
          return;
        }
        setTimeout(function () {
          i += 1;
          step();
        }, delays[i]);
      }
      step();
    }

    /* Observe the headline itself, not the whole combined section —
       same class of bug as the stats glow: the section is now the
       full made-for/stats/blurb/photo composition with huge padding,
       and a 60%-of-target threshold against something that tall can
       never be satisfied by a normal viewport. */
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          playCycle();
          io.disconnect();
        }
      });
    }, { threshold: 0.6 });
    io.observe(word.closest('.wf-feature-headline'));

    /* The dropdown panel is taller than the fixed gap to the stats
       below it, so left alone it overlaps the $10,000+ number. Rather
       than shrink the panel, push the stats down while it's open —
       .wf-feature-top gets a class the CSS uses to grow its own
       bottom margin, so the content reflows out of the way instead of
       being covered. */
    var dropdown = document.getElementById('madefor-dropdown');
    var top = trigger.closest('.wf-feature-top');
    if (dropdown && top) {
      var openClass = 'madefor-open';
      var close = function () { top.classList.remove(openClass); };
      var open = function () { top.classList.add(openClass); };
      word.addEventListener('mouseenter', open);
      dropdown.addEventListener('mouseenter', open);
      word.addEventListener('mouseleave', close);
      dropdown.addEventListener('mouseleave', close);
    }
  }

  /* Color bleeding through the stat numbers themselves — no borders,
     no background shapes, nothing else on the page. A metaballs
     shader is masked to the exact glyph shapes of each settled number
     (same masking technique as the hero title) and faded in only
     after the count-up finishes, so the text is the only thing that
     ever moves or glows. */
  function initStatsNumberGlow() {
    if (reduceMotion) return;
    var pairs = [
      { number: document.getElementById('stat-number-1'), glow: document.getElementById('stat-glow-1') },
      { number: document.getElementById('stat-number-2'), glow: document.getElementById('stat-glow-2') },
    ].filter(function (p) { return p.number && p.glow; });
    if (!pairs.length) return;

    /* Observe the compact stats block itself, not the whole combined
       section — the section is now the full made-for/stats/blurb/
       photo composition with huge padding, far taller than any
       viewport, so a 50%-of-target threshold against it could never
       be satisfied. */
    var statsSection = document.querySelector('.wf-feature-stats');
    if (!statsSection) return;

    var gl = document.createElement('canvas').getContext('webgl2');
    if (!gl) return;

    var noiseImg = getShaderNoiseTexture();

    function buildMaskFor(numberEl, glowEl) {
      var rect = numberEl.getBoundingClientRect();
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = Math.max(1, Math.round(rect.width * dpr));
      var h = Math.max(1, Math.round(rect.height * dpr));
      var c = document.createElement('canvas');
      c.width = w;
      c.height = h;
      var ctx = c.getContext('2d');
      var cs = getComputedStyle(numberEl);
      ctx.fillStyle = '#fff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      var fontSize = parseFloat(cs.fontSize) * dpr;
      ctx.font = cs.fontWeight + ' ' + fontSize + 'px ' + cs.fontFamily;
      /* fillText ignores CSS letter-spacing entirely unless told about
         it explicitly — without this, the canvas draws glyphs at their
         natural (wider) spacing while the real text is tightened by
         -0.02em, so the mask drifts further right of the actual digits
         the longer the string is. ctx.letterSpacing needs a px string,
         same unit computation as the CSS value at this element's own
         font size, not the ancestor's (see the em-inheritance bug
         fixed earlier for the dropdown — different failure mode, same
         family of bug: an em-based value evaluated at the wrong size). */
      var letterSpacingPx = parseFloat(cs.letterSpacing);
      if (!isNaN(letterSpacingPx) && 'letterSpacing' in ctx) {
        ctx.letterSpacing = (letterSpacingPx * dpr) + 'px';
      }
      var measured = ctx.measureText(numberEl.textContent).width;
      var available = w * 0.99;
      if (measured > available) {
        fontSize *= available / measured;
        ctx.font = cs.fontWeight + ' ' + fontSize + 'px ' + cs.fontFamily;
      }
      ctx.fillText(numberEl.textContent, w / 2, h / 2);
      var url = c.toDataURL('image/png');
      glowEl.style.webkitMaskImage = 'url(' + url + ')';
      glowEl.style.maskImage = 'url(' + url + ')';
      glowEl.style.webkitMaskRepeat = 'no-repeat';
      glowEl.style.maskRepeat = 'no-repeat';
      glowEl.style.webkitMaskSize = '100% 100%';
      glowEl.style.maskSize = '100% 100%';
    }

    /* Vivid red + blue — a deliberate exception to the muted gold used
       everywhere else on the page, bleeding directly into the white
       digits rather than sitting as a tint behind them. */
    var VIVID = [
      [0.937, 0.267, 0.267, 1],
      [0.098, 0.400, 1.0, 1],
      [0.929, 0.929, 0.980, 1],
    ];

    function expectedText(numberEl) {
      var target = parseInt(numberEl.dataset.target, 10);
      var prefix = numberEl.dataset.prefix || '';
      var suffix = numberEl.dataset.suffix || '';
      return prefix + target.toLocaleString('en-US') + suffix;
    }

    function mount() {
      /* Raised from the original cap (220x140 @1x — visibly blocky,
         the "chunky" edges) to a resolution that actually resolves
         the metaballs' soft falloff smoothly. Only 2 instances, both
         idle at low speed until revealed, so the extra resolution
         costs little. */
      var LOW_RES_RATIO = 2;
      var LOW_RES_MAX_PX = 700 * 420;

      pairs.forEach(function (p) {
        try {
          /* The $10,000+ stat spans more horizontal space than 15,000+,
             so one extra blob keeps its bleed feeling as full as the
             shorter number's — with just a hair more speed so the
             extra blob doesn't read as static filler. */
          var isWide = p.number.id === 'stat-number-2';
          var shaderMount = new ShaderMount(p.glow, metaballsFragmentShader, {
            u_colorBack: [0, 0, 0, 0],
            u_colors: VIVID,
            u_colorsCount: 3,
            u_count: isWide ? 7 : 6,
            u_size: 0.95,
            u_noiseTexture: noiseImg,
            u_fit: 2, u_scale: 1, u_rotation: 0,
            u_offsetX: 0, u_offsetY: 0, u_originX: 0.5, u_originY: 0.5,
            u_worldWidth: 0, u_worldHeight: 0,
          }, undefined, 0, 0, LOW_RES_RATIO, LOW_RES_MAX_PX);
          p.mount = shaderMount;
          p.speed = isWide ? 0.24 : 0.2;
        } catch (e) {
          console.error(e);
        }
      });

      var resizeRaf = null;
      window.addEventListener('resize', function () {
        if (resizeRaf) cancelAnimationFrame(resizeRaf);
        resizeRaf = requestAnimationFrame(function () {
          pairs.forEach(function (p) {
            if (p.number.textContent === expectedText(p.number)) buildMaskFor(p.number, p.glow);
          });
        });
      });

      /* Rather than guess how long the count-up animation takes (a
         magic-number timer tied to a *different* IntersectionObserver
         elsewhere was the actual bug last round — it could fire before
         or after the real count finished, building a mask from
         whatever partial number happened to be on screen at that
         moment, which is exactly what read as a misregistered
         "shadow"). Poll the number's own text and only build the mask
         — the one moment it matters — once it truly matches the final
         value. */
      function waitForSettledThenReveal(p, attempt) {
        attempt = attempt || 0;
        if (p.number.textContent === expectedText(p.number) || attempt > 100) {
          buildMaskFor(p.number, p.glow);
          p.glow.classList.add('is-visible');
          if (p.mount) p.mount.setSpeed(p.speed || 0.2);
          return;
        }
        setTimeout(function () { waitForSettledThenReveal(p, attempt + 1); }, 80);
      }

      var revealed = false;
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting && !revealed) {
            revealed = true;
            pairs.forEach(waitForSettledThenReveal);
            io.disconnect();
          }
        });
      }, { threshold: 0.5 });
      io.observe(statsSection);
    }

    if (noiseImg.complete) {
      mount();
    } else {
      noiseImg.onload = mount;
    }
  }

  /* Magnetic hover: buttons pull a few px toward the cursor within
     their own bounds, then spring back — a small, deliberate detail
     rather than a plain color-change hover. Desktop pointers only. */
  function initMagneticButtons() {
    if (reduceMotion || !window.matchMedia('(pointer: fine)').matches) return;
    document.querySelectorAll('.wf-magnetic').forEach(function (btn) {
      btn.addEventListener('pointermove', function (e) {
        var rect = btn.getBoundingClientRect();
        var px = (e.clientX - rect.left) / rect.width - 0.5;
        var py = (e.clientY - rect.top) / rect.height - 0.5;
        /* -2px keeps the existing hover-lift alive — an inline style
           here otherwise wins specificity over the :hover rule and
           would silently cancel the lift while the pointer moves. */
        btn.style.transform = 'translate(' + (px * 6).toFixed(1) + 'px, ' + (py * 6 - 2).toFixed(1) + 'px)';
      });
      btn.addEventListener('pointerleave', function () {
        btn.style.transform = '';
      });
    });
  }

  /* Clicking either side card in the transformations triangle
     promotes it to the top slot, swapping places with whatever card
     is up there — the DOM never reorders, only each card's
     `data-slot` attribute changes, which flips which CSS grid
     position (and size) it claims. A FLIP animation (First, Last,
     Invert, Play) makes that swap read as one card sliding into the
     other's spot rather than a hard cut: measure both cards' rects
     before the swap, apply the swap, measure again, then animate from
     the old rect to the new one via transform so the browser never
     has to lay out mid-transition. */
  function initTriangleSwap() {
    var grid = document.getElementById('transformations');
    if (!grid) return;

    grid.addEventListener('click', function (e) {
      // Let real interactions (visit-site links, the before/after
      // drag handle) behave normally instead of triggering a swap.
      if (e.target.closest('a, [data-slider], .ba-handle')) return;

      var clicked = e.target.closest('.ba-card[data-slot="left"], .ba-card[data-slot="right"]');
      if (!clicked) return;
      var top = grid.querySelector('.ba-card[data-slot="top"]');
      if (!top || top === clicked) return;

      if (reduceMotion) {
        var slot = clicked.getAttribute('data-slot');
        clicked.setAttribute('data-slot', 'top');
        top.setAttribute('data-slot', slot);
        return;
      }

      var firstClicked = clicked.getBoundingClientRect();
      var firstTop = top.getBoundingClientRect();

      var clickedSlot = clicked.getAttribute('data-slot');
      clicked.setAttribute('data-slot', 'top');
      top.setAttribute('data-slot', clickedSlot);

      var lastClicked = clicked.getBoundingClientRect();
      var lastTop = top.getBoundingClientRect();

      flip(clicked, firstClicked, lastClicked);
      flip(top, firstTop, lastTop);
    });

    function flip(el, first, last) {
      var dx = first.left - last.left;
      var dy = first.top - last.top;
      var sx = first.width / last.width;
      var sy = first.height / last.height;
      el.style.transformOrigin = 'top left';
      el.style.transition = 'none';
      el.style.transform = 'translate(' + dx + 'px, ' + dy + 'px) scale(' + sx + ', ' + sy + ')';
      el.getBoundingClientRect(); // force the starting transform to apply before animating
      requestAnimationFrame(function () {
        el.style.transition = 'transform 1s var(--wf-ease, cubic-bezier(0.16, 1, 0.3, 1))';
        el.style.transform = '';
      });
      el.addEventListener('transitionend', function cleanup(ev) {
        if (ev.propertyName !== 'transform') return;
        el.style.transition = '';
        el.style.transformOrigin = '';
        el.removeEventListener('transitionend', cleanup);
      });
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    try { initDotTitle(); } catch (e) { console.error(e); }
    try { initFadeIns(); } catch (e) { console.error(e); }
    try { initHeroParallax(); } catch (e) { console.error(e); }
    try { initMadeForCycle(); } catch (e) { console.error(e); }
    try { initMagneticButtons(); } catch (e) { console.error(e); }
    try { initStatsNumberGlow(); } catch (e) { console.error(e); }
    try { initTriangleSwap(); } catch (e) { console.error(e); }
  });
})();
