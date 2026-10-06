import os
import fitz

files = [
    '05_Oct/Akshat/06_12Aug_Pune_GingerHotel_BuffetDinner_282.pdf',
    '05_Oct/Akshat/07_13Aug_Pune_GingerHotel_BuffetDinner_2Covers_565.pdf',
    '05_Oct/Akshat/08_14Aug_Pune_GingerHotel_BuffetDinner_282.pdf',
    '05_Oct/Akshat/09_16Aug_Pune_PizzaHut_Hinjewadi_AkshatSinha_419.pdf',
    '05_Oct/Akshat/10_16Aug_Pune_GingerHotel_BuffetDinner_282.pdf',
    '05_Oct/Akshat/11_17Aug_Pune_GingerHotel_BuffetDinner_282.pdf',
    '05_Oct/Mayank/11_16Aug_Pune_PizzaHut_Hinjewadi_Lunch_Mayank_419.pdf'
]

for p in files:
    doc = fitz.open(p)
    print(os.path.basename(p), f"{os.path.getsize(p)/1024:.1f} KB", "pages:", len(doc))
    for page in doc:
        imgs = page.get_images()
        print("  images count:", len(imgs))
        for img in imgs:
            bimg = doc.extract_image(img[0])
            print("    ", bimg["ext"], f"{len(bimg['image'])/1024:.1f} KB", bimg["width"], "x", bimg["height"])
