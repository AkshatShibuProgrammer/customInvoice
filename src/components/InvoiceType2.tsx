import { Address, CommonSettings, Order } from '../types/invoice';
import { signatureDataUrl } from '../assets/images';
import { ddmmyyyyToIso, platformCalc } from '../utils/calc';

interface Props {
  order: Order;
  address: Address;
  common: CommonSettings;
}

const B = ({ children }: { children: React.ReactNode }) => <span style={{ fontWeight: 700 }}>{children}</span>;
const Bar = ({ children }: { children: React.ReactNode }) => (
  <div className="border border-black bg-gray-200" style={{ padding: '7px 12px', marginBottom: '12px' }}>
    <p style={{ fontSize: '13px', fontWeight: 700 }}>{children}</p>
  </div>
);
const td: React.CSSProperties = { padding: '8px 12px', textAlign: 'center' };

export default function InvoiceType2({ order, address, common }: Props) {
  const p = platformCalc(order.platformFee);
  const iso = ddmmyyyyToIso(order.invoiceDate);
  const total3 = p.total.toFixed(3);

  return (
    <div className="invoice-page bg-white text-black flex flex-col" style={{ fontFamily: 'Arial, Helvetica, sans-serif' }}>
      <div className="invoice-top">
        <div className="flex justify-between items-start" style={{ marginBottom: '28px' }}>
          <h1 className="font-bold leading-none" style={{ fontSize: '48px', letterSpacing: '-1.5px' }}>eternal</h1>
          <p style={{ fontSize: '15px', fontWeight: 700, paddingTop: '10px' }}>ORIGINAL FOR RECIPIENT</p>
          <div style={{ width: '120px' }} />
        </div>

        <h2 style={{ fontSize: '18px', fontWeight: 700, marginBottom: '16px' }}>Tax Invoice</h2>

        <Bar>ETERNAL LIMITED (FORMERLY KNOWN AS ZOMATO LIMITED)</Bar>
        <div className="flex" style={{ fontSize: '13px', lineHeight: 1.4, marginBottom: '20px' }}>
          <div style={{ width: '60%', paddingRight: '10px' }}>
            <p><B>Address:</B> {common.eternalAddress}</p>
            <p><B>State:</B> {common.eternalState}</p>
            <p><B>Email ID:</B> {common.eternalEmail}</p>
            <p><B>Invoice No:</B> {order.platformInvoiceNo}</p>
          </div>
          <div style={{ width: '40%' }}>
            <p><B>PAN:</B> {common.eternalPan}</p>
            <p><B>CIN:</B> {common.eternalCin}</p>
            <p><B>GSTIN:</B> {common.eternalGst}</p>
            <p><B>Invoice Date:</B> {iso}</p>
            {order.invoiceTime && <p><B>Order Time:</B> {order.invoiceTime}</p>}
          </div>
        </div>

        <Bar>Customer Details</Bar>
        <div className="flex" style={{ fontSize: '13px', lineHeight: 1.4, marginBottom: '20px' }}>
          <div style={{ width: '60%' }}>
            <p><B>Name:</B> {address.customerName}</p>
            <p><B>Delivery Address:</B> {address.deliveryAddress}</p>
          </div>
          <div style={{ width: '40%' }}>
            <p><B>GSTIN:</B> {common.customerGstin}</p>
            <p><B>Place of Supply:</B> {address.stateName.replace(' (', '(')}</p>
          </div>
        </div>

        <Bar>Service Details</Bar>
        <div className="flex" style={{ fontSize: '13px', marginBottom: '20px' }}>
          <div style={{ width: '60%' }}><p><B>HSN Code:</B> {common.platformHsn}</p></div>
          <div style={{ width: '40%' }}><p><B>Supply Description:</B> {common.supplyDescription}</p></div>
        </div>

        <table className="w-full border-collapse border border-black" style={{ fontSize: '13px', marginBottom: '28px' }}>
          <thead>
            <tr>
              {['Sr.No', 'Particulars', 'Taxable Amount', 'CGST', 'SGST', 'Total'].map((h) => (
                <th key={h} className="border border-black" style={{ ...td, fontWeight: 700 }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="border border-black" style={td}>1</td>
              <td className="border border-black" style={{ ...td, textAlign: 'left' }}>Platform fee</td>
              <td className="border border-black" style={td}>{p.taxable.toFixed(2)}</td>
              <td className="border border-black" style={td}>{p.cgst.toFixed(2)}</td>
              <td className="border border-black" style={td}>{p.sgst.toFixed(2)}</td>
              <td className="border border-black" style={td}>{total3}</td>
            </tr>
            <tr style={{ fontWeight: 700 }}>
              <td className="border border-black" style={{ ...td, textAlign: 'left' }} colSpan={2}>Total</td>
              <td className="border border-black" style={td}>{p.taxable.toFixed(2)}</td>
              <td className="border border-black" style={td}>{p.cgst.toFixed(2)}</td>
              <td className="border border-black" style={td}>{p.sgst.toFixed(2)}</td>
              <td className="border border-black" style={td}>{total3}</td>
            </tr>
          </tbody>
        </table>

        <div style={{ fontSize: '13px', lineHeight: 1.5 }}>
          <p>Amount of ₹{total3} settled through digital mode/payment received against Order id ({order.orderId}) dated ({iso})</p>
          <p>Tax is not payable on reverse charge basis</p>
        </div>
      </div>

      <div className="flex-grow" />

      <div className="invoice-bottom">
        <div style={{ textAlign: 'right', paddingRight: '40px', marginBottom: '20px' }}>
          <p style={{ fontSize: '13px', fontWeight: 700, marginBottom: '20px' }}>For ETERNAL LIMITED (FORMERLY KNOWN AS ZOMATO LIMITED)</p>
          <div style={{ display: 'inline-block', textAlign: 'center', paddingRight: '60px' }}>
            <img src={signatureDataUrl} alt="Signature" style={{ height: '70px', display: 'block', margin: '0 auto 6px' }} />
            <p style={{ fontSize: '13px' }}>{common.authorisedSignatory === 'Authorised Signatory' ? 'Authorized Signatory' : common.authorisedSignatory}</p>
          </div>
        </div>
        <div className="border-t border-black text-center" style={{ paddingTop: '14px', fontSize: '13px' }}>
          <p style={{ marginBottom: '12px' }}>Communication Address: {common.communicationAddress}</p>
          <p>Please refer to {common.termsUrl} for current version of full terms and conditions which are incorporated in this invoice by reference.</p>
        </div>
      </div>
    </div>
  );
}
