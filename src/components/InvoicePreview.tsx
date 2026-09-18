import type { AppData } from '../types/invoice';
import InvoiceType1 from './InvoiceType1';
import InvoiceType2 from './InvoiceType2';
import { useRef, useState, useEffect } from 'react';
import { Loader2, Printer } from 'lucide-react';
import { validateOrders } from '../utils/validation';

interface Props {
  data: AppData;
  selectedOrderId: string | null;
  isDraft?: boolean;
  onShowAll?: () => void;
}

const A4_WIDTH_PX = 210 * 96 / 25.4;

const PRINT_STYLES = `
  @page { size: A4 portrait; margin: 0; }
  html, body { margin: 0 !important; padding: 0 !important; background: #fff !important; }
  *, *::before, *::after { box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
  .invoice-page { width: 210mm; min-height: 297mm; height: auto; margin: 0; padding: 12mm 12mm 8mm; box-shadow: none; transform: none; overflow: visible; break-after: page; page-break-after: always; }
  .invoice-page:last-child { break-after: auto; page-break-after: auto; }
  .invoice-bottom, .invoice-page tr { break-inside: avoid; page-break-inside: avoid; }
  .invoice-page thead { display: table-header-group; }
`;

export async function printHtml(html: string): Promise<void> {
  const w = window.open('', '_blank', 'width=900,height=1200');
  if (!w) throw new Error('The print window was blocked. Allow pop-ups for this page and try again.');
  const doc = w.document;
  doc.open();
  doc.write('<!doctype html><html><head><meta charset="utf-8"><title>Tax Invoice</title></head><body></body></html>');
  doc.close();
  // Use the actual preview CSS, rather than a second approximation of Tailwind rules.
  const style = doc.createElement('style');
  style.textContent = Array.from(document.styleSheets).map((sheet) => {
    try { return Array.from(sheet.cssRules).map((rule) => rule.cssText).join('\n'); }
    catch { return ''; }
  }).join('\n') + PRINT_STYLES;
  doc.head.appendChild(style);
  doc.body.innerHTML = html;
  let timeout: ReturnType<typeof setTimeout> | undefined;
  try {
    const images = Array.from(doc.images).map((image) => new Promise<void>((resolve, reject) => {
      const done = () => image.naturalWidth > 0 ? resolve() : reject(new Error('An invoice image could not load. Please retry before printing.'));
      if (image.complete) done();
      else { image.addEventListener('load', done, { once: true }); image.addEventListener('error', done, { once: true }); }
    }));
    await Promise.race([
      Promise.all([...images, doc.fonts.ready]),
      new Promise<never>((_, reject) => { timeout = setTimeout(() => reject(new Error('The invoice images did not load in time. Please retry.')), 10000); }),
    ]);
    if (w.closed) return;
    w.focus();
    w.print();
  } catch (error) {
    w.close();
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}

export default function InvoicePreview({ data, selectedOrderId, isDraft = false, onShowAll }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const allRef = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(1);
  const [height, setHeight] = useState(1123);
  const [error, setError] = useState('');
  const [printing, setPrinting] = useState(false);

  useEffect(() => {
    const measure = () => {
      if (containerRef.current) setScale(Math.min(1, containerRef.current.clientWidth / A4_WIDTH_PX));
      if (allRef.current) setHeight(allRef.current.offsetHeight);
    };
    measure();
    const ro = new ResizeObserver(measure);
    if (containerRef.current) ro.observe(containerRef.current);
    if (allRef.current) ro.observe(allRef.current);
    return () => ro.disconnect();
  }, []);
  useEffect(() => { setError(''); }, [data, selectedOrderId]);

  const orders = selectedOrderId ? data.orders.filter((o) => o.id === selectedOrderId) : data.orders;

  const pages = orders.flatMap((order) => {
    const restaurant = data.restaurants.find((r) => r.id === order.restaurantId);
    const address = data.addresses.find((a) => a.id === order.addressId);
    if (!restaurant || !address) return [];
    const out = [
      <div key={order.id + '-r'} data-order={order.id}>
        <InvoiceType1 order={order} restaurant={restaurant} address={address} common={data.common} />
      </div>,
    ];
    if (order.includePlatformInvoice) {
      out.push(
        <div key={order.id + '-p'} data-order={order.id}>
          <InvoiceType2 order={order} address={address} common={data.common} />
        </div>,
      );
    }
    return out;
  });

  const printAll = async () => {
    if (!allRef.current || isDraft || printing || !pages.length) return;
    const issues = validateOrders(data, orders);
    if (issues.length) { setError(issues.join('\n')); return; }
    setPrinting(true);
    setError('');
    try {
      // Only invoice roots enter the print document, so each page break is effective.
      const html = Array.from(allRef.current.querySelectorAll<HTMLElement>('.invoice-page')).map((page) => page.outerHTML).join('\n');
      await printHtml(html);
    } catch (failure) {
      setError(failure instanceof Error ? failure.message : 'The invoice could not be printed.');
    } finally {
      setPrinting(false);
    }
  };

  return (
    <div className="flex flex-col items-center w-full">
      <div className="preview-toolbar">
        <button
          type="button" onClick={() => void printAll()} disabled={isDraft || printing || !pages.length}
          className="primary-button"
        >
          {printing ? <Loader2 size={16} className="is-spinning" /> : <Printer size={16} />}
          {isDraft ? 'Approve draft to print' : printing ? 'Preparing print...' : selectedOrderId ? 'Print this order' : 'Print all invoices'}
        </button>
        <span>{orders.length} {orders.length === 1 ? 'order' : 'orders'} / {pages.length} {pages.length === 1 ? 'invoice' : 'invoices'}</span>
        {selectedOrderId && onShowAll && <button type="button" className="text-button" onClick={onShowAll}>Show all</button>}
      </div>
      {error && <p className="print-error" role="alert">{error}</p>}
      {!isDraft && pages.length > 0 && <p className="print-hint">Print settings: A4, 100% scale, no margins or browser headers. Long invoices may continue onto extra pages.</p>}

      <div ref={containerRef} className="w-full flex justify-center">
        <div style={{ width: A4_WIDTH_PX * scale, height: height * scale }}>
          <div ref={allRef} style={{ width: A4_WIDTH_PX, transform: `scale(${scale})`, transformOrigin: 'top left' }} className="preview-page-stack">
            {pages.length === 0 ? (
              <div className="p-10 text-center text-gray-500 bg-white">{orders.length ? 'Choose a saved restaurant and delivery address for each order to see its invoice.' : 'No orders yet. Use the assistant or manual editor to create an invoice.'}</div>
            ) : (
              pages.map((p) => <div key={p.key} className="preview-paper">{p}</div>)
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
