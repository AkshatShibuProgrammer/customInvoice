import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("==================== DETAILED AUDIT OF MAYANK ZOMATO BILLS ====================")
zomato_files = [f for f in sorted(os.listdir('05_Oct/Mayank')) if 'zomato' in f.lower()]

for fname in zomato_files:
    fpath = os.path.join('05_Oct/Mayank', fname)
    doc = fitz.open(fpath)
    p0_txt = doc[0].get_text()
    p1_txt = doc[1].get_text() if len(doc) > 1 else ""
    
    # Extract invoice number lines
    inv_lines = [l.strip() for l in p0_txt.splitlines() if 'invoice' in l.lower() or 'customer' in l.lower() or 'delivery' in l.lower()]
    
    print(f"\nFile: {fname}")
    print("Page 1 Metadata Lines:")
    for l in inv_lines[:6]:
        print("  ", l)
    
    # Check page 2
    if p1_txt:
        p2_lines = [l.strip() for l in p1_txt.splitlines() if 'invoice' in l.lower() or 'email' in l.lower() or 'deliver' in l.lower()]
        print("Page 2 Zomato Lines:")
        for l in p2_lines[:6]:
            print("  ", l)
