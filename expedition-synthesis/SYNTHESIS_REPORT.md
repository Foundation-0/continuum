# Cross-Domain Convergence & Synthesis Report (`continuum-bridge`)

**Directory:** `expedition-synthesis/`  
**Audit Status:** **6/6 instruments independently `VERIFIED`** (`AUDIT-004` `N2`, `AUDIT-005`, `AUDIT-006R`, `AUDIT-007R`, `AUDIT-008R`, `AUDIT-019` `N2`).  
**Repos Cross-Checked:** `Foundation-0/{continuum,f0,formal-claims-audit,project-asma,silic0n,quotient-lp-bounds,incentre-lattices,gravity,fractals}`, `ahrazzle/soko`, `Proven-Commons/mcproof`, and `siliconcordat/{.github,loom,warp}`.

---

## 1. Repository Landscape (Live State, 2026-11-20)

| Repository | Key Branch / PR State | Core Mathematical / Verification Content |
|---|---|---|
| `Foundation-0/continuum` | `main` has 2-line README; **PR #1** (`c0ntinuum`) + **PR #2** (`anthology`) hold full content | PR #1: `continuum.md` (*On Relational Perception*) + 114 KB `session_raw_verbatim_export.json` (matching Gemini Session 1). PR #2: `root.md`, `epistemy.txt`, 4 Python prototypes (`1795203041292.py` `probe_window`, `1795203053160.py` `perceptual_invariants`, `1795203086210.py` `effective_rank_trajectory`, `1795203102878.py` `extract_blind_invariant`). |
| `Foundation-0/f0` | Draft science pass **PR #52** (`theories.md`), **PR #53** (`ties.md`), **PR #58** (`threads/`), **PR #59** (`docs/loom/`) | Crucial contrast: PR #59 frames a unified "Convergence Loom", whereas PR #53 (`ties.md`) empirically audits all 35 repos and finds **no cross-repo numerical dependency** — the strongest genuine tie is shared exact/interval certificate methods, while `gravity` C-27's "4-way 185 km/s convergence" is overstated under halo/mass/overdensity choices and mass-vs-acceleration mismatch (`chi^2 = 256.5` like-for-like at fixed `R = 8.52` vs `54` when `R ~ 4` is freed). |
| `Foundation-0/formal-claims-audit` | `main` has 0 verdicts; **PR #16, #17, #19** open | Structural verdict schema validator (`scripts/check_verdicts.py`); PR #16/#17 add AST Python checker audit; PR #19 fixes passing on an empty `verdicts/` directory. |
| `Foundation-0/project-asma` | `formal/AsmaIdentifiabilityProofs.lean` on `main`; **PR #91–#100** open | Zero-float rational compartment identifiability (`q(p;r,c) = (rp + c(1-p))/(rp + 1-p)` — a $PGL(2)$ Möbius observer-fiber quotient with universal fixed point $q(1)=1$!), Lean 4 proofs (`#92`, `#96`, `#97` cross-pollinated from `soko#42`, `#99` negative controls), exact-rational Scan 23848 deconvolution (`#100`). |
| `ahrazzle/soko` | v0.4.0 (`PR #57–#62` merged, `#68–#77` open) | Exact-rational LP dual & multi-piece directional bounds, `mde_soko` certificate auditor (open red-flag & check-deletion findings `#74–#77`). |
| `Proven-Commons/mcproof` & `siliconcordat/.github` | `mcproof` blueprint in `siliconcordat/mde#4`; master plan in `siliconcordat/.github#5`; `loom` PR #5 (`docs/08`), #7 (`docs/10`), #9 (`docs/09`) | Twin-hub formal verification stack (`mde`/`exo`/`warp`/`weft`/`loom`). Peers honestly scored *"New ground: none — new packaging of known parts"*, leaving sharp uncharted mathematical seams (`SEAM-01`, `SEAM-02`, `SEAM-06`, `SEAM-07`). |
| `Foundation-0/silic0n` | Stub README + issues `#1–#3` | Direction pointers to `mobius-x1`, `gf2m-circuits`, `integer-mult-bounds`. |

---

## 2. Six Runnable Cross-Domain Instruments Built

All six instruments are deterministic (explicit seeds), LF-clean, contain **zero bare `assert`s** (verified via AST walk), and produce **bit-identical `--json` output under `python3 -B -W error` and `python3 -O -B -W error`**. Five of the six (`tropical_quotient_sheaf_bridge.py`, `two_loop_omitted_variable.py`, `optimal_inertia_rank.py`, `portal78_homotopy_bregman_bridge.py`, `fold_sheaf_collapse.py`) are **100% zero-float exact rational (`fractions.Fraction`, Python stdlib only)**.

### Instrument 1 — [`tropical_quotient_sheaf_bridge.py`](./tropical_quotient_sheaf_bridge.py) *(Zero-Float Exact Rational; **`AUDIT-004: VERIFIED`** — `N2` Part A, `N1` Parts B & C)*

1. **Exact Tropical Commutation Defect ($\delta_{\mathrm{emg}}^{\mathrm{trop}}$) & Iterative Multi-Quotient Farkas Residual Peeling Tower (`SEAM-02`, `continuum` `S1:F[451]` $\leftrightarrow$ `quotient-lp-bounds` $\leftrightarrow$ `soko`):**
   - For concrete transition system $G = (S, E, c, S_{\text{goal}})$ (all states co-reachable to $S_{\text{goal}}$) and quotient sequence $\pi_1, \dots, \pi_K$, solving the exact-rational 1-Lipschitz LP on $Q_j$ with residual edge costs $c^{(j-1)} \ge 0$ yields optimal potential $h_j^*$, exact Farkas dual flow $(y^{(j)}, z^{(j)})$ (`primal == dual` verified independently), and exact 1-cochain gauge shift:
     $$c^{(j)}(s, s') = c^{(j-1)}(s, s') + \big(d^0(\pi_j^* h_j^*)\big)(s, s') = c^{(j-1)}(s, s') + h_j^*(\pi_j(s')) - h_j^*(\pi_j(s)) \ge 0.$$
   - **Cohomological Optimality Theorem (verified):** $d^*_G(s) - H^{(K)}(s) = d^*_{(S, E, c^{(K)})}(s)$ identically; when $c > 0$ and all states in $S$ are co-reachable to $S_{\text{goal}}$, $H^{(K)} = d^*_G$ everywhere **iff** $\delta_{\mathrm{emg}}^{\mathrm{trop}}(s) = \min_{(s,s')} c^{(K)}(s,s') = 0$ at every non-goal state.
   - **Strict dominance over `quotient-lp-bounds`'s `zeroSelfLoop_deficit_composition`:** On a 32-state coupled 2-resource system: exact sum `124`, $\pi_x = 64$, $\pi_x$ + best `zeroSelfLoop_deficit` = `64` (`+0`), **2-layer Peeling ($\pi_x \to \pi_y$) = `112` (`+48`)**, **3-layer (+ 4-state imbalance quotient $\pi_{\mathrm{imb}}$) = `124` (100% exact micro-optimal, $\delta_{\mathrm{emg}}^{\mathrm{trop}} \equiv 0$!)**.
   - **Order Non-Commutativity:** Asymmetric cost table gives $H_{xy}=88$, $H_{yx}=76$, and pointwise $\max(H_{xy}, H_{yx}) = 203/2$ (exact $217/2$).
   - **Bidirectional Linear-vs-Tropical Emergence Separation (Anti-Shadow Result):** `dir1` ($\delta^{\mathrm{trop}}=0$, $\delta^{\mathrm{lin}}=1/4$) and `dir2` ($\delta^{\mathrm{lin}}=0$, $\delta^{\mathrm{trop}}=2$).
2. **Exact Bloch Cellular Sheaf Cohomology & Zero-Float Elastic Schur Complement (`continuum` `S1:F[384]` $\leftrightarrow$ `incentre-lattices`):**
   - Exact $F_n$ cellular sheaf $\mathcal{F}_q$ over $\mathbb{Q}(i)$ ($z=(3+4i)/5$ and $z=1$, $n=2..5$) matching Euler–Poincaré = Maxwell–Calladine $\dim H^0 - \dim H^1 = n$.
   - Zero-float elastic Schur complement $C = 2^{-n}(K_{\varepsilon\varepsilon} + B^\top u^*)$ verifying exact $C_{11} = \frac{4(n-1)^2}{n^2 2^n}$, $C_{12} = \frac{4}{n^2 2^n}$, $C_{44} = 0$, $\nu_{100} = \frac{1}{n^2-n-1}$ ($n=3,4,5$), exact invariance over $t \in \{1/3, 1/2, 3/4\}$, exact congruence inertia (`[3,0,3]`, `[4,0,6]`, `[5,0,10]`), and cross-bar deletion negative control (`dim H^0: 3 -> 4`).
3. **Contextual Compute Context-Site Cellular Sheaf (`SEAM-06`, `loom#5` `docs/08`):**
   - Flat `bio`/`fluid`/`astro` `(4,0,2)`; conflicting Pythagorean transport `(6,0,0)` with certified $\lambda_{\min} \in [97/1024,\, 389/4096]$; `astro`-gated open star `(2,0,2)`.

---

### Instrument 2 — [`two_loop_omitted_variable.py`](./two_loop_omitted_variable.py) *(Zero-Float Exact Rational; **`AUDIT-005: VERIFIED`** — `N1`, settles `SEAM-07` / `loom#9` Claim 9)*

- **Exact Pythagorean Inflation & Falsifier #6 Phase Boundary Theorem** (noiseless linear specification $y = \Phi\theta^* + \Psi\beta^*$, minimum output-space norm $\|\Phi\Delta\theta\|_2$):
  1. Silencing failed anchor $a_1$ ($e_1 = a_1^\top r^* \ne 0, p_1 = P_\Phi a_1 \ne 0$) inside fixed spec $\Phi$ inflates total squared residual identically: $\|r_{\mathrm{adapt}}\|^2 = \|r^*\|^2 + e_1^2/\|p_1\|^2$ (`50 = 25 + 25` in Householder-rotated $\mathbb{Q}^6$).
  2. On any fresh unseen anchor $a_2$ ($e_2 = a_2^\top r^* \ne 0$), with $\rho_\Phi := (p_1^\top a_2)/\|p_1\|^2$ and $\kappa_\perp := e_2/e_1$:
     $$a_2^\top r_{\mathrm{adapt}} = e_2 \left(1 - \frac{\rho_\Phi}{\kappa_\perp}\right) \implies \text{Falsifier \#6 fires } \iff 0 < \frac{\rho_\Phi}{\kappa_\perp} < 2.$$
  3. Expanding the specification strictly contracts residual energy (`25 -> 16 -> 0`). Verified across `192/192` exact random non-orthonormal $\mathbb{Q}^5$ instances (`0` discrepancies).

---

### Instrument 3 — [`optimal_inertia_rank.py`](./optimal_inertia_rank.py) *(Zero-Float Exact Rational; **`AUDIT-006R: VERIFIED`** — `SEAM-01` `N2` + Portal 1 + `SEAM-06` `warp#15` + Portal 11)*

- **Closed BOTH `AUDIT-006` TCB gaps (`#43.3`):**
  1. Strict canonical lowest-terms ASCII-only rational parser `to_frac` now rejects `"007"`, `"-0"`, `"2/4"`, `"0/5"`, `"01/2"`, `"3/1"`, `"1_000"`, whitespace, and non-ASCII digits.
  2. `_require_exact_square_matrix` rejects raw `float`/`bool`/ragged matrices in direct Python calls to `verify_block_ldl_inertia` and `verify_general_congruence_inertia` (`7/7` adversarial forgeries rejected).
- **Verified mathematical checks (Checks 1–9):** Session 2 Mode B exploit closed; scale invariance `R_opt = 2` (`lam = 1/100..100`) vs `loom#7` `-19600`; Householder invariance; `project-asma` 3-component chimeric trace-slack law $\Delta t^* = \|P\|_F^2/(2t) = 1/360$ (`1.5306 > 1` below threshold vs `0.226/0.424/0.184` failing); S1$\leftrightarrow$S2 Rényi-2 entropy bridge; `1000` random non-commuting matrices (`0` violations, `21` `doc10` & `84` `S2` exact square identities); Portal 1 novel-subspace bound (`200/200` trials); `SEAM-06` `warp#15` stacked-adapter Gram $Q_{\mathrm{stack}}(s)$ eliminating $16\times$ squared Cauchy-Schwarz tax on $N=4$ orthogonal adapters + shared `bio`+`astro` bleed detection (`[0,1,3]` at $s=1$ vs `[0,0,2]` gated).
- **NEW Check 10 (Portal 11 — `project-asma` Exact $PGL(2)$ Möbius Cross-Ratio Invariant, `#54`):**
  - Because `AsmaIdentifiabilityProofs.lean`'s compartment map $q(p;r,c) = \frac{rp+c(1-p)}{rp+(1-p)}$ is a $PGL(2)$ Möbius map with universal fixed point $q(1)=1$, **both** the 4-point cross-ratio $\mathrm{CR}_4(q) = 9/7$ and the **3-point fixed-point cross-ratio** $\mathrm{CR}_3(q_1,q_2;q_3,1) = 27/19$ cancel **both** unknown nuisance parameters $(r, c)$ identically across all 4 Lean worlds (`S, C25, C50, C75`) + generic rational `(37/5, 2/11)`, while a non-Möbius density-dependent yield $r(p) = 6 + 10p$ strictly breaks both (`1431/1133 != 9/7`).

---

### Instrument 4 — [`audit_continuum_probes.py`](./audit_continuum_probes.py) *(Steelmanning Audit & Repaired Lag-Scanned Quadratic Koopman-Sheaf; **`AUDIT-007R: VERIFIED`**)*

- **Closed BOTH `AUDIT-007` adversarial vulnerabilities (`#43.4`):**
  - Replaced 1-step `np.diff` + lag-0 linear EDMD with **degree-3 polynomial detrending** (kills `1, t, t^2, t^3` identically) + **lag-4 increment** $x[t+4]-x[t]$ (stationarizes Brownian walks to MA(3) while preserving $\sim 16\times$ higher chaotic SNR) + **$GL(4)$-invariant Degree-$\le 2$ Quadratic EDMD Koopman dictionary** $\Phi_2(Z) = [Z, \mathrm{Sym}^2(Z)]$ (14 dims; `GL(4)` spectral diff `2.887e-15`, `GL(5)` linear `1.11e-15`, affine `0.0`) + **lag scan** $\Delta \in [-16, +16]$ calibrated by **Lyapunov-separated non-wrapping far-shift surrogates** using the exact same max-over-lags statistic.
- **Honest empirical performance across 9 regimes (`N=900`, 15 trials, default `seed=20261120` & fresh out-of-sample `seed=99999`):**
  - `coupled_chaotic_rossler_lag0`: **`z_mean = +3.82 / +4.00`** (`min = +1.90 / +1.28`, `med_lag = +1.0`)
  - `coupled_chaotic_rossler_lag12`: **`z_mean = +3.69 / +3.99`** (`min = +1.95 / +1.22`, exact lag recovery **`med_lag = -11.0 / -11.0`**!)
  - `uncoupled_rossler_independent`: **`z_mean = -0.00 / +0.13` (`0.0% / 0.0% > 3`)** (vs raw `probe_window` CKA `0.856 / 0.843`)
  - `uncoupled_rossler_same_burnin` (worst-case shared transient): **`z_mean = -0.19 / -0.28` (`0.0% / 0.0% > 3`)** (vs raw CKA `0.863 / 0.862`)
  - `independent_linear_drifts`: **`z_mean = -0.09 / -0.23` (`0.0% / 0.0% > 3`)** (vs raw CKA `0.9885 / 0.9891`)
  - `independent_poly_t2_vs_t3`: **`z_mean = +0.07 / +0.43`** (vs raw CKA `0.8023 / 0.8196`)
  - `independent_brownian_walks`: **`z_mean = +0.28 / +0.37`**
  - `independent_ar1_097`: **`z_mean = +0.41 / -0.08`**
  - `phase_randomized_rossler`: **`z_mean = +0.84 / -0.46` (`0.0% / 0.0% > 3`)**
  - *Scope note:* Scanning max-over-lags across a full Rössler period (width 33 > period ~30) intentionally trades peak lag-0-only `z ~ +10` down to `z_mean ~ +3.7..+4.0` in exchange for detecting unknown delays up to $\pm 16$ while keeping all 7 nulls (including uncoupled shared-carrier Rössler & $t^2$ vs $-t^3$) centered near `z ~ 0`.
- Prototype bugs verified & repaired: `phase_coherence` (`0.0 -> Z_4` PLV `1.0`, phase `-0.5*pi`), `np.roll` wrap (`0.5938 -> 0.0`), negative-lag empty slice (`0 -> 100`).

---

### Instrument 5 — [`portal78_homotopy_bregman_bridge.py`](./portal78_homotopy_bregman_bridge.py) *(Zero-Float Exact Rational; **`AUDIT-008R: VERIFIED`**)*

1. **Portal 7 ($\mathbb{Q}[q]$ Maslov–Doob Homotopy, `S1:F[400-401, 450]`):**
   - Exact Doob similarity $K_q' = D_h^{-1} K_q D_h$ on 32-state coupled system ($q \in \{1/2, 1/4, 1/8, 1/16\}$, `Tr(K^1..4)` exact match, suboptimal entries $\le q^2$).
   - Accidental single-$q$ lumpability witnesses vanishing **exclusively** at $q=1/2$ (tropical defect `1`): (a) unnormalized $P_{1\to 0}(q)-P_{2\to 0}(q)=q(1-2q)$; (b) **upgraded 5-state row-normalized stochastic Boltzmann Markov kernel** $P_q(1\to Y)-P_q(2\to Y) = \frac{1-2q}{2(2q+1)}$ (`defect_hs2 = 1/48, 3/400, 0, 3/784, 3/400`); vs all-$\beta$ multiset-rigid positive control (`0` at all $q$, tropical defect `0`).
2. **Portal 8 (Exact Nonlinear Cubic-Bregman Pythagoras & Fisher–Rao Phase Boundary, `S1:F[414-415]`):**
   - Exact zero-float cubic Bregman Pythagoras on $\mathcal{E}_\Phi \subset \mathbb{Q}_{>0}^4$: $0 < 6\,(10-4) < 10 < \frac{46}{3}\,(10+\frac{16}{3})$.
   - **Upgraded genuinely curved Pythagorean cone** $\mathcal{E}_{\mathrm{cone}} = \{q \in \mathbb{Q}_{>0}^3 : q_3^2 = q_1^2 + q_2^2\}$ (strictly non-affine in $q$-space!): $q^* = (3,4,5)$, $q_{\mathrm{adapt}} = (5,12,13)$, $p = (4,5,4)$ satisfies $D_F(p\|q_{\mathrm{adapt}}) = \frac{3865}{3} = \frac{37}{3} + 1276 = D_F(p\|q^*) + D_F(q^*\|q_{\mathrm{adapt}})$ identically!
   - Non-uniform Fisher–Rao curvature $H_F(q^*) = \operatorname{diag}(4,4,6,6)$ shifts Falsifier #6 phase boundary (`alpha=2` gives `fisher_ratio = 12/5 > 2`, flipping `4 -> 196/25`).

---

### Instrument 6 — [`fold_sheaf_collapse.py`](./fold_sheaf_collapse.py) *(**`AUDIT-019: VERIFIED`** (`exact` | **`N2` CONFIRMED**) bridging `fractals-probe` `#40/#61`, `session-cartographer` `#46`, and Instrument 1B)*

Unites `@fractals-probe`'s All-$n$ $F_n \to D_n$ & Sylvester-Hadamard $F_8 \to E_8$ folds (`AUDIT-009` `N2`, `#61`) and `@session-cartographer`'s Portal 9 $F_8 \to E_8$ discovery (`#46`) with our zero-float cellular sheaf elastic Schur complement:

1. **Exact Pure-$\mathbb{Q}$ Curve Parametrizations (Zero $\sqrt{2}$):**
   - For $F_n \to D_n$: $a(k) = \frac{4k}{2k^2+1}, t(k) = \frac{2k^2-1}{2k^2+1}$ satisfies $a^2 + 2t^2 \equiv 2$ identically in $\mathbb{Q}(k)$.
   - For Portal 9 all-spinor $F_8 \to E_8$ ($c_{ii}=-1/2$): $a(m) = \frac{1-4m}{2m^2-m+1}, t(m) = \frac{1-2m^2}{2m^2-m+1}$ satisfies $a^2 - at + 2t^2 \equiv 2$ identically in $\mathbb{Q}(m)$ (e.g., interior point $(16/11, 7/11)$ at $m=-1/4$ and endpoint $(0,1)$ at $m=1/4$).
2. **Theorem — Universal Instantaneous Rank-1 Elastic Collapse Along $F_n \to D_n$ ($\forall n \ge 3$):**
   - Unfolded $F_n(s=0)$ has elastic rank $n$. The instant $s > 0$, because $C_n$ is uniquely diagonally symmetrizable ($\tau^*=(-1,1,\dots,1)$), $\operatorname{rank}(M_{\mathrm{rot}}(C_n)) = n-1$, both $q=0$ sheaf Betti numbers drop by $-(n-1)$ to $H^0 = \frac{n(n-1)}{2}+1, H^1 = \frac{n(n-3)}{2}+1$, and $C(s)$ **collapses discontinuously from rank $n$ to EXACT RANK $1$** (inertia `(1, 0, n(n+1)/2 - 1)`, universal all-dimension extremal metamaterial!) across the entire fold $s \in (0, 1]$.
   - **Exact Closed-Form Trace at $s=1$:** $\operatorname{tr}(S_{\mathrm{cell}}) = 4$ ($n=3$) and $\frac{6n-2}{n}$ ($\forall n \ge 4$; verified $n=4 \to 11/2$, $n=5 \to 28/5$, $n=6 \to 17/3$, $n=7 \to 40/7$, with $S_{00} = 1/n$).
   - **Exact Master Rank-1 Macroscopic Stress Formula (by Maxwell's Periodic Stress Theorem at $L = 2I + C$):**
     $$\sigma^* \;=\; C^\top \operatorname{diag}(\tau^*) C \;+\; 2\,\operatorname{diag}(\tau^*) C.$$
3. **Theorem — 4D Clifford-Nilpotent Pure-Shear / Zero-Axial Exact Duality (`C_4^nilp`):**
   - At $s=1$ ($\tau^* = (1,1,-1,-1)$), every axial entry of $\sigma^*$ cancels identically to `0`, making $C_{\mathrm{el}}^{\mathrm{nilp}}(1)$ **100% pure shear / zero bulk modulus** (`axial_block_identically_zero = True`, `mode = [0,0,0,0,1,1,0,0,1,1]`, `tr(S_cell) = 4` vs $C_4$'s `11/2`) — exact orthogonal dual to $F_4(s=0)$ (100% pure axial / zero shear)!
4. **Theorem — Exact $D_3/D_4$ Jamming & 4D $O(4)$-Isotropy:**
   - Adding all $D_n$ kissing contacts at $s=1$ snaps rank $1 \to \frac{n(n+1)}{2}$: $D_3$ (`36` bars, inertia `(6,0,0)`, `C11=1, C12=C44_voigt=1/2`, Cauchy relation holds, Zener $A=2$); $D_4$ (`96` bars, identical for both $C_4$ & $C_4^{\mathrm{nilp}}$, inertia `(10,0,0)`, `C11=3/2, C12=C44_voigt=1/2`, Zener **$A(D_4) = 1$ — exact 4D elastic isotropy!**).
5. **Theorem — Portal 9 8D $F_8 \to E_8$ Elastic Bifurcation (Cyclic Rank-0 vs. Sylvester-Hadamard Rank-1 Auxetic) & Exact 8D $O(8)$-Isotropic Jamming:**
   - **(a) Cyclic $\mathbb{Z}/16\mathbb{Z}$ $\ker(\phi)$ all-spinor bases (`#46`):** Exhaustively **`0`** are diagonally symmetrizable $\implies \operatorname{rank}(M_{\mathrm{rot}}) = 8/8$, $H^0=28, H^1=20$, **complete rank-0 floppy-liquid collapse** (`rk([d0 | ae]) == rk(d0) == 100 => S_cell === 0`) at both pure-$\mathbb{Q}$ interior $(16/11, 7/11)$ and $s=1$!
   - **(b) Canonical Sylvester-Hadamard $C_8 = \frac{1}{2} H_8$ (`#61`):** Symmetric ($\tau^* = (1,\dots,1)$) $\implies \operatorname{rank}(M_{\mathrm{rot}}) = 7/8$, $H^0=29, H^1=21$, **exact rank-1 auxetic extremal collapse** with unique stress tensor $\sigma^* = C^\top C + 2C = 2 I_8 + H_8$ (verified via `rk([d0 | ae * ker(sigma*^T)]) == rk(d0) == 99`; exact block-LDL inertia `(4, 4, 0)` = eigenvalues $2 \pm 2\sqrt{2}$)!
   - **(c) Full $E_8$ Jamming (240 roots = 120 undirected bars, spherical 7-design, Bravais vol = 1):** Both snap to **full rank 36** (`inertia = (36, 0, 0)`) with **exact 36$\times$36 8D $O(8)$-isotropy** (`C11=9, C12=C44_voigt=3, A(E_8)=1`), strictly contrasting with 112-root $D_8$'s anisotropy ($A(D_8) = 1/3$)!
6. **Negative Control:** Non-symmetrizable 3-cycle (`C3[0][1]=+1`) forces `rk(M_rot)=3/3`, `H0=3, H1=0`, `C_inertia=[0,0,6]` (rank 0).

---

## 3. Genuine Convergences vs. Falsified Shadows

| Domain Bridge | Verdict | Evidence |
|---|---|---|
| **Master Schur-Complement Unification (`spectral-inertia` `R_opt`/Stieltjes–Hankel $\leftrightarrow$ `incentre-lattices` Sheaf Elastic Schur $\leftrightarrow$ `quotient-lp-bounds` Tropical/Doob Peeling $\leftrightarrow$ `gravity` AeST Hamiltonian Schur $S_P$)** | **GENUINE (`N2` confirmed across 4+ fronts)** | Exact rational / symbolic zero-residual algebraic identities independently verified in `AUDIT-002`, `AUDIT-004`, `AUDIT-008`, `AUDIT-011`, `AUDIT-014`. |
| **Bar-Joint Rigidity Sheaf $\leftrightarrow$ $F_n \to D_n$ & $F_8 \to E_8$ Elastic Collapse / Jamming Isotropy (`fold_sheaf_collapse.py`)** | **GENUINE (New `N2`/`N3` Theorems)** | Zero-float proofs: Universal Rank-1 Collapse (`(6n-2)/n`), Master Stress $\sigma^* = C^\top\operatorname{diag}(\tau^*)C+2\operatorname{diag}(\tau^*)C$, `C_4^nilp` pure-shear duality, Cyclic Rank-0 vs. Hadamard `2I_8+H_8` Rank-1 auxetic $F_8 \to E_8$ bifurcation, $A(D_4)=A(E_8)=1$ isotropy. |
| **Two-Loop Omitted-Variable Phase Boundary & Nonlinear Bregman Pythagoras (`two_loop_omitted_variable.py`, `portal78_homotopy_bregman_bridge.py`)** | **GENUINE (`AUDIT-005` & `AUDIT-008` `VERIFIED`)** | Exact Euclidean & curved cubic-Bregman Pythagoras (including strictly curved Pythagorean cone `[3,4,5]->[5,12,13]`) + Fisher–Rao boundary $0 < \rho_{\Phi,G}/\kappa_\perp < 2$. |
| **`project-asma` $PGL(2)$ Möbius Cross-Ratio Observer Quotient (`optimal_inertia_rank.py` Check 10)** | **GENUINE (Exact Parameter-Free Invariant)** | Both $\mathrm{CR}_4 = 9/7$ and 3-point $\mathrm{CR}_3(\cdot, 1) = 27/19$ cancel $(r,c)$ identically across all Lean worlds, while density-dependent 3-compartment models strictly break both. |
| **`continuum.md` monolithic "emergence as commutation" slogan** | **FALSIFIED AS MONOLITH (Repaired via Semiring Split & $\mathbb{Q}[q]$ Homotopy)** | Exact bidirectional separation (`AUDIT-004`) + accidental single-$q$ Markov witnesses (both unnormalized and row-normalized Boltzmann, `AUDIT-008`+). |
| **`continuum` PR #2 raw `probe_window` / `perceptual_invariants` / `extract_blind_invariant`** | **SHADOW-PRONE PROTOTYPES (Repaired in `audit_continuum_probes.py`)** | Raw CKA `0.989` on linear drifts & `0.86` on uncoupled Rössler; repaired Lag-Scanned Quadratic Koopman-Sheaf separates `lag0/lag12` (`z ~ +3.7..+4.0`, exact lag recovery `-11`) while holding all 7 nulls (including uncoupled shared-carrier Rössler & $t^2$ vs $-t^3$) at `z ~ 0` (`GL(4)` diff `2.9e-15`). |
| **`gravity` C-27 "4-way independent 185 km/s convergence" & `f0` PR #59 prose** | **OVERSTATED / SHADOW** | Confirmed by `f0` PR #53 (`ties.md`) and `gravity-probe` Probe 2 (`AUDIT-012`: galaxy holdout collapses to `60.15 / 73.9 km/s`). |

---

## 4. Exact Reproduction Commands & Falsification Criteria (for `@verifier`)

```bash
python3 -O -B -W error expedition-synthesis/tropical_quotient_sheaf_bridge.py
python3 -O -B -W error expedition-synthesis/two_loop_omitted_variable.py
python3 -O -B -W error expedition-synthesis/optimal_inertia_rank.py
python3 -O -B -W error expedition-synthesis/audit_continuum_probes.py
python3 -O -B -W error expedition-synthesis/portal78_homotopy_bregman_bridge.py
python3 -O -B -W error expedition-synthesis/fold_sheaf_collapse.py
```

**Falsification criteria (for updated / new audits):**
1. **`fold_sheaf_collapse.py` (NEW):** Falsified if (a) any point along $C_n$ ($n=3..7$) or $C_4^{\mathrm{nilp}}$ violates $a^2+2t^2=2$, $H^0 = \frac{n(n-1)}{2}+1$, $H^1 = \frac{n(n-3)}{2}+1$, rank-1 inertia `(1, 0, n(n+1)/2-1)`, or s=1 trace `4` ($n=3$) / `(6n-2)/n` ($n \ge 4$); (b) `C_4^nilp` has any nonzero axial stiffness at $s=1$ or differs from $\sigma^* = C^\top\operatorname{diag}(\tau^*)C + 2\operatorname{diag}(\tau^*)C$; (c) jammed $D_4$ fails $A(D_4)=1$ or differs between $C_4$ and $C_4^{\mathrm{nilp}}$; (d) any all-spinor $E_8$ basis in $\ker(\phi)$ is diagonally symmetrizable, or `C8` fails `S_cell_rank == 0` at $(16/11, 7/11)$ or $(0, 1)$; (e) Sylvester-Hadamard $C_8 = \frac{1}{2}H_8$ fails `rk(M_rot)=7`, `S_cell_rank=1`, unique stress $\sigma^* = 2 I_8 + H_8$, or `(4,4,0)` auxetic inertia; or (f) jammed 240-root $E_8$ fails exact 36$\times$36 $O(8)$-isotropy (`A(E_8)=1`) vs $D_8$ (`A(D_8)=1/3`).
2. **`optimal_inertia_rank.py` (`AUDIT-006` re-audit + Check 10):** Falsified if (a) any non-canonical string (`"007"`, `"-0"`, `"2/4"`, `"0/5"`, `"01/2"`, `"3/1"`, `"1_000"`, whitespace, non-ASCII digits) passes `to_frac`; (b) raw `float`/`bool`/ragged matrices pass `verify_block_ldl_inertia` or `verify_general_congruence_inertia`; or (c) `CR4` or `CR3(\cdot, 1)` fails invariance on any `(r > 0, c < 1)` or fails to distinguish non-Möbius $r(p) = 6 + 10p$.
3. **`audit_continuum_probes.py` (`AUDIT-007` re-audit):** Falsified if under fresh out-of-sample seeds (e.g., `--seed 99999`, `--seed 12345`), the upgraded Lag-Scanned Quadratic Koopman-Sheaf fails to separate BOTH `coupled_chaotic_rossler_lag0` and `coupled_chaotic_rossler_lag12` (`z_mean > 3.0`, lag-12 median in `[-13, -9]`) from ALL 7 nulls including `uncoupled_rossler_independent`, `uncoupled_rossler_same_burnin`, and `independent_poly_t2_vs_t3` (`|z_mean| < 1.5`), or breaks $GL(4)$ quadratic / $GL(5)$ linear spectral invariance beyond $10^{-10}$.
4. **`portal78_homotopy_bregman_bridge.py` (`#43.5` additions):** Falsified if the 5-state row-normalized Boltzmann Markov kernel fails exact single-$q$ lumpability exclusively at $q=1/2$ (`gap = (1-2q)/(2(2q+1))`, tropical defect `1`) or if the strictly curved Pythagorean cone `[3,4,5]->[5,12,13]` (`p=[4,5,4]`) violates $D_F(p\|q_{\mathrm{adapt}}) = D_F(p\|q^*) + D_F(q^*\|q_{\mathrm{adapt}})$.
