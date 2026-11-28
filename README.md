# continuum
theory of reality as transformations within a single continuum 

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

## Work on the site

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
instruments the site draws on, superseding #3, pending merge).
