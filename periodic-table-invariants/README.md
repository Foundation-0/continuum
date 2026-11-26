# Cross-Civilizational Periodic Table of Exact Invariants

Self-contained, pure-Python standard-library verification module and machine-readable **Periodic Table of Invariants** for `Foundation-0/continuum`, organizing cross-civilizational and modern mathematical structures by shared operator morphology rather than disciplinary labels.

All proofs execute strictly in exact integer (`int`) and rational (`Fraction`) arithmetic with **zero floating-point or complex operations**, **zero `/` or `/=` true-division AST nodes**, **zero negative-exponent powers (`2**-1`)**, **zero `pow()`/`getattr()`/`builtins` escapes**, **zero `__float__`/`__complex__`/`__truediv__`/`__rtruediv__`/`__itruediv__`/`__pow__` attribute references**, **zero `math.<attr>` calls or constant references outside `{gcd, isqrt}` (including import aliases)**, **zero string/float/1-arg/`from_float` `Fraction(...)` calls**, **zero bare `assert` statements**, **zero external dependencies**, **zero unbound external provenance hashes**, and **zero empirical power or energy telemetry claims** (`CPU_ONLY_PURE_Q_NO_ENERGY_CLAIMS`; mechanical hysteresis loop areas are dimensionless geometric quantities).

---

## 1. Four-Class $\aleph_0 \to \mathfrak{c}$ Finite-Net Obstruction Taxonomy (`54 / 54` In-Module Checks)

Every countable symbolic net cutting a continuum encounters exact, frame-invariant obstructions. `verify_periodic_table_invariants.py` computes and certifies **`54 / 54`** pure-$\mathbb{Q}/\mathbb{Z}$ witness checks directly in-module across four disjoint classes:

| Class | Exact Structural Signature | Self-Contained In-Module Certified Witnesses | Checks |
|---|---|---|---:|
| **Class A: Diophantine / Prime-Lattice Incommensurability** | Non-vanishing integer power or best-rational floor ($r^p \neq 2^k$, Hurwitz convergent gap, telescoping $O(1/n^7)$ remainder) | Al-Fārābī `53-TET` ($\gcd(12,11)=1 \implies 12^{53} \neq 2^7 \cdot 11^{53}$, exact gap certified; Holder comma $3^{53} > 2^{84}$); Zu Chongzhi `[3; 7, 15, 1] = 355/113` beats `22/7` by `>= 4,740×` with exhaustive denominator scan over $q \in [114, 16604]$ proving `52163/16604` is the earliest rational beater against a first-principles pure-$\mathbb{Q}$ Machin alternating-series $\pi$ bracket (`0` embedded decimal $\pi$ literals); Rhind `2/17` (`max 68 < 153`) & non-`2/n` Egyptian `5/21` (`max 14 < 945`) compared against live greedy Sylvester decompositions; Antikythera additive beat $254\cdot 223 - 239\cdot 235 = 477 = 9\cdot 53$; Kerala School Mādhava $R_1, R_2, R_3$ telescoping identities (`49/49` each for $n=2..50$) and exact $n=50$ speedup floor `>= 27,872,151,775×` over Leibniz. | **`15 / 15`** |
| **Class B: Finite-Precision Subtractive Cancellation & Rational Sphere Lift** | $\kappa_{\mathrm{sub}}(x) = \frac{x}{1-x}$ clamped bit loss & division-only stereographic/Cayley maps | Al-Bīrūnī Nandana ($\kappa = 215989/11$, `14` bits lost, $R = 28167341479/2200$ cubits); Al-Kāshī chord-doubling wall derived from $k$ ($k=25 \to 51$ bits, $k=26 \to 53$ bits); multiscale quadratic zoom derived from $\ell$ ($\ell=13 \to 51$, $\ell=14 \to 55$, $\ell=16 \to 63$ bits); **generic multivariate integer-polynomial bijection proof (`19/19` identities over $\mathbb{Z}[u,v]$, $\mathbb{Z}[x,y,z]$, $\mathbb{Z}[w_1,w_2,w_3]$, $\mathbb{Z}[q_0,q_1,q_2,q_3]$)** plus `5`-point numerical round-trips for Al-Bīrūnī *Istīʿāb* stereographic $\mathbb{Q}^2 \leftrightarrow S^2(\mathbb{Q})\setminus\{N\}$, rational Cayley $\mathbb{Q}^3 \leftrightarrow S^3(\mathbb{Q})\setminus\{-1\}$, and exact equatorial embedding `(-z, x, y, 0) == cayley_s3(u, v, 0)`. | **`12 / 12`** |
| **Class C: Topological Winding, `C1P` Partition, $\mathbb{F}_2^n$ Hypercube & Sheaf $\check{H}^1$** | Coprimality cycle count, forbidden incidence minor, $\mathbb{F}_2^n$ duality, explicit $H \in \mathbb{F}_2^{5\times 16}$, or twisted coboundary | Chokwe *Sona* exhaustive `576/576` sweep over $(m,n) \in [1,24]^2$ proving `loop_count(m,n) == gcd(m,n)` + 2-opt internal mirror surgery (`(2,2): 2 -> 1`, `(2,3): 1 -> 2`); Pāṇini `14` *Śivasūtras* `43/43` *pratyāhāra* `C1P` decoding + Tucker $C_3$ (`0/6` single-copy orders, resolved by duplicate `h`); Piṅgala `naṣṭa`/`uddiṣṭa` `510/510` bijection ($n=1..8$) + `FWHT_256` `256/256` involution & parity + explicit `5 × 16` Extended Hamming `[16,11,4]` `A_16` SECDED parity-check matrix $H$ (`16/16` distinct nonzero 1-bit syndromes, `120/120` nonzero 2-bit syndromes disjoint from all 1-bit syndromes, `2,048` codewords in $\ker(H)$, $d_{\min} = 4$) + *Bamana* `65,536/65,536` even-Judge parity-conservation identity check and 5-bit `A_16` syndrome correspondence; $\mathbb{Z}_2$ twisted 3-cycle sheaf (`0/8` vs `2/8`); explicit *Casarabe* $C_{2,6}$ (`13` vertices, pinned canonical `24`-edge simple adjacency & degree sequence `[6, 4×6, 3×6]`, $\beta_1 = 12$, 1-cut connected) vs spanning tree $T_{13}$ (pinned `12`-edge adjacency & degrees `[6, 2×6, 1×6]`, $\beta_1 = 0$, 1-cut disconnected) + hierarchical khipu tree-sum checksum & 1-cord tamper detection. | **`19 / 19`** |
| **Class D: Commutation, Sylvester Inertia & Coarse-Graining Defect** | Schur shift, certified inertia separation, Kemeny–Snell Markov defect, or Lie–Trotter commutator | Ibn al-Nafīs readable-record 3×3 Schur complement (`det: 34/625 -> 688/15625`, `trace_drop = 81/1250`); self-certifying $8 \times 8$ congruence $P^\top M P = \operatorname{diag}(d)$ proving passive hydraulic Laplacian inertia `(7, 0, 1)` is non-congruent to indefinite $H_8$ stress $2I_8 + H_8$ inertia `(4, 4, 0)`; explicit $4 \times 4$ row-stochastic Kemeny–Snell strong Markov lumpability (`0/1` vs `1/2`); $SU(2)$ half-angle Cayley Lie–Trotter defect (`262144/17850625`) vs exact palindromic Strang quaternion `(4032063/4293185, 205632/858637, 16/65, 0)`. | **`8 / 8`** |

---

## 2. Subtractive Selection & Opposing-Pair Conservation (`13 / 13` In-Module Checks)

Separates Abelian/commutative **`0/1`** cancellation from non-Abelian / curved-manifold / dissipative nonzero residuals via explicit matrix, Lie-bracket, and equilibrium computations:
- **Zero-Residual Abelian Witnesses (`0/1`):** Explicit $2 \times 2$ counter-rotating planar Al-Ṭūsī orthogonal matrices (curl `0/1`, longitudinal factor `4/5`), exact collinear $SU(2)$ palindromic Strang quaternion (`(829455/1122833, 756808/1122833, 0, 0)`, defect `0/1`), linear antagonistic muscle-pair equilibrium (`net_torque = 0/1`, displaced restoring torque `-1/2`, vanishing mixed coupling $H_{\mathrm{ant}} = 0/1$), and explicit $3 \times 3$ orthogonal Cayley steering matrix $R_{\mathrm{plane}}(1/2)$ (`R^T R = I_3`, norm `1/1`, orthogonal axis retention `1/1` vs $xz$-plane rotation `9/25` squared retention).
- **Nonzero Non-Abelian / Curved / Dissipative Witnesses:** Explicit $3 \times 3$ $SO(3)$ Al-Ṭūsī spherical hippopede product $R_z(\theta) R_y(\alpha) R_z(-2\theta) R_y(\alpha) e_3$ (transverse magnitude `288/3125`), exact $\mathfrak{so}(3)$ Lie-bracket order-3 BCH $C_3(e_1, 2e_2) = (-1/3, -1/6, 0)$ ($\|C_3\|^2 = 5/36$), *Yingzao Fashi* *Dougong* dimensionless Coulomb hysteresis loop area (`96/1`, elastic reference `36/1`, $\pi\zeta = 2/3$), and Machu Picchu slender-ashlar Housner (1963) rocking ($b/h = 1/3 \implies \sin^2\alpha = 1/10$, restitution `289/400`, fractional impact loss `111/400`).

---

## 3. Intrinsic Modular Flow & Minimal Sufficient Partition (`15 / 15` In-Module Checks)

- **Zero-Defect Minimal Partition & Fixed-Width Bit Costs:** Derived directly from the decoded `43` *pratyāhāras*, `42` distinct phonemes, `43` *Śivasūtra* slots, and `14` *it*-markers: storing a naive dense `42`-bit membership vector per class costs `43 × 42 = 1,806` bits; fixed-width binary indexing requires $\lceil \log_2 42 \rceil = 6$ bits per phoneme ID and $\lceil \log_2 14 \rceil = 4$ bits per *it*-marker ID, giving `6 + 4 = 10` bits per `(start_phoneme, end_marker)` descriptor (`43 × 10 = 430` bits $\implies$ `1806/430 = 21/5 = 4.20×`) plus `43 × 6 = 258` bits for the linear slot table (`430 + 258 = 688` bits $\implies$ `1806/688 = 21/8 = 2.625×`) with zero false inclusions, while single-copy `{y, sh, h}` encounters the `0/6` Tucker $C_3$ obstruction.
- **Discrete Rational Modular Sections & Two-Clock Shift:** Qin Jiushao non-coprime CRT **exhaustive `37,960 / 37,960` isomorphism** $\mathbb{Z}/37960\mathbb{Z} \cong G_{\mathrm{compat}} \subset \mathbb{Z}/260\mathbb{Z} \times \mathbb{Z}/365\mathbb{Z} \times \mathbb{Z}/584\mathbb{Z}$ onto the compatible residue subgroup $G_{\mathrm{compat}} = \{(r_1, r_2, r_3) : r_1 \equiv r_2 \pmod 5,\; r_2 \equiv r_3 \pmod{73},\; r_1 \equiv r_3 \pmod 4\}$ ($|G_{\mathrm{compat}}| = 260\cdot 365\cdot 584 / 1460 = 37960$, $x = 12345$, phase compression `1,460×`, Dresden `11960/405 = 2392/81`, inconsistent triple `(0 mod 260, 1 mod 365)` refused), Antikythera gear trains computed via `gear_train_ratio` (`254/19`, `235/19`, `477/4237`, anomalistic `56165/4237`), and exact finite-baseline two-clock Hurst-3/4 variance shift (`112/31 -> 256/31`, $\Delta\beta^2 = 144/31$) contrasted against the explicit `1,024`-sequence Walsh–Rademacher white-noise finite-sample block-variance estimator (`1/1 -> 1/1`, $\Delta\beta^2 = 0/1$).

---

## 4. Machine-Readable Periodic Table (`periodic_table_of_invariants.json`)

Contains **`16` self-contained entries (`PT-01`..`PT-16`)** backed by **`82 / 82` in-module exact pure-$\mathbb{Q}/\mathbb{Z}$ checks** (`54 + 13 + 15`) across **`5` morphological families**, with **zero unbound external digests**. Every entry's `morphism_evidence` flags (`has_forward_inverse_bijection`, `has_non_congruent_inertia_separation`, `has_impossibility_counterexample`, `has_shared_operator_witness`), `morphism_grade` (`EXACT_ISOMORPHISM`, `EXACT_SHARED_OPERATOR`, `SHARED_BLOCK_ELIMINATION_NON_CONGRUENT`, `PROVABLE_OBSTRUCTION`), and `witness_metrics` are derived dynamically from live pillar outputs (degrading any pillar flips its evidence dict and grade), and `--check` validates both live recomputation and exact byte-for-byte equality of both committed JSON files on disk (with `parse_float`/`parse_constant`/duplicate-key/CRLF rejection before canonicalization).

---

## 5. Offline & CI Verification

GitHub Actions (`.github/workflows/verify-periodic-table.yml`) runs both `--check` and `test_periodic_table_invariants.py` across Python `3.11`, `3.12`, and `3.13` in all three isolated modes (`-I -B`, `-I -O -B`, `-I -B -W error`), confirming bit-identical `--check` output and `0` stdout bytes on the test suite (including planted AST/runtime float escapes, $C_{2,6}$ mis-wired ring rejection, morphism-grade degradation, and on-disk JSON tamper controls). No external mutation harness is bundled in this repository.

```bash
cd periodic-table-invariants

# Pure-stdlib, zero-float, zero-div, zero-log verification (validates live math + committed JSON files on disk)
python3 -I -B verify_periodic_table_invariants.py --check
python3 -I -O -B verify_periodic_table_invariants.py --check
python3 -I -B -W error verify_periodic_table_invariants.py --check

# Standalone unit, boundary, AST/runtime float-guard, morphism-grade & disk-tamper suite (0 stdout bytes on PASS)
python3 -I -B test_periodic_table_invariants.py
python3 -I -O -B test_periodic_table_invariants.py
python3 -I -B -W error test_periodic_table_invariants.py
```
