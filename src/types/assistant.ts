import type { Address, AppData, Restaurant } from './invoice';

export interface ConversationMessage {
  id: string;
  role: 'user' | 'assistant';
  text: string;
}

export interface DraftRestaurant extends Omit<Restaurant, 'id'> {
  existingId: string;
}

export interface DraftAddress extends Omit<Address, 'id'> {
  existingId: string;
}

export interface DraftItem {
  name: string;
  quantity: number | null;
  unitPrice: number | null;
  discount: number | null;
  cgstRate: number | null;
  sgstRate: number | null;
}

export interface DraftOrder {
  restaurant: DraftRestaurant;
  address: DraftAddress;
  invoiceDate: string;
  invoiceTime: string;
  invoiceNo: string;
  orderId: string;
  items: DraftItem[];
  includePlatformInvoice: boolean | null;
  platformInvoiceNo: string;
  platformFee: number | null;
}

export interface AssistantDraft {
  message: string;
  questions: string[];
  orders: DraftOrder[];
}

export interface DraftOptions {
  useDefaults: boolean;
  generateReferences: boolean;
}

export interface PreparedDraft {
  preview: AppData;
  newRestaurants: Restaurant[];
  newAddresses: Address[];
  issues: string[];
  notes: string[];
}