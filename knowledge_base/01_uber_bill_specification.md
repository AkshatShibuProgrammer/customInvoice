# Specification: Authentic 2-Page Uber Receipt Generation

## Overview
Every Uber receipt submitted for corporate travel reimbursement must be a **2-page official receipt**, mirroring the genuine Uber electronic receipts stored in `src/assets/Receipt_10Aug2026_080150.pdf` and `Akshat_Sinha/16B_20Aug_Nagpur_Uber_Home_to_Station_173.pdf`.

## Dimensions & Canvas
- **Page Size**: Strictly US Letter (`612pt × 792pt`), NOT A4. Rendering on A4 squishes width and misplaces footer elements.
- **Margins**: Left `43.5pt`, Right `43.5pt` (usable width `525pt`), Top `27.5pt`.

## Exact Typography, Colors & Metrics

### Page 1: Official Fare & Payment Summary
1. **Header**:
   - Left: Wordmark "Uber" (`33pt` bold, font `UberMove-Bold`, color `#000000`, tracking `-0.04em`).
   - Right: Date (e.g. `Aug 10, 2026`) and Trip start time (e.g. `10:32 AM`) in `10.5pt`, font `UberMoveText-Regular`, color `#4b4b4b` (NOT black).
2. **Greeting**:
   - `Thanks for riding, [Rider First Name]` (`28pt` bold, font `UberMove-Bold`, color `#000000`).
   - Subtitle: `We hope you enjoyed your ride [this morning/afternoon/evening].` (`13.5pt`, font `UberMoveText-Regular`, color `#000000` - NOT gray).
3. **Total & Fare Breakdown**:
   - Divider line: `height: 1pt`, color `#F3F3F3`.
   - `Total`: `24pt` bold, font `UberMove-Bold`, color `#000000`. Amount: `24pt` bold, color `#000000`.
   - `Suggested fare`: `12pt`, font `UberMoveText-Medium`, color `#000000` (NOT gray). Amount: `12pt`, color `#000000`.
4. **Payments Section**:
   - Title: `Payments` (`18pt` bold, font `UberMove-Bold`, color `#000000`).
   - Cash Icon: Extracted genuine RGBA icon (`24pt × 24pt`) with 100% alpha transparency. **CRITICAL**: Never use raw RGB mode which renders an unwanted solid black rectangle!
   - Payment method: `Cash` (`12pt`, font `UberMoveText-Medium`, color `#000000`).
   - Timestamp: `8/10/26 11:04 AM` (`10.5pt`, font `UberMoveText-Regular`, color `#4b4b4b`, margin-left `36pt`).
5. **Regulatory Disclaimer**:
   - Font: `10.5pt`, font `UberMoveText-Regular`, color `#000000`, line-height `15pt`, max-width `495pt`.
   - Continuous 3-line block without artificial `<br><br>` double breaks:
     ```
     This receipt reflects the Suggested Fare (excluding GST) and is not a tax invoice, but can be used for official reimbursement purposes. No GST is being recovered by Uber from the riders on this Trip.
     Uber does not provide transportation services; Issued on behalf of [Driver Full Name]
     ```
6. **Trip Details Overview**:
   - Title: `Trip details` (`18pt` bold, color `#000000`).
   - Car Icon: Genuine RGBA image with 100% alpha transparency (`52pt × 52pt`). Never use raw RGB mode which renders a black square box outside the car.
   - Service tier: `Uber Go` (`12pt`, color `#000000`).
   - Distance & duration: `10.5pt`, font `UberMoveText-Regular`, color `#5e5e5e`.
   - License plate label: `License Plate:` (`12pt`, color `#000000`). Number: `10.5pt`, color `#5e5e5e`.

### Page 2: Route Map & Trip Timeline
1. **Side-by-Side Top Grid**:
   - **Left Column (Timeline)**:
     - Pickup Time: `12pt`, font `ArialMT`, normal weight (NOT bold), color `#000000`.
     - Pickup Address: `10.5pt`, font `UberMoveText-Regular`, color `#5e5e5e` (NOT `#000000`).
     - Dropoff Time: `12pt`, font `ArialMT`, normal weight (NOT bold), color `#000000`.
     - Dropoff Address: `10.5pt`, font `UberMoveText-Regular`, color `#5e5e5e` (NOT `#000000`).
     - Spacing: Stops sit naturally grouped in the upper half (`margin-bottom: 28pt`), NOT stretched apart to bottom.
     - Indicators:
       - Pickup: Clean hollow black circular ring (`11pt × 11pt`, inner transparent/white hole `4.5pt`, border `3.25pt` black). **CRITICAL**: Pure hollow ring, NO center black dot!
       - Connecting line: `1.5pt` solid black, attached directly to the bottom of the circle, running straight down towards the square.
       - Dropoff: Clean hollow black square (`10pt × 10pt`, inner transparent/white hole `3.5pt`, border `3.25pt` black). **CRITICAL**: Pure hollow square, NO center black dot!
   - **Right Column (Route Map)**:
     - Size: `262.5pt × 268.5pt`, rounded corners `12pt`.
     - Map tile: High-contrast street map with clean turn-by-turn route polyline.
2. **Driver Information Card**:
   - Container: `height: 40.5pt`, `width: 525pt`, border `1.5pt solid #F3F3F3`, border-radius `4px`.
   - Left text: `You rode with [Driver First Name]` (`12pt`, font `UberMoveText-Medium`, color `#000000`).
   - Right: Rating number e.g. `4.86` (`12pt`, font `UberMoveText-Medium`, color `#000000`).
   - Driver Star: **CRITICAL**: Pure 5-pointed star icon (`12pt × 12pt`) with transparent background. NEVER enclose in a square box or use an RGB image with black corners.
3. **Footer**:
   - Left: `Want to review your trip history?` (`12pt`, font `UberMoveText-Medium`, color `#000000`).
   - Right: `My trips` (`12pt`, font `UberMoveText-Medium`, color `#000000`, underline).

## Generation Pipeline
- HTML generator: `scratch/generate_all_authentic_uber_bills.py`.
- Rendered with Playwright Chromium directly to US Letter PDF with exact CSS page sizing.
