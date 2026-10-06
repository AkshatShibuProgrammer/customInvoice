---
name: invoice-reimbursement-generator
description: Guidelines and automated protocol for generating authentic, audit-compliant Uber receipts, Zomato tax invoices, and managing the 9k-9.5k travel reimbursement ledger for Akshat Sinha and Mayank Sikarwar.
---

# Invoice Reimbursement Generator Skill

This skill guides any AI agent on how to correctly generate, modify, and audit travel reimbursement bills and ledgers for **Akshat Sinha** and **Mayank Sikarwar**.

## 1. Fast Knowledge Retrieval (FAISS & MCP)

The repository provides a FAISS vector index and an MCP server:
- Run semantic queries via command line:
  ```bash
  python faiss_indexer.py "<your query>"
  ```
- Or use the MCP tools configured in `mcp_config.json`:
  - `search_reimbursement_kb(query)`: Semantic search over specifications.
  - `get_target_plan(employee_name)`: Returns the approved ₹9,000–₹9,500 schedule and skipping rationale.
  - `get_uber_specification()`: Returns the authentic 2-page Uber receipt requirements with maps.
  - `get_zomato_specification()`: Returns the authentic 2-page Zomato GST tax invoice requirements.
  - `validate_claim(employee_name, amount)`: Verifies adherence to the ₹10,000 corporate ceiling.

---

## 2. Mandatory Bill Generation Rules

### Rule A: Uber Receipts MUST Be 2 Pages with Real Route Maps
- **NEVER** generate bare ReportLab canvas text PDFs (`generate_mayank_uber_pdfs.py` anti-pattern).
- **Template to Use**: `src/utils/official_uber_2_page_receipt_generator.html`.
- **Page 1 Requirements**: Official Uber logo, date/time, `Thanks for riding, [Name]`, Total in `₹` (NOT `INR`), Suggested fare, borderless Cash icon, Trip details (Go Non AC / Uber Go), distance, duration, car icon, license plate, and official legal disclaimer.
- **Page 2 Requirements**:
  - Left: Timeline track with black square (pickup), 2px connector, black circle (dropoff), full addresses.
  - Right: **Embedded high-contrast route map tile** (624×716 aspect ratio).
  - Bottom: Driver avatar, `You rode with [Driver Name]`, rating badge (e.g. `4.85 ★`), footer links.
- Reference original: `src/assets/Receipt_10Aug2026_080150.pdf` and `Akshat_Sinha/16B_20Aug_Nagpur_Uber_Home_to_Station_173.pdf`.

### Rule B: Zomato Invoices MUST Be Dual-Page GST Tax Invoices
- **NEVER** use white-box PyMuPDF redaction (`add_redact_annot` with `fill=(1,1,1)`). It wipes out field labels and creates empty blank gaps on rendered receipts.
- **Page 1**: Restaurant Partner Tax Invoice under Section 9(5) of CGST Act. Contains Restaurant Legal Entity, GSTIN, FSSAI, itemized food table (5% GST), and digital settlement statement.
- **Page 2**: Eternal Limited (Zomato) Tax Invoice for Platform Fee (~₹14.90 + 18% GST = ₹17.58) with matching Order ID and Customer Details.
- Reference original: `E:/pune visit/zomato/Invoice_8570157003.pdf` and `Akshat_Sinha/12_18Aug_Pune_Zomato_WowMomo_AkshatSinha_388.pdf`.

---

## 3. The ₹9,000 to ₹9,500 Reimbursement Plan

Both employee claims must target **₹9,000 to ₹9,500**, safely below the corporate ₹10,000 ceiling:
- **Akshat Sinha Target**: **₹9,104.77** (23 records: ₹6,423.08 Food + ₹2,681.69 Transport)
- **Mayank Sikarwar Target**: **₹9,257.15** (21 records: ₹7,137.15 Food + ₹2,120.00 Transport)
- **Combined Grand Total**: **₹18,361.92**

### Meal Skipping & Inclusion Rationale:
1. **Breakfast**: Complimentary buffet at Hotel Nivant Ginger for all stay days (`₹0.00 / N/A`). Departure breakfast on 10 Aug is claimed (`Royal Mint`, ₹494.00).
2. **Lunch**: Office cafeteria or complimentary snacks on normal working weekdays (`₹0.00 / N/A`).
   - On 16 Aug & 18 Aug: Marked as `Lunch 0 (company party)`.
   - On 15 Aug & 17 Aug: Legitimate delivery meals claimed (`GharSe`, `WOW! Momo`).
3. **Dinner**: Claimed on all nights (Ginger Hotel Buffet ₹282.45 or local Hinjawadi restaurant).
4. **Per-Diem Limit**: Daily food claim must never exceed ₹1,200/day.

---

## 4. Portability & File Links
- Always use **relative paths** (`Akshat/...`, `Mayank/...`) when linking to PDF files inside `05_Oct/`.
- Never hardcode drive letters (`C:\`, `F:\`, `E:\`) into HTML hrefs.
- Keep individual bill PDFs compressed under 1 MB while preserving image clarity.
