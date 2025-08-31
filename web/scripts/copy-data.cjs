#!/usr/bin/env node
// Copies top-level /data JSON into /web/public/data for local dev and builds.
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..', '..');
const srcDir = path.join(root, 'data');
const destDir = path.join(__dirname, '..', 'public', 'data');

fs.mkdirSync(destDir, { recursive: true });
for (const name of ['recipes.json', 'recipe_views.json']) {
  const src = path.join(srcDir, name);
  const dest = path.join(destDir, name);
  if (!fs.existsSync(src)) {
    console.warn(`[copy-data] Missing ${src}`);
    continue;
  }
  fs.copyFileSync(src, dest);
  console.log(`[copy-data] Copied ${name}`);
}
