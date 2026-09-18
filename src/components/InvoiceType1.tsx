import { Address, CommonSettings, Order, Restaurant } from '../types/invoice';
import { signatureDataUrl, bannerDataUrl } from '../assets/images';
import { amountInWords, ddmmyyyyToIso, orderTotals } from '../utils/calc';

const IOS_APP_URL = 'https://apps.apple.com/in/app/food-safety-connect/id6446887958';
const ANDROID_APP_URL =
  'https://play.google.com/store/apps/details?id=safety.connect.food&pcampaignid=web_share';

interface Props {
  order: Order;
  restaurant: Restaurant;
  address: Address;
  common: CommonSettings;
}

const fmt = (n: number) => n.toFixed(2);
const fmtGross = (n: number) => (Number.isInteger(n) ? String(n) : n.toFixed(2));
const fmtRate = (n: number) => `${n.toFixed(2)}%`;
const cell = (extra: React.CSSProperties = {}): React.CSSProperties => ({ padding: '3px 5px', verticalAlign: 'top', ...extra });
const B = ({ children }: { children: React.ReactNode }) => <span style={{ fontWeight: 700 }}>{children}</span>;

export default function InvoiceType1({ order, restaurant, address, common }: Props) {
  const t = orderTotals(order);

  return (
    <div className="invoice-page bg-white text-black flex flex-col" style={{ fontFamily: 'Arial, Helvetica, sans-serif' }}>
      <div className="invoice-top">
        <div className="flex justify-between items-start" style={{ marginBottom: '28px' }}>
          <h1 className="font-bold leading-none" style={{ fontSize: '48px', letterSpacing: '-1.5px' }}>eternal</h1>
          <div className="text-center" style={{ paddingTop: '6px' }}>
            <p style={{ fontSize: '15px', fontWeight: 700 }}>Tax Invoice</p>
            <p style={{ fontSize: '15px', fontWeight: 700, marginTop: '4px' }}>ORIGINAL FOR RECIPIENT</p>
          </div>
          <div style={{ width: '160px' }} />
        </div>

        <p style={{ fontSize: '13px', fontWeight: 700, marginBottom: '12px' }}>Tax Invoice on behalf of -</p>

        <div style={{ fontSize: '13px', lineHeight: 1.4, marginBottom: '12px' }}>
          <p><B>Legal Entity Name:</B> {restaurant.legalEntityName}</p>
          <p><B>Restaurant Name:</B> {restaurant.restaurantName}</p>
          <p><B>Restaurant Address:</B> {restaurant.restaurantAddress}</p>
          <p><B>Restaurant GSTIN:</B> {restaurant.restaurantGstin}</p>
          <p><B>Restaurant FSSAI:</B> {restaurant.restaurantFssai}</p>
          <p><B>Invoice No.:</B> {order.invoiceNo}</p>
          <p><B>Invoice Date:</B> {order.invoiceDate}</p>
          {order.invoiceTime && <p><B>Order Time:</B> {order.invoiceTime}</p>}
        </div>

        <div style={{ fontSize: '13px', lineHeight: 1.4, marginBottom: '12px' }}>
          <p><B>Customer Name:</B> {address.customerName}</p>
          <p><B>Delivery Address:</B> {address.deliveryAddress}</p>
          <p><B>State name and Place of Supply:</B> {address.stateName}</p>
        </div>

        <div style={{ fontSize: '13px', lineHeight: 1.4, marginBottom: '14px' }}>
          <p><B>HSN Code:</B> {common.hsnCode}</p>
          <p><B>Service Description:</B> {common.serviceDescription}</p>
        </div>

        <table className="w-full border-collapse border border-black" style={{ fontSize: '11px', marginBottom: '14px' }}>
          <thead>
            <tr>
              {['Particulars', 'Gross value', 'Discount', 'Net value', 'CGST (Rate)', 'CGST (INR)', 'SGST (Rate)', 'SGST (INR)', 'Total'].map((h) => (
                <th key={h} className="border border-black" style={{ padding: '4px 5px', textAlign: 'center', fontWeight: 700 }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {order.items.map((item, i) => {
              const r = t.rows[i];
              return (
                <tr key={item.id}>
                  <td className="border border-black" style={cell({ textAlign: 'left' })}>{item.particulars}</td>
                  <td className="border border-black" style={cell({ textAlign: 'right' })}>{fmtGross(r.gross)}</td>
                  <td className="border border-black" style={cell({ textAlign: 'right' })}>{fmt(r.discount)}</td>
                  <td className="border border-black" style={cell({ textAlign: 'right' })}>{fmt(r.net)}</td>
                  <td className="border border-black" style={cell({ textAlign: 'center' })}>{fmtRate(r.cgstRate)}</td>
                  <td className="border border-black" style={cell({ textAlign: 'center' })}>{fmt(r.cgst)}</td>
                  <td className="border border-black" style={cell({ textAlign: 'center' })}>{fmtRate(r.sgstRate)}</td>
                  <td className="border border-black" style={cell({ textAlign: 'center' })}>{fmt(r.sgst)}</td>
                  <td className="border border-black" style={cell({ textAlign: 'right' })}>{fmt(r.total)}</td>
                </tr>
              );
            })}
            <tr>
              <td className="border border-black" style={cell({ fontWeight: 700 })}>Item(s) Total</td>
              <td className="border border-black" style={cell({ textAlign: 'right', fontWeight: 700 })}>{fmt(t.gross)}</td>
              <td className="border border-black" style={cell({ textAlign: 'right', fontWeight: 700 })}>{fmt(t.discount)}</td>
              <td className="border border-black" style={cell({ textAlign: 'right', fontWeight: 700 })}>{fmt(t.net)}</td>
              <td className="border border-black" style={cell()}></td>
              <td className="border border-black" style={cell({ textAlign: 'center', fontWeight: 700 })}>{fmt(t.cgst)}</td>
              <td className="border border-black" style={cell()}></td>
              <td className="border border-black" style={cell({ textAlign: 'center', fontWeight: 700 })}>{fmt(t.sgst)}</td>
              <td className="border border-black" style={cell({ textAlign: 'right', fontWeight: 700 })}>{fmt(t.total)}</td>
            </tr>
            <tr>
              <td className="border border-black" style={cell({ fontWeight: 700 })}>Total Value</td>
              <td className="border border-black" style={cell()}></td>
              <td className="border border-black" style={cell()}></td>
              <td className="border border-black" style={cell({ textAlign: 'right', fontWeight: 700 })}>{fmt(t.net)}</td>
              <td className="border border-black" style={cell()}></td>
              <td className="border border-black" style={cell({ textAlign: 'center', fontWeight: 700 })}>{fmt(t.cgst)}</td>
              <td className="border border-black" style={cell()}></td>
              <td className="border border-black" style={cell({ textAlign: 'center', fontWeight: 700 })}>{fmt(t.sgst)}</td>
              <td className="border border-black" style={cell({ textAlign: 'right', fontWeight: 700 })}>{fmt(t.total)}</td>
            </tr>
          </tbody>
        </table>

        <p style={{ fontSize: '13px', marginBottom: '12px' }}><B>Amount (in words):</B> {amountInWords(t.total)}</p>
        <p style={{ fontSize: '13px', marginBottom: '12px' }}>
          Amount of INR {fmt(t.total)} settled digitally against Order ID {order.orderId} dated {ddmmyyyyToIso(order.invoiceDate)}.
        </p>
        <p style={{ fontSize: '13px', marginBottom: '12px' }}>Supply attracts reverse charge : {common.reverseCharge}</p>
        <p style={{ fontSize: '12px', lineHeight: 1.45 }}>{common.section95Note}</p>
      </div>

      <div className="flex-grow" />

      <div className="invoice-bottom">
        <img src={bannerDataUrl} alt="Zomato Enterprise" className="w-full block" style={{ marginBottom: '16px' }} />
        <p style={{ fontSize: '13px', fontWeight: 700, marginBottom: '8px' }}>For ETERNAL LIMITED (FORMERLY KNOWN AS ZOMATO LIMITED)</p>
        <div className="flex justify-between items-end" style={{ marginBottom: '14px' }}>
          <div style={{ fontSize: '13px', lineHeight: 1.4 }}>
            <p><B>Eternal PAN:</B> {common.eternalPan}</p>
            <p><B>Eternal CIN:</B> {common.eternalCin}</p>
            <p><B>Eternal GST :</B> {common.eternalGst}</p>
            <p><B>Eternal FSSAI :</B> {common.eternalFssai}</p>
          </div>
          <div className="text-center" style={{ minWidth: '160px', paddingRight: '20px' }}>
            <img src={signatureDataUrl} alt="Signature" style={{ height: '62px', display: 'block', margin: '0 auto 2px' }} />
            <p style={{ fontSize: '12px' }}>{common.authorisedSignatory}</p>
          </div>
        </div>
        <div className="fssai-line" style={{ fontSize: '12px', lineHeight: 1.55, fontWeight: 700 }}>
          For food safety complaints and grievances, click here to access the food safety connect app of FSSAI - IoS:{' '}
          <a href={IOS_APP_URL} target="_blank" rel="noopener noreferrer" style={{ color: '#1a0dab', textDecoration: 'underline', fontWeight: 700 }}>Food Safety Connect App</a>
          {' , '}Android:
          <br />
          <a href={ANDROID_APP_URL} target="_blank" rel="noopener noreferrer" style={{ color: '#1a0dab', textDecoration: 'underline', fontWeight: 700 }}>Food Safety Connect App</a>
        </div>
      </div>
    </div>
  );
}
