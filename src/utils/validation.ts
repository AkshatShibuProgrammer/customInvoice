import { defaultAppData } from '../types/invoice';
import type { AppData, Order } from '../types/invoice';

export function isRecord(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

export function normalizeDate(value: string): string {
  const iso = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value.trim());
  return iso ? `${iso[3]}/${iso[2]}/${iso[1]}` : value.trim();
}

export function isValidDate(value: string): boolean {
  const match = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(normalizeDate(value));
  if (!match) return false;
  const [, day, month, year] = match.map(Number);
  const date = new Date(year, month - 1, day);
  return year >= 1900 && year <= 2200 && date.getFullYear() === year && date.getMonth() === month - 1 && date.getDate() === day;
}

export const isValidTime = (value: string) => value === '' || /^([01]\d|2[0-3]):[0-5]\d$/.test(value);

export function validNumber(value: string, max = 100000000, allowPercent = false): boolean {
  const clean = allowPercent ? value.trim().replace(/%$/, '') : value.trim();
  return /^(?:\d+(?:\.\d+)?|\.\d+)$/.test(clean) && Number.isFinite(Number(clean)) && Number(clean) <= max;
}

export function validateOrders(data: AppData, orders: Order[]): string[] {
  const issues: string[] = [];
  const seen = new Set<string>();
  for (const order of data.orders) {
    for (const ref of [order.invoiceNo, ...(order.includePlatformInvoice ? [order.platformInvoiceNo] : [])]) {
      const key = ref.trim().toLowerCase();
      if (key && seen.has(key) && orders.some((o) => o.invoiceNo.trim().toLowerCase() === key || (o.includePlatformInvoice && o.platformInvoiceNo.trim().toLowerCase() === key))) {
        issues.push(`Duplicate invoice number: ${ref}.`);
      }
      seen.add(key);
    }
  }
  orders.forEach((order, index) => {
    const label = `Order ${index + 1}`;
    const restaurant = data.restaurants.find((r) => r.id === order.restaurantId);
    const address = data.addresses.find((a) => a.id === order.addressId);
    if (!restaurant?.restaurantName.trim() || !restaurant.legalEntityName.trim() || !restaurant.restaurantAddress.trim()) issues.push(`${label}: add the restaurant name, legal entity, and address.`);
    if (!address?.customerName.trim() || !address.deliveryAddress.trim() || !address.stateName.trim()) issues.push(`${label}: add the customer name, delivery address, and place of supply.`);
    if (!order.invoiceNo.trim() || !order.orderId.trim()) issues.push(`${label}: invoice number and order ID are required.`);
    if (!isValidDate(order.invoiceDate)) issues.push(`${label}: enter a valid date in DD/MM/YYYY format.`);
    if (!isValidTime(order.invoiceTime ?? '')) issues.push(`${label}: use a time in HH:MM format.`);
    if (!order.items.length) issues.push(`${label}: add at least one food item.`);
    order.items.forEach((item, i) => {
      if (!item.particulars.trim() || !validNumber(item.grossValue) || !validNumber(item.discount) || Number(item.discount) > Number(item.grossValue) || !validNumber(item.cgstRate, 100, true) || !validNumber(item.sgstRate, 100, true)) {
        issues.push(`${label}, item ${i + 1}: check the description, nonnegative amounts, discount, and tax rates (0-100%).`);
      }
    });
    if (order.includePlatformInvoice && (!order.platformInvoiceNo.trim() || !validNumber(order.platformFee))) issues.push(`${label}: check the platform invoice number and fee.`);
  });
  return [...new Set(issues)];
}

// Only admit known fields when restoring browser data or an embedded HTML snapshot.
export function parseWorkspace(value: unknown): AppData | null {
  if (!isRecord(value) || !Array.isArray(value.orders) || !Array.isArray(value.restaurants) || !Array.isArray(value.addresses) || !isRecord(value.common)) return null;
  if (value.orders.length > 1000 || value.restaurants.length > 1000 || value.addresses.length > 1000) return null;
  const readFields = (entry: unknown, fields: string[]) => {
    if (!isRecord(entry)) throw new Error('Invalid stored record.');
    const out: Record<string, string> = {};
    for (const field of fields) {
      if (typeof entry[field] !== 'string' || (entry[field] as string).length > 15000) throw new Error('Invalid stored field.');
      out[field] = entry[field] as string;
    }
    return out;
  };
  try {
    const restaurants = value.restaurants.map((r) => readFields(r, ['id', 'legalEntityName', 'restaurantName', 'restaurantAddress', 'restaurantGstin', 'restaurantFssai']));
    const addresses = value.addresses.map((a) => readFields(a, ['id', 'label', 'customerName', 'deliveryAddress', 'stateName']));
    const orders = value.orders.map((o) => {
      if (!isRecord(o) || !Array.isArray(o.items) || o.items.length > 200 || typeof o.includePlatformInvoice !== 'boolean') throw new Error('Invalid stored order.');
      return {
        ...readFields(o, ['id', 'restaurantId', 'addressId', 'invoiceNo', 'invoiceDate', 'orderId', 'platformInvoiceNo', 'platformFee']),
        invoiceTime: typeof o.invoiceTime === 'string' ? o.invoiceTime.slice(0, 5) : '',
        includePlatformInvoice: o.includePlatformInvoice,
        items: o.items.map((item) => readFields(item, ['id', 'particulars', 'grossValue', 'discount', 'cgstRate', 'sgstRate'])),
      };
    });
    for (const collection of [restaurants, addresses, orders]) {
      const ids = collection.map((entry) => (entry as Record<string, unknown>).id);
      if (ids.some((id) => typeof id !== 'string' || !id) || new Set(ids).size !== ids.length) return null;
    }
    const common = { ...defaultAppData.common };
    for (const key of Object.keys(common) as (keyof typeof common)[]) {
      const field = value.common[key];
      if (typeof field === 'string' && field.length <= 15000) common[key] = field;
    }
    return { restaurants, addresses, orders, common } as unknown as AppData;
  } catch {
    return null;
  }
}