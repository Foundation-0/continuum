#!/usr/bin/env python3
"""Assertion-free, float-free, log-free standalone test suite for verify_periodic_table_invariants.py.

Exercises every primitive boundary, fail-closed refusal path, hardened AST zero-float/zero-div guard,
runtime float trap, morphism-grade programmatic binding, on-disk --check artifact binding (C1/C2),
and forged-witness tamper rejection (even with recomputed result_sha256).
Emits 0 stdout bytes on PASS across -I -B, -I -O -B, and -I -B -W error.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import io
import json
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

_ROOT = str(Path(__file__).resolve().parent)
if _ROOT not in sys.path:
    sys.path.append(_ROOT)

import verify_periodic_table_invariants as ptv


def fail(msg: str) -> None:
    raise RuntimeError(f"CONTINUUM_PT_FAIL: {msg}")


def check(cond: bool, msg: str) -> None:
    if cond is not True:
        fail(msg)


def check_raises_val(fn: Callable[[], Any], label: str, match: str) -> None:
    raised = False
    text = ""
    try:
        fn()
    except ValueError as exc:
        raised = True
        text = str(exc)
    if not raised:
        fail(f"Expected ValueError for {label}")
    if match not in text:
        fail(f"Message mismatch for {label}: expected {match!r} in {text!r}")


def test_ast_and_runtime_float_guards() -> None:
    check(ptv.check_source_zero_floats_and_logs(Path(ptv.__file__).resolve()) == 0, "Target AST has forbidden float/div/math")
    check(ptv.check_source_zero_floats_and_logs(Path(__file__).resolve()) == 0, "Test AST has forbidden float/div/math")

    # Verify hardened AST guard catches C7 (int/int Div & math.sqrt), C8 (0.5), C9 (Fraction("0.5")),
    # /=, negative-exponent powers (2**-1, x**=-1), ALL pow(...) calls (incl. pow(2,-1,None)),
    # getattr / builtins / __builtins__ / __truediv__ / relative-import escapes,
    # complex (1j, complex()), import aliases (math as m, Fraction as F, fractions as fr),
    # from_float/from_decimal, forbidden modules (decimal, builtins), and 1-arg / keyword Fraction(...)
    bad_snippets = (
        ("div_op", "x = 1 / 2\n"),
        ("aug_div_op", "x = 4\nx /= 2\n"),
        ("pow_neg", "x = 2 ** -1\n"),
        ("pow_var", "k = 1\nx = 2 ** k\n"),
        ("pow_bool", "x = 2 ** True\n"),
        ("aug_pow_neg", "x = 2\nx **= -1\n"),
        ("pow_call_neg", "x = pow(2, -1)\n"),
        ("pow_call_none3", "x = pow(2, -1, None)\n"),
        ("pow_call_mod3", "x = pow(3, -1, 7)\n"),
        ("builtins_pow", "import builtins\nx = builtins.pow(2, -1)\n"),
        ("dunder_builtins", "x = __builtins__\n"),
        ("getattr_math", "import math\nx = getattr(math, 'sqrt')(2)\n"),
        ("getattr_builtins", "x = getattr(__builtins__, 'float')(1)\n"),
        ("dunder_truediv", "x = (1).__truediv__(2)\n"),
        ("rel_import", "from . import helper\n"),
        ("math_sqrt", "import math\nx = math.sqrt(2)\n"),
        ("math_sin", "import math\nx = math.sin(1)\n"),
        ("math_alias_sin", "import math as m\nx = m.sin(1)\n"),
        ("from_math_sqrt", "from math import sqrt\nx = sqrt(2)\n"),
        ("import_decimal", "import decimal\n"),
        ("from_decimal", "from decimal import Decimal\n"),
        ("from_frac_star", "from fractions import *\n"),
        ("float_lit", "x = 0.5\n"),
        ("complex_lit", "x = 1j\n"),
        ("float_call", "x = float(1)\n"),
        ("complex_call", "x = complex(1, 2)\n"),
        ("frac_str_1arg", "from fractions import Fraction\nx = Fraction('0.5')\n"),
        ("frac_var_1arg", "from fractions import Fraction\nv = 1\nx = Fraction(v)\n"),
        ("frac_alias_1arg", "from fractions import Fraction as F\nx = F('0.5')\n"),
        ("frac_kw", "from fractions import Fraction\nx = Fraction(numerator=1, denominator=2)\n"),
        ("frac_2arg_str", "from fractions import Fraction\nx = Fraction('1', 2)\n"),
        ("frac_from_float", "from fractions import Fraction\nx = Fraction.from_float(1)\n"),
        ("frac_from_decimal", "from fractions import Fraction\nx = Fraction.from_decimal(1)\n"),
        ("attr_frac", "import fractions\nx = fractions.Fraction(1, 2)\n"),
        ("attr_frac_alias", "import fractions as fr\nx = fr.Fraction(1, 2)\n"),
    )
    with tempfile.TemporaryDirectory() as td:
        for name, code in bad_snippets:
            p = Path(td, f"{name}.py")
            p.write_text(code, encoding="utf-8")
            check(ptv.check_source_zero_floats_and_logs(p) > 0, f"AST guard missed {name}")
        good_p = Path(td, "good.py")
        good_p.write_text(
            "import math as m\n"
            "from math import gcd, isqrt\n"
            "from fractions import Fraction as F\n"
            "x = F(m.gcd(4, 6), isqrt(9))\n"
            "y = 2 ** 0\n"
            "z = 2\n"
            "z **= 0\n",
            encoding="utf-8",
        )
        check(ptv.check_source_zero_floats_and_logs(good_p) == 0, "AST guard false positive on clean code")

    # Recursive runtime float/complex traps (constructed without forbidden AST nodes)
    rt_float = json.loads("0.5")
    rt_complex = ast.literal_eval("1j")
    check_raises_val(lambda: ptv.assert_no_floats_recursive({"a": [1, (2, rt_float)]}), "runtime float nested", "Runtime float or complex forbidden")
    check_raises_val(lambda: ptv.assert_no_floats_recursive({rt_float: "k"}), "runtime float key", "Runtime float or complex forbidden")
    check_raises_val(lambda: ptv.assert_no_floats_recursive([rt_complex]), "runtime complex", "Runtime float or complex forbidden")

    # Strict JSON parse_float / parse_constant / duplicate-key refusal
    check_raises_val(lambda: ptv.loads_strict_no_float_json('{"x": 0.5}'), "json float", "JSON float literal forbidden")
    check_raises_val(lambda: ptv.loads_strict_no_float_json('{"x": NaN}'), "json nan", "JSON non-finite constant forbidden")
    check_raises_val(lambda: ptv.loads_strict_no_float_json('{"a": 1, "a": 2}'), "json dup key", "Duplicate JSON key forbidden")

    # Pillar-boundary runtime type guards
    check(ptv.q_str(Fraction(3, 4)) == "3/4", "q_str valid failed")
    check_raises_val(lambda: ptv.q_str(1), "q_str int", "Expected exact Fraction scalar")  # type: ignore[arg-type]
    check(ptv.z_int(7) == 7, "z_int valid failed")
    check_raises_val(lambda: ptv.z_int(True), "z_int bool", "Expected exact int scalar")
    check_raises_val(lambda: ptv.z_int(Fraction(1, 1)), "z_int frac", "Expected exact int scalar")  # type: ignore[arg-type]


def test_primitives_and_boundaries() -> None:
    check(ptv.q_div(Fraction(3, 4), Fraction(2, 5)) == Fraction(15, 8), "q_div basic")
    check_raises_val(lambda: ptv.q_div(ptv.ONE, ptv.ZERO), "q_div zero", "Rational division by zero")

    check(ptv.is_hex64("0123456789abcdef" * 4) is True, "valid 64-hex rejected")
    check(ptv.is_hex64(123) is False, "non-str accepted by is_hex64")
    check(ptv.is_hex64("0" * 63) is False, "63-hex accepted by is_hex64")
    check(ptv.is_hex64("g" + "0" * 63) is False, "non-hex accepted by is_hex64")

    check(ptv.cf_convergent((3,)) == Fraction(3, 1), "cf single term")
    check_raises_val(lambda: ptv.cf_convergent(()), "cf empty", "must be non-empty")

    # Pure-Q Machin pi bracket & mod_inv_int boundaries
    a5_lo, a5_hi = ptv._arctan_inv_bracket_q(5, 1)
    check(a5_lo < a5_hi, "arctan_inv_bracket_q(5,1) lo < hi")
    check_raises_val(lambda: ptv._arctan_inv_bracket_q(4, 1), "arctan m=4", "arctan_inv m must be >= 5")
    check_raises_val(lambda: ptv._arctan_inv_bracket_q(5, 0), "arctan pairs=0", "arctan_inv pairs must be >= 1")
    check(ptv.mod_inv_int(3, 1) == 0, "mod_inv m=1")
    check(ptv.mod_inv_int(3, 7) == 5, "mod_inv 3 mod 7")
    check_raises_val(lambda: ptv.mod_inv_int(1, 0), "mod_inv m=0", "mod_inv modulus must be >= 1")
    check_raises_val(lambda: ptv.mod_inv_int(2, 4), "mod_inv noncoprime", "mod_inv inputs must be coprime")

    check(ptv.find_first_pi_beater(Fraction(22, 7), 1, 113) == (179, 57), "pi beater 22/7")
    check(ptv.find_first_pi_beater(Fraction(22, 7), 57, 57) == (179, 57), "pi beater q_min==q_max")
    check_raises_val(lambda: ptv.find_first_pi_beater(Fraction(355, 113), 0, 10), "beater q_min=0", "q_min must be >= 1")
    check_raises_val(lambda: ptv.find_first_pi_beater(Fraction(355, 113), 10, 9), "beater q_max<q_min", "q_max must be >= q_min")
    check_raises_val(lambda: ptv.find_first_pi_beater(Fraction(355, 113), 114, 120), "beater none", "No fraction closer")

    check(ptv.greedy_sylvester_egyptian(Fraction(2, 17)) == (9, 153), "greedy 2/17")
    check_raises_val(lambda: ptv.greedy_sylvester_egyptian(ptv.ZERO), "greedy 0", "must be > 0")
    check_raises_val(lambda: ptv.greedy_sylvester_egyptian(ptv.ONE), "greedy 1", "must be < 1")

    check(ptv.leibniz_partial_sum_q(1) == ptv.ONE, "leibniz n=1")
    check_raises_val(lambda: ptv.leibniz_partial_sum_q(0), "leibniz n=0", "Leibniz n must be >= 1")
    check(ptv.madhava_r1_q(1) == Fraction(1, 4), "r1 n=1")
    check_raises_val(lambda: ptv.madhava_r1_q(0), "r1 n=0", "Madhava R1 n must be >= 1")
    check(ptv.madhava_r2_q(1) == Fraction(1, 5), "r2 n=1")
    check_raises_val(lambda: ptv.madhava_r2_q(0), "r2 n=0", "Madhava R2 n must be >= 1")
    check(ptv.madhava_r3_q(1) == Fraction(2, 9), "r3 n=1")
    check_raises_val(lambda: ptv.madhava_r3_q(0), "r3 n=0", "Madhava R3 n must be >= 1")
    check(ptv.madhava_accelerated_pi_q(1, 1) == Fraction(3, 1), "madhava odd n=1")
    check_raises_val(lambda: ptv.madhava_accelerated_pi_q(1, 4), "madhava order=4", "Madhava order must be in")

    check(ptv.interval_abs_err_bounds(Fraction(1, 2), Fraction(1, 2), Fraction(1, 2)) == (ptv.ZERO, ptv.ZERO), "interval inside")
    check_raises_val(lambda: ptv.interval_abs_err_bounds(ptv.ZERO, ptv.ONE, ptv.ZERO), "interval bad", "lo <= hi")

    k1, b1 = ptv.cancellation_kappa_q(Fraction(1, 2))
    check(k1 == ptv.ONE and b1 == 0, "kappa(1/2) != (1, 0)")
    k0, b0 = ptv.cancellation_kappa_q(Fraction(1, 3))
    check(k0 == Fraction(1, 2) and b0 == 0, "kappa(1/3) != (1/2, 0)")
    check_raises_val(lambda: ptv.cancellation_kappa_q(ptv.ZERO), "kappa x=0", "x must be > 0")
    check_raises_val(lambda: ptv.cancellation_kappa_q(ptv.ONE), "kappa x=1", "x must be < 1")

    check(ptv.kashi_chord_arg_q(1) == Fraction(15, 16), "kashi k=1")
    check_raises_val(lambda: ptv.kashi_chord_arg_q(0), "kashi k=0", "Al-Kashi step k must be >= 1")
    check(ptv.multiscale_zoom_arg_q(1) == Fraction(15, 16), "zoom ell=1")
    check_raises_val(lambda: ptv.multiscale_zoom_arg_q(0), "zoom ell=0", "Zoom level ell must be >= 1")

    check_raises_val(lambda: ptv.stereographic_forward_r2_q(ptv.ONE, ptv.ONE, ptv.ZERO), "stereo off sphere", "unit sphere")
    check_raises_val(lambda: ptv.stereographic_forward_r2_q(ptv.ZERO, ptv.ZERO, ptv.ONE), "stereo north pole", "North Pole")
    check_raises_val(lambda: ptv.cayley_s3_inverse_q((ptv.ONE, ptv.ONE, ptv.ZERO, ptv.ZERO)), "cayley off s3", "unit S^3")
    check_raises_val(lambda: ptv.cayley_s3_inverse_q((Fraction(-1, 1), ptv.ZERO, ptv.ZERO, ptv.ZERO)), "cayley south", "South Pole")

    check(ptv.pingala_nasta(1, 1) == (0,) and ptv.pingala_nasta(1, 2) == (1,), "pingala n=1")
    check_raises_val(lambda: ptv.pingala_nasta(0, 1), "pingala n=0", "Pingala n must be >= 1")
    check_raises_val(lambda: ptv.pingala_nasta(1, 0), "pingala k=0", "Pingala rank k must be >= 1")
    check_raises_val(lambda: ptv.pingala_nasta(1, 3), "pingala k>2^n", "Pingala rank k exceeds")
    check_raises_val(lambda: ptv.pingala_uddista(()), "uddista empty", "Pingala meter must be non-empty")
    check_raises_val(lambda: ptv.pingala_uddista((2,)), "uddista bad bit", "Pingala meter bits must be 0 or 1")

    check(ptv.fwht_int([5]) == [5], "fwht len=1")
    check_raises_val(lambda: ptv.fwht_int([]), "fwht empty", "FWHT input must be non-empty")
    check_raises_val(lambda: ptv.fwht_int([1, 2, 3]), "fwht non-pow2", "FWHT length must be a power of 2")

    slots, mend = ptv.build_sivasutra_slots()
    check_raises_val(lambda: ptv.decode_pratyahara_interval(slots, mend, "a", "BAD"), "panini bad marker", "Unknown it-marker")
    check_raises_val(lambda: ptv.decode_pratyahara_interval(slots, mend, "h", "N1"), "panini missing start", "not found before")

    check(ptv.solve_noncoprime_crt(((0, 1),)) == (0, 1), "crt((0,1)) != (0,1)")
    check(ptv.solve_noncoprime_crt(((1, 2), (1, 1))) == (1, 2), "crt second mod=1 failed")
    check_raises_val(lambda: ptv.solve_noncoprime_crt(()), "crt empty", "non-empty")
    check_raises_val(lambda: ptv.solve_noncoprime_crt(((0, 0),)), "crt m0=0", "CRT modulus must be >= 1")
    check_raises_val(lambda: ptv.solve_noncoprime_crt(((0, 2), (0, 0))), "crt mi=0", "CRT modulus must be >= 1")
    check_raises_val(lambda: ptv.solve_noncoprime_crt(((0, 4), (1, 6))), "crt inconsistent", "Inconsistent")

    check(ptv.gear_train_ratio(((1, 1),)) == ptv.ONE, "gear 1/1")
    check_raises_val(lambda: ptv.gear_train_ratio(()), "gear empty", "gear train must be non-empty")
    check_raises_val(lambda: ptv.gear_train_ratio(((0, 1),)), "gear drv=0", "driver teeth must be >= 1")
    check_raises_val(lambda: ptv.gear_train_ratio(((1, 0),)), "gear flw=0", "follower teeth must be >= 1")

    check(ptv.q_cayley_axis(ptv.ZERO, 3) == (ptv.ONE, ptv.ZERO, ptv.ZERO, ptv.ZERO), "cayley axis 3 zero")
    check_raises_val(lambda: ptv.q_cayley_axis(ptv.ZERO, 0), "cayley axis 0", "axis must be in")
    check_raises_val(lambda: ptv.q_cayley_axis(ptv.ZERO, 4), "cayley axis 4", "axis must be in")

    check(ptv.sona_loop_count_with_wall(1, 1, split_wall=False) == 1, "sona(1,1) != 1")
    check(ptv.sona_loop_count_with_wall(2, 1, split_wall=True) == 2, "sona(2,1,wall) != 2")
    check_raises_val(lambda: ptv.sona_loop_count_with_wall(0, 1, split_wall=False), "sona m=0", "m must be >= 1")
    check_raises_val(lambda: ptv.sona_loop_count_with_wall(1, 0, split_wall=False), "sona n=0", "n must be >= 1")
    check_raises_val(lambda: ptv.sona_loop_count_with_wall(1, 2, split_wall=True), "sona wall m=1", "m >= 2")

    check(ptv.graph_connected_components(1, ()) == 1, "graph 1 vert")
    check(ptv.graph_connected_components(2, ((1, 0),)) == 1, "graph v==0 boundary")
    check_raises_val(lambda: ptv.graph_connected_components(0, ()), "graph 0 verts", "Graph must have >= 1 vertex")
    check_raises_val(lambda: ptv.graph_connected_components(2, ((-1, 0),)), "graph u<0", "u < 0")
    check_raises_val(lambda: ptv.graph_connected_components(2, ((2, 0),)), "graph u>=n", "u >= n_verts")
    check_raises_val(lambda: ptv.graph_connected_components(2, ((0, -1),)), "graph v<0", "v < 0")
    check_raises_val(lambda: ptv.graph_connected_components(2, ((0, 2),)), "graph v>=n", "v >= n_verts")

    check_raises_val(lambda: ptv.schur_3x3_elim_last(((ptv.ONE,),)), "schur 1x1", "exactly 3 rows")
    check_raises_val(
        lambda: ptv.schur_3x3_elim_last(((ptv.ONE, ptv.ZERO), (ptv.ZERO, ptv.ONE), (ptv.ZERO, ptv.ZERO))),
        "schur 3x2",
        "exactly 3 columns",
    )
    check_raises_val(
        lambda: ptv.schur_3x3_elim_last(((ptv.ONE, ptv.ZERO, ptv.ZERO), (ptv.ZERO, ptv.ONE, ptv.ZERO), (ptv.ZERO, ptv.ZERO, ptv.ZERO))),
        "schur pivot=0",
        "strictly positive",
    )

    # Inertia & self-certifying congruence boundaries
    check(ptv.certified_symmetric_inertia_q([[ptv.ZERO]]) == (0, 0, 1), "inertia 1x1 zero")
    check(ptv.certified_symmetric_inertia_q([[ptv.ZERO, ptv.ONE], [ptv.ONE, ptv.ZERO]]) == (1, 1, 0), "inertia hyperbolic 2x2")
    check_raises_val(lambda: ptv.certified_symmetric_inertia_q([]), "inertia empty", "Inertia matrix must be non-empty")
    check_raises_val(lambda: ptv.certified_symmetric_inertia_q([[ptv.ONE, ptv.ZERO]]), "inertia nonsq", "Inertia matrix must be square")
    check_raises_val(lambda: ptv.certified_symmetric_inertia_q([[ptv.ONE, ptv.ONE], [ptv.ZERO, ptv.ONE]]), "inertia nonsym", "Inertia matrix must be symmetric")
    check_raises_val(
        lambda: ptv.verify_congruence_certificate_q([[ptv.ONE]], [[ptv.ONE]], [ptv.ZERO]),
        "congruence bad diag",
        "P^T M P == diag(d) failed",
    )
    check_raises_val(
        lambda: ptv.verify_congruence_certificate_q([[ptv.ZERO]], [[ptv.ZERO]], [ptv.ZERO]),
        "congruence singular P",
        "Congruence matrix P must be invertible",
    )

    # Kemeny-Snell Markov boundaries
    check_raises_val(lambda: ptv.kemeny_snell_lumpability_defect_q(((ptv.ONE,),), ((0,),)), "markov 1x1", "Markov matrix must have >= 2 states")
    check_raises_val(lambda: ptv.kemeny_snell_lumpability_defect_q(((ptv.ONE,), (ptv.ONE,)), ((0,), (1,))), "markov nonsq", "Markov matrix must be square")
    check_raises_val(lambda: ptv.kemeny_snell_lumpability_defect_q(((ptv.ONE, ptv.ONE), (ptv.ONE, ptv.ZERO)), ((0,), (1,))), "markov rowsum", "rows must sum to 1")

    # Two-clock Pont beta boundaries
    check(ptv.pont_beta_sq_h34_q(1, 4) == Fraction(1, 1), "pont h34 N=1,L=4")
    check_raises_val(lambda: ptv.pont_beta_sq_h34_q(0, 4), "pont h34 bin=0", "bin_n must be >= 1")
    check_raises_val(lambda: ptv.pont_beta_sq_h34_q(4, 4), "pont h34 L<=N", "total_l must exceed bin_n")
    check_raises_val(lambda: ptv.pont_beta_sq_h34_q(4, 9), "pont h34 nondiv", "divisible by bin_n")
    check_raises_val(lambda: ptv.pont_beta_sq_h34_q(2, 8), "pont h34 nonsq N", "bin_n must be a perfect square")
    check_raises_val(lambda: ptv.pont_beta_sq_h34_q(1, 2), "pont h34 nonsq M", "total_l // bin_n must be a perfect square")
    check(ptv.pont_beta_sq_h34_q(4, 36) == Fraction(8, 5), "pont h34 N=4,L=36")
    # Note: if bin_n and total_l//bin_n are both squares then total_l is always a square; check h12 boundaries:
    check(ptv.pont_beta_sq_h12_q(1, 2) == ptv.ONE, "pont h12 N=1,L=2")
    check_raises_val(lambda: ptv.pont_beta_sq_h12_q(0, 2), "pont h12 bin=0", "white-noise bin_n must be >= 1")
    check_raises_val(lambda: ptv.pont_beta_sq_h12_q(2, 2), "pont h12 L<=N", "white-noise total_l must exceed bin_n")
    check_raises_val(lambda: ptv.pont_beta_sq_h12_q(2, 6), "pont h12 nonpow2", "white-noise total_l must be a power of 2")
    check_raises_val(lambda: ptv.pont_beta_sq_h12_q(3, 8), "pont h12 nondiv", "white-noise total_l must be divisible")

    # Explicit 5x16 A_16 SECDED parity-check matrix boundaries
    check(ptv.gf2_syndrome_a16(0, ptv.A16_H_ROWS) == 0, "a16 word=0 syn != 0")
    check(ptv.gf2_syndrome_a16(65535, ptv.A16_H_ROWS) == 0, "a16 word=65535 syn != 0")
    check_raises_val(lambda: ptv.gf2_syndrome_a16(-1, ptv.A16_H_ROWS), "a16 word=-1", "A_16 word must be >= 0")
    check_raises_val(lambda: ptv.gf2_syndrome_a16(65536, ptv.A16_H_ROWS), "a16 word=65536", "A_16 word must be < 65536")

    # Morphism grade classifier boundaries
    check_raises_val(lambda: ptv.classify_morphism_grade("not_dict"), "grade non-dict", "morphism_evidence must be a dict")  # type: ignore[arg-type]
    check_raises_val(lambda: ptv.classify_morphism_grade({}), "grade bad keys", "morphism_evidence keys mismatch")
    check_raises_val(
        lambda: ptv.classify_morphism_grade(
            {
                "has_forward_inverse_bijection": 1,
                "has_impossibility_counterexample": False,
                "has_non_congruent_inertia_separation": False,
                "has_shared_operator_witness": True,
            }
        ),
        "grade non-bool",
        "must be bool",
    )
    check_raises_val(
        lambda: ptv.classify_morphism_grade(
            {
                "has_forward_inverse_bijection": True,
                "has_impossibility_counterexample": True,
                "has_non_congruent_inertia_separation": False,
                "has_shared_operator_witness": True,
            }
        ),
        "grade non-exclusive",
        "mutually exclusive",
    )
    check_raises_val(
        lambda: ptv.classify_morphism_grade(
            {
                "has_forward_inverse_bijection": False,
                "has_impossibility_counterexample": False,
                "has_non_congruent_inertia_separation": False,
                "has_shared_operator_witness": False,
            }
        ),
        "grade all false",
        "at least one verified",
    )


def test_dynamic_morphism_evidence_degradation() -> None:
    """Verify degrading live pillar outputs actually flips morphism_evidence and morphism_grade."""
    h1_base, h2_base, h3_base = copy.deepcopy(ptv._compute_live_pillars())

    def _entry_by_id(tbl: dict[str, Any], eid: str) -> dict[str, Any]:
        for row in tbl["entries"]:
            if row["entry_id"] == eid:
                return row
        raise RuntimeError(f"Missing {eid}")

    # PT-01: degrading Farabi obstruction flips PROVABLE_OBSTRUCTION -> EXACT_SHARED_OPERATOR
    h1 = copy.deepcopy(h1_base)
    h1["class_a_farabi_obstructed"] = False
    r1 = _entry_by_id(ptv.build_periodic_table_from_pillars(h1, h2_base, h3_base), "PT-01")
    check(r1["morphism_grade"] == "EXACT_SHARED_OPERATOR", "PT-01 grade did not flip on degradation")

    # PT-03: exact boundary max(rhind) == max(greedy) flips PROVABLE_OBSTRUCTION -> EXACT_SHARED_OPERATOR
    h1 = copy.deepcopy(h1_base)
    h1["class_a_rhind_2_17_denoms"] = [12, 51, 153]
    r3a = _entry_by_id(ptv.build_periodic_table_from_pillars(h1, h2_base, h3_base), "PT-03")
    check(r3a["morphism_grade"] == "EXACT_SHARED_OPERATOR", "PT-03 grade did not flip on Rhind max==greedy boundary")

    h1 = copy.deepcopy(h1_base)
    h1["class_a_egypt_5_21_denoms"] = [6, 945]
    r3b = _entry_by_id(ptv.build_periodic_table_from_pillars(h1, h2_base, h3_base), "PT-03")
    check(r3b["morphism_grade"] == "EXACT_SHARED_OPERATOR", "PT-03 grade did not flip on 5/21 max==greedy boundary")

    # PT-05: degrading exhaustive CRT bijection count flips EXACT_ISOMORPHISM -> EXACT_SHARED_OPERATOR
    h3 = copy.deepcopy(h3_base)
    h3["maya_crt_bijection_exhaustive_ok"] = 37959
    r5 = _entry_by_id(ptv.build_periodic_table_from_pillars(h1_base, h2_base, h3), "PT-05")
    check(r5["morphism_grade"] == "EXACT_SHARED_OPERATOR", "PT-05 grade did not flip on degraded CRT bijection")

    # PT-08: degrading stereographic S^2 bijection flips EXACT_ISOMORPHISM -> EXACT_SHARED_OPERATOR
    h1 = copy.deepcopy(h1_base)
    h1["class_b_stereo_s2_bijection_count"] = 4
    r8 = _entry_by_id(ptv.build_periodic_table_from_pillars(h1, h2_base, h3_base), "PT-08")
    check(r8["morphism_grade"] == "EXACT_SHARED_OPERATOR", "PT-08 grade did not flip on degraded S^2 bijection")

    # PT-09: degrading Tucker C_3 single-copy orders flips PROVABLE_OBSTRUCTION -> EXACT_SHARED_OPERATOR
    h1 = copy.deepcopy(h1_base)
    h1["class_c_tucker_c3_single_copy_orders"] = 1
    r9 = _entry_by_id(ptv.build_periodic_table_from_pillars(h1, h2_base, h3_base), "PT-09")
    check(r9["morphism_grade"] == "EXACT_SHARED_OPERATOR", "PT-09 grade did not flip on degraded Tucker C_3")

    # PT-10: degrading A_16 minimum distance flips EXACT_ISOMORPHISM -> EXACT_SHARED_OPERATOR
    h1 = copy.deepcopy(h1_base)
    h1["class_c_a16_secded_matrix"]["min_nonzero_weight"] = 3
    r10 = _entry_by_id(ptv.build_periodic_table_from_pillars(h1, h2_base, h3_base), "PT-10")
    check(r10["morphism_grade"] == "EXACT_SHARED_OPERATOR", "PT-10 grade did not flip on degraded A_16 d_min")

    # PT-13: equating H_8 inertia with hydraulic inertia flips NON_CONGRUENT -> EXACT_SHARED_OPERATOR
    h1 = copy.deepcopy(h1_base)
    h1["class_d_inertia_h8_vs_hydraulic8"][0] = [7, 0, 1]
    r13 = _entry_by_id(ptv.build_periodic_table_from_pillars(h1, h2_base, h3_base), "PT-13")
    check(r13["morphism_grade"] == "EXACT_SHARED_OPERATOR", "PT-13 grade did not flip on equated inertia")

    # PT-02: degrading shared-operator witness leaves zero true evidence flags -> fail closed
    h1 = copy.deepcopy(h1_base)
    h1["class_a_zu_beats_22_7_floor"] = 0
    check_raises_val(
        lambda: ptv.build_periodic_table_from_pillars(h1, h2_base, h3_base),
        "PT-02 degraded shared witness",
        "at least one verified",
    )


def test_cli_on_disk_binding_and_tampers() -> None:
    buf_json = io.StringIO()
    with redirect_stdout(buf_json):
        rc = ptv.main(["--json"])
    check(rc == 0, "CLI --json rc != 0")
    cert = json.loads(buf_json.getvalue())
    ptv.validate_certificate(cert)

    buf_pt = io.StringIO()
    with redirect_stdout(buf_pt):
        rc_pt = ptv.main(["--periodic-table-json"])
    check(rc_pt == 0, "CLI --periodic-table-json rc != 0")
    table = json.loads(buf_pt.getvalue())
    ptv.validate_periodic_table(table)

    # Explicitly validate the real shipped JSON artifacts on disk in Path(__file__).resolve().parent
    here = Path(__file__).resolve().parent
    shipped_cert_path = here.joinpath("periodic_table_certificate.json")
    shipped_table_path = here.joinpath("periodic_table_of_invariants.json")
    check(shipped_cert_path.is_file(), "Shipped periodic_table_certificate.json missing on disk")
    check(shipped_table_path.is_file(), "Shipped periodic_table_of_invariants.json missing on disk")
    shipped_c_sha, shipped_t_sha = ptv.verify_committed_artifacts(here, cert, table)
    check(
        shipped_c_sha == hashlib.sha256(shipped_cert_path.read_bytes()).hexdigest(),
        "Shipped certificate file SHA-256 mismatch",
    )
    check(
        shipped_t_sha == hashlib.sha256(shipped_table_path.read_bytes()).hexdigest(),
        "Shipped periodic table file SHA-256 mismatch",
    )

    buf_chk = io.StringIO()
    with redirect_stdout(buf_chk):
        rc_chk = ptv.main(["--check"])
    chk_out = buf_chk.getvalue()
    check(
        rc_chk == 0
        and f"PASS CONTINUUM_PERIODIC_TABLE_INVARIANTS result_sha256={cert['result_sha256']}" in chk_out
        and f"cert_file_sha256={shipped_c_sha}" in chk_out
        and f"table_file_sha256={shipped_t_sha}" in chk_out,
        "CLI --check failed on shipped artifacts",
    )

    buf_sum = io.StringIO()
    with redirect_stdout(buf_sum):
        rc_sum = ptv.main([])
    check(rc_sum == 0 and cert["result_sha256"] in buf_sum.getvalue(), "CLI summary failed")

    # Mutually exclusive CLI flags rejected
    mux_exited = False
    mux_err = io.StringIO()
    with redirect_stderr(mux_err):
        try:
            ptv.main(["--json", "--check"])
        except SystemExit as exc:
            mux_exited = exc.code != 0
    check(mux_exited, "CLI mutually exclusive flags were not rejected")

    # Controls C1 & C2: --check MUST fail closed if committed JSON on disk is missing, altered, or non-canonical
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        check_raises_val(lambda: ptv.verify_committed_artifacts(tdp, cert, table), "disk missing cert", "Missing committed periodic_table_certificate.json")
        tdp.joinpath("periodic_table_certificate.json").write_text(json.dumps(cert, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        check_raises_val(lambda: ptv.verify_committed_artifacts(tdp, cert, table), "disk missing table", "Missing committed periodic_table_of_invariants.json")

        # Control C1: corrupt PT-07 -> PT-77 in committed table JSON -> --check MUST FAIL
        bad_t = copy.deepcopy(table)
        bad_t["entries"][6]["entry_id"] = "PT-77"
        tdp.joinpath("periodic_table_of_invariants.json").write_text(json.dumps(bad_t, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        check_raises_val(lambda: ptv.main(["--check", "--artifact-dir", td]), "C1 table disk tamper", "Periodic table result_sha256 mismatch")

        # Restore table, test Control C2: corrupt Biruni kappa in committed cert JSON -> --check MUST FAIL
        tdp.joinpath("periodic_table_of_invariants.json").write_text(json.dumps(table, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        bad_c = copy.deepcopy(cert)
        bad_c["four_class_obstructions"]["class_b_biruni_kappa"] = "215989/12"
        tdp.joinpath("periodic_table_certificate.json").write_text(json.dumps(bad_c, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        check_raises_val(lambda: ptv.main(["--check", "--artifact-dir", td]), "C2 cert disk tamper", "Al-Biruni kappa witness mismatch")

        # Rehashed forged JSON on disk (even with recomputed result_sha256) MUST fail closed
        tdp.joinpath("periodic_table_certificate.json").write_text(json.dumps(cert, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        forged_disk_t = copy.deepcopy(table)
        forged_disk_t["entries"][0]["exact_witness"] = "REHASHED_FORGED_ON_DISK"
        forged_disk_t["result_sha256"] = ptv.canonical_sha256(forged_disk_t)
        tdp.joinpath("periodic_table_of_invariants.json").write_text(json.dumps(forged_disk_t, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        check_raises_val(lambda: ptv.verify_committed_artifacts(tdp, cert, table), "rehashed forged disk table", "Periodic table payload does not match recomputed build")

        tdp.joinpath("periodic_table_of_invariants.json").write_text(json.dumps(table, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        forged_disk_c = copy.deepcopy(cert)
        forged_disk_c["extra_forged_key"] = 1
        forged_disk_c["result_sha256"] = ptv.canonical_sha256(forged_disk_c)
        tdp.joinpath("periodic_table_certificate.json").write_text(json.dumps(forged_disk_c, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        check_raises_val(lambda: ptv.verify_committed_artifacts(tdp, cert, table), "rehashed forged disk cert", "Certificate payload does not match recomputed build")

        # Float, NaN, duplicate-key, or CRLF inside JSON on disk MUST fail closed
        tdp.joinpath("periodic_table_certificate.json").write_bytes(b'{"x": 0.5}\n')
        check_raises_val(lambda: ptv.verify_committed_artifacts(tdp, cert, table), "disk json float", "JSON float literal forbidden")
        tdp.joinpath("periodic_table_certificate.json").write_bytes(b'{"x": NaN}\n')
        check_raises_val(lambda: ptv.verify_committed_artifacts(tdp, cert, table), "disk json nan", "JSON non-finite constant forbidden")
        tdp.joinpath("periodic_table_certificate.json").write_bytes(b'{"a": 1, "a": 2}\n')
        check_raises_val(lambda: ptv.verify_committed_artifacts(tdp, cert, table), "disk json dup key", "Duplicate JSON key forbidden")
        tdp.joinpath("periodic_table_certificate.json").write_bytes((json.dumps(cert, sort_keys=True, indent=2) + "\n").replace("\n", "\r\n").encode("utf-8"))
        check_raises_val(lambda: ptv.verify_committed_artifacts(tdp, cert, table), "disk cert crlf", "CRLF forbidden in periodic_table_certificate.json")
        tdp.joinpath("periodic_table_certificate.json").write_bytes((json.dumps(cert, sort_keys=True, indent=2) + "\n").encode("utf-8"))
        tdp.joinpath("periodic_table_of_invariants.json").write_bytes((json.dumps(table, sort_keys=True, indent=2) + "\n").replace("\n", "\r\n").encode("utf-8"))
        check_raises_val(lambda: ptv.verify_committed_artifacts(tdp, cert, table), "disk table crlf", "CRLF forbidden in periodic_table_of_invariants.json")
        tdp.joinpath("periodic_table_of_invariants.json").write_bytes((json.dumps(table, sort_keys=True, indent=2) + "\n").encode("utf-8"))

        # Non-canonical whitespace in committed JSON files must also fail closed
        tdp.joinpath("periodic_table_certificate.json").write_text(json.dumps(cert, sort_keys=True, indent=2) + "\n\n", encoding="utf-8")
        check_raises_val(lambda: ptv.verify_committed_artifacts(tdp, cert, table), "cert non-canonical bytes", "periodic_table_certificate.json bytes differ")
        tdp.joinpath("periodic_table_certificate.json").write_text(json.dumps(cert, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        tdp.joinpath("periodic_table_of_invariants.json").write_text(json.dumps(table, sort_keys=True, indent=2) + "\n\n", encoding="utf-8")
        check_raises_val(lambda: ptv.verify_committed_artifacts(tdp, cert, table), "table non-canonical bytes", "periodic_table_of_invariants.json bytes differ")

    # Forged-hash refusals
    bad_cert_hash = copy.deepcopy(cert)
    bad_cert_hash["result_sha256"] = "0" * 64
    check_raises_val(lambda: ptv.validate_certificate(bad_cert_hash), "forged cert hash", "Certificate result_sha256 mismatch")

    bad_pt_hash = copy.deepcopy(table)
    bad_pt_hash["result_sha256"] = "0" * 64
    check_raises_val(lambda: ptv.validate_periodic_table(bad_pt_hash), "forged pt hash", "Periodic table result_sha256 mismatch")

    def tamper_cert(mutator: Callable[[dict[str, Any]], None], label: str, match: str) -> None:
        bad = copy.deepcopy(cert)
        mutator(bad)
        bad["result_sha256"] = ptv.canonical_sha256(bad)
        check_raises_val(lambda: ptv.validate_certificate(bad), label, match)

    tamper_cert(lambda d: d.__setitem__("schema_version", "bad"), "cert_schema", "Schema version mismatch")
    tamper_cert(lambda d: d.__setitem__("target_repo", "other/repo"), "cert_repo", "Target repo mismatch")
    tamper_cert(lambda d: d.__setitem__("compute_policy_status", "BAD"), "cert_policy", "Compute policy mismatch")
    tamper_cert(lambda d: d.__setitem__("ast_float_div_and_log_count", 1), "cert_ast", "AST must contain zero floats")

    def _set_pair(sec: str, tot_k: str, ok_k: str, val: int) -> Callable[[dict[str, Any]], None]:
        def _fn(d: dict[str, Any]) -> None:
            d[sec][tot_k] = val
            d[sec][ok_k] = val
        return _fn

    tamper_cert(_set_pair("four_class_obstructions", "class_a_diophantine_checks_total", "class_a_diophantine_checks_ok", 14), "h1_a_tot", "Expected 15 Class-A checks")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_a_diophantine_checks_ok", 14), "h1_a_ok", "Class-A check mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_a_zu_beats_22_7_floor", 999999), "forged_zu", "Zu Chongzhi floor witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_a_zu_first_beater", "22/7"), "forged_beater", "Zu first beater witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_a_antikythera_beat_9_times_53", 476), "forged_beat", "Antikythera beat witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_a_madhava_r3_n50_speedup_floor", 99999999999999), "C6_forged_madhava", "Madhava R3 n=50 speedup witness mismatch")

    tamper_cert(_set_pair("four_class_obstructions", "class_b_cancellation_checks_total", "class_b_cancellation_checks_ok", 10), "h1_b_tot", "Expected 11 Class-B checks")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_b_cancellation_checks_ok", 10), "h1_b_ok", "Class-B check mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_b_biruni_kappa", "1/1"), "forged_kappa", "Al-Biruni kappa witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_b_stereo_s2_bijection_count", 4), "forged_stereo", "Stereographic S^2 bijection count mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_b_cayley_s3_bijection_count", 4), "forged_cayley", "Cayley S^3 bijection count mismatch")

    tamper_cert(_set_pair("four_class_obstructions", "class_c_topological_checks_total", "class_c_topological_checks_ok", 17), "h1_c_tot", "Expected 18 Class-C checks")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_c_topological_checks_ok", 17), "h1_c_ok", "Class-C check mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_c_sona_576_exact_count", 575), "forged_sona576", "Sona 576/576 sweep mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_c_panini_43_c1p_count", 42), "forged_panini43", "Panini 43/43 C1P count mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_c_tucker_c3_single_copy_orders", 1), "forged_tucker", "Tucker C_3 witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_c_pingala_510_bijection_count", 509), "forged_pingala", "Pingala 510/510 bijection mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_c_fwht256_involution_and_parity", [255, 256]), "forged_fwht", "FWHT_256 witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_c_bamana_65536_even_and_a16", [1, 65536]), "C6_forged_bamana", "Bamana 65536 A_16 witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"]["class_c_a16_secded_matrix"].__setitem__("min_nonzero_weight", 3), "forged_a16_matrix", "A_16 SECDED 5x16 matrix witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_c_z2_twisted_vs_untwisted_sections", [1, 2]), "forged_z2", "Z_2 sheaf section witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_c_casarabe_vs_tree_betti1", [1, 0]), "forged_betti1", "Casarabe Betti_1 witness mismatch")

    tamper_cert(_set_pair("four_class_obstructions", "class_d_commutation_checks_total", "class_d_commutation_checks_ok", 7), "h1_d_tot", "Expected 8 Class-D checks")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_d_commutation_checks_ok", 7), "h1_d_ok", "Class-D check mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_d_schur_det_unreadable_to_readable", ["1", "1"]), "forged_schur_det", "Schur det witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_d_schur_trace_drop", "0"), "forged_trace_drop", "Schur trace drop witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_d_inertia_h8_vs_hydraulic8", [[8, 0, 0], [7, 0, 1]]), "forged_inertia", "Sylvester inertia separation mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_d_kemeny_snell_lumpability_defects", ["0", "0"]), "forged_markov", "Kemeny-Snell lumpability witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_d_trotter_defect_eps_1_4", "0"), "forged_trotter", "Trotter defect witness mismatch")

    tamper_cert(_set_pair("opposing_pair_conservation", "opposing_pair_checks_total", "opposing_pair_checks_ok", 12), "h2_tot", "Expected 13 opposing-pair checks")
    tamper_cert(lambda d: d["opposing_pair_conservation"].__setitem__("opposing_pair_checks_ok", 12), "h2_ok", "Opposing-pair check mismatch")
    tamper_cert(lambda d: d["opposing_pair_conservation"]["abelian_zero_residual_witnesses"].__setitem__("al_tusi_planar_curl", "1"), "forged_abelian", "Abelian zero-residual witnesses mismatch")
    tamper_cert(lambda d: d["opposing_pair_conservation"]["nonabelian_or_dissipative_nonzero_witnesses"].__setitem__("dougong_pi_zeta", "0"), "forged_nonabelian", "Non-Abelian or dissipative witnesses mismatch")

    tamper_cert(_set_pair("modular_flow_and_partition", "modular_flow_checks_total", "modular_flow_checks_ok", 14), "h3_tot", "Expected 15 modular-flow checks")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("modular_flow_checks_ok", 14), "h3_ok", "Modular-flow check mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("maya_crt_solution_mod_37960", 1), "forged_maya_x", "Maya CRT witness mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("maya_crt_bijection_exhaustive_ok", 37959), "forged_maya_exh", "Maya CRT exhaustive bijection mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("maya_grand_sync_lcm", 1), "forged_maya_lcm", "Maya grand sync LCM mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("maya_phase_compression_ratio", 1), "forged_maya_comp", "Maya phase compression mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("maya_dresden_eclipse_ratio", "1/1"), "forged_dresden", "Maya Dresden ratio mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("inconsistent_crt_refused", False), "h3_crt_refused", "Inconsistent CRT must be refused")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("antikythera_metonic_ratio", "1/1"), "forged_metonic", "Antikythera Metonic ratio mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("antikythera_anomalistic_rate", "1/1"), "forged_anom", "Antikythera anomalistic rate mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("two_clock_record_shift_delta_beta2", "0"), "forged_beta2", "Two-clock shift mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("two_clock_white_noise_delta_beta2", "1"), "forged_white_beta2", "Two-clock white-noise shift mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("panini_c1p_descriptor_ratio", "1/1"), "forged_panini", "Panini descriptor ratio mismatch")

    tamper_cert(lambda d: d["periodic_table_summary"].__setitem__("schema_version", "bad"), "pts_schema", "Periodic table schema mismatch")
    tamper_cert(lambda d: d["periodic_table_summary"].__setitem__("entry_count", 15), "pts_entries", "Expected 16 periodic table entries")
    tamper_cert(lambda d: d["periodic_table_summary"].__setitem__("family_count", 4), "pts_families", "Expected 5 morphological families")
    tamper_cert(lambda d: d["periodic_table_summary"].__setitem__("in_module_verified_entries", 15), "pts_inmod", "Expected 16 in-module verified entries")
    tamper_cert(lambda d: d["periodic_table_summary"].__setitem__("periodic_table_sha256", "0" * 63), "pts_63hex", "Periodic table SHA-256 must be 64-hex")
    tamper_cert(lambda d: d["periodic_table_summary"].__setitem__("periodic_table_sha256", "0" * 64), "pts_forged_sha64", "Certificate payload does not match recomputed build")
    tamper_cert(lambda d: d.__setitem__("forged_extra_field", 1), "cert_forged_extra", "Certificate payload does not match recomputed build")

    def tamper_pt(mutator: Callable[[dict[str, Any]], None], label: str, match: str) -> None:
        bad = copy.deepcopy(table)
        mutator(bad)
        bad["result_sha256"] = ptv.canonical_sha256(bad)
        check_raises_val(lambda: ptv.validate_periodic_table(bad), label, match)

    tamper_pt(lambda d: d.__setitem__("schema_version", "bad"), "pt_schema", "Periodic table schema mismatch")
    tamper_pt(lambda d: d.__setitem__("compute_policy_status", "BAD"), "pt_policy", "Periodic table policy mismatch")

    def _pt_15(d: dict[str, Any]) -> None:
        d["entry_count"] = 15
        d["entries"] = d["entries"][:15]

    tamper_pt(_pt_15, "pt_entry_count", "Expected 16 entries in periodic table")
    tamper_pt(lambda d: d["entries"].pop(), "pt_entries_len", "Periodic table entries length mismatch")
    tamper_pt(lambda d: d.__setitem__("family_count", 4), "pt_family_count", "Expected 5 families in periodic table")
    tamper_pt(lambda d: d.__setitem__("families", ["BAD"]), "pt_families_list", "Periodic table families list mismatch")

    tamper_pt(lambda d: d["entries"][0].__setitem__("entry_id", "PT-02"), "pt_dup_id", "Duplicate entry_id")
    tamper_pt(lambda d: d["entries"][0].__setitem__("family", "BOGUS_FAMILY"), "pt_bad_fam", "Invalid family")
    tamper_pt(lambda d: d["entries"][0].__setitem__("obstruction_class", "BOGUS_CLASS"), "pt_bad_obs", "Invalid obstruction_class")
    tamper_pt(lambda d: d["entries"][0].__setitem__("verification_scope", "CITED_ONLY"), "pt_bad_scope", "Entry must be IN_MODULE_EXACT")
    tamper_pt(lambda d: d["entries"][0].__setitem__("morphism_grade", "BOGUS_GRADE"), "pt_bad_grade", "Invalid morphism_grade")
    # Control C10: relabeling PT-01 from PROVABLE_OBSTRUCTION to EXACT_ISOMORPHISM MUST fail closed!
    tamper_pt(lambda d: d["entries"][0].__setitem__("morphism_grade", "EXACT_ISOMORPHISM"), "C10_relabel_grade", "Morphism grade mismatch for PT-01")
    tamper_pt(lambda d: d["entries"][0].__setitem__("exact_witness", "   "), "pt_empty_witness", "Empty exact_witness")

    def _drop_family(d: dict[str, Any]) -> None:
        for row in d["entries"]:
            if row["family"] == "SUBTRACTIVE_CANCELLATION_WALL":
                row["family"] = "DIOPHANTINE_RESONANCE_LATTICE"

    tamper_pt(_drop_family, "pt_missing_family_coverage", "Entries do not cover all 5 families")
    tamper_pt(lambda d: d["entries"][0].__setitem__("exact_witness", "FORGED_TEXT"), "pt_forged_witness", "Periodic table payload does not match recomputed build")
    tamper_pt(lambda d: d.__setitem__("forged_extra_field", 1), "pt_forged_extra", "Periodic table payload does not match recomputed build")


def main() -> int:
    test_ast_and_runtime_float_guards()
    test_primitives_and_boundaries()
    test_dynamic_morphism_evidence_degradation()
    test_cli_on_disk_binding_and_tampers()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
