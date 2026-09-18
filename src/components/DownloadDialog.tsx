import { useEffect, useRef, useState } from 'react';
import { Check, Download, FileCode2, Loader2, X } from 'lucide-react';
import type { AppData } from '../types/invoice';
import { downloadStandalone } from '../utils/standalone';

export default function DownloadDialog({ data, onClose }: { data: AppData; onClose: () => void }) {
  const dialog = useRef<HTMLDialogElement>(null);
  const [includeData, setIncludeData] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  useEffect(() => {
    const element = dialog.current;
    if (element && !element.open) element.showModal();
    return () => { if (element?.open) element.close(); };
  }, []);

  const download = async () => {
    setBusy(true);
    setError('');
    setSuccess(false);
    try {
      await downloadStandalone(includeData ? data : { ...data, orders: [], restaurants: [], addresses: [] });
      setSuccess(true);
    } catch (failure) {
      setError(failure instanceof Error ? failure.message : 'The HTML file could not be prepared. Please retry.');
    } finally {
      setBusy(false);
    }
  };

  return (
    <dialog ref={dialog} className="download-dialog" onCancel={(event) => { event.preventDefault(); onClose(); }} aria-labelledby="download-title">
      <div className="dialog-top"><FileCode2 size={26} /><button type="button" className="icon-button" aria-label="Close download dialog" onClick={onClose}><X size={19} /></button></div>
      <h2 id="download-title">Your workspace. One HTML file.</h2>
      <p>Download the complete application, not just a picture of the invoice. Open it directly in a modern browser. No installation or separate assets.</p>
      <label className="download-data-option"><input type="checkbox" checked={includeData} onChange={(event) => setIncludeData(event.target.checked)} disabled={busy} /><span><strong>Include my current orders and profiles</strong><span>{data.orders.length} orders, {data.restaurants.length} restaurants, and {data.addresses.length} delivery addresses. Shared company settings are always included.</span></span></label>
      <div className="download-explanation"><p><strong>Works offline:</strong> manual editing, calculations, saved profiles, images, and printing.</p><p><strong>AI mode:</strong> needs internet and a Canvas runtime that supports your supplied blank-key functions. A downloaded file does not provide authentication by itself.</p></div>
      <p className="privacy-note">{includeData ? 'The file will contain your invoice and customer data. Share it only with people who should have access. ' : 'The file opens with an empty order and profile list. '}Assistant conversations are not included.</p>
      {error && <p className="download-error" role="alert">{error}</p>}
      {success && <p className="download-success" role="status"><Check size={16} /> Download started: eternal-invoice-generator.html</p>}
      <button type="button" className="primary-button" onClick={() => void download()} disabled={busy}>{busy ? <Loader2 size={17} className="is-spinning" /> : <Download size={17} />}{busy ? 'Preparing HTML...' : 'Download HTML'}</button>
    </dialog>
  );
}