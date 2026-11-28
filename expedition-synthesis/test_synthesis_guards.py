#!/usr/bin/env python3
"""Must-fail guard tests for the synthesis instruments, in the style of test_double_slit_r5.py."""
from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path

_HERE = str(Path(__file__).resolve().parent)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import fold_sheaf_collapse as fold
import optimal_inertia_rank as inertia
import portal78_homotopy_bregman_bridge as portal
import two_loop_omitted_variable as two_loop


class TwoLoopGuardTests(unittest.TestCase):
    def test_pythagorean_inflation_accepts_the_identity_and_rejects_a_broken_residual(self) -> None:
        r_star = [Fraction(0), Fraction(0), Fraction(5), Fraction(0), Fraction(0), Fraction(0)]
        e1, p1_n2 = Fraction(5), Fraction(1)
        r_adapt = [Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
        # ||r_adapt||^2 = 0, ||r_star||^2 + e1^2/p1_n2 = 25 + 25 = 50, so this must fail
        with self.assertRaises(RuntimeError):
            two_loop.check_pythagorean_inflation(r_adapt, r_star, e1, p1_n2)
        r_ok = [Fraction(5), Fraction(5), Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
        two_loop.check_pythagorean_inflation(r_ok, r_star, e1, p1_n2)

    def test_phase_boundary_iff_rejects_a_swapped_predicate(self) -> None:
        # 0 < ratio < 2 should shrink the residual; a growing residual must fail
        with self.assertRaises(RuntimeError):
            two_loop.check_phase_boundary_iff(Fraction(10), Fraction(5), Fraction(1))
        two_loop.check_phase_boundary_iff(Fraction(0), Fraction(5), Fraction(1))
        two_loop.check_phase_boundary_iff(Fraction(10), Fraction(5), Fraction(3))
        with self.assertRaises(RuntimeError):
            two_loop.check_phase_boundary_iff(Fraction(0), Fraction(5), Fraction(3))


class EntropyHierarchyGuardTests(unittest.TestCase):
    def test_exact_hierarchy_holds_on_the_instrument_spectra_and_rejects_empty(self) -> None:
        spectra = [
            [Fraction(9, 10), Fraction(1, 20), Fraction(1, 20), Fraction(0)],
            [Fraction(1, 3), Fraction(1, 3), Fraction(1, 3), Fraction(0)],
            [Fraction(6404, 10000) ** 2, Fraction(3596, 10000) ** 2, Fraction(0)],
        ]
        for eigs in spectra:
            self.assertTrue(inertia.entropy_hierarchy_holds(eigs))
            inertia.check_entropy_hierarchy(eigs, "ok")
        self.assertFalse(inertia.entropy_hierarchy_holds([Fraction(0), Fraction(0)]))
        with self.assertRaises(RuntimeError):
            inertia.check_entropy_hierarchy([Fraction(0), Fraction(0)], "empty")


class BregmanGuardTests(unittest.TestCase):
    def test_pythagoras_accepts_a_split_and_rejects_a_broken_sum(self) -> None:
        mid, right = Fraction(6), Fraction(10)
        portal.check_bregman_pythagoras(mid + right, mid, right, mode="inflation")
        with self.assertRaises(RuntimeError):
            portal.check_bregman_pythagoras(mid + right + 1, mid, right, mode="inflation")
        portal.check_bregman_pythagoras(mid - right, mid, right, mode="contraction")
        with self.assertRaises(RuntimeError):
            portal.check_bregman_pythagoras(mid, mid, right, mode="contraction")


class FoldGuardTests(unittest.TestCase):
    def test_symmetrizer_accepts_the_cycle_and_rejects_a_broken_sign(self) -> None:
        C3 = fold.make_twisted_cycle_Cn(3)
        self.assertTrue(fold.verify_diagonal_symmetrizer(C3, [-1, 1, 1]))
        self.assertFalse(fold.verify_diagonal_symmetrizer(C3, [1, 1, 1]))
        self.assertEqual(fold.rotational_locking_rank(C3), 2)


class ParserGuardTests(unittest.TestCase):
    def test_to_frac_rejects_noncanonical_and_float_inputs(self) -> None:
        self.assertEqual(inertia.to_frac("1/2"), Fraction(1, 2))
        for bad in ("007", "-0", "2/4", "0/5", "01/2", "3/1", "1_000", " 1", "１"):
            with self.subTest(bad=bad):
                with self.assertRaises((ValueError, TypeError)):
                    inertia.to_frac(bad)
        with self.assertRaises((ValueError, TypeError)):
            inertia.to_frac(1.5)
        with self.assertRaises((ValueError, TypeError)):
            inertia.to_frac(True)


if __name__ == "__main__":
    unittest.main()
