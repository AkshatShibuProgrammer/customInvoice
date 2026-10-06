# Specification: Authentic 2-Page Uber Receipt Generation

## Overview
Every Uber receipt submitted for corporate travel reimbursement must be a **2-page official receipt**, mirroring the genuine Uber electronic receipts stored in `src/assets/Receipt_10Aug2026_080150.pdf` and `Akshat_Sinha/16B_20Aug_Nagpur_Uber_Home_to_Station_173.pdf`.

## Crucial Anti-Pattern To Avoid
DO NOT use raw ReportLab canvas with standard Helvetica text and table dumps (`generate_mayank_uber_pdfs.py`). Such PDFs lack maps, lack brand typography, lack icons, and get flagged during corporate reimbursement audits.

## Required Layout & Styling

### Page 1: Official Fare & Payment Summary
1. **Header**:
   - Left: Wordmark "Uber" (31px bold, tracking -0.04em)
   - Right: Date (e.g. `Aug 10, 2026`) and trip start time (e.g. `11:04 AM`)
2. **Greeting**:
   - `Thanks for riding, [Rider First Name]` (e.g. `Thanks for riding, Mayank`)
   - Subtitle: `We hope you enjoyed your ride this morning.` (or `this evening.` based on time of day)
3. **Total & Fare Breakdown**:
   - Label: `Total` (24px bold)
   - Value: `₹[Amount]` (e.g. `₹432.00` with official Rupee symbol `₹`, NOT `INR`)
   - `Suggested fare`: `₹[Amount]`
4. **Payments Section**:
   - Payment method: `Cash` with the official borderless Cash banknote icon, or `Uber Cash` / `Card`
   - Timestamp of completion
5. **Regulatory Disclaimer**:
   - *"This receipt reflects the Suggested Fare (excluding GST) and is not a tax invoice, but can be used for official reimbursement purposes. No GST is being recovered by Uber from the riders on this Trip."*
   - *"Uber does not provide transportation services; Issued on behalf of [Driver Full Name]"*
6. **Trip Details Overview**:
   - Service tier: `Uber Go` (or `Go Non AC` / `Uber Premier`)
   - Distance and Duration: e.g. `16.8 kilometers, 38 minutes`
   - Vehicle details & License plate: e.g. `UP32LN4821` (Lucknow) or `MH12QW8923` (Pune)
   - Official car icon (SVG/PNG)

### Page 2: Route Map & Trip Timeline
1. **Two-Column Side-by-Side Top Grid**:
   - **Left Column: Trip Timeline**:
     - Pickup: Solid black square (8×8px), Pickup time, Complete pickup address
     - Vertical black connecting line (2px width)
     - Dropoff: Hollow black circle (9×9px, 2.5px border), Dropoff time, Complete dropoff address
   - **Right Column: Official Route Map**:
     - Container: 624×716 aspect ratio (min-height 175px, max-height 215px, rounded 12px)
     - Content: High-contrast street map tile with the highlighted route connecting pickup to dropoff.
2. **Driver Information Row**:
   - Circular avatar placeholder
   - Driver greeting: `You rode with [Driver First Name]`
   - Driver rating badge: e.g. `4.85 ★`
3. **Footer**:
   - Link: `Want to review your trip history?`
   - Action: `My trips`

## Template Implementation
The pixel-perfect HTML/CSS implementation is available in `src/utils/official_uber_2_page_receipt_generator.html`.
When generating PDFs, render this HTML template with high-DPI headless Chromium/playwright or wkhtmltopdf to achieve 100% fidelity.
