/-
Track S174 (`EXP-Q60a/b`): Pure-Init Lean 4.36.0 Formalization of Galactic
Crossover-Horizon N*, `⧅` Dark-Mode Shadow & Moore-Penrose `⧄` Schur Pushforward,
Reciprocal Scale-Inversion Duality `CS-09 <-> CS-Galactic` (`u = 1/N`),
Constructive Crossovers (incl. Karatsuba `[257, 279]` & Portal 220 `sssp-lean`),
& 2nd-Order LDS Fault-Masking Coupling.
Zero imports (pure `Init`), zero `sorry`/`axiom`/`native_decide`/`stop`/`Classical.choice`.
-/

namespace GalacticShadow

def IsCrossoverHorizon (P : Nat → Prop) (nStar : Nat) : Prop :=
  1 ≤ nStar ∧ (∀ n, 1 ≤ n → n < nStar → ¬ P n) ∧ (∀ n, nStar ≤ n → P n)

/-- Theorem 1: Uniqueness of the crossover horizon N*. -/
theorem crossover_horizon_unique (P : Nat → Prop) (n1 n2 : Nat)
    (h1 : IsCrossoverHorizon P n1) (h2 : IsCrossoverHorizon P n2) : n1 = n2 := by
  rcases Nat.lt_trichotomy n1 n2 with hlt | heq | hgt
  · exact absurd (h1.2.2 n1 (Nat.le_refl n1)) (h2.2.1 n1 h1.1 hlt)
  · exact heq
  · exact absurd (h2.2.2 n2 (Nat.le_refl n2)) (h1.2.1 n2 h2.1 hgt)

/-- Theorem 2: Strict monotonicity & exact closed-form affine crossover N* = (fa - fb) / (sb - sa) + 1. -/
theorem affine_crossover_monotone_and_exact (fa sa fb sb : Nat)
    (hs : sa < sb) (hf : fb ≤ fa) :
    (∀ n1 n2, n1 ≤ n2 → fa + sa * n1 < fb + sb * n1 → fa + sa * n2 < fb + sb * n2) ∧
    IsCrossoverHorizon (fun n => fa + sa * n < fb + sb * n) ((fa - fb) / (sb - sa) + 1) := by
  have hmono : ∀ n1 n2, n1 ≤ n2 → fa + sa * n1 < fb + sb * n1 → fa + sa * n2 < fb + sb * n2 := by
    intro n1 n2 hle hlt
    have hsa : sa * (n2 - n1) ≤ sb * (n2 - n1) := Nat.mul_le_mul_right (n2 - n1) (Nat.le_of_lt hs)
    have he1 : n2 = n1 + (n2 - n1) := (Nat.add_sub_cancel' hle).symm
    rw [he1, Nat.mul_add, Nat.mul_add]; omega
  refine ⟨hmono, Nat.succ_pos _, ?_, ?_⟩
  · intro n _ hlt hcost
    have hle_div : n ≤ (fa - fb) / (sb - sa) := Nat.le_of_lt_succ hlt
    have hmul : (sb - sa) * n ≤ (sb - sa) * ((fa - fb) / (sb - sa)) :=
      Nat.mul_le_mul_left (sb - sa) hle_div
    have hdm := Nat.div_add_mod (fa - fb) (sb - sa)
    have hsub : (sb - sa) * n = sb * n - sa * n := Nat.sub_mul sb sa n
    omega
  · intro n hge
    have hmod : (fa - fb) % (sb - sa) < sb - sa := Nat.mod_lt (fa - fb) (by omega)
    have hdm := Nat.div_add_mod (fa - fb) (sb - sa)
    have hmul : (sb - sa) * ((fa - fb) / (sb - sa) + 1) ≤ (sb - sa) * n :=
      Nat.mul_le_mul_left (sb - sa) hge
    have hexp : (sb - sa) * ((fa - fb) / (sb - sa) + 1) =
        (sb - sa) * ((fa - fb) / (sb - sa)) + (sb - sa) := by simp [Nat.mul_add]
    have hsub : (sb - sa) * n = sb * n - sa * n := Nat.sub_mul sb sa n
    omega

/-- Theorem 3: Galactic Shadow vs Terrestrial Crossover dichotomy on [1, nPhys]. -/
theorem galactic_vs_terrestrial_dichotomy (P : Nat → Prop) (nStar nPhys : Nat)
    (hstar : IsCrossoverHorizon P nStar) (hphys : 1 ≤ nPhys) :
    (nPhys < nStar → ∀ n, 1 ≤ n → n ≤ nPhys → ¬ P n) ∧
    (nStar ≤ nPhys → P nPhys ∧ ∃ n, 1 ≤ n ∧ n ≤ nPhys ∧ P n) :=
  ⟨fun hlt n hn1 hnle => hstar.2.1 n hn1 (Nat.lt_of_le_of_lt hnle hlt),
   fun hle => ⟨hstar.2.2 nPhys hle, nPhys, hphys, Nat.le_refl nPhys, hstar.2.2 nPhys hle⟩⟩

structure PosRat where
  num : Nat
  den : Nat
  hnum : 0 < num
  hden : 0 < den

def PosRat.lt (a b : PosRat) : Prop := a.num * b.den < b.num * a.den

def PosRat.inv (a : PosRat) : PosRat := ⟨a.den, a.num, a.hden, a.hnum⟩

def PosRat.unitRecip (n : Nat) (hn : 0 < n) : PosRat := ⟨1, n, Nat.zero_lt_one, hn⟩

/-- Theorem 4: Exact reciprocal order-reversal duality `u = 1/N` between `CS-09` and `CS-Galactic` in exact Q_+. -/
theorem scale_inversion_cs09_galactic_dual (q1 q2 : PosRat) (c M Ncrit Nphys Nstar : Nat)
    (hc : 0 < c) (hM : 0 < M) (hNc : 0 < Ncrit) (hNp : 0 < Nphys) (hNs : 0 < Nstar) :
    (q1.inv.inv = q1) ∧
    (PosRat.lt q2.inv q1.inv ↔ PosRat.lt q1 q2) ∧
    (PosRat.lt (PosRat.unitRecip Ncrit hNc) (PosRat.unitRecip M hM) ↔ M < Ncrit) ∧
    (PosRat.lt (PosRat.unitRecip Nstar hNs) (PosRat.unitRecip Nphys hNp) ↔ Nphys < Nstar) ∧
    ((c * M < c * Ncrit ↔ M < Ncrit) ∧ (c * Nphys < c * Nstar ↔ Nphys < Nstar)) := by
  refine ⟨rfl, ?_, ?_, ?_, ⟨?_, ?_⟩⟩
  · constructor
    · intro h
      dsimp [PosRat.lt, PosRat.inv] at h ⊢
      rw [Nat.mul_comm q1.num q2.den, Nat.mul_comm q2.num q1.den]
      exact h
    · intro h
      dsimp [PosRat.lt, PosRat.inv] at h ⊢
      rw [Nat.mul_comm q2.den q1.num, Nat.mul_comm q1.den q2.num]
      exact h
  · constructor
    · intro h; dsimp [PosRat.lt, PosRat.unitRecip] at h; rw [Nat.one_mul, Nat.one_mul] at h; exact h
    · intro h; dsimp [PosRat.lt, PosRat.unitRecip]; rw [Nat.one_mul, Nat.one_mul]; exact h
  · constructor
    · intro h; dsimp [PosRat.lt, PosRat.unitRecip] at h; rw [Nat.one_mul, Nat.one_mul] at h; exact h
    · intro h; dsimp [PosRat.lt, PosRat.unitRecip]; rw [Nat.one_mul, Nat.one_mul]; exact h
  · constructor
    · intro h
      rcases Nat.lt_trichotomy M Ncrit with hlt | heq | hgt
      · exact hlt
      · subst heq; exact absurd h (Nat.lt_irrefl _)
      · exact absurd (Nat.lt_trans h (Nat.mul_lt_mul_of_pos_left hgt hc)) (Nat.lt_irrefl _)
    · intro h; exact Nat.mul_lt_mul_of_pos_left h hc
  · constructor
    · intro h
      rcases Nat.lt_trichotomy Nphys Nstar with hlt | heq | hgt
      · exact hlt
      · subst heq; exact absurd h (Nat.lt_irrefl _)
      · exact absurd (Nat.lt_trans h (Nat.mul_lt_mul_of_pos_left hgt hc)) (Nat.lt_irrefl _)
    · intro h; exact Nat.mul_lt_mul_of_pos_left h hc

/-- Theorem 5: Two-sided completeness gate characterizing simultaneous terrestrial crossover (N* <= N_phys) and tail-failure exposure (N_crit <= M_obs). -/
theorem two_sided_completeness_gate (P TailFail : Nat → Prop)
    (nStar nPhys mObs nCrit : Nat)
    (hstar : IsCrossoverHorizon P nStar)
    (hcrit_witness : TailFail nCrit)
    (hcrit_min : ∀ k, k < nCrit → ¬ TailFail k) :
    (nStar ≤ nPhys ∧ nCrit ≤ mObs) ↔
    ((∃ n, 1 ≤ n ∧ n ≤ nPhys ∧ P n) ∧ (∃ k, k ≤ mObs ∧ TailFail k)) := by
  constructor
  · intro ⟨h1, h2⟩
    exact ⟨⟨nStar, hstar.1, h1, hstar.2.2 nStar (Nat.le_refl nStar)⟩, ⟨nCrit, h2, hcrit_witness⟩⟩
  · intro ⟨⟨n, hn1, hnle, hPn⟩, ⟨k, hkle, hTk⟩⟩
    refine ⟨?_, ?_⟩
    · apply Nat.ge_of_not_lt
      intro hlt
      exact hstar.2.1 n hn1 (Nat.lt_of_le_of_lt hnle hlt) hPn
    · apply Nat.ge_of_not_lt
      intro hlt
      exact hcrit_min k (Nat.lt_of_le_of_lt hkle hlt) hTk

def muxHalfMarginDen (p q S : Nat) : Nat := 2 * (q ^ S - p ^ S)

/-- Theorem 6: Track S164 MUX Cor. 15 BF16 stall (S=3 pass, S=4 collapse) vs Al-Kashi exact Q (u=0 gives eta_S(0) = 0, so passing reduces to universal margin positivity 9^S < 10^S, i.e. 0 < muxHalfMarginDen 9 10 S, for all S >= 1). -/
theorem mux_cs09_vs_alkashi_exact_witness :
    (muxHalfMarginDen 9 10 3 = 542 ∧ 3 * 542 < 9 * 254) ∧
    (muxHalfMarginDen 9 10 4 = 6878 ∧ 19 * 362 = 6878 ∧ 19 * 253 < 4 * 6878) ∧
    (∀ S : Nat, 1 ≤ S → 9 ^ S < 10 ^ S ∧ 0 < muxHalfMarginDen 9 10 S) := by
  refine ⟨by decide, by decide, fun S hS => ?_⟩
  have hS0 : S ≠ 0 := Nat.ne_of_gt hS
  have hpow : 9 ^ S < 10 ^ S := Nat.pow_lt_pow_left (Nat.lt_succ_self 9) hS0
  exact ⟨hpow, Nat.mul_pos (Nat.succ_pos 1) (Nat.sub_pos_of_lt hpow)⟩

structure Mat2 where
  a11 : Int
  a12 : Int
  a21 : Int
  a22 : Int

def Mat2.mul (x y : Mat2) : Mat2 :=
  ⟨x.a11 * y.a11 + x.a12 * y.a21, x.a11 * y.a12 + x.a12 * y.a22,
   x.a21 * y.a11 + x.a22 * y.a21, x.a21 * y.a12 + x.a22 * y.a22⟩

def Mat2.transpose (x : Mat2) : Mat2 := ⟨x.a11, x.a21, x.a12, x.a22⟩

def Mat2.scale (k : Int) (x : Mat2) : Mat2 := ⟨k * x.a11, k * x.a12, k * x.a21, k * x.a22⟩

def Mat2.applyVec (x : Mat2) (v1 v2 : Int) : Int × Int :=
  (x.a11 * v1 + x.a12 * v2, x.a21 * v1 + x.a22 * v2)

/-- Full 3x3 Pi_inf operator (index 0 = retained A block, indices {1, 2} = dark B block); all Thm 7 blocks are extracted from it. -/
def piInf3 : List (List Int) := [[4, 1, -1], [1, 2, 2], [-1, 2, 2]]

def piInfAt (i j : Nat) : Int := (piInf3.getD i []).getD j 0

def piInfMbb : Mat2 := ⟨piInfAt 1 1, piInfAt 1 2, piInfAt 2 1, piInfAt 2 2⟩

private theorem piInfMbb_eq : piInfMbb = ⟨2, 2, 2, 2⟩ := rfl

def piInfPinvNum : Mat2 := ⟨1, 1, 1, 1⟩

/-- Theorem 7: `⧅` Dark-Mode Shadow kernel (dim_dark = 1, basis (-1, 1), coupling M_AB * (-1, 1) = -2 != 0, r_cross = 1) & Moore-Penrose `⧄` Schur pushforward 8 * M_AA - M_AB * (8 M_BB^+) * M_BA = 8 * 4, with M_AA, M_AB, M_BA, M_BB all extracted from `piInf3`. -/
theorem dark_mode_shadow_and_schur_erasure (v1 v2 : Int) :
    (piInfMbb.applyVec v1 v2 = (0, 0) ↔ ∃ k : Int, v1 = -k ∧ v2 = k) ∧
    (piInfAt 0 1 * (-1) + piInfAt 0 2 * 1 = -2 ∧ (-2 : Int) ≠ 0) ∧
    (piInfMbb.mul (piInfPinvNum.mul piInfMbb) = piInfMbb.scale 8 ∧
     piInfPinvNum.mul (piInfMbb.mul piInfPinvNum) = piInfPinvNum.scale 8 ∧
     (piInfMbb.mul piInfPinvNum).transpose = piInfMbb.mul piInfPinvNum ∧
     (piInfPinvNum.mul piInfMbb).transpose = piInfPinvNum.mul piInfMbb) ∧
    (let pv := piInfPinvNum.applyVec (piInfAt 1 0) (piInfAt 2 0)
     8 * piInfAt 0 0 - (piInfAt 0 1 * pv.1 + piInfAt 0 2 * pv.2) = 8 * 4) := by
  refine ⟨⟨?_, ?_⟩, ⟨rfl, fun h => by cases h⟩, ⟨rfl, rfl, rfl, rfl⟩, rfl⟩
  · intro h
    simp only [piInfMbb_eq, Mat2.applyVec, Prod.mk.injEq] at h
    exact ⟨v2, by omega, rfl⟩
  · rintro ⟨k, h1, h2⟩
    simp only [piInfMbb_eq, Mat2.applyVec, Prod.mk.injEq]
    have h0 : (2 : Int) * v1 + 2 * v2 = 0 := by rw [h1, h2, ← Int.mul_add, Int.add_left_neg, Int.mul_zero]
    exact ⟨h0, h0⟩

def piInfErasure (nPhys : Nat) (P : Nat → Prop) : Prop :=
  ∀ n, 1 ≤ n → n ≤ nPhys → ¬ P n

/-- Theorem 8: Asymptotic erasure Pi_inf shadow: strict exponent advantage eA < eB guarantees eventual dominance while cB * nPhys^eB <= cA * nPhys^eA erases all wins on [1, nPhys]. -/
theorem pi_inf_asymptotic_erasure_shadow (cA cB eA eB nPhys : Nat)
    (he : eA < eB) (hcB : 0 < cB) (hp : 1 ≤ nPhys)
    (hdom : cB * nPhys ^ eB ≤ cA * nPhys ^ eA) :
    (∃ n0 : Nat, 1 ≤ n0 ∧ ∀ n, n0 ≤ n → cA * n ^ eA < cB * n ^ eB) ∧
    piInfErasure nPhys (fun n => cA * n ^ eA < cB * n ^ eB) := by
  have he_split : eA + (eB - eA) = eB := Nat.add_sub_cancel' (Nat.le_of_lt he)
  have hpow_split : ∀ x : Nat, x ^ eB = x ^ (eB - eA) * x ^ eA := fun x =>
    Eq.trans (congrArg (x ^ ·) he_split.symm) (Eq.trans (Nat.pow_add x eA (eB - eA)) (Nat.mul_comm _ _))
  constructor
  · refine ⟨cA + 1, Nat.succ_pos cA, fun n hn => ?_⟩
    have hn_pos : 0 < n := by omega
    have hpow_ea_pos : 0 < n ^ eA := Nat.pow_pos hn_pos
    have hpow_ge : n ≤ n ^ (eB - eA) := by
      have hd : 1 ≤ eB - eA := by omega
      have h1 : n ^ 1 ≤ n ^ (eB - eA) := Nat.pow_le_pow_right hn_pos hd
      simpa [Nat.pow_one] using h1
    have hcb_mul : n ^ (eB - eA) ≤ cB * n ^ (eB - eA) := by
      have h1 : 1 * n ^ (eB - eA) ≤ cB * n ^ (eB - eA) := Nat.mul_le_mul_right _ hcB
      simpa [Nat.one_mul] using h1
    have hlt_gap : cA < cB * n ^ (eB - eA) := by omega
    have hmul := Nat.mul_lt_mul_of_pos_right hlt_gap hpow_ea_pos
    rw [hpow_split n, ← Nat.mul_assoc]
    exact hmul
  · intro n _ hnle hlt
    have hphys_ea_pos : 0 < nPhys ^ eA := Nat.pow_pos hp
    rw [hpow_split nPhys, ← Nat.mul_assoc] at hdom
    have hcoeff : cB * nPhys ^ (eB - eA) ≤ cA := Nat.le_of_mul_le_mul_right hdom hphys_ea_pos
    have hpow_le : n ^ (eB - eA) ≤ nPhys ^ (eB - eA) := Nat.pow_le_pow_left hnle (eB - eA)
    have hle1 : cB * n ^ (eB - eA) ≤ cB * nPhys ^ (eB - eA) := Nat.mul_le_mul_left cB hpow_le
    have hle2 : cB * n ^ (eB - eA) ≤ cA := Nat.le_trans hle1 hcoeff
    have hle3 : cB * n ^ (eB - eA) * n ^ eA ≤ cA * n ^ eA := Nat.mul_le_mul_right (n ^ eA) hle2
    rw [hpow_split n, ← Nat.mul_assoc] at hlt
    exact Nat.not_lt_of_ge hle3 hlt

/-- Theorem 9: FiniteFourier vs FWHT_256 crossovers: C=3 at m*=10 (N*=1024 > 256) and C=4 at m*=17 (N*=131072 > 256). -/
theorem finite_fourier_vs_fwht256_crossover :
    IsCrossoverHorizon (fun m => 9 * (1 + m) < m * m) 10 ∧
    IsCrossoverHorizon (fun m => 16 * (1 + m) < m * m) 17 ∧
    (2 ^ 10 = 1024 ∧ 256 < 1024 ∧ 9 * (1 + 8) = 81 ∧ 8 * 8 = 64) ∧
    (2 ^ 17 = 131072 ∧ 256 < 131072 ∧ 16 * (1 + 16) = 272 ∧ 16 * 16 = 256) := by
  refine ⟨⟨by omega, ?_, ?_⟩, ⟨by omega, ?_, ?_⟩, by decide, by decide⟩
  · intro m _ hlt
    have hle : m * m ≤ 9 * m := Nat.mul_le_mul_right m (by omega)
    omega
  · intro m hge
    have hmul : 10 * m ≤ m * m := Nat.mul_le_mul_right m hge
    omega
  · intro m _ hlt
    have hle : m * m ≤ 16 * m := Nat.mul_le_mul_right m (by omega)
    omega
  · intro m hge
    have hmul : 17 * m ≤ m * m := Nat.mul_le_mul_right m hge
    omega

def karatsubaFuel : Nat → Nat → Nat
  | 0, _ => 0
  | _ + 1, 0 => 0
  | _ + 1, 1 => 2
  | f + 1, n + 2 => 3 * karatsubaFuel f ((n + 3) / 2) + 4 * (n + 2)

def karatsubaSteps (n : Nat) : Nat := karatsubaFuel n n

private theorem karatsubaFuel_eq (f g n : Nat) (hf : n ≤ f) (hg : n ≤ g) :
    karatsubaFuel f n = karatsubaFuel g n := by
  induction f generalizing g n with
  | zero => cases Nat.eq_zero_of_le_zero hf; cases g <;> rfl
  | succ f ih =>
    cases g with
    | zero => cases Nat.eq_zero_of_le_zero hg; rfl
    | succ g =>
      rcases n with _ | _ | k
      · rfl
      · rfl
      · simp only [karatsubaFuel]; rw [ih g ((k + 3) / 2) (by omega) (by omega)]

private theorem karatsubaSteps_succ_succ (k : Nat) :
    karatsubaSteps (k + 2) = 3 * karatsubaSteps ((k + 3) / 2) + 4 * (k + 2) := by
  unfold karatsubaSteps
  have h0 : karatsubaFuel (k + 2) (k + 2) =
      3 * karatsubaFuel (k + 1) ((k + 3) / 2) + 4 * (k + 2) := rfl
  rw [h0, karatsubaFuel_eq (k + 1) ((k + 3) / 2) ((k + 3) / 2) (by omega) (Nat.le_refl _)]

private def checkPredPow2 (P : Nat → Bool) : Nat → Nat → Bool
  | 0, lo => P lo
  | d + 1, lo => checkPredPow2 P d lo && checkPredPow2 P d (lo + 2 ^ d)

private theorem checkPredPow2_sound (P : Nat → Bool) (d lo i : Nat)
    (hok : checkPredPow2 P d lo = true) (hi : i < 2 ^ d) :
    P (lo + i) = true := by
  induction d generalizing lo i with
  | zero =>
    have hi0 : i = 0 := by simp at hi; omega
    subst hi0
    simpa [checkPredPow2] using hok
  | succ d ih =>
    simp only [checkPredPow2, Bool.and_eq_true] at hok
    have hp : 2 ^ (d + 1) = 2 ^ d + 2 ^ d := by simp [Nat.pow_succ, Nat.mul_two]
    by_cases hlt : i < 2 ^ d
    · exact ih lo i hok.1 hlt
    · have hres := ih (lo + 2 ^ d) (i - 2 ^ d) hok.2 (by omega)
      have heq : lo + 2 ^ d + (i - 2 ^ d) = lo + i := by omega
      rw [heq] at hres; exact hres

private def karWinB (n : Nat) : Bool := decide (karatsubaSteps n < 2 * (n * n))

private def karFailB (n : Nat) : Bool := decide (¬ (karatsubaSteps n < 2 * (n * n)))

/-- Theorem 10: Karatsuba recurrence T_K(n) = 3*T_K(ceil(n/2)) + 4*n: Stage-1 [165, 256] mirage, ALL 23/23 re-crossings on [257, 279], and universal global N* = 280. -/
theorem karatsuba_exact_recurrence_global_crossover :
    (¬ (karatsubaSteps 164 < 2 * (164 * 164))) ∧
    (∀ n, 165 ≤ n → n ≤ 256 → karatsubaSteps n < 2 * (n * n)) ∧
    (∀ n, 257 ≤ n → n ≤ 279 → ¬ (karatsubaSteps n < 2 * (n * n))) ∧
    (∀ n, 280 ≤ n → karatsubaSteps n < 2 * (n * n)) := by
  have h165_64 : checkPredPow2 karWinB 6 165 = true := by decide
  have h225_32 : checkPredPow2 karWinB 5 225 = true := by decide
  have h257_16 : checkPredPow2 karFailB 4 257 = true := by decide
  have h273_8 : checkPredPow2 karFailB 3 272 = true := by decide
  have h280_256 : checkPredPow2 karWinB 8 280 = true := by decide
  have h536_32 : checkPredPow2 karWinB 5 536 = true := by decide
  refine ⟨by decide, ?_, ?_, ?_⟩
  · intro n hn1 hn2
    by_cases h229 : n < 229
    · have hs := checkPredPow2_sound karWinB 6 165 (n - 165) h165_64 (by omega)
      rw [show 165 + (n - 165) = n by omega] at hs
      simpa [karWinB] using hs
    · have hs := checkPredPow2_sound karWinB 5 225 (n - 225) h225_32 (by omega)
      rw [show 225 + (n - 225) = n by omega] at hs
      simpa [karWinB] using hs
  · intro n hn1 hn2
    by_cases h273 : n < 273
    · have hs := checkPredPow2_sound karFailB 4 257 (n - 257) h257_16 (by omega)
      rw [show 257 + (n - 257) = n by omega] at hs
      simpa [karFailB] using hs
    · have hs := checkPredPow2_sound karFailB 3 272 (n - 272) h273_8 (by omega)
      rw [show 272 + (n - 272) = n by omega] at hs
      simpa [karFailB] using hs
  · intro n
    refine Nat.strongRecOn (motive := fun x => 280 ≤ x → karatsubaSteps x < 2 * (x * x)) n ?_
    intro x ih hx280
    by_cases hx536 : x < 536
    · have hs := checkPredPow2_sound karWinB 8 280 (x - 280) h280_256 (by omega)
      rw [show 280 + (x - 280) = x by omega] at hs
      simpa [karWinB] using hs
    · by_cases hx568 : x < 568
      · have hs := checkPredPow2_sound karWinB 5 536 (x - 536) h536_32 (by omega)
        rw [show 536 + (x - 536) = x by omega] at hs
        simpa [karWinB] using hs
      · have hge568 : 568 ≤ x := by omega
        obtain ⟨k, rfl⟩ : ∃ k, x = k + 2 := ⟨x - 2, by omega⟩
        let m := (k + 3) / 2
        have ihm : karatsubaSteps m < 2 * (m * m) := ih m (by omega) (by omega)
        have h2m : 2 * m ≤ k + 3 := by omega
        have hsq : (2 * m) * (2 * m) ≤ (k + 3) * (k + 3) := Nat.mul_le_mul h2m h2m
        have hsq_exp : (2 * m) * (2 * m) = 4 * (m * m) := by
          rw [Nat.mul_assoc 2 m (2 * m), Nat.mul_comm m (2 * m), Nat.mul_assoc 2 m m,
              ← Nat.mul_assoc 2 2 (m * m)]
        have hn_sq : 568 * (k + 2) ≤ (k + 2) * (k + 2) := Nat.mul_le_mul_right (k + 2) hge568
        have hrhs : (k + 3) * (k + 3) = (k + 2) * (k + 2) + 2 * (k + 2) + 1 := by
          rw [show k + 3 = (k + 2) + 1 by omega, Nat.add_mul, Nat.mul_add, Nat.mul_one, Nat.one_mul]; omega
        have hstep : karatsubaSteps (k + 2) = 3 * karatsubaSteps m + 4 * (k + 2) :=
          karatsubaSteps_succ_succ k
        omega

private theorem pow_add_of_eq (b m n k : Nat) (h : m + n = k) : b ^ k = b ^ m * b ^ n := by
  cases h; exact Nat.pow_add b m n

private theorem pow_add3_of_eq (b m n p k : Nat) (h : m + n + p = k) :
    b ^ k = b ^ m * b ^ n * b ^ p := by
  cases h; rw [Nat.pow_add, Nat.pow_add]

private theorem lt_of_eq_lt {x y z : Nat} (h1 : x = y) (h2 : y < z) : x < z := by
  cases h1; exact h2

private theorem lt_of_lt_eq {x y z : Nat} (h1 : x < y) (h2 : y = z) : x < z := by
  cases h2; exact h1

/-- Theorem 11: Real stack crossovers: Strassen (1366/1367, N*=1367 <= 37837), HoloSphere-V4 (T*=6), CS-29 (T*=6), AKS sorting (m*=79), S161 AG(4,q) < PG(5,q) for all q >= 2, and Portal 220 sssp-lean (2^266 < 590^64 < 2^590, 591^64 < 2^590: dyadic N = 2^m crossover m* = 590; 590^64 + 1 < 2^590, 591^64 + 1 < 2^590, 592^64 <= 2 * 591^64: exact integer crossover N* = 590^64 + 1 of N > L_N^64). -/
theorem strassen_holosphere_cs29_real_crossovers :
    (1366 ^ 24 < 4 ^ 125 ∧ 4 ^ 125 < 1367 ^ 24 ∧ 1367 ≤ 37837) ∧
    IsCrossoverHorizon (fun t => 65536 + t < 12288 * t) 6 ∧
    IsCrossoverHorizon (fun t => 19200 + 256 * t < 4096 * t) 6 ∧
    IsCrossoverHorizon (fun m => 78 * m < m * m) 79 ∧
    (∀ q : Nat, 2 ≤ q → 2 * (q ^ 4 + q ^ 2) < 2 * (1 + q + q ^ 2 + q ^ 3 + q ^ 4 + q ^ 5 + q ^ 3)) ∧
    (2 ^ 266 < 590 ^ 64 ∧ 2 ^ 589 < 590 ^ 64 ∧ 590 ^ 64 < 2 ^ 590 ∧ 591 ^ 64 < 2 ^ 590) ∧
    (590 ^ 64 + 1 < 2 ^ 590 ∧ 591 ^ 64 + 1 < 2 ^ 590 ∧ 592 ^ 64 < 2 * 591 ^ 64 + 1) := by
  have h590 : 2 ^ 590 = 2 ^ 200 * 2 ^ 200 * 2 ^ 190 := pow_add3_of_eq 2 200 200 190 590 rfl
  refine ⟨by decide, ⟨Nat.le_of_lt (by decide), ?_, fun t _ => by omega⟩,
    ⟨Nat.le_of_lt (by decide), ?_, fun t _ => by omega⟩, ⟨Nat.le_of_lt (by decide), ?_, ?_⟩, ?_, ?_, ?_⟩
  · intro t _ ht; exact Nat.not_lt_of_ge (by omega)
  · intro t _ ht; exact Nat.not_lt_of_ge (by omega)
  · intro m _ _; have : m * m ≤ 78 * m := Nat.mul_le_mul_right m (by omega); exact Nat.not_lt_of_ge this
  · intro m hm; have : 79 * m ≤ m * m := Nat.mul_le_mul_right m hm; omega
  · intro q hq
    have hp : 0 < q ^ 4 := Nat.pow_pos (by omega)
    have h1 : q ^ 4 * 1 < q ^ 4 * q := Nat.mul_lt_mul_of_pos_left hq hp
    have h2 : q ^ 4 < q ^ 5 := by simpa [Nat.pow_succ] using h1
    omega
  · have h266 : 2 ^ 266 = 2 ^ 133 * 2 ^ 133 := pow_add_of_eq 2 133 133 266 rfl
    have h589 : 2 ^ 589 = 2 ^ 200 * 2 ^ 200 * 2 ^ 189 := pow_add3_of_eq 2 200 200 189 589 rfl
    have h1 : 2 ^ 133 * 2 ^ 133 < 590 ^ 64 := by decide
    have h2 : 2 ^ 200 * 2 ^ 200 * 2 ^ 189 < 590 ^ 64 := by decide
    have h3 : 590 ^ 64 < 2 ^ 200 * 2 ^ 200 * 2 ^ 190 := by decide
    have h4 : 591 ^ 64 < 2 ^ 200 * 2 ^ 200 * 2 ^ 190 := by decide
    exact ⟨lt_of_eq_lt h266 h1, lt_of_eq_lt h589 h2,
           lt_of_lt_eq h3 h590.symm, lt_of_lt_eq h4 h590.symm⟩
  · have h5 : 590 ^ 64 + 1 < 2 ^ 200 * 2 ^ 200 * 2 ^ 190 := by decide
    have h6 : 591 ^ 64 + 1 < 2 ^ 200 * 2 ^ 200 * 2 ^ 190 := by decide
    exact ⟨lt_of_lt_eq h5 h590.symm, lt_of_lt_eq h6 h590.symm, by decide⟩

def ldsMaskGate (nStar nPhys : Int) (swapSub flipCmp : Bool) : Int :=
  let gap := if swapSub = true then nPhys - nStar else nStar - nPhys
  if (if flipCmp = true then decide (gap ≤ 0) else decide (0 < gap)) = true then 2 else 1

/-- Theorem 12: True 2nd-order Lipton-DeMillo-Sayward pairwise fault-masking witness: M1 mutants (swapSub) and (flipCmp) are each killed on non-boundary inputs (9, 10) and (11, 10), their M2 combination masks on both non-boundary inputs, and the exact boundary (10, 10) breaks the mask. -/
theorem lipton_demillo_sayward_r5_coupling_witness :
    (ldsMaskGate 9 10 false false = 1 ∧ ldsMaskGate 10 10 false false = 1 ∧ ldsMaskGate 11 10 false false = 2) ∧
    (ldsMaskGate 9 10 true false ≠ 1 ∧ ldsMaskGate 11 10 true false ≠ 2) ∧
    (ldsMaskGate 9 10 false true ≠ 1 ∧ ldsMaskGate 11 10 false true ≠ 2) ∧
    (ldsMaskGate 9 10 true true = 1 ∧ ldsMaskGate 11 10 true true = 2) ∧
    (ldsMaskGate 10 10 true true ≠ 1) := by
  refine ⟨⟨rfl, rfl, rfl⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨rfl, rfl⟩, ?_⟩ <;>
    (intro h; dsimp [ldsMaskGate] at h; cases h)

end GalacticShadow
