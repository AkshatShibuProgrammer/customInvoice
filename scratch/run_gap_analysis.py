import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

def analyze_pdf(path, label):
    print(f"\n=======================================================")
    print(f"[{label}] {path}")
    print(f"=======================================================")
    doc = fitz.open(path)
    print(f"Pages: {len(doc)}")
    for i, page in enumerate(doc):
        print(f"\n--- Page {i+1} (Size: {page.rect.width:.1f} x {page.rect.height:.1f} pt) ---")
        imgs = page.get_images()
        print(f"Images count: {len(imgs)}")
        for j, img in enumerate(imgs):
            bimg = doc.extract_image(img[0])
            print(f"  Img {j+1}: {bimg['ext']} | {bimg['width']}x{bimg['height']} | {len(bimg['image'])/1024:.1f} KB")
        
        # Fonts
        font_list = page.get_fonts()
        print(f"Fonts ({len(font_list)}): {', '.join([f[3] for f in font_list[:5]])}")
        
        # Text sample
        txt = page.get_text()
        print(f"Text ({len(txt)} chars), sample:\n" + "-"*40)
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        for l in lines[:15]:
            print("  ", l)
        print("-"*40)

# Uber Analysis
analyze_pdf("src/assets/Receipt_10Aug2026_080150.pdf", "ORIGINAL UBER INVOICE (from src/assets)")
analyze_pdf("05_Oct/Mayank/01_10Aug_Lucknow_Uber_Home_to_Airport_432.pdf", "CURRENT GENERATED MAYANK UBER INVOICE")

# Zomato Analysis
analyze_pdf("E:/pune visit/zomato/Invoice_8570157003.pdf", "ORIGINAL ZOMATO INVOICE (from E:/pune visit/zomato)")
analyze_pdf("05_Oct/Mayank/01_11Aug_Pune_Zomato_GharSe_Lunch_Mayank_388.pdf", "CURRENT MAYANK ZOMATO INVOICE")
