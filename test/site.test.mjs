// Checks for the static site: links and imports resolve, the condensed
// variants match the page, the vendored Eido files are still
// byte-identical to the pinned upstream commit, and the atlas agrees
// with itself between the HTML links and the instrument data.
import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
import { validateCondensed } from "../src/condense.js";
import { parseHtml } from "./helpers/html-passages.mjs";

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const read = (rel) => fs.readFileSync(path.join(repo, rel), "utf8");
const html = read("site/index.html");

function resolves(fromFile, ref) {
  const clean = ref.split("#")[0].split("?")[0];
  if (!clean) return true;
  const target = path.resolve(path.dirname(fromFile), clean);
  if (!target.startsWith(repo)) return false;
  if (fs.existsSync(target) && fs.statSync(target).isFile()) return true;
  return fs.existsSync(target) && fs.statSync(target).isDirectory() && fs.existsSync(path.join(target, "index.html"));
}
const isExternal = (r) => /^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/i.test(r);

test("the page has a title, one main landmark and the shared shell", () => {
  assert.match(html, /<title>[^<]+<\/title>/);
  assert.equal([...html.matchAll(/<main id="main">/g)].length, 1);
  for (const need of ["assets/site.css", "assets/continuum.css", "assets/theme.js", "assets/loom.js", "assets/continuum.js", "../css/reading-weave.css", "../css/condense.css"]) {
    assert.ok(html.includes(need), `index.html does not load ${need}`);
  }
});

test("every relative href, src, import and fetch resolves", () => {
  const files = ["site/index.html", "site/assets/continuum.js", "site/assets/continuum-math.js"];
  const bad = [];
  for (const rel of files) {
    const abs = path.join(repo, rel);
    const text = fs.readFileSync(abs, "utf8");
    const refs = [
      ...[...text.matchAll(/\b(?:href|src)\s*=\s*"([^"]*)"/g)].map((m) => m[1]).filter((r) => r && !isExternal(r)),
      ...[...text.matchAll(/\bfrom\s+"(\.{1,2}\/[^"]+)"/g)].map((m) => m[1]),
    ];
    for (const ref of refs) if (!resolves(abs, ref)) bad.push(`${rel}: ${ref}`);
    // loadCondensed fetches relative to the document, not the script.
    for (const m of text.matchAll(/\bloadCondensed\(\s*"([^"]+)"/g)) {
      if (!resolves(path.join(repo, "site/index.html"), m[1])) bad.push(`${rel}: ${m[1]} (document-relative)`);
    }
  }
  assert.deepEqual(bad, []);
});

test("every in-page anchor lands on a section that exists", () => {
  const ids = new Set([...html.matchAll(/\bid="([^"]+)"/g)].map((m) => m[1]));
  for (const m of html.matchAll(/href="#([^"]+)"/g)) assert.ok(ids.has(m[1]), `#${m[1]} has no target`);
});

test("site/condensed.json matches every passage and section (strict)", () => {
  const data = JSON.parse(read("site/condensed.json"));
  const { passages, sections } = parseHtml(html, { headings: ["h2"] });
  assert.ok(passages.length >= 30, `expected the article's passages, got ${passages.length}`);
  assert.equal(sections.length, 7);
  assert.deepEqual(validateCondensed(data, { against: { passages, sectionIds: sections.map((s) => s.id) }, strict: true }), []);
  for (const p of passages) assert.ok(p.hash in data.blocks, `no variants for ${p.hash}`);
});

// Moissanite-Labs/weft-eido at be27665255d9aa2553060d275f7d1b1b3306c703.
// A failure here means a vendored file was edited locally (see
// THIRD-PARTY.md) or the pin moved without updating this table.
const VENDORED = {
  "src/aesthetic-mixer.js": "12b4b73e115710c796d6e9826c133e8f6cac9a70f3ae0fc150cb0e6b72c0a094",
  "src/cell-layout.js": "df9b127fcfd3506df1291c8b764a90f61eca833e9e6034253f8fd44bb192b83c",
  "src/condense.js": "6337e250dc49ee1e6e95ff257b4666e8834ff9d87b1375e951239f8ac3636fdf",
  "src/glyph-font.js": "5f4fdad78ebd828c43818c8b7a5e0acc40fae33aeca2b17c3d4cd55c0bc7ea95",
  "src/reading-weave.js": "855cb610d0abd5b323e5b98ac41f5af7614856f84aee06717200414bf50a7fae",
  "src/simplex-pad.js": "1dcd02f81ed38cb85e4d0337a2c71d9edbcdaeabd6dd6a19afaffb05c81f040d",
  "css/condense.css": "4e139e0eef1e14705ff40970abb962d9793c57dc1d24873fdc387b03ef57b5b9",
  "css/reading-weave.css": "47d30add85d8626c4e55b1587a5086b7854d6908df4840d6a6b3f663eedf7daa",
  "site/assets/theme.js": "46bc37f73c5bab0c59d5213ed665f659a6d6556dfa8619bf2a6d3ca4c9777158",
  "site/assets/loom.js": "56421a33fc1c4ad1a616f6b78b2a773153035ef6bd9e53b2d7eb686fc8a6b414",
  "site/assets/loom-core.js": "2743194ea31f8c1fbb9e6f1eb55657ea9a82b6b2f34712290257a2e513964d7e",
  "site/assets/site.css": "ac679a78826d3bca34142bca0db214333381cce8af224fe9ee6763a30d33484b",
  "test/helpers/html-passages.mjs": "abcbd4919423945217998ba5b42dcd44e2a8fb099b1fc9a093bd378e5b42db6f",
};

test("vendored Eido files are byte-identical to the pinned commit", () => {
  for (const [rel, want] of Object.entries(VENDORED)) {
    const got = crypto.createHash("sha256").update(fs.readFileSync(path.join(repo, rel))).digest("hex");
    assert.equal(got, want, `${rel} differs from the pinned weft-eido commit`);
  }
});

test("the atlas HTML links and the instrument data agree", () => {
  const js = read("site/assets/continuum.js");
  const rows = [...js.matchAll(/\{\s*name: "([^"]+)", file: "([^"]+)", bytes: (\d+), audit: "([^"]+)", family: "([^"]+)", href: "([^"]+)"/g)];
  assert.equal(rows.length, 7, "expected seven instruments");
  for (const [, , file, bytes, audit, , href] of rows) {
    assert.ok(Number(bytes) > 0, `${file} needs a byte size`);
    assert.ok(html.includes(`href="${href}"`), `index.html does not link ${file}`);
    assert.ok(html.includes(`>${file}</a>`), `index.html does not name ${file}`);
    assert.ok(html.includes(audit), `index.html does not carry ${audit}`);
  }
});
