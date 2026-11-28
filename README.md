# continuum
theory of reality as transformations within a single continuum

## Contents

| Path | What it is |
|---|---|
| [`periodic-table-invariants/`](periodic-table-invariants/README.md) | Self-contained, standard-library-only Python verifier for a 16-entry "Periodic Table of Invariants" (`PT-01`..`PT-16`), its standalone test suite, and the two committed JSON artifacts the verifier recomputes and checks byte-for-byte. |
| [`.github/workflows/verify-periodic-table.yml`](.github/workflows/verify-periodic-table.yml) | CI job (Python 3.11 / 3.12 / 3.13) that runs the verifier and test suite. |
| [`site/`](site/index.html) | The thesis as a single page on the Eido loom, published at <https://foundation-0.github.io/continuum/>. |

## Scope (what is and is not verified)

- **Verified in-module:** `82` exact integer/`Fraction` checks (`54` four-class obstruction + `13` opposing-pair + `15` modular-flow) that back all `16` table entries. No floats, true division, or logarithms are used; a static AST allowlist scan over both Python files enforces this, and the result is recorded in the certificate.
- **Verified on disk:** `--check` recomputes everything and requires `periodic_table_certificate.json` and `periodic_table_of_invariants.json` to match the canonical build byte-for-byte. Malformed input (symlinks, FIFOs or other non-regular files, files over `1 MiB`, BOM/CRLF/invalid UTF-8, float/NaN literals, duplicate keys, integers over `1024` digits, nesting deeper than `64`) is refused with exit code `2` and a single `FAIL ...` line on stderr, never a traceback.
- **Not verified by the code:** the verifier checks only the exact arithmetic. It does not check the historical attributions attached to each entry, and it makes no empirical, physical, or power/energy claims. Nothing is fetched over the network, and there are no external dependencies.

## Run locally

Requires Python 3.11+ on a POSIX system (the file reader uses `O_NOFOLLOW` / `O_NONBLOCK`).

```bash
cd periodic-table-invariants
python3 -I -B verify_periodic_table_invariants.py --check     # prints PASS ... on success, exit code 0
python3 -I -B test_periodic_table_invariants.py               # prints nothing on success, exit code 0
```

CI runs both commands in three interpreter modes (`-I -B`, `-I -O -B`, `-I -B -W error`) and requires the three `--check` outputs to be byte-identical. Before running anything, CI checks both scripts against SHA-256 hashes pinned in the workflow file, so changing either script means updating those pins in the same change. The pins catch accidental or partial edits. They are not a signature: anyone who can edit the scripts in a PR can edit the workflow too.

## Site

**Site:** <https://foundation-0.github.io/continuum/> — the thesis as a
single page on a single medium, with live instruments for its claims:
twist a projective probe and watch the cross-ratio stand still, couple
a probe to the slits and run the Sorkin test, coarse-grain a field and
read the commutation defect, and skim to watch the prose condense.
Every claim on the page is graded (exact, sampled, proposed,
falsified) in its record section.

The interface is [Eido](https://github.com/Moissanite-Labs/weft-eido),
the design language of ML Weft, vendored unmodified. Provenance and
the pinned upstream commit are in [THIRD-PARTY.md](THIRD-PARTY.md).

Node 20 or newer, no dependencies, no build step:

```bash
npm test                      # instrument math, links, condensed variants, vendor pin
python3 -m http.server 8000   # then open http://localhost:8000/site/
node tools/build-condensed.mjs  # regenerate site/condensed.json after editing variants
```

Pushes to `main` test and publish the site with GitHub Pages
(`.github/workflows/pages.yml`).

The research content itself lives in the open pull requests: #1 (the
framework), #2 (the anthology of session forms) and #16 (the audited
instruments the site draws on, now on main, superseding #3).
