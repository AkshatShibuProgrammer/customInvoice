# Reimbursement Guidelines & AI Operating Rules

## 1. Quality Standards for Bills
- **Uber Receipts**: Always 2 pages, containing the Page 2 route map tile, pickup/dropoff timeline with nodes, official typography, and vehicle/payment icons. Never generate text-only ReportLab PDFs. Reference: `src/utils/official_uber_2_page_receipt_generator.html` and `src/assets/Receipt_10Aug2026_080150.pdf`.
- **Zomato Invoices**: Always dual-page GST format (Page 1 restaurant tax invoice, Page 2 Zomato platform fee). Retain FSSAI and signatory logos. Never apply white-box redactions over text. Reference: `E:/pune visit/zomato/` and `Akshat_Sinha/12_18Aug_Pune_Zomato_WowMomo_AkshatSinha_388.pdf`.

## 2. Target Plan & Policy Rationale
- Target claim total per employee: **₹9,000 to ₹9,500** (Akshat: ₹9,104.77, Mayank: ₹9,257.15).
- Corporate ceiling: ₹10,000.00 maximum per person.
- Daily food limit: ≤ ₹1,200/day.
- Meal skipping rationale: Hotel breakfast is complimentary (₹0); weekday office lunches are cafeteria/tea (₹0); party days (16 Aug, 18 Aug) have lunch covered by company party (₹0).

## 3. FAISS & MCP Tools
- Query the FAISS knowledge base using `python faiss_indexer.py "<query>"`
- Or use the MCP tools defined in `mcp_server.py` (`search_reimbursement_kb`, `get_target_plan`, `get_uber_specification`, `get_zomato_specification`, `validate_claim`).
