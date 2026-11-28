// Checks for the pure instrument math in site/assets/continuum-math.js.
// Oracles are independent of the implementation where it matters: the
// cross-ratio of the starting points is the rational 5/4, the Englert
// pair at gamma = 1/2 is the 3-4-5 pair (0.6, 0.8), the Sorkin scaling
// exponents are exact homogeneity degrees, and block-averaging
// attenuation is the closed-form Dirichlet factor applied to a pure
// mode built inside the test.
import { test } from "node:test";
import assert from "node:assert/strict";
import {
  PROBE_POINTS, crossRatio, mobius,
  visibility, sorkin, twoSlitIntensity, slitIntensity,
  FIELD, fieldValues, diffusionStep, blockAverage, modeAmplitude,
  blockAttenuation, emergence,
} from "../site/assets/continuum-math.js";

const near = (a, b, tol, msg) => assert.ok(Math.abs(a - b) <= tol, `${msg}: got ${a}, want ${b} ± ${tol}`);

test("cross-ratio of the starting points is exactly 5/4", () => {
  assert.equal(crossRatio(PROBE_POINTS), 5 / 4);
});

test("cross-ratio survives projective probes while coordinates move", () => {
  const probes = [
    { alpha: 2, beta: 1, gamma: 0.3 },
    { alpha: 0.5, beta: -2, gamma: -0.1 },
    { alpha: 3, beta: 0.25, gamma: 0.05 },
    { alpha: 1, beta: 0, gamma: 0 },
    { alpha: -1.5, beta: 4, gamma: 0.12 },
  ];
  for (const p of probes) {
    const ys = PROBE_POINTS.map((x) => mobius(x, p));
    near(crossRatio(ys), 5 / 4, 1e-12, `probe ${JSON.stringify(p)}`);
  }
  // The identity probe changes nothing.
  assert.deepEqual(PROBE_POINTS.map((x) => mobius(x)), [...PROBE_POINTS]);
});

test("visibility: V^2 + D^2 = 1, with the 3-4-5 pair at gamma = 1/2", () => {
  const { V, D } = visibility(0.5);
  assert.equal(V, 0.6);
  assert.equal(D, 0.8);
  for (const g of [0, 0.1, 0.25, 0.7, 1, 1.5, 3]) {
    const v = visibility(g);
    near(v.V * v.V + v.D * v.D, 1, 1e-12, `gamma=${g}`);
  }
  assert.equal(visibility(0).V, 1);
  assert.equal(visibility(1).V, 0);
});

test("two-slit fringes wash out as the probe coupling grows", () => {
  const peak = (p) => Math.max(...p);
  const trough = (p) => Math.min(...p.slice(100, 141)); // near centre
  const bare = twoSlitIntensity(0);
  const probed = twoSlitIntensity(1);
  assert.ok(peak(bare) > peak(probed), "coupled probe lowers the fringe peak");
  assert.ok(trough(probed) >= trough(bare), "coupled probe fills the troughs");
});

test("Sorkin I_ABC is zero in the linear regime, including at zero coupling", () => {
  assert.ok(sorkin({ mode: "linear" }).intI3 < 1e-9);
  assert.ok(sorkin({ mode: "looped", g: 0 }).intI3 < 1e-9);
  assert.ok(sorkin({ mode: "kerr", eta: 0 }).intI3 < 1e-9);
});

test("looped coupling: I_ABC scales as lambda^2 and kappa3 is intensity-invariant", () => {
  const a = sorkin({ mode: "looped", g: 0.35, lambda: 1 });
  const b = sorkin({ mode: "looped", g: 0.35, lambda: 2 });
  const c = sorkin({ mode: "looped", g: 0.35, lambda: 3 });
  assert.ok(a.intI3 > 0.1, "looped I_ABC is genuinely nonzero");
  near(b.intI3 / a.intI3, 4, 1e-9, "lambda=2 integral ratio");
  near(c.intI3 / a.intI3, 9, 1e-9, "lambda=3 integral ratio");
  near(b.kappa3 / a.kappa3, 1, 1e-9, "kappa3 invariant");
  near(c.kappa3 / a.kappa3, 1, 1e-9, "kappa3 invariant at lambda=3");
});

test("Kerr term: I_ABC scales as lambda^4 and kappa3 grows with intensity", () => {
  const a = sorkin({ mode: "kerr", eta: 0.05, lambda: 1 });
  const b = sorkin({ mode: "kerr", eta: 0.05, lambda: 2 });
  const c = sorkin({ mode: "kerr", eta: 0.05, lambda: 3 });
  assert.ok(a.intI3 > 0.01, "Kerr I_ABC is genuinely nonzero");
  near(b.intI3 / a.intI3, 16, 1e-6, "lambda=2 integral ratio is lambda^4");
  near(c.intI3 / a.intI3, 81, 1e-5, "lambda=3 integral ratio is lambda^4");
  assert.ok(b.kappa3 > a.kappa3 && c.kappa3 > b.kappa3, "kappa3 grows with intensity");
});

test("single-slit intensities are nonnegative and the full sum peaks at centre", () => {
  const p = slitIntensity(7, { mode: "linear" });
  assert.ok([...p].every((v) => v >= 0));
  const mid = Math.floor(p.length / 2);
  assert.equal(Math.max(...p), p[mid]);
});

test("block averaging attenuates a pure mode by the closed-form factor", () => {
  const N = FIELD.N;
  for (const [b, p, q] of [[2, 2, 1], [4, 2, 1], [3, 4, 2], [6, 3, 0], [4, 5, 3]]) {
    const g = new Float64Array(N * N);
    for (let i = 0; i < N; i += 1) {
      for (let j = 0; j < N; j += 1) {
        const t = (2 * Math.PI * (p * i + q * j)) / N;
        g[i * N + j] = Math.cos(t) + 0.7 * Math.sin(t);
      }
    }
    const before = modeAmplitude(g, N, p, q);
    const after = modeAmplitude(blockAverage(g, N, b), N / b, p, q);
    near(after / before, blockAttenuation(N, b, p, q), 1e-9, `b=${b} mode (${p},${q})`);
  }
});

test("emergence defect: exact at b=1, positive after, much smaller with renormalised nu", () => {
  assert.equal(emergence(1).delta, 0);
  assert.equal(emergence(1).deltaScaled, 0);
  for (const b of [4, 8, 12]) {
    const e = emergence(b);
    assert.ok(e.delta > 0.1, `b=${b} naive defect is large (got ${e.delta})`);
    assert.ok(e.deltaScaled < e.delta / 5, `b=${b} renormalised defect ${e.deltaScaled} << ${e.delta}`);
    assert.ok(e.deltaScaled < 0.05, `b=${b} renormalised defect is small`);
  }
});

test("coarse-graining keeps the long mode and kills the short one", () => {
  const e = emergence(4);
  assert.ok(e.lowAfter / e.lowBefore > 0.7, `low mode survives (${e.lowAfter}/${e.lowBefore})`);
  assert.ok(e.highAfter / e.highBefore < 0.1, `high mode dies (${e.highAfter}/${e.highBefore})`);
  assert.ok(e.varAfter < e.varBefore, "variance does not grow under averaging");
});

test("the field and its diffusion are deterministic", () => {
  assert.deepEqual([...fieldValues()], [...fieldValues()]);
  assert.deepEqual([...diffusionStep(fieldValues(), FIELD.N)], [...diffusionStep(fieldValues(), FIELD.N)]);
  assert.throws(() => blockAverage(fieldValues(), FIELD.N, 5), /does not divide/);
});
