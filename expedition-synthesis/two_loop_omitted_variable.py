#!/usr/bin/env python3
"""Exact-Rational Two-Loop Omitted-Variable Phase Boundary Theorem (SEAM-07).

Zero-float (`fractions.Fraction` only, stdlib only) proof & computational verifier
settling the missing second half of Claim 9 and Falsifier #6 in `siliconcordat/loom#9`
(`docs/09-gate-contracts.md`), bridging The Latch (Claim 10) to Active Multi-Basis
Observer Tomography (Session 1 Portal 4B) and `Foundation-0/gravity` model misspecification.

Exact Linear-Algebraic Setting:
  True signal y = Phi theta* + Psi beta* in Q^m, where:
    - Phi in Q^{m x k} is the current specification's adjustable parameter subspace,
    - Psi in Q^{m x d} is an omitted specification subspace with Psi_perp = (I - P_Phi) Psi != 0
      and true omitted component r* = Psi_perp beta* != 0 (the OLS residual after Latch fitting).

Theorem (Exact Pythagorean Gap & Falsifier #6 Phase Boundary):
  Suppose an outside anchor a_1 in Q^m detects the misspecification (e_1 = a_1^T r* != 0)
  and is NOT orthogonal to Col(Phi) (p_1 = P_Phi a_1 != 0), in a noiseless linear model. Compare two responses:
    (1) Fixed-Spec Anchor Absorption (feed a_1 back to proposer inside Phi):
        Minimum output-space norm shift (minimizing ||Phi Delta_theta||_2) Phi Delta_theta = (e_1 / ||p_1||^2) p_1 silences a_1
        (a_1^T r_adapt = 0), yielding post-absorption residual r_adapt = r* - Phi Delta_theta.
        Because Phi Delta_theta is strictly orthogonal to r* = Psi_perp beta*, Pythagoras gives:
          ||r_adapt||^2 = ||r*||^2 + e_1^2 / ||p_1||^2  >  ||r*||^2   (EXACT INFLATION!).
        On any fresh unseen anchor a_2 in Q^m with e_2 = a_2^T r* != 0, defining:
          rho_Phi(a_1, a_2)   := (p_1^T a_2) / ||p_1||^2,
          kappa_perp(a_1, a_2) := e_2 / e_1,
        the exact post-absorption error on a_2 is:
          a_2^T r_adapt = e_2 * (1 - rho_Phi / kappa_perp).
        Therefore:
          - Falsifier #6 regime (anchor absorption helps on a_2):  0 < rho_Phi / kappa_perp < 2.
          - Claim 9 regime (anchor absorption HURTS on a_2):       rho_Phi / kappa_perp <= 0 or >= 2.
          - Over any centered/isotropic fresh anchor ensemble with covariance Sigma_a = sigma^2 I_m
            (or any fresh anchor a_2 with a_2^T r* uncorrelated with a_2^T p_1):
            E[(a_2^T r_adapt)^2] - E[(a_2^T r*)^2] = sigma^2 * e_1^2 / ||p_1||^2 > 0 ALWAYS!
    (2) Specification Revision (halt adaptation, expand spec Phi -> Phi' = [Phi, Psi_rev]):
        Let P_rev_perp be the orthogonal projector onto Col((I - P_Phi) Psi_rev). Then:
          ||r_rev||^2 = ||r*||^2 - ||P_rev_perp r*||^2  <=  ||r*||^2  <  ||r_adapt||^2
        with strict contraction whenever P_rev_perp r* != 0, and exact zero error (r_rev = 0)
        on ALL fresh unseen anchors when Psi_perp beta* in Col(P_rev_perp)!

Run:
  python3 -O -B expedition-synthesis/two_loop_omitted_variable.py
  python3 -O -B expedition-synthesis/two_loop_omitted_variable.py --json
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
import random
import sys
from pathlib import Path as _Path
_HERE = str(_Path(__file__).resolve().parent)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from typing import Any, Dict, List, Optional, Sequence, Tuple

from optimal_inertia_rank import exact_rational_householder, mat_mul, mat_t

Mat = List[List[Fraction]]
Vec = List[Fraction]


def dot(u: Vec, v: Vec) -> Fraction:
    return sum((a * b for a, b in zip(u, v)), Fraction(0))


def norm2(u: Vec) -> Fraction:
    return dot(u, u)


def vec_add(u: Vec, v: Vec) -> Vec:
    return [a + b for a, b in zip(u, v)]


def vec_sub(u: Vec, v: Vec) -> Vec:
    return [a - b for a, b in zip(u, v)]


def vec_scale(c: Fraction, u: Vec) -> Vec:
    return [c * a for a in u]


def mat_vec(A: Mat, x: Vec) -> Vec:
    return [dot(row, x) for row in A]


def mat_inv_exact(A: Mat) -> Mat:
    """Exact Gauss-Jordan inverse over Q for full-rank square matrix A."""
    n = len(A)
    aug = [A[i][:] + [Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = None
        for r in range(col, n):
            if aug[r][col] != 0:
                piv = r
                break
        if piv is None:
            raise ValueError("SINGULAR_GRAM_MATRIX")
        aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        for c in range(2 * n):
            aug[col][c] /= pv
        for r in range(n):
            if r != col and aug[r][col] != 0:
                fac = aug[r][col]
                for c in range(2 * n):
                    aug[r][c] -= fac * aug[col][c]
    return [row[n:] for row in aug]


def orth_projector(B: Mat) -> Mat:
    """Exact orthogonal projector P_B = B (B^T B)^{-1} B^T over Q for full-column-rank B."""
    Bt = mat_t(B)
    G_inv = mat_inv_exact(mat_mul(Bt, B))
    return mat_mul(mat_mul(B, G_inv), Bt)


def run_two_loop_audit() -> Dict[str, Any]:
    # -----------------------------------------------------------------------
    # 1. Exact Canonical Model (m = 6, k = 2 spec Phi, d = 1 omitted Psi)
    #    Rotated by an exact rational Householder reflection U6 for Gate 2
    #    coordinate/basis invariance!
    # -----------------------------------------------------------------------
    U6 = exact_rational_householder([Fraction(1), Fraction(-1), Fraction(2), Fraction(1), Fraction(-1), Fraction(1)])
    # Phi = columns 0, 1 of U6; omitted Psi = column 2 of U6; pure noise-free orthogonal cols 3,4,5
    Phi = [[U6[r][c] for c in (0, 1)] for r in range(6)]
    Psi = [[U6[r][2]] for r in range(6)]
    theta_star = [Fraction(3), Fraction(-2)]
    beta_star = [Fraction(5)]

    y = vec_add(mat_vec(Phi, theta_star), mat_vec(Psi, beta_star))
    P_Phi = orth_projector(Phi)
    # OLS residual after Latch fitting inside fixed spec Phi
    y_hat_ols = mat_vec(P_Phi, y)
    r_star = vec_sub(y, y_hat_ols)  # equals Psi_perp beta_star exactly!
    r_star_norm2 = norm2(r_star)
    if r_star_norm2 != Fraction(25):
        raise RuntimeError(f"Expected ||r*||^2 == 25, got {r_star_norm2}")

    # Failed anchor a_1 = u_0 + u_2 (has both in-spec projection p_1 = u_0 and omitted overlap e_1 = 5)
    u = [[U6[r][c] for r in range(6)] for c in range(6)]
    a1 = vec_add(u[0], u[2])
    p1 = mat_vec(P_Phi, a1)
    e1 = dot(a1, r_star)
    p1_n2 = norm2(p1)
    if e1 != Fraction(5) or p1_n2 != Fraction(1):
        raise RuntimeError("Anchor a_1 projection mismatch")

    # Policy 1: Fixed-spec anchor absorption (minimum-norm shift inside Phi silencing a_1)
    delta_phi = vec_scale(e1 / p1_n2, p1)
    r_adapt = vec_sub(r_star, delta_phi)
    if dot(a1, r_adapt) != Fraction(0):
        raise RuntimeError("Absorption did not silence a_1!")
    r_adapt_norm2 = norm2(r_adapt)
    # Exact Pythagorean inflation check: ||r_adapt||^2 == ||r*||^2 + e1^2 / ||p1||^2
    expected_adapt_n2 = r_star_norm2 + (e1 * e1) / p1_n2
    if r_adapt_norm2 != expected_adapt_n2 or r_adapt_norm2 <= r_star_norm2:
        raise RuntimeError("Pythagorean inflation identity failed!")

    # Policy 2: Partial and Full Specification Revision
    # 2a: Partial revision adding v_part = (3/5) u_2 + (4/5) u_3 (captures 9/25 of omitted variance)
    v_part = vec_add(vec_scale(Fraction(3, 5), u[2]), vec_scale(Fraction(4, 5), u[3]))
    Phi_part = [Phi[r] + [v_part[r]] for r in range(6)]
    r_rev_part = vec_sub(y, mat_vec(orth_projector(Phi_part), y))
    # 2b: Full revision adding u_2
    Phi_full = [Phi[r] + [u[2][r]] for r in range(6)]
    r_rev_full = vec_sub(y, mat_vec(orth_projector(Phi_full), y))
    if norm2(r_rev_part) != Fraction(16) or norm2(r_rev_full) != Fraction(0):
        raise RuntimeError(f"Spec revision norm mismatch: part={norm2(r_rev_part)}, full={norm2(r_rev_full)}")

    # -----------------------------------------------------------------------
    # 2. Exact Phase-Boundary Sweep Across Fresh Unseen Anchors a_2
    #    a_2(alpha) = alpha * u_0 + u_2  =>  rho_Phi = alpha, kappa_perp = 1, ratio = alpha!
    #    Falsifier #6 fires iff 0 < alpha < 2; Claim 9 wins strictly iff alpha <= 0 or alpha >= 2!
    # -----------------------------------------------------------------------
    sweep = []
    for alpha in (Fraction(-1), Fraction(0), Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2), Fraction(3)):
        a2 = vec_add(vec_scale(alpha, u[0]), u[2])
        e2_ols = dot(a2, r_star)
        e2_adapt = dot(a2, r_adapt)
        e2_rev_part = dot(a2, r_rev_part)
        e2_rev_full = dot(a2, r_rev_full)
        ratio = (dot(p1, a2) / p1_n2) / (e2_ols / e1)
        expected_e2_adapt = e2_ols * (Fraction(1) - ratio)
        if e2_adapt != expected_e2_adapt:
            raise RuntimeError("Phase-boundary algebraic formula mismatch!")
        falsifier6_fires = (e2_adapt * e2_adapt < e2_ols * e2_ols)
        if falsifier6_fires != (Fraction(0) < ratio < Fraction(2)):
            raise RuntimeError("Phase-boundary iff condition violated!")
        sweep.append({
            "alpha_ratio": str(ratio),
            "err_sq_ols": str(e2_ols * e2_ols),
            "err_sq_anchor_adapt": str(e2_adapt * e2_adapt),
            "err_sq_partial_spec_rev": str(e2_rev_part * e2_rev_part),
            "err_sq_full_spec_rev": str(e2_rev_full * e2_rev_full),
            "falsifier6_fires": falsifier6_fires,
        })

    # -----------------------------------------------------------------------
    # 3. Exact Randomized Multi-Basis Verification (200 exact rational instances)
    # -----------------------------------------------------------------------
    rng = random.Random(20261120)
    trials = 200
    pythagorean_exact = 0
    phase_iff_exact = 0
    for _ in range(trials):
        # Random orthogonal basis via Householder on Q^5
        vh = [Fraction(rng.randint(-3, 3)) for _ in range(5)]
        if all(x == 0 for x in vh):
            vh[0] = Fraction(1)
        Uh = exact_rational_householder(vh)
        Phi_t = [[Uh[r][c] for c in (0, 1)] for r in range(5)]
        Psi_t = [[Uh[r][c] for c in (2, 3)] for r in range(5)]
        P_t = orth_projector(Phi_t)
        th_t = [Fraction(rng.randint(-4, 4)) for _ in range(2)]
        be_t = [Fraction(rng.randint(1, 4)), Fraction(rng.randint(-3, 3))]
        y_t = vec_add(mat_vec(Phi_t, th_t), mat_vec(Psi_t, be_t))
        r_t = vec_sub(y_t, mat_vec(P_t, y_t))
        a1_t = [Fraction(rng.randint(-3, 3)) for _ in range(5)]
        a2_t = [Fraction(rng.randint(-3, 3)) for _ in range(5)]
        p1_t = mat_vec(P_t, a1_t)
        e1_t = dot(a1_t, r_t)
        e2_t = dot(a2_t, r_t)
        if norm2(p1_t) == 0 or e1_t == 0 or e2_t == 0:
            continue
        r_ad_t = vec_sub(r_t, vec_scale(e1_t / norm2(p1_t), p1_t))
        if norm2(r_ad_t) != norm2(r_t) + (e1_t * e1_t) / norm2(p1_t):
            raise RuntimeError("Random Pythagorean identity failed!")
        pythagorean_exact += 1
        rat_t = (dot(p1_t, a2_t) / norm2(p1_t)) / (e2_t / e1_t)
        if (dot(a2_t, r_ad_t) ** 2 < e2_t ** 2) != (Fraction(0) < rat_t < Fraction(2)):
            raise RuntimeError("Random phase-boundary iff failed!")
        phase_iff_exact += 1

    return {
        "canonical_householder_6d": {
            "norm2_ols_r_star": str(r_star_norm2),
            "norm2_fixed_spec_anchor_adapt": str(r_adapt_norm2),
            "pythagorean_inflation_e1sq_over_p1sq": str((e1 * e1) / p1_n2),
            "norm2_partial_spec_revision": str(norm2(r_rev_part)),
            "norm2_full_spec_revision": str(norm2(r_rev_full)),
            "global_ordering_strict": norm2(r_rev_full) < norm2(r_rev_part) < r_star_norm2 < r_adapt_norm2,
        },
        "fresh_anchor_phase_boundary_sweep": sweep,
        "random_exact_rational_verification": {
            "seed": 20261120,
            "tested_nondegenerate_instances": pythagorean_exact,
            "pythagorean_exact_matches": pythagorean_exact,
            "phase_boundary_iff_matches": phase_iff_exact,
        },
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args(argv)
    rep = run_two_loop_audit()
    if args.json:
        print(json.dumps(rep, indent=2))
    else:
        print("=== two_loop_omitted_variable.py: SEAM-07 PHASE BOUNDARY VERIFIED (ZERO FLOAT) ===")
        c = rep["canonical_householder_6d"]
        print(
            f"1. Global residual^2 (Householder-rotated Q^6): "
            f"full_rev={c['norm2_full_spec_revision']} < partial_rev={c['norm2_partial_spec_revision']} < "
            f"OLS={c['norm2_ols_r_star']} < anchor_adapt={c['norm2_fixed_spec_anchor_adapt']} "
            f"(exact inflation +{c['pythagorean_inflation_e1sq_over_p1sq']})"
        )
        print("2. Fresh-anchor phase boundary (ratio = rho_Phi / kappa_perp; Falsifier #6 iff 0 < ratio < 2):")
        for row in rep["fresh_anchor_phase_boundary_sweep"]:
            print(
                f"   ratio={row['alpha_ratio']:>4s} | OLS^2={row['err_sq_ols']:>3s} | "
                f"adapt^2={row['err_sq_anchor_adapt']:>5s} | part_rev^2={row['err_sq_partial_spec_rev']:>6s} | "
                f"full_rev^2={row['err_sq_full_spec_rev']:>2s} | Falsifier#6={row['falsifier6_fires']}"
            )
        r = rep["random_exact_rational_verification"]
        print(
            f"3. Random exact Q^5 Householder verification: {r['pythagorean_exact_matches']}/{r['tested_nondegenerate_instances']} "
            f"Pythagorean & {r['phase_boundary_iff_matches']}/{r['tested_nondegenerate_instances']} phase-boundary iff matches"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
