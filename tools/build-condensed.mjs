// Authors site/condensed.json for site/index.html.
//
// The variants below are the editorial record: each passage of the page
// at Concise, Terse and Caveman, plus each section's folded headings,
// one-line summary and simple-words version. They are keyed here by the
// passage hash that src/condense.js computes, with the opening words of
// the passage in a comment so the pairing can be reviewed. Run with:
//
//   node tools/build-condensed.mjs
//
// The script refuses to write anything unless every passage on the
// page has variants, every variant is no longer than the level above
// it, and validateCondensed (strict) is clean. Edit the variants here,
// never the generated JSON.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { validateCondensed } from "../src/condense.js";
import { parseHtml } from "../test/helpers/html-passages.mjs";

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

// [Concise, Terse, Caveman] per passage hash.
const BLOCKS = {
  // Reality as transformations within a single continuum...
  "2518cac5": [
    "Reality as transformations in one continuum. The real part is the invariant that survives every change of net.",
    "One continuum, many nets. Real = what survives changing nets.",
    "One wave. Real bit stays when net changes.",
  ],
  // This page is one document on one medium...
  "5ebce608": [
    "One document, one medium: the threads behind the text are that sum, computed live on a clock that runs all visit. No other pages. Slicing a continuum into labelled fragments is where theories fracture, so this site slices as little as a page can.",
    "One page, one medium, live threads, one clock. Cutting continua into named bits breaks theories. This site cuts least.",
    "One page only. Threads move live. Cutting wave into named bits breaks ideas. Here: almost no cuts.",
  ],
  // Every instrument and every formal language...
  "c57f6392": [
    "Instruments and languages assume things at points on an external clock. We grid a seamless continuum, name the pieces, and theories break at the seams between names.",
    "Tools assume things, points, outside clock. We grid the continuum, name pieces. Theories break between names.",
    "We chop smooth world into named bits. Ideas break where bits join.",
  ],
  // The mismatch is structural...
  "615a3670": [
    "The mismatch is structural. Symbols are countable, ℵ<sub>0</sub>. The continuum is uncountable, 𝔠. Almost all of it falls between symbols forever, at any resolution.",
    "Symbols: countable ℵ<sub>0</sub>. Continuum: uncountable 𝔠. Most of reality falls between symbols, always.",
    "Words can be counted. Smooth world cannot. Most of world slips past words.",
  ],
  // The way out is not to give up rigour...
  "878ba0ab": [
    "Keep rigour, change the target: knowledge is what stays fixed under every change of net. Twist the probe, resample, zoom. What moves is apparatus. What stands still may be real. This page builds that idea four ways, then asks what would falsify it.",
    "Keep rigour. Knowledge = fixed under all net changes. Moves with probe: apparatus. Stands still: maybe real.",
    "Know what stays when net twists. Still bit may be real.",
  ],
  // Start with your own apparatus...
  "e181df6d": [
    "Your apparatus first. The triangle is a style point: weights sum to one, hue is their circular mean, so two reds never make cyan. Drag it: colour, spacing, rounding change. Every number below stays put. A twistable frame over steady content is the thesis in miniature.",
    "Triangle = style point. Weights sum to 1, hue goes round the circle. Drag: page changes, numbers below do not.",
    "Drag triangle. Page colours change. Numbers below stay same. Frame moves, truth does not.",
  ],
  // Four inherited habits...
  "e3ff619f": [
    "Four habits must be replaced at the root first. Each replacement is standard mathematics, read in one direction.",
    "Four habits to replace first. Standard maths, read one way.",
    "First fix four old habits.",
  ],
  // Replace points with overlapping relations...
  "39dc42b0": [
    "<strong>Points become overlapping relations.</strong> A point takes infinite energy to resolve. Pointless topology uses regions and overlaps; Yoneda says an object is its web of relations. Map transformations, skip substance.",
    "<strong>Points to relations.</strong> Points cost infinite energy. Use overlaps. A thing = its relations.",
    "<strong>No dots.</strong> Dots cost too much. Thing is how it touches other things.",
  ],
  // Replace the external clock...
  "c8212723": [
    "<strong>External clocks become intrinsic flow.</strong> A faithful state generates its own flow, σ<sub>s</sub><sup>ω</sup>(a) = Δ<sub>ω</sub><sup>is</sup> a Δ<sub>ω</sub><sup>−is</sup>. Time becomes a parameter woven from correlation inside the system.",
    "<strong>Clock becomes inner flow.</strong> States make own time from correlation. No outside stage.",
    "<strong>Time inside.</strong> No outside clock. System makes own time.",
  ],
  // Quotient out the observer...
  "a6ed4db9": [
    "<strong>Quotient out the observer.</strong> Observation is coupling, never passive readout. Collect every probe setting as a group G<sub>obs</sub>. What changes under twisting is apparatus. Data is the invariant part all views share.",
    "<strong>Remove the observer.</strong> Looking is touching. Twist probe every way. Shared part = data.",
    "<strong>Twist the tool.</strong> What changes is tool. What stays is data.",
  ],
  // Unify the senses as one bundle...
  "a3a5b056": [
    "<strong>Unify the senses as one bundle.</strong> Sight, sound, pressure, heat: local sections of one bundle. Failure to glue is curvature and obstruction, not noise. A pattern is a hole that refuses to contract under stretching or resampling.",
    "<strong>Senses = one bundle.</strong> Bad joins = curvature, not noise. Pattern = hole that will not shrink away.",
    "<strong>All senses one cloth.</strong> Rip in cloth is clue, not noise.",
  ],
  // The third habit is the one you can test...
  "282bbfc6": [
    "Test the third habit by hand. Four points, one projective probe φ(x) = (αx + β)/(γx + 1). Every coordinate moves; the cross-ratio does not, because projective maps preserve it. The exact instruments use the same trick: cross-ratios 9/7 and 27/19 cancel two unknown observer parameters.",
    "Hands on: four points, projective probe. Coordinates move, cross-ratio stays. Exact tools use this: 9/7 and 27/19 cancel observer unknowns.",
    "Move sliders. Points slide. Special four-point number stays. Big tools use same trick.",
  ],
  // Notice what kind of fact survives...
  "329225b8": [
    "What survives is a relation among four things, not a position or a length. Facts tied to one probe setting describe the probe. Relations every probe preserves are the finite observer's closest approach to the continuum.",
    "Survivor: a four-way relation, not a place. Probe-dependent facts describe the probe.",
    "Still thing is link between things, not spot. Spot belongs to tool.",
  ],
  // Strip the labels, grids and single-sense silos...
  "c6308af2": [
    "Without labels, grids and silos, unrelated streams show the same four transformations. Read as grammar: the few moves by which a continuum makes structure, repeated because they belong to the medium.",
    "Drop labels. Unrelated streams, same four moves. The medium's grammar.",
    "No names: all streams do same four tricks.",
  ],
  // Subtractive selection...
  "4b605d21": [
    "<strong>Subtractive selection.</strong> The continuum builds by cancellation: waves erase each other, and stationary-phase knots, δS = 0, persist. Zooming out repeats it: accidents die, universality classes remain. Reality forgets details, remembers symmetries.",
    "<strong>Building by erasing.</strong> Waves cancel; δS = 0 knots stay. Zoom out: details die, symmetries stay.",
    "<strong>Waves rub out.</strong> Left-over knot is thing. Far view kills detail, keeps shape.",
  ],
  // Symmetry fracture...
  "ab89e639": [
    "<strong>Symmetry fracture.</strong> Perfect symmetry has no features. Break G to H unevenly and defects get trapped, π<sub>k</sub>(G/H): walls, strings, vortices. A particle can be a topological scar that cannot be untied without tearing the medium.",
    "<strong>Broken symmetry.</strong> Even field: nothing to see. Uneven break traps knots. Particle as scar.",
    "<strong>Crack the pattern.</strong> Cracks trap knots. Knot acts like thing.",
  ],
  // Irreversibility as geometry...
  "8aba17aa": [
    "<strong>Irreversibility as geometry.</strong> Time's arrow is path asymmetry: Σ[Γ] = ln(dP[Γ]/dP[ΘΓ]). Where forward and backward fail to mirror, direction appears: ratchets, memory, ageing, cause.",
    "<strong>Time's arrow = lopsided paths.</strong> Forward ≠ backward gives memory, ageing, cause.",
    "<strong>One-way roads.</strong> Trip back differs. That makes past and future.",
  ],
  // Duality and emergent space...
  "5fda8c1f": [
    "<strong>Duality and emergent space.</strong> Unrelated descriptions are exact translations: L ⊣ R, τ ↦ −1/τ. Holographically, distance is built from correlation. Space is the shape of correlation, not its container.",
    "<strong>Duality.</strong> Strange maps translate exactly. Distance comes from correlation. Space = correlation's shape.",
    "<strong>Two maps, one land.</strong> Space grows from links, not box.",
  ],
  // The first move, selection by cancellation... (139 words)
  "86400ccf": [
    "Cancellation is where observation enters, at the double slit. Probe coupling γ fades fringes exactly: V = (1 − γ²)/(1 + γ²), D = 2γ/(1 + γ²), V² + D² = 1. Open a third slit and Sorkin's I<sub>ABC</sub> must vanish in any linear Born theory. Only two escapes exist, split by source intensity λ: looped coupling holds κ<sub>3</sub> fixed, a Kerr term grows the signal as λ<sup>4</sup>.",
    "Double slit: probe γ fades fringes, V² + D² = 1. Third slit: I<sub>ABC</sub> = 0 if linear. Looped: κ<sub>3</sub> fixed in λ. Kerr: signal grows λ<sup>4</sup>.",
    "Probe touches slits, stripes fade by exact rule. Third slit tests lie: bright-up splits two cheats apart.",
  ],
  // Read the regimes honestly... (102 words)
  "7da2835a": [
    "Honest reading shrinks the postulate. Fringe loss proves little: classical disturbance kills fringes too. The exact audit splits four regimes; only quantum coupling passes delayed-choice tests, where classical models are fenced by D² + V² ≤ 1 and CHSH ≤ 2 against an exact 14/5. A nonlinear continuum survives at a price: nonzero I<sub>ABC</sub> with λ<sup>4</sup> growth, bounded near 10<sup>−5</sup>.",
    "Fringe loss proves little; classical knocks kill fringes too. Four regimes split exactly. Nonlinear continuum: allowed, at a measured price.",
    "Faded stripes prove little. Four boxes, tests sort them. Bent world possible, must pay exact price.",
  ],
  // This figure is floating-point illustration...
  "c94b2582": [
    "This figure is browser floating-point. Its claims were checked in exact rational arithmetic in the atlas instrument. On any disagreement the exact instrument wins and this page is only the picture.",
    "Browser floats here. Exact rational checks in the atlas tool outrank this picture.",
    "Picture here uses round numbers. Real check uses exact fractions. Fractions win.",
  ],
  // The four moves do not happen once...
  "2c3d0e0d": [
    "The moves repeat across size, self-similar structure and abstraction levels. Discrete magnification λ<sup>n</sup> gives power laws a log-periodic heartbeat and complex exponents. Fractals become natural resting places of recursion, with a spectrum of dimensions.",
    "Moves repeat at every size. Stepwise zoom gives heartbeat power laws, complex exponents, fractal spectra.",
    "Same tricks big and small. Zoom in steps: wobbly laws, branching shapes.",
  ],
  // That raises a testable question...
  "38c7b22a": [
    "When is a level real, not just a summary? With fine dynamics T, coarse-graining π and candidate coarse dynamics T′, measure δ<sub>emg</sub> = ‖π∘T − T′∘π‖. A level is real when the defect nears zero while the coarse view still predicts and compresses.",
    "Real level test: δ<sub>emg</sub> = ‖π∘T − T′∘π‖ near zero, coarse view still predicting.",
    "Test a big view: two paths must agree. Agree well: level is real.",
  ],
  // The field above is fixed... (146 words)
  "0312f47b": [
    "The field is fixed: long waves, a bump, a short wave, a checkerboard. Block averaging kills the short parts by the predicted sinc factors and keeps the long wave. Reusing the fine step ν at coarse scale fails, defect past 0.9; renormalising to ν/b² drops it below 0.05. Commutation is a test levels pass or fail, and the one-line slogan failed it: linear and tropical defects split in both directions.",
    "Averaging kills fine detail, keeps long wave. Same ν fails (0.9); ν/b² passes (under 0.05). Slogan failed as monolith; split by semiring.",
    "Blur kills small pattern, keeps big wave. Wrong big-step fails test, fixed step passes. One-line slogan broke; now two tests.",
  ],
  // If relations are what survive... (99 words)
  "499aef8b": [
    "Organise knowledge by mathematical shape, not by discipline. The sessions produced a first taxonomy: ten channels read without labels, each a mathematical sculpture. Treat it as a looking-map, not measurement: they are exploratory sessions, and later audit found the raw session detectors easy to fool.",
    "File by shape, not subject. Ten channels, ten sculptures. A looking-map, not measurements; raw detectors were later fooled in audit.",
    "Sort by shape, not school subject. Ten wave shapes. Map for looking, not proof.",
  ],
  // What the repository can stand behind today...
  "31cd3da4": [
    "What stands today is narrower and stronger: seven runnable instruments, six built on exact rational arithmetic, independently audited with falsification criteria. Below, cell area is file size in bytes alone. Threads join the exact family and the one sampled instrument.",
    "Solid today: seven audited tools, six exact rational. Cell area below = bytes only.",
    "Strong bit: seven checked tools, exact fractions. Box size = file size.",
  ],
  // Each instrument runs on the Python standard library...
  "a2da1802": [
    "Each runs on the Python standard library and prints a reproducible verdict.",
    "Standard-library Python with byte-for-byte reproducible verdicts.",
    "Plain Python. Same answer each run.",
  ],
  // A page about invariants should say plainly...
  "f1ba1b87": [
    "This page grades its own sentences, read from the repository on 22 November 2026. Exact: rational arithmetic, independently verified. Sampled: stated cases, null controls. Proposed: argued, untested. Falsified: tested, wrong as stated, repair named.",
    "Self-grading, read 22 Nov 2026. Exact, sampled, proposed, falsified: definitions as in the table.",
    "Page marks own homework: exact, sampled, idea, or wrong.",
  ],
  // The raw session exports...
  "63628599": [
    "Raw session exports stay in the pull requests, not republished here. Working transcripts make provenance, not reading. Every strong sentence above points to a branch, pull request or test that can check it.",
    "Raw transcripts not republished. Strong sentences point to checkable branches, requests, tests.",
    "Rough talk stays in files. Big claims point to checks.",
  ],
  // One more separation matters...
  "574ed070": [
    "Verified instruments are not evidence for the whole framework. They load-test particular bridges: a peeling tower, a rank collapse, a regime split. Some planks held, several snapped and were replaced. The crossing as a whole is still an open program.",
    "Checked tools test single bridges, not the continent. Some planks held, some snapped. Crossing still open.",
    "Strong small bridges do not prove whole land. Some boards broke. Road still open.",
  ],
  // For anyone who wants to push perception...
  "ce2c546a": [
    "The framework ends in four working instructions. None needs new physics. All can start with existing instruments.",
    "Four instructions to end. No new physics needed.",
    "Four jobs. Start with tools we have.",
  ],
  // Compute in the wave before digitising...
  "f018a8bb": [
    "<strong>Compute in the wave first.</strong> Let interference extract invariants at propagation speed; convert to symbols only when spectral and topological parts remain.",
    "<strong>Wave first.</strong> Interfere first, digitise last.",
    "<strong>Wave thinks first.</strong> Numbers late.",
  ],
  // Learn operators, not grids...
  "81f68291": [
    "<strong>Learn operators, not grids.</strong> Train on function spaces with consistency across resolutions and modalities, not grid imitating grid under labels.",
    "<strong>Operators over grids.</strong> Consistency across zoom and sense.",
    "<strong>Rules, not grids.</strong> All zooms same.",
  ],
  // Never trust a stationary sensor...
  "6f631fdb": [
    "<strong>Never trust a stationary sensor.</strong> Vary coupling, basis, bandwidth, geometry; discard what moves with the probe. The residue is the observer-quotiented core.",
    "<strong>Move the sensor.</strong> Drop what follows the probe. Keep the residue.",
    "<strong>Wiggle the eye.</strong> What follows eye is eye. Rest is world.",
  ],
  // Build the table of invariants, not nouns...
  "9df1fa31": [
    "<strong>Table of invariants, not nouns.</strong> File by shape: shears, split multiplets, rank collapses, resonance lattices, commutation strata. Disciplines follow shapes.",
    "<strong>File by shape.</strong> Shears, splits, collapses, lattices, strata.",
    "<strong>Sort by shape.</strong> Names come last.",
  ],
  // A paradox sits at the centre...
  "e219e130": [
    "The paradox stays. Frictionless resonance would erase distortion and distinction together: no cut, no memory, no knower. The fold that distorts is the fold that lets awareness exist. Stay inside the frame, cancel its biases against themselves, read the grammar through the cut.",
    "No cut, no knower. The distorting fold enables awareness. Cancel lens biases against each other; read through the cut.",
    "Cut hurts view, cut makes viewer. Use lenses against lenses. Peek through crack.",
  ],
  // This page tries to practise its own instructions... (130 words)
  "7835a0bb": [
    "This page practises at page scale: one document, style as a continuous point, a title from checkable bits, figures that compute live with numbers beside curves. It also notices reading: skim and prose condenses in steps, with a visible score and an off switch. Read passages never change, the score stays in your browser, print is always full text.",
    "Page does its own lesson: one flow, point-style, live numbers. Skim: text shrinks in steps, switch provided. Print: full text.",
    "Page walks talk: one flow, live sums. Skim and words shrink. Off switch there. Print shows all.",
  ],
  // The page runs on Eido...
  "de2ce9d5": [
    "The page runs on <a href=\"https://github.com/Moissanite-Labs/weft-eido\">Eido</a>, ML Weft's design language, vendored unmodified under Apache-2.0: style as a point, value-encoded layout, bitmask glyphs, text answering reading. Same philosophy as the thesis, for interfaces. Take modules from Eido, instruments from here, check both.",
    "Runs on <a href=\"https://github.com/Moissanite-Labs/weft-eido\">Eido</a> (Apache-2.0), copied untouched: point-style, glyphs, reading text. Check both projects yourself.",
    "Page wears Eido cloth, copied clean. Check cloth and tools yourself.",
  ],
};

// Folded headings per section: [Concise, Terse, Caveman, TL;DR heading, ELI5 heading].
const HEADINGS = {
  thesis: ["What survives a change of net", "What survives", "What stays", "Survivors", "The bit that stays"],
  frame: ["Dissolving the frame", "The frame dissolves", "Melt the frame", "Frame", "Changing the glasses"],
  grammar: ["The generative grammar", "The grammar", "Four moves", "Grammar", "How waves make things"],
  scale: ["The vertical axis", "Up and down scales", "Big and small", "Scales", "Zooming out"],
  atlas: ["A table of invariants", "The table", "Shape table", "Atlas", "A chart of shapes"],
  record: ["Proven and proposed", "The record", "Marks", "Record", "What we know, what we guess"],
  program: ["The program ahead", "What to do", "Jobs", "Program", "What to try next"],
};

const TLDR = {
  thesis: "Symbols are countable, the continuum is not: trust only what survives changing nets.",
  frame: "Relations over points, inner time, quotient the observer, one bundle per phenomenon.",
  grammar: "Cancellation, fracture, irreversibility, duality: four moves, tested live at the slits.",
  scale: "A level is real when coarse-graining commutes with dynamics, defect measured here.",
  atlas: "Ten session shapes as a map; seven exact audited instruments as the solid ground.",
  record: "Framework proposed, two early claims falsified and repaired, seven instruments verified.",
  program: "Compute in waves, learn operators, move sensors, file by shape; keep the cut honest.",
};

const ELI5 = {
  thesis: "Imagine fishing with different nets. The fish shape that every net agrees on is the bit worth believing. Words can list only countably many things, but the smooth world has more, so most of it slips between words.",
  frame: "Four swaps: describe things by how they touch others, let systems keep their own time, twist your measuring tools and keep only what stays, and treat all senses as one joined-up sheet with telling rips.",
  grammar: "Waves mostly cancel out and the leftovers become things. Fair patterns crack and trap knots. Trips that differ backwards make past and future. Different maps can describe the same land exactly, and space grows from links.",
  scale: "Squinting at a picture blur destroys small detail but keeps big shapes. A blurry view earns trust when blurring then changing matches changing then blurring. Here we measure that match, and fixing the step size makes it pass.",
  atlas: "First a picture book of ten wave shapes from old exploring sessions, fun but not proof. Then seven small computer programs checked very carefully with exact fractions. The programs are the part you can lean on.",
  record: "Honest marks for every big claim. The main idea is still a guess with a plan. Two early tries failed tests and got fixed. Seven little programs passed hard exact checks done by separate checkers.",
  program: "Four jobs: let real waves do early thinking, learn rules that work at every zoom, keep wiggling your instruments so tool effects fall away, and sort knowledge by shape. The viewing cut can never vanish, so use it honestly.",
};

const html = fs.readFileSync(path.join(repo, "site/index.html"), "utf8");
const { passages, sections } = parseHtml(html, { headings: ["h2"] });

const missing = passages.filter((p) => !(p.hash in BLOCKS));
if (missing.length) {
  for (const p of missing) console.error(`missing variants: ${p.hash} "${p.text.slice(0, 60)}"`);
  process.exit(1);
}
const known = new Set(passages.map((p) => p.hash));
const orphan = Object.keys(BLOCKS).filter((h) => !known.has(h));
if (orphan.length) {
  console.error(`variants with no passage (page edited?): ${orphan.join(", ")}`);
  process.exit(1);
}

const data = {
  version: 1,
  levels: ["Full prose", "Concise", "Terse", "Caveman"],
  blocks: BLOCKS,
  headings: HEADINGS,
  tldr: TLDR,
  eli5: ELI5,
};

const problems = validateCondensed(data, {
  against: { passages, sectionIds: sections.map((s) => s.id) },
  strict: true,
});
if (problems.length) {
  console.error(problems.join("\n"));
  process.exit(1);
}

const out = path.join(repo, "site/condensed.json");
fs.writeFileSync(out, `${JSON.stringify(data, null, 1)}\n`);
console.log(`wrote ${out}: ${passages.length} passages, ${sections.length} sections, strict validation clean`);
