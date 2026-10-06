import os
import io
import fitz
from PIL import Image

def compress_pdf_file(input_path, output_path, max_dimension=1800, quality=75):
    doc = fitz.open(input_path)
    
    # Check if this PDF has embedded images (like the Ginger Hotel scans)
    has_large_image = False
    for page in doc:
        for img in page.get_images():
            bimg = doc.extract_image(img[0])
            if len(bimg["image"]) > 200 * 1024 or bimg["width"] > 1000 or bimg["height"] > 1000:
                has_large_image = True
                break

    if has_large_image:
        # Re-encode embedded image(s) with optimal resolution and JPEG compression
        for page in doc:
            for img_info in page.get_images():
                xref = img_info[0]
                bimg = doc.extract_image(xref)
                raw_bytes = bimg["image"]
                pil_img = Image.open(io.BytesIO(raw_bytes))
                
                # Resize if exceeding max_dimension while preserving aspect ratio
                w, h = pil_img.size
                scale = min(1.0, max_dimension / max(w, h))
                if scale < 1.0:
                    new_size = (int(w * scale), int(h * scale))
                    pil_img = pil_img.resize(new_size, Image.Resampling.LANCZOS)
                
                if pil_img.mode != 'RGB':
                    pil_img = pil_img.convert('RGB')
                
                out_buffer = io.BytesIO()
                pil_img.save(out_buffer, format='JPEG', quality=quality, optimize=True)
                compressed_bytes = out_buffer.getvalue()
                
                # Replace the image stream in PDF
                page.replace_image(xref, stream=compressed_bytes)

        doc.save(output_path, deflate=True, garbage=4, clean=True)
    else:
        # Vector / font-heavy PDF (like Pizza Hut) -> Render at crisp 150 DPI and save as compact PDF
        new_doc = fitz.open()
        for page in doc:
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("jpeg", jpg_quality=quality)
            new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_page.insert_image(page.rect, stream=img_bytes)
        new_doc.save(output_path, deflate=True, garbage=4)
        new_doc.close()

    doc.close()

# Test compression on all 7 target files
test_files = [
    '05_Oct/Akshat/06_12Aug_Pune_GingerHotel_BuffetDinner_282.pdf',
    '05_Oct/Akshat/07_13Aug_Pune_GingerHotel_BuffetDinner_2Covers_565.pdf',
    '05_Oct/Akshat/08_14Aug_Pune_GingerHotel_BuffetDinner_282.pdf',
    '05_Oct/Akshat/09_16Aug_Pune_PizzaHut_Hinjewadi_AkshatSinha_419.pdf',
    '05_Oct/Akshat/10_16Aug_Pune_GingerHotel_BuffetDinner_282.pdf',
    '05_Oct/Akshat/11_17Aug_Pune_GingerHotel_BuffetDinner_282.pdf',
    '05_Oct/Mayank/11_16Aug_Pune_PizzaHut_Hinjewadi_Lunch_Mayank_419.pdf'
]

os.makedirs('scratch/compressed_test', exist_ok=True)
for p in test_files:
    fname = os.path.basename(p)
    out_p = os.path.join('scratch/compressed_test', fname)
    compress_pdf_file(p, out_p)
    orig_kb = os.path.getsize(p) / 1024
    new_kb = os.path.getsize(out_p) / 1024
    print(f"{fname}:\n  {orig_kb:.1f} KB -> {new_kb:.1f} KB (reduced by {(1 - new_kb/orig_kb)*100:.1f}%)")
