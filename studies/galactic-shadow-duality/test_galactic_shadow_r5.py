#!/usr/bin/env python3
"""Track S174 (EXP-Q60a/b) Stage-2 Fortress R1-R7 & Mutation-Hardening Test Suite.

Stdlib-only, zero bare asserts, zero floats, zero ast.Div, RO-snapshot safe
(`chmod 0o644` on copied temp files), 3x -I bit-identical (`0` stdout bytes).
"""
from __future__ import annotations

import ast
from contextlib import redirect_stderr, redirect_stdout
import errno
from fractions import Fraction
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from typing import Any, Callable, Sequence


TRACK_DIR = Path(__file__).resolve().parent
if str(TRACK_DIR) not in sys.path:
    sys.path.insert(0, str(TRACK_DIR))

import galactic_shadow_verifier as gsv  # noqa: E402


def _copy_writable(src: Path, dst: Path) -> None:
    """Copy a file even from a chmod a-w RO snapshot and make the temp copy 0o644."""
    shutil.copy2(src, dst)
    os.chmod(dst, 0o644)


def _mock_lean_runner(
    *,
    version_rc: int = 0,
    version_out: bytes = b"Lean (version 4.36.0, x86_64-unknown-linux-gnu, commit 611c117bfaf7b7ae1cfcf246ce6fba31e8f509e9, Release)\n",
    version_err: bytes = b"",
    build_rc: int = 0,
    build_out: bytes = b"Build completed successfully.\n",
    build_err: bytes = b"",
    axiom_rc: int = 0,
    axiom_err: bytes = b"",
    axiom_override: bytes | None = None,
) -> Callable[[Sequence[str], Path, int], tuple[int, bytes, bytes]]:
    def _runner(args: Sequence[str], cwd: Path, timeout: int) -> tuple[int, bytes, bytes]:
        if list(args) == ["lean", "--version"]:
            return version_rc, version_out, version_err
        if list(args) == ["lake", "build"]:
            return build_rc, build_out, build_err
        if axiom_override is not None:
            return axiom_rc, axiom_override, axiom_err
        lines: list[str] = []
        for thm in gsv.EXPECTED_THEOREMS:
            if thm in gsv.EXPECTED_ZERO_AXIOM_THEOREMS:
                lines.append(f"'{thm}' does not depend on any axioms")
            elif thm in gsv.EXPECTED_PROPEXT_ONLY_THEOREMS:
                lines.append(f"'{thm}' depends on axioms: [propext]")
            else:
                lines.append(f"'{thm}' depends on axioms: [propext, Quot.sound]")
        return axiom_rc, ("\n".join(lines) + "\n").encode("utf-8"), axiom_err

    return _runner


def _write_clean_bundle(dst: Path) -> None:
    for fname in (
        "GalacticShadow.lean",
        "lean-toolchain",
        "lakefile.toml",
        "lake-manifest.json",
        "galactic_shadow_verifier.py",
        "test_galactic_shadow_r5.py",
    ):
        _copy_writable(TRACK_DIR.joinpath(fname), dst.joinpath(fname))


def _write_fake_aletheia_pkg(
    pkg_root: Path,
    *,
    dim_dark_pi: int = 1,
    r_cross_pi: int = 1,
    kb_pi: str = "((Fraction(-1, 1), Fraction(1, 1)),)",
    cm_pi: str = "((Fraction(-2, 1),),)",
    schur_pi: int = 4,
    dim_dark_full: int = 0,
    r_cross_full: int = 0,
    kb_full: str = "()",
    cm_full: str = "None",
    schur_full: int = 3,
    r5_pass_ok: bool = True,
    r5_pass_num: int = 2,
    r5_leak_ok: bool = False,
    r5_leak_num: int = 1,
    broken_import: bool = False,
) -> None:
    pkg_dir = pkg_root.joinpath("aletheia")
    pkg_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(pkg_dir, 0o755)
    init_p = pkg_dir.joinpath("__init__.py")
    init_p.write_text("", encoding="utf-8", newline="\n")
    os.chmod(init_p, 0o644)
    calc_p = pkg_dir.joinpath("calculus.py")
    if broken_import:
        calc_p.write_text("raise RuntimeError('broken')\n", encoding="utf-8", newline="\n")
        os.chmod(calc_p, 0o644)
        return
    src = (
        "from dataclasses import dataclass\n"
        "from fractions import Fraction\n"
        "@dataclass(frozen=True)\n"
        "class IndexSet:\n"
        "    indices: tuple[int, ...]\n"
        "@dataclass(frozen=True)\n"
        "class ShadowRecord:\n"
        "    kernel_basis: object\n"
        "    coupling_map: object\n"
        "    dim_dark: int\n"
        "    r_cross: int\n"
        "@dataclass(frozen=True)\n"
        "class R5Spec:\n"
        "    predicate: object\n"
        "    mutants: tuple[object, ...]\n"
        "@dataclass(frozen=True)\n"
        "class GateResult:\n"
        "    passed: bool\n"
        "    kill_ratio: Fraction\n"
        "def qmat(rows):\n"
        "    return tuple(tuple(Fraction(v, 1) for v in r) for r in rows)\n"
        "def op_dark_mode_shadow(m, elim):\n"
        f"    if len(m) == 3: return ShadowRecord({kb_pi}, {cm_pi}, {dim_dark_pi}, {r_cross_pi})\n"
        f"    return ShadowRecord({kb_full}, {cm_full}, {dim_dark_full}, {r_cross_full})\n"
        "def op_schur_pushforward(m, elim):\n"
        f"    if len(m) == 3: return ((Fraction({schur_pi}, 1),),)\n"
        f"    return ((Fraction({schur_full}, 1),),)\n"
        "def op_r5_gate(spec, target):\n"
        f"    if spec.mutants[1] == (1024, 256): return GateResult({r5_pass_ok}, Fraction({r5_pass_num}, 2))\n"
        f"    return GateResult({r5_leak_ok}, Fraction({r5_leak_num}, 2))\n"
    )
    calc_p.write_text(src, encoding="utf-8", newline="\n")
    os.chmod(calc_p, 0o644)


class TestS174GalacticShadowR5(unittest.TestCase):
    def _assert_err(self, expected_code: str, fn: Callable[[], Any]) -> None:
        with self.assertRaises(gsv.VerifierError) as cm:
            fn()
        self.assertEqual(cm.exception.code, expected_code)

    def test_01_strict_types_fractions_ast_and_zone_b_io(self) -> None:
        self.assertTrue(gsv.is_exact_int(5))
        self.assertFalse(gsv.is_exact_int(True))
        self.assertEqual(gsv.require_strict_int(1, "x", min_value=1, max_value=5), 1)
        self.assertEqual(gsv.require_strict_int(5, "x", min_value=1, max_value=5), 5)
        self._assert_err("STRICT_INT_REQUIRED", lambda: gsv.require_strict_int(True, "x"))
        self._assert_err("STRICT_INT_REQUIRED", lambda: gsv.require_strict_int("1", "x"))
        self._assert_err("INT_OUT_OF_RANGE", lambda: gsv.require_strict_int(0, "x", min_value=1))
        self._assert_err("INT_OUT_OF_RANGE", lambda: gsv.require_strict_int(6, "x", min_value=1, max_value=5))

        self.assertEqual(gsv.require_fraction("3/4", "f", positive=True), Fraction(3, 4))
        self.assertEqual(gsv.require_fraction("+3/4", "f", positive=True), Fraction(3, 4))
        self.assertEqual(gsv.require_fraction(Fraction(0, 1), "f", non_negative=True), Fraction(0, 1))
        self.assertEqual(gsv.require_fraction(2, "f", positive=True), Fraction(2, 1))
        self.assertEqual(gsv.require_fraction("9" * gsv.MAX_INT_DIGITS, "ok_dig"), Fraction(int("9" * gsv.MAX_INT_DIGITS), 1))
        self.assertEqual(gsv.require_fraction(Fraction((1 << gsv.MAX_FRAC_BITS) - 1, 1), "ok_bits"), Fraction((1 << gsv.MAX_FRAC_BITS) - 1, 1))
        self._assert_err("BOOL_FORBIDDEN", lambda: gsv.require_fraction(True, "f"))
        self._assert_err("FLOAT_FORBIDDEN", lambda: gsv.require_fraction(json.loads("1.5"), "f"))
        self._assert_err("FLOAT_TEXT_FORBIDDEN", lambda: gsv.require_fraction("", "f"))
        self._assert_err("FLOAT_TEXT_FORBIDDEN", lambda: gsv.require_fraction("1.5", "f"))
        self._assert_err("FLOAT_TEXT_FORBIDDEN", lambda: gsv.require_fraction("1e3", "f"))
        # LOW-2 regression: non-ASCII Unicode digits must be rejected
        self._assert_err("FLOAT_TEXT_FORBIDDEN", lambda: gsv.require_fraction("\u0661\u0662/\u0663", "f"))
        self._assert_err("BAD_FRACTION_STRING", lambda: gsv.require_fraction("1/0", "f"))
        # MED-5 regression: digit and bit limits on Fraction terms (incl. leading-zero >1024 digits killing M014)
        self._assert_err("FRAC_TOO_LONG", lambda: gsv.require_fraction("0" * (gsv.MAX_INT_DIGITS + 1), "f"))
        self._assert_err("FRAC_TOO_LONG", lambda: gsv.require_fraction("1/" + ("9" * (gsv.MAX_INT_DIGITS + 1)), "f"))
        self._assert_err("FRAC_TOO_LONG", lambda: gsv.require_fraction(Fraction(1 << gsv.MAX_FRAC_BITS, 1), "f"))
        self._assert_err("FRAC_TOO_LONG", lambda: gsv.require_fraction(Fraction(1, 1 << gsv.MAX_FRAC_BITS), "f"))
        self._assert_err("BAD_FRACTION_TYPE", lambda: gsv.require_fraction([1], "f"))
        self._assert_err("FRACTION_NOT_POSITIVE", lambda: gsv.require_fraction(0, "f", positive=True))
        self._assert_err("FRACTION_NEGATIVE", lambda: gsv.require_fraction(-1, "f", non_negative=True))
        self._assert_err("ZERO_DIVISOR", lambda: gsv.qdiv(Fraction(1, 1), Fraction(0, 1)))
        self.assertEqual(gsv._exact_isqrt_if_square(-1), None)
        self.assertEqual(gsv._exact_isqrt_if_square(0), 0)
        self.assertEqual(gsv._exact_isqrt_if_square(9), 3)
        self.assertEqual(gsv._exact_isqrt_if_square(10), None)

        # Self AST check & negative AST catches (incl. MED-7 float()/pow()/2**-1)
        gsv.verify_pure_q_ast(TRACK_DIR.joinpath("galactic_shadow_verifier.py").read_text(encoding="utf-8"), "self")
        gsv.verify_pure_q_ast(TRACK_DIR.joinpath("test_galactic_shadow_r5.py").read_text(encoding="utf-8"), "test")
        self._assert_err("AST_SYNTAX", lambda: gsv.verify_pure_q_ast("def (", "bad"))
        self._assert_err("AST_DIV_FORBIDDEN", lambda: gsv.verify_pure_q_ast("x = 1 / 2\n", "div"))
        self._assert_err("AST_ASSERT_FORBIDDEN", lambda: gsv.verify_pure_q_ast("assert True\n", "asrt"))
        self._assert_err("AST_FLOAT_LITERAL", lambda: gsv.verify_pure_q_ast("x = 1." + "5\n", "flt"))
        self._assert_err("AST_FLOAT_LITERAL", lambda: gsv.verify_pure_q_ast("x = 1j\n", "cpx"))
        self._assert_err("AST_FORBIDDEN_IMPORT", lambda: gsv.verify_pure_q_ast("import math\n", "imp"))
        self._assert_err("AST_FORBIDDEN_IMPORT", lambda: gsv.verify_pure_q_ast("from math import sqrt\n", "fimp"))
        self._assert_err("AST_FORBIDDEN_NAME", lambda: gsv.verify_pure_q_ast("eval('1')\n", "nm"))
        self._assert_err("AST_FORBIDDEN_NAME", lambda: gsv.verify_pure_q_ast("x = fl" + "oat(1)\n", "fnm"))
        self._assert_err("AST_FORBIDDEN_NAME", lambda: gsv.verify_pure_q_ast("x = p" + "ow(2, -1)\n", "pnm"))
        self._assert_err("AST_NEG_POW_FORBIDDEN", lambda: gsv.verify_pure_q_ast("x = 2 ** -1\n", "npow"))
        self._assert_err("AST_FORBIDDEN_ATTR", lambda: gsv.verify_pure_q_ast("Fraction.from_float(x)\n", "at"))
        # MED-3 (Delta-2) regressions: computed/negative ** exponents, operator/getattr/dunder & dynamic-import float bypasses
        self._assert_err("AST_NONLITERAL_POW_FORBIDDEN", lambda: gsv.verify_pure_q_ast("x = 2 ** (0 - 1)\n", "cpow"))
        self._assert_err("AST_NONLITERAL_POW_FORBIDDEN", lambda: gsv.verify_pure_q_ast("e = 1\nx = 2 ** e\n", "npow2"))
        self._assert_err("AST_NONLITERAL_POW_FORBIDDEN", lambda: gsv.verify_pure_q_ast("x = 2\nx **= (0 - 1)\n", "apow"))
        self._assert_err("AST_NONLITERAL_POW_FORBIDDEN", lambda: gsv.verify_pure_q_ast("x = 2 ** True\n", "bpow"))
        self._assert_err("AST_FORBIDDEN_IMPORT", lambda: gsv.verify_pure_q_ast("import operator\nx = operator.truediv(1, 2)\n", "op1"))
        self._assert_err("AST_FORBIDDEN_IMPORT", lambda: gsv.verify_pure_q_ast("import operator\nx = operator.pow(2, -1)\n", "op2"))
        self._assert_err("AST_FORBIDDEN_IMPORT", lambda: gsv.verify_pure_q_ast("from operator import truediv\n", "op3"))
        self._assert_err("AST_FORBIDDEN_ATTR", lambda: gsv.verify_pure_q_ast("x = o.truediv(1, 2)\n", "op4"))
        self._assert_err("AST_FORBIDDEN_ATTR", lambda: gsv.verify_pure_q_ast("x = (1).__truediv__(2)\n", "dun"))
        self._assert_err("AST_FORBIDDEN_NAME", lambda: gsv.verify_pure_q_ast("x = getattr(__builtins__, 'fl' + 'oat')(1)\n", "ga"))
        self._assert_err("AST_FORBIDDEN_NAME", lambda: gsv.verify_pure_q_ast("from importlib import import_module\n", "imf"))
        self._assert_err("AST_FORBIDDEN_DYNAMIC_IMPORT", lambda: gsv.verify_pure_q_ast("import importlib\nm = importlib.import_module('math')\n", "dyn"))
        self._assert_err("AST_FORBIDDEN_DYNAMIC_IMPORT", lambda: gsv.verify_pure_q_ast("import importlib\nm = importlib.import_module(name)\n", "dyn2"))
        gsv.verify_pure_q_ast("import importlib\nm = importlib.import_module('aletheia.calculus')\nx = 2 ** 3\ny = 2\ny **= 2\n", "dyn_ok")
        self.assertEqual((gsv._ipow(3, 5), gsv._ipow(7, 0), gsv._ipow(-2, 3), gsv._ipow(2, 1)), (243, 1, -8, 2))
        self._assert_err("IPOW_DOMAIN", lambda: gsv._ipow(2, -1))
        self._assert_err("IPOW_DOMAIN", lambda: gsv._ipow(True, 2))
        self._assert_err("IPOW_DOMAIN", lambda: gsv._ipow(2, Fraction(1, 2)))

        # Exact JSON equal (keys + values + types)
        self.assertTrue(gsv.exact_json_equal({"a": [1, True, None, "x"]}, {"a": [1, True, None, "x"]}))
        self.assertFalse(gsv.exact_json_equal(True, 1))
        self.assertFalse(gsv.exact_json_equal({"a": 1}, {"a": True}))
        self.assertFalse(gsv.exact_json_equal({1: "x"}, {True: "x"}))
        self.assertFalse(gsv.exact_json_equal({"a": 1}, {"a": 1, "b": 2}))
        self.assertFalse(gsv.exact_json_equal({"a": 1}, {"b": 1}))
        self.assertFalse(gsv.exact_json_equal([1, 2], [1]))
        self.assertFalse(gsv.exact_json_equal("a", "b"))

        # Strict JSON & Zone-B O_NOFOLLOW I/O
        self._assert_err("EMPTY_JSON", lambda: gsv.parse_exact_json(b"", "e"))
        self._assert_err("BOM_FORBIDDEN", lambda: gsv.parse_exact_json(b"\xef\xbb\xbf{}\n", "b"))
        self._assert_err("CR_FORBIDDEN", lambda: gsv.parse_exact_json(b"{}\r\n", "c"))
        self._assert_err("NO_FINAL_LF", lambda: gsv.parse_exact_json(b"{}", "n"))
        self._assert_err("BAD_UTF8", lambda: gsv.parse_exact_json(b"\xff\n", "u"))
        self._assert_err("FLOAT_FORBIDDEN", lambda: gsv.parse_exact_json(b'{"a":1.5}\n', "f"))
        self._assert_err("CONST_FORBIDDEN", lambda: gsv.parse_exact_json(b'{"a":NaN}\n', "nan"))
        self._assert_err("INT_TOO_LONG", lambda: gsv.parse_exact_json(f'{{"a":{gsv._ipow(10, gsv.MAX_INT_DIGITS)}}}\n'.encode(), "big"))
        self.assertEqual(gsv.parse_exact_json(f'{{"a":{(gsv._ipow(10, gsv.MAX_INT_DIGITS)) - 1}}}\n'.encode(), "ok")["a"], (gsv._ipow(10, gsv.MAX_INT_DIGITS)) - 1)
        self._assert_err("DUP_KEY", lambda: gsv.parse_exact_json(b'{"a":1,"a":2}\n', "dup"))
        self._assert_err("JSON_SYNTAX", lambda: gsv.parse_exact_json(b"{bad}\n", "syn"))
        self._assert_err("JSON_SURROGATE", lambda: gsv.parse_exact_json(b'{"a":"\\ud800"}\n', "sur"))
        deep_ok = ('{"a":' * 64 + "1" + "}" * 64 + "\n").encode()
        deep_bad = ('{"a":' * 65 + "1" + "}" * 65 + "\n").encode()
        self.assertEqual(type(gsv.parse_exact_json(deep_ok, "d64")), dict)
        self._assert_err("JSON_DEPTH", lambda: gsv.parse_exact_json(deep_bad, "d65"))
        list_ok = ("[" * 64 + "1" + "]" * 64 + "\n").encode()
        list_bad = ("[" * 65 + "1" + "]" * 65 + "\n").encode()
        self.assertEqual(type(gsv.parse_exact_json(list_ok, "l64")), list)
        self._assert_err("JSON_DEPTH", lambda: gsv.parse_exact_json(list_bad, "l65"))

        self._assert_err("BAD_PATH", lambda: gsv.read_nofollow_bytes("", "p"))
        self._assert_err("BAD_PATH_TYPE", lambda: gsv.read_nofollow_bytes(123, "p"))  # type: ignore[arg-type]
        self._assert_err("BAD_PATH", lambda: gsv.read_nofollow_bytes("a\x00b", "p"))
        self._assert_err("DOTDOT_FORBIDDEN", lambda: gsv.read_nofollow_bytes("../x", "p"))
        self._assert_err("BAD_LEAF", lambda: gsv.read_nofollow_bytes("/", "p"))
        rel_dfd, rel_leaf = gsv._open_parent_dir_fd("single.txt", "rel")
        try:
            self.assertEqual(rel_leaf, "single.txt")
        finally:
            os.close(rel_dfd)

        with tempfile.TemporaryDirectory() as td:
            tp = Path(td)
            f_ok = tp.joinpath("ok.txt")
            gsv.atomic_write_nofollow(f_ok, b"abcd")
            self.assertEqual(gsv.read_nofollow_bytes(f_ok, "ok", max_bytes=4), b"abcd")
            self._assert_err("FILE_TOO_BIG", lambda: gsv.read_nofollow_bytes(f_ok, "ok", max_bytes=3))
            os.chmod(f_ok, 0o600)
            gsv.atomic_write_nofollow(f_ok, b"efgh")
            self.assertEqual(os.stat(f_ok).st_mode & 0o777, 0o600)

            w_mock_p = tp.joinpath("mock_io.txt")
            with mock.patch("os.lstat", side_effect=OSError(errno.EACCES, "denied")):
                self._assert_err("WRITE_LSTAT", lambda: gsv.atomic_write_nofollow(w_mock_p, b"abcd"))
            with mock.patch("os.write", side_effect=[0, 4]):
                self._assert_err("WRITE_ZERO", lambda: gsv.atomic_write_nofollow(w_mock_p, b"abcd"))
            with mock.patch("os.fsync", side_effect=[None, OSError(errno.EINVAL, "einval")]):
                gsv.atomic_write_nofollow(w_mock_p, b"abcd")
            with mock.patch("os.fsync", side_effect=[None, OSError(errno.EROFS, "erofs")]):
                gsv.atomic_write_nofollow(w_mock_p, b"abcd")
            with mock.patch("os.fsync", side_effect=[None, OSError(errno.EIO, "io")]):
                self._assert_err("DIR_FSYNC", lambda: gsv.atomic_write_nofollow(w_mock_p, b"abcd"))

            sym = tp.joinpath("sym.txt")
            sym.symlink_to(f_ok)
            self._assert_err("OPEN_FAILED", lambda: gsv.read_nofollow_bytes(sym, "sym"))
            self._assert_err("WRITE_NOT_REG", lambda: gsv.atomic_write_nofollow(sym, b"x"))
            self._assert_err("NOT_REG_FILE", lambda: gsv.read_nofollow_bytes(tp, "dir"))

            hl = tp.joinpath("hl.txt")
            os.link(f_ok, hl)
            self._assert_err("HARDLINK_REJECTED", lambda: gsv.read_nofollow_bytes(hl, "hl"))
            self._assert_err("WRITE_HARDLINK", lambda: gsv.atomic_write_nofollow(hl, b"x"))

            ro_sub = tp.joinpath("ro_sub")
            ro_sub.mkdir()
            ro_file = ro_sub.joinpath("x.txt")
            os.chmod(ro_sub, 0o555)
            try:
                if os.geteuid() != 0:
                    self._assert_err("WRITE_IO", lambda: gsv.atomic_write_nofollow(ro_file, b"x"))
            finally:
                os.chmod(ro_sub, 0o755)
            self._assert_err("PARENT_OPEN", lambda: gsv.atomic_write_nofollow(tp.joinpath("missing_dir", "x.txt"), b"x"))

    def test_02_lean_static_hardening_and_live_bundle(self) -> None:
        # MED-1 & LOW-5 & S168 Delta-3 regressions: PURE non-conflated ambiguous interpolation rejections
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('private def _evil_dbg : Nat := dbg_trace "{(by sorry : Nat)}"; 1\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f : Nat := dbg_trace "\\{"\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f : Nat := throwError "{"\ndef g : String := "}"\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f : Nat := m! "{"\ndef g : String := "}"\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f : Nat := bad! "{x}"\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f : Nat := throwErrorAt 1 "{"\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f : Nat := throwErrorAt stx "{"\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f : Nat := throwErrorAt (x) "{"\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f : Nat := throwErrorAt "a" "{"\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f : Nat := throwErrorAt «stx» "{"\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f : Nat := trace[a] "{"\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f : Nat := Macro.trace[a] "{"\n'))
        self.assertEqual(gsv.audit_lean_static('def f : Nat := dbg_trace "plain ok"; 1\ndef g := obj.m! "{"\n'), [])
        # MED-2 (Delta-2) regressions: allowlisted-macro pending_args bypasses (s!/raw/char first args, compound x[0]!)
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f := throwErrorAt s!"a" "{(by sorry : Nat)}"\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f := throwErrorAt r#"a"# "{(by sorry : Nat)}"\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static("def f := throwErrorAt 'a' \"{(by sorry : Nat)}\"\n"))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f (x : List Nat) : Nat := throwErrorAt x[0]! "{(by sorry : Nat)}"\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('open Lean Macro in def f (x : List Syntax) : MacroM Unit := throwNamedErrorAt x[0]! foo "{(by sorry : Nat)}"\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f := trace[a] (x) \n  "{"\n'))
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f := Macro.trace[a] 1 "{"\n'))
        self.assertEqual(gsv.audit_lean_static("def f := throwErrorAt 'a' \"plain\"\ndef g := throwErrorAt r#\"a\"# s!\"b {1}\"\n"), [])
        # Guard resets only at a proven command boundary (column-0 top-level declaration keyword)
        self.assertEqual(gsv.audit_lean_static('def f := throwErrorAt x "a"\ndef g : String := "{}"\n'), [])
        self._assert_err("LEAN_AMBIG_INTERP", lambda: gsv.audit_lean_static('def f := throwErrorAt x "a"\n  def g : String := "{}"\n'))

        # Separate non-conflated macro_rules / debug / stop / Lean.Elab rejections
        self._assert_err("LEAN_FORBIDDEN_KW", lambda: gsv.audit_lean_static("macro_rules | `($_ < $_) => `(True)\n"))
        self._assert_err("LEAN_DEBUG_ESCAPE", lambda: gsv.audit_lean_static("set_option debug.skipKernelTC true\n"))
        self._assert_err("LEAN_META_ESCAPE", lambda: gsv.audit_lean_static("def x := Lean.Elab.Term\n"))
        self._assert_err("LEAN_FORBIDDEN_KW", lambda: gsv.audit_lean_static("theorem p : 1 = 1 := by\n  open Nat in\n  rfl\n  stop\n  exact rfl\n"))

        # Namespace/section scope stack + allowed Init interpolation + forbidden escapes
        ns_src = "namespace A.B\ntheorem t1 : True := trivial\nend B\ntheorem t2 : True := trivial\nend A\n"
        self.assertEqual(gsv.audit_lean_static(ns_src), ["A.B.t1", "A.t2"])
        clean_src = (
            '/- /- sorry -/ -/\n-- stop\n'
            'def a : String := r#"axiom"#\n'
            "def c : Char := '\"'\n"
            'def s : String := s!"ok {1 + 1}"\n'
            "private theorem p : True := trivial\n"
            "section S\ntheorem t : True := trivial\nend S\n"
        )
        self.assertEqual(gsv.audit_lean_static(clean_src), ["t"])
        self._assert_err("LEAN_FORBIDDEN_KW", lambda: gsv.audit_lean_static('def s := s!"{sorry}"\n'))
        self._assert_err("LEAN_FORBIDDEN_AX", lambda: gsv.audit_lean_static("def x := _root_.sorryAx\n"))
        self._assert_err("LEAN_VAR_INC", lambda: gsv.audit_lean_static("variable (n : Nat)\ninclude n\n"))
        self._assert_err("LEAN_PARTIAL", lambda: gsv.audit_lean_static("partial private def f : Nat := 0\n"))
        self._assert_err("LEAN_DECIDE_NATIVE", lambda: gsv.audit_lean_static("theorem t : True := by decide +native\n"))
        self._assert_err("LEAN_DECIDE_NATIVE", lambda: gsv.audit_lean_static("theorem t : True := by decide (native := true)\n"))
        self._assert_err("LEAN_DECIDE_NATIVE", lambda: gsv.audit_lean_static("theorem t : True := by decide (config := { native := true })\n"))
        self._assert_err("LEAN_ATTR_ESCAPE", lambda: gsv.audit_lean_static("@[extern \"c\"] def f : Nat := 0\n"))
        self._assert_err("LEAN_ATTR_ESCAPE", lambda: gsv.audit_lean_static("def f : Nat := 0\nattribute [extern \"c\"] f\n"))
        self._assert_err("LEAN_HASH_ESCAPE", lambda: gsv.audit_lean_static("#eval 1\n"))
        self._assert_err("LEAN_UNTERM_LEX", lambda: gsv.audit_lean_static("/- unclosed\n"))
        self._assert_err("LEAN_UNTERM_LEX", lambda: gsv.audit_lean_static('def x := "unclosed\n'))
        self._assert_err("LEAN_UNTERM_LEX", lambda: gsv.audit_lean_static('def s := s!"unclosed {1 + 1\n'))
        self._assert_err("LEAN_UNTERM_LEX", lambda: gsv.audit_lean_static('def x := r#"unclosed\n'))
        self._assert_err("LEAN_UNTERM_IDENT", lambda: gsv.audit_lean_static("def «unclosed := 0\n"))

        # Lakefile TOML strict schema (incl. LOW-4 root/glob/target pinning)
        gsv._audit_lakefile_toml_strict('name = "GalacticShadow"\nversion = "0.1.0"\ndefaultTargets = ["GalacticShadow"]\n[[lean_lib]]\nname = "GalacticShadow"\nsrcDir = "."\nroots = ["GalacticShadow"]\nglobs = ["GalacticShadow"]\n')
        self._assert_err("LAKEFILE_TOML", lambda: gsv._audit_lakefile_toml_strict("=bad"))
        self._assert_err("LAKEFILE_UNSAFE_KEY", lambda: gsv._audit_lakefile_toml_strict('evil = "x"\n'))
        self._assert_err("LAKEFILE_BAD_SCHEMA", lambda: gsv._audit_lakefile_toml_strict('name = "bad name"\n'))
        self._assert_err("LAKEFILE_BAD_SCHEMA", lambda: gsv._audit_lakefile_toml_strict('version = "bad"\n'))
        self._assert_err("LAKEFILE_BAD_SCHEMA", lambda: gsv._audit_lakefile_toml_strict('defaultTargets = ["Other"]\n'))
        self._assert_err("LAKEFILE_BAD_SCHEMA", lambda: gsv._audit_lakefile_toml_strict('lean_lib = "bad"\n'))
        self._assert_err("LAKEFILE_BAD_SCHEMA", lambda: gsv._audit_lakefile_toml_strict('[[lean_lib]]\nname = "GalacticShadow"\n[[lean_lib]]\nname = "GalacticShadow"\n'))
        self._assert_err("LAKEFILE_BAD_SCHEMA", lambda: gsv._audit_lakefile_toml_strict("lean_lib = [1]\n"))
        self._assert_err("LAKEFILE_UNSAFE_KEY", lambda: gsv._audit_lakefile_toml_strict('[[lean_lib]]\nbadk = 1\n'))
        self._assert_err("LAKEFILE_UNSAFE_ROOT", lambda: gsv._audit_lakefile_toml_strict('[[lean_lib]]\nname = "Other"\n'))
        self._assert_err("LAKEFILE_UNSAFE_PATH", lambda: gsv._audit_lakefile_toml_strict('[[lean_lib]]\nname = "GalacticShadow"\nsrcDir = "../evil"\n'))
        self._assert_err("LAKEFILE_UNSAFE_PATH", lambda: gsv._audit_lakefile_toml_strict('[[lean_lib]]\nname = "GalacticShadow"\nsrcDir = "/abs"\n'))
        self._assert_err("LAKEFILE_UNSAFE_PATH", lambda: gsv._audit_lakefile_toml_strict('[[lean_lib]]\nname = "GalacticShadow"\nsrcDir = ""\n'))
        self._assert_err("LAKEFILE_UNSAFE_PATH", lambda: gsv._audit_lakefile_toml_strict('[[lean_lib]]\nname = "GalacticShadow"\nsrcDir = 1\n'))
        self._assert_err("LAKEFILE_UNSAFE_ROOT", lambda: gsv._audit_lakefile_toml_strict('[[lean_lib]]\nname = "GalacticShadow"\nroots = ["Other"]\n'))
        self._assert_err("LAKEFILE_UNSAFE_GLOB", lambda: gsv._audit_lakefile_toml_strict('[[lean_lib]]\nname = "GalacticShadow"\nglobs = ["Other"]\n'))
        self._assert_err("LAKEFILE_UNSAFE_STR", lambda: gsv._audit_lakefile_toml_strict('name = "debug_byAsSorry"\n[[lean_lib]]\nname = "GalacticShadow"\nsrcDir = "a/debug.byAsSorry"\n'))

        # Bundle refusal checks + mocked live runner checks + ELF resolver checks (RO-snapshot-safe)
        with tempfile.TemporaryDirectory() as td:
            tp = Path(td)
            _write_clean_bundle(tp)
            fake_home = tp.joinpath("fake_home")
            tc_bin = fake_home.joinpath(".elan", "toolchains", "leanprover--lean4---v4.36.0", "bin")
            tc_bin.mkdir(parents=True)
            with mock.patch("pwd.getpwuid", return_value=type("PW", (), {"pw_dir": os.fspath(fake_home)})()):
                self._assert_err("LEAN_EXEC_FAILED", gsv._resolve_verified_elf_lean)
                tc_bin.joinpath("lean").write_bytes(b"\x7fELF")
                os.chmod(tc_bin.joinpath("lean"), 0o644)
                tc_bin.joinpath("lake").write_bytes(b"\x7fELF")
                os.chmod(tc_bin.joinpath("lake"), 0o755)
                self._assert_err("LEAN_TOOL_UNTRUSTED", gsv._resolve_verified_elf_lean)
                tc_bin.joinpath("lean").write_bytes(b"#!/bin/sh\n")
                os.chmod(tc_bin.joinpath("lean"), 0o755)
                self._assert_err("LEAN_TOOL_UNTRUSTED", gsv._resolve_verified_elf_lean)
                tc_bin.joinpath("lean").write_bytes(b"\x7fELF")
                os.chmod(tc_bin.joinpath("lean"), 0o755)
                resolved_bins = gsv._resolve_verified_elf_lean()
                self.assertEqual(resolved_bins[2], fake_home)
                fake_proc = type("Proc", (), {"returncode": 0, "stdout": b"ok", "stderr": b""})()
                with mock.patch("subprocess.run", return_value=fake_proc) as m_run:
                    self.assertEqual(gsv._default_lean_runner(["lean", "--version"], tp, 5), (0, b"ok", b""))
                    self.assertEqual(m_run.call_args.args[0][0], os.fspath(tc_bin.joinpath("lean")))
                    self.assertEqual(gsv._default_lean_runner(["lake", "build"], tp, 5), (0, b"ok", b""))
                    self.assertEqual(m_run.call_args.args[0][0], os.fspath(tc_bin.joinpath("lake")))
                    self.assertEqual(gsv._default_lean_runner(["lake", "env", "lean", "A.lean"], tp, 5), (0, b"ok", b""))
                    self.assertEqual(m_run.call_args.args[0][2], os.fspath(tc_bin.joinpath("lean")))
                with mock.patch("subprocess.run", side_effect=subprocess.TimeoutExpired(["lean"], 1)):
                    self._assert_err("LEAN_EXEC_FAILED", lambda: gsv._default_lean_runner(["lean", "--version"], tp, 1))

            # Live mocked pass (4 zero-axiom, 2 propext-only, 6 propext+Quot.sound)
            live_res = gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner())
            self.assertEqual(live_res["lean_live_mode"], "LIVE_LEAN_4_36_0_PASS")
            self.assertEqual(live_res["axioms_verified_count"], 12)
            self.assertEqual(live_res["zero_axiom_theorems"], 4)
            self.assertEqual(live_res["propext_only_theorems"], 2)
            self.assertEqual(live_res["propext_quot_theorems"], 6)
            self.assertTrue(live_res["theorem_types_live_checked"])
            self.assertTrue(live_res["pinned_lean_sha256_verified"])

            # Live mocked failures (incl. LOW-3 non-empty lean --version stderr)
            self._assert_err("LEAN_VER_BAD", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(version_rc=1)))
            self._assert_err("LEAN_VER_BAD", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(version_err=b"warn\n")))
            self._assert_err("LIVE_LEAN_UTF8", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(version_out=b"\xff\n")))
            self._assert_err("LAKE_BUILD_BAD", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(build_rc=1)))
            self._assert_err("LIVE_LEAN_UTF8", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(build_out=b"\xff\n")))
            self._assert_err("LAKE_BUILD_WARNING", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(build_out=b"warning: unused\n")))
            self._assert_err("AXIOM_EXEC_BAD", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(axiom_rc=1)))
            self._assert_err("LIVE_LEAN_UTF8", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(axiom_override=b"\xff\n")))
            self._assert_err("AXIOM_EXEC_WARNING", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(axiom_override=b"warning: x\n")))
            dup_ax = b"'GalacticShadow.crossover_horizon_unique' does not depend on any axioms\n'GalacticShadow.crossover_horizon_unique' does not depend on any axioms\n"
            self._assert_err("AXIOM_DUP_THEOREM", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(axiom_override=dup_ax)))
            dup_ax_list = b"'GalacticShadow.lipton_demillo_sayward_r5_coupling_witness' depends on axioms: [propext]\n'GalacticShadow.lipton_demillo_sayward_r5_coupling_witness' depends on axioms: [propext]\n"
            self._assert_err("AXIOM_DUP_THEOREM", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(axiom_override=dup_ax_list)))
            self._assert_err("AXIOM_LINE_BAD", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(axiom_override=b"garbled\n")))
            bad_ax = b"'GalacticShadow.crossover_horizon_unique' depends on axioms: [Classical.choice]\n"
            self._assert_err("FORBIDDEN_AXIOM", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(axiom_override=bad_ax)))
            self._assert_err("AXIOM_SET_MISMATCH", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(axiom_override=b"'GalacticShadow.crossover_horizon_unique' does not depend on any axioms\n")))
            swapped = []
            for thm in gsv.EXPECTED_THEOREMS:
                if thm == "GalacticShadow.crossover_horizon_unique":
                    swapped.append(f"'{thm}' depends on axioms: [propext]")
                elif thm in gsv.EXPECTED_ZERO_AXIOM_THEOREMS:
                    swapped.append(f"'{thm}' does not depend on any axioms")
                else:
                    swapped.append(f"'{thm}' depends on axioms: [propext, Quot.sound]")
            self._assert_err("ZERO_AX_SPLIT_MISMATCH", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(axiom_override=("\n".join(swapped) + "\n").encode())))
            swapped_prop = []
            for thm in gsv.EXPECTED_THEOREMS:
                if thm in gsv.EXPECTED_ZERO_AXIOM_THEOREMS:
                    swapped_prop.append(f"'{thm}' does not depend on any axioms")
                else:
                    swapped_prop.append(f"'{thm}' depends on axioms: [propext, Quot.sound]")
            self._assert_err("PROPEXT_SPLIT_MISMATCH", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(axiom_override=("\n".join(swapped_prop) + "\n").encode())))
            bad_part = []
            for thm in gsv.EXPECTED_THEOREMS:
                if thm in gsv.EXPECTED_ZERO_AXIOM_THEOREMS:
                    bad_part.append(f"'{thm}' does not depend on any axioms")
                elif thm in gsv.EXPECTED_PROPEXT_ONLY_THEOREMS:
                    bad_part.append(f"'{thm}' depends on axioms: [propext]")
                elif thm == "GalacticShadow.finite_fourier_vs_fwht256_crossover":
                    bad_part.append(f"'{thm}' depends on axioms: [Quot.sound]")
                else:
                    bad_part.append(f"'{thm}' depends on axioms: [propext, Quot.sound]")
            self._assert_err("AXIOM_PARTITION_MISMATCH", lambda: gsv.verify_lean_bundle(tp, live_lean=True, runner=_mock_lean_runner(axiom_override=("\n".join(bad_part) + "\n").encode())))

            # Static bundle tamper checks (incl. MED-3 signature + SHA-256 pinning, LOW-4 broken symlinks + extra .lean)
            orig_lf = tp.joinpath("lakefile.toml").read_bytes()
            tp.joinpath("lakefile.toml").write_bytes(orig_lf.replace(b"\n", b"\r\n"))
            self._assert_err("LEAN_BUNDLE_CR", lambda: gsv.verify_lean_bundle(tp))
            tp.joinpath("lakefile.toml").write_bytes(orig_lf)
            tp.joinpath("lean-toolchain").write_bytes(b"\xff\n")
            self._assert_err("LEAN_BUNDLE_UTF8", lambda: gsv.verify_lean_bundle(tp))
            tp.joinpath("lean-toolchain").write_text("leanprover/lean4:v4.0.0\n", encoding="utf-8", newline="\n")
            self._assert_err("TOOLCHAIN_BAD", lambda: gsv.verify_lean_bundle(tp))
            _copy_writable(TRACK_DIR.joinpath("lean-toolchain"), tp.joinpath("lean-toolchain"))
            tp.joinpath("lake-manifest.json").write_text('{"packages":["bad"]}\n', encoding="utf-8", newline="\n")
            self._assert_err("MANIFEST_PKGS", lambda: gsv.verify_lean_bundle(tp))
            _copy_writable(TRACK_DIR.joinpath("lake-manifest.json"), tp.joinpath("lake-manifest.json"))

            # MED-3: replacing theorem types with `True := trivial` fails THEOREM_SIGNATURE_MISMATCH
            trivial_thms = "namespace GalacticShadow\n" + "\n".join(
                f"theorem {t.split('.', 1)[1]} : True := trivial" for t in gsv.EXPECTED_THEOREMS
            ) + "\nend GalacticShadow\n"
            tp.joinpath("GalacticShadow.lean").write_text(trivial_thms, encoding="utf-8", newline="\n")
            self._assert_err("THEOREM_SIGNATURE_MISMATCH", lambda: gsv.verify_lean_bundle(tp))

            # MED-3 + exact MAX_LEAN_LINES boundary: padding to MAX_LEAN_LINES hits LEAN_HASH_MISMATCH, +1 hits LEAN_TOO_LONG
            lean_orig = TRACK_DIR.joinpath("GalacticShadow.lean").read_text(encoding="utf-8")
            pad_max = lean_orig + ("-- pad\n" * (gsv.MAX_LEAN_LINES - len(lean_orig.splitlines())))
            tp.joinpath("GalacticShadow.lean").write_text(pad_max, encoding="utf-8", newline="\n")
            self._assert_err("LEAN_HASH_MISMATCH", lambda: gsv.verify_lean_bundle(tp))
            tp.joinpath("GalacticShadow.lean").write_text(pad_max + "-- over\n", encoding="utf-8", newline="\n")
            self._assert_err("LEAN_TOO_LONG", lambda: gsv.verify_lean_bundle(tp))
            tp.joinpath("GalacticShadow.lean").write_text("theorem x : True := trivial\n", encoding="utf-8", newline="\n")
            self._assert_err("THEOREM_LIST_MISMATCH", lambda: gsv.verify_lean_bundle(tp))
            _copy_writable(TRACK_DIR.joinpath("GalacticShadow.lean"), tp.joinpath("GalacticShadow.lean"))

            # LOW-4: extra .lean file + broken symlinks for lakefile.lean and .lake
            tp.joinpath("Extra.lean").write_text("theorem extra : True := trivial\n", encoding="utf-8", newline="\n")
            self._assert_err("EXTRA_LEAN_FILE_FORBIDDEN", lambda: gsv.verify_lean_bundle(tp))
            tp.joinpath("Extra.lean").unlink()
            tp.joinpath("lakefile.lean").symlink_to(tp.joinpath("nonexistent_target"))
            self._assert_err("LAKEFILE_LEAN_FORBIDDEN", lambda: gsv.verify_lean_bundle(tp))
            tp.joinpath("lakefile.lean").unlink()
            tp.joinpath(".lake").symlink_to(tp.joinpath("nonexistent_target"))
            self._assert_err("LAKE_RESIDUE", lambda: gsv.verify_lean_bundle(tp))

    def test_03_galactic_oracle_horizons_karatsuba_and_operators(self) -> None:
        h1 = gsv.validate_horizon_bound({"kind": "exact_int", "value_int": 8})
        h2 = gsv.validate_horizon_bound({"kind": "pow2_bound", "log2_exp": "3", "tower_height": 1})
        self.assertEqual(h1["value_int"], 8)
        self.assertEqual(h2["value_int"], 8)
        self.assertFalse(gsv.compare_horizon_gt(h1, h2))
        self.assertTrue(gsv.compare_horizon_gt(gsv.validate_horizon_bound(9), h1))
        h_big = gsv.validate_horizon_bound({"kind": "pow2_bound", "log2_exp": "5000", "tower_height": 1})
        h_big2 = gsv.validate_horizon_bound({"kind": "pow2_bound", "log2_exp": "5001", "tower_height": 1})
        self.assertTrue(gsv.compare_horizon_gt(h_big2, h_big))
        self.assertFalse(gsv.compare_horizon_gt(h_big, h_big))

        # HIGH-1(a) regression: multi-height tower comparison (tower_height accounted for strictly!)
        ht3_10 = gsv.validate_horizon_bound({"kind": "pow2_bound", "log2_exp": "10", "tower_height": 3})
        ht2_266 = gsv.validate_horizon_bound({"kind": "pow2_bound", "log2_exp": "266", "tower_height": 2})
        self.assertTrue(gsv.compare_horizon_gt(ht3_10, ht2_266))
        self.assertFalse(gsv.compare_horizon_gt(ht2_266, ht3_10))
        r_h1a = gsv.detect_galactic_shadow(
            {"kind": "tower_cutoff", "valid_from_log2_exp": "10", "tower_height": 3},
            {"kind": "power", "coeff": "1", "exponent": "2"},
            {"kind": "pow2_bound", "log2_exp": "266", "tower_height": 2},
        )
        self.assertEqual(r_h1a["status"], "GALACTIC_SHADOW")
        # Exact multi-height equality & boundary cases: tower(4, 3) == tower(2, 256)
        ht4_3 = gsv.validate_horizon_bound({"kind": "pow2_bound", "log2_exp": "3", "tower_height": 4})
        ht2_256 = gsv.validate_horizon_bound({"kind": "pow2_bound", "log2_exp": "256", "tower_height": 2})
        ht2_255 = gsv.validate_horizon_bound({"kind": "pow2_bound", "log2_exp": "255", "tower_height": 2})
        ht2_257 = gsv.validate_horizon_bound({"kind": "pow2_bound", "log2_exp": "257", "tower_height": 2})
        self.assertFalse(gsv.compare_horizon_gt(ht4_3, ht2_256))
        self.assertFalse(gsv.compare_horizon_gt(ht2_256, ht4_3))
        self.assertTrue(gsv.compare_horizon_gt(ht4_3, ht2_255))
        self.assertTrue(gsv.compare_horizon_gt(ht2_257, ht4_3))
        # _cmp_tower_vs_rational edge cases (x < 1, x == 1, dh==1 fractional, dh>=2 overlap)
        self.assertEqual(gsv._cmp_tower_vs_rational(1, Fraction(0, 1), Fraction(1, 2)), 1)
        self.assertEqual(gsv._cmp_tower_vs_rational(1, Fraction(0, 1), Fraction(1, 1)), 0)
        self.assertEqual(gsv._cmp_tower_vs_rational(1, Fraction(1, 1), Fraction(1, 1)), 1)
        self.assertEqual(gsv._cmp_tower_vs_rational(2, Fraction(0, 1), Fraction(1, 1)), 1)
        self.assertEqual(gsv._cmp_tower_vs_rational(1, Fraction(3, 1), Fraction(9, 1)), -1)
        self.assertEqual(gsv._cmp_tower_vs_rational(1, Fraction(3, 2), Fraction(3, 1)), -1)
        self.assertEqual(gsv._cmp_tower_vs_rational(1, Fraction(3, 2), Fraction(5, 2)), 1)
        self.assertEqual(gsv._cmp_tower_vs_rational(2, Fraction(2, 1), Fraction(17, 1)), -1)
        self.assertEqual(gsv._cmp_tower_vs_rational(2, Fraction(1, 1), Fraction(9, 1)), -1)
        self._assert_err("HORIZON_INCOMPARABLE", lambda: gsv._cmp_tower_vs_rational(1, Fraction(4097, 2) + Fraction(2049, 1), Fraction((1 << 4097) + 1, 1)))
        self._assert_err("HORIZON_INCOMPARABLE", lambda: gsv._cmp_tower_vs_rational(2, Fraction(1, 2), Fraction(3, 1)))
        # Fail-closed HORIZON_INCOMPARABLE on overlapping pow2_bound intervals
        ov_lhs = {"kind": "pow2_bound", "value_int": None, "log2_lower_q": Fraction(3990, 1), "log2_upper_q": Fraction(4150, 1), "tower_height": 1, "strict_above_lower": True, "strict_below_upper": False}
        ov_rhs = gsv.validate_horizon_bound({"kind": "pow2_bound", "log2_exp": "4000", "tower_height": 1})
        self._assert_err("HORIZON_INCOMPARABLE", lambda: gsv.compare_horizon_gt(ov_lhs, ov_rhs))
        # Exact tie with strict_below_upper on rhs: exact 2^5000 vs strict_above_lower=True 2^5000+1
        strict_lhs = {"kind": "pow2_bound", "value_int": None, "log2_lower_q": Fraction(5000, 1), "log2_upper_q": Fraction(5001, 1), "tower_height": 1, "strict_above_lower": True, "strict_below_upper": True}
        self.assertTrue(gsv.compare_horizon_gt(strict_lhs, h_big))

        # HIGH-1(b) regressions: overlapping power bounds & exact-tie 2^5000+1 vs 2^5000
        r_h1b1 = gsv.detect_galactic_shadow(
            {"kind": "power", "coeff": "3", "exponent": "1"},
            {"kind": "power", "coeff": "1", "exponent": "2557/2556"},
            {"kind": "pow2_bound", "log2_exp": "4000", "tower_height": 1},
        )
        self.assertEqual(r_h1b1["status"], "GALACTIC_SHADOW")
        r_h1b1_big_t = gsv.detect_galactic_shadow(
            {"kind": "power", "coeff": "3", "exponent": "1"},
            {"kind": "power", "coeff": "1", "exponent": "3155/3154"},
            {"kind": "pow2_bound", "log2_exp": "5000", "tower_height": 1},
        )
        self.assertEqual(r_h1b1_big_t["status"], "TERRESTRIAL_CROSSOVER")
        r_h1b1_big_g = gsv.detect_galactic_shadow(
            {"kind": "power", "coeff": "3", "exponent": "1"},
            {"kind": "power", "coeff": "1", "exponent": "3156/3155"},
            {"kind": "pow2_bound", "log2_exp": "5000", "tower_height": 1},
        )
        self.assertEqual(r_h1b1_big_g["status"], "GALACTIC_SHADOW")
        r_h1b2 = gsv.detect_galactic_shadow(
            {"kind": "power", "coeff": "2", "exponent": "1"},
            {"kind": "power", "coeff": "1", "exponent": "5001/5000"},
            {"kind": "pow2_bound", "log2_exp": "5000", "tower_height": 1},
        )
        self.assertEqual(r_h1b2["status"], "GALACTIC_SHADOW")
        # Non-refinable power overlap fails closed with HORIZON_INCOMPARABLE
        self._assert_err(
            "HORIZON_INCOMPARABLE",
            lambda: gsv._resolve_power_horizon_gt_exact(
                {"coeff": Fraction(3, 1), "exponent": Fraction(1, 1)},
                {"coeff": Fraction(1, 1), "exponent": Fraction(3155, 3154)},
                {"kind": "pow2_bound", "value_int": None, "log2_lower_q": Fraction(5000, 1), "log2_upper_q": Fraction(5001, 1), "tower_height": 1, "strict_above_lower": False, "strict_below_upper": False},
            ),
        )
        self._assert_err(
            "HORIZON_INCOMPARABLE",
            lambda: gsv._resolve_power_horizon_gt_exact(
                {"coeff": Fraction(3, 1), "exponent": Fraction(1, 1)},
                {"coeff": Fraction(1, 1), "exponent": Fraction(10001, 10000)},
                {"kind": "pow2_bound", "value_int": None, "log2_lower_q": Fraction(100000, 1), "log2_upper_q": Fraction(100000, 1), "tower_height": 1, "strict_above_lower": False, "strict_below_upper": False},
            ),
        )

        # HIGH-1 (Delta-2) R5: integer problem sizes N <= floor(2^(k_n/k_d)) on fractional pow2_bound limits (k_d > 1)
        self.assertEqual((gsv._iroot_floor(8, 2), gsv._iroot_floor(1, 5), gsv._iroot_floor(1 << 10, 1), gsv._iroot_floor(1 << 3, 7)), (2, 1, 1024, 1))
        pow2_3_2 = {"kind": "pow2_bound", "log2_exp": "3/2"}
        quad_b = {"kind": "power", "coeff": "1", "exponent": "2"}
        r_h1_52 = gsv.detect_galactic_shadow({"kind": "power", "coeff": "5/2", "exponent": "1"}, quad_b, pow2_3_2)
        self.assertEqual((r_h1_52["status"], r_h1_52["n_star"]["value_int_str"], r_h1_52["n_phys_max"]["kind"]), ("GALACTIC_SHADOW", "3", "pow2_bound"))
        r_h1_2 = gsv.detect_galactic_shadow({"kind": "power", "coeff": "2", "exponent": "1"}, quad_b, pow2_3_2)
        self.assertEqual((r_h1_2["status"], r_h1_2["n_star"]["value_int_str"]), ("GALACTIC_SHADOW", "3"))
        r_h1_199 = gsv.detect_galactic_shadow({"kind": "power", "coeff": "199/100", "exponent": "1"}, quad_b, pow2_3_2)
        self.assertEqual((r_h1_199["status"], r_h1_199["n_star"]["value_int_str"]), ("TERRESTRIAL_CROSSOVER", "2"))
        # > 2^4096 regime: (r_n/r_d)^10 strictly inside (floor(2^(8201/2)), 2^(8201/2)) => N* = floor(2^(8201/2)) + 1
        f_8201_2 = gsv._iroot_floor(1 << 8201, 2)
        self.assertTrue(f_8201_2 * f_8201_2 < (1 << 8201) < (f_8201_2 + 1) * (f_8201_2 + 1))
        scale_s = 1 << 4600
        cf_lo = Fraction(gsv._iroot_floor(f_8201_2 * scale_s ** 10, 10) + 1, scale_s)
        cf_hi = Fraction(gsv._iroot_floor((1 << 8201) * scale_s ** 20, 20), scale_s)
        cf_terms: list[int] = []
        cf_x, cf_y = cf_lo, cf_hi
        while True:
            cf_a = cf_x.numerator // cf_x.denominator
            if Fraction(cf_a + 1, 1) < cf_y:
                cf_terms.append(cf_a + 1)
                break
            cf_terms.append(cf_a)
            cf_x, cf_y = gsv.qdiv(Fraction(1, 1), cf_y - cf_a), gsv.qdiv(Fraction(1, 1), cf_x - cf_a)
        cf_r = Fraction(cf_terms[-1], 1)
        for cf_t in reversed(cf_terms[:-1]):
            cf_r = cf_t + gsv.qdiv(Fraction(1, 1), cf_r)
        self.assertTrue(f_8201_2 < cf_r ** 10 and cf_r ** 20 < (1 << 8201))
        self.assertEqual((cf_r.numerator.bit_length(), cf_r.denominator.bit_length()), (2259, 1849))
        h8201 = {"kind": "pow2_bound", "log2_exp": "8201/2", "tower_height": 1}
        r_h1_big = gsv.detect_galactic_shadow({"kind": "power", "coeff": f"{cf_r.numerator}/{cf_r.denominator}", "exponent": "1"}, {"kind": "power", "coeff": "1", "exponent": "11/10"}, h8201)
        self.assertEqual((r_h1_big["status"], r_h1_big["n_star"]["value_int_str"]), ("GALACTIC_SHADOW", None))
        cf_r_lo = Fraction(f_8201_2 - 1, 1) ** 1
        self.assertFalse(gsv._resolve_power_horizon_gt_exact(
            {"coeff": cf_r_lo, "exponent": Fraction(1, 1)}, {"coeff": Fraction(1, 1), "exponent": Fraction(2, 1)}, gsv.validate_horizon_bound(h8201)))
        self.assertTrue(gsv._resolve_power_horizon_gt_exact(
            {"coeff": Fraction(f_8201_2, 1), "exponent": Fraction(1, 1)}, {"coeff": Fraction(1, 1), "exponent": Fraction(2, 1)}, gsv.validate_horizon_bound(h8201)))
        self._assert_err(
            "HORIZON_INCOMPARABLE",
            lambda: gsv._resolve_power_horizon_gt_exact(
                {"coeff": Fraction(3, 1), "exponent": Fraction(1, 1)},
                {"coeff": Fraction(1, 1), "exponent": Fraction(2, 1)},
                {"kind": "pow2_bound", "value_int": None, "log2_lower_q": Fraction(1, 1 << 17), "log2_upper_q": Fraction(1, 1 << 17), "tower_height": 1, "strict_above_lower": False, "strict_below_upper": False},
            ),
        )

        self._assert_err("BAD_HORIZON_SPEC", lambda: gsv.validate_horizon_bound("bad"))
        self._assert_err("UNKNOWN_HORIZON_KIND", lambda: gsv.validate_horizon_bound({"kind": "bad"}))
        self._assert_err("INT_OUT_OF_RANGE", lambda: gsv.validate_horizon_bound({"kind": "pow2_bound", "log2_exp": "10", "tower_height": 65}))
        self._assert_err("BAD_COST_SPEC", lambda: gsv.validate_cost_spec("x", "c"))
        self._assert_err("BAD_COST_KIND", lambda: gsv.validate_cost_spec({"kind": "bad"}, "c"))

        # MED-5 regression: bounded rational exponents & bit budget (incl. exact boundary == MAX_POWER_WORK_BITS)
        self._assert_err("EXP_OUT_OF_RANGE", lambda: gsv.validate_cost_spec({"kind": "power", "coeff": "2", "exponent": "999999/1000000"}, "c"))
        self._assert_err("EXP_OUT_OF_RANGE", lambda: gsv.validate_cost_spec({"kind": "power", "coeff": "2", "exponent": "1025"}, "c"))
        self._assert_err("EXP_OUT_OF_RANGE", lambda: gsv.validate_cost_spec({"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1/65", "log_exponent": "1"}, "c"))
        self._assert_err("EXP_OUT_OF_RANGE", lambda: gsv.validate_cost_spec({"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "1025"}, "c"))
        self._assert_err("INT_OUT_OF_RANGE", lambda: gsv.validate_cost_spec({"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "1", "log_offset": gsv.MAX_LOG_OFFSET + 1}, "c"))
        self._assert_err("POWER_EXPONENT_LIMIT", lambda: gsv._eval_power_ratio_lt(Fraction(1 << 500, 1), Fraction(1, 1), Fraction(1, 1), Fraction(1001, 1000), 2))
        self._assert_err("POWER_EXPONENT_LIMIT", lambda: gsv._eval_power_ratio_lt(Fraction(1 << 500, 1), Fraction(1001, 1000), Fraction(1, 1), Fraction(1, 1), 2))
        self._assert_err("POWER_EXPONENT_LIMIT", lambda: gsv._solve_power_crossover(Fraction((1 << 100) + 1, 1 << 100), Fraction(1, 1), Fraction(1, 1), Fraction(1001, 1000)))
        self.assertEqual(gsv._solve_power_crossover(Fraction((1 << 31) + 1, 1 << 31), Fraction(1, 1), Fraction(1, 1), Fraction(2049, 2048))["value_int"], 2)
        # Non-power HORIZON_INCOMPARABLE propagation through detect_galactic_shadow (kills M192)
        self._assert_err(
            "HORIZON_INCOMPARABLE",
            lambda: gsv.detect_galactic_shadow(
                {"kind": "tower_cutoff", "valid_from_log2_exp": "1/2", "tower_height": 3},
                {"kind": "power", "coeff": "1", "exponent": "2"},
                {"kind": "pow2_bound", "log2_exp": "3", "tower_height": 1},
            ),
        )

        # Power edges
        self.assertEqual(gsv.detect_galactic_shadow({"kind": "power", "coeff": "1/2", "exponent": "1"}, {"kind": "power", "coeff": "1", "exponent": "2"}, 1)["n_star"]["value_int_str"], "1")
        self.assertEqual(gsv.detect_galactic_shadow({"kind": "power", "coeff": "1", "exponent": "1"}, {"kind": "power", "coeff": "1", "exponent": "2"}, 1)["n_star"]["value_int_str"], "2")
        self.assertEqual(gsv.detect_galactic_shadow({"kind": "power", "coeff": "1", "exponent": "2"}, {"kind": "power", "coeff": "2", "exponent": "2"}, 1)["status"], "TERRESTRIAL_CROSSOVER")
        self.assertEqual(gsv.detect_galactic_shadow({"kind": "power", "coeff": "2", "exponent": "2"}, {"kind": "power", "coeff": "2", "exponent": "2"}, 10)["status"], "NO_ASYMPTOTIC_ADVANTAGE")
        self.assertTrue(gsv._eval_power_ratio_lt(Fraction(1, 1), Fraction(2, 1), Fraction(4, 1), Fraction(1, 1), 2))
        self.assertFalse(gsv._eval_power_ratio_lt(Fraction(1, 1), Fraction(2, 1), Fraction(4, 1), Fraction(1, 1), 4))
        self.assertTrue(gsv._eval_power_ratio_lt(Fraction(1, 1), Fraction(1, 1), Fraction(2, 1), Fraction(1, 1), 5))
        r_pow2_gt = gsv.detect_galactic_shadow({"kind": "power", "coeff": "2", "exponent": "1"}, {"kind": "power", "coeff": "1", "exponent": "5001/5000"}, 10)
        self.assertEqual(r_pow2_gt["n_star"]["log2_upper_q"], "5120001/1024")
        self.assertEqual(r_pow2_gt["n_star"]["tower_height"], 1)
        r_est_eq = gsv.detect_galactic_shadow({"kind": "power", "coeff": str((1 << 64) - 1), "exponent": "1"}, {"kind": "power", "coeff": "1", "exponent": "65/64"}, 10)
        self.assertIsNotNone(r_est_eq["n_star"]["value_int_str"])
        r_huge_np2 = gsv.detect_galactic_shadow({"kind": "power", "coeff": "3", "exponent": "1"}, {"kind": "power", "coeff": "1", "exponent": "10001/10000"}, 10)
        self.assertIsNone(r_huge_np2["n_star"]["value_int_str"])

        # HIGH-2 regressions: polylog early dips & uncapped search + Portal 220 sssp-lean
        self._assert_err("POLYLOG_DOMAIN", lambda: gsv._eval_polylog_dyadic_lt({"coeff": Fraction(1), "n_exponent": Fraction(1), "log_exponent": Fraction(1), "log_offset": 0}, {"coeff": Fraction(1), "n_exponent": Fraction(1), "log_exponent": Fraction(1), "log_offset": 0}, 0))
        self._assert_err("POLYLOG_EXPONENT_LIMIT", lambda: gsv._eval_polylog_dyadic_lt({"coeff": Fraction(1), "n_exponent": Fraction(1), "log_exponent": Fraction(1), "log_offset": 0}, {"coeff": Fraction(1), "n_exponent": Fraction(2), "log_exponent": Fraction(1), "log_offset": 0}, gsv.MAX_POLYLOG_SHIFT_BITS + 1))
        self.assertTrue(gsv._eval_polylog_dyadic_lt({"coeff": Fraction(1), "n_exponent": Fraction(1), "log_exponent": Fraction(0), "log_offset": 0}, {"coeff": Fraction(1), "n_exponent": Fraction(2), "log_exponent": Fraction(0), "log_offset": 0}, gsv.MAX_POLYLOG_SHIFT_BITS))
        self._assert_err("POLYLOG_EXPONENT_LIMIT", lambda: gsv._eval_polylog_dyadic_lt({"coeff": Fraction(1), "n_exponent": Fraction(1), "log_exponent": Fraction(1000, 67), "log_offset": 0}, {"coeff": Fraction(1), "n_exponent": Fraction(1), "log_exponent": Fraction(1000, 61), "log_offset": 0}, 1))
        self.assertEqual(gsv.detect_galactic_shadow({"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "2", "log_exponent": "1", "log_offset": 0}, {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "2", "log_offset": 0}, 16)["status"], "NO_ASYMPTOTIC_ADVANTAGE")
        self.assertEqual(gsv.detect_galactic_shadow({"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "2", "log_offset": 0}, {"kind": "polylog_dyadic", "coeff": "10", "n_exponent": "1", "log_exponent": "1", "log_offset": 0}, 16)["status"], "NO_ASYMPTOTIC_ADVANTAGE")
        # Same n_exp & same log_exp cases
        self.assertEqual(gsv.detect_galactic_shadow({"kind": "polylog_dyadic", "coeff": "2", "n_exponent": "1", "log_exponent": "1", "log_offset": 0}, {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "1", "log_offset": 0}, 16)["status"], "NO_ASYMPTOTIC_ADVANTAGE")
        self.assertEqual(gsv.detect_galactic_shadow({"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "1", "log_offset": 2}, {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "1", "log_offset": 1}, 16)["status"], "NO_ASYMPTOTIC_ADVANTAGE")
        self.assertEqual(gsv.detect_galactic_shadow({"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "1", "log_offset": 0}, {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "1", "log_offset": 2}, 16)["n_star"]["value_int_str"], "2")
        self.assertEqual(gsv.detect_galactic_shadow({"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "1", "log_offset": 10}, {"kind": "polylog_dyadic", "coeff": "2", "n_exponent": "1", "log_exponent": "1", "log_offset": 0}, 16)["n_star"]["log2_lower_q"], "11/1")
        # HIGH-2 live repro 1 (early m=1 dip, true N*=2048)
        r_h2_1 = gsv.detect_galactic_shadow(
            {"kind": "polylog_dyadic", "coeff": "3", "n_exponent": "1", "log_exponent": "3", "log_offset": 0},
            {"kind": "polylog_dyadic", "coeff": "2", "n_exponent": "2", "log_exponent": "0", "log_offset": 0},
            1024,
        )
        self.assertEqual(r_h2_1["status"], "GALACTIC_SHADOW")
        self.assertEqual(r_h2_1["n_star"]["value_int_str"], "2048")
        # HIGH-2 live repro 2 (same n_exp dip, true m*=788, ratio=5/2)
        r_h2_2 = gsv.detect_galactic_shadow(
            {"kind": "polylog_dyadic", "coeff": "1000", "n_exponent": "1", "log_exponent": "1", "log_offset": 0},
            {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "2", "log_offset": 100},
            1 << 100,
        )
        self.assertEqual(r_h2_2["status"], "GALACTIC_SHADOW")
        self.assertEqual(r_h2_2["n_star"]["log2_lower_q"], "788/1")
        self.assertEqual(r_h2_2["dominance_ratio_at_n_phys_q"], "5/2")
        # HIGH-2 live repro 3 (exceeds old 8192 cap, true m*=20001)
        r_h2_3 = gsv.detect_galactic_shadow(
            {"kind": "polylog_dyadic", "coeff": "20000", "n_exponent": "1", "log_exponent": "1", "log_offset": 0},
            {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "2", "log_offset": 0},
            1 << 100,
        )
        self.assertEqual(r_h2_3["status"], "GALACTIC_SHADOW")
        self.assertEqual(r_h2_3["n_star"]["log2_lower_q"], "20001/1")
        # Polylog everywhere-dominant & delta_n>0 downward-scan paths + Portal 220 sssp-lean
        r_pl_all1 = gsv.detect_galactic_shadow(
            {"kind": "polylog_dyadic", "coeff": "1/100", "n_exponent": "1", "log_exponent": "1", "log_offset": 0},
            {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "2", "log_offset": 10},
            16,
        )
        self.assertEqual(r_pl_all1["n_star"]["value_int_str"], "2")
        r_pl_down = gsv.detect_galactic_shadow(
            {"kind": "polylog_dyadic", "coeff": "16", "n_exponent": "1", "log_exponent": "1", "log_offset": 0},
            {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "2", "log_exponent": "1", "log_offset": 0},
            32,
        )
        self.assertEqual(r_pl_down["status"], "TERRESTRIAL_CROSSOVER")
        self.assertEqual(r_pl_down["n_star"]["log2_lower_q"], "5/1")
        r_pl_down1 = gsv.detect_galactic_shadow(
            {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "2", "log_offset": 0},
            {"kind": "polylog_dyadic", "coeff": "100", "n_exponent": "2", "log_exponent": "0", "log_offset": 0},
            32,
        )
        self.assertEqual(r_pl_down1["n_star"]["value_int_str"], "2")
        r_ff_256 = gsv.detect_galactic_shadow(
            {"kind": "polylog_dyadic", "coeff": "3", "n_exponent": "1", "log_exponent": "1/2", "log_offset": 1},
            {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "1", "log_offset": 0},
            256,
        )
        self.assertEqual(r_ff_256["dominance_ratio_at_n_phys_q"], "9/8")
        self.assertEqual(r_ff_256["n_star"]["value_int_str"], "1024")
        # Portal 220 sssp-lean (m+1)^64 < 2^m crosses at m*=590 > 266
        r_p220 = gsv.detect_galactic_shadow(
            {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "0", "log_exponent": "64", "log_offset": 1},
            {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "0", "log_offset": 0},
            {"kind": "pow2_bound", "log2_exp": "266", "tower_height": 1},
        )
        self.assertEqual(r_p220["status"], "GALACTIC_SHADOW")
        self.assertEqual(r_p220["n_star"]["log2_lower_q"], "590/1")
        # Exact MAX_POLYLOG_M boundary (kills M183 & M185) + overflow
        r_pl_max1 = gsv.detect_galactic_shadow(
            {"kind": "polylog_dyadic", "coeff": f"{(1 << 60) - 1}/{1 << 60}", "n_exponent": "1", "log_exponent": "1", "log_offset": 1},
            {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "1", "log_offset": 0},
            16,
        )
        self.assertEqual(r_pl_max1["n_star"]["log2_lower_q"], f"{1 << 60}/1")
        r_pl_max2 = gsv.detect_galactic_shadow(
            {"kind": "polylog_dyadic", "coeff": str((1 << 60) - 1), "n_exponent": "1", "log_exponent": "1", "log_offset": 0},
            {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "2", "log_offset": 0},
            16,
        )
        self.assertEqual(r_pl_max2["n_star"]["log2_lower_q"], f"{1 << 60}/1")
        self._assert_err(
            "POLYLOG_EXPONENT_LIMIT",
            lambda: gsv.detect_galactic_shadow(
                {"kind": "polylog_dyadic", "coeff": str(1 << 80), "n_exponent": "1", "log_exponent": "1", "log_offset": 0},
                {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "1", "log_exponent": "2", "log_offset": 0},
                16,
            ),
        )
        self._assert_err(
            "POLYLOG_EXPONENT_LIMIT",
            lambda: gsv.detect_galactic_shadow(
                {"kind": "polylog_dyadic", "coeff": str((1 << 70) - 1), "n_exponent": "1", "log_exponent": "1", "log_offset": 100},
                {"kind": "polylog_dyadic", "coeff": str(1 << 70), "n_exponent": "1", "log_exponent": "1", "log_offset": 0},
                16,
            ),
        )

        # LOW-3 (Delta-2): cancelling equal-offset polylog exponents (ba == bb, oa == ob) => exact m* = 1, no spurious limit
        r_low3 = gsv.detect_galactic_shadow(
            {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "0", "log_exponent": "1000", "log_offset": 0},
            {"kind": "polylog_dyadic", "coeff": "2", "n_exponent": "1/64", "log_exponent": "1000", "log_offset": 0},
            16,
        )
        self.assertEqual((r_low3["status"], r_low3["n_star"]["log2_lower_q"]), ("TERRESTRIAL_CROSSOVER", "1/1"))
        r_low3b = gsv.detect_galactic_shadow(
            {"kind": "polylog_dyadic", "coeff": "1", "n_exponent": "0", "log_exponent": "1000", "log_offset": 5},
            {"kind": "polylog_dyadic", "coeff": "2", "n_exponent": "1/64", "log_exponent": "1001", "log_offset": 3},
            16,
        )
        self.assertEqual(r_low3b["n_star"]["log2_lower_q"], "229/1")

        # HIGH-3 regressions: affine & quadratic vertex-start everywhere-dominant + transient dip
        self.assertEqual(gsv.detect_galactic_shadow({"kind": "affine_linear", "fixed": "0", "slope": "1", "quad": "2"}, {"kind": "affine_linear", "fixed": "10", "slope": "10", "quad": "1"}, 10)["status"], "NO_ASYMPTOTIC_ADVANTAGE")
        self.assertEqual(gsv.detect_galactic_shadow({"kind": "affine_linear", "fixed": "0", "slope": "5", "quad": "0"}, {"kind": "affine_linear", "fixed": "10", "slope": "2", "quad": "0"}, 10)["status"], "NO_ASYMPTOTIC_ADVANTAGE")
        self.assertEqual(gsv.detect_galactic_shadow({"kind": "affine_linear", "fixed": "1", "slope": "2", "quad": "0"}, {"kind": "affine_linear", "fixed": "2", "slope": "2", "quad": "0"}, 1)["status"], "TERRESTRIAL_CROSSOVER")
        self.assertEqual(gsv.detect_galactic_shadow({"kind": "affine_linear", "fixed": "2", "slope": "2", "quad": "0"}, {"kind": "affine_linear", "fixed": "2", "slope": "2", "quad": "0"}, 10)["status"], "NO_ASYMPTOTIC_ADVANTAGE")
        # HIGH-3 live repro: 20*N < 1000 + N + N^2 for ALL N >= 1 -> N*=1 TERRESTRIAL_CROSSOVER
        r_h3 = gsv.detect_galactic_shadow(
            {"kind": "affine_linear", "fixed": "0", "slope": "20", "quad": "0"},
            {"kind": "affine_linear", "fixed": "1000", "slope": "1", "quad": "1"},
            5,
        )
        self.assertEqual(r_h3["status"], "TERRESTRIAL_CROSSOVER")
        self.assertEqual(r_h3["n_star"]["value_int_str"], "1")
        self.assertEqual(r_h3["dominance_ratio_at_n_phys_q"], "10/103")
        # Vertex edge: D(N) = 2*N^2 - 17*N + 36 = (N - 4)(2*N - 9) -> D(4)=0, D(5)=1 -> N*=5
        r_h3_v = gsv.detect_galactic_shadow(
            {"kind": "affine_linear", "fixed": "0", "slope": "18", "quad": "0"},
            {"kind": "affine_linear", "fixed": "36", "slope": "1", "quad": "2"},
            5,
        )
        self.assertEqual(r_h3_v["n_star"]["value_int_str"], "5")
        r_quad_dip = gsv.detect_galactic_shadow(
            {"kind": "affine_linear", "fixed": "0", "slope": "20", "quad": "0"},
            {"kind": "affine_linear", "fixed": "25", "slope": "1", "quad": "1"},
            10,
        )
        self.assertEqual(r_quad_dip["status"], "GALACTIC_SHADOW")
        self.assertEqual(r_quad_dip["n_star"]["value_int_str"], "18")

        # MED-4 regressions: tower_cutoff asymp_rank enforcement
        t1 = {"kind": "tower_cutoff", "valid_from_log2_exp": "100", "tower_height": 2, "asymp_rank": 1}
        t2 = {"kind": "tower_cutoff", "valid_from_log2_exp": "50", "tower_height": 2, "asymp_rank": 2}
        self.assertEqual(gsv.detect_galactic_shadow(t1, t1, 10)["status"], "NO_ASYMPTOTIC_ADVANTAGE")
        self.assertEqual(gsv.detect_galactic_shadow(t2, t1, 10)["status"], "NO_ASYMPTOTIC_ADVANTAGE")
        self.assertEqual(gsv.detect_galactic_shadow(t2, {"kind": "power", "coeff": "1", "exponent": "2"}, 10)["status"], "NO_ASYMPTOTIC_ADVANTAGE")
        self.assertEqual(gsv.detect_galactic_shadow(t1, t2, 10)["status"], "GALACTIC_SHADOW")
        self._assert_err("INCOMPATIBLE_COST_MODELS", lambda: gsv.detect_galactic_shadow({"kind": "power", "coeff": "1", "exponent": "1"}, {"kind": "affine_linear", "fixed": "0", "slope": "1", "quad": "0"}, 10))
        self._assert_err("TOWER_INCOMPATIBLE", lambda: gsv.detect_galactic_shadow(t1, {"kind": "affine_linear", "fixed": "0", "slope": "1", "quad": "0"}, 10))

        # Karatsuba exact recurrence + [257, 279] guard + S161 + MUX + duality + Portal 220 guards
        kar = gsv._verify_karatsuba_recurrence_exact(8192)
        self.assertEqual(kar["stage1_truncated_window_256_n_star"], 165)
        self.assertEqual(kar["re_crossing_interval"], [257, 279])
        self.assertEqual(kar["re_crossing_count"], 23)
        self.assertEqual(kar["global_n_star"], 280)
        self._assert_err("KAR_STAGE1_BAD", lambda: gsv._verify_karatsuba_recurrence_exact(280, tk_override=lambda n: 1))
        self._assert_err("KAR_GLOBAL_BAD", lambda: gsv._verify_karatsuba_recurrence_exact(256))
        self._assert_err("KAR_RECROSS_BAD", lambda: gsv._verify_karatsuba_recurrence_exact(285, tk_override=lambda n: (2 * n * n) if n in (164, 279) else 1))
        self._assert_err("S161_DOM_FAIL", lambda: gsv._verify_s161_dominance((2,), ag4_fn=lambda q: 142))
        self._assert_err("MUX_CS09_FAIL", lambda: gsv._verify_mux_cs09_witness(Fraction(0, 1)))
        self._assert_err("MUX_CS09_FAIL", lambda: gsv._verify_mux_cs09_witness(Fraction(1, 16)))
        self._assert_err("MUX_CS09_FAIL", lambda: gsv._verify_mux_cs09_witness(e3_half_override=gsv.qdiv(Fraction(3, 256), Fraction(127, 128))))
        self._assert_err("MUX_CS09_FAIL", lambda: gsv._verify_mux_cs09_witness(e4_half_override=gsv.qdiv(Fraction(4, 256), Fraction(253, 256))))
        self._assert_err("CS09_DUAL_FAIL", lambda: gsv._verify_cs09_galactic_duality_witness(scale_pairs=()))
        self._assert_err("CS09_DUAL_FAIL", lambda: gsv._verify_cs09_galactic_duality_witness(scale_pairs=((0, 2),)))
        self._assert_err("CS09_DUAL_FAIL", lambda: gsv._verify_cs09_galactic_duality_witness(scale_pairs=((4, 3),)))
        self.assertTrue(gsv._verify_portal_220_sssp_lean_witness()["exceeds_universe_2_pow_266"])
        self._assert_err("SSSP_P220_FAIL", lambda: gsv._verify_portal_220_sssp_lean_witness(base=2))
        # Portal 220 integer crossovers, independently recomputed: FIRST crossing 589^64 + 1 (least N with N > L_N^64) and
        # EVENTUAL crossover N* = 590^64 + 1 (least N0 with N > L_N^64 for all N >= N0); the dyadic crossover is m* = 590.
        p220 = gsv._verify_portal_220_sssp_lean_witness()
        n_first = 589 ** 64 + 1
        n_int = 590 ** 64 + 1
        self.assertEqual(p220["first_crossing_n_str"], str(n_first))
        self.assertEqual(p220["integer_crossover_n_star_str"], str(n_int))
        self.assertEqual(
            (p220["first_crossing_bit_length"], p220["integer_crossover_bit_length"], p220["dyadic_crossover_m_star"]),
            (589, 590, 590),
        )
        self.assertEqual(p220["refail_window_first_n_str"], str((1 << 589) - 1))
        self.assertEqual(p220["refail_window_last_n_str"], str(590 ** 64))
        self.assertIs(p220["integer_crossover_universal_induction_exact"], True)
        self.assertTrue(n_first > (n_first + 1).bit_length() ** 64 and n_first - 1 <= ((n_first - 1) + 1).bit_length() ** 64)
        self.assertTrue(n_int > (n_int + 1).bit_length() ** 64 and n_int - 1 <= ((n_int - 1) + 1).bit_length() ** 64)
        # The first crossing is NOT the eventual crossover: P re-fails at 2^589 - 1 <= 590^64 (L = 590 band).
        n_refail = (1 << 589) - 1
        self.assertTrue(n_refail <= (n_refail + 1).bit_length() ** 64 and n_first < n_refail < n_int)
        self.assertTrue(589 ** 64 < (1 << 589) - 2 and ((1 << 589) - 1) <= ((1 << 589) - 1 + 1).bit_length() ** 64)
        # Exhaustive brute-force cross-check of the band scan on a small instance (base=6, exp=2): first=26, eventual=37.
        p_small = gsv._verify_portal_220_sssp_lean_witness(base=6, exp=2, univ_bits=2)
        fails_small = [n for n in range(1, 4096) if n <= ((n + 1).bit_length()) ** 2]
        self.assertEqual(min(n for n in range(1, 4096) if n not in fails_small), int(p_small["first_crossing_n_str"]))
        self.assertEqual(max(fails_small) + 1, int(p_small["integer_crossover_n_star_str"]))
        self.assertEqual((p_small["first_crossing_n_str"], p_small["integer_crossover_n_star_str"]), ("26", "37"))
        self._assert_err("SSSP_P220_INT_FAIL", lambda: gsv._verify_portal_220_sssp_lean_witness(base=(1 << 589) + 1, exp=1))
        mux_w = gsv._verify_mux_cs09_witness()
        self.assertIs(mux_w[4], True)

        # Dark-mode shadow & R5 gate operators + errors
        sh_zero = gsv.dark_mode_shadow_and_schur_exact([[Fraction(4), Fraction(1)], [Fraction(1), Fraction(0)]], (1,))
        self.assertEqual((sh_zero["dim_dark"], sh_zero["r_cross"], sh_zero["schur_q"]), (1, 1, [["4/1"]]))
        sh_idx0 = gsv.dark_mode_shadow_and_schur_exact([[Fraction(2), Fraction(1)], [Fraction(1), Fraction(5)]], (0,))
        self.assertEqual((sh_idx0["dim_dark"], sh_idx0["schur_q"]), (0, [["9/2"]]))
        self._assert_err("SINGULAR_SUBMATRIX", lambda: gsv._qinv_sym([[Fraction(1), Fraction(1)], [Fraction(1), Fraction(1)]]))
        self._assert_err("SMALL_MATRIX", lambda: gsv.dark_mode_shadow_and_schur_exact([[Fraction(1)]], (0,)))
        self._assert_err("NON_SQUARE_MATRIX", lambda: gsv.dark_mode_shadow_and_schur_exact([[Fraction(1), Fraction(0)], [Fraction(0)]], (1,)))
        self._assert_err("SHADOW_NOT_SYM", lambda: gsv.dark_mode_shadow_and_schur_exact([[Fraction(1), Fraction(2)], [Fraction(0), Fraction(1)]], (1,)))
        self._assert_err("BAD_ELIM_SET", lambda: gsv.dark_mode_shadow_and_schur_exact([[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]], (0, 1)))
        self._assert_err("SHADOW_OOB", lambda: gsv.dark_mode_shadow_and_schur_exact([[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]], (2,)))
        self._assert_err("EMPTY_MUTANTS", lambda: gsv.op_r5_gate_exact(lambda x: True, 1, []))

    def test_04_aletheia_calculus_parity_and_lds_coupling(self) -> None:
        self._assert_err("ALETHEIA_ROOT_MISSING", lambda: gsv.verify_aletheia_calculus_parity(Path("/nonexistent_s174_aletheia")))
        with tempfile.TemporaryDirectory() as td:
            tp = Path(td)
            p_ok = tp.joinpath("ok")
            _write_fake_aletheia_pkg(p_ok)
            res_ok = gsv.verify_aletheia_calculus_parity(p_ok)
            self.assertEqual(res_ok["mode"], "LIVE_ALETHEIA_CALCULUS_PASS")
            self.assertTrue(res_ok["live_checked"])
            sys.modules.pop("aletheia.calculus", None)
            sys.modules.pop("aletheia", None)

            # MED-6: test kernel_basis & coupling_map parity mismatches too!
            for lbl, kw, err_code in (
                ("broken", {"broken_import": True}, "ALETHEIA_IMPORT_FAIL"),
                ("bad_sh_d", {"dim_dark_pi": 0}, "ALETHEIA_SHADOW_PARITY_FAIL"),
                ("bad_sh_r", {"r_cross_pi": 0}, "ALETHEIA_SHADOW_PARITY_FAIL"),
                ("bad_sh_kb", {"kb_pi": "((Fraction(1, 1), Fraction(1, 1)),)"}, "ALETHEIA_SHADOW_PARITY_FAIL"),
                ("bad_sh_cm", {"cm_pi": "((Fraction(2, 1),),)"}, "ALETHEIA_SHADOW_PARITY_FAIL"),
                ("bad_sh_cmn", {"cm_pi": "None"}, "ALETHEIA_SHADOW_PARITY_FAIL"),
                ("bad_sh_s", {"schur_pi": 5}, "ALETHEIA_SHADOW_PARITY_FAIL"),
                ("bad_sc_d", {"dim_dark_full": 1}, "ALETHEIA_SCHUR_PARITY_FAIL"),
                ("bad_sc_r", {"r_cross_full": 1}, "ALETHEIA_SCHUR_PARITY_FAIL"),
                ("bad_sc_kb", {"kb_full": "((Fraction(1, 1),),)"}, "ALETHEIA_SCHUR_PARITY_FAIL"),
                ("bad_sc_cm", {"cm_full": "((Fraction(0, 1),),)"}, "ALETHEIA_SCHUR_PARITY_FAIL"),
                ("bad_sc_s", {"schur_full": 99}, "ALETHEIA_SCHUR_PARITY_FAIL"),
                ("bad_r5_ok", {"r5_pass_ok": False}, "ALETHEIA_R5_PARITY_FAIL"),
                ("bad_r5_kr", {"r5_pass_num": 1}, "ALETHEIA_R5_PARITY_FAIL"),
                ("bad_r5_lk", {"r5_leak_ok": True}, "ALETHEIA_R5_PARITY_FAIL"),
                ("bad_r5_ln", {"r5_leak_num": 2}, "ALETHEIA_R5_PARITY_FAIL"),
            ):
                p_sub = tp.joinpath(lbl)
                _write_fake_aletheia_pkg(p_sub, **kw)  # type: ignore[arg-type]
                self._assert_err(err_code, lambda ps=p_sub: gsv.verify_aletheia_calculus_parity(ps))
                sys.modules.pop("aletheia.calculus", None)
                sys.modules.pop("aletheia", None)

        # Self-contained operator & portfolio/gate invariant guards
        ok_pi = {"dim_dark": 1, "r_cross": 1, "kernel_basis_q": [["-1/1", "1/1"]], "coupling_map_q": [["-2/1"]], "schur_q": [["4/1"]]}
        ok_fu = {"dim_dark": 0, "r_cross": 0, "kernel_basis_q": [], "coupling_map_q": [], "schur_q": [["3/1"]]}
        for side_sh, code in (
            ([dict(ok_pi, dim_dark=0), ok_fu], "SELF_SHADOW_MISMATCH"),
            ([dict(ok_pi, r_cross=0), ok_fu], "SELF_SHADOW_MISMATCH"),
            ([dict(ok_pi, kernel_basis_q=[["1/1", "1/1"]]), ok_fu], "SELF_SHADOW_MISMATCH"),
            ([dict(ok_pi, coupling_map_q=[["2/1"]]), ok_fu], "SELF_SHADOW_MISMATCH"),
            ([dict(ok_pi, schur_q=[["5/1"]]), ok_fu], "SELF_SHADOW_MISMATCH"),
            ([ok_pi, dict(ok_fu, dim_dark=1)], "SELF_SCHUR_MISMATCH"),
            ([ok_pi, dict(ok_fu, r_cross=1)], "SELF_SCHUR_MISMATCH"),
            ([ok_pi, dict(ok_fu, kernel_basis_q=[["1/1"]])], "SELF_SCHUR_MISMATCH"),
            ([ok_pi, dict(ok_fu, coupling_map_q=[["1/1"]])], "SELF_SCHUR_MISMATCH"),
            ([ok_pi, dict(ok_fu, schur_q=[["4/1"]])], "SELF_SCHUR_MISMATCH"),
        ):
            with mock.patch.object(gsv, "dark_mode_shadow_and_schur_exact", side_effect=side_sh):
                self._assert_err(code, lambda: gsv.verify_aletheia_calculus_parity(None))

        for side_r5, code in (
            ([{"passed": False, "kill_ratio_q": "1/1"}, {"passed": False, "kill_ratio_q": "1/2"}], "SELF_R5_PASS_BAD"),
            ([{"passed": True, "kill_ratio_q": "0/1"}, {"passed": False, "kill_ratio_q": "1/2"}], "SELF_R5_PASS_BAD"),
            ([{"passed": True, "kill_ratio_q": "1/1"}, {"passed": True, "kill_ratio_q": "1/2"}], "SELF_R5_LEAK_BAD"),
            ([{"passed": True, "kill_ratio_q": "1/1"}, {"passed": False, "kill_ratio_q": "1/1"}], "SELF_R5_LEAK_BAD"),
        ):
            with mock.patch.object(gsv, "op_r5_gate_exact", side_effect=side_r5):
                self._assert_err(code, lambda: gsv.verify_aletheia_calculus_parity(None))

        bad_port = [{"pair_id": "bad", "source": "x", "cost_asymp": {"kind": "power", "coeff": "1", "exponent": "1"}, "cost_practical": {"kind": "power", "coeff": "1", "exponent": "2"}, "n_phys_max": 1, "expected_status": "TERRESTRIAL_CROSSOVER"}]
        with mock.patch.object(gsv, "build_real_algorithm_portfolio", return_value=bad_port):
            self._assert_err("PORTFOLIO_MISMATCH", lambda: gsv._verify_exp_q60a_portfolio_and_duality(None))

        for side_b in (
            [{"status": "WRONG", "n_star": {"value_int_str": "11"}}, {"status": "GALACTIC_SHADOW", "n_star": {"value_int_str": "11"}}],
            [{"status": "TERRESTRIAL_CROSSOVER", "n_star": {"value_int_str": "10"}}, {"status": "GALACTIC_SHADOW", "n_star": {"value_int_str": "11"}}],
            [{"status": "TERRESTRIAL_CROSSOVER", "n_star": {"value_int_str": "11"}}, {"status": "WRONG", "n_star": {"value_int_str": "11"}}],
            [{"status": "TERRESTRIAL_CROSSOVER", "n_star": {"value_int_str": "11"}}, {"status": "GALACTIC_SHADOW", "n_star": {"value_int_str": "10"}}],
        ):
            with mock.patch.object(gsv, "detect_galactic_shadow", side_effect=side_b):
                self._assert_err("BOUNDARY_N11_FAIL", gsv._verify_exp_q60b_gate_and_lds)

        ok_mw = {
            "m1_sub_swap_killed_without_boundary": True,
            "m1_cmp_neg_killed_without_boundary": True,
            "m2_pairwise_masking_survives_without_boundary": True,
            "m2_pairwise_masking_killed_with_boundary": True,
        }
        for lds_ret, code in (
            ({"m1_kill_rate_q": "0/1", "m2_coupling_rate_q": "1/1", "m2_survivors": [], "m2_pairwise_masking_witness": ok_mw}, "LDS_M1_FAIL"),
            ({"m1_kill_rate_q": "1/1", "m2_coupling_rate_q": "0/1", "m2_survivors": [], "m2_pairwise_masking_witness": ok_mw}, "LDS_M2_FAIL"),
            ({"m1_kill_rate_q": "1/1", "m2_coupling_rate_q": "1/1", "m2_survivors": ["s"], "m2_pairwise_masking_witness": ok_mw}, "LDS_M2_FAIL"),
            ({"m1_kill_rate_q": "1/1", "m2_coupling_rate_q": "1/1", "m2_survivors": [], "m2_pairwise_masking_witness": dict(ok_mw, m1_sub_swap_killed_without_boundary=False)}, "LDS_MASKING_MISSING"),
            ({"m1_kill_rate_q": "1/1", "m2_coupling_rate_q": "1/1", "m2_survivors": [], "m2_pairwise_masking_witness": dict(ok_mw, m1_cmp_neg_killed_without_boundary=False)}, "LDS_MASKING_MISSING"),
            ({"m1_kill_rate_q": "1/1", "m2_coupling_rate_q": "1/1", "m2_survivors": [], "m2_pairwise_masking_witness": dict(ok_mw, m2_pairwise_masking_survives_without_boundary=False)}, "LDS_MASKING_MISSING"),
            ({"m1_kill_rate_q": "1/1", "m2_coupling_rate_q": "1/1", "m2_survivors": [], "m2_pairwise_masking_witness": dict(ok_mw, m2_pairwise_masking_killed_with_boundary=False)}, "LDS_MASKING_MISSING"),
        ):
            with mock.patch.object(gsv, "run_lipton_demillo_sayward_coupling", return_value=lds_ret):
                self._assert_err(code, gsv._verify_exp_q60b_gate_and_lds)

        lds = gsv.run_lipton_demillo_sayward_coupling()
        self.assertEqual(lds["m1_kill_rate_q"], "1/1")
        self.assertEqual(lds["m2_coupling_rate_q"], "1/1")
        self.assertEqual(lds["m2_survivors"], [])
        self.assertEqual(lds["m2_pairwise_masking_witness"], ok_mw)
        self._assert_err("LDS_BASELINE_FAIL", lambda: gsv.run_lipton_demillo_sayward_coupling("x = 1\n"))
        self._assert_err("LDS_BASELINE_FAIL", lambda: gsv.run_lipton_demillo_sayward_coupling("def gate_kernel(*a):\n    return 'WRONG'\n"))
        self._assert_err("LDS_AST_UNSUPPORTED", lambda: gsv._eval_ast_expr(ast.parse("1 + 2", mode="eval").body, {}))
        # LOW-6: unknown cmpop must fail closed instead of falling back to != (kills M217)
        self._assert_err("LDS_AST_UNSUPPORTED", lambda: gsv._eval_ast_expr(ast.parse("1 is not 2", mode="eval").body, {}))
        # LOW-4 (Delta-2): fail-closed LDS helpers & non-Return If bodies / unknown statements
        def _fn(src: str) -> ast.FunctionDef:
            node = ast.parse(src).body[0]
            self.assertIsInstance(node, ast.FunctionDef)
            return node  # type: ignore[return-value]
        self._assert_err("LDS_AST_UNSUPPORTED", lambda: gsv._eval_gate_kernel_ast(_fn("def g(a):\n    if a:\n        x = 1\n    return 2\n"), (True,)))
        self._assert_err("LDS_AST_UNSUPPORTED", lambda: gsv._eval_gate_kernel_ast(_fn("def g(a):\n    if a:\n        return 1\n    else:\n        return 3\n"), (False,)))
        self._assert_err("LDS_AST_UNSUPPORTED", lambda: gsv._eval_gate_kernel_ast(_fn("def g(a):\n    pass\n"), (True,)))
        self.assertEqual(gsv._eval_gate_kernel_ast(_fn("def g(a):\n    if a:\n        return 1\n    return 2\n"), (False,)), 2)
        self._assert_err("LDS_AST_UNSUPPORTED", lambda: gsv._lds_apply_sub_swap(ast.parse("x = 1\n")))
        self._assert_err("LDS_AST_UNSUPPORTED", lambda: gsv._lds_apply_sub_swap(ast.parse("")))
        self._assert_err("LDS_AST_UNSUPPORTED", lambda: gsv._lds_apply_cmp_neg(ast.parse("x = 1\n")))
        self._assert_err("LDS_AST_UNSUPPORTED", lambda: gsv._lds_apply_cmp_neg(ast.parse("def f(a):\n    gap = a - 1\n    if gap >= 0:\n        return 1\n    return 2\n")))

    def test_05_certificate_roundtrip_ro_safe_forgeries_and_cli(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            tp = Path(td)
            _write_clean_bundle(tp)
            cert_p = tp.joinpath("s174_stage2_certificate.json")

            # Static write + check roundtrip
            static_cert = gsv.build_certificate(tp, live_lean=False, aletheia_root=None)
            gsv.atomic_write_nofollow(cert_p, gsv._canon_bytes(static_cert))
            verified = gsv.verify_certificate_file(cert_p, tp, live_lean=False)
            self.assertEqual(verified["lean_bundle"]["lean_live_mode"], "STATIC_ONLY")
            self.assertFalse(verified["lean_bundle"]["live_lean_checked"])
            self.assertEqual(verified["exp_q60a"]["aletheia_calculus_parity"]["mode"], "SELF_CONTAINED_EXACT")
            self.assertEqual(verified["exp_q60a"]["portfolio_total"], 15)
            self.assertEqual(verified["queue_id"], "EXP-Q60a+EXP-Q60b")

            # Structural cert shape & live/static forgery checks
            for bad_bytes, err_code in (
                (b"[]\n", "CERT_NOT_DICT"),
                (b"{}\n", "CERT_MISMATCH"),
                (b'{"lean_bundle":{}}\n', "CERT_MISMATCH"),
                (b'{"lean_bundle":[],"exp_q60a":{"aletheia_calculus_parity":{"live_checked":false,"mode":"SELF_CONTAINED_EXACT"}}}\n', "CERT_MISMATCH"),
            ):
                gsv.atomic_write_nofollow(cert_p, bad_bytes)
                self._assert_err(err_code, lambda: gsv.verify_certificate_file(cert_p, tp, live_lean=False))

            # Offline forgery rejection: LIVE_LEAN_4_36_0_PASS (flag or mode alone)
            for fl_flag, fl_mode in ((True, "LIVE_LEAN_4_36_0_PASS"), (False, "LIVE_LEAN_4_36_0_PASS"), (True, "STATIC_ONLY")):
                forged_lean = json.loads(gsv._canon_bytes(static_cert).decode("utf-8"))
                forged_lean["lean_bundle"]["live_lean_checked"] = fl_flag
                forged_lean["lean_bundle"]["lean_live_mode"] = fl_mode
                gsv.atomic_write_nofollow(cert_p, gsv._canon_bytes(forged_lean))
                self._assert_err("LEAN_LIVE_STATUS_MISMATCH", lambda: gsv.verify_certificate_file(cert_p, tp, live_lean=False))

            # Offline forgery rejection: LIVE_ALETHEIA_CALCULUS_PASS (flag or mode alone)
            for fa_flag, fa_mode in ((True, "LIVE_ALETHEIA_CALCULUS_PASS"), (False, "LIVE_ALETHEIA_CALCULUS_PASS"), (True, "SELF_CONTAINED_EXACT")):
                forged_ale = json.loads(gsv._canon_bytes(static_cert).decode("utf-8"))
                forged_ale["exp_q60a"]["aletheia_calculus_parity"]["live_checked"] = fa_flag
                forged_ale["exp_q60a"]["aletheia_calculus_parity"]["mode"] = fa_mode
                gsv.atomic_write_nofollow(cert_p, gsv._canon_bytes(forged_ale))
                self._assert_err("ALETHEIA_LIVE_STATUS_MISMATCH", lambda: gsv.verify_certificate_file(cert_p, tp, live_lean=False))

            # Bool-for-int spoof rejection & non-canonical bytes rejection
            forged_bool = json.loads(gsv._canon_bytes(static_cert).decode("utf-8"))
            forged_bool["weights_inside_expedition"] = False
            gsv.atomic_write_nofollow(cert_p, gsv._canon_bytes(forged_bool))
            self._assert_err("CERT_MISMATCH", lambda: gsv.verify_certificate_file(cert_p, tp, live_lean=False))

            gsv.atomic_write_nofollow(cert_p, gsv._canon_bytes(static_cert) + b" \n")
            self._assert_err("CERT_NON_CANONICAL", lambda: gsv.verify_certificate_file(cert_p, tp, live_lean=False))

            # Live mocked Lean + fake aletheia roundtrip + live failure paths
            fake_ale = tp.joinpath("fake_ale")
            _write_fake_aletheia_pkg(fake_ale)
            live_cert = gsv.build_certificate(tp, live_lean=True, aletheia_root=fake_ale, runner=_mock_lean_runner())
            sys.modules.pop("aletheia.calculus", None)
            sys.modules.pop("aletheia", None)
            gsv.atomic_write_nofollow(cert_p, gsv._canon_bytes(live_cert))
            v_live = gsv.verify_certificate_file(cert_p, tp, live_lean=True, aletheia_root=fake_ale, runner=_mock_lean_runner())
            sys.modules.pop("aletheia.calculus", None)
            sys.modules.pop("aletheia", None)
            self.assertTrue(v_live["lean_bundle"]["live_lean_checked"])
            self.assertTrue(v_live["exp_q60a"]["aletheia_calculus_parity"]["live_checked"])

            # Partial / tampered / non-canonical live cert checks
            part_lean = json.loads(gsv._canon_bytes(live_cert).decode("utf-8"))
            part_lean["lean_bundle"]["live_lean_checked"] = False
            gsv.atomic_write_nofollow(cert_p, gsv._canon_bytes(part_lean))
            self._assert_err("LEAN_LIVE_STATUS_MISMATCH", lambda: gsv.verify_certificate_file(cert_p, tp, live_lean=True, aletheia_root=fake_ale, runner=_mock_lean_runner()))
            sys.modules.pop("aletheia.calculus", None)
            sys.modules.pop("aletheia", None)

            part_ale = json.loads(gsv._canon_bytes(live_cert).decode("utf-8"))
            part_ale["exp_q60a"]["aletheia_calculus_parity"]["live_checked"] = False
            gsv.atomic_write_nofollow(cert_p, gsv._canon_bytes(part_ale))
            self._assert_err("ALETHEIA_LIVE_STATUS_MISMATCH", lambda: gsv.verify_certificate_file(cert_p, tp, live_lean=True, aletheia_root=fake_ale, runner=_mock_lean_runner()))
            sys.modules.pop("aletheia.calculus", None)
            sys.modules.pop("aletheia", None)

            bad_live = json.loads(gsv._canon_bytes(live_cert).decode("utf-8"))
            bad_live["weights_inside_expedition"] = 1
            gsv.atomic_write_nofollow(cert_p, gsv._canon_bytes(bad_live))
            self._assert_err("CERT_MISMATCH", lambda: gsv.verify_certificate_file(cert_p, tp, live_lean=True, aletheia_root=fake_ale, runner=_mock_lean_runner()))
            sys.modules.pop("aletheia.calculus", None)
            sys.modules.pop("aletheia", None)

            gsv.atomic_write_nofollow(cert_p, gsv._canon_bytes(live_cert) + b" \n")
            self._assert_err("CERT_NON_CANONICAL", lambda: gsv.verify_certificate_file(cert_p, tp, live_lean=True, aletheia_root=fake_ale, runner=_mock_lean_runner()))
            sys.modules.pop("aletheia.calculus", None)
            sys.modules.pop("aletheia", None)

            # Static cert checked under --live-lean OR --aletheia-root passes & rejects bad bytes
            gsv.atomic_write_nofollow(cert_p, gsv._canon_bytes(static_cert))
            v_both = gsv.verify_certificate_file(cert_p, tp, live_lean=True, runner=_mock_lean_runner())
            self.assertEqual(v_both["lean_bundle"]["lean_live_mode"], "LIVE_LEAN_4_36_0_PASS")
            v_ale_only = gsv.verify_certificate_file(cert_p, tp, live_lean=False, aletheia_root=fake_ale)
            sys.modules.pop("aletheia.calculus", None)
            sys.modules.pop("aletheia", None)
            self.assertEqual(v_ale_only["exp_q60a"]["aletheia_calculus_parity"]["mode"], "LIVE_ALETHEIA_CALCULUS_PASS")

            tampered_static = json.loads(gsv._canon_bytes(static_cert).decode("utf-8"))
            tampered_static["weights_inside_expedition"] = 1
            gsv.atomic_write_nofollow(cert_p, gsv._canon_bytes(tampered_static))
            self._assert_err("CERT_MISMATCH", lambda: gsv.verify_certificate_file(cert_p, tp, live_lean=True, runner=_mock_lean_runner()))
            gsv.atomic_write_nofollow(cert_p, gsv._canon_bytes(static_cert) + b" \n")
            self._assert_err("CERT_NON_CANONICAL", lambda: gsv.verify_certificate_file(cert_p, tp, live_lean=True, runner=_mock_lean_runner()))

            # CLI tests (JSON help RC=0, standalone RC=0, write RC=0, check RC=0, abbrev & removed --json rejected RC=2)
            for argv, exp_rc in (
                (["--help"], 0),
                (["--track-dir", os.fspath(tp), "--standalone"], 0),
                (["--track-dir", os.fspath(tp), "--write", os.fspath(cert_p)], 0),
                (["--track-dir", os.fspath(tp), "--check", os.fspath(cert_p)], 0),
                (["--stan"], 2),
                (["--json"], 2),
                (["--track-dir", os.fspath(tp), "--check", os.fspath(tp.joinpath("missing.json"))], 2),
            ):
                out_s, err_s = io.StringIO(), io.StringIO()
                with redirect_stdout(out_s), redirect_stderr(err_s):
                    rc = gsv.main(argv)
                self.assertEqual(rc, exp_rc, f"CLI {argv} stderr={err_s.getvalue()}")


if __name__ == "__main__":
    unittest.main()
