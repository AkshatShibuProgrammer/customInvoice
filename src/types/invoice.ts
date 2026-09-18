export interface InvoiceItem {
  id: string;
  particulars: string;
  grossValue: string;
  discount: string;
  cgstRate: string;
  sgstRate: string;
}

export interface Restaurant {
  id: string;
  legalEntityName: string;
  restaurantName: string;
  restaurantAddress: string;
  restaurantGstin: string;
  restaurantFssai: string;
}

export interface Address {
  id: string;
  label: string;
  customerName: string;
  deliveryAddress: string;
  stateName: string; // e.g. Madhya Pradesh (23)
}

export interface Order {
  id: string;
  restaurantId: string;
  addressId: string;
  invoiceNo: string;
  invoiceDate: string; // DD/MM/YYYY
  invoiceTime?: string; // Optional local order time, HH:MM.
  orderId: string;
  items: InvoiceItem[];
  includePlatformInvoice: boolean;
  platformInvoiceNo: string;
  platformFee: string; // taxable amount
}

export interface CommonSettings {
  hsnCode: string;
  serviceDescription: string;
  reverseCharge: string;
  section95Note: string;
  eternalAddress: string;
  eternalState: string;
  eternalEmail: string;
  customerGstin: string;
  supplyDescription: string;
  platformHsn: string;
  eternalPan: string;
  eternalCin: string;
  eternalGst: string;
  eternalFssai: string;
  authorisedSignatory: string;
  communicationAddress: string;
  termsUrl: string;
}

export interface AppData {
  restaurants: Restaurant[];
  addresses: Address[];
  orders: Order[];
  common: CommonSettings;
}

export const uid = () => Math.random().toString(36).slice(2, 10);

const rand = (chars: string, n: number) =>
  Array.from({ length: n }, () => chars[Math.floor(Math.random() * chars.length)]).join('');

export const genInvoiceNo = () => `26${rand('ABCDEFGHJKLMNPQRSTUVWXYZ0123456789', 6)}${rand('0123456789', 8)}`;
export const genPlatformInvoiceNo = () => `Z27MPOT${rand('0123456789', 9)}`;
export const genOrderId = () => `8${rand('0123456789', 9)}`;

export const todayDDMMYYYY = () => {
  const d = new Date();
  return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}/${d.getFullYear()}`;
};

export const newItem = (): InvoiceItem => ({
  id: uid(),
  particulars: '',
  grossValue: '',
  discount: '0',
  cgstRate: '2.5',
  sgstRate: '2.5',
});

export const newOrder = (restaurantId: string, addressId: string): Order => ({
  id: uid(),
  restaurantId,
  addressId,
  invoiceNo: genInvoiceNo(),
  invoiceDate: todayDDMMYYYY(),
  invoiceTime: '',
  orderId: genOrderId(),
  items: [newItem()],
  includePlatformInvoice: true,
  platformInvoiceNo: genPlatformInvoiceNo(),
  platformFee: '14.90',
});

const r1: Restaurant = {
  id: 'r1',
  legalEntityName: 'Hariom Foods',
  restaurantName: 'Sagar Gaire Fast Food - Awadhpuri',
  restaurantAddress: 'G1, G2, G3, G4, Near Vidhya Sagar College, BHEL, Bhopal',
  restaurantGstin: '23AAQFH5112G1ZM',
  restaurantFssai: '11423010000704',
};
const r2: Restaurant = {
  id: 'r2',
  legalEntityName: 'Najir Alam',
  restaurantName: 'New Zam Zam',
  restaurantAddress: '86 A, Awadhpuri, Main Road, Near Ondoor Super Market, BHEL, Bhopal',
  restaurantGstin: '',
  restaurantFssai: '21420010004125',
};
const a1: Address = {
  id: 'a1',
  label: 'Home',
  customerName: 'Akshat Sinha',
  deliveryAddress: 'H 18 Galaxy City Awadhpuri, 462043',
  stateName: 'Madhya Pradesh (23)',
};
const a2: Address = {
  id: 'a2',
  label: 'Pragati Kunj',
  customerName: 'Akshat Sinha',
  deliveryAddress: 'Pragati kunj, House no 5, 462022',
  stateName: 'Madhya Pradesh (23)',
};

export const defaultAppData: AppData = {
  restaurants: [r1, r2],
  addresses: [a1, a2],
  orders: [
    {
      id: 'o1',
      restaurantId: 'r1',
      addressId: 'a1',
      invoiceNo: '26D7AXQQ00012195',
      invoiceDate: '25/07/2026',
      orderId: '8388157899',
      items: [
        { id: 'i1', particulars: '1 x Hakka Noodles', grossValue: '186', discount: '0', cgstRate: '2.5', sgstRate: '2.5' },
        { id: 'i2', particulars: '1 x Veg Biryani', grossValue: '202', discount: '0', cgstRate: '2.5', sgstRate: '2.5' },
      ],
      includePlatformInvoice: true,
      platformInvoiceNo: 'Z27MPOT009433213',
      platformFee: '14.90',
    },
    {
      id: 'o2',
      restaurantId: 'r2',
      addressId: 'a2',
      invoiceNo: '26KCG64F00004996',
      invoiceDate: '26/07/2026',
      orderId: '8393840203',
      items: [
        { id: 'i3', particulars: '1 x Chiken Wings Fry [6 Psc With Chatni', grossValue: '295', discount: '140', cgstRate: '2.5', sgstRate: '2.5' },
      ],
      includePlatformInvoice: true,
      platformInvoiceNo: 'Z27MPOT009524381',
      platformFee: '14.90',
    },
  ],
  common: {
    hsnCode: '996331',
    serviceDescription: 'Restaurant Service',
    reverseCharge: 'No',
    section95Note:
      'This invoice covers only those items for which Eternal issues the tax invoice on behalf of the restaurant partner under Section 9(5) of the CGST Act, 2017. For other items, please refer to the invoice issued by the restaurant partner.',
    eternalAddress:
      'Unit No. 27, 28, 5th Floor, Bansal One, Habibganj Railway Station, CW-2, Bhopal, Bhopal, Madhya Pradesh, 462016',
    eternalState: 'Madhya Pradesh',
    eternalEmail: 'order@zomato.com',
    customerGstin: 'UNREGISTERED',
    supplyDescription: 'Other Services N.E.C',
    platformHsn: '999799',
    eternalPan: 'AADCD4946L',
    eternalCin: 'L93030DL2010PLC198141',
    eternalGst: '23AADCD4946L1ZI',
    eternalFssai: '10019064001810',
    authorisedSignatory: 'Authorised Signatory',
    communicationAddress: 'Pioneer Square, Ground Floor, Golf Course Extension, Gurugram, Haryana, 122102',
    termsUrl: 'https://www.zomato.com/conditions',
  },
};
