# Third-party code in this repository

The site in `site/` runs on **Eido**, the design language of ML Weft,
from [Moissanite-Labs/weft-eido](https://github.com/Moissanite-Labs/weft-eido),
vendored unmodified at commit
`be27665255d9aa2553060d275f7d1b1b3306c703` (2026-11-17, its `main` at
the time of copying). Eido code is Apache-2.0 and its documentation is
CC BY 4.0. The full license text is in `licenses/Apache-2.0.txt` and
the upstream notice in `licenses/NOTICE-weft-eido`.

Vendored files, byte-identical to upstream (verify with `npm test`:
`test/site.test.mjs` pins each file's SHA-256, or diff against the
pinned commit):

- `src/aesthetic-mixer.js`, `src/simplex-pad.js`, `src/cell-layout.js`,
  `src/glyph-font.js`, `src/reading-weave.js`, `src/condense.js`
- `css/reading-weave.css`, `css/condense.css`
- `site/assets/theme.js`, `site/assets/loom.js`,
  `site/assets/loom-core.js`, `site/assets/site.css`
- `test/helpers/html-passages.mjs`

Written for this repository, not part of Eido:

- `site/index.html`, `site/condensed.json`
- `site/assets/continuum-math.js` (the pure instrument mathematics),
  `site/assets/continuum.js` (the page wiring),
  `site/assets/continuum.css`
- `test/continuum-math.test.mjs`, `test/site.test.mjs`,
  `tools/build-condensed.mjs`
- `.github/workflows/pages.yml` (adapted from the Eido workflow, with a
  test step added before assembly)

To update Eido, copy the files again from a newer upstream commit,
update the pin above, and run `npm test`. Do not edit the vendored
files in place: local changes belong in the continuum files, so the
diff against upstream stays empty and auditable.
