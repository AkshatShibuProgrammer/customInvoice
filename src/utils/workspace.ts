import { defaultAppData } from '../types/invoice';
import type { AppData } from '../types/invoice';
import { isRecord, parseWorkspace } from './validation';

const LEGACY_KEY = 'eternal-invoice-data-v2';
export const SNAPSHOT_ID = 'invoice-workspace-data';

export function loadWorkspace(): { data: AppData; storageKey: string; warning: string } {
  let initial = defaultAppData;
  let storageKey = LEGACY_KEY;
  let warning = '';
  try {
    const embedded = document.getElementById(SNAPSHOT_ID)?.textContent;
    if (embedded) {
      const snapshot: unknown = JSON.parse(embedded);
      if (isRecord(snapshot) && snapshot.version === 1 && typeof snapshot.workspaceId === 'string' && /^[\w-]{1,100}$/.test(snapshot.workspaceId)) {
        const restored = parseWorkspace(snapshot.data);
        if (restored) {
          initial = restored;
          storageKey = `${LEGACY_KEY}:${snapshot.workspaceId}`;
        } else warning = 'The embedded workspace could not be restored. The sample workspace is shown instead.';
      }
    }
    const raw = localStorage.getItem(storageKey);
    if (raw) {
      const saved = parseWorkspace(JSON.parse(raw));
      if (saved) return { data: saved, storageKey, warning };
      warning = 'Saved browser data was not readable. The embedded workspace or sample data has been loaded.';
    }
  } catch {
    warning = 'Browser storage is unavailable or unreadable. Editing still works; download the HTML with your data to keep a copy.';
  }
  return { data: initial, storageKey, warning };
}

export function saveWorkspace(storageKey: string, data: AppData): boolean {
  try {
    localStorage.setItem(storageKey, JSON.stringify(data));
    return true;
  } catch {
    return false;
  }
}