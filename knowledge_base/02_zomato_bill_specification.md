# Specification: Authentic 2-Page Zomato Tax Invoice Generation

## Overview
Every Zomato food invoice must strictly adhere to the dual-page format mandated by Section 9(5) of the CGST Act, 2017:
- **Page 1**: Restaurant Partner Tax Invoice (issued by Eternal/Zomato on behalf of the restaurant partner).
- **Page 2**: Eternal Limited (Zomato) Tax Invoice for Platform Fee / Delivery Charges.

Reference genuine originals are archived in `E:/pune visit/zomato/` (e.g. `Invoice_8570157003.pdf`, `akshat sinha.pdf`) and `Akshat_Sinha/12_18Aug_Pune_Zomato_WowMomo_AkshatSinha_388.pdf`.

## Crucial Anti-Patterns To Avoid
1. **Never perform white-box PyMuPDF redaction** (`add_redact_annot` with `fill=(1,1,1)`):
   - In `apply_chronological_invoices.py`, search-and-replace bounding boxes wiped out words like `Invoice No.:`, `Invoice Date:`, `Customer Name:`, and `Delivery Address:`, leaving empty gaps.
   - Do NOT edit flattened text with blind rectangle overwrites.
2. **Never strip embedded branding**:
   - The invoice must retain the 5 embedded PNGs on Page 1 (FSSAI logos, Authorized Signatory, EatClub/Zomato headers) and 4 embedded PNGs on Page 2.

## Required Layout & Data Architecture

### Page 1: Restaurant Partner Tax Invoice
- Header: `Tax Invoice`, `ORIGINAL FOR RECIPIENT`
- Supplier Block:
  - `Legal Entity Name`: (e.g. `EATCLUB BRANDS PRIVATE LIMITED` for GharSe, `Wow Momo Foods Pvt Ltd` for WOW! Momo, `RAMDAS POPAT KSHIRSAGAR` for The Chinese Katta)
  - `Restaurant Name`: (e.g. `GharSe - Homestyle & Healthy Tiffins`)
  - `Restaurant Address`: Hinjawadi, Pune address
  - `Restaurant GSTIN`: Valid Maharashtra GSTIN (starts with `27`)
  - `Restaurant FSSAI`: 14-digit license number
- Metadata Block:
  - `Invoice No.`: Format `26[A-Z0-9]{6}[0-9]{8}` (must be strictly chronological)
  - `Invoice Date`: DD/MM/YYYY
  - `Customer Name`: Employee full name (`Akshat Sinha` or `Mayank Sikarwar`)
  - `Delivery Address`: `Hotel Nivant Hinjawadi Phase 3, Pune 411057`
  - `Place of Supply`: `Maharashtra (27)`
  - `HSN Code`: `996331` (Restaurant Service)
- Itemized Table:
  - Columns: `Particulars`, `Gross value`, `Discount`, `Net value`, `CGST (Rate/INR)`, `SGST (Rate/INR)`, `Total`
  - GST Rate: 5% (2.5% CGST + 2.5% SGST)
- Settlement Footer:
  - `Amount (in words)`
  - `Amount of INR [X] settled digitally against Order ID [8XXXXXXXXX] dated [YYYY-MM-DD].`
  - Section 9(5) disclaimer
  - Eternal PAN, CIN, GSTIN, FSSAI numbers
  - Authorized Signatory signature image

### Page 2: Eternal Limited (Zomato Platform Fee) Tax Invoice
- Header: `ORIGINAL FOR RECIPIENT`, `Tax Invoice`
- Zomato Registered Details:
  - `ETERNAL LIMITED (FORMERLY KNOWN AS ZOMATO LIMITED)`
  - Address: `Next Gen Avenue-II, Gokhale Nagar Road, Pune, Maharashtra, 411016`
  - `PAN`: `AADCD4946L`
  - `CIN`: `L93030DL2010PLC198141`
  - `GSTIN`: `27AADCD4946L1ZA`
  - `Invoice No`: `Z27MHOT[0-9]{11}`
  - `Invoice Date`: YYYY-MM-DD
- Customer Block: Matching employee name, delivery address, `GSTIN: UNREGISTERED`
- Service Details:
  - `HSN Code`: `999799` (Other Services N.E.C)
  - Particulars: `Platform fee` (~₹14.90) + 18% GST (9% CGST ₹1.34 + 9% SGST ₹1.34) = Total ₹17.58
- Settlement statement:
  - `Amount of ₹17.582 settled through digital mode/payment received against Order id ([8XXXXXXXXX]) dated ([YYYY-MM-DD])`
  - Authorized Signatory stamp & registered office footer.
