import os
import io
import shutil
import fitz
from PIL import Image

def compress_pdf_file(input_path, output_path, max_dimension=1800, quality=75):
    doc = fitz.open(input_path)
    
    # Check if this PDF has embedded images
    has_large_image = False
    for page in doc:
        for img in page.get_images():
            bimg = doc.extract_image(img[0])
            if len(bimg["image"]) > 200 * 1024 or bimg["width"] > 1000 or bimg["height"] > 1000:
                has_large_image = True
                break

    if has_large_image:
        for page in doc:
            for img_info in page.get_images():
                xref = img_info[0]
                bimg = doc.extract_image(xref)
                raw_bytes = bimg["image"]
                pil_img = Image.open(io.BytesIO(raw_bytes))
                
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
                
                page.replace_image(xref, stream=compressed_bytes)

        temp_out = output_path + ".tmp"
        doc.save(temp_out, deflate=True, garbage=4, clean=True)
        doc.close()
        shutil.move(temp_out, output_path)
    else:
        new_doc = fitz.open()
        for page in doc:
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("jpeg", jpg_quality=quality)
            new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_page.insert_image(page.rect, stream=img_bytes)
        
        temp_out = output_path + ".tmp"
        new_doc.save(temp_out, deflate=True, garbage=4)
        new_doc.close()
        doc.close()
        shutil.move(temp_out, output_path)

def process_folder(folder_path):
    print(f"\n==================== PROCESSING {folder_path} ====================")
    for f in sorted(os.listdir(folder_path)):
        if f.endswith('.pdf') and not f.endswith('_Merged.pdf'):
            full_path = os.path.join(folder_path, f)
            sz_before = os.path.getsize(full_path)
            
            # If already well under 1 MB (< 300 KB), no need to recompress unless desired
            if sz_before > 300 * 1024:
                compress_pdf_file(full_path, full_path)
                sz_after = os.path.getsize(full_path)
                print(f"COMPRESSED: {f}\n  {sz_before/1024:.1f} KB -> {sz_after/1024:.1f} KB (saved {(1 - sz_after/sz_before)*100:.1f}%)")
            else:
                print(f"KEPT (already small): {f} ({sz_before/1024:.1f} KB)")

# Process both 05_Oct subdirectories
process_folder('05_Oct/Akshat')
process_folder('05_Oct/Mayank')

# Verify all individual files are strictly < 1 MB
print("\n==================== VERIFYING FINAL SIZES IN 05_Oct ====================")
all_under_1mb = True
for emp in ['Akshat', 'Mayank']:
    p = os.path.join('05_Oct', emp)
    print(f"\n--- 05_Oct/{emp} ---")
    for f in sorted(os.listdir(p)):
        if f.endswith('.pdf'):
            fp = os.path.join(p, f)
            sz = os.path.getsize(fp)
            is_merged = '_Merged' in f
            status = "PASS (<1MB)" if sz < 1024*1024 else ("EXEMPT (Consolidated Merged PDF)" if is_merged else "FAIL (>1MB)")
            if not is_merged and sz >= 1024*1024:
                all_under_1mb = False
            print(f"  {f:55s} : {sz/1024:7.1f} KB | {status}")

print(f"\nAll individual bill PDFs are < 1 MB: {all_under_1mb}")
