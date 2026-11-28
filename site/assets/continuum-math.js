// The pure half of the continuum instruments: no DOM, so every number the
// page prints can be checked in Node (test/continuum-math.test.mjs).
//
// Three instruments, one per claim the page makes checkable:
//
//   1. The observer quotient. Four points on a line, seen through a
//      projective probe (a Mobius map). Every coordinate moves when the
//      probe is twisted; the cross-ratio does not. This is the same
//      PGL(2) invariance the synthesis report uses for its exact
//      cross-ratio invariants, drawn with points anyone can drag a
//      probe across.
//
//   2. Slits. A Fraunhofer sum over open slits. In the linear regime the
//      Sorkin triple-slit combination I_ABC is zero identically. It
//      becomes nonzero two different ways: slit-to-slit looped coupling
//      (still linear in the source, so its size scales as lambda^2 and
//      the normalised kappa_3 is intensity-invariant) and a quartic
//      Kerr term in the detection rule (whose I_ABC scales as lambda^4,
//      so kappa_3 grows with intensity). Two-slit mode draws the
//      probe-coupling formulas V(gamma) and D(gamma) from the
//      double-slit report (AUDIT-054, regime I, pure bath).
//
//   3. Coarse-graining. A fixed deterministic field, one diffusion step
//      T, and block averaging pi_b. The page prints the commutation
//      defect delta_emg(b) = ||pi(T f) - T'(pi f)|| / ||pi(T f)|| and
//      the survival of two Fourier modes under pi_b. Block averaging
//      attenuates a mode by a known sinc factor, which the tests use
//      as an independent oracle.
//
// Everything here is floating-point illustration of claims whose exact
// rational forms live in the repository's Python instruments. The page
// says so beside each figure; the identities that must hold exactly
// (I_ABC = 0 in the linear regime, cross-ratio invariance, scaling
// exponents) are asserted in the tests to floating-point tolerance.

/* ------------------------------------------------------------------ */
/* 1. Cross-ratio under a projective probe                            */
/* ------------------------------------------------------------------ */

/** The four collinear points the instrument starts from. Their cross-ratio is 5/4. */
export const PROBE_POINTS = Object.freeze([0, 1, 3, 6]);

/** Cross-ratio (A, B; C, D) = ((C - A)(D - B)) / ((C - B)(D - A)). */
export function crossRatio([a, b, c, d]) {
  return ((c - a) * (d - b)) / ((c - b) * (d - a));
}

/** A Mobius probe phi(x) = (alpha x + beta) / (gamma x + 1). */
export function mobius(x, { alpha = 1, beta = 0, gamma = 0 } = {}) {
  const den = gamma * x + 1;
  if (Math.abs(den) < 1e-12) return NaN;
  return (alpha * x + beta) / den;
}

/* ------------------------------------------------------------------ */
/* 2. Slits                                                           */
/* ------------------------------------------------------------------ */

export const SLITS = Object.freeze({
  N: 241, // screen samples on u in [-1, 1]
  F: 6, // fringe frequency (cycles across the half-screen per unit slit offset)
  POS: Object.freeze([-1, 0, 1]),
  ENV: 0.85, // Gaussian envelope width
  LOOP_PHASE: 0.7, // looped-coupling phase per unit slit separation
});

export const screenU = (i, n = SLITS.N) => -1 + (2 * i) / (n - 1);

/** Englert pair for a pure probe bath: V = (1 - g^2)/(1 + g^2), D = 2g/(1 + g^2), so V^2 + D^2 = 1. */
export function visibility(gamma) {
  const d = 1 + gamma * gamma;
  return { V: (1 - gamma * gamma) / d, D: (2 * gamma) / d };
}

// Complex helpers on [re, im] pairs.
const cadd = (a, b) => [a[0] + b[0], a[1] + b[1]];
const cmul = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
const cscale = (a, s) => [a[0] * s, a[1] * s];

/** Unit-source field of slit j at screen position u. */
function slitField(j, u) {
  const env = Math.exp(-((u / SLITS.ENV) ** 2));
  const ph = 2 * Math.PI * SLITS.F * u * SLITS.POS[j];
  return [env * Math.cos(ph), env * Math.sin(ph)];
}

/** Solve a small complex linear system by Gaussian elimination. A: n x n of [re, im]. */
function solveComplex(A, b) {
  const n = b.length;
  const M = A.map((row, i) => [...row.map((z) => [...z]), [...b[i]]]);
  for (let col = 0; col < n; col += 1) {
    let piv = col;
    for (let r = col + 1; r < n; r += 1) {
      if (Math.hypot(...M[r][col]) > Math.hypot(...M[piv][col])) piv = r;
    }
    [M[col], M[piv]] = [M[piv], M[col]];
    const p = M[col][col];
    const pd = p[0] * p[0] + p[1] * p[1];
    for (let r = 0; r < n; r += 1) {
      if (r === col) continue;
      const f = M[r][col];
      const q = [(f[0] * p[0] + f[1] * p[1]) / pd, (f[1] * p[0] - f[0] * p[1]) / pd];
      for (let c = col; c <= n; c += 1) {
        const sub = cmul(q, M[col][c]);
        M[r][c] = [M[r][c][0] - sub[0], M[r][c][1] - sub[1]];
      }
    }
  }
  return M.map((row, i) => {
    const p = row[i];
    const pd = p[0] * p[0] + p[1] * p[1];
    const v = row[n];
    return [(v[0] * p[0] + v[1] * p[1]) / pd, (v[1] * p[0] - v[0] * p[1]) / pd];
  });
}

/**
 * Slit amplitudes a_j for the open set `mask` (bits over POS), with source
 * strength `lambda`. Linear and Kerr modes ignore coupling; looped mode
 * solves (I - g M_S) a = lambda * 1_S, M_jk = exp(i * phase * |j - k|)
 * off-diagonal, which makes the response nonlinear in the mask while
 * staying linear (homogeneous of degree 2 in intensity) in lambda.
 */
export function slitAmplitudes(mask, { mode = "linear", g = 0, lambda = 1 } = {}) {
  const open = [0, 1, 2].filter((j) => mask & (1 << j));
  const a = [[0, 0], [0, 0], [0, 0]];
  if (!open.length) return a;
  if (mode !== "looped" || g === 0) {
    for (const j of open) a[j] = [lambda, 0];
    return a;
  }
  const A = open.map((j) =>
    open.map((k) => {
      if (j === k) return [1, 0];
      const ph = SLITS.LOOP_PHASE * Math.abs(j - k);
      return [-g * Math.cos(ph), -g * Math.sin(ph)];
    }),
  );
  const sol = solveComplex(A, open.map(() => [lambda, 0]));
  open.forEach((j, i) => { a[j] = sol[i]; });
  return a;
}

/** Intensity P_S(u) for one open set, sampled on the screen grid. */
export function slitIntensity(mask, { mode = "linear", g = 0, eta = 0, lambda = 1 } = {}) {
  const a = slitAmplitudes(mask, { mode, g, lambda });
  const out = new Float64Array(SLITS.N);
  for (let i = 0; i < SLITS.N; i += 1) {
    const u = screenU(i);
    let psi = [0, 0];
    for (let j = 0; j < 3; j += 1) {
      if (a[j][0] === 0 && a[j][1] === 0) continue;
      psi = cadd(psi, cmul(a[j], slitField(j, u)));
    }
    const p2 = psi[0] * psi[0] + psi[1] * psi[1];
    out[i] = mode === "kerr" ? p2 + eta * p2 * p2 : p2;
  }
  return out;
}

/** Two-slit intensity with probe coupling gamma damping the cross term by V(gamma). */
export function twoSlitIntensity(gamma, { lambda = 1 } = {}) {
  const { V } = visibility(gamma);
  const out = new Float64Array(SLITS.N);
  for (let i = 0; i < SLITS.N; i += 1) {
    const u = screenU(i);
    const A = cscale(slitField(0, u), lambda);
    const B = cscale(slitField(2, u), lambda);
    const cross = 2 * (A[0] * B[0] + A[1] * B[1]); // 2 Re(A* B)
    out[i] = A[0] ** 2 + A[1] ** 2 + B[0] ** 2 + B[1] ** 2 + V * cross;
  }
  return out;
}

/**
 * The Sorkin combination over all seven non-empty masks, plus summaries.
 * kappa3 = sum_u |I_ABC| / sum_u (|I_AB| + |I_AC| + |I_BC|), with the
 * pairwise combinations I_XY = P_XY - P_X - P_Y.
 */
export function sorkin({ mode = "linear", g = 0, eta = 0, lambda = 1 } = {}) {
  const opts = { mode, g, eta, lambda };
  const P = {};
  for (let mask = 1; mask <= 7; mask += 1) P[mask] = slitIntensity(mask, opts);
  const I3 = new Float64Array(SLITS.N);
  let intI3 = 0;
  let intPairs = 0;
  let maxP = 0;
  for (let i = 0; i < SLITS.N; i += 1) {
    I3[i] = P[7][i] - P[3][i] - P[5][i] - P[6][i] + P[1][i] + P[2][i] + P[4][i];
    intI3 += Math.abs(I3[i]);
    intPairs +=
      Math.abs(P[3][i] - P[1][i] - P[2][i]) +
      Math.abs(P[5][i] - P[1][i] - P[4][i]) +
      Math.abs(P[6][i] - P[2][i] - P[4][i]);
    if (P[7][i] > maxP) maxP = P[7][i];
  }
  const du = 2 / (SLITS.N - 1);
  return {
    Pabc: P[7],
    I3,
    intI3: intI3 * du,
    intPairs: intPairs * du,
    kappa3: intPairs > 0 ? intI3 / intPairs : 0,
    maxP,
  };
}

/* ------------------------------------------------------------------ */
/* 3. Coarse-graining and the emergence defect                        */
/* ------------------------------------------------------------------ */

export const FIELD = Object.freeze({
  N: 48, // grid is N x N, periodic
  NU: 0.18, // diffusion step size (stable: NU <= 1/4)
  LOW: Object.freeze([2, 1]), // a long-wavelength mode that should survive
  HIGH: Object.freeze([11, 9]), // a short-wavelength mode that should die
  BLOCKS: Object.freeze([1, 2, 3, 4, 6, 8, 12]),
});

/** The fixed field f on the unit torus, sampled on the N x N grid. Same numbers every run. */
export function fieldValues() {
  const { N, LOW, HIGH } = FIELD;
  const f = new Float64Array(N * N);
  for (let i = 0; i < N; i += 1) {
    for (let j = 0; j < N; j += 1) {
      const x = i / N;
      const y = j / N;
      const dx = Math.min(Math.abs(x - 0.62), 1 - Math.abs(x - 0.62));
      const dy = Math.min(Math.abs(y - 0.38), 1 - Math.abs(y - 0.38));
      f[i * N + j] =
        0.6 * Math.sin(2 * Math.PI * (LOW[0] * x + LOW[1] * y)) +
        0.4 * Math.cos(2 * Math.PI * (3 * y - x)) +
        1.2 * Math.exp(-(dx * dx + dy * dy) / 0.02) +
        0.35 * Math.sin(2 * Math.PI * HIGH[0] * x) * Math.sin(2 * Math.PI * HIGH[1] * y) +
        0.2 * ((i + j) % 2 === 0 ? 1 : -1);
    }
  }
  return f;
}

/** One periodic 5-point diffusion step on an n x n grid. */
export function diffusionStep(f, n, nu = FIELD.NU) {
  const out = new Float64Array(f.length);
  for (let i = 0; i < n; i += 1) {
    for (let j = 0; j < n; j += 1) {
      const c = f[i * n + j];
      const lap =
        f[((i + 1) % n) * n + j] + f[((i + n - 1) % n) * n + j] +
        f[i * n + ((j + 1) % n)] + f[i * n + ((j + n - 1) % n)] - 4 * c;
      out[i * n + j] = c + nu * lap;
    }
  }
  return out;
}

/** Block averaging pi_b: n x n down to (n/b) x (n/b). b must divide n. */
export function blockAverage(f, n, b) {
  if (n % b !== 0) throw new Error(`block ${b} does not divide ${n}`);
  const m = n / b;
  const out = new Float64Array(m * m);
  for (let i = 0; i < m; i += 1) {
    for (let j = 0; j < m; j += 1) {
      let s = 0;
      for (let di = 0; di < b; di += 1) for (let dj = 0; dj < b; dj += 1) s += f[(i * b + di) * n + (j * b + dj)];
      out[i * m + j] = s / (b * b);
    }
  }
  return out;
}

/** Piecewise-constant lift of a coarse grid back to n x n (for display and mode projection). */
export function liftBlocks(coarse, m, b) {
  const n = m * b;
  const out = new Float64Array(n * n);
  for (let i = 0; i < n; i += 1) for (let j = 0; j < n; j += 1) out[i * n + j] = coarse[Math.floor(i / b) * m + Math.floor(j / b)];
  return out;
}

/** Amplitude of Fourier mode (p, q): sqrt of summed sine/cosine projection power, on an n x n grid. */
export function modeAmplitude(f, n, p, q) {
  let cc = 0, cs = 0, sc = 0, ss = 0;
  for (let i = 0; i < n; i += 1) {
    for (let j = 0; j < n; j += 1) {
      const v = f[i * n + j];
      const ax = (2 * Math.PI * p * i) / n;
      const ay = (2 * Math.PI * q * j) / n;
      cc += v * Math.cos(ax) * Math.cos(ay);
      cs += v * Math.cos(ax) * Math.sin(ay);
      sc += v * Math.sin(ax) * Math.cos(ay);
      ss += v * Math.sin(ax) * Math.sin(ay);
    }
  }
  return (2 / (n * n)) * Math.sqrt(cc * cc + cs * cs + sc * sc + ss * ss);
}

/**
 * Expected attenuation of mode (p, q) under b x b block averaging on an
 * n x n grid: the product of Dirichlet-kernel factors
 * |sin(pi p b / n)| / (b |sin(pi p / n)|) in each direction, with the
 * p = 0 factor equal to 1. This closed form is the tests' oracle.
 */
export function blockAttenuation(n, b, p, q) {
  const dir = (k) => {
    if (k === 0) return 1;
    return Math.abs(Math.sin((Math.PI * k * b) / n)) / (b * Math.abs(Math.sin((Math.PI * k) / n)));
  };
  return dir(p) * dir(q);
}

const norm2 = (f) => Math.sqrt([...f].reduce((s, v) => s + v * v, 0));

/**
 * delta_emg(b) = || pi_b(T f) - T'(pi_b f) || / || pi_b(T f) ||, where T
 * and T' are the same diffusion stencil on the fine and coarse grids.
 * Also returns the coarse field and the two tracked mode amplitudes
 * before and after coarse-graining (projected on the lifted field).
 */
export function emergence(b) {
  const { N, LOW, HIGH } = FIELD;
  const f = fieldValues();
  const Tf = diffusionStep(f, N);
  const piTf = blockAverage(Tf, N, b);
  const pif = blockAverage(f, N, b);
  const m = N / b;
  const TpiF = diffusionStep(pif, m);
  const diff = piTf.map((v, i) => v - TpiF[i]);
  // The same coarse stencil with the renormalised step nu / b^2: diffusion
  // over one coarse cell of width b*h in the same time step. Whether a
  // level commutes depends on finding the right macro dynamics, and the
  // page prints both defects so the difference is visible, not asserted.
  const TpiFScaled = diffusionStep(pif, m, FIELD.NU / (b * b));
  const diffScaled = piTf.map((v, i) => v - TpiFScaled[i]);
  const lifted = liftBlocks(pif, m, b);
  const mean = (g) => [...g].reduce((s, v) => s + v, 0) / g.length;
  const variance = (g) => {
    const mu = mean(g);
    return [...g].reduce((s, v) => s + (v - mu) ** 2, 0) / g.length;
  };
  return {
    b,
    m,
    delta: norm2(diff) / norm2(piTf),
    deltaScaled: norm2(diffScaled) / norm2(piTf),
    coarse: pif,
    lowBefore: modeAmplitude(f, N, LOW[0], LOW[1]),
    lowAfter: modeAmplitude(lifted, N, LOW[0], LOW[1]),
    highBefore: modeAmplitude(f, N, HIGH[0], HIGH[1]),
    highAfter: modeAmplitude(lifted, N, HIGH[0], HIGH[1]),
    varBefore: variance(f),
    varAfter: variance(lifted),
  };
}
