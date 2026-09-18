import { useCallback, useEffect, useState } from 'react';
import { Check, Download, PenLine, Sparkles, X } from 'lucide-react';
import { defaultAppData } from './types/invoice';
import type { AppData } from './types/invoice';
import type { PreparedDraft } from './types/assistant';
import InvoiceForm from './components/InvoiceForm';
import InvoicePreview from './components/InvoicePreview';
import AssistantPanel from './components/AssistantPanel';
import DownloadDialog from './components/DownloadDialog';
import { loadWorkspace, saveWorkspace } from './utils/workspace';

export default function App() {
  const [workspace] = useState(loadWorkspace);
  const [data, setData] = useState<AppData>(workspace.data);
  const [selectedOrderId, setSelectedOrderId] = useState<string | null>(null);
  const [mode, setMode] = useState<'assistant' | 'manual'>('assistant');
  const [draftPreview, setDraftPreview] = useState<AppData | null>(null);
  const [downloadOpen, setDownloadOpen] = useState(false);
  const [saved, setSaved] = useState(true);
  const [warning, setWarning] = useState(workspace.warning);
  const [toast, setToast] = useState('');
  const [resetToken, setResetToken] = useState(0);
  const [focusOrdersToken, setFocusOrdersToken] = useState(0);

  useEffect(() => { setSaved(saveWorkspace(workspace.storageKey, data)); }, [data, workspace.storageKey]);
  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => setToast(''), 7000);
    return () => clearTimeout(timer);
  }, [toast]);

  const applyDraft = useCallback((prepared: PreparedDraft) => {
    const orders = prepared.preview.orders;
    setData((previous) => ({
      ...previous,
      restaurants: [...previous.restaurants, ...prepared.newRestaurants],
      addresses: [...previous.addresses, ...prepared.newAddresses],
      orders: [...previous.orders, ...orders],
    }));
    setSelectedOrderId(orders.length === 1 ? orders[0].id : null);
    setDraftPreview(null);
    setFocusOrdersToken((value) => value + 1);
    setMode('manual');
    setToast(`${orders.length} ${orders.length === 1 ? 'order added' : 'orders added'}. Review or edit below, then print when ready.`);
  }, []);

  const reset = () => {
    if (window.confirm('Replace all saved orders, profiles, and the current assistant draft with the sample defaults?')) {
      setData(defaultAppData);
      setSelectedOrderId(null);
      setDraftPreview(null);
      setResetToken((value) => value + 1);
      setFocusOrdersToken((value) => value + 1);
      setToast('Sample workspace restored.');
    }
  };

  const showingDraft = mode === 'assistant' && draftPreview !== null;

  return (
    <div className="invoice-workspace">
      <header className="workspace-header">
        <div className="workspace-identity"><span className="workspace-wordmark">eternal</span><div className="workspace-title"><h1>Invoice Generator</h1><p>Your orders. Your details. One workspace.</p></div></div>
        <div className="workspace-header-actions"><span className={`save-status ${saved ? '' : 'unsaved'}`}><span className="status-dot" />{saved ? 'Saved on this device' : 'Session only'}</span><button type="button" className="secondary-button" onClick={() => setDownloadOpen(true)}><Download size={16} /> Download HTML</button></div>
      </header>

      {(warning || !saved) && <div className="workspace-warning" role="status"><p>{warning || 'Browser storage is unavailable. Your edits work for this session; download the HTML with your current data to keep a copy.'}</p>{warning && <button type="button" aria-label="Dismiss storage notice" onClick={() => setWarning('')}><X size={16} /></button>}</div>}

      <main className="workspace-grid">
        <section className="editor-panel" aria-label="Invoice details workspace">
          <div className="editor-mode-bar" role="tablist" aria-label="Choose how to enter details" onKeyDown={(event) => {
            if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
            event.preventDefault();
            const next = event.key === 'Home' ? 'assistant' : event.key === 'End' ? 'manual' : mode === 'assistant' ? 'manual' : 'assistant';
            setMode(next);
            document.getElementById(`mode-${next}`)?.focus();
          }}>
            <button id="mode-assistant" type="button" role="tab" tabIndex={mode === 'assistant' ? 0 : -1} aria-selected={mode === 'assistant'} aria-controls="assistant-panel" className={mode === 'assistant' ? 'active' : ''} onClick={() => setMode('assistant')}><Sparkles size={16} /> AI assistant</button>
            <button id="mode-manual" type="button" role="tab" tabIndex={mode === 'manual' ? 0 : -1} aria-selected={mode === 'manual'} aria-controls="manual-panel" className={mode === 'manual' ? 'active' : ''} onClick={() => setMode('manual')}><PenLine size={16} /> Manual editor</button>
          </div>
          <div className="editor-scroll-area">
            <div id="assistant-panel" role="tabpanel" aria-labelledby="mode-assistant" hidden={mode !== 'assistant'}><AssistantPanel key={resetToken} data={data} onApply={applyDraft} onPreview={setDraftPreview} onManual={() => setMode('manual')} /></div>
            <div id="manual-panel" role="tabpanel" aria-labelledby="mode-manual" hidden={mode !== 'manual'} className="manual-editor"><div className="manual-intro"><h2>Make it yours.</h2><p>Edit every detail, reuse a profile, or add another order.</p></div><InvoiceForm data={data} onChange={setData} selectedOrderId={selectedOrderId} onSelectOrder={setSelectedOrderId} focusOrdersToken={focusOrdersToken} /></div>
          </div>
          <div className="editor-footer"><span>{mode === 'manual' ? 'Manual mode works without internet.' : 'Drafts are never saved without your approval.'}</span><button type="button" onClick={reset}>Reset to sample</button></div>
        </section>

        <section className="preview-panel" aria-label="Invoice preview">
          <div className="preview-panel-heading"><div><span className="assistant-eyebrow">{showingDraft ? 'NOT SAVED YET' : 'YOUR DOCUMENTS'}</span><h2>{showingDraft ? 'Draft preview' : 'Live preview'}</h2></div><span>A4 <span aria-hidden="true">/</span> Print-ready layout</span></div>
          <div className="preview-scroll-area"><InvoicePreview data={showingDraft ? draftPreview! : data} selectedOrderId={showingDraft ? null : selectedOrderId} isDraft={showingDraft} onShowAll={() => setSelectedOrderId(null)} /></div>
        </section>
      </main>

      {toast && <div className="workspace-toast" role="status"><Check size={17} /><p>{toast}</p><button type="button" className="icon-button" aria-label="Dismiss notification" onClick={() => setToast('')}><X size={15} /></button></div>}
      {downloadOpen && <DownloadDialog data={data} onClose={() => setDownloadOpen(false)} />}
    </div>
  );
}
