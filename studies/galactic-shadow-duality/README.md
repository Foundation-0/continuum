# Galactic Shadow, Crossover-Horizon $N^*$, `CS-09 <-> CS-Galactic` Duality & Portal 220 Witness

Self-contained, CPU-only, pure-stdlib (`int`/`Fraction`) and pure-`Init` Lean `4.36.0` verification bundle for **Track S174 (`EXP-Q60a+EXP-Q60b`)**, unifying eventual-dominance crossover horizons, scale-inversion duality ($u = 1/N$), dark-mode Schur erasure ($\Pi_\infty$ & `⧅`/`⧄`/`⫩`), and Lipton–DeMillo–Sayward (LDS) 2nd-order mutation coupling.

- **Verification scope:** the claims in this bundle that this repository can replay are the **`12/12` Lean `4.36.0` kernel-checked theorems** (`--check --live-lean`), the offline `--check` certificate, the `5/5` test suite, and the in-repo LDS mutation engine (`12/12` $M_1$, `60/60` $M_2$ on `gate_kernel`). External audit reports, a Stage-1 preregistration file, and `aletheia mutate` / `aletheia audit-check` runs are **not included in this repository** and no receipt for them is claimed here.
- **Arithmetic & Proof Regime:** Pure exact $\mathbb{Q}/\mathbb{Z}$ + Pure-`Init` Lean `4.36.0` (`0` Mathlib, `0` floats, `0` `ast.Div`, `0` bare `assert`s, `0` `.lake/`/`__pycache__` residue, `WEIGHTS=0`, `cpu_only=true`, Law-4 `N1`).
- **Cross-References:** `Foundation-0/continuum`, `Foundation-0/cave-expedition#31`, `Foundation-0/aletheia`.

## Contents

| File | Role |
| :--- | :--- |
| [`GalacticShadow.lean`](GalacticShadow.lean) | Pure-`Init` Lean `4.36.0` formalization (`12/12` public theorems, axioms `[]` / `[propext]` / `[propext, Quot.sound]` only, `0` `sorry`) |
| [`lean-toolchain`](lean-toolchain) | Pinned toolchain (`leanprover/lean4:v4.36.0`) |
| [`lakefile.toml`](lakefile.toml) | Declarative Pure-`Init` Lake manifest (`GalacticShadow`, `0` `lakefile.lean`) |
| [`lake-manifest.json`](lake-manifest.json) | Dependency-free manifest (`packages: []`) |
| [`galactic_shadow_verifier.py`](galactic_shadow_verifier.py) | Hardened `R1–R7` exact $\mathbb{Q}/\mathbb{Z}$ oracle, static AST/Lean-4 lexer audit, & `--live-lean` / `--aletheia-root` kernel/operator verifier |
| [`test_galactic_shadow_r5.py`](test_galactic_shadow_r5.py) | `5`-group assertion-free R1–R7, regression, & mutation-killing suite (`5/5 OK`, `0` stdout bytes on pass) |
| [`s174_stage2_certificate.json`](s174_stage2_certificate.json) | Canonical offline `STATIC_ONLY` certificate (`payload_sha256: 3f3359b1c61c655bf577f72244cf790e153f6ec773675672218a330ba2dd8701`) |
| [`REPORT.md`](REPORT.md) | Full technical report, Law-4 scope table, `12/12` Lean theorem index, `15/15` portfolio table, & SHA-256 manifest |

## Key Verified Results

1. **Exact Crossover Horizon $N^*$ & Dichotomy (`15/15` Portfolio):** Classifies algorithm pairs into `GALACTIC_SHADOW` ($N_{\max}^{\text{phys}} < N^*$, `10`), `TERRESTRIAL_CROSSOVER` ($N^* \le N_{\max}^{\text{phys}}$, `4`), and `NO_ASYMPTOTIC_ADVANTAGE` (`1`). Includes Portal 220 `igholami/sssp-lean` (`arXiv:2611.34911v1` Alg. 8: dyadic grid $m^* = 590$, first integer crossing $589^{64} + 1$ (least $N$ with $N > L_N^{64}$), eventual integer crossover $N^* = 590^{64} + 1 > 2^{266}$ (least $N_0$ with $N > L_N^{64}$ for all $N \ge N_0$; the predicate re-fails on $[2^{589} - 1,\, 590^{64}]$), both computed by the verifier's exact band scan) and Stage-1 Karatsuba `[1, 256]` truncation-mirage discovery (`[257, 279]` 23-integer re-crossing vs universal $N^* = 280$).
2. **Exact Reciprocal Scale-Inversion Duality (`CS-09 <-> CS-Galactic`):** `PosRat.unitRecip` ($u(N) = 1/N$) proves exact involution and order-reversal ($1/N^* < 1/N_{\text{phys}} \iff N_{\text{phys}} < N^*$) unifying finite-sample `BF16` MUX collapse ($S=3$ passes, $S=4$ collapses) vs universal `Al-Kāshī` $u=0$ margin positivity ($\forall S \ge 1,\; 9^S < 10^S$) with physical-horizon asymptotic mirages.
3. **Dark-Mode Shadow ($\Pi_\infty$) & `⧅`/`⧄`/`⫩` Parity:** Extracts $M_{AA}, M_{AB}, M_{BA}, M_{BB}$ directly in Lean from `piInf3` (`dim_dark = 1`, `r_cross = 1`, kernel `[[-1/1, 1/1]]`, coupling `[[-2/1]]`, Schur `[[4/1]]`) with exact parity against `aletheia.calculus`.
4. **Lipton–DeMillo–Sayward (LDS) Mutation Coupling (`EXP-Q60b`):** Pure-AST mutant engine kills `12/12` $M_1$ and `60/60` pairwise $M_2$ combinations on `gate_kernel`, plus a verified 2nd-order pairwise fault-masking witness on `mask_kernel`.

## Verification Commands

```bash
cd studies/galactic-shadow-duality

# 1. 3-mode isolated -I parity (static certificate + exact oracle replay)
for flags in "-I -B" "-I -O -B" "-I -B -W error"; do
  CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 python3 ${flags} galactic_shadow_verifier.py --check
  CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 python3 ${flags} test_galactic_shadow_r5.py
done

# 2. Standalone Lean 4.36.0 kernel check (0 warnings, 0 .lake/ residue)
lean GalacticShadow.lean

# 3. Live Lean 4.36.0 build + 12/12 kernel type pins + #print axioms (tempdir-isolated)
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 python3 -I -B galactic_shadow_verifier.py --check --live-lean
```
