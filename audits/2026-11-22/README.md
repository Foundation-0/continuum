# Audit: Foundation-0/continuum (2026-11-22)

Auditor: amp-vela (Muse seat), at A's request, alongside the site work in
[PR #4](https://github.com/Foundation-0/continuum/pull/4). Method: Aletheia
single-agent loop. Every Python artifact was executed locally. Headline
identities were re-derived with zero-shared-code checkers, kept beside this
report in [`checks/`](checks/). Failed checker assumptions were repaired
before any negative verdict.

Issues filed from this audit:
[session-material privacy decision](https://github.com/Foundation-0/continuum/issues/5),
[missing license](https://github.com/Foundation-0/continuum/issues/6),
[zero-float wording](https://github.com/Foundation-0/continuum/issues/7).

Rerun the independent checks from the repository root:

```bash
python3 -I -B audits/2026-11-22/checks/check_exact_identities.py
python3 -I -O -B audits/2026-11-22/checks/check_exact_identities.py
python3 -I -B -W error audits/2026-11-22/checks/check_exact_identities.py
git show origin/anthology:gemini-code-1795203041292.py > /tmp/probe_original.py
python3 -I -B audits/2026-11-22/checks/check_probe_shadow.py /tmp/probe_original.py
```

## 0. Inventory

| Ref | Contents | State |
|---|---|---|
| `main` | Two-line README only | Default branch. Nothing else has ever landed |
| `c0ntinuum` ([PR #1](https://github.com/Foundation-0/continuum/pull/1)) | The framework essay (twice, plus a 735 KB RTF), verbatim session JSON | Open |
| `anthology` ([PR #2](https://github.com/Foundation-0/continuum/pull/2)) | `root.md` session transcript (the same blob as `root.txt` and `root.rtf`), `epistemy.txt`, 9 notation scraps, 4 Python prototypes | Open |
| `expedition/synthesis-instruments` ([PR #3](https://github.com/Foundation-0/continuum/pull/3)) | Six synthesis instruments plus the double-slit instrument, two reports, one prior-art fence, one test file, one certificate | Open |
| `site/continuum-pages` ([PR #4](https://github.com/Foundation-0/continuum/pull/4)) | The GitHub Pages site | Open, awaiting required review |

No issues. No CI anywhere until PR #4. No license, no `.gitignore`, no
CODEOWNERS. Org ruleset `protect-main` requires a pull request with one
approving review for `main`. Public repository, about 240 KiB of objects.

## 1. Verdict summary

| # | Claim or artifact | Grade claimed | Audit verdict |
|---|---|---|---|
| 1 | Six synthesis instruments run clean, bit-identical across interpreter modes | Verified | **VERIFIED** (reproduced) |
| 2 | Five of six synthesis instruments are "100% zero-float" | Exact | **PARTIAL**: exact cores, float display and one float gate |
| 3 | Double-slit instrument: four regimes, zero floats in theorems, certificate | Verified, N1 | **VERIFIED** (runs, tests, certificate all reproduce) |
| 4 | Repaired Koopman-sheaf detector separates coupled from nulls | Verified, sampled | **VERIFIED** (passes own falsification bars on two unseen seeds) |
| 5 | Raw PR #2 prototypes detect blind invariants | (implicit) | **FALSIFIED as stated** (confirmed on the original code) |
| 6 | Asma cross-ratios 9/7 and 27/19 cancel observer parameters | Exact | **VERIFIED mechanism** (textbook Möbius invariance, values reproduce) |
| 7 | Two-loop Pythagoras and Falsifier #6 boundary | Exact | **VERIFIED** (independent checker, 400/400) |
| 8 | Fold collapse: curves, Hadamard stress, D4/E8 isotropy values | Exact, N2 | **Values VERIFIED as computed. Novelty UNCONFIRMED** |
| 9 | Session export integrity (size and SHA-256 in `root.md`) | Verbatim | **VERIFIED** (hash matches byte for byte) |
| 10 | Ten-form atlas numbers (named datasets, constants) | (session narrative) | **UNVERIFIED**: no data, code path or provenance in repo |
| 11 | The framework (four habits, four moves, vertical axis) | Thesis | **PROPOSED**: coherent program, not yet a tested theory |
| 12 | Secrets in history | n/a | **None found** across all revisions |
| 13 | Site PR #4 (this auditor's own work) | n/a | Sound. One wording overstatement found and fixed (section 7) |

## 2. Exact instruments: reproduction

All six synthesis instruments plus the double-slit observer were run under
`python3 -I -B`, `-I -O -B` and `-I -B -W error` (double-slit also
`-I -O -B -W error`). Every run exited 0 with bit-identical `--json`
(SHA-256 prefixes: tropical `fd554535`, two-loop `4857c33f`, optimal
`7166a23d`, portal78 `950e275d`, fold `d2dd6b10`, double-slit `40fafeec`).
`test_double_slit_r5.py` passes 5/5 in all modes. The live double-slit
JSON is semantically identical to the committed
`double_slit_continuum_certificate.json`. Zero bare `assert` statements in
every instrument (AST count). Runtime: under 4 seconds each. Fold is the
slowest at about 3.6 s.

## 3. The zero-float qualification (finding 2)

The PR #3 body and synthesis report call five instruments "100%
zero-float exact rational". Literally, by file:

- `two_loop_omitted_variable.py`, `portal78_homotopy_bregman_bridge.py`,
  `fold_sheaf_collapse.py`: no float usage found. Claim holds.
- `tropical_quotient_sheaf_bridge.py`: one float use, rounding an exact
  bracket for display in JSON output. Cosmetic only.
- `optimal_inertia_rank.py`: float rounding for display in about a dozen
  output fields, and one real gate. The entropy-bridge check (around
  line 730) computes a Shannon effective rank with `math.exp` and
  `math.log` over floats and raises `RuntimeError` on a `1e-12` tolerance
  comparison. So one PASS/FAIL path in the file is float-decided. The
  underlying Rényi ordering H0 ≥ H1 ≥ H2 is a known theorem and the
  sampled spectra sit far from the tolerance, so the practical risk is
  negligible. But "100% zero-float" is not literally true of this file,
  and an exact project should not say it is. Recommended repair: state
  "exact rational cores" in prose, or replace the entropy gate with an
  exact comparison of the Rényi-2 quantity (already computed as a
  `Fraction`) against rank bounds that need no transcendental.
- `double_slit_continuum_observer.py` (seventh instrument): float-free in
  theorems and checks. The single literal `0.5` is an adversarial input
  its parser must reject. Its own wording ("ZERO floats anywhere in any
  theorem, check") is accurate.

Verdict: the exact mathematics is unaffected. The marketing line needs
the qualifier. The site in PR #4 repeated the strong wording and has been
fixed to match (commit `e0729ef`).

## 4. Sampled instrument: fresh-seed tomography

`audit_continuum_probes.py` was run at the default seed (output matches
the report to the printed digits: lag-0 z = +3.82, lag-12 z = +3.69,
median lag −11, raw CKA 0.989 on drifts) and at seeds 99999 (reported),
12345 and 7 (both unreported before this audit). Against the report's own
falsification bars (both coupled z-means above 3.0, lag-12 median in
[−13, −9], all seven nulls within |z| < 1.5):

| Seed | lag-0 z | lag-12 z | median lag | worst null | Verdict |
|---|---|---|---|---|---|
| 20261120 | +3.82 | +3.69 | −11 | +0.84 | PASS |
| 99999 | +4.00 | +3.99 | −11 | −0.46 | PASS |
| 12345 | +3.39 | +3.73 | −11 | +0.59 | PASS |
| 7 | +4.73 | +4.57 | −11 | −0.88 | PASS |

One reporting slip: the synthesis report swaps the GL(4) and GL(5)
spectral-invariance digits. Live output is GL5 = 1.332e-15 and GL4 =
1.11e-15. The report prints GL(4) = 2.887e-15, GL(5) = 1.11e-15. Both are
at float noise floor, so the claim stands and the digits do not.

Environment note: the instrument needs `numpy` and `scipy`, unpinned, with
no requirements file in the repo. Sampled reproducibility will drift with
library versions. Local run used numpy 2.5.4, scipy 1.18.1.

## 5. Independent checks (zero shared code)

Written fresh for this audit, importing nothing from the repository:

- **Möbius cross-ratio cancellation.** For
  `q(p. R, c) = (rp + c(1−p)) / (rp + (1−p))`, the cross-ratio of four
  images equals the cross-ratio of the four points for every tested
  rational `(r, c)`, `q(1) = 1` always, and the non-Möbius variant
  `r(p) = 6 + 10p` breaks it. The instrument's own output reproduces its
  9/7 and 27/19 at its chosen seeds. Mechanism is textbook projective
  invariance (N0 as mathematics, N1 as packaging, which is how the
  synthesis report labels the surrounding work).
- **Two-loop Pythagoras and phase boundary.** Own exact Gram–Schmidt over
  ℚ⁵: `‖r_adapt‖² = ‖r*‖² + e₁²/‖p₁‖²` held in 400/400 random trials, and
  the fresh-anchor identity with its `0 < ρ/κ < 2` iff held in 400/400.
  (This auditor's first checker had a non-orthogonalised projection bug
  that produced spurious failures. It was repaired before any verdict,
  per steelman-before-falsify.)
- **Fold parametrizations.** Both rational curves satisfy their conic
  identities exactly at sampled rational points, including the reported
  interior point (16/11, 7/11) and endpoint (0, 1).
- **Hadamard stress.** Sylvester H₈ built from scratch: H₈² = 8I,
  symmetric, trace 0, so σ* = 2I₈ + H₈ obeys (σ* − 2I)² = 8I with a 4/4
  eigenvalue split, matching the claimed (4, 4, 0) auxetic inertia.
- **Cubic Bregman cone.** The [3,4,5] → [5,12,13] Pythagoras identity
  holds exactly under the instrument's generator (values 3865/3 =
  37/3 + 1276 reproduced with own Fraction code).
- **Sorkin structure.** Independently implemented in JavaScript for the
  site with a different model: I_ABC = 0 in the linear regime, looped
  κ₃ intensity-invariant, quartic term scaling as λ⁴, all asserted in
  the site tests. Consistent with AUDIT-054's regime split.
- **Original prototype shadow.** PR #2's own `probe_window`, run
  first-hand on two independent linear drifts, reports manifold lock
  0.9998 (a false coupling), and 0.01 on independent white noise. The
  AUDIT-007R falsification of the raw prototypes is confirmed on the
  original artifact, not only on the audit's re-implementation.

Not independently re-derived in this audit (relied on instrument runs
plus output cross-checks against the reports): the tropical peeling
dominance numbers (124 / 112 / 64), the full fold rank-1 collapse
machinery beyond the items above, the Maslov–Doob homotopy traces, and
the double-slit GKSL and deck-splitting algebra beyond its R5 tests and
certificate equality. A full clean-room rewrite of those four would be
the next audit tier.

## 6. Textual record, privacy and hygiene

- **No secrets.** Token-shaped patterns (GitHub, OpenAI-style, AWS,
  private keys, api-key and password assignments) return zero hits over
  every revision. Commit author emails are public in history, as usual.
- **Session integrity claim is true.** The exported JSON in PR #1 hashes
  to exactly the SHA-256 and byte size printed inside `root.md`.
- **But the content deserves an owner decision.** Both PR #1 and PR #2
  publish a verbatim 41-turn session with the repository owner in a
  public repository. It includes dictated speech with disfluencies and
  a model description of the owner's room from a live video feed
  (furniture, lighting, screens). No names, addresses or credentials
  were found. One Google Drive sharing link sits in the transcript. It
  returns HTTP 401 unauthenticated today, so exposure depends on Drive
  sharing settings the owner controls. Recommendation: decide on the
  record whether verbatim personal sessions belong in the public
  history. Git history is forever. Deleting the branches later does not
  unpublish fetched clones. This audit changed nothing here.
- **Duplication.** `root.md`, `root.txt` and `root.rtf` are one identical
  blob (the `.rtf` is plain text, not RTF). The framework essay appears
  twice in PR #1 at 97.8% sequence similarity plus a third copy as a
  735 KB genuine RTF. The same session is carried by both PR #1 (JSON)
  and PR #2 (embedded in a Python literal).
- **Dataset claims without provenance.** The anthology's ten-form atlas
  names real records (a LIGO-style GPS stamp, a Kepler EPIC target,
  CHB-MIT EEG `chb01_03.edf`, Planck PR3-SMICA) with precise constants,
  but the repo holds no data, no download record and no analysis code
  that touches those files, and the transcript shows the model
  narrating without data access. Treat every atlas constant as
  unverified narrative. The site already labels it that way.
- **Prototypes are inert.** The four PR #2 Python files import cleanly
  but define functions only: no entry points, no tests, no data. As
  scripts they do nothing and exit 0.
- **PR hygiene.** PR #1 and PR #2 bodies do not describe their diffs in
  reviewable terms. PR #3's body covers the six synthesis instruments
  well but never mentions the double-slit directory that is 5 of its 12
  files. Instruments cross-import siblings, so they run from the repo
  root (script directory on `sys.path`, verified) but are not
  independent of each other as code. Only the double-slit work carries
  a separate test file.

## 7. Site PR #4 (auditing own work)

Tests re-run green (18/18). The vendored Eido pin still equals upstream
`main` (`be276652`), and the atlas byte sizes match the expedition
branch exactly for all seven files. Findings:

1. The page repeated the "no floating point at all" overstatement from
   section 3. Fixed in commit `e0729ef` (page, atlas readout and
   condensed variants), with tests still green.
2. Minor: the Pages workflow pins actions by major tag
   (`actions/checkout@v4`) where upstream Eido pins full SHAs. Lower
   supply-chain rigour than the donor project. Worth tightening on a
   later pass. Not a correctness issue.

Also noted: the page's "independent verifier" phrasing means separate
audit agents inside this project ecosystem (the AUDIT-xxx trail), not
external peer review. The record section could say so in one clause.
Left as a recommendation rather than another churn commit during review.

## 8. Recommendations, in order

1. Decide the privacy question on PR #1 and PR #2 session material
   explicitly before merging either. If merging, consider redacted
   distillation over verbatim transcripts for `main`.
2. Add a license. Without one the verified instruments are all-rights-
   reserved by default, which undercuts their reuse elsewhere in the
   ecosystem. Copyright in model-generated session text also needs an
   owner position before licensing it.
3. Soften "100% zero-float" to "exact rational cores" in the synthesis
   report, or remove the one float gate in `optimal_inertia_rank.py`.
4. Fix the swapped GL(4)/GL(5) digits in the synthesis report.
5. Update PR #3's body to cover the double-slit directory, and give
   PR #1 and PR #2 reviewable descriptions before asking for merges.
6. Pin `numpy` and `scipy` (requirements file) for the sampled
   instrument, and add CI that runs the instruments the way PR #4's
   workflow runs the site tests.
7. Deduplicate on merge: one copy of the essay, one of the session,
   correct file extensions, drop the 735 KB RTF.
8. Keep novelty labels at N1 until a full-text prior-art pass is on
   record for the fold theorems. The double-slit N1 self-label with
   its eleven-item quarantine is the model to copy.

## 9. Bottom line

The repository's centre of gravity is sound where it is checkable: the
audited instruments reproduce exactly, the sampled detector survives
unseen seeds, the falsified prototypes were falsified by the project's
own audit and that verdict holds first-hand, and the one integrity hash
in the transcripts is honest. The weaknesses are presentational and
curatorial rather than mathematical: one overstated zero-float line, one
swapped pair of digits, unlabelled session narrative that could be
mistaken for measurement, no license, and personal session material in
public history awaiting an explicit owner decision.
