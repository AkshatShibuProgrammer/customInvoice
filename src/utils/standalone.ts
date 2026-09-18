import type { AppData } from '../types/invoice';
import { uid } from '../types/invoice';
import { SNAPSHOT_ID } from './workspace';

// Vite's dev server exposes ?raw as a JSON string literal in an ES module.
// Decode the literal as data, never by evaluating downloaded JavaScript.
function decodeRawModule(source: string): string {
  const text = source.trim();
  if (text.startsWith('<!') || text.startsWith('<html')) return text;
  const prefix = /^export default\s+/.exec(text);
  if (!prefix || text[prefix[0].length] !== '"') throw new Error('The single-file production build is not available yet.');
  const start = prefix[0].length;
  let escaped = false;
  for (let i = start + 1; i < text.length; i++) {
    if (!escaped && text[i] === '"') return JSON.parse(text.slice(start, i + 1)) as string;
    if (!escaped && text[i] === '\\') escaped = true;
    else escaped = false;
  }
  throw new Error('The production build could not be read.');
}

export async function createStandaloneHtml(data: AppData): Promise<string> {
  let source: Document = document;
  if (import.meta.env.DEV) {
    // Export the compiled application, never the Vite/HMR development entry point.
    const url = new URL(`${import.meta.env.BASE_URL}dist/index.html?raw&import`, window.location.origin);
    const response = await fetch(url, { cache: 'no-store' });
    if (!response.ok) throw new Error('The compiled HTML is not available in this preview. Use dist/index.html after the production build.');
    source = new DOMParser().parseFromString(decodeRawModule(await response.text()), 'text/html');
  }
  const appScript = Array.from(source.querySelectorAll<HTMLScriptElement>('script[type="module"]'))
    .filter((script) => !script.src && script.textContent && script.textContent.length > 10000)
    .sort((a, b) => (b.textContent?.length ?? 0) - (a.textContent?.length ?? 0))[0];
  const integration = source.getElementById('gemini-canvas-integration');
  const styles = Array.from(source.querySelectorAll('style'));
  if (!appScript || !integration || !styles.length) throw new Error('This is not a self-contained production build. Download dist/index.html after building the application.');

  const output = document.implementation.createHTMLDocument('Eternal Invoice Generator');
  output.documentElement.lang = 'en';
  const charset = output.createElement('meta');
  charset.setAttribute('charset', 'UTF-8');
  const viewport = output.createElement('meta');
  viewport.name = 'viewport';
  viewport.content = 'width=device-width, initial-scale=1.0';
  output.head.prepend(charset, viewport);
  styles.forEach((style) => output.head.appendChild(style.cloneNode(true)));
  output.head.appendChild(integration.cloneNode(true));

  const snapshot = output.createElement('script');
  snapshot.id = SNAPSHOT_ID;
  snapshot.type = 'application/json';
  snapshot.textContent = JSON.stringify({ version: 1, workspaceId: `export-${uid()}-${Date.now()}`, data })
    .replace(/</g, '\\u003c').replace(/>/g, '\\u003e').replace(/&/g, '\\u0026').replace(/\u2028/g, '\\u2028').replace(/\u2029/g, '\\u2029');
  output.head.appendChild(snapshot);
  const root = output.createElement('div');
  root.id = 'root';
  output.body.appendChild(root);
  output.body.appendChild(appScript.cloneNode(true));
  return `<!doctype html>\n${output.documentElement.outerHTML}`;
}

export async function downloadStandalone(data: AppData): Promise<void> {
  const html = await createStandaloneHtml(data);
  const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'eternal-invoice-generator.html';
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 30000);
}