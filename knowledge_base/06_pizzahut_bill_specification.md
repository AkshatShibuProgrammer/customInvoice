# Specification: Authentic Pizza Hut (Devyani International Ltd) Tax Invoices

## Overview
Authentic Pizza Hut invoices in this codebase originate from Devyani International Ltd. (PHD VJ Happiness Street, Shop 4 & 5, Ground Floor, Hinjewadi, Pune).
Reference genuine bills:
- `E:/pune visit/zomato/akshat sinha.pdf` (Original Akshat Sinha — ₹3,250.80)
- `E:/pune visit/zomato/rakesh gupta.pdf` (Original Rakesh Gupta — ₹3,041.86)

## Document Geometry & Key Visual Elements
1. **Page Size & Geometry**:
   - Page dimensions: Standard A4 (`595.28 x 841.89` pt).
   - Layout: Single-column centered thermal register bill (content width ~210 pt, centered horizontally at `x ≈ 2.0 – 210.0` pt).
2. **Authentic Embedded Dynamic QR Code**:
   - Location: On Page 1 at bottom: `Rect(81.25, 789.52, 115.44, 823.70)` (34.18 x 34.18 pt square).
   - Authentic Decoded Devyani PineLabs/POS Payload Schema:
     `RR No ;AuthCode -;TDate -;TTime-cardType-cardname -GST IN NO -27AABCD5534A1Z5;HSN -996331;Invoice No-{internal_inv};Date & Time{qr_dt_str};Items -{num_items};Mode of Payment -Cash-0;Total-{total_str};SGST-{sgst_str}CGST-{cgst_str}`
   - Dynamic per-order generation:
     - `internal_inv`: Walk-in POS invoice identifier (e.g. `P720W00624`, `P720W00612`).
     - `qr_dt_str`: Format `MM/DD/YY H:MM:SS AM/PM` matching Promise Delivery Time.
     - `num_items`: Exact count of line items in order.
     - `total_str`: Net total amount formatted to 2 decimals.
     - `sgst_str` / `cgst_str`: Exact 2.5% tax components.
   - Quiet Zone / Generation Parameters: Standard QR error correction `M`, `border=4` modules, `box_size=6` ensuring instant optical decode by OpenCV and smartphone cameras.
   - **Critical Rule**: All generated Pizza Hut bills MUST generate a unique dynamic QR code matching the specific order, embedded losslessly at `Rect(81.25, 789.52, 115.44, 823.70)`.

## Mandatory Header & Legal Identifiers
- Brand: `PIZZAHUT`
- Legal Entity: `Devyani International Ltd.`
- Unit: `PHD VJ Happiness Street`
- Address: `Shop.4 & 5, Ground Floor, VJ Happiness Street, Hinjewadi, Pune`
- POS State: `Maharashtra`
- Store Contact: `8510039631`
- GSTIN: `27AABCD5534A1Z5`
- FSSAI License: `11522083000418`
- Service Code Tariff: `996331` (Restaurant service)
- Corporate Email: `devyani@dil-rjcorp.com`
- Corporate CIN: `L15135HR1991PLC143853`

## Sequential Invoice Structure
- `INVOICE` header
- `INV No.`: Format `P720202600[4-digit-id]` (e.g. `P7202026004216`, `P7202026004217`, `P7202026004218`)
- `POS No.`: `TP7221`
- `Order No.`: Format `P720202601[4-digit-id]` (e.g. `P7202026016781`, `P7202026016783`, `P7202026016785`)
- `Token No.`: Sequential 2-digit integer (e.g. 71, 73, 79, 65)
- `OLO No.`: 8-digit online tracking number (e.g. `14420297`, `15156386`)
- `Staff`: `vaishnavi`
- `Table No`: `0`
- `Guest Name`: `*** TAKEAWAY ***`
- `**DUPLICATE**` or `ORIGINAL COPY`
- Customer Name: Full employee name (`AKSHAT SINHA` or `MAYANK SIKARWAR`)
- Order Punch & Promise Delivery Times: Sequential lunch window (1:00 PM – 1:35 PM)

## Tax Calculation Architecture
- GST Rate: 5% (CGST 2.5% + SGST 2.5%)
- Subtotal + GST 5% = Total Net Bill Amount
- Payments: `Online Payment`
