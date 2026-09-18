import { InvoiceItem, Order } from '../types/invoice';

const num = (s: string) => parseFloat(s) || 0;

export const itemCalc = (item: InvoiceItem) => {
  const gross = num(item.grossValue);
  const discount = num(item.discount);
  const net = gross - discount;
  const cgstRate = num(item.cgstRate);
  const sgstRate = num(item.sgstRate);
  const cgst = (net * cgstRate) / 100;
  const sgst = (net * sgstRate) / 100;
  return { gross, discount, net, cgstRate, sgstRate, cgst, sgst, total: net + cgst + sgst };
};

export const orderTotals = (order: Order) => {
  const rows = order.items.map(itemCalc);
  const sum = (k: keyof ReturnType<typeof itemCalc>) => rows.reduce((a, r) => a + (r[k] as number), 0);
  return {
    rows,
    gross: sum('gross'),
    discount: sum('discount'),
    net: sum('net'),
    cgst: sum('cgst'),
    sgst: sum('sgst'),
    total: sum('total'),
  };
};

export const platformCalc = (fee: string) => {
  const taxable = num(fee);
  const cgst = taxable * 0.09;
  const sgst = taxable * 0.09;
  return { taxable, cgst, sgst, total: taxable + cgst + sgst };
};

export const ddmmyyyyToIso = (d: string) => {
  const m = d.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
  return m ? `${m[3]}-${m[2]}-${m[1]}` : d;
};

const ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'];
const tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety'];

const below1000 = (n: number): string => {
  let s = '';
  if (n >= 100) {
    s += ones[Math.floor(n / 100)] + ' Hundred';
    n %= 100;
    if (n) s += ' ';
  }
  if (n >= 20) {
    s += tens[Math.floor(n / 10)];
    if (n % 10) s += ' ' + ones[n % 10];
  } else if (n > 0) s += ones[n];
  return s;
};

const intToWords = (n: number): string => {
  if (n === 0) return 'Zero';
  const parts: string[] = [];
  const crore = Math.floor(n / 10000000);
  n %= 10000000;
  const lakh = Math.floor(n / 100000);
  n %= 100000;
  const thousand = Math.floor(n / 1000);
  n %= 1000;
  if (crore) parts.push(intToWords(crore) + ' Crore');
  if (lakh) parts.push(below1000(lakh) + ' Lakh');
  if (thousand) parts.push(below1000(thousand) + ' Thousand');
  if (n) parts.push(below1000(n));
  return parts.join(' ');
};

export const amountInWords = (amount: number) => {
  if (!Number.isFinite(amount) || amount < 0) return 'Invalid amount';
  const totalPaisa = Math.round((amount + Number.EPSILON) * 100);
  const rupees = Math.floor(totalPaisa / 100);
  const paisa = totalPaisa % 100;
  let s = `${intToWords(rupees)} Rupees`;
  if (paisa) s += ` And ${intToWords(paisa)} Paisa`;
  return s + ' Only';
};
