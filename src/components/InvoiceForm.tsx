import { useEffect, useId, useState } from 'react';
import {
  Address, AppData, CommonSettings, Order, Restaurant,
  genInvoiceNo, genOrderId, genPlatformInvoiceNo, newItem, newOrder, uid,
} from '../types/invoice';
import { orderTotals } from '../utils/calc';
import { Copy, Plus, RefreshCw, Trash2 } from 'lucide-react';

interface Props {
  data: AppData;
  onChange: (d: AppData) => void;
  selectedOrderId: string | null;
  onSelectOrder: (id: string | null) => void;
  focusOrdersToken?: number;
}

const inp = 'w-full border border-gray-300 rounded px-2 py-1 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500';
const lbl = 'text-xs font-medium text-gray-600 mb-0.5 block';
const card = 'bg-gray-50 border border-gray-200 rounded p-3 mb-3';

function Field({ label, value, onChange, span }: { label: string; value: string; onChange: (v: string) => void; span?: boolean }) {
  const id = useId();
  return (
    <div className={span ? 'md:col-span-2' : ''}>
      <label className={lbl} htmlFor={id}>{label}</label>
      <input id={id} className={inp} value={value} onChange={(e) => onChange(e.target.value)} />
    </div>
  );
}

export default function InvoiceForm({ data, onChange, selectedOrderId, onSelectOrder, focusOrdersToken }: Props) {
  const [tab, setTab] = useState<'orders' | 'profiles' | 'settings'>('orders');
  useEffect(() => { setTab('orders'); }, [focusOrdersToken]);

  const setOrders = (orders: Order[]) => onChange({ ...data, orders });
  const updOrder = (id: string, patch: Partial<Order>) => setOrders(data.orders.map((o) => (o.id === id ? { ...o, ...patch } : o)));
  const setRestaurants = (restaurants: Restaurant[]) => onChange({ ...data, restaurants });
  const setAddresses = (addresses: Address[]) => onChange({ ...data, addresses });
  const setCommon = (patch: Partial<CommonSettings>) => onChange({ ...data, common: { ...data.common, ...patch } });

  const addOrder = () => {
    const last = data.orders[data.orders.length - 1];
    const o = newOrder(last?.restaurantId ?? data.restaurants[0]?.id ?? '', last?.addressId ?? data.addresses[0]?.id ?? '');
    setOrders([...data.orders, o]);
    onSelectOrder(o.id);
  };
  const duplicateOrder = (o: Order) => {
    const copy: Order = {
      ...o, id: uid(), invoiceNo: genInvoiceNo(), orderId: genOrderId(), platformInvoiceNo: genPlatformInvoiceNo(),
      items: o.items.map((i) => ({ ...i, id: uid() })),
    };
    setOrders([...data.orders, copy]);
    onSelectOrder(copy.id);
  };
  const removeOrder = (id: string) => {
    setOrders(data.orders.filter((o) => o.id !== id));
    if (selectedOrderId === id) onSelectOrder(null);
  };

  const addRestaurant = () => setRestaurants([...data.restaurants, { id: uid(), legalEntityName: '', restaurantName: 'New Restaurant', restaurantAddress: '', restaurantGstin: '', restaurantFssai: '' }]);
  const addAddress = () => setAddresses([...data.addresses, { id: uid(), label: 'New Address', customerName: data.addresses[0]?.customerName ?? '', deliveryAddress: '', stateName: 'Madhya Pradesh (23)' }]);

  const TabBtn = ({ id, label }: { id: typeof tab; label: string }) => (
    <button onClick={() => setTab(id)} className={`px-3 py-1.5 text-sm rounded-t border-b-2 ${tab === id ? 'border-blue-600 text-blue-700 font-semibold' : 'border-transparent text-gray-500 hover:text-gray-800'}`}>{label}</button>
  );

  return (
    <div>
      <div className="flex flex-wrap gap-1 border-b border-gray-200 mb-3">
        <TabBtn id="orders" label={`Orders (${data.orders.length})`} />
        <TabBtn id="profiles" label="Restaurants & Addresses" />
        <TabBtn id="settings" label="Company Settings" />
      </div>

      {/* ================= ORDERS ================= */}
      {tab === 'orders' && (
        <div>
          {(!data.restaurants.length || !data.addresses.length) && <div className="manual-setup-notice"><p>Save at least one restaurant and delivery address before adding an order.</p><button type="button" onClick={() => setTab('profiles')}>Set up restaurants &amp; addresses</button></div>}
          <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
            <div className="flex min-w-0 max-w-full items-center gap-2 text-sm">
              <span className="text-gray-600">Preview:</span>
              <select aria-label="Select orders to preview" className="min-w-0 border border-gray-300 rounded px-2 py-1 text-sm" value={selectedOrderId ?? ''} onChange={(e) => onSelectOrder(e.target.value || null)}>
                <option value="">All orders</option>
                {data.orders.map((o, i) => <option key={o.id} value={o.id}>#{i + 1} · {o.invoiceDate} · {o.invoiceNo}</option>)}
              </select>
            </div>
            <button onClick={addOrder} disabled={!data.restaurants.length || !data.addresses.length} className="flex items-center gap-1 bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700 disabled:opacity-40"><Plus size={16} /> Add Order</button>
          </div>

          {data.orders.map((o, idx) => {
            const t = orderTotals(o);
            const open = selectedOrderId === null || selectedOrderId === o.id;
            return (
              <div key={o.id} className={`${card} ${selectedOrderId === o.id ? 'ring-2 ring-blue-400' : ''}`}>
                <div className="flex items-center justify-between mb-2">
                  <button type="button" className="text-left text-sm font-semibold" aria-expanded={open} onClick={() => onSelectOrder(selectedOrderId === o.id ? null : o.id)}>
                    Order #{idx + 1} <span className="font-normal text-gray-500">/ {data.restaurants.find((r) => r.id === o.restaurantId)?.restaurantName ?? 'Select a restaurant'} / {o.invoiceDate}{o.invoiceTime ? ` ${o.invoiceTime}` : ''} / INR {t.total.toFixed(2)}</span>
                  </button>
                  <div className="flex gap-1" onClick={(e) => e.stopPropagation()}>
                    <button title="Duplicate" onClick={() => duplicateOrder(o)} className="p-1 text-gray-500 hover:text-blue-600"><Copy size={16} /></button>
                    <button title="Delete" onClick={() => removeOrder(o.id)} className="p-1 text-gray-500 hover:text-red-600"><Trash2 size={16} /></button>
                  </div>
                </div>

                {open && (
                  <>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mb-2">
                      <div>
                        <label className={lbl}>Restaurant</label>
                        <select className={inp} value={o.restaurantId} onChange={(e) => updOrder(o.id, { restaurantId: e.target.value })}>
                          {data.restaurants.map((r) => <option key={r.id} value={r.id}>{r.restaurantName}</option>)}
                        </select>
                      </div>
                      <div>
                        <label className={lbl}>Delivery Address</label>
                        <select className={inp} value={o.addressId} onChange={(e) => updOrder(o.id, { addressId: e.target.value })}>
                          {data.addresses.map((a) => <option key={a.id} value={a.id}>{a.label} — {a.deliveryAddress}</option>)}
                        </select>
                      </div>
                      <div>
                        <label className={lbl}>Invoice Date (DD/MM/YYYY)</label>
                        <input className={inp} value={o.invoiceDate} onChange={(e) => updOrder(o.id, { invoiceDate: e.target.value })} />
                      </div>
                      <div>
                        <label className={lbl} htmlFor={`order-time-${o.id}`}>Order time (optional, local time)</label>
                        <input id={`order-time-${o.id}`} type="time" className={inp} value={o.invoiceTime ?? ''} onChange={(e) => updOrder(o.id, { invoiceTime: e.target.value })} />
                      </div>
                      <div>
                        <label className={lbl}>Order ID</label>
                        <div className="flex gap-1">
                          <input className={inp} value={o.orderId} onChange={(e) => updOrder(o.id, { orderId: e.target.value })} />
                          <button title="Regenerate" onClick={() => updOrder(o.id, { orderId: genOrderId() })} className="p-1 text-gray-500 hover:text-blue-600"><RefreshCw size={14} /></button>
                        </div>
                      </div>
                      <div>
                        <label className={lbl}>Restaurant Invoice No.</label>
                        <div className="flex gap-1">
                          <input className={inp} value={o.invoiceNo} onChange={(e) => updOrder(o.id, { invoiceNo: e.target.value })} />
                          <button title="Regenerate" onClick={() => updOrder(o.id, { invoiceNo: genInvoiceNo() })} className="p-1 text-gray-500 hover:text-blue-600"><RefreshCw size={14} /></button>
                        </div>
                      </div>
                      <div>
                        <label className={lbl}>Platform Invoice No.</label>
                        <div className="flex gap-1">
                          <input className={inp} value={o.platformInvoiceNo} onChange={(e) => updOrder(o.id, { platformInvoiceNo: e.target.value })} />
                          <button title="Regenerate" onClick={() => updOrder(o.id, { platformInvoiceNo: genPlatformInvoiceNo() })} className="p-1 text-gray-500 hover:text-blue-600"><RefreshCw size={14} /></button>
                        </div>
                      </div>
                      <div className="flex items-end gap-3">
                        <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={o.includePlatformInvoice} onChange={(e) => updOrder(o.id, { includePlatformInvoice: e.target.checked })} /> Include platform-fee invoice</label>
                      </div>
                      <div>
                        <label className={lbl}>Platform fee (taxable, ₹)</label>
                        <input className={inp} value={o.platformFee} onChange={(e) => updOrder(o.id, { platformFee: e.target.value })} />
                      </div>
                    </div>

                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-semibold text-gray-700">Food Items</span>
                      <button onClick={() => updOrder(o.id, { items: [...o.items, newItem()] })} className="text-xs text-blue-600 hover:underline flex items-center gap-1"><Plus size={12} /> Add item</button>
                    </div>
                    <div className="overflow-x-auto">
                    <table className="w-full min-w-[470px] text-xs border border-gray-300">
                      <thead className="bg-gray-100">
                        <tr>
                          <th className="border px-1 py-1 text-left">Particulars (e.g. 1 x Veg Biryani)</th>
                          <th className="border px-1 py-1 w-16">Gross</th>
                          <th className="border px-1 py-1 w-16">Disc.</th>
                          <th className="border px-1 py-1 w-14">CGST%</th>
                          <th className="border px-1 py-1 w-14">SGST%</th>
                          <th className="border px-1 py-1 w-16">Total</th>
                          <th className="border px-1 py-1 w-8"></th>
                        </tr>
                      </thead>
                      <tbody>
                        {o.items.map((it, i) => {
                          const upd = (patch: Partial<typeof it>) => updOrder(o.id, { items: o.items.map((x) => (x.id === it.id ? { ...x, ...patch } : x)) });
                          return (
                            <tr key={it.id}>
                              <td className="border px-1"><input className="w-full outline-none py-1" value={it.particulars} onChange={(e) => upd({ particulars: e.target.value })} /></td>
                              <td className="border px-1"><input className="w-full outline-none py-1 text-right" value={it.grossValue} onChange={(e) => upd({ grossValue: e.target.value })} /></td>
                              <td className="border px-1"><input className="w-full outline-none py-1 text-right" value={it.discount} onChange={(e) => upd({ discount: e.target.value })} /></td>
                              <td className="border px-1"><input className="w-full outline-none py-1 text-center" value={it.cgstRate} onChange={(e) => upd({ cgstRate: e.target.value })} /></td>
                              <td className="border px-1"><input className="w-full outline-none py-1 text-center" value={it.sgstRate} onChange={(e) => upd({ sgstRate: e.target.value })} /></td>
                              <td className="border px-1 text-right">{t.rows[i].total.toFixed(2)}</td>
                              <td className="border text-center"><button disabled={o.items.length <= 1} onClick={() => updOrder(o.id, { items: o.items.filter((x) => x.id !== it.id) })} className="text-red-500 disabled:opacity-30">×</button></td>
                            </tr>
                          );
                        })}
                        <tr className="bg-gray-50 font-semibold">
                          <td className="border px-1 py-1">Total</td>
                          <td className="border px-1 text-right">{t.gross.toFixed(2)}</td>
                          <td className="border px-1 text-right">{t.discount.toFixed(2)}</td>
                          <td className="border px-1 text-center">{t.cgst.toFixed(2)}</td>
                          <td className="border px-1 text-center">{t.sgst.toFixed(2)}</td>
                          <td className="border px-1 text-right">{t.total.toFixed(2)}</td>
                          <td className="border"></td>
                        </tr>
                      </tbody>
                    </table>
                    </div>
                  </>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* ================= PROFILES ================= */}
      {tab === 'profiles' && (
        <div>
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-semibold">Restaurants</h3>
            <button onClick={addRestaurant} className="text-sm text-blue-600 flex items-center gap-1"><Plus size={14} /> Add restaurant</button>
          </div>
          {data.restaurants.map((r) => {
            const upd = (patch: Partial<Restaurant>) => setRestaurants(data.restaurants.map((x) => (x.id === r.id ? { ...x, ...patch } : x)));
            const inUse = data.orders.some((o) => o.restaurantId === r.id);
            return (
              <div key={r.id} className={card}>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  <Field label="Restaurant Name" value={r.restaurantName} onChange={(v) => upd({ restaurantName: v })} />
                  <Field label="Legal Entity Name" value={r.legalEntityName} onChange={(v) => upd({ legalEntityName: v })} />
                  <Field label="Restaurant Address" value={r.restaurantAddress} onChange={(v) => upd({ restaurantAddress: v })} span />
                  <Field label="Restaurant GSTIN" value={r.restaurantGstin} onChange={(v) => upd({ restaurantGstin: v })} />
                  <Field label="Restaurant FSSAI" value={r.restaurantFssai} onChange={(v) => upd({ restaurantFssai: v })} />
                </div>
                <div className="text-right mt-1">
                  <button disabled={inUse || data.restaurants.length <= 1} title={inUse ? 'Used by an order' : 'Delete'} onClick={() => setRestaurants(data.restaurants.filter((x) => x.id !== r.id))} className="text-xs text-red-500 disabled:opacity-30">Delete</button>
                </div>
              </div>
            );
          })}

          <div className="flex items-center justify-between mb-2 mt-5">
            <h3 className="text-sm font-semibold">Delivery Addresses</h3>
            <button onClick={addAddress} className="text-sm text-blue-600 flex items-center gap-1"><Plus size={14} /> Add address</button>
          </div>
          {data.addresses.map((a) => {
            const upd = (patch: Partial<Address>) => setAddresses(data.addresses.map((x) => (x.id === a.id ? { ...x, ...patch } : x)));
            const inUse = data.orders.some((o) => o.addressId === a.id);
            return (
              <div key={a.id} className={card}>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  <Field label="Label" value={a.label} onChange={(v) => upd({ label: v })} />
                  <Field label="Customer Name" value={a.customerName} onChange={(v) => upd({ customerName: v })} />
                  <Field label="Delivery Address" value={a.deliveryAddress} onChange={(v) => upd({ deliveryAddress: v })} span />
                  <Field label="State name and Place of Supply" value={a.stateName} onChange={(v) => upd({ stateName: v })} span />
                </div>
                <div className="text-right mt-1">
                  <button disabled={inUse || data.addresses.length <= 1} title={inUse ? 'Used by an order' : 'Delete'} onClick={() => setAddresses(data.addresses.filter((x) => x.id !== a.id))} className="text-xs text-red-500 disabled:opacity-30">Delete</button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* ================= SETTINGS ================= */}
      {tab === 'settings' && (
        <div>
          <div className={card}>
            <h3 className="text-sm font-semibold mb-2">Restaurant Invoice</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              <Field label="HSN Code" value={data.common.hsnCode} onChange={(v) => setCommon({ hsnCode: v })} />
              <Field label="Service Description" value={data.common.serviceDescription} onChange={(v) => setCommon({ serviceDescription: v })} />
              <Field label="Supply attracts reverse charge" value={data.common.reverseCharge} onChange={(v) => setCommon({ reverseCharge: v })} />
              <div className="md:col-span-2">
                <label className={lbl}>Section 9(5) Note</label>
                <textarea className={inp} rows={3} value={data.common.section95Note} onChange={(e) => setCommon({ section95Note: e.target.value })} />
              </div>
            </div>
          </div>
          <div className={card}>
            <h3 className="text-sm font-semibold mb-2">Platform-fee Invoice</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              <Field label="Eternal Address" value={data.common.eternalAddress} onChange={(v) => setCommon({ eternalAddress: v })} span />
              <Field label="State" value={data.common.eternalState} onChange={(v) => setCommon({ eternalState: v })} />
              <Field label="Email ID" value={data.common.eternalEmail} onChange={(v) => setCommon({ eternalEmail: v })} />
              <Field label="Customer GSTIN" value={data.common.customerGstin} onChange={(v) => setCommon({ customerGstin: v })} />
              <Field label="HSN Code" value={data.common.platformHsn} onChange={(v) => setCommon({ platformHsn: v })} />
              <Field label="Supply Description" value={data.common.supplyDescription} onChange={(v) => setCommon({ supplyDescription: v })} span />
            </div>
          </div>
          <div className={card}>
            <h3 className="text-sm font-semibold mb-2">Eternal Limited</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              <Field label="PAN" value={data.common.eternalPan} onChange={(v) => setCommon({ eternalPan: v })} />
              <Field label="CIN" value={data.common.eternalCin} onChange={(v) => setCommon({ eternalCin: v })} />
              <Field label="GST" value={data.common.eternalGst} onChange={(v) => setCommon({ eternalGst: v })} />
              <Field label="FSSAI" value={data.common.eternalFssai} onChange={(v) => setCommon({ eternalFssai: v })} />
              <Field label="Authorised Signatory" value={data.common.authorisedSignatory} onChange={(v) => setCommon({ authorisedSignatory: v })} />
              <Field label="Terms URL" value={data.common.termsUrl} onChange={(v) => setCommon({ termsUrl: v })} />
              <Field label="Communication Address" value={data.common.communicationAddress} onChange={(v) => setCommon({ communicationAddress: v })} span />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
