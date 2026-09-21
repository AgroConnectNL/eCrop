#!/usr/bin/env node
// Checks that every examples/<business-case>/README.md (all case folders
// except _template) contains the required section headings, per the
// skeleton in examples/_template/README.md.

const fs = require('fs');
const path = require('path');

const EXAMPLES_DIR = path.join(__dirname, '..', 'examples');

const REQUIRED_HEADINGS = [
  'Use case and starting points',
  'Operations used',
  'Example flow',
  'Still to be arranged',
];

function headingsOf(markdown) {
  return markdown
    .split('\n')
    .filter((line) => /^##\s+/.test(line))
    .map((line) =>
      line
        .replace(/^##\s+/, '')
        .replace(/^\d+(\.\d+)*\.?\s*/, '') // strip "1. " / "2.3 " numbering
        .trim()
        .toLowerCase()
    );
}

function main() {
  const entries = fs.readdirSync(EXAMPLES_DIR, { withFileTypes: true });
  const caseDirs = entries
    .filter((e) => e.isDirectory() && e.name !== '_template')
    .map((e) => e.name)
    .sort();

  let failed = false;

  for (const dir of caseDirs) {
    const readmePath = path.join(EXAMPLES_DIR, dir, 'README.md');
    if (!fs.existsSync(readmePath)) {
      console.error(`examples/${dir}: missing README.md`);
      failed = true;
      continue;
    }
    const headings = headingsOf(fs.readFileSync(readmePath, 'utf8'));
    const missing = REQUIRED_HEADINGS.filter(
      (required) => !headings.includes(required.toLowerCase())
    );
    if (missing.length > 0) {
      console.error(`examples/${dir}/README.md: missing required section(s): ${missing.join(', ')}`);
      failed = true;
    }
  }

  if (failed) {
    console.error('\nSee examples/_template/README.md for the expected structure.');
    process.exit(1);
  }

  console.log(`OK: checked ${caseDirs.length} business case(s) in examples/.`);
}

main();
