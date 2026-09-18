import { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowRight, Check, ChevronRight, CircleAlert, Loader2, RotateCcw, Send, Sparkles } from 'lucide-react';
import type { AppData } from '../types/invoice';
import { uid } from '../types/invoice';
import type { AssistantDraft, ConversationMessage, DraftOptions, PreparedDraft } from '../types/assistant';
import { assistantError, createAssistantPrompt, prepareDraft, requestAssistant } from '../utils/assistant';
import { orderTotals, platformCalc } from '../utils/calc';

interface Props {
  data: AppData;
  onApply: (draft: PreparedDraft) => void;
  onPreview: (preview: AppData | null) => void;
  onManual: () => void;
}

const money = (amount: number) => new Intl.NumberFormat('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(amount);

export default function AssistantPanel({ data, onApply, onPreview, onManual }: Props) {
  const [messages, setMessages] = useState<ConversationMessage[]>([]);
  const [draft, setDraft] = useState<AssistantDraft | null>(null);
  const [input, setInput] = useState('');
  const [shareContext, setShareContext] = useState(true);
  const [options, setOptions] = useState<DraftOptions>({ useDefaults: true, generateReferences: true });
  const [busy, setBusy] = useState(false);
  const [needsRefresh, setNeedsRefresh] = useState(false);
  const [error, setError] = useState('');
  const [acknowledged, setAcknowledged] = useState(false);
  const [notice, setNotice] = useState('');
  const requestId = useRef(0);
  const requestLock = useRef(false);
  const applyLock = useRef(false);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const conversationRef = useRef<HTMLDivElement>(null);

  const prepared = useMemo(() => draft ? prepareDraft(data, draft, options) : null, [data, draft, options]);
  const ready = !!prepared && prepared.issues.length === 0 && draft?.questions.length === 0 && !busy && !needsRefresh;

  useEffect(() => {
    onPreview(ready ? prepared!.preview : null);
  }, [prepared, ready, onPreview]);

  useEffect(() => {
    setAcknowledged(false);
    applyLock.current = false;
  }, [prepared]);

  useEffect(() => {
    const element = conversationRef.current;
    if (element) element.scrollTop = element.scrollHeight;
  }, [messages, busy]);

  useEffect(() => () => { requestId.current += 1; }, []);

  const run = async (history: ConversationMessage[]) => {
    if (requestLock.current) return;
    const thisRequest = ++requestId.current;
    requestLock.current = true;
    setBusy(true);
    setNeedsRefresh(true);
    setError('');
    setNotice('');
    setAcknowledged(false);
    try {
      const result = await requestAssistant(createAssistantPrompt(history, draft, data, shareContext, options));
      if (requestId.current !== thisRequest) return;
      if (!shareContext && result.orders.some((o) => o.restaurant.existingId || o.address.existingId)) {
        throw new Error('Saved-profile sharing is off, but the assistant tried to reference a saved profile. Supply the details in your message, or enable sharing and retry. Nothing was changed.');
      }
      setDraft(result);
      setNeedsRefresh(false);
      setMessages((previous) => [...previous, { id: uid(), role: 'assistant', text: result.message }]);
    } catch (failure) {
      if (requestId.current === thisRequest) setError(assistantError(failure));
    } finally {
      if (requestId.current === thisRequest) {
        requestLock.current = false;
        setBusy(false);
      }
    }
  };

  const send = () => {
    const value = input.trim();
    if (!value || value.length > 12000 || requestLock.current) return;
    const next = [...messages, { id: uid(), role: 'user' as const, text: value }];
    setMessages(next);
    setInput('');
    void run(next);
  };

  const stop = () => {
    requestId.current += 1;
    requestLock.current = false;
    setBusy(false);
    setNotice('Stopped waiting. Any late response will be ignored. The remote request may still finish; no orders have changed.');
  };

  const reset = () => {
    if ((draft || messages.length > 0) && !window.confirm('Discard this assistant conversation and draft? Saved invoices will not change.')) return;
    requestId.current += 1;
    requestLock.current = false;
    setBusy(false);
    setDraft(null);
    setMessages([]);
    setInput('');
    setError('');
    setNotice('');
    setNeedsRefresh(false);
    inputRef.current?.focus();
  };

  const example = () => {
    const restaurant = data.restaurants[0];
    const address = data.addresses[0];
    setInput(restaurant && address
      ? `Prepare two separate orders on 25/07/2026 and 26/07/2026, both at 19:30. Use saved restaurant "${restaurant.restaurantName}" and saved delivery address "${address.label}" for ${address.customerName}. Each order has 1 Hakka Noodles at INR 186 and 1 Veg Biryani at INR 202 before tax. No discount, CGST 2.5% and SGST 2.5%. Include a platform-fee invoice at INR 14.90 before tax for each order. Use local references for missing numbers.`
      : 'Prepare a dinner order for 25/07/2026 at 19:30: 2 Veg Biryani at INR 202 each before tax, no discount, CGST 2.5% and SGST 2.5%. No platform-fee invoice. Ask me for the restaurant and delivery details.');
    setShareContext(true);
    setOptions((previous) => ({ ...previous, generateReferences: true }));
    inputRef.current?.focus();
  };

  const apply = () => {
    if (!ready || !prepared || !acknowledged || applyLock.current) return;
    applyLock.current = true;
    onApply(prepared);
    setDraft(null);
    setMessages([]);
    setInput('');
    setAcknowledged(false);
  };

  return (
    <section className="assistant-panel" aria-label="AI invoice assistant">
      <div className="assistant-heading">
        <div>
          <div className="assistant-eyebrow"><Sparkles size={13} /> AI-ASSISTED CREATION</div>
          <h2>Tell us about your order.</h2>
          <p>One meal or a whole batch. Describe the details, review the draft, then add your invoices.</p>
        </div>
        {(messages.length > 0 || draft) && <button type="button" onClick={reset} className="icon-button" title="Start a new conversation" aria-label="Start a new conversation"><RotateCcw size={17} /></button>}
      </div>

      <div className="canvas-notice">
        <span className="status-dot" />
        <p><strong>Canvas integration</strong> uses your supplied functions with blank keys. AI needs internet and a compatible Canvas runtime; manual editing works offline.</p>
      </div>

      {!messages.length && (
        <button type="button" className="example-prompt" onClick={example}>
          <span><strong>Same dinner, two different days?</strong><span>Try a multi-order example using your saved details.</span></span>
          <ChevronRight size={18} />
        </button>
      )}

      {messages.length > 0 && (
        <div className="conversation" ref={conversationRef} role="log" aria-label="Invoice conversation" aria-live="polite" aria-relevant="additions text">
          {messages.map((message) => (
            <div key={message.id} className={`agent-message ${message.role}`}>
              <span className="message-author">{message.role === 'user' ? 'You' : 'Invoice assistant'}</span>
              <p>{message.text}</p>
            </div>
          ))}
          {busy && <div className="assistant-working"><Loader2 size={16} className="is-spinning" /><span>Collecting details and checking the draft...</span><button type="button" onClick={stop}>Stop waiting</button></div>}
        </div>
      )}

      {error && <div className="assistant-error" role="alert"><CircleAlert size={18} /><div><p>{error}</p><div className="inline-actions"><button type="button" disabled={busy} onClick={() => void run(messages)}>Retry request</button><button type="button" onClick={onManual}>Continue manually <ArrowRight size={13} /></button></div></div></div>}
      {notice && <p className="agent-notice" role="status">{notice}</p>}

      {draft && !busy && !needsRefresh && (draft.questions.length > 0 || (prepared && prepared.issues.length > 0)) && (
        <div className="clarification-section">
          <h3>A few details to finish</h3>
          {draft.questions.length > 0 && <ol>{draft.questions.map((question, index) => <li key={index}>{question}</li>)}</ol>}
          {prepared && prepared.issues.length > 0 && <details open={!draft.questions.length}><summary>{prepared.issues.length} field {prepared.issues.length === 1 ? 'check' : 'checks'} still need attention</summary><ul>{prepared.issues.map((issue) => <li key={issue}>{issue}</li>)}</ul></details>}
          <p>Reply below. Your answers will update the same draft.</p>
        </div>
      )}

      <form className="assistant-composer" onSubmit={(event) => { event.preventDefault(); send(); }}>
        <label htmlFor="assistant-message">{messages.length ? 'Your reply or changes' : 'Describe your invoice details'}</label>
        <div className="composer-input">
          <textarea
            id="assistant-message" ref={inputRef} value={input} onChange={(event) => setInput(event.target.value)}
            placeholder="For example: Two orders from Sagar Gaire, July 25 and 26 at 7:30 pm. Same Home address. One Hakka Noodles at 186 and one Veg Biryani at 202 each day..."
            rows={5} maxLength={12000} disabled={busy}
            onKeyDown={(event) => { if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) { event.preventDefault(); send(); } }}
          />
          <div className="composer-bottom"><span>Amounts in INR <span aria-hidden="true">/</span> Ctrl + Enter to send</span><button type="submit" className="primary-button" disabled={busy || !input.trim()}>{busy ? <Loader2 size={15} className="is-spinning" /> : <Send size={15} />}{messages.length ? 'Send details' : 'Prepare draft'}</button></div>
        </div>
      </form>

      <div className="assistant-options">
        <label><input type="checkbox" checked={shareContext} disabled={busy} onChange={(event) => setShareContext(event.target.checked)} /><span>Let the assistant use saved restaurants, addresses, and recent orders.</span></label>
        <details>
          <summary>Draft defaults &amp; reference numbers</summary>
          <label><input type="checkbox" checked={options.useDefaults} disabled={busy} onChange={(event) => setOptions((previous) => ({ ...previous, useDefaults: event.target.checked }))} /><span>For omitted fields: quantity 1, discount 0, CGST/SGST 2.5% each, plus a platform page with INR 14.90 fee and 9% CGST/SGST each.</span></label>
          <label><input type="checkbox" checked={options.generateReferences} disabled={busy} onChange={(event) => setOptions((previous) => ({ ...previous, generateReferences: event.target.checked }))} /><span>Assign local invoice/order reference numbers if I do not provide them. These are not verified source-issued numbers.</span></label>
        </details>
        <p className="privacy-note">Sending shares your message, this conversation, and enabled saved context with Gemini. No API key is requested or stored. The assistant never prints or changes saved invoices on its own.</p>
      </div>

      {prepared && draft && draft.orders.length > 0 && (
        <section className="draft-review" aria-labelledby="draft-review-title">
          <div className="review-heading"><div><span className="assistant-eyebrow">REVIEW BEFORE ADDING</span><h3 id="draft-review-title">{draft.orders.length} {draft.orders.length === 1 ? 'order' : 'orders'} in this draft</h3></div><span className={`draft-state ${ready ? 'ready' : ''}`}>{ready ? <><Check size={13} /> Ready for review</> : 'Needs details'}</span></div>
          {needsRefresh && <p className="draft-warning">Your last requested changes have not been applied. Retry the request before adding this draft.</p>}
          {prepared.preview.orders.map((order, index) => {
            const restaurant = prepared.preview.restaurants.find((r) => r.id === order.restaurantId);
            const address = prepared.preview.addresses.find((a) => a.id === order.addressId);
            const totals = orderTotals(order);
            const platform = order.includePlatformInvoice ? platformCalc(order.platformFee).total : 0;
            return (
              <article className="draft-order" key={order.id}>
                <div className="draft-order-heading"><strong>Order {index + 1}</strong><span>{order.invoiceDate || 'Date needed'}{order.invoiceTime ? ` at ${order.invoiceTime}` : ''}</span></div>
                <p className="draft-restaurant">{restaurant?.restaurantName || 'Restaurant needed'}</p>
                <p className="draft-address">{address?.customerName || 'Customer needed'}<br />{address?.deliveryAddress || 'Delivery address needed'}</p>
                <div className="draft-items">{order.items.map((item, i) => <div key={item.id}><span>{item.particulars || 'Food description needed'}</span><span>INR {money(totals.rows[i].total)}</span></div>)}</div>
                <div className="draft-total"><span>Food total, including tax</span><strong>INR {money(totals.total)}</strong></div>
                {order.includePlatformInvoice && <div className="draft-platform"><span>Separate platform-fee invoice</span><span>INR {money(platform)}</span></div>}
                <details className="draft-detail-list"><summary>Check invoice, tax &amp; profile details</summary><dl>
                  <dt>Invoice number</dt><dd>{order.invoiceNo || 'Not supplied'}</dd><dt>Order ID</dt><dd>{order.orderId || 'Not supplied'}</dd>
                  <dt>Legal entity</dt><dd>{restaurant?.legalEntityName || 'Not supplied'}</dd><dt>Restaurant address</dt><dd>{restaurant?.restaurantAddress || 'Not supplied'}</dd>
                  <dt>Restaurant GSTIN / FSSAI</dt><dd>{restaurant?.restaurantGstin || 'Blank'} / {restaurant?.restaurantFssai || 'Blank'}</dd>
                  <dt>Place of supply</dt><dd>{address?.stateName || 'Not supplied'}</dd>
                  <dt>Taxable value / discount</dt><dd>INR {money(totals.net)} / INR {money(totals.discount)}</dd>
                  <dt>CGST / SGST</dt><dd>INR {money(totals.cgst)} / INR {money(totals.sgst)}</dd>
                  {order.includePlatformInvoice && <><dt>Platform invoice number</dt><dd>{order.platformInvoiceNo || 'Not supplied'}</dd><dt>Platform fee before tax</dt><dd>INR {order.platformFee || 'Not supplied'}</dd></>}
                </dl></details>
              </article>
            );
          })}
          {prepared.notes.length > 0 && <details className="review-notes" open><summary>Defaults and details to verify</summary><ul>{prepared.notes.map((note) => <li key={note}>{note}</li>)}</ul></details>}
          <p className="review-append-note">Adds {prepared.preview.orders.length} new {prepared.preview.orders.length === 1 ? 'order' : 'orders'}{prepared.newRestaurants.length > 0 ? `, ${prepared.newRestaurants.length} new restaurant profile(s)` : ''}{prepared.newAddresses.length > 0 ? `, ${prepared.newAddresses.length} new address profile(s)` : ''}. Your {data.orders.length} saved orders stay unchanged.</p>
          <label className="review-confirm"><input type="checkbox" checked={acknowledged} disabled={!ready} onChange={(event) => setAcknowledged(event.target.checked)} /><span>I have checked the transaction details, taxes, and reference numbers.</span></label>
          <button type="button" className="primary-button apply-draft-button" disabled={!ready || !acknowledged} onClick={apply}>Add {draft.orders.length === 1 ? 'order' : `${draft.orders.length} orders`} &amp; open manual editor <ArrowRight size={16} /></button>
          <p className="review-footnote">Everything remains editable before you print.</p>
        </section>
      )}
    </section>
  );
}