#!/usr/bin/env python3
"""Assertion-free, float-free, log-free standalone test suite for verify_periodic_table_invariants.py.

Exercises every boundary condition, fail-closed refusal path, forged-witness rejection,
and boolean condition, and unconditionally validates committed JSON artifacts against
live verifier output. Emits 0 stdout bytes on PASS across -I -B, -I -O -B, and -I -B -W error.
"""

from __future__ import annotations

import copy
import io
import json
import sys
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


def check_raises_val(fn: Callable[[], Any], label: str, match: str | None = None) -> None:
    raised = False
    text = ""
    try:
        fn()
    except ValueError as exc:
        raised = True
        text = str(exc)
    if not raised:
        fail(f"Expected ValueError for {label}")
    if match is not None and match not in text:
        fail(f"Message mismatch for {label}: expected {match!r} in {text!r}")


def test_primitives_and_boundaries() -> None:
    check(ptv.check_source_zero_floats_and_logs(Path(ptv.__file__).resolve()) == 0, "Target AST has floats/logs")
    check(ptv.check_source_zero_floats_and_logs(Path(__file__).resolve()) == 0, "Test AST has floats/logs")

    # is_hex64 exact validation
    check(ptv.is_hex64("0123456789abcdef" * 4) is True, "valid 64-hex rejected")
    check(ptv.is_hex64(123) is False, "non-str accepted by is_hex64")
    check(ptv.is_hex64("0" * 63) is False, "63-hex accepted by is_hex64")
    check(ptv.is_hex64("g" + "0" * 63) is False, "non-hex accepted by is_hex64")

    k1, b1 = ptv.cancellation_kappa_q(Fraction(1, 2))
    check(k1 == ptv.ONE and b1 == 0, "kappa(1/2) != (1, 0)")
    k0, b0 = ptv.cancellation_kappa_q(Fraction(1, 3))
    check(k0 == Fraction(1, 2) and b0 == 0, "kappa(1/3) != (1/2, 0)")
    check_raises_val(lambda: ptv.cancellation_kappa_q(ptv.ZERO), "kappa x=0", "x must be > 0")
    check_raises_val(lambda: ptv.cancellation_kappa_q(ptv.ONE), "kappa x=1", "x must be < 1")

    check(ptv.solve_noncoprime_crt(((0, 1),)) == (0, 1), "crt((0,1)) != (0,1)")
    check(ptv.solve_noncoprime_crt(((1, 2), (1, 1))) == (1, 2), "crt second mod=1 failed")
    check_raises_val(lambda: ptv.solve_noncoprime_crt(()), "crt empty", "non-empty")
    check_raises_val(lambda: ptv.solve_noncoprime_crt(((0, 0),)), "crt m0=0", "modulus must be >= 1")
    check_raises_val(lambda: ptv.solve_noncoprime_crt(((0, 2), (0, 0))), "crt mi=0", "modulus must be >= 1")
    check_raises_val(lambda: ptv.solve_noncoprime_crt(((0, 4), (1, 6))), "crt inconsistent", "Inconsistent")

    check(ptv.q_cayley_axis(ptv.ZERO, 3) == (ptv.ONE, ptv.ZERO, ptv.ZERO, ptv.ZERO), "cayley axis 3 zero")
    check_raises_val(lambda: ptv.q_cayley_axis(ptv.ZERO, 0), "cayley axis 0", "axis must be in")
    check_raises_val(lambda: ptv.q_cayley_axis(ptv.ZERO, 4), "cayley axis 4", "axis must be in")

    check(ptv.sona_loop_count_with_wall(1, 1, split_wall=False) == 1, "sona(1,1) != 1")
    check(ptv.sona_loop_count_with_wall(2, 1, split_wall=True) == 2, "sona(2,1,wall) != 2")
    check_raises_val(lambda: ptv.sona_loop_count_with_wall(0, 1, split_wall=False), "sona m=0", "m must be >= 1")
    check_raises_val(lambda: ptv.sona_loop_count_with_wall(1, 0, split_wall=False), "sona n=0", "n must be >= 1")
    check_raises_val(lambda: ptv.sona_loop_count_with_wall(1, 2, split_wall=True), "sona wall m=1", "m >= 2")

    # schur_3x3_elim_last shape and pivot rejections
    check_raises_val(lambda: ptv.schur_3x3_elim_last(((ptv.ONE,),)), "schur 1x1", "exactly 3 rows")
    check_raises_val(
        lambda: ptv.schur_3x3_elim_last(((ptv.ONE, ptv.ZERO), (ptv.ZERO, ptv.ONE), (ptv.ZERO, ptv.ZERO))),
        "schur 3x2",
        "exactly 3 columns",
    )
    bad_mat = (
        (ptv.ONE, ptv.ZERO, ptv.ZERO),
        (ptv.ZERO, ptv.ONE, ptv.ZERO),
        (ptv.ZERO, ptv.ZERO, ptv.ZERO),
    )
    check_raises_val(lambda: ptv.schur_3x3_elim_last(bad_mat), "schur pivot=0", "strictly positive")


def test_certificate_and_periodic_table_tampers() -> None:
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

    buf_chk = io.StringIO()
    with redirect_stdout(buf_chk):
        rc_chk = ptv.main(["--check"])
    check(
        rc_chk == 0 and f"PASS CONTINUUM_PERIODIC_TABLE_INVARIANTS result_sha256={cert['result_sha256']}" in buf_chk.getvalue(),
        "CLI --check failed",
    )

    buf_sum = io.StringIO()
    with redirect_stdout(buf_sum):
        rc_sum = ptv.main([])
    check(rc_sum == 0 and cert["result_sha256"] in buf_sum.getvalue(), "CLI summary failed")

    # Mutually exclusive CLI flags rejected fail-closed
    mux_exited = False
    mux_err = io.StringIO()
    with redirect_stderr(mux_err):
        try:
            ptv.main(["--json", "--check"])
        except SystemExit as exc:
            mux_exited = exc.code != 0
    check(mux_exited, "CLI mutually exclusive flags were not rejected")

    # Unconditionally validate committed JSON files match live output exactly
    here = Path(__file__).resolve().parent
    cert_file = here / "periodic_table_certificate.json"
    pt_file = here / "periodic_table_of_invariants.json"
    check(cert_file.is_file(), "Missing committed periodic_table_certificate.json")
    check(pt_file.is_file(), "Missing committed periodic_table_of_invariants.json")
    disk_cert = json.loads(cert_file.read_text(encoding="utf-8"))
    ptv.validate_certificate(disk_cert)
    check(disk_cert == cert, "Committed certificate differs from live output")
    disk_pt = json.loads(pt_file.read_text(encoding="utf-8"))
    ptv.validate_periodic_table(disk_pt)
    check(disk_pt == table, "Committed periodic table differs from live output")

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
    tamper_cert(lambda d: d.__setitem__("ast_float_and_log_count", 1), "cert_ast", "AST must contain zero floats")

    def _set_pair(sec: str, tot_k: str, ok_k: str, val: int) -> Callable[[dict[str, Any]], None]:
        def _fn(d: dict[str, Any]) -> None:
            d[sec][tot_k] = val
            d[sec][ok_k] = val
        return _fn

    tamper_cert(_set_pair("four_class_obstructions", "class_a_diophantine_checks_total", "class_a_diophantine_checks_ok", 8), "h1_a_tot", "Expected 9 Class-A checks")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_a_diophantine_checks_ok", 8), "h1_a_ok", "Class-A check mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_a_zu_beats_22_7_floor", 999999), "forged_zu", "Zu Chongzhi floor witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_a_antikythera_beat_9_times_53", 476), "forged_beat", "Antikythera beat witness mismatch")
    tamper_cert(_set_pair("four_class_obstructions", "class_b_cancellation_checks_total", "class_b_cancellation_checks_ok", 7), "h1_b_tot", "Expected 8 Class-B checks")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_b_cancellation_checks_ok", 7), "h1_b_ok", "Class-B check mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_b_biruni_kappa", "1/1"), "forged_kappa", "Al-Biruni kappa witness mismatch")
    tamper_cert(_set_pair("four_class_obstructions", "class_c_topological_checks_total", "class_c_topological_checks_ok", 8), "h1_c_tot", "Expected 9 Class-C checks")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_c_topological_checks_ok", 8), "h1_c_ok", "Class-C check mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_c_sona_loops_3x5_4x6_2x2_wall", [1, 1, 1, 1]), "forged_sona", "Sona loop witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_c_tucker_c3_single_copy_orders", 1), "forged_tucker", "Tucker C_3 witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_c_z2_twisted_vs_untwisted_sections", [1, 2]), "forged_z2", "Z_2 sheaf section witness mismatch")
    tamper_cert(_set_pair("four_class_obstructions", "class_d_commutation_checks_total", "class_d_commutation_checks_ok", 6), "h1_d_tot", "Expected 7 Class-D checks")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_d_commutation_checks_ok", 6), "h1_d_ok", "Class-D check mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_d_schur_det_unreadable_to_readable", ["1", "1"]), "forged_schur_det", "Schur det witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_d_schur_trace_drop", "0"), "forged_trace_drop", "Schur trace drop witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_d_markov_lumpability_defects", ["0", "0"]), "forged_markov", "Markov lumpability witness mismatch")
    tamper_cert(lambda d: d["four_class_obstructions"].__setitem__("class_d_trotter_defect_eps_1_4", "0"), "forged_trotter", "Trotter defect witness mismatch")

    tamper_cert(_set_pair("opposing_pair_conservation", "opposing_pair_checks_total", "opposing_pair_checks_ok", 12), "h2_tot", "Expected 13 opposing-pair checks")
    tamper_cert(lambda d: d["opposing_pair_conservation"].__setitem__("opposing_pair_checks_ok", 12), "h2_ok", "Opposing-pair check mismatch")
    tamper_cert(lambda d: d["opposing_pair_conservation"]["abelian_zero_residual_witnesses"].__setitem__("al_tusi_planar_curl", "1"), "forged_abelian", "Abelian zero-residual witnesses mismatch")
    tamper_cert(lambda d: d["opposing_pair_conservation"]["nonabelian_or_dissipative_nonzero_witnesses"].__setitem__("dougong_pi_zeta", "0"), "forged_nonabelian", "Non-Abelian or dissipative witnesses mismatch")

    tamper_cert(_set_pair("modular_flow_and_partition", "modular_flow_checks_total", "modular_flow_checks_ok", 14), "h3_tot", "Expected 15 modular-flow checks")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("modular_flow_checks_ok", 14), "h3_ok", "Modular-flow check mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("maya_crt_solution_mod_37960", 1), "forged_maya_x", "Maya CRT witness mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("maya_grand_sync_lcm", 1), "forged_maya_lcm", "Maya grand sync LCM mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("maya_phase_compression_ratio", 1), "forged_maya_comp", "Maya phase compression mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("maya_dresden_eclipse_ratio", "1/1"), "forged_dresden", "Maya Dresden ratio mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("inconsistent_crt_refused", False), "h3_crt_refused", "Inconsistent CRT must be refused")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("antikythera_metonic_ratio", "1/1"), "forged_metonic", "Antikythera Metonic ratio mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("antikythera_anomalistic_rate", "1/1"), "forged_anom", "Antikythera anomalistic rate mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("two_clock_record_shift_delta_beta2", "0"), "forged_beta2", "Two-clock shift mismatch")
    tamper_cert(lambda d: d["modular_flow_and_partition"].__setitem__("panini_c1p_descriptor_ratio", "1/1"), "forged_panini", "Panini descriptor ratio mismatch")

    tamper_cert(lambda d: d["periodic_table_summary"].__setitem__("schema_version", "bad"), "pts_schema", "Periodic table schema mismatch")
    tamper_cert(lambda d: d["periodic_table_summary"].__setitem__("entry_count", 15), "pts_entries", "Expected 16 periodic table entries")
    tamper_cert(lambda d: d["periodic_table_summary"].__setitem__("family_count", 4), "pts_families", "Expected 5 morphological families")
    tamper_cert(lambda d: d["periodic_table_summary"].__setitem__("provenance_count", 9), "pts_prov", "Expected 10 provenance digests")
    tamper_cert(lambda d: d["periodic_table_summary"].__setitem__("periodic_table_sha256", "0" * 63), "pts_63hex", "Periodic table SHA-256 must be 64-hex")
    tamper_cert(
        lambda d: d["periodic_table_summary"].__setitem__("periodic_table_sha256", "0" * 64),
        "pts_forged_sha64",
        "Certificate payload does not match recomputed build",
    )
    tamper_cert(
        lambda d: d.__setitem__("forged_extra_field", True),
        "cert_forged_extra",
        "Certificate payload does not match recomputed build",
    )

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
    tamper_pt(lambda d: d["provenance_digests"].__setitem__("south_asia_exact_operators_cert", "0" * 63), "pt_prov_63hex", "is not 64-hex")
    tamper_pt(lambda d: d["provenance_digests"].__setitem__("south_asia_exact_operators_cert", "0" * 64), "pt_prov_sha", "Provenance digests mismatch")

    # Forged entry tampers (with recomputed result_sha256)
    tamper_pt(lambda d: d["entries"][0].__setitem__("entry_id", "PT-02"), "pt_dup_id", "Duplicate entry_id")
    tamper_pt(lambda d: d["entries"][0].__setitem__("family", "BOGUS_FAMILY"), "pt_bad_fam", "Invalid family")
    tamper_pt(lambda d: d["entries"][0].__setitem__("obstruction_class", "BOGUS_CLASS"), "pt_bad_obs", "Invalid obstruction_class")
    tamper_pt(lambda d: d["entries"][0].__setitem__("morphism_grade", "BOGUS_GRADE"), "pt_bad_grade", "Invalid morphism_grade")
    tamper_pt(lambda d: d["entries"][0].__setitem__("provenance_key", "unknown_key"), "pt_bad_pkey", "Unknown provenance_key")
    tamper_pt(lambda d: d["entries"][0].__setitem__("provenance_sha256", "0" * 63), "pt_entry_63hex", "Entry provenance_sha256 must be 64-hex")
    tamper_pt(lambda d: d["entries"][0].__setitem__("provenance_sha256", "0" * 64), "pt_entry_wrong_sha", "Entry provenance_sha256 does not match registry")
    tamper_pt(lambda d: d["entries"][0].__setitem__("exact_witness", "   "), "pt_empty_witness", "Empty exact_witness")

    # Drop all entries of one family (replace 2 SUBTRACTIVE entries with DIOPHANTINE) to test family coverage guard
    def _drop_family(d: dict[str, Any]) -> None:
        for row in d["entries"]:
            if row["family"] == "SUBTRACTIVE_CANCELLATION_WALL":
                row["family"] = "DIOPHANTINE_RESONANCE_LATTICE"

    tamper_pt(_drop_family, "pt_missing_family_coverage", "Entries do not cover all 5 families")

    # Forged prose / witness text with valid schema and recomputed result_sha256 rejected by recomputed-build equality
    tamper_pt(
        lambda d: d["entries"][0].__setitem__("exact_witness", "FORGED_WITNESS_TEXT"),
        "pt_forged_witness_text",
        "Periodic table payload does not match recomputed build",
    )
    tamper_pt(
        lambda d: d.__setitem__("continuum_scope", "FORGED_SCOPE"),
        "pt_forged_scope",
        "Periodic table payload does not match recomputed build",
    )


def main() -> int:
    test_primitives_and_boundaries()
    test_certificate_and_periodic_table_tampers()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
