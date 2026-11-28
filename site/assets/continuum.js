// The continuum page. One document, one medium (the Eido loom), and four
// instruments that compute the page's claims live:
//
//   frame     the style point (Eido D1): twist your probe; hue is a
//             circular mean, and no number on the page moves with it.
//   quotient  four points under a projective probe: coordinates move,
//             the cross-ratio does not (continuum-math.js).
//   slits     two-slit probe coupling and the Sorkin triple-slit test,
//             with the scaling that separates looped from Kerr.
//   scale     block averaging with the commutation defect printed for
//             the naive and the renormalised macro dynamics.
//   atlas     the exact instruments of pull request 3 as a value field:
//             cell area is file size in bytes, nothing else.
//
// Reading is Eido D6: the whole article condenses as it is skimmed
// (condensed.json, authored ahead of time), on the reading score, with
// the panel's off switch. Without the variants it falls back to the
// plain reading weave, exactly as on the Eido site.

import { mixAestheticPresets } from "../../src/aesthetic-mixer.js";
import { mountSimplexPad } from "../../src/simplex-pad.js";
import { layoutCells, layerThreads, hitTest } from "../../src/cell-layout.js";
import { setupReadingWeave } from "../../src/reading-weave.js";
import { loadCondensed, setupCondense } from "../../src/condense.js";
import { scene, setHue, mediumState, onFrame, reduced } from "./loom.js";
import {
  PROBE_POINTS, crossRatio, mobius,
  visibility, sorkin, twoSlitIntensity, screenU, SLITS,
  FIELD, emergence,
} from "./continuum-math.js";

const $ = (sel, el = document) => el.querySelector(sel);
const $$ = (sel, el = document) => [...el.querySelectorAll(sel)];
const fmt = (v, d = 4) => (Math.abs(v) !== 0 && Math.abs(v) < 1e-3 ? v.toExponential(2) : v.toFixed(d));

/* ---------- The medium, written out ---------- */

function paintMedium() {
  const el = $("#medium-eq");
  if (!el) return;
  const m = mediumState();
  el.textContent =
    `y(x, t) = Σ aₙ · sin(nπx / W) · cos(2π·n·f₁·t + n·φᵢ)     n = 1 … ${m.amps.length}\n` +
    `f₁ = ${m.f1.toFixed(3)} Hz   t = ${m.t.toFixed(1)} s   ${m.threads} threads   a = ${m.amps.map((a) => a.toFixed(2)).join("  ")}`;
}

/* ---------- Your frame: style as a point (Eido D1) ---------- */

// Two presets sit at hue 0.95 and 0.05, five percent apart on the
// circle and ninety apart on a line, so the circular mean is visible:
// blending them stays red, where a linear average would give cyan.
const PRESETS = {
  wave: { rounding: 0.9, density: 0.35, hue: 0.5444, contrast: 0.06 },
  grid: { rounding: 0.0, density: 0.9, hue: 0.05, contrast: 0.02 },
  grain: { rounding: 0.45, density: 0.15, hue: 0.95, contrast: 0.22 },
};
const PRESET_NAMES = Object.keys(PRESETS);
const frameState = { w: [0.6, 0.2, 0.2] };

function applyFrame() {
  const v = mixAestheticPresets(PRESETS, Object.fromEntries(PRESET_NAMES.map((n, i) => [n, frameState.w[i]])));
  setHue(v.hue * 360);
  const root = document.documentElement.style;
  root.setProperty("--rounding", v.rounding.toFixed(4));
  root.setProperty("--density", v.density.toFixed(4));
  root.setProperty("--contrast", v.contrast.toFixed(4));
  const el = $("#frame-state");
  if (el) {
    el.textContent =
      `w [${frameState.w.map((x) => x.toFixed(2)).join(", ")}]  Σ ${frameState.w.reduce((a, b) => a + b, 0).toFixed(2)}\n` +
      `hue ${(v.hue * 360).toFixed(0)}°  rounding ${v.rounding.toFixed(2)}  density ${v.density.toFixed(2)}  contrast ${v.contrast.toFixed(2)}`;
  }
  return v;
}

function initFrame() {
  const host = $("#frame-pad");
  if (!host) return;
  mountSimplexPad(host, {
    labels: ["Wave", "Grid", "Grain"],
    weights: frameState.w,
    hues: PRESET_NAMES.map((n) => PRESETS[n].hue),
    onChange: (w) => { frameState.w = w; applyFrame(); },
  });
  applyFrame();
}

/* ---------- Quotient out the observer: the cross-ratio ---------- */

const probe = { alpha: 1.6, beta: 0.8, gamma: 0.22 };

function paintQuotient() {
  const el = $("#quotient-numbers");
  if (!el) return;
  const ys = PROBE_POINTS.map((x) => mobius(x, probe));
  const cr0 = crossRatio(PROBE_POINTS);
  const cr1 = crossRatio(ys);
  el.textContent =
    `x        ${PROBE_POINTS.map((v) => v.toFixed(3).padStart(8)).join(" ")}\n` +
    `φ(x)     ${ys.map((v) => v.toFixed(3).padStart(8)).join(" ")}\n` +
    `(A,B;C,D) = ${cr0.toFixed(10)}   through the probe = ${cr1.toFixed(10)}   |Δ| = ${Math.abs(cr1 - cr0).toExponential(1)}`;
}

function initQuotient() {
  const canvas = $("#quotient-stage");
  if (!canvas) return;
  const handle = scene(canvas, {
    frame(ctx, { w, h, pal }) {
      ctx.clearRect(0, 0, w, h);
      const ys = PROBE_POINTS.map((x) => mobius(x, probe));
      const lanes = [
        { pts: [...PROBE_POINTS], y: h * 0.3, label: "x" },
        { pts: ys, y: h * 0.72, label: "φ(x)" },
      ];
      ctx.font = "12px ui-monospace, monospace";
      for (const lane of lanes) {
        const lo = Math.min(...lane.pts);
        const hi = Math.max(...lane.pts);
        const X = (v) => (w * 0.08) + ((v - lo) / (hi - lo || 1)) * w * 0.84;
        ctx.strokeStyle = pal.line;
        ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(w * 0.04, lane.y); ctx.lineTo(w * 0.96, lane.y); ctx.stroke();
        ctx.fillStyle = pal.ink2 || pal.ink;
        ctx.fillText(lane.label, w * 0.04, lane.y - 14);
        lane.pts.forEach((v, i) => {
          ctx.fillStyle = pal.voice(i, 1);
          ctx.beginPath(); ctx.arc(X(v), lane.y, 6, 0, Math.PI * 2); ctx.fill();
          ctx.fillText("ABCD"[i], X(v) - 4, lane.y + 24);
        });
      }
      // Threads joining each point to its image: what the probe does.
      const lo0 = Math.min(...PROBE_POINTS), hi0 = Math.max(...PROBE_POINTS);
      const lo1 = Math.min(...ys), hi1 = Math.max(...ys);
      const X0 = (v) => w * 0.08 + ((v - lo0) / (hi0 - lo0)) * w * 0.84;
      const X1 = (v) => w * 0.08 + ((v - lo1) / (hi1 - lo1 || 1)) * w * 0.84;
      ctx.lineWidth = 1;
      PROBE_POINTS.forEach((x, i) => {
        ctx.strokeStyle = pal.voice(i, 0.35);
        ctx.beginPath(); ctx.moveTo(X0(x), h * 0.3 + 8); ctx.lineTo(X1(ys[i]), h * 0.72 - 8); ctx.stroke();
      });
    },
  });
  const bind = (id, key) => {
    const input = $(id);
    if (!input) return;
    input.addEventListener("input", () => {
      probe[key] = Number(input.value);
      const out = $(`${id}-out`);
      if (out) out.textContent = probe[key].toFixed(2);
      paintQuotient();
      handle.invalidate();
    });
  };
  bind("#probe-alpha", "alpha");
  bind("#probe-beta", "beta");
  bind("#probe-gamma", "gamma");
  paintQuotient();
}

/* ---------- Subtractive selection: slits and the Sorkin test ---------- */

const slitState = { mode: "two", gamma: 0.5, coupling: 0.35, eta: 0.05, lambda: 1 };

function slitCurves() {
  if (slitState.mode === "two") return { P: twoSlitIntensity(slitState.gamma), I3: null, s: null };
  const s = sorkin({
    mode: slitState.mode,
    g: slitState.mode === "looped" ? slitState.coupling : 0,
    eta: slitState.mode === "kerr" ? slitState.eta : 0,
    lambda: slitState.lambda,
  });
  return { P: s.Pabc, I3: s.I3, s };
}

function paintSlits() {
  const el = $("#slit-numbers");
  if (!el) return;
  if (slitState.mode === "two") {
    const { V, D } = visibility(slitState.gamma);
    el.textContent =
      `γ = ${slitState.gamma.toFixed(2)}   V = (1 − γ²)/(1 + γ²) = ${V.toFixed(4)}   D = 2γ/(1 + γ²) = ${D.toFixed(4)}\n` +
      `V² + D² = ${(V * V + D * D).toFixed(6)}   (pure probe bath; a mixed bath gives < 1)`;
    return;
  }
  const { s } = slitCurves();
  const what = slitState.mode === "looped" ? `g = ${slitState.coupling.toFixed(2)}` : slitState.mode === "kerr" ? `η = ${slitState.eta.toFixed(2)}` : "no coupling";
  el.textContent =
    `${slitState.mode}   ${what}   λ = ${slitState.lambda}\n` +
    `∫|I_ABC| du = ${fmt(s.intI3, 6)}   κ₃ = ∫|I_ABC| / Σ∫|I_pairs| = ${fmt(s.kappa3, 6)}   max P_ABC = ${s.maxP.toFixed(2)}`;
}

function initSlits() {
  const canvas = $("#slit-stage");
  if (!canvas) return;
  const handle = scene(canvas, {
    frame(ctx, { w, h, pal }) {
      ctx.clearRect(0, 0, w, h);
      const { P, I3 } = slitCurves();
      const maxP = Math.max(...P, 1e-9);
      const X = (i) => (i / (SLITS.N - 1)) * w;
      const Y = (v) => h * 0.92 - (v / maxP) * h * 0.8;
      ctx.strokeStyle = pal.line;
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(0, h * 0.92); ctx.lineTo(w, h * 0.92); ctx.stroke();
      ctx.strokeStyle = pal.crest(0.95);
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      for (let i = 0; i < SLITS.N; i += 1) { const x = X(i), y = Y(P[i]); if (i) ctx.lineTo(x, y); else ctx.moveTo(x, y); }
      ctx.stroke();
      if (I3) {
        const maxI = Math.max(...[...I3].map(Math.abs), 1e-12);
        const mid = h * 0.92;
        ctx.strokeStyle = pal.trough(0.9);
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        for (let i = 0; i < SLITS.N; i += 1) {
          const x = X(i);
          const y = mid - (I3[i] / maxI) * h * 0.22;
          if (i) ctx.lineTo(x, y); else ctx.moveTo(x, y);
        }
        ctx.stroke();
      }
      ctx.font = "12px ui-monospace, monospace";
      ctx.fillStyle = pal.ink2 || pal.ink;
      ctx.fillText(slitState.mode === "two" ? "P(u) two slits" : "P_ABC(u)", 8, 18);
      if (I3) ctx.fillText("I_ABC(u), scaled to fit", 8, 36);
      void screenU;
    },
  });
  const refresh = () => { paintSlits(); handle.invalidate(); };
  $$("[data-slit-mode]").forEach((btn) => {
    btn.addEventListener("click", () => {
      slitState.mode = btn.dataset.slitMode;
      $$("[data-slit-mode]").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
      refresh();
    });
  });
  $$("[data-lambda]").forEach((btn) => {
    btn.addEventListener("click", () => {
      slitState.lambda = Number(btn.dataset.lambda);
      $$("[data-lambda]").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
      refresh();
    });
  });
  const bindRange = (id, fn) => {
    const input = $(id);
    if (!input) return;
    input.addEventListener("input", () => {
      fn(Number(input.value));
      const out = $(`${id}-out`);
      if (out) out.textContent = Number(input.value).toFixed(2);
      refresh();
    });
  };
  bindRange("#slit-gamma", (v) => { slitState.gamma = v; });
  bindRange("#slit-coupling", (v) => { slitState.coupling = v; slitState.eta = v * 0.15; });
  paintSlits();
}

/* ---------- The vertical axis: coarse-graining ---------- */

const scaleState = { b: 4 };

function paintScale() {
  const el = $("#scale-numbers");
  if (!el) return;
  const e = emergence(scaleState.b);
  el.textContent =
    `b = ${e.b}   grid ${FIELD.N}×${FIELD.N} → ${e.m}×${e.m}\n` +
    `δ_emg (same ν) = ${e.delta.toFixed(4)}   δ_emg (ν/b²) = ${e.deltaScaled.toFixed(4)}\n` +
    `mode (2,1): ${e.lowBefore.toFixed(3)} → ${e.lowAfter.toFixed(3)}   mode (11,9): ${e.highBefore.toFixed(3)} → ${e.highAfter.toFixed(3)}   variance ${e.varBefore.toFixed(3)} → ${e.varAfter.toFixed(3)}`;
}

function initScale() {
  const canvas = $("#scale-stage");
  if (!canvas) return;
  const handle = scene(canvas, {
    frame(ctx, { w, h, pal }) {
      ctx.clearRect(0, 0, w, h);
      const e = emergence(scaleState.b);
      const m = e.m;
      const side = Math.min(w, h) * 0.96;
      const ox = (w - side) / 2;
      const oy = (h - side) / 2;
      const cell = side / m;
      let lo = Infinity, hi = -Infinity;
      for (const v of e.coarse) { if (v < lo) lo = v; if (v > hi) hi = v; }
      const mid = (lo + hi) / 2;
      const span = (hi - lo) / 2 || 1;
      for (let i = 0; i < m; i += 1) {
        for (let j = 0; j < m; j += 1) {
          const v = (e.coarse[i * m + j] - mid) / span;
          ctx.fillStyle = pal.phase(v, 0.92);
          ctx.fillRect(ox + j * cell + 0.5, oy + i * cell + 0.5, cell - 1, cell - 1);
        }
      }
    },
  });
  $$("[data-block]").forEach((btn) => {
    btn.addEventListener("click", () => {
      scaleState.b = Number(btn.dataset.block);
      $$("[data-block]").forEach((x) => x.setAttribute("aria-pressed", String(x === btn)));
      paintScale();
      handle.invalidate();
    });
  });
  paintScale();
}

/* ---------- Atlas: the verified instruments as a value field ---------- */

// Bytes are the file sizes in pull request 3 (branch
// expedition/synthesis-instruments), read 22 November 2026. hrefs point
// at that pull request's head 7fe4ee22, pending merge, not at main.
// Area encodes bytes and nothing else; threads join each family.
export const INSTRUMENTS = [
  { name: "double-slit observer", file: "double_slit_continuum_observer.py", bytes: 56461, audit: "AUDIT-054", family: "exact", href: "https://github.com/Foundation-0/continuum/blob/7fe4ee2202dad0e5c5420756a037c212fd3e52ee/expedition-double-slit-continuum/double_slit_continuum_observer.py" },
  { name: "optimal inertia rank", file: "optimal_inertia_rank.py", bytes: 52247, audit: "AUDIT-006R", family: "exact", href: "https://github.com/Foundation-0/continuum/blob/7fe4ee2202dad0e5c5420756a037c212fd3e52ee/expedition-synthesis/optimal_inertia_rank.py" },
  { name: "tropical quotient sheaf", file: "tropical_quotient_sheaf_bridge.py", bytes: 49270, audit: "AUDIT-004", family: "exact", href: "https://github.com/Foundation-0/continuum/blob/7fe4ee2202dad0e5c5420756a037c212fd3e52ee/expedition-synthesis/tropical_quotient_sheaf_bridge.py" },
  { name: "fold sheaf collapse", file: "fold_sheaf_collapse.py", bytes: 35275, audit: "AUDIT-019", family: "exact", href: "https://github.com/Foundation-0/continuum/blob/7fe4ee2202dad0e5c5420756a037c212fd3e52ee/expedition-synthesis/fold_sheaf_collapse.py" },
  { name: "continuum probes audit", file: "audit_continuum_probes.py", bytes: 29597, audit: "AUDIT-007R", family: "sampled", href: "https://github.com/Foundation-0/continuum/blob/7fe4ee2202dad0e5c5420756a037c212fd3e52ee/expedition-synthesis/audit_continuum_probes.py" },
  { name: "homotopy Bregman bridge", file: "portal78_homotopy_bregman_bridge.py", bytes: 28562, audit: "AUDIT-008R", family: "exact", href: "https://github.com/Foundation-0/continuum/blob/7fe4ee2202dad0e5c5420756a037c212fd3e52ee/expedition-synthesis/portal78_homotopy_bregman_bridge.py" },
  { name: "two-loop omitted variable", file: "two_loop_omitted_variable.py", bytes: 13732, audit: "AUDIT-005", family: "exact", href: "https://github.com/Foundation-0/continuum/blob/7fe4ee2202dad0e5c5420756a037c212fd3e52ee/expedition-synthesis/two_loop_omitted_variable.py" },
];

const atlasState = { layout: null, hit: -1 };

function paintAtlasReadout() {
  const el = $("#atlas-readout");
  if (!el) return;
  const it = INSTRUMENTS[atlasState.hit];
  el.textContent = it
    ? `${it.file}  ·  ${it.bytes.toLocaleString("en-GB")} bytes  ·  ${it.audit}  ·  ${it.family === "exact" ? "exact rational core" : "sampled, with null controls"}`
    : "Press a cell. The same instruments are listed as links below.";
}

function initAtlas() {
  const canvas = $("#atlas-stage");
  if (!canvas) return;
  const handle = scene(canvas, {
    frame(ctx, { w, h, pal }) {
      ctx.clearRect(0, 0, w, h);
      const items = INSTRUMENTS.map((it) => ({ weight: it.bytes, labelLength: it.name.length }));
      const layout = layoutCells(items, { width: w, height: h });
      atlasState.layout = layout;
      const threads = layerThreads(layout.cells, INSTRUMENTS.map((it) => it.family));
      ctx.lineWidth = 1.2;
      for (const e of threads) {
        const A = layout.cells[e.a];
        const B = layout.cells[e.b];
        ctx.strokeStyle = pal.voice(INSTRUMENTS[e.a].family === "exact" ? 0 : 1, 0.45);
        ctx.beginPath(); ctx.moveTo(A.x, A.y); ctx.lineTo(B.x, B.y); ctx.stroke();
      }
      ctx.font = "11px ui-monospace, monospace";
      layout.cells.forEach((c, i) => {
        const it = INSTRUMENTS[i];
        ctx.strokeStyle = pal.voice(it.family === "exact" ? 0 : 1, i === atlasState.hit ? 1 : 0.8);
        ctx.lineWidth = i === atlasState.hit ? 2.5 : 1.4;
        ctx.strokeRect(c.x - c.half, c.y - c.half, c.side, c.side);
        ctx.fillStyle = pal.ink2 || pal.ink;
        ctx.textAlign = "center";
        ctx.fillText(it.name, c.x, c.y + c.half + 14, Math.max(c.labelW, c.side));
        ctx.textAlign = "start";
      });
    },
  });
  canvas.addEventListener("pointerdown", (ev) => {
    if (!atlasState.layout) return;
    const r = canvas.getBoundingClientRect();
    atlasState.hit = hitTest(atlasState.layout, ev.clientX - r.left, ev.clientY - r.top);
    paintAtlasReadout();
    handle.invalidate();
  });
  paintAtlasReadout();
}

/* ---------- Reading: the article answers how it is read (Eido D6) ---------- */

function initReading() {
  loadCondensed("condensed.json").then((data) => {
    if (!data) return setupReadingWeave();
    const reading = setupReadingWeave({ motion: false, panel: false });
    if (reading) setupCondense(data, reading, { noun: "page" });
    return undefined;
  }).catch(() => setupReadingWeave());
}

/* ---------- Boot ---------- */

initFrame();
initQuotient();
initSlits();
initScale();
initAtlas();
initReading();
paintMedium();
if (!reduced()) {
  let lastPaint = 0;
  onFrame((now) => {
    if (now - lastPaint > 500) { lastPaint = now; paintMedium(); }
  });
}

