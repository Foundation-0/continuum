#!/usr/bin/env python3
"""Track S174 (EXP-Q60a/b): Stage-2 Fortress Pure-Q/Z & Lean 4.36.0 Verifier.

Stdlib-only, zero floats, zero bare asserts, zero ast.Div (`/`), zero exec/eval,
zero unseeded RNG, 3x -I bit-identical (`-I -B`, `-I -O -B`, `-I -B -W error`).
"""
from __future__ import annotations

import argparse
import ast
import copy
import errno
from fractions import Fraction
import hashlib
import importlib
import json
import os
from pathlib import Path
import pwd
import re
import secrets
import stat
import subprocess
import sys
import tempfile
import tomllib
from typing import Any, Callable, Mapping, Sequence


MAX_BYTES = 2 * 1024 * 1024
MAX_JSON_DEPTH = 64
MAX_INT_DIGITS = 1024
MAX_FRAC_BITS = 3402
MAX_EXACT_INT_EXP = 4096
MAX_TOWER_HEIGHT = 64
MAX_EXP_DENOM = 10000
MAX_POLYLOG_EXP_DENOM = 64
MAX_EXP_VALUE = 1024
MAX_LOG_OFFSET = 1000000
MAX_POWER_WORK_BITS = 65536
MAX_POLYLOG_SHIFT_BITS = 65536
MAX_POLYLOG_M = 1 << 60
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.36.0"
EXPECTED_LEAN_VERSION_TOKEN = "version 4.36.0,"
MAX_LEAN_LINES = 420
PINNED_LEAN_SHA256 = "de3356872dbf6ab1d263d2a2167266e2ca99bc518e1df266a008ffbd9ae76b5e"
PINNED_THEOREM_SIG_SHA256 = "369d38789473f0efce7c1c57718aefb00023a79bf4f875fc0ce2d5153d6b3046"

EXPECTED_THEOREMS: tuple[str, ...] = (
    "GalacticShadow.crossover_horizon_unique",
    "GalacticShadow.affine_crossover_monotone_and_exact",
    "GalacticShadow.galactic_vs_terrestrial_dichotomy",
    "GalacticShadow.scale_inversion_cs09_galactic_dual",
    "GalacticShadow.two_sided_completeness_gate",
    "GalacticShadow.mux_cs09_vs_alkashi_exact_witness",
    "GalacticShadow.dark_mode_shadow_and_schur_erasure",
    "GalacticShadow.pi_inf_asymptotic_erasure_shadow",
    "GalacticShadow.finite_fourier_vs_fwht256_crossover",
    "GalacticShadow.karatsuba_exact_recurrence_global_crossover",
    "GalacticShadow.strassen_holosphere_cs29_real_crossovers",
    "GalacticShadow.lipton_demillo_sayward_r5_coupling_witness",
)
EXPECTED_ZERO_AXIOM_THEOREMS: frozenset[str] = frozenset({
    "GalacticShadow.crossover_horizon_unique",
    "GalacticShadow.galactic_vs_terrestrial_dichotomy",
    "GalacticShadow.scale_inversion_cs09_galactic_dual",
    "GalacticShadow.two_sided_completeness_gate",
})
EXPECTED_PROPEXT_ONLY_THEOREMS: frozenset[str] = frozenset({
    "GalacticShadow.mux_cs09_vs_alkashi_exact_witness",
    "GalacticShadow.lipton_demillo_sayward_r5_coupling_witness",
})
ALLOWED_AXIOMS: frozenset[str] = frozenset({"propext", "Quot.sound"})
EXPECTED_THEOREM_LIVE_TYPE_PINS: tuple[str, ...] = (
    "example : ∀ (P : Nat → Prop) (n1 n2 : Nat), GalacticShadow.IsCrossoverHorizon P n1 → GalacticShadow.IsCrossoverHorizon P n2 → n1 = n2 := @GalacticShadow.crossover_horizon_unique",
    "example : ∀ (fa sa fb sb : Nat), sa < sb → fb ≤ fa → (∀ n1 n2, n1 ≤ n2 → fa + sa * n1 < fb + sb * n1 → fa + sa * n2 < fb + sb * n2) ∧ GalacticShadow.IsCrossoverHorizon (fun n => fa + sa * n < fb + sb * n) ((fa - fb) / (sb - sa) + 1) := @GalacticShadow.affine_crossover_monotone_and_exact",
    "example : ∀ (P : Nat → Prop) (nStar nPhys : Nat), GalacticShadow.IsCrossoverHorizon P nStar → 1 ≤ nPhys → (nPhys < nStar → ∀ n, 1 ≤ n → n ≤ nPhys → ¬ P n) ∧ (nStar ≤ nPhys → P nPhys ∧ ∃ n, 1 ≤ n ∧ n ≤ nPhys ∧ P n) := @GalacticShadow.galactic_vs_terrestrial_dichotomy",
    "example : ∀ (q1 q2 : GalacticShadow.PosRat) (c M Ncrit Nphys Nstar : Nat), 0 < c → ∀ (hM : 0 < M) (hNc : 0 < Ncrit) (hNp : 0 < Nphys) (hNs : 0 < Nstar), (q1.inv.inv = q1) ∧ (GalacticShadow.PosRat.lt q2.inv q1.inv ↔ GalacticShadow.PosRat.lt q1 q2) ∧ (GalacticShadow.PosRat.lt (GalacticShadow.PosRat.unitRecip Ncrit hNc) (GalacticShadow.PosRat.unitRecip M hM) ↔ M < Ncrit) ∧ (GalacticShadow.PosRat.lt (GalacticShadow.PosRat.unitRecip Nstar hNs) (GalacticShadow.PosRat.unitRecip Nphys hNp) ↔ Nphys < Nstar) ∧ ((c * M < c * Ncrit ↔ M < Ncrit) ∧ (c * Nphys < c * Nstar ↔ Nphys < Nstar)) := @GalacticShadow.scale_inversion_cs09_galactic_dual",
    "example : ∀ (P TailFail : Nat → Prop) (nStar nPhys mObs nCrit : Nat), GalacticShadow.IsCrossoverHorizon P nStar → TailFail nCrit → (∀ k, k < nCrit → ¬ TailFail k) → ((nStar ≤ nPhys ∧ nCrit ≤ mObs) ↔ ((∃ n, 1 ≤ n ∧ n ≤ nPhys ∧ P n) ∧ (∃ k, k ≤ mObs ∧ TailFail k))) := @GalacticShadow.two_sided_completeness_gate",
    "example : (GalacticShadow.muxHalfMarginDen 9 10 3 = 542 ∧ 3 * 542 < 9 * 254) ∧ (GalacticShadow.muxHalfMarginDen 9 10 4 = 6878 ∧ 19 * 362 = 6878 ∧ 19 * 253 < 4 * 6878) ∧ (∀ S : Nat, 1 ≤ S → 9 ^ S < 10 ^ S ∧ 0 < GalacticShadow.muxHalfMarginDen 9 10 S) := @GalacticShadow.mux_cs09_vs_alkashi_exact_witness",
    "example : ∀ (v1 v2 : Int), (GalacticShadow.piInfMbb.applyVec v1 v2 = (0, 0) ↔ ∃ k : Int, v1 = -k ∧ v2 = k) ∧ (GalacticShadow.piInfAt 0 1 * (-1) + GalacticShadow.piInfAt 0 2 * 1 = -2 ∧ (-2 : Int) ≠ 0) ∧ (GalacticShadow.piInfMbb.mul (GalacticShadow.piInfPinvNum.mul GalacticShadow.piInfMbb) = GalacticShadow.piInfMbb.scale 8 ∧ GalacticShadow.piInfPinvNum.mul (GalacticShadow.piInfMbb.mul GalacticShadow.piInfPinvNum) = GalacticShadow.piInfPinvNum.scale 8 ∧ (GalacticShadow.piInfMbb.mul GalacticShadow.piInfPinvNum).transpose = GalacticShadow.piInfMbb.mul GalacticShadow.piInfPinvNum ∧ (GalacticShadow.piInfPinvNum.mul GalacticShadow.piInfMbb).transpose = GalacticShadow.piInfPinvNum.mul GalacticShadow.piInfMbb) ∧ (let pv := GalacticShadow.piInfPinvNum.applyVec (GalacticShadow.piInfAt 1 0) (GalacticShadow.piInfAt 2 0); 8 * GalacticShadow.piInfAt 0 0 - (GalacticShadow.piInfAt 0 1 * pv.1 + GalacticShadow.piInfAt 0 2 * pv.2) = 8 * 4) := @GalacticShadow.dark_mode_shadow_and_schur_erasure",
    "example : ∀ (cA cB eA eB nPhys : Nat), eA < eB → 0 < cB → 1 ≤ nPhys → cB * nPhys ^ eB ≤ cA * nPhys ^ eA → (∃ n0 : Nat, 1 ≤ n0 ∧ ∀ n, n0 ≤ n → cA * n ^ eA < cB * n ^ eB) ∧ GalacticShadow.piInfErasure nPhys (fun n => cA * n ^ eA < cB * n ^ eB) := @GalacticShadow.pi_inf_asymptotic_erasure_shadow",
    "example : GalacticShadow.IsCrossoverHorizon (fun m => 9 * (1 + m) < m * m) 10 ∧ GalacticShadow.IsCrossoverHorizon (fun m => 16 * (1 + m) < m * m) 17 ∧ (2 ^ 10 = 1024 ∧ 256 < 1024 ∧ 9 * (1 + 8) = 81 ∧ 8 * 8 = 64) ∧ (2 ^ 17 = 131072 ∧ 256 < 131072 ∧ 16 * (1 + 16) = 272 ∧ 16 * 16 = 256) := @GalacticShadow.finite_fourier_vs_fwht256_crossover",
    "example : (¬ (GalacticShadow.karatsubaSteps 164 < 2 * (164 * 164))) ∧ (∀ n, 165 ≤ n → n ≤ 256 → GalacticShadow.karatsubaSteps n < 2 * (n * n)) ∧ (∀ n, 257 ≤ n → n ≤ 279 → ¬ (GalacticShadow.karatsubaSteps n < 2 * (n * n))) ∧ (∀ n, 280 ≤ n → GalacticShadow.karatsubaSteps n < 2 * (n * n)) := @GalacticShadow.karatsuba_exact_recurrence_global_crossover",
    "example : (1366 ^ 24 < 4 ^ 125 ∧ 4 ^ 125 < 1367 ^ 24 ∧ 1367 ≤ 37837) ∧ GalacticShadow.IsCrossoverHorizon (fun t => 65536 + t < 12288 * t) 6 ∧ GalacticShadow.IsCrossoverHorizon (fun t => 19200 + 256 * t < 4096 * t) 6 ∧ GalacticShadow.IsCrossoverHorizon (fun m => 78 * m < m * m) 79 ∧ (∀ q : Nat, 2 ≤ q → 2 * (q ^ 4 + q ^ 2) < 2 * (1 + q + q ^ 2 + q ^ 3 + q ^ 4 + q ^ 5 + q ^ 3)) ∧ (2 ^ 266 < 590 ^ 64 ∧ 2 ^ 589 < 590 ^ 64 ∧ 590 ^ 64 < 2 ^ 590 ∧ 591 ^ 64 < 2 ^ 590) ∧ (590 ^ 64 + 1 < 2 ^ 590 ∧ 591 ^ 64 + 1 < 2 ^ 590 ∧ 592 ^ 64 < 2 * 591 ^ 64 + 1) := @GalacticShadow.strassen_holosphere_cs29_real_crossovers",
    "example : (GalacticShadow.ldsMaskGate 9 10 false false = 1 ∧ GalacticShadow.ldsMaskGate 10 10 false false = 1 ∧ GalacticShadow.ldsMaskGate 11 10 false false = 2) ∧ (GalacticShadow.ldsMaskGate 9 10 true false ≠ 1 ∧ GalacticShadow.ldsMaskGate 11 10 true false ≠ 2) ∧ (GalacticShadow.ldsMaskGate 9 10 false true ≠ 1 ∧ GalacticShadow.ldsMaskGate 11 10 false true ≠ 2) ∧ (GalacticShadow.ldsMaskGate 9 10 true true = 1 ∧ GalacticShadow.ldsMaskGate 11 10 true true = 2) ∧ (GalacticShadow.ldsMaskGate 10 10 true true ≠ 1) := @GalacticShadow.lipton_demillo_sayward_r5_coupling_witness",
)
SOURCE_FILES_TO_PIN: tuple[str, ...] = (
    "galactic_shadow_verifier.py",
    "test_galactic_shadow_r5.py",
)

_ZERO = Fraction(0, 1)
_ONE = Fraction(1, 1)
_FRAC_RE = re.compile(r"\A[+-]?[0-9]+(?:/[0-9]+)?\Z")
_VALID_COST_KINDS = frozenset({"power", "polylog_dyadic", "affine_linear", "tower_cutoff"})
_FORBIDDEN_AST_MODULES = frozenset({
    "math", "cmath", "decimal", "statistics", "numpy", "scipy", "torch", "random", "builtins",
    "operator", "_operator", "struct", "ctypes", "pickle", "marshal",
})
_FORBIDDEN_AST_NAMES = frozenset({
    "float", "complex", "pow", "eval", "exec", "compile", "__import__", "from_float", "from_decimal",
    "getattr", "setattr", "delattr", "vars", "globals", "locals", "__builtins__", "import_module",
    "truediv", "itruediv",
})
_FORBIDDEN_AST_ATTRS = frozenset({
    "from_float", "from_decimal", "truediv", "itruediv", "pow", "ipow",
    "__truediv__", "__rtruediv__", "__itruediv__", "__pow__", "__rpow__", "__ipow__", "__float__", "__complex__",
    "__import__", "__builtins__", "exec_module", "load_module", "module_from_spec", "spec_from_file_location",
})
# MED-3 (Delta-2): the ONLY permitted dynamic import target (live aletheia.calculus parity).
_ALLOWED_DYNAMIC_IMPORTS = frozenset({"aletheia.calculus"})
_HEX_DIGITS = frozenset("0123456789abcdefABCDEF")
# S168 Delta-3 Lean 4.36.0 interpolation hardening: ONLY Init-reserved prefixes (`s!`, `f!`, `println!`)
# enter interpolated-string mode. All ambiguous prefixes (`dbg_trace`, `m!`, `throwError`, `throwErrorAt`,
# `log*`, arg macros, arbitrary `<ident>!`) followed by `{`/`}` strings fail closed (`LEAN_AMBIG_INTERP`).
_INIT_INTERP_BANGS = frozenset({"s!", "f!", "println!"})
_AMBIG_INTERP_PLAINS = frozenset({"dbg_trace", "throwError", "logInfo", "logError", "logWarning"})
_ALLOWLIST_INTERP_ARG_MACROS: dict[str, tuple[int, bool]] = {
    "Macro.trace": (1, True),
    "trace_goal": (1, True),
    "trace": (1, True),
    "throwNamedErrorAt": (2, False),
    "logNamedErrorAt": (2, False),
    "logNamedWarningAt": (2, False),
    "throwErrorAt": (1, False),
    "throwNamedError": (1, False),
    "logNamedError": (1, False),
    "logNamedWarning": (1, False),
}
_FORBIDDEN_KW_TOKENS = frozenset({
    "sorry", "admit", "axiom", "unsafe", "opaque", "instance", "stop",
    "native_decide", "bv_decide", "bv_check",
    "run_cmd", "run_meta", "run_tac", "run_elab", "by_elab", "initialize", "builtin_initialize",
    "syntax", "macro", "macro_rules", "elab", "elab_rules", "declare_syntax_cat",
    "notation", "infix", "infixl", "infixr", "prefix", "postfix",
    "import",
})
_FORBIDDEN_IDENT_TOKENS = frozenset({
    "sorryAx", "mkSorry", "ofReduceBool", "ofReduceNat", "trustCompiler", "_native",
})
_FORBIDDEN_DEBUG_SUFFIXES = frozenset({
    "skipKernelTC", "byAsSorry", "proofAsSorry", "terminalTacticsAsSorry",
})
_FORBIDDEN_HASH_CMDS = frozenset({"eval", "eval!", "reduce", "exit", "guard_msgs", "check_failure", "print"})
_FORBIDDEN_ATTR_TOKENS = frozenset({"extern", "implemented_by", "export", "init", "builtin_init", "macro", "elab", "tactic", "default_instance"})
_PARTIAL_TARGETS = frozenset({"def", "instance", "abbrev", "theorem", "lemma", "opaque"})
_TOP_DECL_WORDS = frozenset({
    "theorem", "lemma", "def", "abbrev", "opaque", "axiom", "example", "instance",
    "structure", "inductive", "class", "namespace", "section", "end",
    "variable", "universe", "attribute", "private", "protected", "noncomputable",
    "unsafe", "partial", "scoped", "local",
})
_ALLOWED_TOML_TOP_KEYS = frozenset({"name", "version", "defaultTargets", "lean_lib"})
_ALLOWED_TOML_LIB_KEYS = frozenset({"name", "srcDir", "roots", "globs"})
_SKIP_DIR_SEGS = frozenset({".git", ".lake", ".venv", "venv", "node_modules", "__pycache__"})
_MOD_RE = re.compile(r"\A[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\Z")
_GLOB_RE = re.compile(r"\A[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*(?:\.\+|\.\*)?\Z")
_PKG_NAME_RE = re.compile(r"\A[A-Za-z_][A-Za-z0-9_-]*\Z")
_VER_RE = re.compile(r"\A[0-9]+\.[0-9]+\.[0-9]+(?:-[A-Za-z0-9.-]+)?\Z")
_AXIOM_NONE_RE = re.compile(r"\A'([^']+)' does not depend on any axioms\Z")
_AXIOM_LIST_RE = re.compile(r"\A'([^']+)' depends on axioms: \[([^\]]*)\]\Z")
_LEAN_WARN_RE = re.compile(r"(?:^|\s)warning(?:\s*\([^)]*\))?:", re.IGNORECASE)
_UNSAFE_TOML_STRS = ("debug.byAsSorry", "debug.skipKernelTC", "debug.proofAsSorry", "debug.terminalTacticsAsSorry")


class VerifierError(ValueError):
    """Fail-closed error raised by the Track S174 Stage-2 verifier."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class _HelpExit(Exception):
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload
        super().__init__("HELP")


def need(cond: bool, code: str, message: str) -> None:
    """Fail-closed non-assert guard (survives python3 -O)."""
    if not cond:
        raise VerifierError(code, message)


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def is_exact_int(val: Any) -> bool:
    """Strict exact int check (rejects bool)."""
    return type(val) is int


def require_strict_int(
    val: Any,
    name: str,
    *,
    min_value: int | None = None,
    max_value: int | None = None,
) -> int:
    need(type(val) is int, "STRICT_INT_REQUIRED", f"{name} must be exact int, got {type(val).__name__}")
    if min_value is not None:
        need(val >= min_value, "INT_OUT_OF_RANGE", f"{name} must be >= {min_value}, got {val}")
    if max_value is not None:
        need(val <= max_value, "INT_OUT_OF_RANGE", f"{name} must be <= {max_value}, got {val}")
    return val


def require_fraction(val: Any, name: str, *, positive: bool = False, non_negative: bool = False) -> Fraction:
    need(type(val) is not bool, "BOOL_FORBIDDEN", f"{name} must not be bool")
    need(type(val).__name__ != "float", "FLOAT_FORBIDDEN", f"{name} must not be float")
    if isinstance(val, Fraction):
        frac = val
    elif type(val) is int:
        frac = Fraction(val, 1)
    elif isinstance(val, str):
        s = val.strip()
        need(_FRAC_RE.match(s) is not None, "FLOAT_TEXT_FORBIDDEN", f"{name} must be strict ASCII rational")
        parts = s.split("/", 1)
        for part in parts:
            dig = part[1:] if part.startswith(("+", "-")) else part
            need(len(dig) <= MAX_INT_DIGITS, "FRAC_TOO_LONG", f"{name}: rational term > {MAX_INT_DIGITS} digits")
        try:
            frac = Fraction(s)
        except ZeroDivisionError as exc:
            raise VerifierError("BAD_FRACTION_STRING", f"{name}: zero denominator {val!r}") from exc
    else:
        raise VerifierError("BAD_FRACTION_TYPE", f"{name}: unsupported type {type(val).__name__}")
    need(
        abs(frac.numerator).bit_length() <= MAX_FRAC_BITS and frac.denominator.bit_length() <= MAX_FRAC_BITS,
        "FRAC_TOO_LONG",
        f"{name}: rational term exceeds {MAX_FRAC_BITS}-bit bound",
    )
    if positive:
        need(frac > _ZERO, "FRACTION_NOT_POSITIVE", f"{name} must be > 0, got {frac}")
    elif non_negative:
        need(frac >= _ZERO, "FRACTION_NEGATIVE", f"{name} must be >= 0, got {frac}")
    return frac


def qdiv(a: Fraction, b: Fraction) -> Fraction:
    """Exact rational division without ast.Div (`/`)."""
    need(b != _ZERO, "ZERO_DIVISOR", "rational divisor must be nonzero")
    return Fraction(a.numerator * b.denominator, a.denominator * b.numerator)


def fmt_q(val: Fraction) -> str:
    return f"{val.numerator}/{val.denominator}"


def _exact_isqrt_if_square(n: int) -> int | None:
    if n < 0:
        return None
    if n == 0:
        return 0
    r = 1 << ((n.bit_length() + 1) // 2)
    while True:
        nr = (r + n // r) // 2
        if nr >= r:
            break
        r = nr
    return r if r * r == n else None


def _ipow(base: int, exp: int) -> int:
    """Exact int power with a runtime-proved non-negative int exponent (int ** int>=0 never yields float).

    MED-3 (Delta-2): every non-literal `**` in pinned sources must route through this guard; the AST gate
    only admits `**` whose exponent is a non-negative int literal.
    """
    need(type(base) is int and type(exp) is int and exp >= 0, "IPOW_DOMAIN", "_ipow requires int base and non-negative int exponent")
    result = 1
    while exp > 0:
        if exp & 1:
            result *= base
        exp >>= 1
        if exp:
            base *= base
    return result


def _iroot_floor(x: int, k: int) -> int:
    """Exact floor(x^(1/k)) for x >= 1, k >= 1 via integer Newton descent from the upper bound 2^ceil(bits/k)."""
    r = 1 << ((x.bit_length() + k - 1) // k)
    while True:
        nr = ((k - 1) * r + x // _ipow(r, k - 1)) // k
        if nr >= r:
            break
        r = nr
    return r


def _is_nonneg_int_literal(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and type(node.value) is int and node.value >= 0


def verify_pure_q_ast(source_text: str, label: str) -> None:
    """Verify Python source uses zero floats, zero float()/pow()/operator/getattr, literal-only ** exponents, zero bare asserts, zero ast.Div."""
    try:
        tree = ast.parse(source_text, filename=label)
    except SyntaxError as exc:
        raise VerifierError("AST_SYNTAX", f"{label}: {exc}") from exc
    # ast.walk is breadth-first, so an allowlisted Call is always visited before its `func` Attribute child.
    allowed_dyn_imports: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "import_module"
            and len(node.args) == 1
            and not node.keywords
            and isinstance(node.args[0], ast.Constant)
            and node.args[0].value in _ALLOWED_DYNAMIC_IMPORTS
        ):
            allowed_dyn_imports.add(id(node.func))
        need(not isinstance(node, ast.Div), "AST_DIV_FORBIDDEN", f"{label}: ast.Div forbidden")
        need(not isinstance(node, ast.Assert), "AST_ASSERT_FORBIDDEN", f"{label}: bare assert forbidden")
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
            neg_u = isinstance(node.right, ast.UnaryOp) and isinstance(node.right.op, ast.USub)
            need(not neg_u, "AST_NEG_POW_FORBIDDEN", f"{label}: negative exponent produces float")
            need(_is_nonneg_int_literal(node.right), "AST_NONLITERAL_POW_FORBIDDEN", f"{label}: ** exponent must be a non-negative int literal (use _ipow)")
        elif isinstance(node, ast.AugAssign) and isinstance(node.op, ast.Pow):
            need(_is_nonneg_int_literal(node.value), "AST_NONLITERAL_POW_FORBIDDEN", f"{label}: **= exponent must be a non-negative int literal (use _ipow)")
        if isinstance(node, ast.Constant):
            tname = type(node.value).__name__
            need(tname != "float" and tname != "complex", "AST_FLOAT_LITERAL", f"{label}: {tname} literal forbidden")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                need(alias.name.split(".", 1)[0] not in _FORBIDDEN_AST_MODULES, "AST_FORBIDDEN_IMPORT", f"{label}: {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            need((node.module or "").split(".", 1)[0] not in _FORBIDDEN_AST_MODULES, "AST_FORBIDDEN_IMPORT", f"{label}: {node.module}")
            for alias in node.names:
                need(alias.name not in _FORBIDDEN_AST_NAMES and alias.name not in _FORBIDDEN_AST_ATTRS, "AST_FORBIDDEN_NAME", f"{label}: {alias.name}")
        elif isinstance(node, ast.Name):
            need(node.id not in _FORBIDDEN_AST_NAMES, "AST_FORBIDDEN_NAME", f"{label}: {node.id}")
        elif isinstance(node, ast.Attribute):
            need(node.attr not in _FORBIDDEN_AST_ATTRS, "AST_FORBIDDEN_ATTR", f"{label}: {node.attr}")
            need(node.attr != "import_module" or id(node) in allowed_dyn_imports, "AST_FORBIDDEN_DYNAMIC_IMPORT", f"{label}: non-allowlisted import_module")


def exact_json_equal(a: Any, b: Any) -> bool:
    """Iterative type-exact JSON equality checking BOTH dict key types and value types."""
    stack: list[tuple[Any, Any]] = [(a, b)]
    while stack:
        x, y = stack.pop()
        if type(x) is not type(y):
            return False
        if type(x) is dict:
            if len(x) != len(y):
                return False
            xt = {(type(k), k): v for k, v in x.items()}
            yt = {(type(k), k): v for k, v in y.items()}
            for tk, xv in xt.items():
                if tk not in yt:
                    return False
                stack.append((xv, yt[tk]))
        elif type(x) is list:
            if len(x) != len(y):
                return False
            for xv, yv in zip(x, y):
                stack.append((xv, yv))
        elif x != y:
            return False
    return True


def _open_parent_dir_fd(path: Any, label: str) -> tuple[int, str]:
    if type(path) is str:
        need(len(path) > 0, "BAD_PATH", f"{label}: empty path")
        p = Path(path)
    else:
        need(isinstance(path, Path), "BAD_PATH_TYPE", f"{label}: expected str or Path")
        p = path
    raw = os.fspath(p)
    need("\x00" not in raw, "BAD_PATH", f"{label}: NUL byte forbidden")
    parts = p.parts
    need(".." not in parts, "DOTDOT_FORBIDDEN", f"{label}: '..' traversal forbidden")
    anchor = os.sep if p.is_absolute() else "."
    segs = parts[1:] if p.is_absolute() else parts
    need(len(segs) >= 1, "BAD_LEAF", f"{label}: invalid leaf")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    cur_fd = -1
    try:
        cur_fd = os.open(anchor, flags)
        for seg in segs[:-1]:
            nxt = os.open(seg, flags, dir_fd=cur_fd)
            os.close(cur_fd)
            cur_fd = nxt
        return cur_fd, segs[-1]
    except OSError as exc:
        if cur_fd >= 0:
            os.close(cur_fd)
        raise VerifierError("PARENT_OPEN", f"{label}: {exc}") from exc


def read_nofollow_bytes(path: str | Path, label: str = "file", max_bytes: int = MAX_BYTES) -> bytes:
    """Read regular non-symlink, non-hardlink file under O_NOFOLLOW | O_NONBLOCK."""
    parent_dfd, leaf = _open_parent_dir_fd(path, label)
    fd = -1
    try:
        try:
            fd = os.open(leaf, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_dfd)
            st = os.fstat(fd)
        except OSError as exc:
            raise VerifierError("OPEN_FAILED", f"{label}: {exc}") from exc
        need(stat.S_ISREG(st.st_mode), "NOT_REG_FILE", f"{label}: not a regular file")
        need(st.st_nlink == 1, "HARDLINK_REJECTED", f"{label}: hardlink forbidden (nlink={st.st_nlink})")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(fd, 65536)
            if not chunk:
                break
            total += len(chunk)
            need(total <= max_bytes, "FILE_TOO_BIG", f"{label}: exceeds {max_bytes} bytes")
            chunks.append(chunk)
        return b"".join(chunks)
    finally:
        if fd >= 0:
            os.close(fd)
        os.close(parent_dfd)


def _check_json_depth_surrogates(obj: Any, max_depth: int = MAX_JSON_DEPTH) -> None:
    stack: list[tuple[Any, int]] = [(obj, 1)]
    while stack:
        cur, depth = stack.pop()
        if type(cur) is str:
            for ch in cur:
                need(not (0xD800 <= ord(ch) <= 0xDFFF), "JSON_SURROGATE", "lone surrogate forbidden")
        elif type(cur) is dict:
            need(depth <= max_depth, "JSON_DEPTH", "JSON depth exceeded")
            for k, v in cur.items():
                stack.append((k, depth + 1))
                stack.append((v, depth + 1))
        elif type(cur) is list:
            need(depth <= max_depth, "JSON_DEPTH", "JSON depth exceeded")
            for v in cur:
                stack.append((v, depth + 1))


def parse_exact_json(raw: bytes, label: str = "json") -> Any:
    """Strict float-free JSON parser (no BOM/CR/CRLF, trailing LF, no duplicate keys)."""
    need(len(raw) > 0, "EMPTY_JSON", f"{label}: empty JSON")
    need(not raw.startswith(b"\xef\xbb\xbf"), "BOM_FORBIDDEN", f"{label}: BOM forbidden")
    need(b"\r" not in raw, "CR_FORBIDDEN", f"{label}: CR/CRLF forbidden")
    need(raw.endswith(b"\n"), "NO_FINAL_LF", f"{label}: trailing LF required")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerifierError("BAD_UTF8", f"{label}: invalid UTF-8") from exc

    def _no_float(tok: str) -> Any:
        raise VerifierError("FLOAT_FORBIDDEN", f"{label}: float forbidden: {tok!r}")

    def _no_const(tok: str) -> Any:
        raise VerifierError("CONST_FORBIDDEN", f"{label}: non-finite constant: {tok!r}")

    def _strict_int(tok: str) -> int:
        digits = len(tok) - 1 if tok.startswith("-") else len(tok)
        need(digits <= MAX_INT_DIGITS, "INT_TOO_LONG", f"{label}: integer > {MAX_INT_DIGITS} digits")
        return int(tok)

    def _no_dup(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        d: dict[str, Any] = {}
        for k, v in pairs:
            need(k not in d, "DUP_KEY", f"{label}: duplicate key {k!r}")
            d[k] = v
        return d

    try:
        obj = json.loads(
            text,
            parse_float=_no_float,
            parse_constant=_no_const,
            parse_int=_strict_int,
            object_pairs_hook=_no_dup,
        )
    except VerifierError:
        raise
    except (ValueError, RecursionError) as exc:
        raise VerifierError("JSON_SYNTAX", f"{label}: {exc}") from exc
    _check_json_depth_surrogates(obj)
    return obj


def _canon_bytes(obj: dict[str, Any]) -> bytes:
    return (json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")


def atomic_write_nofollow(path: str | Path, raw: bytes) -> None:
    """Atomically write LF-only bytes with O_NOFOLLOW + O_EXCL + 0o644."""
    parent_dfd, leaf = _open_parent_dir_fd(path, "write_cert")
    tmp_name = f".{leaf[:48]}.s174_{os.getpid()}_{secrets.token_hex(8)}.tmp"
    fd = -1
    created = False
    try:
        try:
            st = os.lstat(leaf, dir_fd=parent_dfd)
        except FileNotFoundError:
            st = None
        except OSError as exc:
            raise VerifierError("WRITE_LSTAT", str(exc)) from exc
        mode = 0o644
        if st is not None:
            need(stat.S_ISREG(st.st_mode), "WRITE_NOT_REG", "existing write target is not regular")
            need(st.st_nlink == 1, "WRITE_HARDLINK", "refusing to overwrite hardlinked target")
            mode = stat.S_IMODE(st.st_mode)
        try:
            fd = os.open(tmp_name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode, dir_fd=parent_dfd)
            created = True
            os.fchmod(fd, mode)
            off = 0
            while off < len(raw):
                n = os.write(fd, raw[off:])
                need(n > 0, "WRITE_ZERO", "short zero write")
                off += n
            os.fsync(fd)
            os.close(fd)
            fd = -1
            os.replace(tmp_name, leaf, src_dir_fd=parent_dfd, dst_dir_fd=parent_dfd)
            created = False
        except OSError as exc:
            raise VerifierError("WRITE_IO", str(exc)) from exc
        try:
            os.fsync(parent_dfd)
        except OSError as exc:
            if exc.errno not in (errno.EINVAL, errno.EROFS):
                raise VerifierError("DIR_FSYNC", str(exc)) from exc
    finally:
        if fd >= 0:
            os.close(fd)
        if created:
            try:
                os.unlink(tmp_name, dir_fd=parent_dfd)
            except OSError:
                pass
        os.close(parent_dfd)


# ---------------------------------------------------------------------------
# Hardened Lean 4.36.0 Static Lexer/Auditor & Isolated Live ELF Verifier
# (Matches S168 Delta-3: dbg_trace / m! / throwError / throwErrorAt / stop / macro_rules)
# ---------------------------------------------------------------------------

def _char_lit_end(src: str, i: int, n: int) -> int | None:
    if i + 2 < n and src[i + 1] not in ("\\", "'") and src[i + 2] == "'":
        return i + 3
    if i + 3 < n and src[i + 1] == "\\":
        if src[i + 3] == "'" and src[i + 2] != "\n":
            return i + 4
        esc = src[i + 2]
        if esc == "x" and i + 5 < n and src[i + 5] == "'" and all(c in _HEX_DIGITS for c in src[i + 3 : i + 5]):
            return i + 6
        if esc == "u" and i + 7 < n and src[i + 7] == "'" and all(c in _HEX_DIGITS for c in src[i + 3 : i + 7]):
            return i + 8
    return None


def _is_id_start(ch: str) -> bool:
    return ch.isalpha() or ch == "_"


def _is_id_cont(ch: str) -> bool:
    return ch.isalnum() or ch in "_'!?"


def tokenize_lean4(source: str) -> list[tuple[str, str, int]]:
    """Typed-token Lean 4.36.0 lexer matching S168 Delta-3 fail-closed interpolation guard."""
    tokens: list[tuple[str, str, int]] = []
    i = 0
    n = len(source)
    lineno = 1
    interp_braces: list[int] = []
    pending_args = 0
    arg_depth = 0
    ambig_next_quote = False
    prev_was_dot = False
    # MED-2 (Delta-2): once an allowlisted argument macro is seen, EVERY subsequent plain string forbids `{`/`}`
    # until a proven command boundary (a column-0 top-level declaration keyword), independent of pending_args
    # argument counting (closes `s!"a"`, `r#"a"#`, `'a'`, and compound `x[0]!` first-argument bypasses).
    macro_guard = False

    def _consume_block_comment(pos: int) -> tuple[int, int]:
        depth = 1
        step = 3 if (pos + 2 < n and source[pos + 2] in ("-", "!")) else 2
        ln_inc = 0
        p = pos + step
        while p < n and depth > 0:
            if source.startswith("/-", p):
                depth += 1
                p += 2
            elif source.startswith("-/", p):
                depth -= 1
                p += 2
            else:
                if source[p] == "\n":
                    ln_inc += 1
                p += 1
        need(depth == 0, "LEAN_UNTERM_LEX", "unterminated block comment")
        return p, ln_inc

    def _consume_plain_string(pos: int, *, forbid_braces: bool, start_line: int) -> tuple[int, int]:
        p = pos + 1
        ln_inc = 0
        while p < n:
            if source[p] == "\\" and p + 1 < n:
                need(not (forbid_braces and source[p + 1] in "{}"), "LEAN_AMBIG_INTERP", f"line {start_line}: ambiguous non-Init interpolated string with braces")
                if source[p + 1] == "\n":
                    ln_inc += 1
                p += 2
            elif source[p] == '"':
                return p + 1, ln_inc
            else:
                need(not (forbid_braces and source[p] in "{}"), "LEAN_AMBIG_INTERP", f"line {start_line}: ambiguous non-Init interpolated string with braces")
                if source[p] == "\n":
                    ln_inc += 1
                p += 1
        raise VerifierError("LEAN_UNTERM_LEX", "unterminated string literal")

    def _consume_raw_string(pos: int, hashes: int) -> tuple[int, int]:
        close_seq = '"' + ("#" * hashes)
        p = pos + 2 + hashes
        ln_inc = 0
        while p < n:
            if source.startswith(close_seq, p):
                return p + len(close_seq), ln_inc
            if source[p] == "\n":
                ln_inc += 1
            p += 1
        raise VerifierError("LEAN_UNTERM_LEX", "unterminated raw string literal")

    def _peek_next_code(pos: int) -> int:
        p = pos
        while p < n:
            if source[p].isspace():
                p += 1
            elif source.startswith("--", p):
                while p < n and source[p] != "\n":
                    p += 1
            elif source.startswith("/-", p):
                p, _ = _consume_block_comment(p)
            else:
                break
        return p

    while i < n:
        if interp_braces and interp_braces[-1] == 0:
            ch = source[i]
            if ch == "\\" and i + 1 < n:
                if source[i + 1] == "\n":
                    lineno += 1
                i += 2
            elif ch == '"':
                interp_braces.pop()
                i += 1
            elif ch == "{":
                interp_braces[-1] = 1
                prev_was_dot = False
                i += 1
            else:
                if ch == "\n":
                    lineno += 1
                i += 1
            continue

        ch = source[i]
        if ch == "\n":
            tokens.append(("NL", "\n", lineno))
            lineno += 1
            i += 1
            continue
        if ch.isspace():
            i += 1
            continue
        if source.startswith("--", i):
            while i < n and source[i] != "\n":
                i += 1
            continue
        if source.startswith("/-", i):
            i, inc = _consume_block_comment(i)
            lineno += inc
            continue

        was_ambig = ambig_next_quote
        ambig_next_quote = False

        if ch == "r" and not prev_was_dot:
            j = i + 1
            while j < n and source[j] == "#":
                j += 1
            if j < n and source[j] == '"':
                i, inc = _consume_raw_string(i, j - (i + 1))
                lineno += inc
                prev_was_dot = False
                if pending_args > 0 and arg_depth == 0:
                    pending_args -= 1
                    ambig_next_quote = pending_args == 0
                continue

        if ch == '"':
            i, inc = _consume_plain_string(i, forbid_braces=was_ambig or macro_guard, start_line=lineno)
            lineno += inc
            prev_was_dot = False
            if pending_args > 0 and arg_depth == 0:
                pending_args -= 1
                ambig_next_quote = pending_args == 0
            continue

        if ch == "'":
            cend = _char_lit_end(source, i, n)
            if cend is not None:
                if source[i + 1] == "\n":
                    lineno += 1
                i = cend
                prev_was_dot = False
                if pending_args > 0 and arg_depth == 0:
                    pending_args -= 1
                    ambig_next_quote = pending_args == 0
                continue

        if ch == "«":
            end_g = source.find("»", i + 1)
            need(end_g != -1, "LEAN_UNTERM_IDENT", "unterminated guillemet identifier")
            inner = source[i + 1 : end_g]
            ln_inc = inner.count("\n")
            ident = inner.replace("\n", " ").strip()
            if ident:
                tokens.append(("IDENT", ident, lineno))
            lineno += ln_inc
            i = end_g + 1
            prev_was_dot = False
            if pending_args > 0 and arg_depth == 0:
                pending_args -= 1
                ambig_next_quote = pending_args == 0
            continue

        if ch.isdigit():
            k = i + 1
            while k < n and (source[k].isalnum() or source[k] == "_"):
                k += 1
            tokens.append(("NUM", source[i:k], lineno))
            i = k
            prev_was_dot = False
            if pending_args > 0 and arg_depth == 0:
                pending_args -= 1
                ambig_next_quote = pending_args == 0
            continue

        if interp_braces:
            if ch == "{":
                interp_braces[-1] += 1
                tokens.append(("SYM", "{", lineno))
                prev_was_dot = False
                i += 1
                continue
            if ch == "}":
                interp_braces[-1] -= 1
                if interp_braces[-1] > 0:
                    tokens.append(("SYM", "}", lineno))
                prev_was_dot = False
                i += 1
                continue

        if _is_id_start(ch):
            k = i + 1
            while k < n and _is_id_cont(source[k]):
                k += 1
            tok = source[i:k]
            if tok in _TOP_DECL_WORDS and (i == 0 or source[i - 1] == "\n"):
                macro_guard = False
            if not prev_was_dot and tok == "Macro" and k < n and source[k] == "." and source.startswith("trace[", k + 1):
                tokens.append(("IDENT", "Macro.trace", lineno))
                tokens.append(("SYM", "[", lineno))
                i = k + 7
                pending_args = 1
                arg_depth = 1
                macro_guard = True
                prev_was_dot = False
                continue
            if not prev_was_dot and tok in _ALLOWLIST_INTERP_ARG_MACROS:
                argc, needs_br = _ALLOWLIST_INTERP_ARG_MACROS[tok]
                if needs_br and k < n and source[k] == "[":
                    tokens.append(("IDENT", tok, lineno))
                    tokens.append(("SYM", "[", lineno))
                    i = k + 1
                    pending_args = argc
                    arg_depth = 1
                    macro_guard = True
                    prev_was_dot = False
                    continue
                if not needs_br:
                    tokens.append(("IDENT", tok, lineno))
                    i = k
                    pending_args = argc
                    arg_depth = 0
                    macro_guard = True
                    prev_was_dot = False
                    continue
            if not prev_was_dot and tok in _INIT_INTERP_BANGS:
                nxt_q = _peek_next_code(k)
                if nxt_q < n and source[nxt_q] == '"':
                    lineno += source.count("\n", i, nxt_q + 1)
                    interp_braces.append(0)
                    i = nxt_q + 1
                    prev_was_dot = False
                    if pending_args > 0 and arg_depth == 0:
                        pending_args -= 1
                        ambig_next_quote = pending_args == 0
                    continue
            if not prev_was_dot and (tok.endswith("!") or tok in _AMBIG_INTERP_PLAINS):
                nxt_q = _peek_next_code(k)
                if nxt_q < n and source[nxt_q] == '"':
                    ambig_next_quote = True
            tokens.append(("IDENT", tok, lineno))
            i = k
            prev_was_dot = False
            if pending_args > 0 and arg_depth == 0 and not (i < n and source[i] == "."):
                pending_args -= 1
                ambig_next_quote = pending_args == 0
            continue

        if source.startswith(":=", i):
            tokens.append(("SYM", ":=", lineno))
            prev_was_dot = False
            i += 2
            continue

        if pending_args > 0:
            if ch in "([{":
                arg_depth += 1
            elif ch in ")]}" and arg_depth > 0:
                arg_depth -= 1
                if arg_depth == 0:
                    pending_args -= 1
                    ambig_next_quote = pending_args == 0
            elif arg_depth == 0 and ch != ".":
                pending_args = 0

        tokens.append(("SYM", ch, lineno))
        prev_was_dot = (ch == ".")
        i += 1

    need(len(interp_braces) == 0, "LEAN_UNTERM_LEX", "unterminated interpolated string")
    return tokens


def _audit_lean_token_stream(raw_toks: list[tuple[str, str, int]]) -> tuple[list[str], dict[str, list[str]]]:
    toks: list[tuple[str, str, int]] = []
    idx = 0
    nt = len(raw_toks)
    while idx < nt:
        k, txt, ln = raw_toks[idx]
        if k == "IDENT" and txt == "_root_":
            j = idx + 1
            while j < nt and raw_toks[j][0] == "NL":
                j += 1
            if j < nt and raw_toks[j][0] == "SYM" and raw_toks[j][1] == ".":
                idx = j + 1
                continue
        toks.append((k, txt, ln))
        idx += 1

    code: list[tuple[str, str, int]] = [t for t in toks if t[0] != "NL"]
    nc = len(code)
    has_var = False
    has_inc = False

    for ci, (kind, txt, ln) in enumerate(code):
        if kind == "IDENT":
            need(txt not in _FORBIDDEN_KW_TOKENS, "LEAN_FORBIDDEN_KW", f"line {ln}: forbidden keyword {txt!r}")
            need(txt not in _FORBIDDEN_IDENT_TOKENS, "LEAN_FORBIDDEN_AX", f"line {ln}: forbidden identifier {txt!r}")
            if txt == "variable":
                has_var = True
            elif txt == "include":
                has_inc = True
            elif txt == "Lean" and ci + 2 < nc and code[ci + 1][1] == "." and code[ci + 2][1] in ("Elab", "Meta"):
                raise VerifierError("LEAN_META_ESCAPE", f"line {ln}: forbidden Lean.{code[ci + 2][1]}")
            elif txt == "debug" and ci + 2 < nc and code[ci + 1][1] == "." and code[ci + 2][1] in _FORBIDDEN_DEBUG_SUFFIXES:
                raise VerifierError("LEAN_DEBUG_ESCAPE", f"line {ln}: forbidden debug.{code[ci + 2][1]}")
            elif txt == "partial":
                j = ci + 1
                while j < nc and code[j][1] in ("private", "protected", "noncomputable", "unsafe"):
                    j += 1
                if j < nc and code[j][1] in _PARTIAL_TARGETS:
                    raise VerifierError("LEAN_PARTIAL", f"line {ln}: partial declaration forbidden")
            elif txt == "decide":
                j = ci + 1
                while j < nc:
                    if code[j][1] == "+":
                        j += 2
                    elif code[j][1] == "(":
                        pdepth = 1
                        j += 1
                        while j < nc and pdepth > 0:
                            if code[j][1] == "(":
                                pdepth += 1
                            elif code[j][1] == ")":
                                pdepth -= 1
                            elif code[j][1] in ("native", "config"):
                                raise VerifierError("LEAN_DECIDE_NATIVE", f"line {ln}: decide ({code[j][1]} := ...) forbidden")
                            j += 1
                    else:
                        break
            elif txt == "attribute" and ci + 1 < nc and code[ci + 1][1] == "[":
                j = ci + 2
                while j < nc and code[j][1] != "]":
                    need(code[j][1] not in _FORBIDDEN_ATTR_TOKENS, "LEAN_ATTR_ESCAPE", f"line {ln}: forbidden attr {code[j][1]!r}")
                    j += 1
        elif kind == "SYM":
            if txt == "+" and ci + 1 < nc and code[ci + 1][1] == "native":
                raise VerifierError("LEAN_DECIDE_NATIVE", f"line {ln}: +native option forbidden")
            if txt == "#" and ci + 1 < nc and code[ci + 1][1] in _FORBIDDEN_HASH_CMDS:
                raise VerifierError("LEAN_HASH_ESCAPE", f"line {ln}: forbidden #{code[ci + 1][1]}")
            if txt == "@" and ci + 1 < nc and code[ci + 1][1] == "[":
                j = ci + 2
                while j < nc and code[j][1] != "]":
                    need(code[j][1] not in _FORBIDDEN_ATTR_TOKENS, "LEAN_ATTR_ESCAPE", f"line {ln}: forbidden attr {code[j][1]!r}")
                    j += 1

    need(not (has_var and has_inc), "LEAN_VAR_INC", "variable+include forbidden")

    # Multiline theorem & signature extraction with segment-by-segment namespace/section scope stack
    scopes: list[tuple[str, list[str]]] = []
    thms: list[str] = []
    sigs: dict[str, list[str]] = {}
    pending_private = False
    ci = 0
    while ci < nc:
        _, txt, _ = code[ci]
        if txt == "@" and ci + 1 < nc and code[ci + 1][1] == "[":
            ci += 2
            while ci < nc and code[ci][1] != "]":
                ci += 1
            ci += 1
            continue
        if txt in ("protected", "noncomputable", "scoped", "local"):
            ci += 1
            continue
        if txt == "private":
            pending_private = True
            ci += 1
            continue
        if txt == "namespace" and ci + 1 < nc and code[ci + 1][0] == "IDENT":
            ns_parts = [code[ci + 1][1]]
            ci += 2
            while ci + 1 < nc and code[ci][1] == "." and code[ci + 1][0] == "IDENT":
                ns_parts.append(code[ci + 1][1])
                ci += 2
            for seg in ns_parts:
                scopes.append(("namespace", [seg]))
            pending_private = False
            continue
        if txt == "section":
            if ci + 1 < nc and code[ci + 1][0] == "IDENT" and code[ci + 1][1] not in _TOP_DECL_WORDS:
                sec_parts = [code[ci + 1][1]]
                ci += 2
                while ci + 1 < nc and code[ci][1] == "." and code[ci + 1][0] == "IDENT":
                    sec_parts.append(code[ci + 1][1])
                    ci += 2
                scopes.append(("section", sec_parts))
            else:
                scopes.append(("section", []))
                ci += 1
            pending_private = False
            continue
        if txt == "end":
            if ci + 1 < nc and code[ci + 1][0] == "IDENT" and scopes:
                end_parts = [code[ci + 1][1]]
                j = ci + 2
                while j + 1 < nc and code[j][1] == "." and code[j + 1][0] == "IDENT":
                    end_parts.append(code[j + 1][1])
                    j += 2
                if len(end_parts) <= len(scopes) and [s[1][0] if len(s[1]) == 1 else "" for s in scopes[-len(end_parts):]] == end_parts:
                    del scopes[-len(end_parts):]
                    ci = j
                    pending_private = False
                    continue
                if scopes[-1][1] == end_parts:
                    scopes.pop()
                    ci = j
                    pending_private = False
                    continue
            if scopes:
                scopes.pop()
            pending_private = False
            ci += 1
            continue
        if txt in ("theorem", "lemma") and ci + 1 < nc and code[ci + 1][0] == "IDENT":
            name_parts = [code[ci + 1][1]]
            ci += 2
            while ci + 1 < nc and code[ci][1] == "." and code[ci + 1][0] == "IDENT":
                name_parts.append(code[ci + 1][1])
                ci += 2
            if not pending_private:
                ns_prefix = [p for sk, sp in scopes if sk == "namespace" for p in sp]
                full_name = ".".join((*ns_prefix, *name_parts))
                thms.append(full_name)
                sig_toks: list[str] = []
                j = ci
                depth = 0
                while j < nc:
                    t_txt = code[j][1]
                    if depth == 0 and t_txt == ":=":
                        break
                    if t_txt in ("(", "[", "{"):
                        depth += 1
                    elif t_txt in (")", "]", "}") and depth > 0:
                        depth -= 1
                    sig_toks.append(t_txt)
                    j += 1
                sigs[full_name] = sig_toks
            pending_private = False
            continue
        pending_private = False
        ci += 1
    return thms, sigs


def audit_lean_static_with_sigs(source: str) -> tuple[list[str], dict[str, list[str]]]:
    """Static Lean 4.36.0 audit returning declared public theorem names and normalized signature token maps."""
    return _audit_lean_token_stream(tokenize_lean4(source))


def audit_lean_static(source: str) -> list[str]:
    """Static Lean 4.36.0 audit returning declared public theorem names."""
    thms, _ = audit_lean_static_with_sigs(source)
    return thms


def _theorem_sigs_sha256(sigs: Mapping[str, list[str]]) -> str:
    return _sha256(json.dumps(sigs, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8"))


def _audit_lakefile_toml_strict(lf_text: str) -> None:
    try:
        toml_obj = tomllib.loads(lf_text)
    except tomllib.TOMLDecodeError as exc:
        raise VerifierError("LAKEFILE_TOML", str(exc)) from exc
    for k, v in toml_obj.items():
        need(k in _ALLOWED_TOML_TOP_KEYS, "LAKEFILE_UNSAFE_KEY", f"unsafe lakefile key {k}")
        if k == "name":
            need(type(v) is str and _PKG_NAME_RE.match(v) is not None, "LAKEFILE_BAD_SCHEMA", "invalid lakefile name")
        elif k == "version":
            need(type(v) is str and _VER_RE.match(v) is not None, "LAKEFILE_BAD_SCHEMA", "invalid lakefile version")
        elif k == "defaultTargets":
            need(type(v) is list and v == ["GalacticShadow"], "LAKEFILE_BAD_SCHEMA", "defaultTargets must be ['GalacticShadow']")
        elif k == "lean_lib":
            need(type(v) is list and len(v) == 1, "LAKEFILE_BAD_SCHEMA", "lean_lib must have single GalacticShadow entry")
            for entry in v:
                need(type(entry) is dict, "LAKEFILE_BAD_SCHEMA", "lean_lib item must be dict")
                for lk, lv in entry.items():
                    need(lk in _ALLOWED_TOML_LIB_KEYS, "LAKEFILE_UNSAFE_KEY", f"unsafe lean_lib key {lk}")
                    if lk == "name":
                        need(type(lv) is str and lv == "GalacticShadow", "LAKEFILE_UNSAFE_ROOT", f"bad lean_lib name {lv!r}")
                    elif lk == "srcDir":
                        need(type(lv) is str and len(lv) > 0 and "\x00" not in lv and not lv.startswith(("/", "\\")), "LAKEFILE_UNSAFE_PATH", f"unsafe srcDir {lv!r}")
                        if lv != ".":
                            segs = re.split(r"[/\\]", lv)
                            need(all(s and s != ".." and s not in _SKIP_DIR_SEGS and not s.startswith(".") for s in segs), "LAKEFILE_UNSAFE_PATH", f"unsafe srcDir {lv!r}")
                    elif lk == "roots":
                        need(
                            type(lv) is list and lv == ["GalacticShadow"],
                            "LAKEFILE_UNSAFE_ROOT",
                            f"unsafe roots {lv!r}",
                        )
                    elif lk == "globs":
                        need(
                            type(lv) is list and lv == ["GalacticShadow"],
                            "LAKEFILE_UNSAFE_GLOB",
                            f"unsafe globs {lv!r}",
                        )
    t_stack: list[Any] = [toml_obj]
    while t_stack:
        cur = t_stack.pop()
        if type(cur) is dict:
            t_stack.extend(cur.values())
        elif type(cur) is list:
            t_stack.extend(cur)
        elif type(cur) is str:
            for bad in _UNSAFE_TOML_STRS:
                need(bad not in cur, "LAKEFILE_UNSAFE_STR", f"unsafe lakefile string {cur}")


def _resolve_verified_elf_lean() -> tuple[Path, Path, Path]:
    real_home = Path(pwd.getpwuid(os.getuid()).pw_dir)
    tc_dir_name = EXPECTED_TOOLCHAIN.replace("/", "--").replace(":", "---")
    bin_dir = real_home.joinpath(".elan", "toolchains", tc_dir_name, "bin")
    lean_bin = bin_dir.joinpath("lean")
    lake_bin = bin_dir.joinpath("lake")
    for bp, nm in ((lean_bin, "lean"), (lake_bin, "lake")):
        try:
            st = os.lstat(bp)
        except OSError as exc:
            raise VerifierError("LEAN_EXEC_FAILED", f"{nm} missing at {bp}: {exc}") from exc
        need(stat.S_ISREG(st.st_mode) and bool(st.st_mode & 0o111), "LEAN_TOOL_UNTRUSTED", f"{nm} must be regular executable")
        hdr = read_nofollow_bytes(bp, nm, max_bytes=MAX_BYTES * 64)[:4]
        need(hdr == b"\x7fELF", "LEAN_TOOL_UNTRUSTED", f"{nm} must be native ELF binary")
    return lean_bin, lake_bin, real_home


def _default_lean_runner(args: Sequence[str], cwd: Path, timeout: int) -> tuple[int, bytes, bytes]:
    lean_bin, lake_bin, real_home = _resolve_verified_elf_lean()
    resolved: list[str] = []
    for idx, tok in enumerate(args):
        if idx == 0 and tok == "lean":
            resolved.append(os.fspath(lean_bin))
        elif idx == 0 and tok == "lake":
            resolved.append(os.fspath(lake_bin))
        elif idx == 2 and len(args) >= 3 and args[0] == "lake" and args[1] == "env" and tok == "lean":
            resolved.append(os.fspath(lean_bin))
        else:
            resolved.append(tok)
    clean_env = {
        "PATH": f"{os.fspath(lean_bin.parent)}:/usr/bin:/bin",
        "HOME": os.fspath(real_home),
        "LC_ALL": "C.UTF-8",
        "LANG": "C.UTF-8",
    }
    try:
        proc = subprocess.run(resolved, cwd=str(cwd), env=clean_env, capture_output=True, timeout=timeout, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        raise VerifierError("LEAN_EXEC_FAILED", str(exc)) from exc
    return proc.returncode, proc.stdout, proc.stderr


def verify_lean_bundle(
    track_dir: Path,
    *,
    live_lean: bool = False,
    runner: Callable[[Sequence[str], Path, int], tuple[int, bytes, bytes]] | None = None,
) -> dict[str, Any]:
    """Verify Lean 4.36.0 bundle statically (including theorem signatures & file SHA-256) and via live ELF kernel."""
    need(not os.path.lexists(track_dir.joinpath("lakefile.lean")), "LAKEFILE_LEAN_FORBIDDEN", "executable lakefile.lean forbidden")
    need(not os.path.lexists(track_dir.joinpath(".lake")), "LAKE_RESIDUE", ".lake residue forbidden in track directory")
    with os.scandir(track_dir) as entries:
        for entry in entries:
            if entry.name.endswith(".lean"):
                need(entry.name == "GalacticShadow.lean", "EXTRA_LEAN_FILE_FORBIDDEN", f"unexpected Lean file {entry.name}")
    lean_files = ("GalacticShadow.lean", "lean-toolchain", "lakefile.toml", "lake-manifest.json")
    pinned: dict[str, bytes] = {}
    hashes: dict[str, str] = {}
    for fname in lean_files:
        raw = read_nofollow_bytes(track_dir.joinpath(fname), fname)
        need(b"\r" not in raw, "LEAN_BUNDLE_CR", f"{fname}: CR/CRLF forbidden")
        pinned[fname] = raw
        hashes[fname] = _sha256(raw)

    try:
        tc_text = pinned["lean-toolchain"].decode("utf-8").strip()
        lf_text = pinned["lakefile.toml"].decode("utf-8")
        lean_text = pinned["GalacticShadow.lean"].decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerifierError("LEAN_BUNDLE_UTF8", str(exc)) from exc

    need(tc_text == EXPECTED_TOOLCHAIN, "TOOLCHAIN_BAD", f"expected {EXPECTED_TOOLCHAIN}, got {tc_text}")
    manifest = parse_exact_json(pinned["lake-manifest.json"], "lake-manifest.json")
    need(type(manifest) is dict and manifest.get("packages") == [], "MANIFEST_PKGS", "lake-manifest packages must be []")
    _audit_lakefile_toml_strict(lf_text)

    line_count = len(lean_text.splitlines())
    need(line_count <= MAX_LEAN_LINES, "LEAN_TOO_LONG", f"GalacticShadow.lean {line_count} > {MAX_LEAN_LINES} lines")
    declared, sigs = audit_lean_static_with_sigs(lean_text)
    need(tuple(declared) == EXPECTED_THEOREMS, "THEOREM_LIST_MISMATCH", f"declared theorems mismatch: {declared}")
    sig_sha = _theorem_sigs_sha256(sigs)
    need(sig_sha == PINNED_THEOREM_SIG_SHA256, "THEOREM_SIGNATURE_MISMATCH", f"theorem signature digest mismatch: {sig_sha}")
    need(hashes["GalacticShadow.lean"] == PINNED_LEAN_SHA256, "LEAN_HASH_MISMATCH", f"GalacticShadow.lean SHA-256 mismatch: {hashes['GalacticShadow.lean']}")

    lean_static_status = "STATIC_PASS"
    lean_live_mode = "STATIC_ONLY"
    live_lean_checked = False
    axioms_verified_count = 0
    zero_ax_cnt: int | None = None
    propext_only_cnt: int | None = None
    propext_quot_cnt: int | None = None

    if live_lean:
        exec_fn = _default_lean_runner if runner is None else runner
        with tempfile.TemporaryDirectory(prefix="s174_lean_ver_") as tmp_s:
            tmp_dir = Path(tmp_s)
            os.chmod(tmp_dir, 0o700)
            for fname, raw in pinned.items():
                dst = tmp_dir.joinpath(fname)
                dst.write_bytes(raw)
                os.chmod(dst, 0o644)
            audit_src = "\n".join([
                "import GalacticShadow",
                *EXPECTED_THEOREM_LIVE_TYPE_PINS,
                *(f"#print axioms {t}" for t in EXPECTED_THEOREMS),
                "",
            ])
            audit_p = tmp_dir.joinpath("__AuditS174.lean")
            audit_p.write_bytes(audit_src.encode("utf-8"))
            os.chmod(audit_p, 0o644)

            v_rc, v_out_b, v_err_b = exec_fn(["lean", "--version"], tmp_dir, 60)
            try:
                v_out = v_out_b.decode("utf-8").strip()
                v_err = v_err_b.decode("utf-8").strip()
            except UnicodeDecodeError as exc:
                raise VerifierError("LIVE_LEAN_UTF8", str(exc)) from exc
            need(v_rc == 0 and v_err == "" and EXPECTED_LEAN_VERSION_TOKEN in v_out, "LEAN_VER_BAD", f"unexpected Lean version: {v_out} err={v_err}")

            b_rc, b_out_b, b_err_b = exec_fn(["lake", "build"], tmp_dir, 120)
            try:
                b_out = b_out_b.decode("utf-8")
                b_err = b_err_b.decode("utf-8").strip()
            except UnicodeDecodeError as exc:
                raise VerifierError("LIVE_LEAN_UTF8", str(exc)) from exc
            need(b_rc == 0 and b_err == "", "LAKE_BUILD_BAD", f"lake build rc={b_rc} err={b_err}")
            need(_LEAN_WARN_RE.search(b_out) is None, "LAKE_BUILD_WARNING", f"lake build warning: {b_out.strip()[:200]}")

            a_rc, a_out_b, a_err_b = exec_fn(["lake", "env", "lean", "__AuditS174.lean"], tmp_dir, 120)
            try:
                a_out = a_out_b.decode("utf-8")
                a_err = a_err_b.decode("utf-8").strip()
            except UnicodeDecodeError as exc:
                raise VerifierError("LIVE_LEAN_UTF8", str(exc)) from exc
            need(a_rc == 0 and a_err == "", "AXIOM_EXEC_BAD", f"axiom/type check rc={a_rc} err={a_err}")
            need(_LEAN_WARN_RE.search(a_out) is None, "AXIOM_EXEC_WARNING", f"axiom/type check warning: {a_out.strip()[:200]}")

            seen: dict[str, tuple[str, ...]] = {}
            for line in a_out.splitlines():
                s = line.strip()
                if not s:
                    continue
                m0 = _AXIOM_NONE_RE.match(s)
                if m0 is not None:
                    need(m0.group(1) not in seen, "AXIOM_DUP_THEOREM", f"duplicate axiom report for {m0.group(1)}")
                    seen[m0.group(1)] = ()
                    continue
                m1 = _AXIOM_LIST_RE.match(s)
                need(m1 is not None, "AXIOM_LINE_BAD", f"unparsed axiom line: {s!r}")
                need(m1.group(1) not in seen, "AXIOM_DUP_THEOREM", f"duplicate axiom report for {m1.group(1)}")
                axs = tuple(tok.strip() for tok in m1.group(2).split(",") if tok.strip())
                for ax in axs:
                    need(ax in ALLOWED_AXIOMS, "FORBIDDEN_AXIOM", f"{m1.group(1)} uses disallowed axiom {ax}")
                seen[m1.group(1)] = axs

            need(set(seen.keys()) == set(EXPECTED_THEOREMS), "AXIOM_SET_MISMATCH", "missing or extra theorems in #print axioms")
            actual_zero = {k for k, v in seen.items() if v == ()}
            actual_prop = {k for k, v in seen.items() if v == ("propext",)}
            actual_prop_quot = {k for k, v in seen.items() if len(v) == 2 and set(v) == {"propext", "Quot.sound"}}
            need(actual_zero == EXPECTED_ZERO_AXIOM_THEOREMS, "ZERO_AX_SPLIT_MISMATCH", f"zero-axiom split mismatch: {sorted(actual_zero)}")
            need(actual_prop == EXPECTED_PROPEXT_ONLY_THEOREMS, "PROPEXT_SPLIT_MISMATCH", f"propext split mismatch: {sorted(actual_prop)}")
            need(len(actual_zero) + len(actual_prop) + len(actual_prop_quot) == len(seen), "AXIOM_PARTITION_MISMATCH", "unexpected axiom split")

            lean_live_mode = "LIVE_LEAN_4_36_0_PASS"
            live_lean_checked = True
            axioms_verified_count = len(seen)
            zero_ax_cnt = len(actual_zero)
            propext_only_cnt = len(actual_prop)
            propext_quot_cnt = len(actual_prop_quot)

    return {
        "axioms_verified_count": axioms_verified_count,
        "file_sha256": hashes,
        "lean_line_count": line_count,
        "lean_live_mode": lean_live_mode,
        "lean_module": "GalacticShadow",
        "lean_static_status": lean_static_status,
        "lean_toolchain": EXPECTED_TOOLCHAIN,
        "live_lean_checked": live_lean_checked,
        "pinned_lean_sha256_verified": True,
        "propext_only_theorems": propext_only_cnt,
        "propext_quot_theorems": propext_quot_cnt,
        "public_theorems": len(EXPECTED_THEOREMS),
        "theorem_signatures_sha256": sig_sha,
        "theorem_types_live_checked": live_lean_checked,
        "zero_axiom_theorems": zero_ax_cnt,
    }


# ---------------------------------------------------------------------------
# Exact Pure-Q Crossover-Horizon & Galactic Shadow Oracle (`detect_galactic_shadow`)
# Canonical tower semantics: tower_2(h, x) = 2^(2^(...^(2^x))) with h base-2 layers
# (h=1 => 2^x, h=2 => 2^(2^x), h=3 => 2^(2^(2^x))).
# ---------------------------------------------------------------------------

def validate_horizon_bound(spec: Any, name: str = "n_phys_max") -> dict[str, Any]:
    if type(spec) is int:
        val = require_strict_int(spec, name, min_value=1)
        not_pow2 = (val & (val - 1)) != 0
        return {
            "kind": "exact_int",
            "value_int": val,
            "log2_lower_q": Fraction(val.bit_length() - 1, 1),
            "log2_upper_q": Fraction(val.bit_length(), 1) if not_pow2 else Fraction(val.bit_length() - 1, 1),
            "tower_height": 1,
            "strict_above_lower": not_pow2,
            "strict_below_upper": not_pow2,
        }
    need(isinstance(spec, Mapping), "BAD_HORIZON_SPEC", f"{name} must be exact int or Horizon dict")
    kind = spec.get("kind")
    if kind == "exact_int":
        val = require_strict_int(spec.get("value_int"), f"{name}.value_int", min_value=1)
        return validate_horizon_bound(val, name)
    if kind == "pow2_bound":
        exp_val = require_fraction(spec.get("log2_exp"), f"{name}.log2_exp", non_negative=True)
        tower_h = require_strict_int(spec.get("tower_height", 1), f"{name}.tower_height", min_value=1, max_value=MAX_TOWER_HEIGHT)
        if tower_h == 1 and exp_val.denominator == 1 and exp_val.numerator <= MAX_EXACT_INT_EXP:
            exact_v = 1 << exp_val.numerator
            return {
                "kind": "exact_int",
                "value_int": exact_v,
                "log2_lower_q": exp_val,
                "log2_upper_q": exp_val,
                "tower_height": 1,
                "strict_above_lower": False,
                "strict_below_upper": False,
            }
        return {
            "kind": "pow2_bound",
            "value_int": None,
            "log2_lower_q": exp_val,
            "log2_upper_q": exp_val,
            "tower_height": tower_h,
            "strict_above_lower": False,
            "strict_below_upper": False,
        }
    raise VerifierError("UNKNOWN_HORIZON_KIND", f"{name}.kind unsupported: {kind!r}")


def _cmp_tower_vs_rational(dh: int, y: Fraction, x: Fraction) -> int:
    """Exact comparison of tower_2(dh, y) vs x for dh >= 1, y >= 0, x >= 0. Returns -1, 0, or 1."""
    if x < _ONE:
        return 1
    if x == _ONE:
        return 0 if (dh == 1 and y == _ZERO) else 1
    k = (x.numerator // x.denominator).bit_length() - 1
    x_is_pow2 = (x.denominator == 1) and (x.numerator == (1 << k))
    if dh == 1:
        if y >= Fraction(k + 1, 1):
            return 1
        if y < Fraction(k, 1):
            return -1
        if y == Fraction(k, 1):
            return 0 if x_is_pow2 else -1
        need(
            y.numerator <= MAX_EXACT_INT_EXP
            and y.denominator * max(x.numerator.bit_length(), x.denominator.bit_length()) <= MAX_POWER_WORK_BITS,
            "HORIZON_INCOMPARABLE",
            "fractional tower exponent exceeds exact comparison budget",
        )
        lhs_v = (_ipow(x.denominator, y.denominator)) << y.numerator
        rhs_v = _ipow(x.numerator, y.denominator)
        return 1 if lhs_v > rhs_v else -1
    c_hi = _cmp_tower_vs_rational(dh - 1, y, Fraction(k + 1, 1))
    if c_hi >= 0:
        return 1
    c_lo = _cmp_tower_vs_rational(dh - 1, y, Fraction(k, 1))
    if c_lo < 0:
        return -1
    if c_lo == 0:
        return 0 if x_is_pow2 else -1
    raise VerifierError("HORIZON_INCOMPARABLE", "multi-height non-integer tower boundary cannot be ordered")


def _cmp_horizon_endpoint(h1: int, x1: Fraction, h2: int, x2: Fraction) -> int:
    if h1 == h2:
        return 1 if x1 > x2 else (-1 if x1 < x2 else 0)
    if h1 > h2:
        return _cmp_tower_vs_rational(h1 - h2, x1, x2)
    return -_cmp_tower_vs_rational(h2 - h1, x2, x1)


def compare_horizon_gt(lhs: dict[str, Any], rhs: dict[str, Any]) -> bool:
    """Exact multi-height horizon comparison (fail-closed HORIZON_INCOMPARABLE on overlapping intervals)."""
    if lhs["value_int"] is not None and rhs["value_int"] is not None:
        return lhs["value_int"] > rhs["value_int"]
    h1, h2 = lhs["tower_height"], rhs["tower_height"]
    s1_lo = bool(lhs.get("strict_above_lower", False))
    s2_hi = bool(rhs.get("strict_below_upper", False))
    c_lo_hi = _cmp_horizon_endpoint(h1, lhs["log2_lower_q"], h2, rhs["log2_upper_q"])
    if c_lo_hi > 0 or (c_lo_hi == 0 and (s1_lo or s2_hi)):
        return True
    c_hi_lo = _cmp_horizon_endpoint(h1, lhs["log2_upper_q"], h2, rhs["log2_lower_q"])
    if c_hi_lo <= 0:
        return False
    raise VerifierError("HORIZON_INCOMPARABLE", "overlapping horizon bounds cannot be ordered without exact refinement")


def validate_cost_spec(spec: Any, name: str) -> dict[str, Any]:
    need(isinstance(spec, Mapping), "BAD_COST_SPEC", f"{name} must be a mapping")
    kind = spec.get("kind")
    need(isinstance(kind, str) and kind in _VALID_COST_KINDS, "BAD_COST_KIND", f"{name}.kind={kind!r} invalid")
    if kind == "power":
        coeff = require_fraction(spec.get("coeff"), f"{name}.coeff", positive=True)
        exp_q = require_fraction(spec.get("exponent"), f"{name}.exponent", non_negative=True)
        need(exp_q.denominator <= MAX_EXP_DENOM and exp_q <= Fraction(MAX_EXP_VALUE, 1), "EXP_OUT_OF_RANGE", f"{name}.exponent out of exact bounds")
        return {"kind": "power", "coeff": coeff, "exponent": exp_q}
    if kind == "polylog_dyadic":
        coeff = require_fraction(spec.get("coeff"), f"{name}.coeff", positive=True)
        n_exp = require_fraction(spec.get("n_exponent", 1), f"{name}.n_exponent", non_negative=True)
        log_exp = require_fraction(spec.get("log_exponent"), f"{name}.log_exponent", non_negative=True)
        need(
            n_exp.denominator <= MAX_POLYLOG_EXP_DENOM
            and log_exp.denominator <= MAX_POLYLOG_EXP_DENOM
            and n_exp <= Fraction(MAX_EXP_VALUE, 1)
            and log_exp <= Fraction(MAX_EXP_VALUE, 1),
            "EXP_OUT_OF_RANGE",
            f"{name} polylog exponents out of exact bounds",
        )
        log_offset = require_strict_int(spec.get("log_offset", 0), f"{name}.log_offset", min_value=0, max_value=MAX_LOG_OFFSET)
        return {"kind": "polylog_dyadic", "coeff": coeff, "n_exponent": n_exp, "log_exponent": log_exp, "log_offset": log_offset}
    if kind == "affine_linear":
        fixed = require_fraction(spec.get("fixed", 0), f"{name}.fixed", non_negative=True)
        slope = require_fraction(spec.get("slope"), f"{name}.slope", positive=True)
        quad = require_fraction(spec.get("quad", 0), f"{name}.quad", non_negative=True)
        return {"kind": "affine_linear", "fixed": fixed, "slope": slope, "quad": quad}
    min_log2_exp = require_fraction(spec.get("valid_from_log2_exp"), f"{name}.valid_from_log2_exp", positive=True)
    tower_h = require_strict_int(spec.get("tower_height", 1), f"{name}.tower_height", min_value=1, max_value=MAX_TOWER_HEIGHT)
    asymp_order = require_strict_int(spec.get("asymp_rank", 1), f"{name}.asymp_rank", min_value=1)
    return {"kind": "tower_cutoff", "valid_from_log2_exp": min_log2_exp, "tower_height": tower_h, "asymp_rank": asymp_order}


def _eval_power_ratio_lt(c_a: Fraction, exp_a: Fraction, c_b: Fraction, exp_b: Fraction, n: int) -> bool:
    delta = exp_b - exp_a
    if delta == _ZERO:
        return c_a < c_b
    coeff_bits = max(c_a.numerator.bit_length(), c_a.denominator.bit_length(), c_b.numerator.bit_length(), c_b.denominator.bit_length())
    if delta < _ZERO:
        neg_delta = -delta
        p, q = neg_delta.numerator, neg_delta.denominator
        need(q * coeff_bits <= MAX_POWER_WORK_BITS and p * n.bit_length() <= MAX_POWER_WORK_BITS, "POWER_EXPONENT_LIMIT", "power comparison exceeds bit budget")
        return (_ipow(c_a.numerator, q)) * (_ipow(c_b.denominator, q)) * (_ipow(n, p)) < (_ipow(c_b.numerator, q)) * (_ipow(c_a.denominator, q))
    p, q = delta.numerator, delta.denominator
    need(q * coeff_bits <= MAX_POWER_WORK_BITS and p * n.bit_length() <= MAX_POWER_WORK_BITS, "POWER_EXPONENT_LIMIT", "power comparison exceeds bit budget")
    return (_ipow(c_a.numerator, q)) * (_ipow(c_b.denominator, q)) < (_ipow(c_b.numerator, q)) * (_ipow(c_a.denominator, q)) * (_ipow(n, p))


def _resolve_power_horizon_gt_exact(spec_a: dict[str, Any], spec_b: dict[str, Any], phys: dict[str, Any]) -> bool:
    """Resolve overlapping power-crossover intervals directly from exact cleared-denominator inequality."""
    c_a, exp_a = spec_a["coeff"], spec_a["exponent"]
    c_b, exp_b = spec_b["coeff"], spec_b["exponent"]
    if phys["value_int"] is not None:
        return not _eval_power_ratio_lt(c_a, exp_a, c_b, exp_b, phys["value_int"])
    if (
        phys["tower_height"] == 1
        and phys["log2_lower_q"] == phys["log2_upper_q"]
        and not phys.get("strict_above_lower", False)
        and not phys.get("strict_below_upper", False)
    ):
        # HIGH-1 (Delta-2): physical problem sizes are INTEGERS N <= 2^(k_n/k_d), i.e. N <= F := floor(2^(k_n/k_d))
        # (exact integer k_d-th root). With R = c_a/c_b and delta = p/q, N* = floor(R^(q/p)) + 1, hence
        # N* > F  <=>  R^(q/p) >= F  <=>  r_n^q >= r_d^q * F^p (exact for fractional k_d > 1 as well as k_d == 1).
        delta = exp_b - exp_a
        ratio = qdiv(c_a, c_b)
        p, q = delta.numerator, delta.denominator
        k_q = phys["log2_lower_q"]
        k_n, k_d = k_q.numerator, k_q.denominator
        r_n, r_d = ratio.numerator, ratio.denominator
        need(
            q * max(r_n.bit_length(), r_d.bit_length()) <= MAX_POWER_WORK_BITS
            and k_n <= MAX_POWER_WORK_BITS
            and k_d <= MAX_POWER_WORK_BITS
            and p * (k_n // k_d + 1) <= MAX_POWER_WORK_BITS,
            "HORIZON_INCOMPARABLE",
            "power vs pow2_bound refinement exceeds bit budget",
        )
        f_int = _iroot_floor(1 << k_n, k_d)
        return _ipow(r_n, q) >= _ipow(r_d, q) * _ipow(f_int, p)
    raise VerifierError("HORIZON_INCOMPARABLE", "power horizon overlap cannot be refined")


def _solve_power_crossover(c_a: Fraction, exp_a: Fraction, c_b: Fraction, exp_b: Fraction) -> dict[str, Any]:
    delta = exp_b - exp_a
    ratio = qdiv(c_a, c_b)
    if ratio < _ONE:
        return validate_horizon_bound(1, "n_star")
    if ratio == _ONE:
        return validate_horizon_bound(2, "n_star")

    p, q = delta.numerator, delta.denominator
    r_n, r_d = ratio.numerator, ratio.denominator
    is_pow2_ratio = (r_d == 1) and ((r_n & (r_n - 1)) == 0)
    if is_pow2_ratio:
        k_bits = r_n.bit_length() - 1
        exact_log2 = Fraction(q * k_bits, p)
        if exact_log2.denominator == 1 and exact_log2.numerator > MAX_EXACT_INT_EXP:
            return {
                "kind": "pow2_bound",
                "value_int": None,
                "log2_lower_q": exact_log2,
                "log2_upper_q": exact_log2 + Fraction(1, 1024),
                "tower_height": 1,
                "strict_above_lower": True,
                "strict_below_upper": True,
            }

    if r_n.bit_length() <= 512 and r_d.bit_length() <= 512:
        scaled_floor = ((r_n ** 16) // (r_d ** 16)).bit_length() - 1
        log2_ratio_lb = Fraction(scaled_floor, 16)
        log2_ratio_ub = Fraction(scaled_floor + 1, 16)
    else:
        log2_ratio_lb = Fraction(max(0, (r_n // r_d).bit_length() - 1), 1)
        log2_ratio_ub = Fraction(r_n.bit_length() - r_d.bit_length() + 1, 1)
    est_exp_ub = Fraction(q, p) * log2_ratio_ub
    if est_exp_ub > Fraction(MAX_EXACT_INT_EXP, 1):
        return {
            "kind": "pow2_bound",
            "value_int": None,
            "log2_lower_q": Fraction(q, p) * log2_ratio_lb,
            "log2_upper_q": est_exp_ub,
            "tower_height": 1,
            "strict_above_lower": True,
            "strict_below_upper": False,
        }

    need(q * max(r_n.bit_length(), r_d.bit_length()) <= MAX_POWER_WORK_BITS, "POWER_EXPONENT_LIMIT", "exact power crossover exceeds bit budget")
    lhs_coeff = _ipow(r_d, q)
    rhs_const = _ipow(r_n, q)
    hi = 2
    while lhs_coeff * (_ipow(hi, p)) <= rhs_const:
        hi *= 2
    lo = hi // 2
    while lo < hi:
        mid = (lo + hi) // 2
        if lhs_coeff * (_ipow(mid, p)) > rhs_const:
            hi = mid
        else:
            lo = mid + 1
    return validate_horizon_bound(lo, "n_star")


def _eval_polylog_dyadic_lt(spec_a: dict[str, Any], spec_b: dict[str, Any], m: int) -> bool:
    """Exact comparison at N = 2^m across general n_exponent and log_exponent."""
    val_a_base = m + spec_a["log_offset"]
    val_b_base = m + spec_b["log_offset"]
    need(val_a_base >= 1 and val_b_base >= 1, "POLYLOG_DOMAIN", "log term must be >= 1")
    delta_n = spec_b["n_exponent"] - spec_a["n_exponent"]
    ba, bb = spec_a["log_exponent"], spec_b["log_exponent"]
    ca, cb = spec_a["coeff"], spec_b["coeff"]
    d_all = delta_n.denominator * ba.denominator * bb.denominator
    p_ba = ba.numerator * delta_n.denominator * bb.denominator
    p_bb = bb.numerator * delta_n.denominator * ba.denominator
    need(
        d_all <= MAX_POLYLOG_SHIFT_BITS and p_ba <= MAX_POLYLOG_SHIFT_BITS and p_bb <= MAX_POLYLOG_SHIFT_BITS,
        "POLYLOG_EXPONENT_LIMIT",
        "polylog cleared exponent exceeds exact budget",
    )
    lhs_base = (_ipow(ca.numerator, d_all)) * (_ipow(cb.denominator, d_all)) * (_ipow(val_a_base, p_ba))
    rhs_base = (_ipow(cb.numerator, d_all)) * (_ipow(ca.denominator, d_all)) * (_ipow(val_b_base, p_bb))
    if delta_n == _ZERO:
        return lhs_base < rhs_base
    p_n = delta_n.numerator * ba.denominator * bb.denominator
    need(m * p_n <= MAX_POLYLOG_SHIFT_BITS, "POLYLOG_EXPONENT_LIMIT", "polylog shift exceeds exact bit budget")
    return lhs_base < rhs_base * (1 << (m * p_n))


def _solve_polylog_dyadic_crossover(spec_a: dict[str, Any], spec_b: dict[str, Any]) -> tuple[bool, dict[str, Any] | None]:
    """Exact global eventual-dominance horizon m* = min{M >= 1 : forall m >= M, A(2^m) < B(2^m)}."""
    na, nb = spec_a["n_exponent"], spec_b["n_exponent"]
    ba, bb = spec_a["log_exponent"], spec_b["log_exponent"]
    ca, cb = spec_a["coeff"], spec_b["coeff"]
    oa, ob = spec_a["log_offset"], spec_b["log_offset"]

    if na > nb:
        return False, None
    if na == nb and ba > bb:
        return False, None
    if na == nb and ba == bb:
        if ca > cb or (ca == cb and (ba == _ZERO or oa >= ob)):
            return False, None
        if oa <= ob:
            return True, validate_horizon_bound({"kind": "pow2_bound", "log2_exp": Fraction(1, 1), "tower_height": 1}, "n_star")
        # ca < cb and oa > ob: ((m + oa) / (m + ob))^ba is strictly decreasing in m -> binary search
        hi = 1
        while not _eval_polylog_dyadic_lt(spec_a, spec_b, hi):
            hi *= 2
            need(hi <= MAX_POLYLOG_M, "POLYLOG_EXPONENT_LIMIT", "polylog crossover m* exceeds search bound")
        lo = 1 if hi == 1 else hi // 2
        while lo < hi:
            mid = (lo + hi) // 2
            if _eval_polylog_dyadic_lt(spec_a, spec_b, mid):
                hi = mid
            else:
                lo = mid + 1
        return True, validate_horizon_bound({"kind": "pow2_bound", "log2_exp": Fraction(lo, 1), "tower_height": 1}, "n_star")

    if na == nb:
        # delta_n == 0, delta_b = bb - ba > 0: f'(m) = 0 at unique peak m_peak = (ba*ob - bb*oa)/(bb - ba).
        # f(m) increases for m < m_peak and strictly decreases for m > m_peak, so max on Z>=1 is at {m0, m0+1}.
        m_peak_q = qdiv(ba * ob - bb * oa, bb - ba)
        m0 = max(1, m_peak_q.numerator // m_peak_q.denominator)
        lt0 = _eval_polylog_dyadic_lt(spec_a, spec_b, m0)
        lt1 = _eval_polylog_dyadic_lt(spec_a, spec_b, m0 + 1)
        if lt0 and lt1:
            return True, validate_horizon_bound({"kind": "pow2_bound", "log2_exp": Fraction(1, 1), "tower_height": 1}, "n_star")
        start_m = m0 + 1 if not lt1 else m0
        hi = start_m
        while not _eval_polylog_dyadic_lt(spec_a, spec_b, hi):
            hi *= 2
            need(hi <= MAX_POLYLOG_M, "POLYLOG_EXPONENT_LIMIT", "polylog crossover m* exceeds search bound")
        lo = hi // 2
        while lo < hi:
            mid = (lo + hi) // 2
            if _eval_polylog_dyadic_lt(spec_a, spec_b, mid):
                hi = mid
            else:
                lo = mid + 1
        return True, validate_horizon_bound({"kind": "pow2_bound", "log2_exp": Fraction(lo, 1), "tower_height": 1}, "n_star")

    # delta_n > 0: since ln(2) > 693/1000, f'(m) < 0 strictly for all m >= m_mono.
    # LOW-3 (Delta-2): for ob <= oa, bb/(m+ob) >= bb/(m+oa), so f'(m) <= (ba - bb)/(m+oa) - delta_n*ln2; the
    # cancelling exponent ba_eff = ba - bb (<= 0 => strictly decreasing everywhere, m_mono = 1) avoids spurious limits.
    delta_n = nb - na
    ba_eff = (ba - bb) if ob <= oa else ba
    m_mono = max(1, (1000 * ba_eff.numerator * delta_n.denominator) // (693 * ba_eff.denominator * delta_n.numerator) + 1 - oa)
    if not _eval_polylog_dyadic_lt(spec_a, spec_b, m_mono):
        hi = m_mono
        while not _eval_polylog_dyadic_lt(spec_a, spec_b, hi):
            hi *= 2
        lo = hi // 2
        while lo < hi:
            mid = (lo + hi) // 2
            if _eval_polylog_dyadic_lt(spec_a, spec_b, mid):
                hi = mid
            else:
                lo = mid + 1
        m_star = lo
    else:
        m_star = 1
        for m in range(m_mono - 1, 0, -1):
            if not _eval_polylog_dyadic_lt(spec_a, spec_b, m):
                m_star = m + 1
                break
    return True, validate_horizon_bound({"kind": "pow2_bound", "log2_exp": Fraction(m_star, 1), "tower_height": 1}, "n_star")


def _eval_affine_q(spec: dict[str, Any], n: int) -> Fraction:
    return spec["fixed"] + spec["slope"] * n + spec["quad"] * (n * n)


def _solve_affine_crossover(spec_a: dict[str, Any], spec_b: dict[str, Any]) -> tuple[bool, dict[str, Any] | None]:
    """Exact tail crossover N* = min{N0 >= 1 : forall N >= N0, A(N) < B(N)} for affine/quadratic specs."""
    qa, qb = spec_a["quad"], spec_b["quad"]
    sa, sb = spec_a["slope"], spec_b["slope"]
    fa, fb = spec_a["fixed"], spec_b["fixed"]

    if qa > qb or (qa == qb and sa > sb):
        return False, None
    if qa == qb and sa == sb:
        if fa < fb:
            return True, validate_horizon_bound(1, "n_star")
        return False, None

    # For quadratic advantage (qb > qa), D(N) = B(N) - A(N) is strictly convex with global integer minimum
    # at {n0, n0+1} where n0 = max(1, floor((sa - sb) / (2 * (qb - qa)))).
    start_n = 1
    if qb > qa and sa > sb:
        v_q = qdiv(sa - sb, 2 * (qb - qa))
        n0 = max(1, v_q.numerator // v_q.denominator)
        lt0 = _eval_affine_q(spec_a, n0) < _eval_affine_q(spec_b, n0)
        lt1 = _eval_affine_q(spec_a, n0 + 1) < _eval_affine_q(spec_b, n0 + 1)
        if lt0 and lt1:
            return True, validate_horizon_bound(1, "n_star")
        start_n = n0 + 1 if not lt1 else n0

    hi = start_n
    while _eval_affine_q(spec_a, hi) >= _eval_affine_q(spec_b, hi):
        hi *= 2
    lo = start_n if hi == start_n else hi // 2
    while lo < hi:
        mid = (lo + hi) // 2
        if _eval_affine_q(spec_a, mid) < _eval_affine_q(spec_b, mid):
            hi = mid
        else:
            lo = mid + 1
    return True, validate_horizon_bound(lo, "n_star")


def _serialize_horizon(h: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": h["kind"],
        "value_int_str": str(h["value_int"]) if h["value_int"] is not None else None,
        "log2_lower_q": fmt_q(h["log2_lower_q"]),
        "log2_upper_q": fmt_q(h["log2_upper_q"]),
        "tower_height": h["tower_height"],
        "strict_above_lower": bool(h.get("strict_above_lower", False)),
        "strict_below_upper": bool(h.get("strict_below_upper", False)),
    }


def detect_galactic_shadow(cost_asymp: Any, cost_practical: Any, n_phys_max: Any) -> dict[str, Any]:
    """Executable pure-Q Galactic-Shadow detector (CS-Galactic dual to CS-09)."""
    spec_a = validate_cost_spec(cost_asymp, "cost_asymp")
    spec_b = validate_cost_spec(cost_practical, "cost_practical")
    phys = validate_horizon_bound(n_phys_max, "n_phys_max")
    kind_a, kind_b = spec_a["kind"], spec_b["kind"]

    n_star: dict[str, Any] | None = None
    asymptotic_dominant = False
    dom_ratio_q: str | None = None

    if kind_a == "tower_cutoff":
        need(kind_b in ("power", "polylog_dyadic", "tower_cutoff"), "TOWER_INCOMPATIBLE", "tower_cutoff requires compatible practical baseline")
        practical_rank = spec_b["asymp_rank"] if kind_b == "tower_cutoff" else 2
        if spec_a["asymp_rank"] < practical_rank:
            asymptotic_dominant = True
            n_star = validate_horizon_bound(
                {"kind": "pow2_bound", "log2_exp": spec_a["valid_from_log2_exp"], "tower_height": spec_a["tower_height"]},
                "n_star",
            )
    elif kind_a == "power" and kind_b == "power":
        exp_a, exp_b = spec_a["exponent"], spec_b["exponent"]
        if exp_a > exp_b or (exp_a == exp_b and spec_a["coeff"] >= spec_b["coeff"]):
            asymptotic_dominant = False
        else:
            asymptotic_dominant = True
            n_star = _solve_power_crossover(spec_a["coeff"], exp_a, spec_b["coeff"], exp_b)
            if phys["value_int"] is not None and exp_a.denominator == 1 and exp_b.denominator == 1:
                n_v = phys["value_int"]
                dom_ratio_q = fmt_q(qdiv(spec_a["coeff"] * (_ipow(n_v, exp_a.numerator)), spec_b["coeff"] * (_ipow(n_v, exp_b.numerator))))
    elif kind_a == "polylog_dyadic" and kind_b == "polylog_dyadic":
        asymptotic_dominant, n_star = _solve_polylog_dyadic_crossover(spec_a, spec_b)
        if phys["value_int"] is not None and (phys["value_int"] & (phys["value_int"] - 1)) == 0:
            m_v = phys["value_int"].bit_length() - 1
            if m_v >= 1 and spec_a["n_exponent"] == spec_b["n_exponent"]:
                ba, bb = spec_a["log_exponent"], spec_b["log_exponent"]
                if ba.denominator == 1 and bb.denominator == 1:
                    num = spec_a["coeff"] * (_ipow(m_v + spec_a["log_offset"], ba.numerator))
                    den = spec_b["coeff"] * (_ipow(m_v + spec_b["log_offset"], bb.numerator))
                    dom_ratio_q = fmt_q(qdiv(num, den))
                elif ba == Fraction(1, 2) and bb.denominator == 1:
                    rt = _exact_isqrt_if_square(m_v + spec_a["log_offset"])
                    if rt is not None:
                        num = spec_a["coeff"] * rt
                        den = spec_b["coeff"] * (_ipow(m_v + spec_b["log_offset"], bb.numerator))
                        dom_ratio_q = fmt_q(qdiv(num, den))
    elif kind_a == "affine_linear" and kind_b == "affine_linear":
        asymptotic_dominant, n_star = _solve_affine_crossover(spec_a, spec_b)
        if phys["value_int"] is not None:
            n_v = phys["value_int"]
            dom_ratio_q = fmt_q(qdiv(_eval_affine_q(spec_a, n_v), _eval_affine_q(spec_b, n_v)))
    else:
        raise VerifierError("INCOMPATIBLE_COST_MODELS", f"cannot compare {kind_a!r} vs {kind_b!r}")

    if not asymptotic_dominant:
        return {
            "status": "NO_ASYMPTOTIC_ADVANTAGE",
            "shadow_detected": False,
            "asymptotic_dominant": False,
            "n_star": None,
            "n_phys_max": _serialize_horizon(phys),
            "dominance_ratio_at_n_phys_q": dom_ratio_q,
        }

    try:
        shadow = compare_horizon_gt(n_star, phys)  # type: ignore[arg-type]
    except VerifierError as exc:
        if exc.code == "HORIZON_INCOMPARABLE" and kind_a == "power" and kind_b == "power":
            shadow = _resolve_power_horizon_gt_exact(spec_a, spec_b, phys)
        else:
            raise
    return {
        "status": "GALACTIC_SHADOW" if shadow else "TERRESTRIAL_CROSSOVER",
        "shadow_detected": shadow,
        "asymptotic_dominant": True,
        "n_star": _serialize_horizon(n_star),  # type: ignore[arg-type]
        "n_phys_max": _serialize_horizon(phys),
        "dominance_ratio_at_n_phys_q": dom_ratio_q,
    }


def build_real_algorithm_portfolio() -> list[dict[str, Any]]:
    """15 real algorithm pairs: Lipton Portal 209 + EXP-Q28c + Portal 220 sssp-lean + S161/S164/S166/SiliQuant/HoloSphere-V4."""
    universe_pow2 = {"kind": "pow2_bound", "log2_exp": "266", "tower_height": 1}
    sm86_vram_bits = 8 * (1 << 30) * 8
    sm86_gemm_max_dim = 37837
    return [
        {
            "pair_id": "williams_23727_vs_stothers_23737_halving",
            "source": "Lipton 2011 (matrix-breakthrough-2011)",
            "expected_status": "GALACTIC_SHADOW",
            "cost_asymp": {"kind": "power", "coeff": "2", "exponent": "23727/10000"},
            "cost_practical": {"kind": "power", "coeff": "1", "exponent": "23737/10000"},
            "n_phys_max": universe_pow2,
        },
        {
            "pair_id": "pass_omega_9_4_vs_strassen_q28c",
            "source": "EXP-Q28c / Portal 140 (lukehutch/matmul-9-ov-4)",
            "expected_status": "GALACTIC_SHADOW",
            "cost_asymp": {"kind": "tower_cutoff", "valid_from_log2_exp": "6906285000000000000000", "tower_height": 1, "asymp_rank": 1},
            "cost_practical": {"kind": "power", "coeff": "1", "exponent": "2808/1000"},
            "n_phys_max": universe_pow2,
        },
        {
            "pair_id": "strassen_hybrid_vs_cubed_gemm_sm86",
            "source": "Lipton comment-7566 (D'Alberto-Nicolau GotoBLAS crossover)",
            "expected_status": "TERRESTRIAL_CROSSOVER",
            "cost_asymp": {"kind": "power", "coeff": "4", "exponent": "2808/1000"},
            "cost_practical": {"kind": "power", "coeff": "1", "exponent": "3"},
            "n_phys_max": sm86_gemm_max_dim,
        },
        {
            "pair_id": "dickson_10x_cw_vs_cubed_gemm_8gib",
            "source": "Lipton comment-7566 (Dickson 10x crossover)",
            "expected_status": "GALACTIC_SHADOW",
            "cost_asymp": {"kind": "power", "coeff": "10", "exponent": "2808/1000"},
            "cost_practical": {"kind": "power", "coeff": "1", "exponent": "3"},
            "n_phys_max": sm86_gemm_max_dim,
        },
        {
            "pair_id": "harvey_vanderhoeven_nlogn_vs_schonhage_strassen",
            "source": "Lipton 2019 (integer-mult-nlogn-2019)",
            "expected_status": "GALACTIC_SHADOW",
            "cost_asymp": {"kind": "tower_cutoff", "valid_from_log2_exp": str(1729 ** 12), "tower_height": 1, "asymp_rank": 1},
            "cost_practical": {"kind": "power", "coeff": "1", "exponent": "2"},
            "n_phys_max": sm86_vram_bits,
        },
        {
            "pair_id": "karatsuba_vs_schoolbook_limbs",
            "source": "GMP limb multiplication (L1 32 KiB = 4096 64-bit limbs; power N*=38)",
            "expected_status": "TERRESTRIAL_CROSSOVER",
            "cost_asymp": {"kind": "power", "coeff": "9", "exponent": "1585/1000"},
            "cost_practical": {"kind": "power", "coeff": "2", "exponent": "2"},
            "n_phys_max": 4096,
        },
        {
            "pair_id": "aks_sorting_network_vs_batcher_bitonic",
            "source": "Knuth 1998 / Lipton 2014 (galactic-sorting-2014)",
            "expected_status": "GALACTIC_SHADOW",
            "cost_asymp": {"kind": "polylog_dyadic", "coeff": "39/2", "n_exponent": "1", "log_exponent": "1", "log_offset": 0},
            "cost_practical": {"kind": "polylog_dyadic", "coeff": "1/4", "n_exponent": "1", "log_exponent": "2", "log_offset": 0},
            "n_phys_max": 1 << 31,
        },
        {
            "pair_id": "aks_primality_vs_aprcl_deterministic",
            "source": "Lipton 2011 / Primality (b > 2^(2^64) bit-length)",
            "expected_status": "GALACTIC_SHADOW",
            "cost_asymp": {"kind": "tower_cutoff", "valid_from_log2_exp": "64", "tower_height": 2, "asymp_rank": 1},
            "cost_practical": {"kind": "power", "coeff": "1", "exponent": "6"},
            "n_phys_max": sm86_vram_bits,
        },
        {
            "pair_id": "aks_primality_vs_miller_rabin_nondominance",
            "source": "Primality R5 non-dominance control (AKS b^6 vs 40*b^3)",
            "expected_status": "NO_ASYMPTOTIC_ADVANTAGE",
            "cost_asymp": {"kind": "power", "coeff": "1", "exponent": "6"},
            "cost_practical": {"kind": "power", "coeff": "40", "exponent": "3"},
            "n_phys_max": 16384,
        },
        {
            "pair_id": "finite_fourier_vs_fwht_256",
            "source": "Track S164 (FiniteFourier C=3 vs FWHT_256)",
            "expected_status": "GALACTIC_SHADOW",
            "cost_asymp": {"kind": "polylog_dyadic", "coeff": "3", "n_exponent": "1", "log_exponent": "1/2", "log_offset": 1},
            "cost_practical": {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "1", "log_offset": 0},
            "n_phys_max": 256,
        },
        {
            "pair_id": "siliquant_voronoi_asymptotic_vs_a16_lop3_popc",
            "source": "SiliKernels (A_16 LOP3+POPC vs hampack reuse crossover)",
            "expected_status": "GALACTIC_SHADOW",
            "cost_asymp": {"kind": "affine_linear", "fixed": "1000000", "slope": "17/4", "quad": "0"},
            "cost_practical": {"kind": "affine_linear", "fixed": "0", "slope": "9/2", "quad": "0"},
            "n_phys_max": 49152,
        },
        {
            "pair_id": "holosphere_v4_cayley_su2_sfast_vs_dense_kv",
            "source": "Track S159 / S164 / S171 (S_fast 65,536 B vs FP16 KV 12,288 B/tok)",
            "expected_status": "TERRESTRIAL_CROSSOVER",
            "cost_asymp": {"kind": "affine_linear", "fixed": "65536", "slope": "1", "quad": "0"},
            "cost_practical": {"kind": "affine_linear", "fixed": "0", "slope": "12288", "quad": "0"},
            "n_phys_max": 8192,
        },
        {
            "pair_id": "holosphere_high_overhead_rf_vs_dense_attention",
            "source": "Linear random-feature attention C=2^20 vs dense T^2",
            "expected_status": "GALACTIC_SHADOW",
            "cost_asymp": {"kind": "affine_linear", "fixed": "0", "slope": str(1 << 20), "quad": "0"},
            "cost_practical": {"kind": "affine_linear", "fixed": "0", "slope": "1", "quad": "1"},
            "n_phys_max": 131072,
        },
        {
            "pair_id": "cs29_ephemeral_worker_vs_inline_coordinator",
            "source": "Track S166 / SOP-20 (W=19200, s=256 vs B=4096)",
            "expected_status": "TERRESTRIAL_CROSSOVER",
            "cost_asymp": {"kind": "affine_linear", "fixed": "19200", "slope": "256", "quad": "0"},
            "cost_practical": {"kind": "affine_linear", "fixed": "0", "slope": "4096", "quad": "0"},
            "n_phys_max": 40,
        },
        {
            "pair_id": "igholami_sssp_lean_vs_dijkstra_cutoff",
            "source": "Portal 220 / arXiv:2611.34911v1 (igholami/sssp-lean Alg. 8: N <= L_N^64; dyadic N = 2^m crossover m* = 590 (N = 2^590); exact integer crossover N* = 590^64 + 1 > 2^266)",
            "expected_status": "GALACTIC_SHADOW",
            "cost_asymp": {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "0", "log_exponent": "64", "log_offset": 1},
            "cost_practical": {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "0", "log_offset": 0},
            "n_phys_max": universe_pow2,
        },
    ]


# ---------------------------------------------------------------------------
# Pure-Q Matrix Operators (OP-02 ⧅, OP-01 ⧄, OP-08 ⫩) & Live aletheia.calculus Parity
# ---------------------------------------------------------------------------

def _qsubmat(m: Sequence[Sequence[Fraction]], rows: Sequence[int], cols: Sequence[int]) -> list[list[Fraction]]:
    return [[m[i][j] for j in cols] for i in rows]


def _qmul(a: Sequence[Sequence[Fraction]], b: Sequence[Sequence[Fraction]]) -> list[list[Fraction]]:
    rows, inner = len(a), len(b)
    cols = len(b[0]) if b and b[0] else 0
    return [[sum((a[i][k] * b[k][j] for k in range(inner)), _ZERO) for j in range(cols)] for i in range(rows)]


def _qtranspose(a: Sequence[Sequence[Fraction]]) -> list[list[Fraction]]:
    if not a:
        return []
    return [[a[i][j] for i in range(len(a))] for j in range(len(a[0]))]


def _qnullspace(a: Sequence[Sequence[Fraction]]) -> list[list[Fraction]]:
    if not a:
        return []
    m_rows, n_cols = len(a), len(a[0])
    mat = [list(r) for r in a]
    pivots: list[int] = []
    r = 0
    for c in range(n_cols):
        if r >= m_rows:
            break
        piv = -1
        for i in range(r, m_rows):
            if mat[i][c] != _ZERO:
                piv = i
                break
        if piv < 0:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        inv = qdiv(_ONE, mat[r][c])
        mat[r] = [v * inv for v in mat[r]]
        for i in range(m_rows):
            if i != r and mat[i][c] != _ZERO:
                f = mat[i][c]
                mat[i] = [mat[i][j] - f * mat[r][j] for j in range(n_cols)]
        pivots.append(c)
        r += 1
    piv_set = set(pivots)
    basis: list[list[Fraction]] = []
    for free_c in range(n_cols):
        if free_c in piv_set:
            continue
        vec = [_ZERO for _ in range(n_cols)]
        vec[free_c] = _ONE
        for row_idx, piv_c in enumerate(pivots):
            vec[piv_c] = -mat[row_idx][free_c]
        basis.append(vec)
    return basis


def _qrank(a: Sequence[Sequence[Fraction]]) -> int:
    if not a or not a[0]:
        return 0
    return len(a[0]) - len(_qnullspace(a))


def _qinv_sym(a: Sequence[Sequence[Fraction]]) -> list[list[Fraction]]:
    n = len(a)
    aug = [list(a[i]) + [_ONE if i == j else _ZERO for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = -1
        for row in range(col, n):
            if aug[row][col] != _ZERO:
                piv = row
                break
        need(piv >= 0, "SINGULAR_SUBMATRIX", "matrix is singular")
        aug[col], aug[piv] = aug[piv], aug[col]
        inv = qdiv(_ONE, aug[col][col])
        aug[col] = [v * inv for v in aug[col]]
        for row in range(n):
            if row != col and aug[row][col] != _ZERO:
                f = aug[row][col]
                aug[row] = [aug[row][j] - f * aug[col][j] for j in range(2 * n)]
    return [row[n:] for row in aug]


def _qpinv_sym(a: Sequence[Sequence[Fraction]]) -> list[list[Fraction]]:
    n = len(a)
    if n == 0:
        return []
    null_b = _qnullspace(a)
    r = n - len(null_b)
    if r == 0:
        return [[_ZERO for _ in range(n)] for _ in range(n)]
    if r == n:
        return _qinv_sym(a)
    mat = [list(row) for row in a]
    pivots: list[int] = []
    row_i = 0
    for c in range(n):
        if row_i >= n:
            break
        piv = -1
        for i in range(row_i, n):
            if mat[i][c] != _ZERO:
                piv = i
                break
        if piv < 0:
            continue
        mat[row_i], mat[piv] = mat[piv], mat[row_i]
        inv = qdiv(_ONE, mat[row_i][c])
        mat[row_i] = [v * inv for v in mat[row_i]]
        for i in range(n):
            if i != row_i and mat[i][c] != _ZERO:
                f = mat[i][c]
                mat[i] = [mat[i][j] - f * mat[row_i][j] for j in range(n)]
        pivots.append(c)
        row_i += 1
    b_cols = _qsubmat(a, list(range(n)), pivots)
    bt_b = _qmul(_qtranspose(b_cols), b_cols)
    inv_btb = _qinv_sym(bt_b)
    u_mat = b_cols
    v_mat = _qmul(inv_btb, _qmul(_qtranspose(u_mat), a))
    v_vt_inv = _qinv_sym(_qmul(v_mat, _qtranspose(v_mat)))
    return _qmul(_qtranspose(v_mat), _qmul(v_vt_inv, _qmul(inv_btb, _qtranspose(u_mat))))


def dark_mode_shadow_and_schur_exact(
    m_rows: Sequence[Sequence[Fraction]],
    elim_indices: Sequence[int],
) -> dict[str, Any]:
    """Self-contained exact OP-02 (⧅) and OP-01 (⧄) over Q."""
    n = len(m_rows)
    need(n >= 2, "SMALL_MATRIX", "matrix must be at least 2x2")
    for row in m_rows:
        need(len(row) == n, "NON_SQUARE_MATRIX", "matrix must be square")
    for i in range(n):
        for j in range(i + 1, n):
            need(m_rows[i][j] == m_rows[j][i], "SHADOW_NOT_SYM", "matrix must be symmetric")
    b_set = set(elim_indices)
    need(len(b_set) == len(elim_indices) and 1 <= len(b_set) < n, "BAD_ELIM_SET", "invalid elimination indices")
    for idx in elim_indices:
        need(0 <= idx < n, "SHADOW_OOB", "elimination index out of bounds")
    a_idx = [i for i in range(n) if i not in b_set]
    b_idx = list(elim_indices)
    m_aa = _qsubmat(m_rows, a_idx, a_idx)
    m_ab = _qsubmat(m_rows, a_idx, b_idx)
    m_ba = _qsubmat(m_rows, b_idx, a_idx)
    m_bb = _qsubmat(m_rows, b_idx, b_idx)
    k_b = _qnullspace(m_bb)
    dim_dark = len(k_b)
    if dim_dark > 0:
        c_ab = _qmul(m_ab, _qtranspose(k_b))
        r_cross = _qrank(c_ab)
    else:
        c_ab = []
        r_cross = 0
    m_bb_pinv = _qpinv_sym(m_bb)
    corr = _qmul(m_ab, _qmul(m_bb_pinv, m_ba))
    schur = [[m_aa[i][j] - corr[i][j] for j in range(len(a_idx))] for i in range(len(a_idx))]
    return {
        "dim_dark": dim_dark,
        "r_cross": r_cross,
        "kernel_basis_q": [[fmt_q(v) for v in vec] for vec in k_b],
        "coupling_map_q": [[fmt_q(v) for v in row] for row in c_ab],
        "schur_q": [[fmt_q(v) for v in row] for row in schur],
    }


def op_r5_gate_exact(predicate: Callable[[Any], bool], target: Any, mutants: Sequence[Any]) -> dict[str, Any]:
    """Self-contained exact OP-08 (⫩): T ⫩ x iff T(x) is True AND forall m in M, T(m) is False."""
    need(len(mutants) > 0, "EMPTY_MUTANTS", "R5 gate requires non-empty mutant family")
    accept_ok = bool(predicate(target))
    killed = sum(1 for m in mutants if not bool(predicate(m)))
    total = len(mutants)
    return {
        "passed": accept_ok and (killed == total),
        "accept_target": accept_ok,
        "killed": killed,
        "total_mutants": total,
        "kill_ratio_q": fmt_q(Fraction(killed, total)),
    }


def verify_aletheia_calculus_parity(aletheia_root: Path | None) -> dict[str, Any]:
    """Verify OP-02 (⧅), OP-01 (⧄), and OP-08 (⫩) locally and optionally against live aletheia.calculus."""
    m_pi_inf = [
        [Fraction(4, 1), Fraction(1, 1), Fraction(-1, 1)],
        [Fraction(1, 1), Fraction(2, 1), Fraction(2, 1)],
        [Fraction(-1, 1), Fraction(2, 1), Fraction(2, 1)],
    ]
    sh_pi = dark_mode_shadow_and_schur_exact(m_pi_inf, (1, 2))
    m_full = [[Fraction(5, 1), Fraction(2, 1)], [Fraction(2, 1), Fraction(2, 1)]]
    sh_full = dark_mode_shadow_and_schur_exact(m_full, (1,))

    pred = lambda pair: pair[0] <= pair[1]
    r5_pass = op_r5_gate_exact(pred, (6, 8192), [(8193, 8192), (1024, 256)])
    r5_leak = op_r5_gate_exact(pred, (6, 8192), [(8193, 8192), (8, 8192)])
    need(
        sh_pi["dim_dark"] == 1
        and sh_pi["r_cross"] == 1
        and sh_pi["kernel_basis_q"] == [["-1/1", "1/1"]]
        and sh_pi["coupling_map_q"] == [["-2/1"]]
        and sh_pi["schur_q"] == [["4/1"]],
        "SELF_SHADOW_MISMATCH",
        "self shadow check failed",
    )
    need(
        sh_full["dim_dark"] == 0
        and sh_full["r_cross"] == 0
        and sh_full["kernel_basis_q"] == []
        and sh_full["coupling_map_q"] == []
        and sh_full["schur_q"] == [["3/1"]],
        "SELF_SCHUR_MISMATCH",
        "self full-rank shadow check failed",
    )
    need(r5_pass["passed"] is True and r5_pass["kill_ratio_q"] == "1/1", "SELF_R5_PASS_BAD", "self R5 pass check failed")
    need(r5_leak["passed"] is False and r5_leak["kill_ratio_q"] == "1/2", "SELF_R5_LEAK_BAD", "self R5 leak check failed")

    if aletheia_root is None:
        return {
            "mode": "SELF_CONTAINED_EXACT",
            "live_checked": False,
            "operators_checked": ["⧅", "⧄", "⫩"],
            "dark_mode_dim_dark": sh_pi["dim_dark"],
            "dark_mode_r_cross": sh_pi["r_cross"],
            "r5_gate_parity": True,
        }

    root_p = aletheia_root
    need(root_p.is_dir(), "ALETHEIA_ROOT_MISSING", f"aletheia root missing: {root_p}")
    calc_path = root_p.joinpath("aletheia", "calculus.py")
    _ = read_nofollow_bytes(calc_path, "aletheia/calculus.py")
    root_s = os.fspath(root_p)
    inserted = False
    if root_s not in sys.path:
        sys.path.insert(0, root_s)
        inserted = True
    try:
        try:
            cal_pkg = importlib.import_module("aletheia.calculus")
        except Exception as exc:
            raise VerifierError("ALETHEIA_IMPORT_FAIL", f"cannot import aletheia.calculus: {exc}") from exc

        # ⧅ and ⧄ full live parity (dim_dark, r_cross, kernel_basis, coupling_map, full Schur matrix)
        m_cal = cal_pkg.qmat([[4, 1, -1], [1, 2, 2], [-1, 2, 2]])
        e_cal = cal_pkg.IndexSet((1, 2))
        live_sh = cal_pkg.op_dark_mode_shadow(m_cal, e_cal)
        live_sc = cal_pkg.op_schur_pushforward(m_cal, e_cal)
        live_kb_q = [[fmt_q(v) for v in vec] for vec in live_sh.kernel_basis]
        live_cm_q = [[fmt_q(v) for v in row] for row in live_sh.coupling_map] if live_sh.coupling_map is not None else []
        live_sc_q = [[fmt_q(v) for v in row] for row in live_sc]
        need(
            live_sh.dim_dark == sh_pi["dim_dark"]
            and live_sh.r_cross == sh_pi["r_cross"]
            and live_kb_q == sh_pi["kernel_basis_q"]
            and live_cm_q == sh_pi["coupling_map_q"]
            and live_sc_q == sh_pi["schur_q"],
            "ALETHEIA_SHADOW_PARITY_FAIL",
            "live aletheia.calculus ⧅ / ⧄ parity mismatch on Pi_inf",
        )
        m_cal_full = cal_pkg.qmat([[5, 2], [2, 2]])
        e_full = cal_pkg.IndexSet((1,))
        live_sh_f = cal_pkg.op_dark_mode_shadow(m_cal_full, e_full)
        live_sc_f = cal_pkg.op_schur_pushforward(m_cal_full, e_full)
        live_sc_f_q = [[fmt_q(v) for v in row] for row in live_sc_f]
        need(
            live_sh_f.dim_dark == sh_full["dim_dark"]
            and live_sh_f.r_cross == sh_full["r_cross"]
            and len(live_sh_f.kernel_basis) == 0
            and live_sh_f.coupling_map is None
            and live_sc_f_q == sh_full["schur_q"],
            "ALETHEIA_SCHUR_PARITY_FAIL",
            "live aletheia.calculus ⧅ / ⧄ parity mismatch on full-rank",
        )

        # ⫩ live parity on passing and leaking R5Spec
        live_r5_pass = cal_pkg.op_r5_gate(cal_pkg.R5Spec(predicate=pred, mutants=((8193, 8192), (1024, 256))), (6, 8192))
        live_r5_leak = cal_pkg.op_r5_gate(cal_pkg.R5Spec(predicate=pred, mutants=((8193, 8192), (8, 8192))), (6, 8192))
        need(
            live_r5_pass.passed is r5_pass["passed"]
            and fmt_q(live_r5_pass.kill_ratio) == r5_pass["kill_ratio_q"]
            and live_r5_leak.passed is r5_leak["passed"]
            and fmt_q(live_r5_leak.kill_ratio) == r5_leak["kill_ratio_q"],
            "ALETHEIA_R5_PARITY_FAIL",
            "live aletheia.calculus ⫩ parity mismatch",
        )
    finally:
        if inserted and root_s in sys.path:
            sys.path.remove(root_s)

    return {
        "mode": "LIVE_ALETHEIA_CALCULUS_PASS",
        "live_checked": True,
        "operators_checked": ["⧅", "⧄", "⫩"],
        "dark_mode_dim_dark": sh_pi["dim_dark"],
        "dark_mode_r_cross": sh_pi["r_cross"],
        "r5_gate_parity": True,
    }


# ---------------------------------------------------------------------------
# Lipton-DeMillo-Sayward (1978) Pure-AST Evaluator (ZERO exec / eval / compile)
# ---------------------------------------------------------------------------

_GATE_KERNEL_SRC = """
def gate_kernel(delta_num, delta_den, ca_num, ca_den, cb_num, cb_den, n_star, n_phys_max):
    if type(n_phys_max) is bool:
        return "REJECT_BOOL"
    if n_phys_max <= 0:
        return "REJECT_NONPOS"
    if delta_den <= 0:
        return "REJECT_BAD_DEN"
    if delta_num < 0:
        return "NO_ASYMPTOTIC_ADVANTAGE"
    if delta_num == 0 and ca_num * cb_den >= cb_num * ca_den:
        return "NO_ASYMPTOTIC_ADVANTAGE"
    if n_star > n_phys_max:
        return "GALACTIC_SHADOW"
    return "TERRESTRIAL_CROSSOVER"
""".strip()

_MASK_KERNEL_SRC = """
def mask_kernel(n_star, n_phys_max):
    gap = n_star - n_phys_max
    if gap > 0:
        return "GALACTIC_SHADOW"
    return "TERRESTRIAL_CROSSOVER"
""".strip()

_CMP_ALT: dict[type[ast.cmpop], type[ast.cmpop]] = {
    ast.LtE: ast.Lt,
    ast.Lt: ast.LtE,
    ast.GtE: ast.Gt,
    ast.Gt: ast.GtE,
    ast.Eq: ast.NotEq,
    ast.NotEq: ast.Eq,
}


def _discover_lds_sites(tree: ast.AST) -> list[dict[str, Any]]:
    sites: list[dict[str, Any]] = []
    for idx, node in enumerate(ast.walk(tree)):
        if isinstance(node, ast.If):
            sites.append({"site_idx": idx, "kind": "guard_false", "lineno": node.lineno})
            if isinstance(node.test, ast.Compare):
                for op_i, op in enumerate(node.test.ops):
                    if type(op) in _CMP_ALT:
                        sites.append({"site_idx": idx, "kind": "cmp_flip", "op_i": op_i, "lineno": node.lineno})
            elif isinstance(node.test, ast.BoolOp):
                for val_i, val in enumerate(node.test.values):
                    if isinstance(val, ast.Compare):
                        for op_i, op in enumerate(val.ops):
                            if type(op) in _CMP_ALT:
                                sites.append({"site_idx": idx, "kind": "bool_cmp_flip", "val_i": val_i, "op_i": op_i, "lineno": node.lineno})
    return sites


def _apply_lds_site(tree: ast.AST, site: Mapping[str, Any]) -> None:
    target_idx = site["site_idx"]
    for idx, node in enumerate(ast.walk(tree)):
        if idx == target_idx and isinstance(node, ast.If):
            if site["kind"] == "guard_false":
                node.test = ast.Constant(value=False)
            elif site["kind"] == "cmp_flip" and isinstance(node.test, ast.Compare):
                op_i = site["op_i"]
                node.test.ops[op_i] = _CMP_ALT[type(node.test.ops[op_i])]()
            elif site["kind"] == "bool_cmp_flip" and isinstance(node.test, ast.BoolOp):
                sub = node.test.values[site["val_i"]]
                if isinstance(sub, ast.Compare):
                    op_i = site["op_i"]
                    sub.ops[op_i] = _CMP_ALT[type(sub.ops[op_i])]()
            return


def _eval_ast_expr(expr: ast.expr, env: Mapping[str, Any]) -> Any:
    if isinstance(expr, ast.Constant):
        return expr.value
    if isinstance(expr, ast.Name):
        if expr.id == "bool":
            return bool
        return env[expr.id]
    if isinstance(expr, ast.BinOp) and isinstance(expr.op, ast.Mult):
        return _eval_ast_expr(expr.left, env) * _eval_ast_expr(expr.right, env)
    if isinstance(expr, ast.BinOp) and isinstance(expr.op, ast.Sub):
        return _eval_ast_expr(expr.left, env) - _eval_ast_expr(expr.right, env)
    if isinstance(expr, ast.Call) and isinstance(expr.func, ast.Name) and expr.func.id == "type":
        return type(_eval_ast_expr(expr.args[0], env))
    if isinstance(expr, ast.BoolOp):
        if isinstance(expr.op, ast.And):
            return all(_eval_ast_expr(v, env) for v in expr.values)
        return any(_eval_ast_expr(v, env) for v in expr.values)
    if isinstance(expr, ast.Compare):
        left = _eval_ast_expr(expr.left, env)
        for op, comp in zip(expr.ops, expr.comparators):
            right = _eval_ast_expr(comp, env)
            if isinstance(op, ast.Is):
                ok = left is right
            elif isinstance(op, ast.LtE):
                ok = left <= right
            elif isinstance(op, ast.Lt):
                ok = left < right
            elif isinstance(op, ast.GtE):
                ok = left >= right
            elif isinstance(op, ast.Gt):
                ok = left > right
            elif isinstance(op, ast.Eq):
                ok = left == right
            elif isinstance(op, ast.NotEq):
                ok = left != right
            else:
                raise VerifierError("LDS_AST_UNSUPPORTED", f"unsupported cmpop {type(op).__name__}")
            if not ok:
                return False
            left = right
        return True
    raise VerifierError("LDS_AST_UNSUPPORTED", f"unsupported AST expr {type(expr).__name__}")


def _eval_gate_kernel_ast(fn_def: ast.FunctionDef, args: tuple[Any, ...]) -> Any:
    env: dict[str, Any] = {arg.arg: val for arg, val in zip(fn_def.args.args, args)}
    for stmt in fn_def.body:
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
            env[stmt.targets[0].id] = _eval_ast_expr(stmt.value, env)
        elif isinstance(stmt, ast.If):
            # LOW-4 (Delta-2): fail closed on any If shape other than `if <test>: return <expr>` (no elif/else).
            need(
                len(stmt.body) == 1 and isinstance(stmt.body[0], ast.Return) and stmt.body[0].value is not None and not stmt.orelse,
                "LDS_AST_UNSUPPORTED",
                "unsupported If statement shape in gate kernel",
            )
            if _eval_ast_expr(stmt.test, env):
                return _eval_ast_expr(stmt.body[0].value, env)
        elif isinstance(stmt, ast.Return) and stmt.value is not None:
            return _eval_ast_expr(stmt.value, env)
        else:
            raise VerifierError("LDS_AST_UNSUPPORTED", f"unsupported statement {type(stmt).__name__} in gate kernel")
    return None


def _lds_apply_sub_swap(t: ast.Module) -> None:
    """M1(A): swap the operands of `gap = n_star - n_phys_max` (fail closed if the AST shape drifts)."""
    fn = t.body[0] if t.body else None
    need(
        isinstance(fn, ast.FunctionDef)
        and len(fn.body) >= 2
        and isinstance(fn.body[0], ast.Assign)
        and isinstance(fn.body[0].value, ast.BinOp)
        and isinstance(fn.body[0].value.op, ast.Sub),
        "LDS_AST_UNSUPPORTED",
        "sub_swap target shape mismatch",
    )
    fn.body[0].value.left, fn.body[0].value.right = fn.body[0].value.right, fn.body[0].value.left


def _lds_apply_cmp_neg(t: ast.Module) -> None:
    """M1(B): flip `gap > 0` to `gap <= 0` (fail closed if the AST shape drifts)."""
    fn = t.body[0] if t.body else None
    need(
        isinstance(fn, ast.FunctionDef)
        and len(fn.body) >= 2
        and isinstance(fn.body[1], ast.If)
        and isinstance(fn.body[1].test, ast.Compare)
        and len(fn.body[1].test.ops) == 1
        and isinstance(fn.body[1].test.ops[0], ast.Gt),
        "LDS_AST_UNSUPPORTED",
        "cmp_neg target shape mismatch",
    )
    fn.body[1].test.ops[0] = ast.LtE()


def _verify_m2_pairwise_masking_witness() -> dict[str, Any]:
    """True 2nd-order pairwise fault-masking witness (pure AST): M1(A) & M1(B) each killed on non-boundary, M2(A+B) masks until boundary."""
    base = ast.parse(_MASK_KERNEL_SRC)
    non_boundary = [((99, 100), "TERRESTRIAL_CROSSOVER"), ((101, 100), "GALACTIC_SHADOW")]
    with_boundary = non_boundary + [((100, 100), "TERRESTRIAL_CROSSOVER")]

    def _passes(t: ast.Module, vecs: Sequence[tuple[tuple[int, int], str]]) -> bool:
        fn = t.body[0]
        return isinstance(fn, ast.FunctionDef) and all(_eval_gate_kernel_ast(fn, a) == exp for a, exp in vecs)

    m_a = copy.deepcopy(base)
    _lds_apply_sub_swap(m_a)
    m_b = copy.deepcopy(base)
    _lds_apply_cmp_neg(m_b)
    m_ab = copy.deepcopy(base)
    _lds_apply_sub_swap(m_ab)
    _lds_apply_cmp_neg(m_ab)

    m1_a_killed_nb = not _passes(m_a, non_boundary)
    m1_b_killed_nb = not _passes(m_b, non_boundary)
    m2_ab_survives_nb = _passes(m_ab, non_boundary)
    m2_ab_killed_with_b = not _passes(m_ab, with_boundary)
    return {
        "m1_sub_swap_killed_without_boundary": m1_a_killed_nb,
        "m1_cmp_neg_killed_without_boundary": m1_b_killed_nb,
        "m2_pairwise_masking_survives_without_boundary": m2_ab_survives_nb,
        "m2_pairwise_masking_killed_with_boundary": m2_ab_killed_with_b,
    }


def run_lipton_demillo_sayward_coupling(gate_src: str = _GATE_KERNEL_SRC) -> dict[str, Any]:
    """Verify M_1 1st-order & M_2 2nd-order mutation coupling plus true 2nd-order pairwise masking witness."""
    base_tree = ast.parse(gate_src)
    sites = _discover_lds_sites(base_tree)
    vectors: list[tuple[tuple[Any, ...], str]] = [
        ((1, 1, 2, 1, 1, 1, 100, True), "REJECT_BOOL"),
        ((1, 1, 2, 1, 1, 1, 100, 0), "REJECT_NONPOS"),
        ((1, 1, 2, 1, 1, 1, 100, -1), "REJECT_NONPOS"),
        ((1, 0, 2, 1, 1, 1, 100, 100), "REJECT_BAD_DEN"),
        ((-1, 1, 1, 1, 2, 1, 1, 100), "NO_ASYMPTOTIC_ADVANTAGE"),
        ((0, 1, 2, 1, 2, 1, 1, 100), "NO_ASYMPTOTIC_ADVANTAGE"),
        ((0, 1, 3, 1, 2, 1, 1, 100), "NO_ASYMPTOTIC_ADVANTAGE"),
        ((0, 1, 1, 1, 2, 1, 1, 100), "TERRESTRIAL_CROSSOVER"),
        ((1, 1, 2, 1, 1, 1, 100, 100), "TERRESTRIAL_CROSSOVER"),
        ((1, 1, 2, 1, 1, 1, 101, 100), "GALACTIC_SHADOW"),
    ]

    def _eval_tree(tree_obj: ast.Module) -> bool:
        fn_def = tree_obj.body[0]
        if not isinstance(fn_def, ast.FunctionDef):
            return False
        for args, expected in vectors:
            if _eval_gate_kernel_ast(fn_def, args) != expected:
                return False
        return True

    need(_eval_tree(copy.deepcopy(base_tree)), "LDS_BASELINE_FAIL", "gate_kernel baseline failed R5 vectors")

    m1_killed = 0
    for s in sites:
        mut = copy.deepcopy(base_tree)
        _apply_lds_site(mut, s)
        if not _eval_tree(mut):
            m1_killed += 1

    m2_total = 0
    m2_killed = 0
    survivor_pairs: list[dict[str, Any]] = []
    for i in range(len(sites)):
        for j in range(i + 1, len(sites)):
            if sites[i]["site_idx"] == sites[j]["site_idx"] and (
                sites[i]["kind"] == "guard_false" or sites[j]["kind"] == "guard_false"
            ):
                continue
            m2_total += 1
            mut2 = copy.deepcopy(base_tree)
            _apply_lds_site(mut2, sites[i])
            _apply_lds_site(mut2, sites[j])
            if not _eval_tree(mut2):
                m2_killed += 1
            else:
                survivor_pairs.append({"site_a": sites[i], "site_b": sites[j]})

    m2_mask = _verify_m2_pairwise_masking_witness()
    m1_rate = Fraction(m1_killed, len(sites))
    m2_rate = Fraction(m2_killed, m2_total)
    return {
        "m1_total": len(sites),
        "m1_killed": m1_killed,
        "m1_kill_rate_q": fmt_q(m1_rate),
        "m2_total": m2_total,
        "m2_killed": m2_killed,
        "m2_coupling_rate_q": fmt_q(m2_rate),
        "m2_survivors": survivor_pairs,
        "m2_pairwise_masking_witness": m2_mask,
    }


# ---------------------------------------------------------------------------
# Full Stage-2 Certificate Assembly & Verification (`R1–R7`)
# ---------------------------------------------------------------------------

def _verify_karatsuba_recurrence_exact(
    max_n: int = 8192,
    *,
    tk_override: Callable[[int], int] | None = None,
) -> dict[str, Any]:
    memo: dict[int, int] = {1: 2}

    def _tk(n: int) -> int:
        if tk_override is not None:
            return tk_override(n)
        if n in memo:
            return memo[n]
        v = 3 * _tk((n + 1) // 2) + 4 * n
        memo[n] = v
        return v

    fails_256 = [n for n in range(1, 257) if _tk(n) >= 2 * n * n]
    fails_all = [n for n in range(1, max_n + 1) if _tk(n) >= 2 * n * n]
    stage1_n_star = (max(fails_256) + 1) if fails_256 else 1
    global_n_star = (max(fails_all) + 1) if fails_all else 1
    need(stage1_n_star == 165, "KAR_STAGE1_BAD", f"expected stage1 illusion 165, got {stage1_n_star}")
    need(global_n_star == 280, "KAR_GLOBAL_BAD", f"expected global N*=280, got {global_n_star}")
    re_cross = [n for n in range(257, 280) if _tk(n) >= 2 * n * n]
    need(re_cross == list(range(257, 280)), "KAR_RECROSS_BAD", f"expected all 23 integers in [257, 279] to re-cross, got {len(re_cross)}")
    return {
        "stage1_truncated_window_256_n_star": stage1_n_star,
        "re_crossing_interval": [re_cross[0], re_cross[-1]],
        "re_crossing_count": len(re_cross),
        "global_n_star": global_n_star,
        "verified_up_to": max_n,
        "tk_at_256": _tk(256),
        "tk_at_257": _tk(257),
        "tk_at_279": _tk(279),
        "tk_at_280": _tk(280),
    }


def _verify_s161_dominance(
    q_values: Sequence[int] = tuple(range(2, 28)),
    *,
    ag4_fn: Callable[[int], int] | None = None,
) -> None:
    for q in q_values:
        ag4 = (2 * (q ** 4 + q ** 2)) if ag4_fn is None else ag4_fn(q)
        pg5 = 2 * (sum(_ipow(q, k) for k in range(6)) + q ** 3)
        need(ag4 < pg5, "S161_DOM_FAIL", f"AG(4,{q}) not < PG(5,{q})")


def _verify_mux_cs09_witness(
    u_bf16: Fraction = Fraction(1, 256),
    *,
    e3_half_override: Fraction | None = None,
    e4_half_override: Fraction | None = None,
) -> tuple[Fraction, Fraction, Fraction, Fraction, bool]:
    e3_half = Fraction(9, 2 * (10 ** 3 - 9 ** 3)) if e3_half_override is None else e3_half_override
    eta3 = qdiv(3 * u_bf16, _ONE - 2 * u_bf16)
    e4_half = Fraction(19, 2 * (10 ** 4 - 9 ** 4)) if e4_half_override is None else e4_half_override
    eta4 = qdiv(4 * u_bf16, _ONE - 3 * u_bf16)
    need(eta3 < e3_half and eta4 > e4_half, "MUX_CS09_FAIL", "MUX BF16 S=3/S=4 witness failed")
    # LOW-1 (Delta-2): Al-Kashi u = 0 gives eta_S(0) = 0, so passing reduces to margin positivity 9^S < 10^S;
    # Python checks the finite window S in [1, 16]; the universal claim for all S >= 1 is Lean Theorem 6.
    alkashi_ok = all(_ipow(9, s) < _ipow(10, s) and _ZERO < Fraction(1, 2 * (_ipow(10, s) - _ipow(9, s))) for s in range(1, 17))
    return eta3, e3_half, eta4, e4_half, alkashi_ok


def _verify_cs09_galactic_duality_witness(
    *,
    scale_pairs: Sequence[tuple[int, int]] = ((3, 4), (8, 10), (25, 222), (256, 1024), (1 << 266, 590 ** 64)),
) -> bool:
    """Verify exact u = 1/N order-reversal duality (a < b <-> 1/b < 1/a) across CS-09 & CS-Galactic pairs."""
    need(len(scale_pairs) > 0, "CS09_DUAL_FAIL", "duality witness requires non-empty scale pairs")
    for lo_n, hi_n in scale_pairs:
        u_ok = (
            lo_n > 0
            and hi_n > 0
            and lo_n < hi_n
            and Fraction(1, hi_n) < Fraction(1, lo_n)
            and qdiv(_ONE, Fraction(1, hi_n)) == Fraction(hi_n, 1)
            and qdiv(_ONE, Fraction(1, lo_n)) == Fraction(lo_n, 1)
        )
        need(u_ok, "CS09_DUAL_FAIL", f"reciprocal inversion duality failed for ({lo_n}, {hi_n})")
    return True


def _verify_portal_220_sssp_lean_witness(
    *,
    base: int = 590,
    exp: int = 64,
    univ_bits: int = 266,
) -> dict[str, Any]:
    """Pure-Z verification of Portal 220 (arXiv:2611.34911v1 / igholami/sssp-lean) cutoff 590^64 > 2^266.

    MED-1 (Delta-2): with L_N = ceil(log2(N + 2)) = (N + 1).bit_length(), the exact INTEGER crossover of
    N > L_N^64 is N* = 590^64 + 1 (L = 590 on [2^589 - 1, 2^590 - 2] and N = 590^64 <= L^64 fails), while
    N = 2^590 is only the DYADIC (N = 2^m) crossover m* = 590. Universality for all N >= 590^64 + 1:
    L = 590 gives N > 590^64; L >= 591 gives N >= 2^(L-1) - 1 > L^64 by induction from 591^64 + 1 < 2^590
    and (L + 1)^64 <= 2 * L^64 (ratio decreasing in L, checked at L = 591).
    """
    cut_590_64 = _ipow(base, exp)
    cut_591_64 = _ipow(base + 1, exp)
    cut_592_64 = _ipow(base + 2, exp)
    univ_266 = 1 << univ_bits
    p589 = 1 << 589
    p590 = 1 << 590
    need(cut_590_64 > univ_266 and p589 < cut_590_64 < p590 and cut_591_64 < p590, "SSSP_P220_FAIL", "Portal 220 590^64 cutoff witness failed")
    n_int_star = cut_590_64 + 1
    l_at_cut = (cut_590_64 + 1).bit_length()
    l_at_star = (n_int_star + 1).bit_length()
    need(
        l_at_cut == base
        and cut_590_64 <= _ipow(l_at_cut, exp)
        and l_at_star == base
        and n_int_star > _ipow(l_at_star, exp)
        and cut_591_64 + 1 < p590
        and cut_592_64 <= 2 * cut_591_64,
        "SSSP_P220_INT_FAIL",
        "Portal 220 exact integer crossover 590^64 + 1 witness failed",
    )
    return {
        "source": "arXiv:2611.34911v1 / igholami/sssp-lean (Alg. 8: N <= L_N^64, L_N = ceil(log2(N + 2)))",
        "cutoff_590_pow_64_str": str(cut_590_64),
        "cutoff_bit_length": cut_590_64.bit_length(),
        "exceeds_universe_2_pow_266": True,
        "dyadic_crossover_m_star": 590,
        "dyadic_crossover_n_label": "2^590 (N = 2^m dyadic grid only)",
        "dyadic_bracket_589_590_exact": True,
        "integer_crossover_n_star_str": str(n_int_star),
        "integer_crossover_n_star_label": "590^64 + 1",
        "integer_crossover_bit_length": n_int_star.bit_length(),
        "integer_crossover_universal_induction_exact": True,
    }


def _verify_exp_q60a_portfolio_and_duality(aletheia_root: Path | None) -> dict[str, Any]:
    kar_info = _verify_karatsuba_recurrence_exact(8192)

    ff_crossovers: list[dict[str, Any]] = []
    for c_ff in (3, 4):
        m_star = 1
        while (m_star * m_star) <= (c_ff * c_ff) * (1 + m_star):
            m_star += 1
        ff_crossovers.append({
            "c_ff": c_ff,
            "m_star": m_star,
            "n_star": 1 << m_star,
            "cleared_lhs_at_m_star": m_star * m_star,
            "cleared_rhs_at_m_star": (c_ff * c_ff) * (1 + m_star),
            "exceeds_byte_width_256": (1 << m_star) > 256,
        })

    _verify_s161_dominance()
    s161_ag4_25_sym = 2 * (25 ** 4 + 25 ** 2)
    s161_ag4_25_pconn = 2 * (25 ** 4) + 496 + 497 - 1
    s161_pg5_27 = 2 * (sum(_ipow(27, k) for k in range(6)) + 27 ** 3)
    s161_ratio = Fraction(s161_pg5_27, s161_ag4_25_pconn)

    eta3, e3_half, eta4, e4_half, alkashi_ok = _verify_mux_cs09_witness()
    p220_witness = _verify_portal_220_sssp_lean_witness()

    m_pi_inf = [
        [Fraction(4, 1), Fraction(1, 1), Fraction(-1, 1)],
        [Fraction(1, 1), Fraction(2, 1), Fraction(2, 1)],
        [Fraction(-1, 1), Fraction(2, 1), Fraction(2, 1)],
    ]
    shadow_pi_inf = dark_mode_shadow_and_schur_exact(m_pi_inf, (1, 2))
    parity_info = verify_aletheia_calculus_parity(aletheia_root)

    duality_verified = _verify_cs09_galactic_duality_witness()

    portfolio = build_real_algorithm_portfolio()
    portfolio_rows: list[dict[str, Any]] = []
    for entry in portfolio:
        res = detect_galactic_shadow(entry["cost_asymp"], entry["cost_practical"], entry["n_phys_max"])
        matched = res["status"] == entry["expected_status"]
        need(matched, "PORTFOLIO_MISMATCH", f"{entry['pair_id']} expected {entry['expected_status']}, got {res['status']}")
        portfolio_rows.append({
            "pair_id": entry["pair_id"],
            "source": entry["source"],
            "expected_status": entry["expected_status"],
            "observed_status": res["status"],
            "matched": True,
            "shadow_detected": res["shadow_detected"],
            "n_star": res["n_star"],
            "n_phys_max": res["n_phys_max"],
            "dominance_ratio_at_n_phys_q": res["dominance_ratio_at_n_phys_q"],
        })

    return {
        "portfolio_total": len(portfolio_rows),
        "portfolio_matched": len(portfolio_rows),
        "galactic_shadow_count": sum(1 for r in portfolio_rows if r["observed_status"] == "GALACTIC_SHADOW"),
        "terrestrial_crossover_count": sum(1 for r in portfolio_rows if r["observed_status"] == "TERRESTRIAL_CROSSOVER"),
        "no_advantage_count": sum(1 for r in portfolio_rows if r["observed_status"] == "NO_ASYMPTOTIC_ADVANTAGE"),
        "portfolio_results": portfolio_rows,
        "karatsuba_exact_recurrence": kar_info,
        "finite_fourier_vs_fwht256": ff_crossovers,
        "s161_ag4_25_sym": s161_ag4_25_sym,
        "s161_ag4_25_pconn": s161_ag4_25_pconn,
        "s161_pg5_27": s161_pg5_27,
        "s161_cross_scale_pg5_27_over_ag4_25_q": fmt_q(s161_ratio),
        "mux_cs09_witness": {
            "s3_eta_q": fmt_q(eta3),
            "s3_half_margin_q": fmt_q(e3_half),
            "s3_passes": True,
            "s4_eta_q": fmt_q(eta4),
            "s4_half_margin_q": fmt_q(e4_half),
            "s4_collapses": True,
            "alkashi_u0_passes_checked_s_1_to_16": alkashi_ok,
            "alkashi_u0_all_s_ge_1_lean_theorem": "GalacticShadow.mux_cs09_vs_alkashi_exact_witness",
        },
        "portal_220_sssp_lean_witness": p220_witness,
        "dark_mode_shadow_pi_inf": shadow_pi_inf,
        "aletheia_calculus_parity": parity_info,
        "cs09_galactic_duality_verified": duality_verified,
    }


def _verify_exp_q60b_gate_and_lds() -> dict[str, Any]:
    b_cost_a = {"kind": "power", "coeff": "10", "exponent": "1"}
    b_cost_b = {"kind": "power", "coeff": "1", "exponent": "2"}
    res_at_11 = detect_galactic_shadow(b_cost_a, b_cost_b, 11)
    res_at_10 = detect_galactic_shadow(b_cost_a, b_cost_b, 10)
    need(
        res_at_11["status"] == "TERRESTRIAL_CROSSOVER"
        and res_at_11["n_star"]["value_int_str"] == "11"
        and res_at_10["status"] == "GALACTIC_SHADOW"
        and res_at_10["n_star"]["value_int_str"] == "11",
        "BOUNDARY_N11_FAIL",
        "N*=11 vs N_phys=10/11 boundary mismatch",
    )

    r5_reject_cases = [
        ("bool_horizon", lambda: detect_galactic_shadow(b_cost_a, b_cost_b, True)),
        ("float_horizon", lambda: detect_galactic_shadow(b_cost_a, b_cost_b, json.loads("10.5"))),
        ("zero_horizon", lambda: detect_galactic_shadow(b_cost_a, b_cost_b, 0)),
        ("float_coeff", lambda: detect_galactic_shadow({"kind": "power", "coeff": json.loads("1.5"), "exponent": "1"}, b_cost_b, 10)),
        ("bad_kind", lambda: detect_galactic_shadow({"kind": "exp", "coeff": "1", "exponent": "1"}, b_cost_b, 10)),
        ("dup_json", lambda: parse_exact_json(b'{"a":1,"a":2}\n', "dup")),
        ("float_json", lambda: parse_exact_json(b'{"a":1.5}\n', "flt")),
        ("unicode_digits_frac", lambda: require_fraction("\u0661\u0662/\u0663", "u")),
        ("huge_denom_exp", lambda: detect_galactic_shadow({"kind": "power", "coeff": "2", "exponent": "999999/1000000"}, b_cost_b, 10)),
    ]
    r5_caught = 0
    for lbl, fn in r5_reject_cases:
        try:
            fn()
        except VerifierError:
            r5_caught += 1
        else:
            raise VerifierError("R5_CASE_NOT_REJECTED", f"R5 reject case {lbl} unexpectedly passed")

    lds = run_lipton_demillo_sayward_coupling()
    mw = lds["m2_pairwise_masking_witness"]
    need(Fraction(lds["m1_kill_rate_q"]) == _ONE, "LDS_M1_FAIL", "LDS M1 kill rate < 1/1")
    need(Fraction(lds["m2_coupling_rate_q"]) == _ONE and len(lds["m2_survivors"]) == 0, "LDS_M2_FAIL", "LDS M2 survivor detected")
    need(
        mw["m1_sub_swap_killed_without_boundary"]
        and mw["m1_cmp_neg_killed_without_boundary"]
        and mw["m2_pairwise_masking_survives_without_boundary"]
        and mw["m2_pairwise_masking_killed_with_boundary"],
        "LDS_MASKING_MISSING",
        "2nd-order pairwise fault-masking demonstration failed",
    )

    return {
        "boundary_n11_vs_n10_ok": True,
        "r5_reject_cases_caught": r5_caught,
        "r5_reject_cases_total": len(r5_reject_cases),
        "lds_coupling": lds,
    }


def build_certificate(
    track_dir: Path,
    *,
    live_lean: bool = False,
    aletheia_root: Path | None = None,
    runner: Callable[[Sequence[str], Path, int], tuple[int, bytes, bytes]] | None = None,
) -> dict[str, Any]:
    """Independently compute the Stage-2 Fortress certificate and canonical payload SHA-256."""
    source_bytes = {fname: read_nofollow_bytes(track_dir.joinpath(fname), fname) for fname in SOURCE_FILES_TO_PIN}
    for fname, raw in source_bytes.items():
        verify_pure_q_ast(raw.decode("utf-8"), fname)
    source_hashes = {fname: _sha256(raw) for fname, raw in source_bytes.items()}

    lean_info = verify_lean_bundle(track_dir, live_lean=live_lean, runner=runner)
    q60a = _verify_exp_q60a_portfolio_and_duality(aletheia_root)
    q60b = _verify_exp_q60b_gate_and_lds()

    body: dict[str, Any] = {
        "cpu_only": True,
        "cross_references": [
            "Foundation-0/continuum",
            "Foundation-0/cave-expedition#31",
            "Foundation-0/aletheia",
        ],
        "exp_q60a": q60a,
        "exp_q60b": q60b,
        "lean_bundle": lean_info,
        "novelty_classification": "N1",
        "oracle_class": "exact",
        "prior_stage1_prereg_id": "PREREG-W22-GALACTIC-SHADOW",
        "prior_stage1_prereg_sha256": "8145a7c7bbc25a14ba0cc38d0866e9884f8459ea5bb0a8af6713f14fdbc0565f",
        "queue_id": "EXP-Q60a+EXP-Q60b",
        "schema": "s174.q60.galactic_shadow_certificate.v2",
        "source_sha256": source_hashes,
        "stage": "STAGE2_FORTRESS",
        "track": "S174",
        "weights_inside_expedition": 0,
        "zero_ast_div": True,
        "zero_bare_asserts": True,
        "zero_floats": True,
    }
    payload_sha = _sha256(_canon_bytes(body))
    cert = dict(body)
    cert["payload_sha256"] = payload_sha
    return cert


def verify_certificate_file(
    cert_path: Path,
    track_dir: Path,
    *,
    live_lean: bool = False,
    aletheia_root: Path | None = None,
    runner: Callable[[Sequence[str], Path, int], tuple[int, bytes, bytes]] | None = None,
) -> dict[str, Any]:
    """Read cert_path under O_NOFOLLOW and verify strict equality + STATIC_ONLY vs live split."""
    raw = read_nofollow_bytes(cert_path, "certificate")
    loaded = parse_exact_json(raw, "certificate")
    need(type(loaded) is dict, "CERT_NOT_DICT", "certificate root must be object")

    lb = loaded.get("lean_bundle")
    need(type(lb) is dict, "CERT_MISMATCH", "certificate missing lean_bundle")
    q60a_raw = loaded.get("exp_q60a")
    ap = q60a_raw.get("aletheia_calculus_parity") if type(q60a_raw) is dict else None
    need(type(ap) is dict, "CERT_MISMATCH", "certificate missing aletheia_calculus_parity")

    if not live_lean:
        need(
            lb.get("live_lean_checked") is False and lb.get("lean_live_mode") == "STATIC_ONLY",
            "LEAN_LIVE_STATUS_MISMATCH",
            "offline --check rejects certificates claiming live Lean verification; pass --live-lean",
        )
    if aletheia_root is None:
        need(
            ap.get("live_checked") is False and ap.get("mode") == "SELF_CONTAINED_EXACT",
            "ALETHEIA_LIVE_STATUS_MISMATCH",
            "offline --check rejects certificates claiming live aletheia.calculus verification; pass --aletheia-root",
        )

    is_static_cert = (lb.get("live_lean_checked") is False) and (ap.get("live_checked") is False)
    if is_static_cert and (live_lean or aletheia_root is not None):
        expected_static = build_certificate(track_dir, live_lean=False, aletheia_root=None)
        need(exact_json_equal(loaded, expected_static), "CERT_MISMATCH", "static certificate mismatch")
        need(raw == _canon_bytes(expected_static), "CERT_NON_CANONICAL", "static certificate bytes non-canonical")
        return build_certificate(track_dir, live_lean=live_lean, aletheia_root=aletheia_root, runner=runner)

    if live_lean:
        need(lb.get("live_lean_checked") is True, "LEAN_LIVE_STATUS_MISMATCH", "invalid live_lean_checked")
    if aletheia_root is not None:
        need(ap.get("live_checked") is True, "ALETHEIA_LIVE_STATUS_MISMATCH", "invalid aletheia live_checked")
    expected = build_certificate(track_dir, live_lean=live_lean, aletheia_root=aletheia_root, runner=runner)
    need(exact_json_equal(loaded, expected), "CERT_MISMATCH", "certificate does not match expected payload")
    need(raw == _canon_bytes(expected), "CERT_NON_CANONICAL", "certificate bytes are not canonical")
    return expected


class _VerHelpAction(argparse.Action):
    def __init__(self, option_strings: Sequence[str], dest: str = argparse.SUPPRESS, default: Any = argparse.SUPPRESS, help: str | None = None) -> None:
        super().__init__(option_strings=option_strings, dest=dest, default=default, nargs=0, help=help)

    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values: Any, option_string: str | None = None) -> None:
        raise _HelpExit({"description": parser.description or "", "prog": parser.prog, "status": "HELP", "usage": parser.format_usage().strip()})


class _StrictParser(argparse.ArgumentParser):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["allow_abbrev"] = False
        kwargs["add_help"] = False
        super().__init__(*args, **kwargs)
        self.add_argument("-h", "--help", action=_VerHelpAction, help="Emit canonical JSON help and exit 0")

    def error(self, message: str) -> Any:
        raise VerifierError("CLI_ARG_ERROR", message)


def main(argv: Sequence[str] | None = None) -> int:
    try:
        parser = _StrictParser(prog="galactic_shadow_verifier", description="Track S174 Stage-2 Fortress Verifier", allow_abbrev=False)
        parser.add_argument("--track-dir", type=Path, default=Path(__file__).resolve().parent, help="Track directory")
        grp = parser.add_mutually_exclusive_group(required=False)
        grp.add_argument("--write", type=Path, default=None, help="Write certificate atomically with O_NOFOLLOW")
        grp.add_argument("--check", type=Path, nargs="?", const=Path("s174_stage2_certificate.json"), default=None, help="Verify certificate file")
        grp.add_argument("--standalone", action="store_true", help="Compute and emit certificate JSON to stdout")
        parser.add_argument("--live-lean", action="store_true", help="Run isolated Lean 4.36.0 kernel replay")
        parser.add_argument("--aletheia-root", type=Path, default=None, help="Optional path to aletheia repo for live calculus parity")
        args = parser.parse_args(argv)

        track_dir = args.track_dir
        aletheia_root = args.aletheia_root
        if args.standalone:
            cert = build_certificate(track_dir, live_lean=args.live_lean, aletheia_root=aletheia_root)
            sys.stdout.write(_canon_bytes(cert).decode("utf-8"))
            return 0
        if args.write is not None:
            cert = build_certificate(track_dir, live_lean=args.live_lean, aletheia_root=aletheia_root)
            raw = _canon_bytes(cert)
            atomic_write_nofollow(args.write, raw)
            sys.stdout.write(raw.decode("utf-8"))
            return 0

        cert_path = args.check if args.check is not None else track_dir.joinpath("s174_stage2_certificate.json")
        if not cert_path.is_absolute():
            cand = track_dir.joinpath(cert_path)
            if cand.exists():
                cert_path = cand
        cert = verify_certificate_file(cert_path, track_dir, live_lean=args.live_lean, aletheia_root=aletheia_root)
        sys.stdout.write(_canon_bytes(cert).decode("utf-8"))
        return 0
    except _HelpExit as sig:
        sys.stdout.write(json.dumps(sig.payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n")
        return 0
    except VerifierError as exc:
        sys.stderr.write(json.dumps({"code": exc.code, "message": exc.message, "status": "ERROR"}, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n")
        return 2
    except SystemExit as exc:
        sys.stderr.write(json.dumps({"code": "CLI_SYSTEM_EXIT", "message": f"unexpected SystemExit({exc.code})", "status": "ERROR"}, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n")
        return 2
    except Exception as exc:
        sys.stderr.write(json.dumps({"code": f"UNHANDLED_{type(exc).__name__.upper()}", "message": str(exc), "status": "ERROR"}, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
