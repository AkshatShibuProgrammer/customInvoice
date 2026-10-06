import fitz
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def inspect_pdf(label, path):
    print(f"\n==================== {label} ====================")
    print("Path:", path)
    if not os.path.exists(path):
        print("FILE DOES NOT EXIST!")
        return
    print(f"File size: {os.path.getsize(path)/1024:.1f} KB")
    doc = fitz.open(path)
    print("Page count:", len(doc))
    for i, p in enumerate(doc):
        txt = p.get_text()
        imgs = p.get_images()
        print(f"\n--- Page {i+1} (dimensions: {p.rect.width} x {p.rect.height}) ---")
        print(f"Images count: {len(imgs)}")
        for img in imgs:
            bimg = doc.extract_image(img[0])
            print(f"  img: {bimg['ext']}, {bimg['width']}x{bimg['height']}, {len(bimg['image'])/1024:.1f} KB")
        print(f"Text length: {len(txt)} chars")
        lines = [line.strip() for line in txt.split('\n') if line.strip()]
        print("First 20 lines of text:")
        for line in lines[:20]:
            print("  ", line)

# Uber comparison
inspect_pdf("ORIGINAL UBER (src/assets)", "src/assets/Receipt_10Aug2026_080150.pdf")
inspect_pdf("ORIGINAL UBER AKSHAT (16B)", "Akshat_Sinha/16B_20Aug_Nagpur_Uber_Home_to_Station_173.pdf")
inspect_pdf("MAYANK UBER (generate_mayank_uber_pdfs)", "Mayank_Sikarwar/Travelling/01_10Aug_Lucknow_Uber_Home_to_Airport_432.pdf")

# Zomato comparison
inspect_pdf("ZOMATO AKSHAT 12_18Aug", "Akshat_Sinha/12_18Aug_Pune_Zomato_WowMomo_AkshatSinha_388.pdf")
inspect_pdf("ZOMATO MAYANK 01_11Aug", "Mayank_Sikarwar/01_11Aug_Pune_Zomato_GharSe_Lunch_Mayank_388.pdf")
