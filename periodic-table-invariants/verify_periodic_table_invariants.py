#!/usr/bin/env python3
"""Pure-Q/Z Self-Contained Verifier for Cross-Civilizational Universal Invariants & Periodic Table.

Self-contained Python 3 standard-library verifier for Foundation-0/continuum.
Contains ZERO float or complex literals, ZERO ast.Div ('/' or '/=') true divisions,
ZERO negative-exponent powers (2**-1), ZERO pow()/getattr()/builtins escapes,
ZERO __float__/__complex__/__truediv__/__rtruediv__/__itruediv__/__pow__ attribute refs,
ZERO float()/complex() calls, ZERO math.<attr> calls or constant refs outside {gcd, isqrt}
(including aliases), ZERO string/float/1-arg/from_float Fraction(...) calls, ZERO bare
assert statements, and ZERO unbound external provenance digests.

Every one of the 16 Periodic Table entries (PT-01..PT-16) is computed and certified
directly in-module in exact integer (int) and rational (Fraction) arithmetic:
  1. 4-Class Aleph_0 -> c Finite-Net Obstruction Taxonomy (Class A, B, C, D):
       - Class A (Diophantine / Prime-Lattice): Al-Farabi 53-TET prime obstruction,
         Zu Chongzhi [3;7,15,1] = 355/113 Hurwitz floor (>= 4740x) & exhaustive first-beater
         scan proving 52163/16604 is the earliest rational beater in q in [114, 16604]
         using a first-principles pure-Q Machin alternating-series pi bracket (0 decimal pi literals),
         Rhind 2/17 & Egyptian 5/21 vs computed greedy Sylvester decompositions,
         Antikythera gear-train products & additive beat 254*223 - 239*235 = 9*53,
         Kerala School Madhava R_1, R_2, R_3 telescoping identities (n = 2..50) and
         exact n = 50 speedup floor (>= 27,872,151,775x over Leibniz).
       - Class B (Subtractive Cancellation & Rational Sphere Lift): kappa_sub(x) = x/(1-x)
         for Al-Biruni Nandana (215989/11, 14b), Al-Kashi chord wall derived from k (k=25 vs 26),
         multiscale quadratic zoom derived from ell (ell=13, 14, 16), plus generic multivariate
         polynomial bijection proof (19/19 exact identities over Z[u,v], Z[x,y,z], Z[w1,w2,w3],
         Z[q0,q1,q2,q3]) and 5-point numerical round-trips for Al-Biruni Isti'ab stereographic
         S^2(Q)\\{N} <-> Q^2 and Cayley S^3(Q)\\{-1} <-> Q^3.
       - Class C (Topological Winding, C1P Partition, GF(2) Hypercube & Sheaf H^1):
         Chokwe Sona mirror-curve exhaustive sweep across all 576/576 grids in [1,24]^2 plus
         2-opt internal mirror surgery ((2,2): 2->1; (2,3): 1->2), Panini 14-Sivasutra
         43/43 C1P decoding + Tucker C_3 0/6 single-copy impossibility + duplicate-h resolution,
         Pingala nasta/uddista 510/510 bijection + FWHT_256 256/256 involution & parity +
         explicit 5x16 Extended Hamming [16,11,4] A_16 SECDED parity-check matrix H
         (16/16 distinct nonzero 1-bit syndromes, 120/120 disjoint nonzero 2-bit syndromes,
         2,048 codewords, d_min = 4) + Bamana 65,536/65,536 even-Judge parity-conservation
         identity check and A_16 syndrome correspondence, Z_2 twisted 3-cycle sheaf (0/8 vs 2/8),
         explicit Casarabe C_{2,6} (13 vertices, pinned canonical 24-edge set & degree sequence
         [6, 4*6, 3*6], beta_1 = 12) vs spanning tree T_13 (pinned 12-edge set & degrees
         [6, 2*6, 1*6], beta_1 = 0) cut resilience, and hierarchical tree-sum checksums.
       - Class D (Commutation, Schur Inertia & Coarse-Graining Defect): Ibn al-Nafis
         readable-record 3x3 covariance Schur complement (det 34/625 -> 688/15625, drop 81/1250),
         self-certifying 8x8 Sylvester congruence P^T M P = diag(d) separating passive hydraulic
         Laplacian inertia (7, 0, 1) from indefinite H_8 master stress inertia (4, 4, 0),
         explicit 4x4 stochastic-matrix Kemeny-Snell Markov lumpability defect (0/1 vs 1/2),
         and SU(2) half-angle Cayley Lie-Trotter defect vs exact palindromic Strang quaternion.
  2. Subtractive Selection & Opposing-Pair Conservation:
       Explicit 2x2 planar Al-Tusi counter-rotating matrices vs 3x3 SO(3) spherical hippopede
       (288/3125), explicit so(3) Lie-bracket order-3 BCH C_3(e_1, 2e_2) = (-1/3, -1/6, 0)
       (||C_3||^2 = 5/36), exact collinear SU(2) Strang quaternion, antagonistic joint torque
       equilibrium + stiffness + vanishing mixed coupling H_ant = 0, explicit 3x3 orthogonal
       Cayley steering matrix vs state-dependent xz-plane rotation, dimensionless Dougong
       Coulomb hysteresis loop area (96/1, pi*zeta = 2/3), and Housner rocking loss (111/400).
  3. Intrinsic Modular Flow & Minimal Sufficient Partition:
       Panini C1P compression derived from decoded 43 classes / 42 phonemes / 43 slots / 14
       it-markers using fixed-width index bit lengths ceil(log2(42))=6 bits per phoneme ID and
       ceil(log2(14))=4 bits per it-marker ID (6+4=10-bit descriptor -> 21/5; + 43*6-bit slot
       table -> 21/8), Qin Jiushao non-coprime CRT exhaustive 37,960/37,960 forward+inverse
       isomorphism Z/37960Z <-> compatible subgroup of Z/260Z x Z/365Z x Z/584Z
       (r1=r2 mod 5, r2=r3 mod 73, r1=r3 mod 4; compression 1460x, Dresden 2392/81,
       inconsistent triple refused), Antikythera gear trains (254/19, 235/19, 477/4237,
       56165/4237), and exact finite-baseline two-clock Hurst-3/4 variance shift
       (112/31 -> 256/31, delta 144/31) vs explicit 1,024-sequence Walsh-Rademacher
       white-noise finite-sample block-variance estimator (1/1 -> 1/1, delta 0/1).
  4. Machine-Readable Periodic Table of Invariants:
       16 self-contained entries across 5 morphological families whose morphism_evidence flags,
       morphism_grade labels, and witness metrics are derived dynamically from live pillar
       outputs, with fail-closed --check validation (including parse_float/parse_constant
       rejection) of both committed JSON files on disk.
"""

from __future__ import annotations

import argparse
import ast
import copy
import functools
import hashlib
import hmac
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "continuum.universal_invariants_certificate.v2"
PERIODIC_TABLE_SCHEMA = "continuum.periodic_table_of_invariants.v2"
COMPUTE_POLICY_STATUS = "CPU_ONLY_PURE_Q_NO_ENERGY_CLAIMS"

ZERO = Fraction(0, 1)
ONE = Fraction(1, 1)
TWO = Fraction(2, 1)
FOUR = Fraction(4, 1)

HEX_DIGITS = frozenset("0123456789abcdef")

ALLOWED_FAMILIES = frozenset(
    (
        "COMMUTATION_SCHUR_STRATUM",
        "DIOPHANTINE_RESONANCE_LATTICE",
        "OPPOSING_PAIR_CONSERVATION_AND_DAMPING",
        "SUBTRACTIVE_CANCELLATION_WALL",
        "TOPOLOGICAL_PARTITION_OBSTRUCTION",
    )
)
ALLOWED_OBSTRUCTION_CLASSES = frozenset(
    (
        "CLASS_A_DIOPHANTINE",
        "CLASS_B_CANCELLATION",
        "CLASS_C_TOPOLOGICAL",
        "CLASS_D_COMMUTATION",
    )
)
ALLOWED_MORPHISM_GRADES = frozenset(
    (
        "EXACT_ISOMORPHISM",
        "EXACT_SHARED_OPERATOR",
        "PROVABLE_OBSTRUCTION",
        "SHARED_BLOCK_ELIMINATION_NON_CONGRUENT",
    )
)
EVIDENCE_KEYS = frozenset(
    (
        "has_forward_inverse_bijection",
        "has_impossibility_counterexample",
        "has_non_congruent_inertia_separation",
        "has_shared_operator_witness",
    )
)

# Authentic 14 Sivasutras: (sutra_id, marker_id, phonemes)
# 'h' appears twice (S5 and S14); it-marker 'N' appears twice (S1='N1', S6='N2').
SIVASUTRAS: tuple[tuple[int, str, tuple[str, ...]], ...] = (
    (1, "N1", ("a", "i", "u")),
    (2, "k", ("R", "L")),
    (3, "G", ("e", "o")),
    (4, "c", ("ai", "au")),
    (5, "T", ("h", "y", "v", "r")),
    (6, "N2", ("l",)),
    (7, "m", ("ny", "m", "ng", "nr", "n")),
    (8, "J", ("jh", "bh")),
    (9, "S", ("gh", "dhr", "dh")),
    (10, "z", ("j", "b", "g", "dr", "d")),
    (11, "v", ("kh", "ph", "ch", "thr", "th", "c", "tr", "t")),
    (12, "y", ("k", "p")),
    (13, "r", ("sh", "sr", "s")),
    (14, "l", ("h",)),
)

# Canonical 43 Paninian pratyaharas: (name, start_phoneme, end_marker, expected_member_count)
CANONICAL_PRATYAHARAS: tuple[tuple[str, str, str, int], ...] = (
    ("aN", "a", "N1", 3),
    ("ak", "a", "k", 5),
    ("ik", "i", "k", 4),
    ("uk", "u", "k", 3),
    ("eG", "e", "G", 2),
    ("ac", "a", "c", 9),
    ("ic", "i", "c", 8),
    ("ec", "e", "c", 4),
    ("aic", "ai", "c", 2),
    ("aT", "a", "T", 13),
    ("aN2", "a", "N2", 14),
    ("iN", "i", "N2", 13),
    ("yaN", "y", "N2", 4),
    ("ra", "r", "N2", 2),
    ("am", "a", "m", 19),
    ("yam", "y", "m", 9),
    ("Gam", "ng", "m", 3),
    ("yaJ", "y", "J", 11),
    ("jhaS", "jh", "S", 5),
    ("bhaS", "bh", "S", 4),
    ("az", "a", "z", 29),
    ("haz", "h", "z", 20),
    ("vaz", "v", "z", 18),
    ("jhaz", "jh", "z", 10),
    ("jaz", "j", "z", 5),
    ("baz", "b", "z", 4),
    ("chav", "ch", "v", 6),
    ("yay", "y", "y", 29),
    ("may", "m", "y", 24),
    ("jhay", "jh", "y", 20),
    ("khay", "kh", "y", 10),
    ("cay", "c", "y", 5),
    ("yar", "y", "r", 32),
    ("jhar", "jh", "r", 23),
    ("khar", "kh", "r", 13),
    ("car", "c", "r", 8),
    ("zar", "sh", "r", 3),
    ("al", "a", "l", 42),
    ("hal", "h", "l", 33),
    ("val", "v", "l", 32),
    ("ral", "r", "l", 31),
    ("jhal", "jh", "l", 24),
    ("zal", "sh", "l", 4),
)

QuatQ = tuple[Fraction, Fraction, Fraction, Fraction]
Vec3Q = tuple[Fraction, Fraction, Fraction]


def require_ok(cond: bool, msg: str) -> None:
    """Fail-closed invariant guard (zero bare asserts)."""
    if cond is not True:
        raise ValueError(msg)


def q_div(a: Fraction, b: Fraction) -> Fraction:
    """Exact rational division a / b without Python true-division operator ('/')."""
    require_ok(b != ZERO, "Rational division by zero")
    return Fraction(a.numerator * b.denominator, a.denominator * b.numerator)


def is_hex64(value: Any) -> bool:
    """Return True iff value is a 64-character lowercase hexadecimal SHA-256 string."""
    if not isinstance(value, str):
        return False
    if len(value) != 64:
        return False
    for ch in value:
        if ch not in HEX_DIGITS:
            return False
    return True


def q_str(val: Fraction) -> str:
    """Enforce exact Fraction runtime type at pillar boundary before serialization."""
    require_ok(type(val) is Fraction, "Expected exact Fraction scalar at pillar boundary")
    return str(val)


def z_int(val: int) -> int:
    """Enforce exact int runtime type (excluding bool/float) at pillar boundary."""
    require_ok(type(val) is int, "Expected exact int scalar at pillar boundary")
    return val


def assert_no_floats_recursive(obj: Any) -> None:
    """Recursively reject any runtime float or complex instance in a serialized payload."""
    require_ok(not isinstance(obj, (float, complex)), "Runtime float or complex forbidden in serialized payload")
    if isinstance(obj, dict):
        for k, v in obj.items():
            assert_no_floats_recursive(k)
            assert_no_floats_recursive(v)
    elif isinstance(obj, (list, tuple)):
        for item in obj:
            assert_no_floats_recursive(item)


def _reject_json_float(token: str) -> Any:
    raise ValueError(f"JSON float literal forbidden: {token}")


def _reject_json_constant(token: str) -> Any:
    raise ValueError(f"JSON non-finite constant forbidden: {token}")


def _reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in pairs:
        require_ok(k not in out, f"Duplicate JSON key forbidden: {k}")
        out[k] = v
    return out


def loads_strict_no_float_json(raw: str) -> Any:
    """Parse JSON while failing closed on floats, NaN/Infinity tokens, or duplicate keys."""
    return json.loads(
        raw,
        parse_float=_reject_json_float,
        parse_constant=_reject_json_constant,
        object_pairs_hook=_reject_duplicate_json_keys,
    )


def _arctan_inv_bracket_q(m: int, pairs: int) -> tuple[Fraction, Fraction]:
    """Rigorous pure-Q alternating-series [lo, hi] bracket for arctan(1/m), m >= 5."""
    require_ok(m >= 5, "arctan_inv m must be >= 5")
    require_ok(pairs >= 1, "arctan_inv pairs must be >= 1")
    acc = ZERO
    p = m
    m2 = m * m
    for k in range(2 * pairs):
        term = Fraction(1, (2 * k + 1) * p)
        if (k & 1) == 0:
            acc = acc + term
        else:
            acc = acc - term
        p = p * m2
    return (acc, acc + Fraction(1, (4 * pairs + 1) * p))


def machin_pi_bracket_q(pairs: int = 7) -> tuple[int, int, int]:
    """Derive conservative integer-scaled [pi_lo_n/pi_den, pi_hi_n/pi_den] bracket for pi via Machin's formula."""
    a5_lo, a5_hi = _arctan_inv_bracket_q(5, pairs)
    a239_lo, a239_hi = _arctan_inv_bracket_q(239, 3)
    m_lo = Fraction(16, 1) * a5_lo - FOUR * a239_hi
    m_hi = Fraction(16, 1) * a5_hi - FOUR * a239_lo
    pi_den = 10**18
    pi_lo_n = (m_lo.numerator * pi_den) // m_lo.denominator
    pi_hi_n = (m_hi.numerator * pi_den + m_hi.denominator - 1) // m_hi.denominator
    return (pi_lo_n, pi_hi_n, pi_den)


PI_LO_N, PI_HI_N, PI_DEN = machin_pi_bracket_q(7)
PI_LO = Fraction(PI_LO_N, PI_DEN)
PI_HI = Fraction(PI_HI_N, PI_DEN)


def canonical_sha256(obj: dict[str, Any]) -> str:
    assert_no_floats_recursive(obj)
    payload = {k: v for k, v in obj.items() if k != "result_sha256"}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


# =============================================================================
# Core Pure-Q/Z Primitives (Zero ast.Div, Zero Float, Zero External Deps)
# =============================================================================

def cf_convergent(terms: tuple[int, ...]) -> Fraction:
    """Evaluate exact finite continued fraction [a0; a1, ..., ak] in Q."""
    require_ok(len(terms) >= 1, "Continued fraction terms must be non-empty")
    val = Fraction(terms[-1], 1)
    for a in reversed(terms[:-1]):
        val = Fraction(a, 1) + q_div(ONE, val)
    return val


def find_first_pi_beater(zu: Fraction, q_min: int, q_max: int) -> tuple[int, int]:
    """Exhaustively scan denominators q in [q_min, q_max] for the earliest fraction strictly closer to pi than zu."""
    require_ok(q_min >= 1, "q_min must be >= 1")
    require_ok(q_max >= q_min, "q_max must be >= q_min")
    pi_den = PI_DEN
    pi_lo_n = PI_LO_N
    pi_hi_n = PI_HI_N
    zu_err_lo_num = zu.numerator * pi_den - zu.denominator * pi_hi_n
    zu_d = zu.denominator
    for q in range(q_min, q_max + 1):
        p0 = (q * pi_lo_n) // pi_den
        for p in (p0, p0 + 1):
            lhs_lo = p * pi_den
            if lhs_lo < q * pi_lo_n:
                err_hi_num = q * pi_hi_n - lhs_lo
            else:
                err_hi_num = lhs_lo - q * pi_lo_n
            if err_hi_num * zu_d < zu_err_lo_num * q:
                return (p, q)
    raise ValueError("No fraction closer to pi found in range")


def greedy_sylvester_egyptian(target: Fraction) -> tuple[int, ...]:
    """Compute exact Fibonacci-Sylvester greedy unit-fraction denominators for 0 < target < 1."""
    require_ok(target > ZERO, "Egyptian fraction target must be > 0")
    require_ok(target < ONE, "Egyptian fraction target must be < 1")
    denoms: list[int] = []
    rem = target
    while rem > ZERO:
        d = (rem.denominator + rem.numerator - 1) // rem.numerator
        denoms.append(d)
        rem = rem - Fraction(1, d)
    return tuple(denoms)


def leibniz_partial_sum_q(n: int) -> Fraction:
    """Exact rational Madhava-Leibniz partial sum S_0(n) = sum_{k=1}^n (-1)^(k-1)/(2k-1)."""
    require_ok(n >= 1, "Leibniz n must be >= 1")
    acc = ZERO
    for k in range(1, n + 1):
        term = Fraction(1, 2 * k - 1)
        if (k & 1) == 1:
            acc = acc + term
        else:
            acc = acc - term
    return acc


def madhava_r1_q(n: int) -> Fraction:
    require_ok(n >= 1, "Madhava R1 n must be >= 1")
    return Fraction(1, 4 * n)


def madhava_r2_q(n: int) -> Fraction:
    require_ok(n >= 1, "Madhava R2 n must be >= 1")
    return Fraction(n, 4 * n * n + 1)


def madhava_r3_q(n: int) -> Fraction:
    require_ok(n >= 1, "Madhava R3 n must be >= 1")
    return Fraction(n * n + 1, 4 * n * n * n + 5 * n)


def madhava_accelerated_pi_q(n: int, order: int) -> Fraction:
    """Return exact rational 4 * (S_0(n) + (-1)^n R_order(n)) for order in {0, 1, 2, 3}."""
    require_ok(order in (0, 1, 2, 3), "Madhava order must be in {0, 1, 2, 3}")
    s0 = leibniz_partial_sum_q(n)
    if order == 0:
        return FOUR * s0
    if order == 1:
        rem = madhava_r1_q(n)
    elif order == 2:
        rem = madhava_r2_q(n)
    else:
        rem = madhava_r3_q(n)
    if (n & 1) == 0:
        return FOUR * (s0 + rem)
    return FOUR * (s0 - rem)


def interval_abs_err_bounds(x: Fraction, lo: Fraction, hi: Fraction) -> tuple[Fraction, Fraction]:
    """Conservative pure-Q [min_err, max_err] for |x - target| given target in [lo, hi]."""
    require_ok(lo <= hi, "Interval bracket must satisfy lo <= hi")
    if x < lo:
        return (lo - x, hi - x)
    if x > hi:
        return (x - hi, x - lo)
    return (ZERO, max(x - lo, hi - x))


def cancellation_kappa_q(x: Fraction) -> tuple[Fraction, int]:
    """Exact subtraction condition number kappa(x) = x / (1 - x) and clamped bit loss max(0, floor(log2(kappa)))."""
    require_ok(x > ZERO, "x must be > 0")
    require_ok(x < ONE, "x must be < 1")
    kappa = q_div(x, ONE - x)
    q_int = kappa.numerator // kappa.denominator
    bit_loss = 0 if q_int == 0 else q_int.bit_length() - 1
    return (kappa, bit_loss)


def kashi_chord_arg_q(k: int) -> Fraction:
    """Al-Kashi chord-doubling half-angle subtraction argument x(k) = 1 - 2^-(2k+2)."""
    require_ok(k >= 1, "Al-Kashi step k must be >= 1")
    shift = 2 * k + 2
    return Fraction((1 << shift) - 1, 1 << shift)


def multiscale_zoom_arg_q(ell: int) -> Fraction:
    """Multiscale quadratic zoom subtraction argument x(ell) = 1 - 2^-(4*ell)."""
    require_ok(ell >= 1, "Zoom level ell must be >= 1")
    shift = 4 * ell
    return Fraction((1 << shift) - 1, 1 << shift)


def stereographic_inverse_s2_q(u: Fraction, v: Fraction) -> Vec3Q:
    """Inverse stereographic map Phi: Q^2 -> S^2(Q) \\ {(0,0,1)} from North Pole."""
    r2 = u * u + v * v
    den = ONE + r2
    return (q_div(TWO * u, den), q_div(TWO * v, den), q_div(r2 - ONE, den))


def stereographic_forward_r2_q(x: Fraction, y: Fraction, z: Fraction) -> tuple[Fraction, Fraction]:
    """Forward stereographic map Pi: S^2(Q) \\ {(0,0,1)} -> Q^2 from North Pole."""
    require_ok(x * x + y * y + z * z == ONE, "Point must lie on unit sphere S^2")
    require_ok(z != ONE, "North Pole (0, 0, 1) excluded from stereographic domain")
    omz = ONE - z
    return (q_div(x, omz), q_div(y, omz))


def cayley_s3_spinor_q(w1: Fraction, w2: Fraction, w3: Fraction) -> QuatQ:
    """Rational Cayley spinor lift (1 + w)^2 / (1 + ||w||^2) in S^3(Q)."""
    r2 = w1 * w1 + w2 * w2 + w3 * w3
    den = ONE + r2
    raw: QuatQ = (ONE, w1, w2, w3)
    sq = q_mul(raw, raw)
    return (q_div(sq[0], den), q_div(sq[1], den), q_div(sq[2], den), q_div(sq[3], den))


def cayley_s3_inverse_q(q: QuatQ) -> Vec3Q:
    """Inverse 3D-from-S^3 stereographic projection from South Pole (-1,0,0,0)."""
    q0, q1, q2, q3 = q
    require_ok(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3 == ONE, "Quaternion must lie on unit S^3")
    require_ok(q0 != Fraction(-1, 1), "South Pole (-1, 0, 0, 0) excluded from Cayley domain")
    op0 = ONE + q0
    return (q_div(q1, op0), q_div(q2, op0), q_div(q3, op0))


PolyZ = dict[tuple[int, ...], int]


def poly_clean(terms: dict[tuple[int, ...], int]) -> PolyZ:
    return {exp: coeff for exp, coeff in terms.items() if coeff != 0}


def poly_add(a: PolyZ, b: PolyZ) -> PolyZ:
    out = dict(a)
    for exp, coeff in b.items():
        out[exp] = out.get(exp, 0) + coeff
    return poly_clean(out)


def poly_sub(a: PolyZ, b: PolyZ) -> PolyZ:
    out = dict(a)
    for exp, coeff in b.items():
        out[exp] = out.get(exp, 0) - coeff
    return poly_clean(out)


def poly_mul(a: PolyZ, b: PolyZ) -> PolyZ:
    out: dict[tuple[int, ...], int] = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            exp = tuple(x + y for x, y in zip(ea, eb))
            out[exp] = out.get(exp, 0) + ca * cb
    return poly_clean(out)


def _poly_const(nvars: int, coeff: int) -> PolyZ:
    if coeff == 0:
        return {}
    return {tuple(0 for _ in range(nvars)): coeff}


def _poly_var(nvars: int, idx: int) -> PolyZ:
    return {tuple(1 if j == idx else 0 for j in range(nvars)): 1}


def certify_stereo_cayley_polynomial_bijections() -> int:
    """Generically prove S^2(Q)\\{N}<->Q^2, S^3(Q)\\{-1}<->Q^3, and equatorial embedding via exact Z-polynomials.

    Returns exact count of verified polynomial identities (19 when all hold identically over Q):
      - Z[u, v]: unit sphere, North Pole exclusion (D - Nz == 2), left inverse Pi(Phi(u,v)) == (u,v) (4 ids)
      - Z[x, y, z] mod (x^2+y^2+z^2-1): right inverse Phi(Pi(x,y,z)) == (x,y,z) for z != 1 (4 ids)
      - Z[w1, w2, w3]: unit S^3, South Pole exclusion (D + N0 == 2), left inverse C^-1(C(w)) == w (5 ids)
      - Z[q0, q1, q2, q3] mod (q0^2+q1^2+q2^2+q3^2-1): right inverse C(C^-1(q)) == q for q0 != -1 (5 ids)
      - Z[u, v]: equatorial embedding cayley_s3(u, v, 0) == (-z, x, y, 0) (1 id)
    """
    # Part A & E: Z[u, v] stereographic S^2 image, pole exclusion, left inverse, and equatorial embedding
    u, v = _poly_var(2, 0), _poly_var(2, 1)
    c1_2, c2_2 = _poly_const(2, 1), _poly_const(2, 2)
    r2_uv = poly_add(poly_mul(u, u), poly_mul(v, v))
    d_uv = poly_add(c1_2, r2_uv)
    nx_uv = poly_mul(c2_2, u)
    ny_uv = poly_mul(c2_2, v)
    nz_uv = poly_sub(r2_uv, c1_2)
    s2_norm_id = poly_sub(
        poly_add(poly_add(poly_mul(nx_uv, nx_uv), poly_mul(ny_uv, ny_uv)), poly_mul(nz_uv, nz_uv)),
        poly_mul(d_uv, d_uv),
    )
    d_minus_nz = poly_sub(d_uv, nz_uv)
    s2_left_u = poly_sub(nx_uv, poly_mul(u, d_minus_nz))
    s2_left_v = poly_sub(ny_uv, poly_mul(v, d_minus_nz))
    n0_eq = poly_sub(c1_2, r2_uv)
    eq_embed_id = poly_add(n0_eq, nz_uv)

    # Part B: Z[x, y, z] right inverse Phi(Pi(x, y, z)) == (x, y, z) modulo S2 = x^2 + y^2 + z^2 - 1
    x, y, z = _poly_var(3, 0), _poly_var(3, 1), _poly_var(3, 2)
    c1_3, c2_3 = _poly_const(3, 1), _poly_const(3, 2)
    omz = poly_sub(c1_3, z)
    omz2 = poly_mul(omz, omz)
    x2y2 = poly_add(poly_mul(x, x), poly_mul(y, y))
    s2_ideal = poly_sub(poly_add(x2y2, poly_mul(z, z)), c1_3)
    d2_clr = poly_add(omz2, x2y2)
    nz_clr = poly_sub(x2y2, omz2)
    d2_on_s2 = poly_sub(d2_clr, s2_ideal)
    two_omz = poly_mul(c2_3, omz)
    s2_right_d = poly_sub(d2_on_s2, two_omz)
    s2_right_x = poly_sub(poly_mul(c2_3, poly_mul(x, omz)), poly_mul(x, d2_on_s2))
    s2_right_y = poly_sub(poly_mul(c2_3, poly_mul(y, omz)), poly_mul(y, d2_on_s2))
    s2_right_z = poly_sub(poly_sub(nz_clr, s2_ideal), poly_mul(z, d2_on_s2))

    # Part C: Z[w1, w2, w3] Cayley spinor S^3 image, pole exclusion, and left inverse
    w1, w2, w3 = _poly_var(3, 0), _poly_var(3, 1), _poly_var(3, 2)
    r2_w = poly_add(poly_add(poly_mul(w1, w1), poly_mul(w2, w2)), poly_mul(w3, w3))
    d_w = poly_add(c1_3, r2_w)
    # Exact symbolic quaternion square (1 + w)^2 = (1 - ||w||^2, 2*w1, 2*w2, 2*w3)
    n0_w = poly_sub(c1_3, r2_w)
    n1_w = poly_add(poly_mul(c1_3, w1), poly_mul(w1, c1_3))
    n2_w = poly_add(poly_mul(c1_3, w2), poly_mul(w2, c1_3))
    n3_w = poly_add(poly_mul(c1_3, w3), poly_mul(w3, c1_3))
    s3_norm_id = poly_sub(
        poly_add(
            poly_add(poly_mul(n0_w, n0_w), poly_mul(n1_w, n1_w)),
            poly_add(poly_mul(n2_w, n2_w), poly_mul(n3_w, n3_w)),
        ),
        poly_mul(d_w, d_w),
    )
    d_plus_n0 = poly_add(d_w, n0_w)
    s3_left_w1 = poly_sub(n1_w, poly_mul(w1, d_plus_n0))
    s3_left_w2 = poly_sub(n2_w, poly_mul(w2, d_plus_n0))
    s3_left_w3 = poly_sub(n3_w, poly_mul(w3, d_plus_n0))

    # Part D: Z[q0, q1, q2, q3] right inverse C(C^-1(q)) == q modulo S3 = q0^2 + q1^2 + q2^2 + q3^2 - 1
    q0, q1, q2, q3 = _poly_var(4, 0), _poly_var(4, 1), _poly_var(4, 2), _poly_var(4, 3)
    c1_4, c2_4 = _poly_const(4, 1), _poly_const(4, 2)
    op0 = poly_add(c1_4, q0)
    op02 = poly_mul(op0, op0)
    qvec2 = poly_add(poly_add(poly_mul(q1, q1), poly_mul(q2, q2)), poly_mul(q3, q3))
    s3_ideal = poly_sub(poly_add(poly_mul(q0, q0), qvec2), c1_4)
    d3_clr = poly_add(op02, qvec2)
    n0_clr = poly_sub(op02, qvec2)
    d3_on_s3 = poly_sub(d3_clr, s3_ideal)
    two_op0 = poly_mul(c2_4, op0)
    s3_right_d = poly_sub(d3_on_s3, two_op0)
    s3_right_q0 = poly_sub(poly_add(n0_clr, s3_ideal), poly_mul(q0, d3_on_s3))
    s3_right_q1 = poly_sub(poly_mul(c2_4, poly_mul(q1, op0)), poly_mul(q1, d3_on_s3))
    s3_right_q2 = poly_sub(poly_mul(c2_4, poly_mul(q2, op0)), poly_mul(q2, d3_on_s3))
    s3_right_q3 = poly_sub(poly_mul(c2_4, poly_mul(q3, op0)), poly_mul(q3, d3_on_s3))

    return sum(
        (
            1 if s2_norm_id == {} else 0,
            1 if d_minus_nz == c2_2 else 0,
            1 if s2_left_u == {} else 0,
            1 if s2_left_v == {} else 0,
            1 if s2_right_d == {} else 0,
            1 if s2_right_x == {} else 0,
            1 if s2_right_y == {} else 0,
            1 if s2_right_z == {} else 0,
            1 if s3_norm_id == {} else 0,
            1 if d_plus_n0 == c2_3 else 0,
            1 if s3_left_w1 == {} else 0,
            1 if s3_left_w2 == {} else 0,
            1 if s3_left_w3 == {} else 0,
            1 if s3_right_d == {} else 0,
            1 if s3_right_q0 == {} else 0,
            1 if s3_right_q1 == {} else 0,
            1 if s3_right_q2 == {} else 0,
            1 if s3_right_q3 == {} else 0,
            1 if eq_embed_id == {} else 0,
        )
    )


def pingala_nasta(n: int, k: int) -> tuple[int, ...]:
    """Authentic Pingala Chandasastra (nasta): 1-based rank k -> n-bit (0=guru, 1=laghu)."""
    require_ok(n >= 1, "Pingala n must be >= 1")
    require_ok(k >= 1, "Pingala rank k must be >= 1")
    require_ok(k <= (1 << n), "Pingala rank k exceeds 2^n")
    bits: list[int] = []
    cur = k
    for _ in range(n):
        if (cur & 1) == 0:
            bits.append(1)
            cur = cur // 2
        else:
            bits.append(0)
            cur = (cur + 1) // 2
    return tuple(bits)


def pingala_uddista(bits: tuple[int, ...]) -> int:
    """Authentic Pingala Chandasastra (uddista): n-bit meter -> 1-based rank k."""
    require_ok(len(bits) >= 1, "Pingala meter must be non-empty")
    acc = 1
    for b in reversed(bits):
        require_ok(b in (0, 1), "Pingala meter bits must be 0 or 1")
        if b == 1:
            acc = 2 * acc
        else:
            acc = 2 * acc - 1
    return acc


def fwht_int(vec: list[int]) -> list[int]:
    """Exact pure-integer Fast Walsh-Hadamard Transform (power-of-2 length)."""
    n = len(vec)
    require_ok(n >= 1, "FWHT input must be non-empty")
    require_ok((n & (n - 1)) == 0, "FWHT length must be a power of 2")
    out = list(vec)
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x = out[j]
                y = out[j + h]
                out[j] = x + y
                out[j + h] = x - y
        h = h * 2
    return out


def build_sivasutra_slots() -> tuple[tuple[str, ...], dict[str, int]]:
    """Flatten authentic 14 Sivasutras into 43 linear slots and marker end-indices."""
    slots: list[str] = []
    marker_end: dict[str, int] = {}
    for _, marker, phones in SIVASUTRAS:
        for p in phones:
            slots.append(p)
        marker_end[marker] = len(slots) - 1
    return (tuple(slots), marker_end)


def decode_pratyahara_interval(
    slots: tuple[str, ...],
    marker_end: dict[str, int],
    start_phoneme: str,
    end_marker: str,
) -> tuple[int, int, frozenset[str]]:
    """Decode a Paninian pratyahara (start_phoneme, end_marker) into contiguous slice & phoneme set."""
    require_ok(end_marker in marker_end, f"Unknown it-marker: {end_marker}")
    end_idx = marker_end[end_marker]
    start_idx = -1
    for idx in range(end_idx + 1):
        if slots[idx] == start_phoneme:
            start_idx = idx
            break
    require_ok(start_idx >= 0, f"Start phoneme {start_phoneme!r} not found before {end_marker!r}")
    return (start_idx, end_idx, frozenset(slots[start_idx : end_idx + 1]))


def is_c1p_interval_on_order(order: tuple[str, ...], target: frozenset[str]) -> bool:
    """Return True iff target equals the phoneme set of some contiguous slice of order."""
    n = len(order)
    for i in range(n):
        if order[i] not in target:
            continue
        seen: set[str] = set()
        for j in range(i, n):
            tok = order[j]
            if tok not in target:
                break
            seen.add(tok)
            if len(seen) == len(target):
                return True
    return False


def mod_inv_int(a: int, m: int) -> int:
    """Exact pure-integer modular inverse a^-1 mod m via iterative Extended Euclidean algorithm (zero pow calls)."""
    require_ok(m >= 1, "mod_inv modulus must be >= 1")
    if m == 1:
        return 0
    r0, r1 = m, a % m
    t0, t1 = 0, 1
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        t0, t1 = t1, t0 - q * t1
    require_ok(r0 == 1, "mod_inv inputs must be coprime")
    return t0 % m


def solve_noncoprime_crt(congruences: tuple[tuple[int, int], ...]) -> tuple[int, int]:
    """Qin Jiushao Dayan exact non-coprime CRT returning (x mod L, L = lcm(m_i)); refuses inconsistency."""
    require_ok(len(congruences) >= 1, "congruences must be non-empty")
    r0, m0 = congruences[0]
    require_ok(m0 >= 1, "CRT modulus must be >= 1")
    x = r0 % m0
    mod = m0
    for ri, mi in congruences[1:]:
        require_ok(mi >= 1, "CRT modulus must be >= 1")
        g = math.gcd(mod, mi)
        diff = ri - x
        require_ok(diff % g == 0, "Inconsistent non-coprime CRT congruences")
        mod_r = mod // g
        mi_r = mi // g
        inv = mod_inv_int(mod_r, mi_r)
        step = ((diff // g) * inv) % mi_r
        x = (x + mod * step) % (mod_r * mi)
        mod = mod_r * mi
    return (x, mod)


def gear_train_ratio(pairs: tuple[tuple[int, int], ...]) -> Fraction:
    """Compute exact product prod_k (driver_k / follower_k) in Q."""
    require_ok(len(pairs) >= 1, "gear train must be non-empty")
    ratio = ONE
    for drv, flw in pairs:
        require_ok(drv >= 1, "driver teeth must be >= 1")
        require_ok(flw >= 1, "follower teeth must be >= 1")
        ratio = ratio * Fraction(drv, flw)
    return ratio


def q_mul(a: QuatQ, b: QuatQ) -> QuatQ:
    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b
    return (
        a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3,
        a0 * b1 + a1 * b0 + a2 * b3 - a3 * b2,
        a0 * b2 - a1 * b3 + a2 * b0 + a3 * b1,
        a0 * b3 + a1 * b2 - a2 * b1 + a3 * b0,
    )


def q_cayley_axis(eps: Fraction, axis: int) -> QuatQ:
    """Exact rational SU(2) Cayley quaternion C(eps * e_axis) = ((1-e^2) + 2e*e_axis) / (1+e^2)."""
    require_ok(axis in (1, 2, 3), "axis must be in {1, 2, 3}")
    e2 = eps * eps
    den = ONE + e2
    q0 = q_div(ONE - e2, den)
    qv = q_div(TWO * eps, den)
    if axis == 1:
        return (q0, qv, ZERO, ZERO)
    if axis == 2:
        return (q0, ZERO, qv, ZERO)
    return (q0, ZERO, ZERO, qv)


def q_diff_norm2(a: QuatQ, b: QuatQ) -> Fraction:
    return sum(((x - y) * (x - y) for x, y in zip(a, b)), ZERO)


def so3_bracket(u: Vec3Q, v: Vec3Q) -> Vec3Q:
    """Exact so(3) Lie bracket [u, v] = u x v satisfying [e_1, e_2] = e_3."""
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def bch_c3_so3(x: Vec3Q, y: Vec3Q) -> Vec3Q:
    """Exact order-3 Baker-Campbell-Hausdorff term (1/12)([x,[x,y]] + [y,[y,x]]) in so(3)."""
    t1 = so3_bracket(x, so3_bracket(x, y))
    t2 = so3_bracket(y, so3_bracket(y, x))
    twelve = Fraction(12, 1)
    return (q_div(t1[0] + t2[0], twelve), q_div(t1[1] + t2[1], twelve), q_div(t1[2] + t2[2], twelve))


def mat_mul_q(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    m = len(a)
    k = len(a[0])
    n = len(b[0])
    return [[sum((a[i][t] * b[t][j] for t in range(k)), ZERO) for j in range(n)] for i in range(m)]


def mat_transpose_q(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a[i][j] for i in range(len(a))] for j in range(len(a[0]))]


def mat3_vec_q(m: list[list[Fraction]], v: Vec3Q) -> Vec3Q:
    return (
        m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2],
        m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2],
        m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2],
    )


def rot_y_q(c: Fraction, s: Fraction) -> list[list[Fraction]]:
    return [[c, ZERO, s], [ZERO, ONE, ZERO], [-s, ZERO, c]]


def rot_z_q(c: Fraction, s: Fraction) -> list[list[Fraction]]:
    return [[c, -s, ZERO], [s, c, ZERO], [ZERO, ZERO, ONE]]


def sona_loop_count_with_wall(m: int, n: int, split_wall: bool, wall_y: int = 1) -> int:
    """Exact Chokwe Sona mirror-curve cycle counter on m x n dot lattice with optional vertical wall at (2, wall_y)."""
    require_ok(m >= 1, "m must be >= 1")
    require_ok(n >= 1, "n must be >= 1")
    w2 = 2 * m
    h2 = 2 * n
    starts: list[tuple[int, int, int, int]] = []
    for cx in range(m):
        px = 2 * cx + 1
        starts.append((px, 0, 1, 1))
        starts.append((px, 0, -1, 1))
        starts.append((px, h2, 1, -1))
        starts.append((px, h2, -1, -1))
    for cy in range(n):
        py = 2 * cy + 1
        starts.append((0, py, 1, 1))
        starts.append((0, py, 1, -1))
        starts.append((w2, py, -1, 1))
        starts.append((w2, py, -1, -1))
    if split_wall:
        require_ok(m >= 2, "split_wall requires m >= 2")
        starts.append((2, wall_y, 1, 1))
        starts.append((2, wall_y, 1, -1))
        starts.append((2, wall_y, -1, 1))
        starts.append((2, wall_y, -1, -1))

    visited: set[int] = set()
    max_steps = 8 * m * n + 16
    loops = 0
    for sx, sy, sdx, sdy in starts:
        key = (sx << 12) | (sy << 2) | (2 if sdx < 0 else 0) | (1 if sdy < 0 else 0)
        if key in visited:
            continue
        x, y, dx, dy = sx, sy, sdx, sdy
        for _ in range(max_steps):
            if key in visited:
                break
            visited.add(key)
            x += dx
            y += dy
            if x == 0 or x == w2:
                dx = -dx
            if y == 0 or y == h2:
                dy = -dy
            if split_wall:
                if x == 2:
                    if y == wall_y:
                        dx = -dx
            key = (x << 12) | (y << 2) | (2 if dx < 0 else 0) | (1 if dy < 0 else 0)
        if key in visited:
            loops += 1
    return loops // 2


def graph_connected_components(n_verts: int, edges: tuple[tuple[int, int], ...]) -> int:
    """Count exact connected components of an undirected graph via iterative BFS."""
    require_ok(n_verts >= 1, "Graph must have >= 1 vertex")
    adj: list[list[int]] = [[] for _ in range(n_verts)]
    for u, v in edges:
        require_ok(0 <= u, "Edge vertex u < 0")
        require_ok(u < n_verts, "Edge vertex u >= n_verts")
        require_ok(0 <= v, "Edge vertex v < 0")
        require_ok(v < n_verts, "Edge vertex v >= n_verts")
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * n_verts
    comps = 0
    for start in range(n_verts):
        if seen[start]:
            continue
        comps += 1
        stack = [start]
        seen[start] = True
        while stack:
            cur = stack.pop()
            for nxt in adj[cur]:
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append(nxt)
    return comps


def graph_betti1(n_verts: int, edges: tuple[tuple[int, int], ...]) -> int:
    """Compute exact first Betti number beta_1(G) = |E| - |V| + c(G)."""
    return len(edges) - n_verts + graph_connected_components(n_verts, edges)


# Canonical Casarabe C_{2,6} (hub 0 + inner 6-ring 1..6 + outer 6-ring 7..12) and spanning tree T_13 adjacency pins
CASARABE_C2_6_EXPECTED_EDGES: frozenset[tuple[int, int]] = frozenset(
    (
        (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
        (1, 7), (2, 8), (3, 9), (4, 10), (5, 11), (6, 12),
        (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (1, 6),
        (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (7, 12),
    )
)
CASARABE_C2_6_EXPECTED_DEGREES: tuple[int, ...] = (6, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3)
TREE_T13_EXPECTED_EDGES: frozenset[tuple[int, int]] = frozenset(
    (
        (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
        (1, 7), (2, 8), (3, 9), (4, 10), (5, 11), (6, 12),
    )
)
TREE_T13_EXPECTED_DEGREES: tuple[int, ...] = (6, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1)


def graph_simple_edges_and_degrees(
    n_verts: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[frozenset[tuple[int, int]], tuple[int, ...]]:
    """Validate simple undirected graph (no self-loops or duplicate edges) and return (canonical_edges, degrees)."""
    require_ok(n_verts >= 1, "Simple graph must have >= 1 vertex")
    degrees = [0] * n_verts
    canon: set[tuple[int, int]] = set()
    for u, v in edges:
        require_ok(0 <= u, "Simple graph vertex u < 0")
        require_ok(u < n_verts, "Simple graph vertex u >= n_verts")
        require_ok(0 <= v, "Simple graph vertex v < 0")
        require_ok(v < n_verts, "Simple graph vertex v >= n_verts")
        require_ok(u != v, "Simple graph forbids self-loops")
        edge = (u, v) if u < v else (v, u)
        require_ok(edge not in canon, "Simple graph forbids duplicate edges")
        canon.add(edge)
        degrees[u] += 1
        degrees[v] += 1
    return (frozenset(canon), tuple(degrees))


def verify_khipu_tree_checksum(node: dict[str, Any]) -> bool:
    """Recursively check that every internal node value equals the exact integer sum of its children."""
    children = node["children"]
    if not children:
        return True
    child_sum = sum(c["value"] for c in children)
    if node["value"] != child_sum:
        return False
    for c in children:
        if not verify_khipu_tree_checksum(c):
            return False
    return True


def schur_3x3_elim_last(
    mat: tuple[tuple[Fraction, ...], ...],
) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    """Exact pure-Q Schur complement A - B D^-1 B^T eliminating index 2 of a 3x3 symmetric matrix."""
    require_ok(len(mat) == 3, "Schur matrix must have exactly 3 rows")
    for row in mat:
        require_ok(len(row) == 3, "Each Schur matrix row must have exactly 3 columns")
    d_val = mat[2][2]
    require_ok(d_val > ZERO, "Schur pivot D must be strictly positive")
    s00 = mat[0][0] - q_div(mat[0][2] * mat[2][0], d_val)
    s01 = mat[0][1] - q_div(mat[0][2] * mat[2][1], d_val)
    s10 = mat[1][0] - q_div(mat[1][2] * mat[2][0], d_val)
    s11 = mat[1][1] - q_div(mat[1][2] * mat[2][1], d_val)
    return ((s00, s01), (s10, s11))


def mat2_det(m: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def exact_rank_q(mat: list[list[Fraction]]) -> int:
    """Exact row-echelon rank over Q using q_div (zero ast.Div)."""
    m = len(mat)
    n = len(mat[0])
    work = [list(row) for row in mat]
    rank = 0
    for col in range(n):
        piv = -1
        for r in range(rank, m):
            if work[r][col] != ZERO:
                piv = r
                break
        if piv == -1:
            continue
        if piv != rank:
            work[rank], work[piv] = work[piv], work[rank]
        pv = work[rank][col]
        for j in range(col, n):
            work[rank][j] = q_div(work[rank][j], pv)
        for r in range(m):
            if r != rank:
                if work[r][col] != ZERO:
                    fac = work[r][col]
                    for j in range(col, n):
                        work[r][j] = work[r][j] - fac * work[rank][j]
        rank += 1
    return rank


def verify_congruence_certificate_q(
    mat: list[list[Fraction]],
    p_mat: list[list[Fraction]],
    diag: list[Fraction],
) -> None:
    """Verify invertible P in GL_n(Q) satisfies P^T M P == diag(d) identically."""
    n = len(mat)
    reconstructed = mat_mul_q(mat_transpose_q(p_mat), mat_mul_q(mat, p_mat))
    expected_diag = [[diag[i] if i == j else ZERO for j in range(n)] for i in range(n)]
    require_ok(reconstructed == expected_diag, "Self-certifying congruence P^T M P == diag(d) failed")
    require_ok(exact_rank_q(p_mat) == n, "Congruence matrix P must be invertible")


def certified_symmetric_inertia_q(mat: list[list[Fraction]]) -> tuple[int, int, int]:
    """Construct invertible P in GL_n(Q) with P^T M P = diag(d), self-certify, and return (n_pos, n_neg, n_zero)."""
    n = len(mat)
    require_ok(n >= 1, "Inertia matrix must be non-empty")
    for row in mat:
        require_ok(len(row) == n, "Inertia matrix must be square")
    for i in range(n):
        for j in range(i + 1, n):
            require_ok(mat[i][j] == mat[j][i], "Inertia matrix must be symmetric")

    work = [list(row) for row in mat]
    p_mat = [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]

    def swap_rc(i: int, j: int) -> None:
        if i == j:
            return
        work[i], work[j] = work[j], work[i]
        for row in work:
            row[i], row[j] = row[j], row[i]
        for row in p_mat:
            row[i], row[j] = row[j], row[i]

    def add_col_row(target: int, src: int, scale: Fraction) -> None:
        if scale == ZERO:
            return
        for r in range(n):
            p_mat[r][target] = p_mat[r][target] + scale * p_mat[r][src]
            work[r][target] = work[r][target] + scale * work[r][src]
        for c in range(n):
            work[target][c] = work[target][c] + scale * work[src][c]

    k = 0
    while k < n:
        piv1 = -1
        for r in range(k, n):
            if work[r][r] != ZERO:
                piv1 = r
                break
        if piv1 != -1:
            swap_rc(k, piv1)
            d_piv = work[k][k]
            for r in range(k + 1, n):
                if work[k][r] != ZERO:
                    add_col_row(r, k, q_div(-work[k][r], d_piv))
            k += 1
            continue
        pair: tuple[int, int] | None = None
        for r in range(k, n):
            for c in range(r + 1, n):
                if work[r][c] != ZERO:
                    pair = (r, c)
                    break
            if pair is not None:
                break
        if pair is None:
            break
        r_idx, c_idx = pair
        swap_rc(k, r_idx)
        swap_rc(k + 1, c_idx)
        add_col_row(k, k + 1, ONE)

    diag = [work[i][i] for i in range(n)]
    verify_congruence_certificate_q(mat, p_mat, diag)

    n_pos = sum(1 for d in diag if d > ZERO)
    n_neg = sum(1 for d in diag if d < ZERO)
    n_zero = sum(1 for d in diag if d == ZERO)
    return (n_pos, n_neg, n_zero)


def kemeny_snell_lumpability_defect_q(
    trans: tuple[tuple[Fraction, ...], ...],
    partition: tuple[tuple[int, ...], ...],
) -> Fraction:
    """Compute exact Kemeny-Snell strong Markov lumpability defect over Q on a stochastic matrix."""
    n = len(trans)
    require_ok(n >= 2, "Markov matrix must have >= 2 states")
    for row in trans:
        require_ok(len(row) == n, "Markov matrix must be square")
        require_ok(sum(row, ZERO) == ONE, "Markov matrix rows must sum to 1")
    max_def = ZERO
    for block_a in partition:
        for block_b in partition:
            lump_probs = [sum((trans[i][k] for k in block_b), ZERO) for i in block_a]
            diff = max(lump_probs) - min(lump_probs)
            if diff > max_def:
                max_def = diff
    return max_def


def antagonistic_joint_torque_q(
    k_ag: Fraction,
    k_an: Fraction,
    q_ag: Fraction,
    q_an: Fraction,
    a_ag: Fraction,
    a_an: Fraction,
    theta: Fraction,
) -> Fraction:
    """Exact linear antagonistic muscle-pair joint torque tau(a_ag, a_an, theta)."""
    return a_ag * k_ag * (q_ag - theta) + a_an * k_an * (q_an - theta)


def pont_beta_sq_h34_q(bin_n: int, total_l: int) -> Fraction:
    """Exact finite-baseline Hurst-3/4 variance factor beta^2(N, L) = sqrt(N)*(1-(L/N)^(-1/2))/(1-L^(-1/2))."""
    require_ok(bin_n >= 1, "bin_n must be >= 1")
    require_ok(total_l > bin_n, "total_l must exceed bin_n")
    require_ok(total_l % bin_n == 0, "total_l must be divisible by bin_n")
    m_bins = total_l // bin_n
    rn = math.isqrt(bin_n)
    rm = math.isqrt(m_bins)
    require_ok(rn * rn == bin_n, "bin_n must be a perfect square for exact Q")
    require_ok(rm * rm == m_bins, "total_l // bin_n must be a perfect square for exact Q")
    rl = rn * rm
    return q_div(Fraction(rn, 1) * (ONE - Fraction(1, rm)), ONE - Fraction(1, rl))


def pont_beta_sq_h12_q(bin_n: int, total_l: int) -> Fraction:
    """Exact finite-sample white-noise (H=1/2) variance factor computed on the length-L Walsh-Rademacher ensemble.

    Explicitly constructs all L orthogonal +-1 sequences of length L (power of 2), computes
    each sequence's empirical mean, contiguous bin_n-block sums, and unbiased sample variance
    both binned (M = L // bin_n) and unbinned (L), then averages across all L realizations to
    return exact beta^2_white(N, L) = N * E[s^2_bin] / E[s^2_raw].
    """
    require_ok(bin_n >= 1, "white-noise bin_n must be >= 1")
    require_ok(total_l > bin_n, "white-noise total_l must exceed bin_n")
    require_ok((total_l & (total_l - 1)) == 0, "white-noise total_l must be a power of 2")
    require_ok(total_l % bin_n == 0, "white-noise total_l must be divisible by bin_n")
    m_bins = total_l // bin_n
    rows: list[list[int]] = [[1]]
    cur = 1
    while cur < total_l:
        rows = [r + r for r in rows] + [r + [-v for v in r] for r in rows]
        cur = cur * 2
    acc_bin = 0
    acc_raw = 0
    l_sq = total_l * total_l
    for seq in rows:
        tot = sum(seq)
        sq_tot = sum(x * x for x in seq)
        acc_raw += l_sq * sq_tot - total_l * tot * tot
        for start in range(0, total_l, bin_n):
            b_sum = sum(seq[start : start + bin_n])
            diff = m_bins * b_sum - tot
            acc_bin += diff * diff
    denom_base = total_l * l_sq
    v_bin = Fraction(acc_bin, denom_base * (m_bins - 1))
    v_raw = Fraction(acc_raw, denom_base * (total_l - 1))
    return q_div(Fraction(bin_n, 1) * v_bin, v_raw)


# Explicit 5x16 Extended Hamming [16, 11, 4] A_16 SECDED parity-check matrix H over GF(2)
A16_H_ROWS: tuple[tuple[int, ...], ...] = (
    tuple(1 for _ in range(16)),
    tuple((j >> 0) & 1 for j in range(16)),
    tuple((j >> 1) & 1 for j in range(16)),
    tuple((j >> 2) & 1 for j in range(16)),
    tuple((j >> 3) & 1 for j in range(16)),
)


def gf2_syndrome_a16(word: int, h_rows: tuple[tuple[int, ...], ...]) -> int:
    """Compute exact 5-bit syndrome H * word^T over GF(2) from explicit 5x16 parity-check rows."""
    require_ok(0 <= word, "A_16 word must be >= 0")
    require_ok(word < 65536, "A_16 word must be < 65536")
    syn = 0
    for r_idx, row in enumerate(h_rows):
        acc = 0
        for j in range(16):
            if row[j] == 1:
                if ((word >> j) & 1) == 1:
                    acc ^= 1
        syn |= acc << r_idx
    return syn


def certify_a16_secded_matrix(h_rows: tuple[tuple[int, ...], ...]) -> dict[str, int]:
    """Certify [16,11,4] SECDED properties directly from the explicit 5x16 matrix H over GF(2)."""
    single_syndromes: set[int] = set()
    for j in range(16):
        s1 = gf2_syndrome_a16(1 << j, h_rows)
        if s1 != 0:
            single_syndromes.add(s1)

    double_disjoint = 0
    for i in range(16):
        for j in range(i + 1, 16):
            s2 = gf2_syndrome_a16((1 << i) ^ (1 << j), h_rows)
            if s2 != 0:
                if s2 not in single_syndromes:
                    double_disjoint += 1

    row_masks = tuple(sum(bit << j for j, bit in enumerate(row)) for row in h_rows)
    codeword_count = 0
    min_nonzero_weight = 17
    for w in range(65536):
        syn = (
            ((w & row_masks[0]).bit_count() & 1)
            | (((w & row_masks[1]).bit_count() & 1) << 1)
            | (((w & row_masks[2]).bit_count() & 1) << 2)
            | (((w & row_masks[3]).bit_count() & 1) << 3)
            | (((w & row_masks[4]).bit_count() & 1) << 4)
        )
        if syn == 0:
            codeword_count += 1
            if w != 0:
                wt = w.bit_count()
                if wt < min_nonzero_weight:
                    min_nonzero_weight = wt

    return {
        "parity_check_rows": z_int(len(h_rows)),
        "code_length": z_int(len(h_rows[0])),
        "distinct_1bit_syndromes": z_int(len(single_syndromes)),
        "nonzero_disjoint_2bit_syndromes": z_int(double_disjoint),
        "codeword_count": z_int(codeword_count),
        "min_nonzero_weight": z_int(min_nonzero_weight),
    }


# =============================================================================
# Pillar 1: 4-Class Aleph_0 -> c Finite-Net Obstruction Taxonomy
# =============================================================================

def certify_four_class_obstructions() -> dict[str, Any]:
    # --- Class A: Diophantine / Prime-Lattice Incommensurability ---
    # 1. Al-Farabi 53-TET prime obstruction: gcd(12, 11) == 1 => 12^53 != 2^7 * 11^53
    farabi_lhs = 12**53
    farabi_rhs = (1 << 7) * (11**53)
    farabi_gap = farabi_rhs - farabi_lhs
    farabi_expected_gap = 427408770020421687429769023309341164189038935654902132096
    farabi_obstructed = (
        sum(
            (
                1 if math.gcd(12, 11) == 1 else 0,
                1 if farabi_lhs % 11 == 1 else 0,
                1 if farabi_rhs % 11 == 0 else 0,
                1 if farabi_gap == farabi_expected_gap else 0,
            )
        )
        == 4
    )
    holder_comma = Fraction(3**53, 1 << 84)
    holder_comma_gt_1 = holder_comma > ONE

    # 2. Zu Chongzhi [3; 7, 15, 1] = 355/113 + exhaustive first beater scan q in [114, 16604]
    zu = cf_convergent((3, 7, 15, 1))
    arch_hi = Fraction(22, 7)
    zu_beats_22_7_floor = (arch_hi - PI_HI) // (zu - PI_LO)
    first_beater_p, first_beater_q = find_first_pi_beater(zu, 114, 16604)

    # 3. Rhind 2/17 and non-2/n Egyptian 5/21 vs computed greedy Sylvester algorithm
    rhind_2_17_denoms = (12, 51, 68)
    greedy_2_17_denoms = greedy_sylvester_egyptian(Fraction(2, 17))
    rhind_2_17_ok = (
        sum(
            (
                1 if sum((Fraction(1, d) for d in rhind_2_17_denoms), ZERO) == Fraction(2, 17) else 0,
                1 if max(rhind_2_17_denoms) < max(greedy_2_17_denoms) else 0,
            )
        )
        == 2
    )
    egypt_5_21_denoms = (6, 14)
    greedy_5_21_denoms = greedy_sylvester_egyptian(Fraction(5, 21))
    egypt_5_21_ok = (
        sum(
            (
                1 if sum((Fraction(1, d) for d in egypt_5_21_denoms), ZERO) == Fraction(5, 21) else 0,
                1 if max(egypt_5_21_denoms) < max(greedy_5_21_denoms) else 0,
            )
        )
        == 2
    )

    # 4. Antikythera additive beat 254*223 - 239*235 == 9*53
    antikythera_beat = 254 * 223 - 239 * 235

    # 5. Kerala School Madhava R_1, R_2, R_3 telescoping identities (n = 2..50) & n = 50 speedup floor
    d1_exact = 0
    d2_exact = 0
    d3_exact = 0
    for n in range(2, 51):
        inv = Fraction(1, 2 * n - 1)
        if madhava_r1_q(n - 1) + madhava_r1_q(n) - inv == Fraction(1, 4 * (2 * n - 1) * (n - 1) * n):
            d1_exact += 1
        if madhava_r2_q(n - 1) + madhava_r2_q(n) - inv == Fraction(-4, (2 * n - 1) * (4 * (n - 1) * (n - 1) + 1) * (4 * n * n + 1)):
            d2_exact += 1
        if madhava_r3_q(n - 1) + madhava_r3_q(n) - inv == Fraction(9, (2 * n - 1) * (n - 1) * n * (4 * (n - 1) * (n - 1) + 5) * (4 * n * n + 5)):
            d3_exact += 1
    pi_50 = [madhava_accelerated_pi_q(50, order) for order in range(4)]
    e0_lo_50, _ = interval_abs_err_bounds(pi_50[0], PI_LO, PI_HI)
    _, e3_hi_50 = interval_abs_err_bounds(pi_50[3], PI_LO, PI_HI)
    madhava_r3_speedup = e0_lo_50 // e3_hi_50
    madhava_enclosure_ok = (
        sum(
            (
                1 if pi_50[2] < PI_LO else 0,
                1 if PI_HI < pi_50[3] else 0,
                1 if pi_50[3] < pi_50[1] else 0,
            )
        )
        == 3
    )

    class_a_checks = sum(
        (
            1 if farabi_obstructed else 0,
            1 if holder_comma_gt_1 else 0,
            1 if zu == Fraction(355, 113) else 0,
            1 if zu_beats_22_7_floor == 4740 else 0,
            1 if (first_beater_p, first_beater_q) == (52163, 16604) else 0,
            1 if rhind_2_17_ok else 0,
            1 if greedy_2_17_denoms == (9, 153) else 0,
            1 if egypt_5_21_ok else 0,
            1 if greedy_5_21_denoms == (5, 27, 945) else 0,
            1 if antikythera_beat == 9 * 53 else 0,
            1 if d1_exact == 49 else 0,
            1 if d2_exact == 49 else 0,
            1 if d3_exact == 49 else 0,
            1 if madhava_enclosure_ok else 0,
            1 if madhava_r3_speedup == 27872151775 else 0,
        )
    )

    # --- Class B: Subtractive Precision Cancellation & Stereographic/Cayley Rational Lift ---
    kb, bb = cancellation_kappa_q(Fraction(215989, 216000))
    r_biruni = Fraction(130411, 200) * kb
    _, kashi_25_b = cancellation_kappa_q(kashi_chord_arg_q(25))
    _, kashi_26_b = cancellation_kappa_q(kashi_chord_arg_q(26))
    _, zoom_13_b = cancellation_kappa_q(multiscale_zoom_arg_q(13))
    _, zoom_14_b = cancellation_kappa_q(multiscale_zoom_arg_q(14))
    _, zoom_16_b = cancellation_kappa_q(multiscale_zoom_arg_q(16))

    # Generic multivariate polynomial bijection proof over Z[u,v], Z[x,y,z], Z[w1,w2,w3], Z[q0,q1,q2,q3]
    stereo_cayley_poly_proof = certify_stereo_cayley_polynomial_bijections()

    # Plus 5-point numerical round-trips exercising the runtime Q^2 <-> S^2(Q) and Q^3 <-> S^3(Q) maps
    stereo_pts = (
        (ZERO, ZERO),
        (ONE, ZERO),
        (Fraction(3, 4), ZERO),
        (Fraction(1, 2), Fraction(2, 3)),
        (Fraction(-5, 3), Fraction(7, 4)),
    )
    stereo_bijection_ok = 0
    stereo_cayley_embed_ok = 0
    for u, v in stereo_pts:
        px, py, pz = stereographic_inverse_s2_q(u, v)
        u_back, v_back = stereographic_forward_r2_q(px, py, pz)
        p_back = stereographic_inverse_s2_q(u_back, v_back)
        if ((u_back, v_back), p_back) == ((u, v), (px, py, pz)):
            stereo_bijection_ok += 1
        q_emb = cayley_s3_spinor_q(u, v, ZERO)
        if q_emb == (-pz, px, py, ZERO):
            stereo_cayley_embed_ok += 1

    cayley_pts = (
        (ZERO, ZERO, ZERO),
        (Fraction(1, 2), ZERO, ZERO),
        (Fraction(1, 2), Fraction(2, 3), ZERO),
        (Fraction(1, 3), Fraction(-1, 4), Fraction(2, 5)),
        (Fraction(-3, 5), Fraction(4, 7), Fraction(-2, 3)),
    )
    cayley_s3_bijection_ok = 0
    for w1, w2, w3 in cayley_pts:
        q_val = cayley_s3_spinor_q(w1, w2, w3)
        w_back = cayley_s3_inverse_q(q_val)
        q_back = cayley_s3_spinor_q(w_back[0], w_back[1], w_back[2])
        if (w_back, q_back) == ((w1, w2, w3), q_val):
            cayley_s3_bijection_ok += 1

    class_b_checks = sum(
        (
            1 if kb == Fraction(215989, 11) else 0,
            1 if bb == 14 else 0,
            1 if r_biruni == Fraction(28167341479, 2200) else 0,
            1 if kashi_25_b == 51 else 0,
            1 if kashi_26_b == 53 else 0,
            1 if zoom_13_b == 51 else 0,
            1 if zoom_14_b == 55 else 0,
            1 if zoom_16_b == 63 else 0,
            1 if stereo_cayley_poly_proof == 19 else 0,
            1 if stereo_bijection_ok == 5 else 0,
            1 if stereo_cayley_embed_ok == 5 else 0,
            1 if cayley_s3_bijection_ok == 5 else 0,
        )
    )

    # --- Class C: Topological Winding, C1P Partition, GF(2) Hypercube & Sheaf H^1 ---
    # 1. Exhaustive Chokwe Sona 576/576 over [1, 24]^2 + 2-opt wall merge/split
    sona_576_exact = 0
    for m in range(1, 25):
        for n in range(1, 25):
            if sona_loop_count_with_wall(m, n, split_wall=False) == math.gcd(m, n):
                sona_576_exact += 1
    sona_2_2_plain = sona_loop_count_with_wall(2, 2, split_wall=False)
    sona_2_2_walled = sona_loop_count_with_wall(2, 2, split_wall=True, wall_y=1)
    sona_2_3_plain = sona_loop_count_with_wall(2, 3, split_wall=False)
    sona_2_3_split = sona_loop_count_with_wall(2, 3, split_wall=True, wall_y=3)

    # 2. Panini 14 Sivasutras 43/43 C1P + Tucker C_3 0/6 + duplicate-h resolution
    slots, marker_end = build_sivasutra_slots()
    distinct_phonemes = frozenset(slots)
    panini_classes: dict[str, frozenset[str]] = {}
    panini_43_exact = 0
    for pname, sp, em, exp_sz in CANONICAL_PRATYAHARAS:
        _, _, pset = decode_pratyahara_interval(slots, marker_end, sp, em)
        panini_classes[pname] = pset
        if len(pset) == exp_sz:
            panini_43_exact += 1
    tucker_u = frozenset(("y", "sh", "h"))
    s_at = panini_classes["aT"] & tucker_u
    s_zal = panini_classes["zal"] & tucker_u
    s_yar = panini_classes["yar"] & tucker_u
    tucker_single_ok = 0
    for perm in (
        ("y", "sh", "h"),
        ("y", "h", "sh"),
        ("sh", "y", "h"),
        ("sh", "h", "y"),
        ("h", "y", "sh"),
        ("h", "sh", "y"),
    ):
        if is_c1p_interval_on_order(perm, s_at):
            if is_c1p_interval_on_order(perm, s_zal):
                if is_c1p_interval_on_order(perm, s_yar):
                    tucker_single_ok += 1
    dup_h_order = ("h", "y", "sh", "h")
    dup_h_resolves = (
        sum(
            (
                1 if is_c1p_interval_on_order(dup_h_order, s_at) else 0,
                1 if is_c1p_interval_on_order(dup_h_order, s_zal) else 0,
                1 if is_c1p_interval_on_order(dup_h_order, s_yar) else 0,
            )
        )
        == 3
    )

    # 3. Pingala nasta/uddista 510/510 + FWHT_256 256/256 + Bamana 65,536/65,536 A_16 SECDED
    pingala_510_exact = 0
    for n in range(1, 9):
        for k in range(1, (1 << n) + 1):
            bits = pingala_nasta(n, k)
            if pingala_uddista(bits) == k:
                if sum(bits[j] << j for j in range(n)) == k - 1:
                    pingala_510_exact += 1
    sig = [((i * 37 + 11) % 19) - 9 for i in range(256)]
    hat = fwht_int(sig)
    inv = fwht_int(hat)
    fwht_involution_exact = sum(1 for a, b in zip(sig, inv) if b == 256 * a)
    fwht_parity_exact = 0
    for x in range(256):
        acc = 0
        for y in range(256):
            if ((x & y).bit_count() & 1) == 0:
                acc += sig[y]
            else:
                acc -= sig[y]
        if acc == hat[x]:
            fwht_parity_exact += 1

    # Explicit 5x16 Extended Hamming [16,11,4] A_16 SECDED parity-check matrix H verification
    a16_matrix = certify_a16_secded_matrix(A16_H_ROWS)
    a16_masks = tuple(sum(bit << j for j, bit in enumerate(row)) for row in A16_H_ROWS)

    # Bamana 4x4 tableau: (wr ^ wl) has even weight by F_2 parity-conservation identity
    # (row-XOR parity == col-XOR parity == total bit-weight mod 2), paired with 5-bit A_16 syndrome correspondence.
    bamana_even_judge_parity_identity = 0
    bamana_a16_exact = 0
    for w in range(65536):
        m0 = w & 0xF
        m1 = (w >> 4) & 0xF
        m2 = (w >> 8) & 0xF
        m3 = (w >> 12) & 0xF
        d0 = (m0 & 1) | ((m1 & 1) << 1) | ((m2 & 1) << 2) | ((m3 & 1) << 3)
        d1 = ((m0 >> 1) & 1) | (((m1 >> 1) & 1) << 1) | (((m2 >> 1) & 1) << 2) | (((m3 >> 1) & 1) << 3)
        d2 = ((m0 >> 2) & 1) | (((m1 >> 2) & 1) << 1) | (((m2 >> 2) & 1) << 2) | (((m3 >> 2) & 1) << 3)
        d3 = ((m0 >> 3) & 1) | (((m1 >> 3) & 1) << 1) | (((m2 >> 3) & 1) << 2) | (((m3 >> 3) & 1) << 3)
        n1 = m2 ^ m3
        n3 = d2 ^ d3
        wr = m0 ^ m1 ^ n1
        wl = d0 ^ d1 ^ n3
        if ((wr ^ wl).bit_count() & 1) == 0:
            bamana_even_judge_parity_identity += 1
        p0 = (w & a16_masks[0]).bit_count() & 1
        a16_match = (
            (p0 ^ (wr.bit_count() & 1))
            | (p0 ^ (wl.bit_count() & 1))
            | (((w & a16_masks[1]).bit_count() & 1) ^ ((d1 ^ d3).bit_count() & 1))
            | (((w & a16_masks[2]).bit_count() & 1) ^ (n3.bit_count() & 1))
            | (((w & a16_masks[3]).bit_count() & 1) ^ ((m1 ^ m3).bit_count() & 1))
            | (((w & a16_masks[4]).bit_count() & 1) ^ (n1.bit_count() & 1))
        )
        if a16_match == 0:
            bamana_a16_exact += 1

    # 4. Z_2 twisted 3-cycle sheaf H^1
    twisted_sections = 0
    untwisted_sections = 0
    for s0 in (-1, 1):
        for s1 in (-1, 1):
            for s2 in (-1, 1):
                if s0 * s1 == 1:
                    if s1 * s2 == 1:
                        if s2 * s0 == -1:
                            twisted_sections += 1
                        if s2 * s0 == 1:
                            untwisted_sections += 1

    # 5. Explicit Casarabe C_{2,6} graph (13 verts, pinned 24-edge adjacency & degrees) vs spanning tree T_13 + cut resilience & khipu tree checksum
    casarabe_edges: tuple[tuple[int, int], ...] = (
        tuple((0, i) for i in range(1, 7))
        + tuple((i, i + 6) for i in range(1, 7))
        + tuple((i, (i % 6) + 1) for i in range(1, 7))
        + tuple((i + 6, (i % 6) + 7) for i in range(1, 7))
    )
    tree_edges: tuple[tuple[int, int], ...] = (
        tuple((0, i) for i in range(1, 7)) + tuple((i, i + 6) for i in range(1, 7))
    )
    casarabe_edge_set, casarabe_degrees = graph_simple_edges_and_degrees(13, casarabe_edges)
    tree_edge_set, tree_degrees = graph_simple_edges_and_degrees(13, tree_edges)
    casarabe_adjacency_exact = (
        casarabe_edge_set == CASARABE_C2_6_EXPECTED_EDGES,
        casarabe_degrees == CASARABE_C2_6_EXPECTED_DEGREES,
        tree_edge_set == TREE_T13_EXPECTED_EDGES,
        tree_degrees == TREE_T13_EXPECTED_DEGREES,
    ) == (True, True, True, True)
    casarabe_betti1 = graph_betti1(13, casarabe_edges)
    tree_betti1 = graph_betti1(13, tree_edges)
    casarabe_cut_comps = graph_connected_components(13, casarabe_edges[1:])
    tree_cut_comps = graph_connected_components(13, tree_edges[1:])

    khipu_valid_tree = {
        "value": 157,
        "children": [
            {"value": 45, "children": [{"value": 20, "children": []}, {"value": 25, "children": []}]},
            {"value": 112, "children": [{"value": 60, "children": []}, {"value": 52, "children": []}]},
        ],
    }
    khipu_tampered_tree = {
        "value": 157,
        "children": [
            {"value": 45, "children": [{"value": 21, "children": []}, {"value": 25, "children": []}]},
            {"value": 112, "children": [{"value": 60, "children": []}, {"value": 52, "children": []}]},
        ],
    }
    khipu_valid_ok = verify_khipu_tree_checksum(khipu_valid_tree)
    khipu_tamper_caught = not verify_khipu_tree_checksum(khipu_tampered_tree)

    class_c_checks = sum(
        (
            1 if sona_576_exact == 576 else 0,
            1 if (sona_2_2_plain, sona_2_2_walled, sona_2_3_plain, sona_2_3_split) == (2, 1, 1, 2) else 0,
            1 if panini_43_exact == 43 else 0,
            1 if tucker_single_ok == 0 else 0,
            1 if dup_h_resolves else 0,
            1 if pingala_510_exact == 510 else 0,
            1 if fwht_involution_exact == 256 else 0,
            1 if fwht_parity_exact == 256 else 0,
            1 if bamana_even_judge_parity_identity == 65536 else 0,
            1 if bamana_a16_exact == 65536 else 0,
            1 if a16_matrix["distinct_1bit_syndromes"] == 16 else 0,
            1 if a16_matrix["nonzero_disjoint_2bit_syndromes"] == 120 else 0,
            1 if a16_matrix["codeword_count"] == 2048 else 0,
            1 if a16_matrix["min_nonzero_weight"] == 4 else 0,
            1 if (twisted_sections, untwisted_sections) == (0, 2) else 0,
            1 if casarabe_adjacency_exact else 0,
            1 if (casarabe_betti1, tree_betti1) == (12, 0) else 0,
            1 if (casarabe_cut_comps, tree_cut_comps) == (1, 2) else 0,
            1 if (khipu_valid_ok, khipu_tamper_caught) == (True, True) else 0,
        )
    )

    # --- Class D: Commutation, Schur Inertia & Coarse-Graining Defect ---
    sig_unreadable = (
        (Fraction(17, 50), ZERO, ZERO),
        (ZERO, Fraction(4, 25), ZERO),
        (ZERO, ZERO, TWO),
    )
    sig_readable = (
        (Fraction(17, 50), ZERO, Fraction(9, 25)),
        (ZERO, Fraction(4, 25), ZERO),
        (Fraction(9, 25), ZERO, TWO),
    )
    sch_un = schur_3x3_elim_last(sig_unreadable)
    sch_rd = schur_3x3_elim_last(sig_readable)
    det_un = mat2_det(sch_un)
    det_rd = mat2_det(sch_rd)
    trace_drop = (sch_un[0][0] + sch_un[1][1]) - (sch_rd[0][0] + sch_rd[1][1])

    # Explicit 8x8 Sylvester-Hadamard master stress 2*I_8 + H_8 vs 8x8 passive hydraulic Laplacian
    h8_int = [[1]]
    for _ in range(3):
        h8_int = [r + r for r in h8_int] + [r + [-v for v in r] for r in h8_int]
    sigma_h8 = [
        [Fraction(h8_int[i][j] + (2 if i == j else 0), 1) for j in range(8)]
        for i in range(8)
    ]
    hyd_lap_8 = [[ZERO for _ in range(8)] for _ in range(8)]
    for u in range(7):
        hyd_lap_8[u][u] = hyd_lap_8[u][u] + TWO
        hyd_lap_8[u + 1][u + 1] = hyd_lap_8[u + 1][u + 1] + TWO
        hyd_lap_8[u][u + 1] = hyd_lap_8[u][u + 1] - TWO
        hyd_lap_8[u + 1][u] = hyd_lap_8[u + 1][u] - TWO
    inertia_h8 = certified_symmetric_inertia_q(sigma_h8)
    inertia_hyd8 = certified_symmetric_inertia_q(hyd_lap_8)
    inertia_separated = (inertia_h8, inertia_hyd8) == ((4, 4, 0), (7, 0, 1))

    # Explicit 4x4 row-stochastic Markov chains for Kemeny-Snell strong lumpability
    p_lumpable = (
        (Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(1, 4)),
        (Fraction(3, 8), Fraction(1, 8), Fraction(1, 8), Fraction(3, 8)),
        (Fraction(1, 2), ZERO, Fraction(1, 4), Fraction(1, 4)),
        (Fraction(1, 4), Fraction(1, 4), Fraction(1, 2), ZERO),
    )
    p_nonlumpable = (
        (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4), ZERO),
        (Fraction(1, 8), Fraction(1, 8), Fraction(1, 2), Fraction(1, 4)),
        (Fraction(1, 2), ZERO, Fraction(1, 2), ZERO),
        (Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(1, 4)),
    )
    part_2x2 = ((0, 1), (2, 3))
    delta_lumpable = kemeny_snell_lumpability_defect_q(p_lumpable, part_2x2)
    delta_nonlumpable = kemeny_snell_lumpability_defect_q(p_nonlumpable, part_2x2)

    # Exact SU(2) Cayley Lie-Trotter defect vs full palindromic Strang quaternion at eps = 1/4
    eps = Fraction(1, 4)
    u_i = q_cayley_axis(q_div(eps, TWO), 1)
    u_j = q_cayley_axis(q_div(eps, TWO), 2)
    u_i_half = q_cayley_axis(q_div(eps, FOUR), 1)
    trotter_defect = q_diff_norm2(q_mul(u_i, u_j), q_mul(u_j, u_i))
    strang_q = q_mul(q_mul(u_i_half, u_j), u_i_half)
    expected_strang_q: QuatQ = (Fraction(4032063, 4293185), Fraction(205632, 858637), Fraction(16, 65), ZERO)

    class_d_checks = sum(
        (
            1 if det_un == Fraction(34, 625) else 0,
            1 if det_rd == Fraction(688, 15625) else 0,
            1 if trace_drop == Fraction(81, 1250) else 0,
            1 if inertia_separated else 0,
            1 if delta_lumpable == ZERO else 0,
            1 if delta_nonlumpable == Fraction(1, 2) else 0,
            1 if trotter_defect == Fraction(262144, 17850625) else 0,
            1 if strang_q == expected_strang_q else 0,
        )
    )

    return {
        "class_a_diophantine_checks_ok": z_int(class_a_checks),
        "class_a_diophantine_checks_total": 15,
        "class_a_farabi_obstructed": farabi_obstructed,
        "class_a_holder_comma_gt_1": holder_comma_gt_1,
        "class_a_farabi_gap": str(z_int(farabi_gap)),
        "class_a_zu_beats_22_7_floor": z_int(zu_beats_22_7_floor),
        "class_a_zu_first_beater": f"{z_int(first_beater_p)}/{z_int(first_beater_q)}",
        "class_a_rhind_2_17_denoms": [z_int(d) for d in rhind_2_17_denoms],
        "class_a_greedy_2_17_denoms": [z_int(d) for d in greedy_2_17_denoms],
        "class_a_egypt_5_21_denoms": [z_int(d) for d in egypt_5_21_denoms],
        "class_a_greedy_5_21_denoms": [z_int(d) for d in greedy_5_21_denoms],
        "class_a_rhind_beats_greedy": (rhind_2_17_ok, egypt_5_21_ok) == (True, True),
        "class_a_antikythera_beat_9_times_53": z_int(antikythera_beat),
        "class_a_madhava_telescoping_counts": [z_int(d1_exact), z_int(d2_exact), z_int(d3_exact)],
        "class_a_madhava_r3_n50_speedup_floor": z_int(madhava_r3_speedup),
        "class_b_cancellation_checks_ok": z_int(class_b_checks),
        "class_b_cancellation_checks_total": 12,
        "class_b_biruni_kappa": q_str(kb),
        "class_b_bit_losses": {
            "biruni": z_int(bb),
            "kashi_25": z_int(kashi_25_b),
            "kashi_26": z_int(kashi_26_b),
            "zoom_13": z_int(zoom_13_b),
            "zoom_14": z_int(zoom_14_b),
            "zoom_16": z_int(zoom_16_b),
        },
        "class_b_stereo_cayley_poly_proof_identities": z_int(stereo_cayley_poly_proof),
        "class_b_stereo_s2_roundtrip_count": z_int(stereo_bijection_ok),
        "class_b_stereo_cayley_embed_count": z_int(stereo_cayley_embed_ok),
        "class_b_cayley_s3_roundtrip_count": z_int(cayley_s3_bijection_ok),
        "class_c_topological_checks_ok": z_int(class_c_checks),
        "class_c_topological_checks_total": 19,
        "class_c_sona_576_exact_count": z_int(sona_576_exact),
        "class_c_sona_wall_surgery_2x2_2x3": [
            z_int(sona_2_2_plain),
            z_int(sona_2_2_walled),
            z_int(sona_2_3_plain),
            z_int(sona_2_3_split),
        ],
        "class_c_panini_43_c1p_count": z_int(panini_43_exact),
        "class_c_tucker_c3_single_copy_orders": z_int(tucker_single_ok),
        "class_c_dup_h_resolves": dup_h_resolves,
        "class_c_pingala_510_bijection_count": z_int(pingala_510_exact),
        "class_c_fwht256_involution_and_parity": [z_int(fwht_involution_exact), z_int(fwht_parity_exact)],
        "class_c_bamana_65536_parity_identity_and_a16": [z_int(bamana_even_judge_parity_identity), z_int(bamana_a16_exact)],
        "class_c_a16_secded_matrix": a16_matrix,
        "class_c_z2_twisted_vs_untwisted_sections": [z_int(twisted_sections), z_int(untwisted_sections)],
        "class_c_casarabe_adjacency_exact": casarabe_adjacency_exact,
        "class_c_casarabe_degree_sequence": [z_int(d) for d in casarabe_degrees],
        "class_c_casarabe_graph_counts": [13, z_int(len(casarabe_edges)), z_int(len(tree_edges))],
        "class_c_casarabe_vs_tree_betti1": [z_int(casarabe_betti1), z_int(tree_betti1)],
        "class_c_casarabe_vs_tree_cut_comps": [z_int(casarabe_cut_comps), z_int(tree_cut_comps)],
        "class_c_khipu_valid_and_tamper": [khipu_valid_ok, khipu_tamper_caught],
        "class_d_commutation_checks_ok": z_int(class_d_checks),
        "class_d_commutation_checks_total": 8,
        "class_d_schur_det_unreadable_to_readable": [q_str(det_un), q_str(det_rd)],
        "class_d_schur_trace_drop": q_str(trace_drop),
        "class_d_inertia_h8_vs_hydraulic8": [[z_int(v) for v in inertia_h8], [z_int(v) for v in inertia_hyd8]],
        "class_d_kemeny_snell_lumpability_defects": [q_str(delta_lumpable), q_str(delta_nonlumpable)],
        "class_d_trotter_defect_eps_1_4": q_str(trotter_defect),
        "class_d_strang_quaternion_eps_1_4": [q_str(c) for c in strang_q],
        "panini_slot_and_phoneme_counts": [
            z_int(len(slots)),
            z_int(len(distinct_phonemes)),
            z_int(len(CANONICAL_PRATYAHARAS)),
            z_int(len(SIVASUTRAS)),
        ],
    }


# =============================================================================
# Pillar 2: Subtractive Selection & Opposing-Pair Conservation
# =============================================================================

def certify_opposing_pair_conservation() -> dict[str, Any]:
    # 1. Al-Tusi planar couple from explicit 2x2 counter-rotating orthogonal matrices
    cos_a, sin_a = Fraction(4, 5), Fraction(3, 5)
    m_plus = [[cos_a, -sin_a], [sin_a, cos_a]]
    m_minus = [[cos_a, sin_a], [-sin_a, cos_a]]
    m_avg = [
        [q_div(m_plus[r][c] + m_minus[r][c], TWO) for c in range(2)]
        for r in range(2)
    ]
    al_tusi_planar_orth = (
        mat_mul_q(mat_transpose_q(m_plus), m_plus),
        mat_mul_q(mat_transpose_q(m_minus), m_minus),
    ) == ([[ONE, ZERO], [ZERO, ONE]], [[ONE, ZERO], [ZERO, ONE]])
    al_tusi_planar_curl = m_avg[0][1]

    # 2. Spherical S^2 Al-Tusi hippopede via explicit 3x3 SO(3) matrix product
    # R_z(theta) R_y(alpha) R_z(-2*theta) R_y(alpha) e_3 at (cos a, sin a) = (4/5, 3/5), (cos t, sin t) = (4/5, 3/5)
    cos_2t = cos_a * cos_a - sin_a * sin_a
    sin_2t = TWO * sin_a * cos_a
    r_s2 = mat_mul_q(
        rot_z_q(cos_a, sin_a),
        mat_mul_q(
            rot_y_q(cos_a, sin_a),
            mat_mul_q(rot_z_q(cos_2t, -sin_2t), rot_y_q(cos_a, sin_a)),
        ),
    )
    s2_pt = mat3_vec_q(r_s2, (ZERO, ZERO, ONE))
    al_tusi_s2_hippopede = abs(s2_pt[1])

    # 3. Order-3 BCH C_3(e_1, 2*e_2) computed directly from so(3) Lie bracket
    c3_vec = bch_c3_so3((ONE, ZERO, ZERO), (ZERO, TWO, ZERO))
    c3_norm2 = sum((x * x for x in c3_vec), ZERO)

    # 4. Collinear SU(2) palindromic Strang exact quaternion & zero defect
    eps = Fraction(1, 4)
    u1_half = q_cayley_axis(q_div(eps, FOUR), 1)
    u2_col = q_cayley_axis(eps, 1)
    col_strang = q_mul(q_mul(u1_half, u2_col), u1_half)
    col_ref = q_mul(u2_col, q_mul(u1_half, u1_half))
    collinear_defect = q_diff_norm2(col_strang, col_ref)
    expected_col_q: QuatQ = (Fraction(829455, 1122833), Fraction(756808, 1122833), ZERO, ZERO)

    # 5. Dimensionless structural Coulomb hysteresis loop area (geometric damping model)
    fy, uy, eta = Fraction(12, 1), Fraction(4, 1), Fraction(3, 2)
    u_max = eta * uy
    dougong_loop_area = FOUR * fy * (u_max - uy)
    dougong_elastic_ref = q_div(fy * u_max, TWO)
    dougong_pi_zeta = q_div(dougong_loop_area, FOUR * dougong_elastic_ref)

    # 6. Machu Picchu slender-ashlar Housner rocking (1963)
    bh = Fraction(1, 3)
    sin2_alpha = q_div(bh * bh, ONE + bh * bh)
    housner_factor = ONE - Fraction(3, 2) * sin2_alpha
    housner_r = housner_factor * housner_factor
    housner_loss = ONE - housner_r

    # 7. Antagonistic joint torque equilibrium, restoring stiffness & vanishing mixed coupling H_ant = 0
    k_eq = Fraction(3, 2)
    a_half = Fraction(1, 2)
    h_step = Fraction(1, 8)
    antag_bal_torque = antagonistic_joint_torque_q(k_eq, k_eq, ONE, Fraction(-1, 1), a_half, a_half, ZERO)
    antag_displaced_torque = antagonistic_joint_torque_q(k_eq, k_eq, ONE, Fraction(-1, 1), a_half, a_half, Fraction(1, 3))
    antag_h_mixed = (
        antagonistic_joint_torque_q(k_eq, k_eq, ONE, Fraction(-1, 1), a_half + h_step, a_half + h_step, ZERO)
        - antagonistic_joint_torque_q(k_eq, k_eq, ONE, Fraction(-1, 1), a_half + h_step, a_half - h_step, ZERO)
        - antagonistic_joint_torque_q(k_eq, k_eq, ONE, Fraction(-1, 1), a_half - h_step, a_half + h_step, ZERO)
        + antagonistic_joint_torque_q(k_eq, k_eq, ONE, Fraction(-1, 1), a_half - h_step, a_half - h_step, ZERO)
    )

    # 8. Explicit 3x3 orthogonal Cayley steering matrix R_plane(1/2) vs xz-plane rotation R_tan(1/2)
    c_steer = Fraction(1, 2)
    c2 = c_steer * c_steer
    cos_c = q_div(ONE - c2, ONE + c2)
    sin_c = q_div(TWO * c_steer, ONE + c2)
    r_plane = rot_z_q(cos_c, sin_c)
    r_tan = rot_y_q(cos_c, sin_c)
    r_plane_orth = mat_mul_q(mat_transpose_q(r_plane), r_plane) == [[ONE, ZERO, ZERO], [ZERO, ONE, ZERO], [ZERO, ZERO, ONE]]
    h_vec: Vec3Q = (Fraction(3, 5), ZERO, Fraction(4, 5))
    h_plane = mat3_vec_q(r_plane, h_vec)
    plane_norm2 = sum((x * x for x in h_plane), ZERO)
    plane_orth_retention = q_div(h_plane[2], h_vec[2])
    e3_tan = mat3_vec_q(r_tan, (ZERO, ZERO, ONE))
    tan_orth_sq_retention = e3_tan[2] * e3_tan[2]

    h2_checks = sum(
        (
            1 if (al_tusi_planar_orth, m_avg[0][0], al_tusi_planar_curl) == (True, cos_a, ZERO) else 0,
            1 if al_tusi_s2_hippopede == Fraction(288, 3125) else 0,
            1 if (c3_vec, c3_norm2) == ((Fraction(-1, 3), Fraction(-1, 6), ZERO), Fraction(5, 36)) else 0,
            1 if (collinear_defect, col_strang) == (ZERO, expected_col_q) else 0,
            1 if dougong_loop_area == Fraction(96, 1) else 0,
            1 if dougong_pi_zeta == Fraction(2, 3) else 0,
            1 if sin2_alpha == Fraction(1, 10) else 0,
            1 if housner_r == Fraction(289, 400) else 0,
            1 if housner_loss == Fraction(111, 400) else 0,
            1 if (antag_bal_torque, antag_displaced_torque, antag_h_mixed) == (ZERO, Fraction(-1, 2), ZERO) else 0,
            1 if (r_plane_orth, plane_norm2) == (True, ONE) else 0,
            1 if plane_orth_retention == ONE else 0,
            1 if tan_orth_sq_retention == Fraction(9, 25) else 0,
        )
    )

    return {
        "opposing_pair_checks_ok": z_int(h2_checks),
        "opposing_pair_checks_total": 13,
        "dougong_loop_area": q_str(dougong_loop_area),
        "housner_b_over_h": q_str(bh),
        "abelian_zero_residual_witnesses": {
            "al_tusi_planar_curl": q_str(al_tusi_planar_curl),
            "collinear_strang_defect": q_str(collinear_defect),
            "antagonistic_balanced_net_torque": q_str(antag_bal_torque),
            "antagonistic_mixed_coupling_h_ant": q_str(antag_h_mixed),
            "cayley_2dplane_orth_retention": q_str(plane_orth_retention),
        },
        "nonabelian_or_dissipative_nonzero_witnesses": {
            "al_tusi_s2_hippopede_py": q_str(al_tusi_s2_hippopede),
            "bch_c3_e1_2e2_vec": [q_str(c) for c in c3_vec],
            "spinor_hippopede_c3_norm2": q_str(c3_norm2),
            "dougong_pi_zeta": q_str(dougong_pi_zeta),
            "machu_picchu_housner_loss": q_str(housner_loss),
            "cayley_tangent_orth_sq_retention": q_str(tan_orth_sq_retention),
        },
    }


# =============================================================================
# Pillar 3: Intrinsic Modular Flow & Minimal Sufficient Partition
# =============================================================================

def certify_modular_flow_and_partition(panini_counts: list[int]) -> dict[str, Any]:
    # 1. Qin Jiushao non-coprime CRT exhaustive isomorphism Z/37960Z <-> compatible subgroup of Z/260Z x Z/365Z x Z/584Z
    maya_moduli = (260, 365, 584)
    maya_residues = (125, 300, 81)
    x_maya, lcm_maya = solve_noncoprime_crt(((125, 260), (300, 365), (81, 584)))
    crt_roundtrip_ok = tuple(x_maya % m for m in maya_moduli) == maya_residues
    # Exhaustive forward + inverse check across ALL 37,960 elements of Z/37960Z onto compatible subgroup
    # G_compat = {(r1, r2, r3) : r1 == r2 (mod 5), r2 == r3 (mod 73), r1 == r3 (mod 4)}, |G_compat| = 260*365*584 / 1460 = 37960
    crt_bijection_all = 0
    for sample_x in range(lcm_maya):
        r1 = sample_x % 260
        r2 = sample_x % 365
        r3 = sample_x % 584
        compat = (r1 % 5 == r2 % 5, r2 % 73 == r3 % 73, r1 % 4 == r3 % 4) == (True, True, True)
        if compat:
            re_x, re_lcm = solve_noncoprime_crt(((r1, 260), (r2, 365), (r3, 584)))
            if (re_x, re_lcm) == (sample_x, lcm_maya):
                crt_bijection_all += 1

    gcd_th = math.gcd(260, 365)
    lcm_th = (260 * 365) // gcd_th
    gcd_vh = math.gcd(584, 365)
    lcm_vh = (584 * 365) // gcd_vh
    gcd_tv = math.gcd(260, 584)
    phase_compression = (260 * 365 * 584) // lcm_maya
    compat_subgroup_order = (260 * 365 * 584) // (gcd_th * gcd_vh * gcd_tv)
    dresden_gcd = math.gcd(11960, 405)
    dresden_ratio = Fraction(11960, 405)

    inconsistent_rejected = False
    try:
        solve_noncoprime_crt(((0, 260), (1, 365)))
    except ValueError:
        inconsistent_rejected = True

    # 2. Antikythera gear trains via gear_train_ratio
    metonic = gear_train_ratio(((64, 38), (48, 24), (127, 32)))
    synodic = metonic - ONE
    turntable = gear_train_ratio(((64, 38), (53, 96), (27, 223)))
    anomalistic = metonic - turntable
    saros_prod = Fraction(235, 19) * Fraction(239, 223)

    # 3. Exact finite-baseline two-clock Hurst-3/4 variance shift vs explicit Walsh-Rademacher white-noise ensemble
    beta2_h34_t1 = pont_beta_sq_h34_q(16, 1024)
    beta2_h34_t2 = pont_beta_sq_h34_q(256, 1024)
    delta_beta2_record = beta2_h34_t2 - beta2_h34_t1
    beta2_white_t1 = pont_beta_sq_h12_q(16, 1024)
    beta2_white_t2 = pont_beta_sq_h12_q(256, 1024)
    delta_beta2_white = beta2_white_t2 - beta2_white_t1

    # 4. Panini C1P fixed-width binary encoding costs derived from decoded Sivasutra counts:
    #    - Naive dense bitmask: 1 bit per distinct phoneme (42 bits/class -> 43 * 42 = 1,806 bits).
    #    - Fixed-width phoneme ID: ceil(log2(42)) = 6 bits/slot (2^5 < 42 <= 2^6) -> 43 * 6 = 258-bit slot table.
    #    - Fixed-width it-marker ID: ceil(log2(14)) = 4 bits/marker (2^3 < 14 <= 2^4).
    #    - Pratyahara descriptor (start_phoneme_id, end_marker_id): 6 + 4 = 10 bits/class -> 43 * 10 = 430 bits.
    n_slots, n_phonemes, n_classes, n_markers = panini_counts
    phoneme_id_bits = (n_phonemes - 1).bit_length()
    marker_id_bits = (n_markers - 1).bit_length()
    descriptor_bits_per_class = phoneme_id_bits + marker_id_bits
    naive_bits = n_classes * n_phonemes
    desc_bits = n_classes * descriptor_bits_per_class
    table_bits = n_slots * phoneme_id_bits
    total_bits = desc_bits + table_bits
    panini_desc_ratio = Fraction(naive_bits, desc_bits)
    panini_total_ratio = Fraction(naive_bits, total_bits)

    h3_checks = sum(
        (
            1 if (x_maya, crt_roundtrip_ok) == (12345, True) else 0,
            1 if (crt_bijection_all, compat_subgroup_order) == (37960, 37960) else 0,
            1 if lcm_maya == 37960 else 0,
            1 if (gcd_th, gcd_vh, gcd_tv, lcm_th, lcm_vh) == (5, 73, 4, 18980, 2920) else 0,
            1 if phase_compression == 1460 else 0,
            1 if (dresden_gcd, dresden_ratio) == (5, Fraction(2392, 81)) else 0,
            1 if inconsistent_rejected else 0,
            1 if metonic == Fraction(254, 19) else 0,
            1 if synodic == Fraction(235, 19) else 0,
            1 if turntable == Fraction(477, 4237) else 0,
            1 if anomalistic == saros_prod else 0,
            1 if (beta2_h34_t1, beta2_h34_t2) == (Fraction(112, 31), Fraction(256, 31)) else 0,
            1 if (delta_beta2_record, beta2_white_t1, beta2_white_t2, delta_beta2_white) == (Fraction(144, 31), ONE, ONE, ZERO) else 0,
            1 if panini_desc_ratio == Fraction(21, 5) else 0,
            1 if panini_total_ratio == Fraction(21, 8) else 0,
        )
    )

    return {
        "modular_flow_checks_ok": z_int(h3_checks),
        "modular_flow_checks_total": 15,
        "maya_crt_solution_mod_37960": z_int(x_maya),
        "maya_crt_bijection_exhaustive_ok": z_int(crt_bijection_all),
        "maya_compatible_subgroup_order": z_int(compat_subgroup_order),
        "maya_grand_sync_lcm": z_int(lcm_maya),
        "maya_phase_compression_ratio": z_int(phase_compression),
        "maya_dresden_eclipse_ratio": q_str(dresden_ratio),
        "inconsistent_crt_refused": inconsistent_rejected,
        "antikythera_metonic_ratio": q_str(metonic),
        "antikythera_anomalistic_rate": q_str(anomalistic),
        "two_clock_record_shift_delta_beta2": q_str(delta_beta2_record),
        "two_clock_white_noise_beta2_n16_n256": [q_str(beta2_white_t1), q_str(beta2_white_t2)],
        "two_clock_white_noise_delta_beta2": q_str(delta_beta2_white),
        "panini_encoding_bit_widths": {
            "phoneme_id_bits": z_int(phoneme_id_bits),
            "it_marker_id_bits": z_int(marker_id_bits),
            "descriptor_bits_per_class": z_int(descriptor_bits_per_class),
            "naive_bits_total": z_int(naive_bits),
            "descriptor_bits_total": z_int(desc_bits),
            "sivasutra_table_bits": z_int(table_bits),
            "encoded_bits_total": z_int(total_bits),
        },
        "panini_c1p_descriptor_ratio": q_str(panini_desc_ratio),
        "panini_c1p_total_ratio": q_str(panini_total_ratio),
    }


# =============================================================================
# Pillar 4: Programmatically Bound 16-Entry Periodic Table of Invariants
# =============================================================================

def classify_morphism_grade(evidence: dict[str, Any]) -> str:
    """Derive canonical morphism grade strictly from verified structural evidence flags."""
    require_ok(isinstance(evidence, dict), "morphism_evidence must be a dict")
    require_ok(frozenset(evidence.keys()) == EVIDENCE_KEYS, "morphism_evidence keys mismatch")
    for k in EVIDENCE_KEYS:
        require_ok(type(evidence[k]) is bool, f"morphism_evidence[{k}] must be bool")

    is_iso = evidence["has_forward_inverse_bijection"]
    is_noncong = evidence["has_non_congruent_inertia_separation"]
    is_obstr = evidence["has_impossibility_counterexample"]
    is_shared = evidence["has_shared_operator_witness"]

    active_primary = sum((1 if is_iso else 0, 1 if is_noncong else 0, 1 if is_obstr else 0))
    require_ok(active_primary <= 1, "Primary morphism evidence flags must be mutually exclusive")
    if is_noncong:
        return "SHARED_BLOCK_ELIMINATION_NON_CONGRUENT"
    if is_iso:
        return "EXACT_ISOMORPHISM"
    if is_obstr:
        return "PROVABLE_OBSTRUCTION"
    require_ok(is_shared, "Entry must satisfy at least one verified structural evidence criterion")
    return "EXACT_SHARED_OPERATOR"


def _make_entry(
    entry_id: str,
    family: str,
    tradition: str,
    operator: str,
    exact_witness: str,
    obstruction_class: str,
    evidence: dict[str, bool],
    witness_metrics: dict[str, Any],
) -> dict[str, Any]:
    return {
        "entry_id": entry_id,
        "family": family,
        "tradition": tradition,
        "operator": operator,
        "exact_witness": exact_witness,
        "obstruction_class": obstruction_class,
        "verification_scope": "IN_MODULE_EXACT",
        "morphism_evidence": evidence,
        "morphism_grade": classify_morphism_grade(evidence),
        "witness_metrics": witness_metrics,
    }


def _ev(bijection: bool, impossibility: bool, noncong: bool, shared: bool) -> dict[str, bool]:
    """Construct canonical 4-flag morphism_evidence dict from live booleans."""
    return {
        "has_forward_inverse_bijection": bijection,
        "has_impossibility_counterexample": impossibility,
        "has_non_congruent_inertia_separation": noncong,
        "has_shared_operator_witness": shared,
    }


def build_periodic_table_from_pillars(
    h1: dict[str, Any],
    h2: dict[str, Any],
    h3: dict[str, Any],
) -> dict[str, Any]:
    """Build canonical zero-float 16-entry Periodic Table dynamically from live pillar witnesses."""
    ab = h2["abelian_zero_residual_witnesses"]
    nab = h2["nonabelian_or_dissipative_nonzero_witnesses"]
    bl = h1["class_b_bit_losses"]
    a16m = h1["class_c_a16_secded_matrix"]
    rhind_2_17 = h1["class_a_rhind_2_17_denoms"]
    greedy_2_17 = h1["class_a_greedy_2_17_denoms"]
    egypt_5_21 = h1["class_a_egypt_5_21_denoms"]
    greedy_5_21 = h1["class_a_greedy_5_21_denoms"]
    madhava_counts = h1["class_a_madhava_telescoping_counts"]
    cg = h1["class_c_casarabe_graph_counts"]
    cc = h1["class_c_casarabe_vs_tree_cut_comps"]
    kh = h1["class_c_khipu_valid_and_tamper"]
    in_h8, in_hyd = h1["class_d_inertia_h8_vs_hydraulic8"]

    ev_pt01 = _ev(
        False,
        (h1["class_a_farabi_obstructed"], h1["class_a_holder_comma_gt_1"]) == (True, True),
        False,
        h1["class_a_farabi_gap"] != "0",
    )
    ev_pt02 = _ev(
        False,
        False,
        False,
        (h1["class_a_zu_beats_22_7_floor"], h1["class_a_zu_first_beater"]) == (4740, "52163/16604"),
    )
    ev_pt03 = _ev(
        False,
        (
            h1["class_a_rhind_beats_greedy"],
            max(rhind_2_17) < max(greedy_2_17),
            max(egypt_5_21) < max(greedy_5_21),
        )
        == (True, True, True),
        False,
        (len(greedy_2_17), len(greedy_5_21)) == (2, 3),
    )
    ev_pt04 = _ev(
        False,
        False,
        False,
        (h3["antikythera_metonic_ratio"], h1["class_a_antikythera_beat_9_times_53"]) == ("254/19", 477),
    )
    ev_pt05 = _ev(
        (
            h3["maya_crt_bijection_exhaustive_ok"],
            h3["maya_compatible_subgroup_order"],
            h3["maya_crt_solution_mod_37960"],
            h3["inconsistent_crt_refused"],
        )
        == (h3["maya_grand_sync_lcm"], h3["maya_grand_sync_lcm"], 12345, True),
        False,
        False,
        h3["maya_grand_sync_lcm"] == 37960,
    )
    ev_pt06 = _ev(
        False,
        False,
        False,
        (madhava_counts, h1["class_a_madhava_r3_n50_speedup_floor"]) == ([49, 49, 49], 27872151775),
    )
    ev_pt07 = _ev(
        False,
        False,
        False,
        (
            h1["class_b_biruni_kappa"],
            bl["biruni"],
            bl["kashi_25"],
            bl["kashi_26"],
            bl["zoom_13"],
            bl["zoom_14"],
            bl["zoom_16"],
        )
        == ("215989/11", 14, 51, 53, 51, 55, 63),
    )
    ev_pt08 = _ev(
        (
            h1["class_b_stereo_cayley_poly_proof_identities"],
            h1["class_b_stereo_s2_roundtrip_count"],
            h1["class_b_cayley_s3_roundtrip_count"],
            h1["class_b_stereo_cayley_embed_count"],
        )
        == (19, 5, 5, 5),
        False,
        False,
        h1["class_b_stereo_cayley_embed_count"] == 5,
    )
    ev_pt09 = _ev(
        False,
        (h1["class_c_tucker_c3_single_copy_orders"], h1["class_c_dup_h_resolves"]) == (0, True),
        False,
        (h1["class_c_panini_43_c1p_count"], h3["panini_c1p_descriptor_ratio"]) == (43, "21/5"),
    )
    ev_pt10 = _ev(
        (
            h1["class_c_pingala_510_bijection_count"],
            h1["class_c_fwht256_involution_and_parity"],
            h1["class_c_bamana_65536_parity_identity_and_a16"],
            a16m["distinct_1bit_syndromes"],
            a16m["nonzero_disjoint_2bit_syndromes"],
            a16m["codeword_count"],
            a16m["min_nonzero_weight"],
        )
        == (510, [256, 256], [65536, 65536], 16, 120, 2048, 4),
        False,
        False,
        h1["class_c_fwht256_involution_and_parity"] == [256, 256],
    )
    ev_pt11 = _ev(
        False,
        False,
        False,
        (
            h1["class_c_sona_576_exact_count"],
            h1["class_c_sona_wall_surgery_2x2_2x3"],
            h1["class_c_z2_twisted_vs_untwisted_sections"],
        )
        == (576, [2, 1, 1, 2], [0, 2]),
    )
    ev_pt12 = _ev(
        False,
        False,
        False,
        (
            h1["class_c_casarabe_adjacency_exact"],
            h1["class_c_casarabe_degree_sequence"],
            h1["class_c_casarabe_vs_tree_betti1"],
            cg,
            cc,
            kh,
        )
        == (True, list(CASARABE_C2_6_EXPECTED_DEGREES), [12, 0], [13, 24, 12], [1, 2], [True, True]),
    )
    ev_pt13 = _ev(
        False,
        False,
        (in_h8[1] != in_hyd[1], in_h8, in_hyd) == (True, [4, 4, 0], [7, 0, 1]),
        h1["class_d_schur_trace_drop"] == "81/1250",
    )
    ev_pt14 = _ev(
        False,
        False,
        False,
        (
            h1["class_d_kemeny_snell_lumpability_defects"],
            h1["class_d_trotter_defect_eps_1_4"],
            h1["class_d_strang_quaternion_eps_1_4"][3],
        )
        == (["0", "1/2"], "262144/17850625", "0"),
    )
    ev_pt15 = _ev(
        False,
        False,
        False,
        (
            ab["al_tusi_planar_curl"],
            ab["antagonistic_balanced_net_torque"],
            ab["antagonistic_mixed_coupling_h_ant"],
            ab["cayley_2dplane_orth_retention"],
            nab["al_tusi_s2_hippopede_py"],
            nab["spinor_hippopede_c3_norm2"],
        )
        == ("0", "0", "0", "1", "288/3125", "5/36"),
    )
    ev_pt16 = _ev(
        False,
        False,
        False,
        (
            h2["dougong_loop_area"],
            nab["dougong_pi_zeta"],
            nab["machu_picchu_housner_loss"],
            h3["two_clock_record_shift_delta_beta2"],
            h3["two_clock_white_noise_delta_beta2"],
        )
        == ("96", "2/3", "111/400", "144/31", "0"),
    )

    rows: list[dict[str, Any]] = [
        _make_entry(
            "PT-01",
            "DIOPHANTINE_RESONANCE_LATTICE",
            "Islamicate (Al-Farabi 53-TET)",
            "Exact Integer Power Obstruction (12^53 != 2^7 * 11^53)",
            f"gcd(12,11)=1 => 12^53 != 2^7*11^53 (gap {h1['class_a_farabi_gap']}); Holder comma 3^53/2^84 > 1 ({h1['class_a_holder_comma_gt_1']})",
            "CLASS_A_DIOPHANTINE",
            ev_pt01,
            {"farabi_gap": h1["class_a_farabi_gap"], "farabi_obstructed": h1["class_a_farabi_obstructed"]},
        ),
        _make_entry(
            "PT-02",
            "DIOPHANTINE_RESONANCE_LATTICE",
            "East Asian (Zu Chongzhi pi)",
            "Hurwitz CF Convergent [3; 7, 15, 1] = 355/113",
            f"355/113 beats 22/7 by >= {h1['class_a_zu_beats_22_7_floor']}x; exhaustive first beater {h1['class_a_zu_first_beater']}",
            "CLASS_A_DIOPHANTINE",
            ev_pt02,
            {"zu_floor": h1["class_a_zu_beats_22_7_floor"], "first_beater": h1["class_a_zu_first_beater"]},
        ),
        _make_entry(
            "PT-03",
            "DIOPHANTINE_RESONANCE_LATTICE",
            "Ancient Egyptian (Rhind 2/n & Egyptian Unit Fractions)",
            "Min-Max-Denom Unit-Fraction Decomposition vs Greedy Sylvester",
            f"Rhind 2/17 denoms {rhind_2_17} (max {max(rhind_2_17)} < greedy {greedy_2_17} max {max(greedy_2_17)}); "
            f"5/21 denoms {egypt_5_21} (max {max(egypt_5_21)} < greedy {greedy_5_21} max {max(greedy_5_21)})",
            "CLASS_A_DIOPHANTINE",
            ev_pt03,
            {
                "rhind_2_17": rhind_2_17,
                "greedy_2_17": greedy_2_17,
                "egypt_5_21": egypt_5_21,
                "greedy_5_21": greedy_5_21,
            },
        ),
        _make_entry(
            "PT-04",
            "DIOPHANTINE_RESONANCE_LATTICE",
            "Greco-Roman (Antikythera Epicyclic Gears)",
            "Gear-Train Rational Modular Section",
            f"{h3['antikythera_metonic_ratio']} Metonic; anomalistic {h3['antikythera_anomalistic_rate']}; beat 254*223-239*235={h1['class_a_antikythera_beat_9_times_53']}",
            "CLASS_A_DIOPHANTINE",
            ev_pt04,
            {"metonic": h3["antikythera_metonic_ratio"], "beat": h1["class_a_antikythera_beat_9_times_53"]},
        ),
        _make_entry(
            "PT-05",
            "DIOPHANTINE_RESONANCE_LATTICE",
            "East Asian & Mesoamerican (Qin Jiushao CRT + Maya Multi-Clock)",
            "Non-Coprime CRT Bijection: Z/37960Z <-> Compatible Subgroup of Z/260Z x Z/365Z x Z/584Z",
            f"Exhaustive {h3['maya_crt_bijection_exhaustive_ok']}/{h3['maya_compatible_subgroup_order']} isomorphism onto compatible subgroup "
            f"{{(r1,r2,r3): r1=r2 mod 5, r2=r3 mod 73, r1=r3 mod 4}}; x={h3['maya_crt_solution_mod_37960']} mod {h3['maya_grand_sync_lcm']}; "
            f"inconsistent refused={h3['inconsistent_crt_refused']}; compression {h3['maya_phase_compression_ratio']}x; Dresden {h3['maya_dresden_eclipse_ratio']}",
            "CLASS_A_DIOPHANTINE",
            ev_pt05,
            {
                "x": h3["maya_crt_solution_mod_37960"],
                "lcm": h3["maya_grand_sync_lcm"],
                "compatible_subgroup_order": h3["maya_compatible_subgroup_order"],
                "exhaustive_bijection_verified": h3["maya_crt_bijection_exhaustive_ok"],
            },
        ),
        _make_entry(
            "PT-06",
            "DIOPHANTINE_RESONANCE_LATTICE",
            "South Asian (Kerala School Madhava Antya-samskara)",
            "Rational Telescoping Remainder Accelerator R_1, R_2, R_3",
            f"Delta_1/2/3 telescoping exact counts {madhava_counts} (n=2..50); n=50 R_3 speedup >= {h1['class_a_madhava_r3_n50_speedup_floor']}x over Leibniz",
            "CLASS_A_DIOPHANTINE",
            ev_pt06,
            {
                "telescoping_counts_n2_50": madhava_counts,
                "madhava_r3_n50_speedup_floor": h1["class_a_madhava_r3_n50_speedup_floor"],
            },
        ),
        _make_entry(
            "PT-07",
            "SUBTRACTIVE_CANCELLATION_WALL",
            "Islamicate (Al-Biruni Nandana & Al-Kashi Chord Wall) & Float64 Zoom Cliff",
            "kappa_sub(x) = x / (1 - x) Clamped Bit-Loss Wall",
            f"Al-Biruni kappa={h1['class_b_biruni_kappa']} ({bl['biruni']}b); Al-Kashi k=25->{bl['kashi_25']}b, k=26->{bl['kashi_26']}b; "
            f"zoom ell=13->{bl['zoom_13']}b, ell=14->{bl['zoom_14']}b, ell=16->{bl['zoom_16']}b",
            "CLASS_B_CANCELLATION",
            ev_pt07,
            {"biruni_kappa": h1["class_b_biruni_kappa"], "bit_losses": bl},
        ),
        _make_entry(
            "PT-08",
            "SUBTRACTIVE_CANCELLATION_WALL",
            "Islamicate (Al-Biruni Isti'ab Stereographic) <-> Rational S^3(Q) Cayley Lift",
            "Division-Only Rational Stereographic & Cayley Spinor Bijections",
            f"Generic Z-polynomial bijection proof ({h1['class_b_stereo_cayley_poly_proof_identities']}/19 identities over Z[u,v], Z[x,y,z], Z[w1,w2,w3], Z[q0,q1,q2,q3]) + "
            f"5-point numerical round-trips S^2<->Q^2 ({h1['class_b_stereo_s2_roundtrip_count']}/5), S^3<->Q^3 ({h1['class_b_cayley_s3_roundtrip_count']}/5), "
            f"equatorial embedding ({h1['class_b_stereo_cayley_embed_count']}/5)",
            "CLASS_B_CANCELLATION",
            ev_pt08,
            {
                "poly_bijection_identities": h1["class_b_stereo_cayley_poly_proof_identities"],
                "s2_5pt_roundtrip": h1["class_b_stereo_s2_roundtrip_count"],
                "s3_5pt_roundtrip": h1["class_b_cayley_s3_roundtrip_count"],
                "embed_5pt_matches": h1["class_b_stereo_cayley_embed_count"],
            },
        ),
        _make_entry(
            "PT-09",
            "TOPOLOGICAL_PARTITION_OBSTRUCTION",
            "South Asian (Panini 14 Sivasutras) <-> Minimal Sufficient Partition",
            "C1P Contiguous Interval Compression & Tucker C_3 Obstruction",
            f"{h1['class_c_panini_43_c1p_count']}/43 C1P classes decoded; fixed-width bit costs "
            f"(6b phoneme ID + 4b it-marker ID = 10b descriptor, 43x6b table) yield {h3['panini_c1p_descriptor_ratio']} ({h3['panini_c1p_total_ratio']} w/ table); "
            f"Tucker C_3 {h1['class_c_tucker_c3_single_copy_orders']}/6 single-copy orders, dup-h resolved={h1['class_c_dup_h_resolves']}",
            "CLASS_C_TOPOLOGICAL",
            ev_pt09,
            {
                "panini_c1p_exact": h1["class_c_panini_43_c1p_count"],
                "encoding_bit_widths": h3["panini_encoding_bit_widths"],
                "tucker_orders": h1["class_c_tucker_c3_single_copy_orders"],
                "dup_h_resolves": h1["class_c_dup_h_resolves"],
            },
        ),
        _make_entry(
            "PT-10",
            "TOPOLOGICAL_PARTITION_OBSTRUCTION",
            "South Asian (Pingala) + West African (Bamana) <-> F_2^8 FWHT_256 & [16,11,4] A_16 SECDED",
            "F_2^n Hypercube Bijection & Explicit 5x16 GF(2) SECDED Parity-Check Matrix H",
            f"Pingala {h1['class_c_pingala_510_bijection_count']}/510 bijection; FWHT_256 {h1['class_c_fwht256_involution_and_parity']}; "
            f"A_16 5x16 H: {a16m['distinct_1bit_syndromes']}/16 distinct 1-bit, {a16m['nonzero_disjoint_2bit_syndromes']}/120 disjoint 2-bit, "
            f"{a16m['codeword_count']} codewords, d_min={a16m['min_nonzero_weight']}; "
            f"Bamana parity-conservation identity & A_16 syndrome correspondence {h1['class_c_bamana_65536_parity_identity_and_a16']}",
            "CLASS_C_TOPOLOGICAL",
            ev_pt10,
            {
                "pingala_bijection": h1["class_c_pingala_510_bijection_count"],
                "fwht256_involution_and_parity": h1["class_c_fwht256_involution_and_parity"],
                "a16_secded_matrix": a16m,
                "bamana_parity_identity_and_a16": h1["class_c_bamana_65536_parity_identity_and_a16"],
            },
        ),
        _make_entry(
            "PT-11",
            "TOPOLOGICAL_PARTITION_OBSTRUCTION",
            "Sub-Saharan African (Chokwe Sona Mirror Curves) & Discrete Z_2 Sheaf H^1",
            "Torus-Knot Mirror Coprimality loop_count(m,n) == gcd(m,n)",
            f"{h1['class_c_sona_576_exact_count']}/576 [1,24]^2 grids exact; 2-opt wall {h1['class_c_sona_wall_surgery_2x2_2x3']}; Z_2 sheaf {h1['class_c_z2_twisted_vs_untwisted_sections']}",
            "CLASS_C_TOPOLOGICAL",
            ev_pt11,
            {"sona_576_exact": h1["class_c_sona_576_exact_count"], "wall_surgery": h1["class_c_sona_wall_surgery_2x2_2x3"]},
        ),
        _make_entry(
            "PT-12",
            "TOPOLOGICAL_PARTITION_OBSTRUCTION",
            "Andean Tree-Sum Checksums & Amazonian Casarabe C_{2,6} Radial-Ring Topology",
            "Hierarchical Tree-Sum Integrity & Casarabe C_{2,6} Cycle Cut Resilience (beta_1)",
            f"Casarabe C_{{2,6}} ({cg[0]} vertices, pinned 24-edge adjacency={h1['class_c_casarabe_adjacency_exact']}, degrees={h1['class_c_casarabe_degree_sequence']}, "
            f"beta_1={h1['class_c_casarabe_vs_tree_betti1'][0]}, 1-cut comps={cc[0]}) vs spanning tree T_13 ({cg[2]} edges; "
            f"beta_1={h1['class_c_casarabe_vs_tree_betti1'][1]}, 1-cut comps={cc[1]}); khipu tree valid={kh[0]}, 1-cord tamper caught={kh[1]}",
            "CLASS_C_TOPOLOGICAL",
            ev_pt12,
            {
                "casarabe_adjacency_exact": h1["class_c_casarabe_adjacency_exact"],
                "casarabe_degree_sequence": h1["class_c_casarabe_degree_sequence"],
                "graph_counts_v_ec_et": cg,
                "betti1_casarabe_vs_tree": h1["class_c_casarabe_vs_tree_betti1"],
                "cut_comps_casarabe_vs_tree": cc,
                "khipu_valid_and_tamper": kh,
            },
        ),
        _make_entry(
            "PT-13",
            "COMMUTATION_SCHUR_STRATUM",
            "Islamicate (Ibn al-Nafis) & Passive Hydraulic vs Indefinite H_8 Inertia",
            "Schur Complement Block Elimination & Certified Sylvester Inertia",
            f"Schur det {h1['class_d_schur_det_unreadable_to_readable']}, drop {h1['class_d_schur_trace_drop']}; certified inertia H_8={in_h8} vs hydraulic={in_hyd}",
            "CLASS_D_COMMUTATION",
            ev_pt13,
            {"schur_drop": h1["class_d_schur_trace_drop"], "inertia_h8_vs_hyd8": h1["class_d_inertia_h8_vs_hydraulic8"]},
        ),
        _make_entry(
            "PT-14",
            "COMMUTATION_SCHUR_STRATUM",
            "Palindromic Strang Splitting & Kemeny-Snell Strong Markov Lumpability",
            "Commutation Defect & Order-2 BCH Cancellation",
            f"Kemeny-Snell 4x4 Markov defects {h1['class_d_kemeny_snell_lumpability_defects']}; SU(2) Trotter {h1['class_d_trotter_defect_eps_1_4']} vs exact Strang k-axis {h1['class_d_strang_quaternion_eps_1_4'][3]}",
            "CLASS_D_COMMUTATION",
            ev_pt14,
            {"kemeny_snell_defects": h1["class_d_kemeny_snell_lumpability_defects"], "trotter": h1["class_d_trotter_defect_eps_1_4"]},
        ),
        _make_entry(
            "PT-15",
            "OPPOSING_PAIR_CONSERVATION_AND_DAMPING",
            "Islamicate (Al-Tusi Couple) + Spinor-Hippopede + Antagonistic Torque + 2D-Plane Cayley",
            "Opposing-Pair Curl Annihilation (Abelian 0 vs Non-Abelian != 0)",
            f"Planar {ab['al_tusi_planar_curl']}, torque {ab['antagonistic_balanced_net_torque']}, H_ant {ab['antagonistic_mixed_coupling_h_ant']}, plane ret {ab['cayley_2dplane_orth_retention']} vs S^2 {nab['al_tusi_s2_hippopede_py']} & ||C_3(e_1,2e_2)||^2={nab['spinor_hippopede_c3_norm2']}",
            "CLASS_D_COMMUTATION",
            ev_pt15,
            {"s2_py": nab["al_tusi_s2_hippopede_py"], "c3_norm2": nab["spinor_hippopede_c3_norm2"]},
        ),
        _make_entry(
            "PT-16",
            "OPPOSING_PAIR_CONSERVATION_AND_DAMPING",
            "East Asian (Dougong) + Andean (Machu Picchu Rocking) + Two-Clock Variance Shift",
            "Dimensionless Geometric Hysteresis, Rocking Impact Loss & Finite-Baseline Shift",
            f"Dougong loop area {h2['dougong_loop_area']}, pi*zeta={nab['dougong_pi_zeta']}; Housner b/h={h2['housner_b_over_h']} loss={nab['machu_picchu_housner_loss']}; "
            f"H=3/4 shift {h3['two_clock_record_shift_delta_beta2']} vs Walsh-Rademacher white-noise {h3['two_clock_white_noise_beta2_n16_n256']} (delta {h3['two_clock_white_noise_delta_beta2']})",
            "CLASS_D_COMMUTATION",
            ev_pt16,
            {
                "dougong_loop_area": h2["dougong_loop_area"],
                "dougong_pi_zeta": nab["dougong_pi_zeta"],
                "housner_loss": nab["machu_picchu_housner_loss"],
                "white_noise_beta2": h3["two_clock_white_noise_beta2_n16_n256"],
            },
        ),
    ]

    families = sorted({r["family"] for r in rows})
    table: dict[str, Any] = {
        "schema_version": PERIODIC_TABLE_SCHEMA,
        "continuum_scope": "Self-contained cross-civilizational periodic table of exact invariants (Foundation-0/continuum)",
        "compute_policy_status": COMPUTE_POLICY_STATUS,
        "entry_count": len(rows),
        "family_count": len(families),
        "families": families,
        "entries": rows,
    }
    table["result_sha256"] = canonical_sha256(table)
    return table


@functools.lru_cache(maxsize=1)
def _compute_live_pillars() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    h1 = certify_four_class_obstructions()
    h2 = certify_opposing_pair_conservation()
    h3 = certify_modular_flow_and_partition(h1["panini_slot_and_phoneme_counts"])
    return (h1, h2, h3)


def build_periodic_table() -> dict[str, Any]:
    h1, h2, h3 = copy.deepcopy(_compute_live_pillars())
    return build_periodic_table_from_pillars(h1, h2, h3)


# =============================================================================
# Hardened AST Zero-Float / Zero-Div / Zero-Log Guard + Certificate & Validators
# =============================================================================

def _is_nonneg_int_const(expr: ast.expr) -> bool:
    """Return True iff expr is an AST Constant of exact type int with value >= 0."""
    if isinstance(expr, ast.Constant):
        if type(expr.value) is int:
            return expr.value >= 0
    return False


def check_source_zero_floats_and_logs(py_path: Path) -> int:
    """Parse Python AST and count forbidden float/complex/div/pow/getattr/builtins/alias/math/Fraction constructs (must be 0)."""
    src = py_path.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(py_path))
    forbidden_names = frozenset(
        ("float", "log", "log2", "log10", "sqrt", "complex", "pow", "getattr", "eval", "exec", "__import__")
    )
    forbidden_attrs = forbidden_names | frozenset(
        (
            "from_float",
            "from_decimal",
            "__float__",
            "__complex__",
            "__truediv__",
            "__rtruediv__",
            "__itruediv__",
            "__pow__",
            "__rpow__",
            "__ipow__",
        )
    )
    forbidden_mods = frozenset(("cmath", "decimal", "statistics", "builtins", "operator", "importlib", "ctypes"))
    forbidden_refs = frozenset(("builtins", "__builtins__"))
    allowed_math = frozenset(("gcd", "isqrt"))

    math_aliases: set[str] = {"math"}
    frac_mod_aliases: set[str] = {"fractions"}
    frac_cls_aliases: set[str] = {"Fraction"}
    bad_nodes = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                local = alias.asname if alias.asname is not None else alias.name
                root_mod = alias.name.split(".")[0]
                if alias.name == "math":
                    math_aliases.add(local)
                elif alias.name == "fractions":
                    frac_mod_aliases.add(local)
                elif root_mod in forbidden_mods:
                    bad_nodes += 1
        elif isinstance(node, ast.ImportFrom):
            root_mod = (node.module or "").split(".")[0]
            if node.level > 0:
                bad_nodes += 1
            elif node.module == "math":
                for alias in node.names:
                    if alias.name not in allowed_math:
                        bad_nodes += 1
            elif node.module == "fractions":
                for alias in node.names:
                    if alias.name == "Fraction":
                        local = alias.asname if alias.asname is not None else alias.name
                        frac_cls_aliases.add(local)
                    elif alias.name == "*":
                        bad_nodes += 1
            elif root_mod in forbidden_mods:
                bad_nodes += 1

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (float, complex)):
                bad_nodes += 1
        elif isinstance(node, ast.Div):
            bad_nodes += 1
        elif isinstance(node, ast.Assert):
            bad_nodes += 1
        elif isinstance(node, ast.Name):
            if node.id in forbidden_refs:
                bad_nodes += 1
        elif isinstance(node, ast.Attribute):
            if node.attr in forbidden_attrs:
                bad_nodes += 1
            elif isinstance(node.value, ast.Name):
                if node.value.id in math_aliases:
                    if node.attr not in allowed_math:
                        bad_nodes += 1
                elif node.value.id in frac_mod_aliases:
                    if node.attr == "Fraction":
                        bad_nodes += 1
        elif isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Pow):
                if not _is_nonneg_int_const(node.right):
                    bad_nodes += 1
        elif isinstance(node, ast.AugAssign):
            if isinstance(node.op, ast.Pow):
                if not _is_nonneg_int_const(node.value):
                    bad_nodes += 1
        elif isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Name):
                if fn.id in forbidden_names:
                    bad_nodes += 1
                elif fn.id in frac_cls_aliases:
                    if len(node.args) != 2:
                        bad_nodes += 1
                    elif len(node.keywords) != 0:
                        bad_nodes += 1
                    else:
                        for arg in node.args:
                            if isinstance(arg, ast.Constant):
                                if isinstance(arg.value, (str, float, complex)):
                                    bad_nodes += 1
    return bad_nodes


def build_certificate() -> dict[str, Any]:
    h1, h2, h3 = copy.deepcopy(_compute_live_pillars())
    pt = build_periodic_table_from_pillars(h1, h2, h3)
    ast_bad = check_source_zero_floats_and_logs(Path(__file__).resolve())

    cert: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "target_repo": "Foundation-0/continuum",
        "compute_policy_status": COMPUTE_POLICY_STATUS,
        "ast_float_div_and_log_count": ast_bad,
        "four_class_obstructions": h1,
        "opposing_pair_conservation": h2,
        "modular_flow_and_partition": h3,
        "periodic_table_summary": {
            "schema_version": pt["schema_version"],
            "entry_count": pt["entry_count"],
            "family_count": pt["family_count"],
            "in_module_verified_entries": pt["entry_count"],
            "periodic_table_sha256": pt["result_sha256"],
        },
    }
    cert["result_sha256"] = canonical_sha256(cert)
    return cert


def validate_certificate(cert: dict[str, Any]) -> None:
    """Hardened fail-closed certificate validator (rejects floats & forged witnesses even with recomputed hash)."""
    assert_no_floats_recursive(cert)
    require_ok(cert["schema_version"] == SCHEMA_VERSION, "Schema version mismatch")
    require_ok(cert["target_repo"] == "Foundation-0/continuum", "Target repo mismatch")
    require_ok(cert["compute_policy_status"] == COMPUTE_POLICY_STATUS, "Compute policy mismatch")
    require_ok(cert["ast_float_div_and_log_count"] == 0, "AST must contain zero floats, true divisions, or forbidden math calls")

    h1 = cert["four_class_obstructions"]
    require_ok(h1["class_a_diophantine_checks_total"] == 15, "Expected 15 Class-A checks")
    require_ok(h1["class_a_diophantine_checks_ok"] == h1["class_a_diophantine_checks_total"], "Class-A check mismatch")
    require_ok(h1["class_a_zu_beats_22_7_floor"] == 4740, "Zu Chongzhi floor witness mismatch")
    require_ok(h1["class_a_zu_first_beater"] == "52163/16604", "Zu first beater witness mismatch")
    require_ok(h1["class_a_antikythera_beat_9_times_53"] == 477, "Antikythera beat witness mismatch")
    require_ok(h1["class_a_madhava_r3_n50_speedup_floor"] == 27872151775, "Madhava R3 n=50 speedup witness mismatch")

    require_ok(h1["class_b_cancellation_checks_total"] == 12, "Expected 12 Class-B checks")
    require_ok(h1["class_b_cancellation_checks_ok"] == h1["class_b_cancellation_checks_total"], "Class-B check mismatch")
    require_ok(h1["class_b_biruni_kappa"] == "215989/11", "Al-Biruni kappa witness mismatch")
    require_ok(h1["class_b_stereo_cayley_poly_proof_identities"] == 19, "Generic polynomial bijection proof count mismatch")
    require_ok(h1["class_b_stereo_s2_roundtrip_count"] == 5, "Stereographic S^2 5-point round-trip mismatch")
    require_ok(h1["class_b_cayley_s3_roundtrip_count"] == 5, "Cayley S^3 5-point round-trip mismatch")

    require_ok(h1["class_c_topological_checks_total"] == 19, "Expected 19 Class-C checks")
    require_ok(h1["class_c_topological_checks_ok"] == h1["class_c_topological_checks_total"], "Class-C check mismatch")
    require_ok(h1["class_c_sona_576_exact_count"] == 576, "Sona 576/576 sweep mismatch")
    require_ok(h1["class_c_panini_43_c1p_count"] == 43, "Panini 43/43 C1P count mismatch")
    require_ok(h1["class_c_tucker_c3_single_copy_orders"] == 0, "Tucker C_3 witness mismatch")
    require_ok(h1["class_c_pingala_510_bijection_count"] == 510, "Pingala 510/510 bijection mismatch")
    require_ok(h1["class_c_fwht256_involution_and_parity"] == [256, 256], "FWHT_256 witness mismatch")
    require_ok(h1["class_c_bamana_65536_parity_identity_and_a16"] == [65536, 65536], "Bamana 65536 parity identity and A_16 mismatch")
    require_ok(
        h1["class_c_a16_secded_matrix"] == {
            "parity_check_rows": 5,
            "code_length": 16,
            "distinct_1bit_syndromes": 16,
            "nonzero_disjoint_2bit_syndromes": 120,
            "codeword_count": 2048,
            "min_nonzero_weight": 4,
        },
        "A_16 SECDED 5x16 matrix witness mismatch",
    )
    require_ok(h1["class_c_z2_twisted_vs_untwisted_sections"] == [0, 2], "Z_2 sheaf section witness mismatch")
    require_ok(h1["class_c_casarabe_adjacency_exact"] is True, "Casarabe C_{2,6} adjacency mismatch")
    require_ok(
        h1["class_c_casarabe_degree_sequence"] == list(CASARABE_C2_6_EXPECTED_DEGREES),
        "Casarabe C_{2,6} degree sequence mismatch",
    )
    require_ok(h1["class_c_casarabe_vs_tree_betti1"] == [12, 0], "Casarabe Betti_1 witness mismatch")

    require_ok(h1["class_d_commutation_checks_total"] == 8, "Expected 8 Class-D checks")
    require_ok(h1["class_d_commutation_checks_ok"] == h1["class_d_commutation_checks_total"], "Class-D check mismatch")
    require_ok(h1["class_d_schur_det_unreadable_to_readable"] == ["34/625", "688/15625"], "Schur det witness mismatch")
    require_ok(h1["class_d_schur_trace_drop"] == "81/1250", "Schur trace drop witness mismatch")
    require_ok(h1["class_d_inertia_h8_vs_hydraulic8"] == [[4, 4, 0], [7, 0, 1]], "Sylvester inertia separation mismatch")
    require_ok(h1["class_d_kemeny_snell_lumpability_defects"] == ["0", "1/2"], "Kemeny-Snell lumpability witness mismatch")
    require_ok(h1["class_d_trotter_defect_eps_1_4"] == "262144/17850625", "Trotter defect witness mismatch")

    h2 = cert["opposing_pair_conservation"]
    require_ok(h2["opposing_pair_checks_total"] == 13, "Expected 13 opposing-pair checks")
    require_ok(h2["opposing_pair_checks_ok"] == h2["opposing_pair_checks_total"], "Opposing-pair check mismatch")
    require_ok(
        h2["abelian_zero_residual_witnesses"] == {
            "al_tusi_planar_curl": "0",
            "collinear_strang_defect": "0",
            "antagonistic_balanced_net_torque": "0",
            "antagonistic_mixed_coupling_h_ant": "0",
            "cayley_2dplane_orth_retention": "1",
        },
        "Abelian zero-residual witnesses mismatch",
    )
    require_ok(
        h2["nonabelian_or_dissipative_nonzero_witnesses"] == {
            "al_tusi_s2_hippopede_py": "288/3125",
            "bch_c3_e1_2e2_vec": ["-1/3", "-1/6", "0"],
            "spinor_hippopede_c3_norm2": "5/36",
            "dougong_pi_zeta": "2/3",
            "machu_picchu_housner_loss": "111/400",
            "cayley_tangent_orth_sq_retention": "9/25",
        },
        "Non-Abelian or dissipative witnesses mismatch",
    )

    h3 = cert["modular_flow_and_partition"]
    require_ok(h3["modular_flow_checks_total"] == 15, "Expected 15 modular-flow checks")
    require_ok(h3["modular_flow_checks_ok"] == h3["modular_flow_checks_total"], "Modular-flow check mismatch")
    require_ok(h3["maya_crt_solution_mod_37960"] == 12345, "Maya CRT witness mismatch")
    require_ok(h3["maya_crt_bijection_exhaustive_ok"] == 37960, "Maya CRT exhaustive bijection mismatch")
    require_ok(h3["maya_grand_sync_lcm"] == 37960, "Maya grand sync LCM mismatch")
    require_ok(h3["maya_phase_compression_ratio"] == 1460, "Maya phase compression mismatch")
    require_ok(h3["maya_dresden_eclipse_ratio"] == "2392/81", "Maya Dresden ratio mismatch")
    require_ok(h3["inconsistent_crt_refused"] is True, "Inconsistent CRT must be refused")
    require_ok(h3["antikythera_metonic_ratio"] == "254/19", "Antikythera Metonic ratio mismatch")
    require_ok(h3["antikythera_anomalistic_rate"] == "56165/4237", "Antikythera anomalistic rate mismatch")
    require_ok(h3["two_clock_record_shift_delta_beta2"] == "144/31", "Two-clock shift mismatch")
    require_ok(h3["two_clock_white_noise_delta_beta2"] == "0", "Two-clock white-noise shift mismatch")
    require_ok(h3["panini_c1p_descriptor_ratio"] == "21/5", "Panini descriptor ratio mismatch")

    pts = cert["periodic_table_summary"]
    require_ok(pts["schema_version"] == PERIODIC_TABLE_SCHEMA, "Periodic table schema mismatch")
    require_ok(pts["entry_count"] == 16, "Expected 16 periodic table entries")
    require_ok(pts["family_count"] == 5, "Expected 5 morphological families")
    require_ok(pts["in_module_verified_entries"] == 16, "Expected 16 in-module verified entries")
    require_ok(is_hex64(pts["periodic_table_sha256"]), "Periodic table SHA-256 must be 64-hex")

    exp_sha = canonical_sha256(cert)
    got_sha = str(cert.get("result_sha256", ""))
    require_ok(hmac.compare_digest(got_sha, exp_sha), "Certificate result_sha256 mismatch")
    require_ok(cert == build_certificate(), "Certificate payload does not match recomputed build")


def validate_periodic_table(table: dict[str, Any]) -> None:
    """Hardened fail-closed validator for periodic_table_of_invariants.json."""
    assert_no_floats_recursive(table)
    require_ok(table["schema_version"] == PERIODIC_TABLE_SCHEMA, "Periodic table schema mismatch")
    require_ok(table["compute_policy_status"] == COMPUTE_POLICY_STATUS, "Periodic table policy mismatch")
    require_ok(table["entry_count"] == 16, "Expected 16 entries in periodic table")
    entries = table["entries"]
    require_ok(len(entries) == table["entry_count"], "Periodic table entries length mismatch")
    require_ok(table["family_count"] == 5, "Expected 5 families in periodic table")
    require_ok(table["families"] == sorted(ALLOWED_FAMILIES), "Periodic table families list mismatch")

    seen_ids: set[str] = set()
    seen_families: set[str] = set()
    for row in entries:
        eid = row["entry_id"]
        require_ok(eid not in seen_ids, f"Duplicate entry_id: {eid}")
        seen_ids.add(eid)
        fam = row["family"]
        require_ok(fam in ALLOWED_FAMILIES, f"Invalid family: {fam}")
        seen_families.add(fam)
        require_ok(row["obstruction_class"] in ALLOWED_OBSTRUCTION_CLASSES, "Invalid obstruction_class")
        require_ok(row["verification_scope"] == "IN_MODULE_EXACT", "Entry must be IN_MODULE_EXACT")
        require_ok(row["morphism_grade"] in ALLOWED_MORPHISM_GRADES, "Invalid morphism_grade")
        derived_grade = classify_morphism_grade(row["morphism_evidence"])
        require_ok(row["morphism_grade"] == derived_grade, f"Morphism grade mismatch for {eid}: expected {derived_grade}")
        require_ok(len(str(row["exact_witness"]).strip()) > 0, "Empty exact_witness")
    require_ok(seen_families == ALLOWED_FAMILIES, "Entries do not cover all 5 families")

    exp_sha = canonical_sha256(table)
    got_sha = str(table.get("result_sha256", ""))
    require_ok(hmac.compare_digest(got_sha, exp_sha), "Periodic table result_sha256 mismatch")
    require_ok(table == build_periodic_table(), "Periodic table payload does not match recomputed build")


def verify_committed_artifacts(
    artifact_dir: Path,
    live_cert: dict[str, Any],
    live_table: dict[str, Any],
) -> tuple[str, str]:
    """Fail-closed validation of committed periodic_table_certificate.json and periodic_table_of_invariants.json."""
    cert_path = artifact_dir.joinpath("periodic_table_certificate.json")
    pt_path = artifact_dir.joinpath("periodic_table_of_invariants.json")
    require_ok(cert_path.is_file(), "Missing committed periodic_table_certificate.json on disk")
    require_ok(pt_path.is_file(), "Missing committed periodic_table_of_invariants.json on disk")

    cert_raw_bytes = cert_path.read_bytes()
    pt_raw_bytes = pt_path.read_bytes()
    require_ok(b"\r" not in cert_raw_bytes, "CRLF forbidden in periodic_table_certificate.json")
    require_ok(b"\r" not in pt_raw_bytes, "CRLF forbidden in periodic_table_of_invariants.json")
    disk_cert = loads_strict_no_float_json(cert_raw_bytes.decode("utf-8"))
    disk_table = loads_strict_no_float_json(pt_raw_bytes.decode("utf-8"))

    validate_certificate(disk_cert)
    validate_periodic_table(disk_table)

    expected_cert_bytes = (json.dumps(live_cert, sort_keys=True, indent=2) + "\n").encode("utf-8")
    expected_pt_bytes = (json.dumps(live_table, sort_keys=True, indent=2) + "\n").encode("utf-8")
    require_ok(cert_raw_bytes == expected_cert_bytes, "Committed periodic_table_certificate.json bytes differ from canonical build")
    require_ok(pt_raw_bytes == expected_pt_bytes, "Committed periodic_table_of_invariants.json bytes differ from canonical build")

    return (
        hashlib.sha256(cert_raw_bytes).hexdigest(),
        hashlib.sha256(pt_raw_bytes).hexdigest(),
    )


def format_summary(cert: dict[str, Any]) -> str:
    h1 = cert["four_class_obstructions"]
    h2 = cert["opposing_pair_conservation"]
    h3 = cert["modular_flow_and_partition"]
    pts = cert["periodic_table_summary"]
    return "\n".join(
        (
            "Foundation-0/continuum: Self-Contained Cross-Civilizational Periodic Table of Invariants",
            f"AST_FLOAT_DIV_LOG={cert['ast_float_div_and_log_count']} "
            f"OBSTRUCTIONS: A={h1['class_a_diophantine_checks_ok']}/15 B={h1['class_b_cancellation_checks_ok']}/12 "
            f"C={h1['class_c_topological_checks_ok']}/19 D={h1['class_d_commutation_checks_ok']}/8",
            f"OPPOSING_PAIRS={h2['opposing_pair_checks_ok']}/13 MODULAR_FLOW={h3['modular_flow_checks_ok']}/15",
            f"PERIODIC_TABLE: entries={pts['entry_count']} in_module={pts['in_module_verified_entries']} "
            f"families={pts['family_count']} sha256={pts['periodic_table_sha256']}",
            f"result_sha256={cert['result_sha256']}",
        )
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Self-Contained Pure-Q/Z Verifier for Foundation-0/continuum Periodic Table.")
    mode_grp = parser.add_mutually_exclusive_group()
    mode_grp.add_argument("--json", action="store_true", help="Emit canonical certificate JSON.")
    mode_grp.add_argument("--periodic-table-json", action="store_true", help="Emit periodic_table_of_invariants.json.")
    mode_grp.add_argument("--check", action="store_true", help="Validate live math AND committed JSON files on disk.")
    parser.add_argument(
        "--artifact-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory holding committed JSON artifacts for --check.",
    )
    args = parser.parse_args(argv)

    cert = build_certificate()
    validate_certificate(cert)
    table = build_periodic_table()
    validate_periodic_table(table)

    if args.periodic_table_json:
        print(json.dumps(table, sort_keys=True, indent=2))
    elif args.json:
        print(json.dumps(cert, sort_keys=True, indent=2))
    elif args.check:
        cert_file_sha, pt_file_sha = verify_committed_artifacts(args.artifact_dir, cert, table)
        print(
            f"PASS CONTINUUM_PERIODIC_TABLE_INVARIANTS "
            f"result_sha256={cert['result_sha256']} "
            f"cert_file_sha256={cert_file_sha} "
            f"table_file_sha256={pt_file_sha}"
        )
    else:
        print(format_summary(cert))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
