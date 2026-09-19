import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const backendFixturesDir = path.resolve(__dirname, '../../backend/app/ai/fixtures');
const frontendFixturesDir = path.resolve(__dirname, '../src/mocks/fixtures');

console.log('--- Syncing Fixtures ---');
console.log(`Source: ${backendFixturesDir}`);
console.log(`Target: ${frontendFixturesDir}`);

if (!fs.existsSync(backendFixturesDir)) {
  console.log('Backend fixtures directory not found. Using frontend authored fixtures.');
  process.exit(0);
}

if (!fs.existsSync(frontendFixturesDir)) {
  fs.mkdirSync(frontendFixturesDir, { recursive: true });
}

const files = fs.readdirSync(backendFixturesDir);
let syncedCount = 0;

for (const file of files) {
  if (!file.endsWith('.json')) continue;
  const srcPath = path.join(backendFixturesDir, file);
  const destPath = path.join(frontendFixturesDir, file);

  try {
    const content = fs.readFileSync(srcPath, 'utf-8');
    const parsed = JSON.parse(content || '{}');
    // Only overwrite if backend fixture has actual substantive content
    if (parsed && Object.keys(parsed).length > 0) {
      fs.copyFileSync(srcPath, destPath);
      console.log(`Synced: ${file}`);
      syncedCount++;
    } else {
      console.log(`Skipped empty backend fixture: ${file} (retaining frontend fixture)`);
    }
  } catch (err) {
    console.error(`Error processing ${file}:`, err.message);
  }
}

console.log(`Sync complete. ${syncedCount} fixtures synced.`);
