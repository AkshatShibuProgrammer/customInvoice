import os
import sys
import fitz
import re

sys.stdout.reconfigure(encoding='utf-8')

def audit_file(emp, fname, fpath):
    issues = []
    doc = fitz.open(fpath)
    page_count = len(doc)
    file_size_kb = os.path.getsize(fpath) / 1024
    
    all_text = ""
    total_imgs = 0
    for i, p in enumerate(doc):
        t = p.get_text()
        all_text += f"\n--- Page {i+1} ---\n" + t
        imgs = p.get_images()
        total_imgs += len(imgs)

    # 1. Check Uber
    if 'uber' in fname.lower():
        if page_count < 2:
            issues.append(f"Uber receipt is only {page_count} page(s) (Must be 2 pages)")
        # Check map on page 2
        if page_count >= 2:
            p2_imgs = len(doc[1].get_images())
            if p2_imgs == 0:
                issues.append("Page 2 has ZERO images (Route map is missing!)")
            p2_txt = doc[1].get_text()
            if "G PICKUP" in p2_txt or "I DROPOFF" in p2_txt:
                issues.append("Contains ReportLab canvas plain text markers ('G PICKUP' / 'I DROPOFF') instead of official Uber timeline track")
        if "INR" in all_text and "₹" not in all_text:
            issues.append("Uses plain 'INR' instead of authentic '₹' currency symbol")
        if total_imgs == 0:
            issues.append("Has zero visual assets (no Uber logo, no car icon, no cash banknote icon)")

    # 2. Check Zomato
    elif 'zomato' in fname.lower():
        if page_count < 2:
            issues.append(f"Zomato receipt is only {page_count} page(s) (Must be dual-page GST tax invoice)")
        # Check for wiped-out fields from bad redactions
        p1_txt = doc[0].get_text()
        # Look for "Invoice No.:" without number or broken labels
        if re.search(r'Invoice No\.:\s*\n\s*Invoice Date', p1_txt):
            issues.append("Invoice No value is BLANK/WIPED (redaction rectangle overlapped text)")
        if re.search(r'Invoice Date\s*\n\s*Customer Name:', p1_txt):
            issues.append("Invoice Date value is BLANK/WIPED")
        if re.search(r'Customer Name:\s*\n\s*Delivery Address', p1_txt):
            issues.append("Customer Name value is BLANK/WIPED")
        if re.search(r'Delivery Address\s*\n\s*State name', p1_txt):
            issues.append("Delivery Address value is BLANK/WIPED")
        if page_count >= 2:
            p2_txt = doc[1].get_text()
            if "Email ID: or" in p2_txt:
                issues.append("Page 2 email is truncated to 'Email ID: or' due to redaction clipping")
            if re.search(r'Invoice No:\s*\n\s*PAN:', p2_txt):
                issues.append("Page 2 Zomato Invoice No is BLANK/WIPED")
            if re.search(r'Invoice Date:\s*\n\s*Customer Details', p2_txt):
                issues.append("Page 2 Invoice Date is BLANK/WIPED")
            if "Deliver\n" in p2_txt or "Deliver \n" in p2_txt:
                issues.append("Page 2 address label is clipped to 'Deliver'")

    # 3. Check Ola
    elif 'ola' in fname.lower():
        # Check if authentic Ola invoice
        if "CRN" not in all_text and "ANI Technologies" not in all_text:
            issues.append("Missing Ola CRN or ANI Technologies corporate tax details")

    # 4. Check Ginger Hotel / Nivant Scans
    elif 'gingerhotel' in fname.lower() or 'hotel' in fname.lower() or 'nivant' in fname.lower():
        # Check if scan image is present
        if total_imgs == 0:
            issues.append("Thermal POS scan image is missing!")
        if "Roots Corp" not in all_text and "Ginger" not in all_text and "POS" not in all_text:
            # If purely an image scan without OCR
            pass

    # 5. Check Pizza Hut
    elif 'pizzahut' in fname.lower():
        # Check invoice number, dates
        if "Pizza Hut" not in all_text and "Devyani" not in all_text:
            issues.append("Missing Pizza Hut / Devyani International identifier")

    # 6. Check Royal Mint
    elif 'royalmint' in fname.lower():
        if "Royal Mint" not in all_text:
            issues.append("Missing Royal Mint vendor details")
        if "27AKMPG5967E2ZT" not in all_text and "GST" not in all_text:
            issues.append("Missing GSTIN identifier")

    return {
        'employee': emp,
        'filename': fname,
        'size_kb': file_size_kb,
        'pages': page_count,
        'images': total_imgs,
        'issues': issues
    }

print("==================== COMPREHENSIVE AUDIT OF ALL BILLS ====================")

results = []
for emp in ['Akshat', 'Mayank']:
    p = os.path.join('05_Oct', emp)
    for f in sorted(os.listdir(p)):
        if f.endswith('.pdf') and not f.endswith('_Merged.pdf'):
            fp = os.path.join(p, f)
            res = audit_file(emp, f, fp)
            results.append(res)

issue_count = 0
for r in results:
    if r['issues']:
        issue_count += len(r['issues'])
        print(f"\n[FAIL] {r['employee']} -> {r['filename']} ({r['size_kb']:.1f} KB, {r['pages']} pages, {r['images']} imgs)")
        for iss in r['issues']:
            print(f"   ❌ {iss}")
    else:
        print(f"[PASS] {r['employee']} -> {r['filename']} ({r['size_kb']:.1f} KB, {r['pages']} pages, {r['images']} imgs)")

print(f"\nTotal bills audited: {len(results)}")
print(f"Total defects found across all bills: {issue_count}")
