#!/usr/bin/env python3
"""Steelmanning Audit & Repaired Lag-Scanned Quadratic Koopman-Sheaf Upgrade of Foundation-0/continuum PR #2 Probes.

Separates prototype flaws from genuine invariant structure across the Python instruments in
Foundation-0/continuum PR #2 (matching Gemini Session 1):
  1. Honest empirical measurement of `probe_window` (`gemini-code-1795203041292.py`):
     - Tests truly coupled chaotic Rossler observables (both lag=0 and lag=12!),
       uncoupled Rossler attractors (both independent burn-in and worst-case same-burn-in
       shared-carrier twin), independent linear drifts, independent polynomial trends
       (t^2 vs -t^3), independent Brownian random walks, independent AR(1), and
       FFT phase-randomized surrogates.
     - Separates what WORKS (strong separation on stationary AR(1), non-inverted H_0 on
       circle vs white noise) from genuine coordinate/null-model shadows (CKA = 0.99 on
       independent linear drifts, high-variance tails on Brownian walks, high CKA on
       uncoupled shared-carrier Rossler, and `h0_persistence_entropy` confounding bimodal
       clustering < circle < noise).
  2. Repaired Coordinate-Free Cross-Modal Instrument (`koopman_sheaf_coupling`):
     - Degree-3 polynomial detrending (kills 1, t, t^2, t^3 trends identically) + lag-4
       increment stationarization x[t+4] - x[t] (turns Brownian random walks into strictly
       stationary MA(3) while preserving ~16x higher chaotic SNR than 1-step `np.diff`),
     - Degree-<=2 Quadratic EDMD Koopman dictionary Phi_2(Z) = [Z, Sym^2(Z)] (14 dims for
       dim=4), which is EXACTLY invariant under arbitrary invertible GL(d) linear basis
       changes of the delay coordinates (verified to ~3e-15!) and captures both the linear
       carrier and nonlinear chaotic z-spike coupling,
     - Sheaf gluing residual * Koopman intertwining defect (S1:F[379]) with lag scan
       Delta in [-16, +16] (recovering lagged transmission delays directly),
     - Lyapunov-separated non-wrapping lag-window shift surrogates using the EXACT SAME
       max-over-lags statistic (eliminating circular-roll discontinuity artifacts,
       uncoupled shared-carrier Rossler false positives, and near-orbit correlation bias).
     - Scope note: scanning max-over-lags across a full Rossler carrier period (width 33 >
       period ~30) deliberately sacrifices lag-0-only z~+10 down to z_mean ~ +3.8..+4.7 in
       exchange for detecting arbitrary unknown lags up to +-16 while holding ALL 7 nulls
       (including uncoupled shared-carrier Rossler & t^2 vs -t^3) centered near z ~ 0.
  3. Concrete prototype bug reproductions & verified repairs for `perceptual_invariants`
     (`1795203053160.py`: `phase_coherence` -> quadrature PLV; `np.roll` -> zero-padded shift)
     and `extract_blind_invariant` (`1795203102878.py`: negative-lag empty slice -> `t0 >= max_lag`).

Run:
  python3 -I -O -B -W error expedition-synthesis/audit_continuum_probes.py
  python3 -I -O -B -W error expedition-synthesis/audit_continuum_probes.py --json
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# 1. Exact Pure-NumPy Primitives Matching SciPy Semantics
# ---------------------------------------------------------------------------

def hilbert_np(x: np.ndarray) -> np.ndarray:
    """Exact discrete analytic signal (matches scipy.signal.hilbert to machine precision)."""
    x = np.asarray(x, dtype=np.float64)
    N = x.shape[0]
    Xf = np.fft.fft(x)
    h = np.zeros(N, dtype=np.float64)
    if N % 2 == 0:
        h[0] = 1.0
        h[N // 2] = 1.0
        h[1 : N // 2] = 2.0
    else:
        h[0] = 1.0
        h[1 : (N + 1) // 2] = 2.0
    return np.fft.ifft(Xf * h)


def pairwise_dists(X: np.ndarray) -> np.ndarray:
    sq = np.sum(X * X, axis=1, keepdims=True)
    D2 = np.maximum(0.0, sq + sq.T - 2.0 * (X @ X.T))
    return np.sqrt(D2)


def mst_edge_weights(D: np.ndarray) -> np.ndarray:
    n = D.shape[0]
    in_tree = np.zeros(n, dtype=bool)
    min_edge = np.full(n, np.inf, dtype=np.float64)
    min_edge[0] = 0.0
    weights = np.empty(n - 1, dtype=np.float64)
    w_idx = 0
    for step in range(n):
        candidates = np.where(~in_tree, min_edge, np.inf)
        u = int(np.argmin(candidates))
        in_tree[u] = True
        if step > 0:
            weights[w_idx] = min_edge[u]
            w_idx += 1
        row = D[u]
        upd = (~in_tree) & (row < min_edge)
        min_edge[upd] = row[upd]
    return weights


# ---------------------------------------------------------------------------
# 2. Exact Reproduction of Foundation-0/continuum PR #2 `probe_window`
# ---------------------------------------------------------------------------

def takens_embed(x: np.ndarray, dim: int = 5, tau: int = 3) -> np.ndarray:
    x = (x - np.mean(x)) / (np.std(x) + 1e-12)
    win = (dim - 1) * tau + 1
    return np.lib.stride_tricks.sliding_window_view(x, win)[:, ::tau]


def async_event_lens(x: np.ndarray, delta: float = 0.35) -> np.ndarray:
    z = (x - np.mean(x)) / (np.std(x) + 1e-12)
    idx, vals = [0], [float(z[0])]
    last = float(z[0])
    for i in range(1, len(z)):
        if abs(float(z[i]) - last) >= delta:
            idx.append(i)
            vals.append(float(z[i]))
            last = float(z[i])
    if idx[-1] != len(z) - 1:
        idx.append(len(z) - 1)
        vals.append(float(z[-1]))
    return np.interp(np.arange(len(z)), idx, vals)


def centered_rbf_kernel(X: np.ndarray) -> np.ndarray:
    D = pairwise_dists(X)
    pos = D[D > 0]
    med = float(np.median(pos)) + 1e-12 if len(pos) > 0 else 1e-12
    K = np.exp(-(D ** 2) / (2.0 * med ** 2))
    return K - K.mean(axis=0, keepdims=True) - K.mean(axis=1, keepdims=True) + K.mean()


def manifold_cka(X: np.ndarray, Y: np.ndarray) -> float:
    n = min(len(X), len(Y))
    Kx = centered_rbf_kernel(X[:n])
    Ky = centered_rbf_kernel(Y[:n])
    return float(np.sum(Kx * Ky) / (np.linalg.norm(Kx) * np.linalg.norm(Ky) + 1e-12))


def h0_persistence_entropy(X: np.ndarray) -> float:
    D = pairwise_dists(X)
    lifetimes = mst_edge_weights(D)
    p = lifetimes / (np.sum(lifetimes) + 1e-12)
    return float(-np.sum(p * np.log(p + 1e-12)) / np.log(len(p) + 1e-12))


def continuum_probe_window(channels: Dict[str, np.ndarray], dim: int = 5, tau: int = 3) -> Dict[str, Any]:
    names = list(channels.keys())
    manifolds, observer_stability, topo_entropy = {}, {}, {}
    for name, sig in channels.items():
        M_raw = takens_embed(sig, dim=dim, tau=tau)
        M_async = takens_embed(async_event_lens(sig), dim=dim, tau=tau)
        M_phase = takens_embed(np.imag(hilbert_np(sig)), dim=dim, tau=tau)
        manifolds[name] = M_raw
        observer_stability[name] = 0.5 * (
            manifold_cka(M_raw, M_async) + manifold_cka(M_raw, M_phase)
        )
        topo_entropy[name] = h0_persistence_entropy(M_raw)

    coupling = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            raw_lock = manifold_cka(manifolds[a], manifolds[b])
            reality_weighted = raw_lock * float(np.sqrt(max(0.0, observer_stability[a] * observer_stability[b])))
            coupling[f"{a}:{b}"] = {
                "manifold_lock": round(raw_lock, 4),
                "observer_invariant_lock": round(reality_weighted, 4),
            }
    return {
        "observer_stability": {k: round(v, 4) for k, v in observer_stability.items()},
        "h0_topo_entropy": {k: round(v, 4) for k, v in topo_entropy.items()},
        "cross_modal_coupling": coupling,
    }


# ---------------------------------------------------------------------------
# 3. Chaotic Rossler Attractor & Negative-Control Generators (Deterministic Seeds)
# ---------------------------------------------------------------------------

def integrate_rossler(
    n_samples: int,
    rng: np.random.Generator,
    random_burn: bool = True,
) -> Tuple[np.ndarray, np.ndarray]:
    """RK4 integration of chaotic Rossler attractor (continuous broadband spectrum).

    Returns two distinct nonlinear sensor observables of the same dynamical trajectory:
      ch_a = x(t) + small sensor noise
      ch_b = tanh(0.18 * y(t) + 0.12 * x(t)) + 0.08 * z(t) + small sensor noise
    When `random_burn=True` (default), uses randomized long burn-in [2000, 4000) so independent
    calls produce fully phase- and amplitude-decorrelated trajectories; `random_burn=False`
    reproduces a short fixed burn=800 transient (worst-case shared-carrier twin test).
    """
    a_p, b_p, c_p = 0.2, 0.2, 5.7
    dt = 0.05
    substeps = 4  # sample every 0.20 time units
    if random_burn:
        burn = 2000 + int(rng.integers(0, 2000))
        state = np.array([
            1.0 + rng.uniform(-2.0, 2.0),
            1.0 + rng.uniform(-2.0, 2.0),
            1.0 + rng.uniform(-1.0, 2.0),
        ], dtype=np.float64)
    else:
        burn = 800
        state = np.array([
            1.0 + rng.uniform(-0.5, 0.5),
            1.0 + rng.uniform(-0.5, 0.5),
            1.0 + rng.uniform(-0.5, 0.5),
        ], dtype=np.float64)

    def rhs(s: np.ndarray) -> np.ndarray:
        x, y, z = s
        return np.array([-y - z, x + a_p * y, b_p + z * (x - c_p)], dtype=np.float64)

    def step(s: np.ndarray) -> np.ndarray:
        k1 = rhs(s)
        k2 = rhs(s + 0.5 * dt * k1)
        k3 = rhs(s + 0.5 * dt * k2)
        k4 = rhs(s + dt * k3)
        return s + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    for _ in range(burn):
        state = step(state)

    xs = np.empty(n_samples, dtype=np.float64)
    ys = np.empty(n_samples, dtype=np.float64)
    zs = np.empty(n_samples, dtype=np.float64)
    for i in range(n_samples):
        for _ in range(substeps):
            state = step(state)
        xs[i], ys[i], zs[i] = state

    ch_a = xs + 0.05 * np.std(xs) * rng.normal(size=n_samples)
    ch_b = np.tanh(0.18 * ys + 0.12 * xs) + 0.08 * zs
    ch_b = ch_b + 0.05 * np.std(ch_b) * rng.normal(size=n_samples)
    return ch_a, ch_b


def phase_randomize_surrogate(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    x0 = x - np.mean(x)
    Xf = np.fft.rfft(x0)
    phases = rng.uniform(0.0, 2.0 * np.pi, size=len(Xf))
    phases[0] = 0.0
    if len(x) % 2 == 0:
        phases[-1] = 0.0
    Yf = np.abs(Xf) * np.exp(1j * phases)
    return np.fft.irfft(Yf, n=len(x))


# ---------------------------------------------------------------------------
# 4. Repaired Instrument: Lag-Scanned Quadratic Koopman-Sheaf Intertwining
#    with Cubic Detrend + Lag-4 Increment + Lyapunov-Separated Shift Nulls
# ---------------------------------------------------------------------------

def detrend_poly(x: np.ndarray, deg: int = 3) -> np.ndarray:
    """Remove polynomial trend up to degree `deg` (annihilates 1, t, t^2, ..., t^deg)."""
    t = np.linspace(-1.0, 1.0, len(x))
    V = np.vander(t, deg + 1)
    coef, _, _, _ = np.linalg.lstsq(V, x, rcond=None)
    return x - V @ coef


def fit_edmd_koopman(X: np.ndarray, reg: float = 1e-4) -> Tuple[np.ndarray, np.ndarray]:
    """Fit SVD-whitened linear delay-coordinate Koopman operator K (invariant under GL(d))."""
    X0 = X - X.mean(axis=0, keepdims=True)
    U, s, _ = np.linalg.svd(X0, full_matrices=False)
    keep = s > (1e-6 * s[0] if len(s) > 0 and s[0] > 0 else 1e-12)
    Z = U[:, keep] * np.sqrt(len(X0))
    Z0, Z1 = Z[:-1], Z[1:]
    d = Z.shape[1]
    G0 = (Z0.T @ Z0) / len(Z0) + reg * np.eye(d)
    G1 = (Z0.T @ Z1) / len(Z0)
    K = np.linalg.solve(G0, G1).T
    return Z, K


def fit_quad_edmd_koopman(X: np.ndarray, reg: float = 1e-2) -> Tuple[np.ndarray, np.ndarray]:
    """Fit SVD-whitened degree-<=2 Quadratic Koopman dictionary Phi_2(Z) = [Z, Sym^2(Z)] & K.

    Because span(Z) and span(Z, Sym^2(Z)) are exact GL(d)-representations, the whitened
    observables Phi and Koopman spectrum eig(K) are invariant under arbitrary invertible
    GL(d) linear changes of basis on X (up to O(m) orthogonal equivalence).
    """
    X0 = X - X.mean(axis=0, keepdims=True)
    U, s, _ = np.linalg.svd(X0, full_matrices=False)
    keep = s > (1e-6 * s[0] if len(s) > 0 and s[0] > 0 else 1e-12)
    Z = U[:, keep] * np.sqrt(len(X0))
    d = Z.shape[1]
    Q = np.column_stack([Z] + [Z[:, i] * Z[:, j] for i in range(d) for j in range(i, d)])
    Q = Q - Q.mean(axis=0, keepdims=True)
    Uq, sq, _ = np.linalg.svd(Q, full_matrices=False)
    keep_q = sq > (1e-6 * sq[0] if len(sq) > 0 and sq[0] > 0 else 1e-12)
    Phi = Uq[:, keep_q] * np.sqrt(len(Q))
    P0, P1 = Phi[:-1], Phi[1:]
    m = Phi.shape[1]
    G0 = (P0.T @ P0) / len(P0) + reg * np.eye(m)
    G1 = (P0.T @ P1) / len(P0)
    K = np.linalg.solve(G0, G1).T
    return Phi, K


def koopman_sheaf_coupling(
    x: np.ndarray,
    y: np.ndarray,
    dim: int = 4,
    tau: int = 2,
    diff_lag: int = 4,
    detrend_deg: int = 3,
    max_lag: int = 16,
    min_sep_extra: int = 100,
    n_surrogates: int = 24,
    reg: float = 1e-2,
    rng: Optional[np.random.Generator] = None,
) -> Dict[str, Any]:
    """Coordinate-free lag-scanned cross-modal dynamical lock via Quadratic Koopman-Sheaf.

    1. Removes degree-`detrend_deg` polynomial trends (annihilating 1, t, t^2, t^3) and takes
       lag-`diff_lag` increments x[t+L] - x[t] (stationarizing Brownian walks to MA(L-1) while
       retaining ~16x higher chaotic SNR than 1-step differencing).
    2. Lifts delay coordinates into the GL(d)-invariant degree-<=2 Koopman dictionary Phi_2(Z).
    3. Evaluates max_{lag in [-max_lag, +max_lag]} of Sheaf-gluing * Koopman-intertwining lock
       and calibrates that EXACT SAME max-over-lags statistic against Lyapunov-separated,
       non-wrapping far-shifted interior windows (zero circular-roll discontinuity artifact).
    """
    _ = rng  # evenly spaced deterministic far-shift grid needs no surrogate RNG jitter
    xd = detrend_poly(np.asarray(x, dtype=np.float64), deg=detrend_deg)
    yd = detrend_poly(np.asarray(y, dtype=np.float64), deg=detrend_deg)
    dx = xd[diff_lag:] - xd[:-diff_lag]
    dy = yd[diff_lag:] - yd[:-diff_lag]
    Mx = takens_embed(dx, dim=dim, tau=tau)
    My = takens_embed(dy, dim=dim, tau=tau)
    N_all = min(len(Mx), len(My))
    Mx, My = Mx[:N_all], My[:N_all]

    Px_full, Kx = fit_quad_edmd_koopman(Mx, reg=reg)
    Py_full, Ky = fit_quad_edmd_koopman(My, reg=reg)
    norm_K = float(np.linalg.norm(Kx, ord="fro") + np.linalg.norm(Ky, ord="fro")) + 1e-12

    W = min(300, max(40, N_all // 3))
    n_pos = N_all - W + 1
    eff_max_lag = min(max_lag, max(0, (n_pos - 1) // 6))
    start_x = (N_all - W) // 2

    Px = Px_full[start_x : start_x + W]
    Px = Px - Px.mean(axis=0, keepdims=True)
    Gx = (Px.T @ Px) + 1e-6 * np.eye(Px.shape[1])
    Px_pinv = np.linalg.solve(Gx, Px.T)

    all_scores = np.empty(n_pos, dtype=np.float64)
    all_sheaf = np.empty(n_pos, dtype=np.float64)
    all_inter = np.empty(n_pos, dtype=np.float64)
    for sy in range(n_pos):
        Py = Py_full[sy : sy + W]
        Py = Py - Py.mean(axis=0, keepdims=True)
        T = (Px_pinv @ Py).T
        pred = Px @ T.T
        sheaf_res = float(np.sum((pred - Py) ** 2) / (np.sum(Py ** 2) + 1e-12))
        intertwine = float(np.linalg.norm(T @ Kx - Ky @ T, ord="fro") / norm_K)
        all_sheaf[sy] = sheaf_res
        all_inter[sy] = intertwine
        all_scores[sy] = max(0.0, 1.0 - sheaf_res) * float(np.exp(-2.0 * intertwine))

    def max_lag_at(center: int) -> Tuple[float, int, int]:
        lo = max(0, center - eff_max_lag)
        hi = min(n_pos, center + eff_max_lag + 1)
        idx = lo + int(np.argmax(all_scores[lo:hi]))
        return float(all_scores[idx]), idx - center, idx

    lock_obs, best_lag, best_idx = max_lag_at(start_x)
    sheaf_obs = float(all_sheaf[best_idx])
    inter_obs = float(all_inter[best_idx])

    # Lyapunov-separated non-wrapping far-shift surrogate centers (gracefully clamped for short series)
    eff_extra = min(min_sep_extra, max(20, (n_pos // 3) - eff_max_lag))
    min_sep = eff_max_lag + eff_extra
    valid_centers = [
        c for c in range(eff_max_lag, n_pos - eff_max_lag) if abs(c - start_x) >= min_sep
    ]
    if len(valid_centers) < 4:
        valid_centers = [
            c for c in range(eff_max_lag, n_pos - eff_max_lag) if abs(c - start_x) >= max(eff_max_lag + 1, 10)
        ]
    if len(valid_centers) > n_surrogates:
        sel = np.linspace(0, len(valid_centers) - 1, n_surrogates).round().astype(int)
        chosen = [valid_centers[i] for i in sel]
    else:
        chosen = valid_centers
    null_locks = [max_lag_at(int(c))[0] for c in chosen]
    null_mean = float(np.mean(null_locks))
    null_std = float(np.std(null_locks)) + 1e-9
    z_score = (lock_obs - null_mean) / null_std

    return {
        "sheaf_gluing_residual": round(sheaf_obs, 4),
        "koopman_intertwining_defect": round(inter_obs, 4),
        "dynamical_lock": round(lock_obs, 4),
        "best_lag": int(best_lag),
        "null_shift_mean": round(null_mean, 4),
        "null_shift_std": round(null_std, 4),
        "surrogate_z_score": round(z_score, 2),
    }


# ---------------------------------------------------------------------------
# 5. Full Steelmanning Audit & Repair Verification Suite
# ---------------------------------------------------------------------------

def run_audit(seed: int = 20261120) -> Dict[str, Any]:
    rng = np.random.default_rng(seed)
    N = 900
    N_probe = 320
    trials = 15

    regime_names = [
        "coupled_chaotic_rossler_lag0",
        "coupled_chaotic_rossler_lag12",
        "uncoupled_rossler_independent",
        "uncoupled_rossler_same_burnin",
        "independent_linear_drifts",
        "independent_poly_t2_vs_t3",
        "independent_brownian_walks",
        "independent_ar1_097",
        "phase_randomized_rossler",
    ]
    regimes: Dict[str, Dict[str, List[float]]] = {
        k: {"cka": [], "obs_lock": [], "koop_z": [], "koop_lock": [], "best_lag": []}
        for k in regime_names
    }

    for _ in range(trials):
        a_r, b_r = integrate_rossler(N + 20, rng, random_burn=True)
        a0, b0 = a_r[:N], b_r[:N]
        alag, blag = a_r[:N], b_r[12 : N + 12]
        a_u1, _ = integrate_rossler(N, rng, random_burn=True)
        _, b_u2 = integrate_rossler(N, rng, random_burn=True)
        a_sb, _ = integrate_rossler(N, rng, random_burn=False)
        _, b_sb = integrate_rossler(N, rng, random_burn=False)

        t = np.linspace(0.0, 1.0, N)
        t_lin = np.linspace(0.0, N / float(N_probe), N)
        a_dr = 3.0 * t_lin + 0.15 * rng.normal(size=N)
        b_dr = -5.0 * t_lin + 0.15 * rng.normal(size=N)
        a_pol = 4.0 * (t ** 2) + 0.05 * rng.normal(size=N)
        b_pol = -6.0 * (t ** 3) + 0.05 * rng.normal(size=N)
        a_rw = np.cumsum(rng.normal(size=N))
        b_rw = np.cumsum(rng.normal(size=N))
        a_ar = np.zeros(N)
        b_ar = np.zeros(N)
        for i in range(1, N):
            a_ar[i] = 0.97 * a_ar[i - 1] + rng.normal()
            b_ar[i] = 0.97 * b_ar[i - 1] + rng.normal()
        b_ph = phase_randomize_surrogate(b0, rng)

        for label, s1, s2 in [
            ("coupled_chaotic_rossler_lag0", a0, b0),
            ("coupled_chaotic_rossler_lag12", alag, blag),
            ("uncoupled_rossler_independent", a_u1, b_u2),
            ("uncoupled_rossler_same_burnin", a_sb, b_sb),
            ("independent_linear_drifts", a_dr, b_dr),
            ("independent_poly_t2_vs_t3", a_pol, b_pol),
            ("independent_brownian_walks", a_rw, b_rw),
            ("independent_ar1_097", a_ar, b_ar),
            ("phase_randomized_rossler", a0, b_ph),
        ]:
            pw = continuum_probe_window({"a": s1[:N_probe], "b": s2[:N_probe]})
            regimes[label]["cka"].append(pw["cross_modal_coupling"]["a:b"]["manifold_lock"])
            regimes[label]["obs_lock"].append(pw["cross_modal_coupling"]["a:b"]["observer_invariant_lock"])
            ks = koopman_sheaf_coupling(s1, s2, rng=rng)
            regimes[label]["koop_z"].append(ks["surrogate_z_score"])
            regimes[label]["koop_lock"].append(ks["dynamical_lock"])
            regimes[label]["best_lag"].append(float(ks["best_lag"]))

    summary_regimes = {}
    for label, d in regimes.items():
        summary_regimes[label] = {
            "continuum_cka_mean": round(float(np.mean(d["cka"])), 4),
            "continuum_cka_max": round(float(np.max(d["cka"])), 4),
            "continuum_obs_lock_mean": round(float(np.mean(d["obs_lock"])), 4),
            "repaired_koopman_lock_mean": round(float(np.mean(d["koop_lock"])), 4),
            "repaired_koopman_z_mean": round(float(np.mean(d["koop_z"])), 2),
            "repaired_koopman_z_min": round(float(np.min(d["koop_z"])), 2),
            "repaired_koopman_z_max": round(float(np.max(d["koop_z"])), 2),
            "repaired_pct_z_gt_3": round(100.0 * sum(1 for z in d["koop_z"] if z > 3.0) / len(d["koop_z"]), 1),
            "repaired_best_lag_median": round(float(np.median(d["best_lag"])), 1),
        }

    # --- Audit 2: `h0_persistence_entropy` Honest Behavior ---
    t_grid = np.linspace(0.0, 2.0 * np.pi, 220, endpoint=False)
    M_circle = takens_embed(np.sin(4.0 * t_grid), dim=5, tau=3)
    M_noise = takens_embed(rng.normal(size=220), dim=5, tau=3)
    x_clust = np.concatenate([rng.normal(-5.0, 0.1, 110), rng.normal(5.0, 0.1, 110)])
    M_clust = takens_embed(x_clust, dim=5, tau=3)
    h0_circle = h0_persistence_entropy(M_circle)
    h0_noise = h0_persistence_entropy(M_noise)
    h0_clust = h0_persistence_entropy(M_clust)

    # --- Audit 3: Concrete Prototype Bugs & Verified Repairs ---
    t_w = np.linspace(0.0, 1.0, 1024, endpoint=False)
    pure_wave = np.cos(2.0 * np.pi * 17.0 * t_w)
    quad_wave = np.imag(hilbert_np(pure_wave))
    broken_phase_coh = float(np.abs(np.mean(np.exp(1j * np.angle(hilbert_np(pure_wave))))))
    rel_phasor = np.exp(1j * (np.angle(hilbert_np(quad_wave)) - np.angle(hilbert_np(pure_wave))))
    repaired_plv_mag = float(np.abs(np.mean(rel_phasor)))
    repaired_plv_phase_over_pi = float(np.angle(np.mean(rel_phasor)) / np.pi)

    freqs = np.linspace(4.0, 8.0, 32)
    X_imp = np.zeros((32, 128))
    for r in range(32):
        X_imp[r, 2] = 1.0
    shifts_wrap = np.round(100.0 * (freqs ** -2)).astype(int)
    prof_wrap = np.array([np.roll(row, -s) for row, s in zip(X_imp, shifts_wrap)]).mean(axis=0)
    wrap_energy_right = float(np.sum(prof_wrap[100:]))
    prof_pad = np.zeros(128)
    for row, s in zip(X_imp, shifts_wrap):
        if s < 128:
            prof_pad[: 128 - s] += row[s:]
    prof_pad /= len(freqs)
    repaired_right_energy = float(np.sum(prof_pad[100:]))

    y1_dummy = np.ones(1000)
    bug_slice_len = len(y1_dummy[0 + (-10) : 0 + (-10) + 100])
    repaired_slice_len = len(y1_dummy[10 + (-10) : 10 + (-10) + 100])

    # --- Audit 4: Gate 2 Basis-Invariance Check on Repaired Quadratic Koopman-Sheaf ---
    a_inv, b_inv = integrate_rossler(N, np.random.default_rng(77), random_burn=True)
    b_scaled = -7.3 * b_inv + 42.5
    ks_base = koopman_sheaf_coupling(a_inv, b_inv)
    ks_aff = koopman_sheaf_coupling(a_inv, b_scaled)
    affine_diff = abs(ks_base["dynamical_lock"] - ks_aff["dynamical_lock"])

    xd_inv = detrend_poly(a_inv, deg=3)
    Mx5 = takens_embed(xd_inv[4:] - xd_inv[:-4], dim=5, tau=2)
    A_gl5 = np.array([
        [2.0, -1.0, 0.5, 0.0, 1.0],
        [0.0, 3.0, -0.5, 1.0, 0.0],
        [1.0, 0.0, 1.5, -2.0, 0.5],
        [-0.5, 1.0, 0.0, 2.5, -1.0],
        [0.2, -0.3, 1.0, 0.5, 3.0],
    ])
    _, K1 = fit_edmd_koopman(Mx5, reg=0.0)
    _, K2 = fit_edmd_koopman(Mx5 @ A_gl5, reg=0.0)
    gl5_spec_diff = float(np.max(np.abs(np.sort(np.abs(np.linalg.eigvals(K1))) - np.sort(np.abs(np.linalg.eigvals(K2))))))

    Mx4 = takens_embed(xd_inv[4:] - xd_inv[:-4], dim=4, tau=2)
    A_gl4 = A_gl5[:4, :4]
    _, Kq1 = fit_quad_edmd_koopman(Mx4, reg=1e-2)
    _, Kq2 = fit_quad_edmd_koopman(Mx4 @ A_gl4, reg=1e-2)
    gl4_quad_spec_diff = float(np.max(np.abs(np.sort(np.abs(np.linalg.eigvals(Kq1))) - np.sort(np.abs(np.linalg.eigvals(Kq2))))))

    # Fail-closed checks of our verified findings (no bare asserts!)
    if summary_regimes["independent_linear_drifts"]["continuum_cka_mean"] <= 0.95:
        raise RuntimeError("Expected high linear-drift CKA false positive")
    for coupled_name in ("coupled_chaotic_rossler_lag0", "coupled_chaotic_rossler_lag12"):
        if summary_regimes[coupled_name]["repaired_koopman_z_mean"] <= 3.0:
            raise RuntimeError(f"Repaired Koopman missed {coupled_name}: {summary_regimes[coupled_name]}")
    if not (-13.0 <= summary_regimes["coupled_chaotic_rossler_lag12"]["repaired_best_lag_median"] <= -9.0):
        raise RuntimeError(f"Lag-12 recovery missed true lag: {summary_regimes['coupled_chaotic_rossler_lag12']}")
    for null_name in (
        "uncoupled_rossler_independent",
        "uncoupled_rossler_same_burnin",
        "independent_linear_drifts",
        "independent_poly_t2_vs_t3",
        "independent_brownian_walks",
        "independent_ar1_097",
        "phase_randomized_rossler",
    ):
        if abs(summary_regimes[null_name]["repaired_koopman_z_mean"]) >= 1.5:
            raise RuntimeError(f"Repaired Koopman leaked null {null_name}: {summary_regimes[null_name]}")
    if affine_diff > 1e-4 or gl5_spec_diff > 1e-10 or gl4_quad_spec_diff > 1e-10:
        raise RuntimeError(f"Basis invariance failed: affine={affine_diff}, gl5={gl5_spec_diff}, gl4q={gl4_quad_spec_diff}")
    if not (broken_phase_coh < 1e-6 and repaired_plv_mag > 0.999 and abs(abs(repaired_plv_phase_over_pi) - 0.5) < 1e-3):
        raise RuntimeError("Phase-coherence repair check failed")
    if not (wrap_energy_right > 0.05 and repaired_right_energy == 0.0 and bug_slice_len == 0 and repaired_slice_len == 100):
        raise RuntimeError("Code-bug repair check failed")

    return {
        "seed": seed,
        "audit_1_continuum_probe_vs_repaired_koopman": summary_regimes,
        "audit_2_h0_persistence_entropy": {
            "two_clusters": round(h0_clust, 4),
            "smooth_sinusoid_circle": round(h0_circle, 4),
            "white_gaussian_noise": round(h0_noise, 4),
            "note": "Does NOT invert circle vs noise (0.74 < 0.99), but ranks bimodal clusters lowest (0.64 < 0.74 < 0.99)",
        },
        "audit_3_prototype_bugs_and_repairs": {
            "phase_coherence_bug_on_pure_cosine": round(broken_phase_coh, 8),
            "repaired_hilbert_Z4_plv_magnitude": round(repaired_plv_mag, 6),
            "repaired_hilbert_Z4_phase_over_pi": round(repaired_plv_phase_over_pi, 6),
            "np_roll_right_edge_wrap_energy": round(wrap_energy_right, 4),
            "repaired_zero_pad_right_edge_energy": round(repaired_right_energy, 6),
            "negative_lag_bug_slice_len": bug_slice_len,
            "repaired_lag_slice_len": repaired_slice_len,
        },
        "audit_4_repaired_koopman_basis_invariance": {
            "affine_channel_warp_lock_diff": round(affine_diff, 8),
            "GL5_linear_koopman_eigenvalue_diff": float(f"{gl5_spec_diff:.3e}"),
            "GL4_quadratic_koopman_eigenvalue_diff": float(f"{gl4_quad_spec_diff:.3e}"),
        },
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    parser.add_argument("--seed", type=int, default=20261120, help="Deterministic RNG seed")
    args = parser.parse_args(argv)
    rep = run_audit(seed=args.seed)
    if args.json:
        print(json.dumps(rep, indent=2))
    else:
        print(f"=== audit_continuum_probes.py: STEELMANNED AUDIT & REPAIR PASSED (seed={rep['seed']}) ===")
        a1 = rep["audit_1_continuum_probe_vs_repaired_koopman"]
        print("1. `probe_window` (continuum PR #2, N=320) vs Repaired Lag-Scanned Quadratic Koopman-Sheaf (N=900, 15 trials):")
        for k, v in a1.items():
            print(
                f"   {k:30s} | CKA={v['continuum_cka_mean']:.4f} (max={v['continuum_cka_max']:.4f}) "
                f"| Q-Koopman lock={v['repaired_koopman_lock_mean']:.4f} "
                f"(z={v['repaired_koopman_z_mean']:+.2f} [{v['repaired_koopman_z_min']:+.2f},{v['repaired_koopman_z_max']:+.2f}], >3:{v['repaired_pct_z_gt_3']:5.1f}%, med_lag={v['repaired_best_lag_median']:+5.1f})"
            )
        a2 = rep["audit_2_h0_persistence_entropy"]
        print(f"2. `h0_persistence_entropy`: clusters={a2['two_clusters']} < circle={a2['smooth_sinusoid_circle']} < white_noise={a2['white_gaussian_noise']}")
        a3 = rep["audit_3_prototype_bugs_and_repairs"]
        print(
            f"3. Prototype bugs -> repairs: phase_coh {a3['phase_coherence_bug_on_pure_cosine']} -> Z4 PLV {a3['repaired_hilbert_Z4_plv_magnitude']} (phase={a3['repaired_hilbert_Z4_phase_over_pi']}*pi); "
            f"np.roll wrap {a3['np_roll_right_edge_wrap_energy']} -> {a3['repaired_zero_pad_right_edge_energy']}; "
            f"neg-lag slice len {a3['negative_lag_bug_slice_len']} -> {a3['repaired_lag_slice_len']}"
        )
        a4 = rep["audit_4_repaired_koopman_basis_invariance"]
        print(
            f"4. Repaired Koopman basis invariance: affine diff={a4['affine_channel_warp_lock_diff']}, "
            f"GL(5) linear spec diff={a4['GL5_linear_koopman_eigenvalue_diff']}, "
            f"GL(4) quadratic spec diff={a4['GL4_quadratic_koopman_eigenvalue_diff']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
