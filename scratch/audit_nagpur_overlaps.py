import os
import sys
import fitz

sys.stdout.reconfigure(encoding='utf-8')

print("==================== AUDITING NAGPUR ROYAL MINT BILLS FOR OVERLAPS ====================")
nagpur_files = [
    ('Akshat', '05_10Aug_Nagpur_RoyalMint_Breakfast_494.pdf'),
    ('Akshat', '13_19Aug_Nagpur_RoyalMint_Lunch_499.pdf'),
    ('Akshat', '14_19Aug_Nagpur_RoyalMint_Dinner_693.pdf'),
    ('Akshat', '15_20Aug_Nagpur_RoyalMint_Lunch_719.pdf'),
    ('Akshat', '16_20Aug_Nagpur_RoyalMint_Dinner_478.pdf')
]

for emp, fname in nagpur_files:
    fpath = os.path.join('05_Oct', emp, fname)
    doc = fitz.open(fpath)
    print(f"\n--- {fname} (Size: {os.path.getsize(fpath)/1024:.1f} KB, Pages: {len(doc)}) ---")
    for i, p in enumerate(doc):
        txt = p.get_text()
        print(f"Page {i+1} Text:")
        print(txt.strip() if txt.strip() else "[NO EXTRACTABLE TEXT - PURE SCAN/IMAGE]")
        
        # Check text words and their bounding boxes for text collisions
        words = p.get_text("words")
        print(f"Words extracted: {len(words)}")
        if len(words) > 0:
            # Check if any words have overlapping bounding boxes
            # Format: (x0, y0, x1, y1, word, block_no, line_no, word_no)
            overlapped = []
            for w1 in words:
                for w2 in words:
                    if w1 != w2:
                        # Check bounding box intersection
                        r1 = fitz.Rect(w1[:4])
                        r2 = fitz.Rect(w2[:4])
                        intersect = r1.intersect(r2)
                        if not intersect.is_empty and intersect.width > 3 and intersect.height > 3:
                            overlapped.append((w1[4], w2[4], intersect))
            if overlapped:
                print(f"  ⚠️ DETECTED {len(overlapped)} OVERLAPPING TEXT BOXES:")
                for o in overlapped[:10]:
                    print(f"     '{o[0]}' overlaps with '{o[1]}' at rect {o[2]}")
            else:
                print("  ✓ No overlapping text bounding boxes found in PDF stream.")
