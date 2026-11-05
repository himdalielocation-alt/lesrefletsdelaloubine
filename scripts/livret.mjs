#!/usr/bin/env node
// Chiffre / déchiffre le livret d'accueil (livret.html, à la racine du site).
//
// Le contenu du livret n'est jamais stocké en clair dans le dépôt (public) : livret.html
// contient seulement le contenu chiffré (AES-GCM 256) et la page qui le déchiffre dans le
// navigateur. La clé se trouve uniquement après le # de l'URL remise aux voyageurs
// (https://lesrefletsdelaloubine.fr/livret.html#k=<clé>), que le navigateur n'envoie
// jamais au serveur. Sans cette URL complète, impossible de lire ni de modifier le livret.
//
// Usage (clé passée par variable d'environnement, jamais en argument ni dans un fichier du dépôt) :
//   LIVRET_KEY='<URL ou clé>' node scripts/livret.mjs decrypt > contenu.html   # contenu actuel
//   LIVRET_KEY='<URL ou clé>' node scripts/livret.mjs encrypt contenu.html     # republier
//   node scripts/livret.mjs newkey                                             # nouvelle clé = nouvelle URL / nouveau QR code
// Aucune dépendance (Node.js 18+, Web Crypto intégrée).
import { readFileSync, writeFileSync } from 'node:fs';
import { webcrypto as crypto } from 'node:crypto';

const ROOT = new URL('..', import.meta.url);
const SHELL = new URL('scripts/livret_shell.html', ROOT);
const OUTPUT = new URL('livret.html', ROOT);
const BASE_URL = 'https://lesrefletsdelaloubine.fr/livret.html';

const b64url = (buf) => Buffer.from(buf).toString('base64url');
function keyFromEnv() {
  const raw = (process.env.LIVRET_KEY || '').trim();
  const m = raw.match(/k=([A-Za-z0-9_-]{43})/) || raw.match(/^([A-Za-z0-9_-]{43})$/);
  if (!m) { console.error('LIVRET_KEY manquante ou invalide : donnez la clé (43 caractères) ou l\'URL complète du livret.'); process.exit(1); }
  return crypto.subtle.importKey('raw', Buffer.from(m[1], 'base64url'), 'AES-GCM', false, ['encrypt', 'decrypt']);
}

const [cmd, file] = process.argv.slice(2);
if (cmd === 'newkey') {
  console.log(`${BASE_URL}#k=${b64url(crypto.getRandomValues(new Uint8Array(32)))}`);
} else if (cmd === 'encrypt' && file) {
  const key = await keyFromEnv();
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ct = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, readFileSync(file));
  const payload = JSON.stringify({ iv: Buffer.from(iv).toString('base64'), ct: Buffer.from(ct).toString('base64') });
  const page = readFileSync(SHELL, 'utf8').replace('{{PAYLOAD}}', payload);
  writeFileSync(OUTPUT, page);
  console.log(`Écrit : livret.html (${Math.round(page.length / 1024)} Ko)`);
} else if (cmd === 'decrypt') {
  const key = await keyFromEnv();
  const page = readFileSync(OUTPUT, 'utf8');
  const payload = JSON.parse(page.match(/const LIVRET_PAYLOAD = (\{.*?\});/s)[1]);
  const plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: Buffer.from(payload.iv, 'base64') }, key, Buffer.from(payload.ct, 'base64'));
  process.stdout.write(Buffer.from(plain));
} else {
  console.error('Usage : node scripts/livret.mjs newkey | encrypt <contenu.html> | decrypt  (clé dans LIVRET_KEY)');
  process.exit(1);
}
