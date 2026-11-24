// news-image-20261124 — the program the grader runs (Node 22,
// standard library only).
//
// The front page is already finished and lives in this repository as
// entry.png: draw.py paints it from the bundled hero illustration plus
// the day's verified stories, so every headline is spelled right and
// stays readable when the judge looks at the image small. All this
// program does is carry those finished bytes into the grader's output
// directory, after checking the file really is a 1024x1024 PNG under
// 1 MiB. No network, no randomness, no writes anywhere but the output
// directory, so two runs produce byte-identical output. Every check
// happens before anything is written, so a bad image fails loudly
// instead of shipping a bad entry.
//
// Try it locally:
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { chmodSync, copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;
const MAX_BYTES = 1024 * 1024;

function fail(message) {
  throw new Error(`entry.png failed its checks: ${message}`);
}

const repoDir = dirname(fileURLToPath(import.meta.url));
const imagePath = join(repoDir, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const outputPath = join(outputDir, "entry.png");

if (!existsSync(imagePath)) {
  fail(`not found next to main.ts (${imagePath})`);
}
const image = readFileSync(imagePath);
if (!image.subarray(0, 8).equals(PNG_SIGNATURE)) {
  fail("first bytes are not a PNG signature");
}
// A PNG header stores width at bytes 16-19 and height at 20-23,
// both big-endian.
const width = image.readUInt32BE(16);
const height = image.readUInt32BE(20);
if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
  fail(`dimensions are ${width}x${height}, expected 1024x1024`);
}
const size = statSync(imagePath).size;
if (size > MAX_BYTES) {
  fail(`file is ${size} bytes, over the 1 MiB limit`);
}
mkdirSync(outputDir, { recursive: true });
copyFileSync(imagePath, outputPath);
chmodSync(outputPath, 0o644);
