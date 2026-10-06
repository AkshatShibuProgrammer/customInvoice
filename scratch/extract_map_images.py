import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

os.makedirs('scratch/extracted_assets', exist_ok=True)

for path in ['src/assets/Receipt_10Aug2026_080150.pdf', 'src/assets/Receipt_20Aug2026_191922 (1).pdf']:
    name = os.path.basename(path).replace('.pdf', '')
    doc = fitz.open(path)
    print(f"\nExtracting from {name}:")
    for i, page in enumerate(doc):
        for j, img in enumerate(page.get_images()):
            xref = img[0]
            bimg = doc.extract_image(xref)
            ext = bimg['ext']
            out_name = f"scratch/extracted_assets/{name}_p{i+1}_img{j+1}_{bimg['width']}x{bimg['height']}.{ext}"
            with open(out_name, 'wb') as f:
                f.write(bimg['image'])
            print(f"  Saved {out_name} ({bimg['width']}x{bimg['height']}, {len(bimg['image'])/1024:.1f} KB)")
