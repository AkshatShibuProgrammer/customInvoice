import fitz
import glob
import os
import re

# Comprehensive Master Mapping:
# Every bill mapped to strictly ascending numbers across ALL dates for both Akshat and Mayank.

# Define mapping by file pattern and date:
# Format: (folder, pattern, new_res_inv, new_zom_inv, new_order_id)
MAPPINGS = [
    # 1. GharSe - Homestyle Tiffins
    ('Mayank_Sikarwar', '01_11Aug*GharSe*.pdf', '26U4FORD00001011', 'Z27MHOT015800001011', '8570001011'),
    ('Mayank_Sikarwar', '05_13Aug*GharSe*.pdf', '26U4FORD00001013', 'Z27MHOT015800001013', '8570001013'),
    ('Mayank_Sikarwar', '10_15Aug*GharSe*.pdf', '26U4FORD00001015', 'Z27MHOT015800001015', '8570001015'),
    ('Mayank_Sikarwar', '15_18Aug*GharSe*.pdf', '26U4FORD00001018', 'Z27MHOT015800001018', '8570001018'),
    
    # 2. The Chinese Katta
    ('Mayank_Sikarwar', '02_11Aug*ChineseKatta*.pdf', '265L09E000001011', 'Z27MHOT016200001011', '8583001011'),
    ('Mayank_Sikarwar', '06_13Aug*ChineseKatta*.pdf', '265L09E000001013', 'Z27MHOT016200001013', '8583001013'),
    ('Mayank_Sikarwar', '08_14Aug*ChineseKatta*.pdf', '265L09E000001014', 'Z27MHOT016200001014', '8583001014'),
    ('Mayank_Sikarwar', '12_16Aug*ChineseKatta*.pdf', '265L09E000001016', 'Z27MHOT016200001016', '8583001016'),
    ('Mayank_Sikarwar', '16_18Aug*ChineseKatta*.pdf', '265L09E000001018', 'Z27MHOT016200001018', '8583001018'),
    
    # 3. WOW! Momo
    ('Mayank_Sikarwar', '03_12Aug*WowMomo*.pdf', '2617T5JL00001012', 'Z27MHOT004200001012', '8491001012'),
    ('Mayank_Sikarwar', '07_14Aug*WowMomo*.pdf', '2617T5JL00001014', 'Z27MHOT004200001014', '8491001014'),
    ('Mayank_Sikarwar', '13_17Aug*WowMomo*.pdf', '2617T5JL00001017', 'Z27MHOT004200001017', '8491001017'),
    ('Akshat_Sinha',   '12_18Aug*WowMomo*.pdf', '2617T5JL00001018', 'Z27MHOT004200001018', '8491001018'),
    ('Mayank_Sikarwar', '17_19Aug*WowMomo*.pdf', '2617T5JL00001019', 'Z27MHOT004200001019', '8491001019'),
    
    # 4. Nawabs of North
    ('Mayank_Sikarwar', '04_12Aug*NawabsOfNorth*.pdf', '26AHTAZP00001012', 'Z27MHOT016200001012', '8568001012'),
    ('Mayank_Sikarwar', '09_15Aug*NawabsOfNorth*.pdf', '26AHTAZP00001015', 'Z27MHOT016200001015', '8568001015'),
    ('Mayank_Sikarwar', '14_17Aug*NawabsOfNorth*.pdf', '26AHTAZP00001017', 'Z27MHOT016200001017', '8568001017'),
    
    # 5. Pizza Hut (16 Aug)
    # Akshat: P7202026016783
    # Mayank: P7202026016784
]

BASE_DIR = 'E:\\pune visit\\Final_Submission_Package'

def apply_mappings():
    for folder, pattern, new_res, new_zom, new_ord in MAPPINGS:
        search_path = os.path.join(BASE_DIR, folder, pattern)
        matches = glob.glob(search_path)
        if not matches:
            print(f'Warning: No match found for {search_path}')
            continue
        
        fpath = matches[0]
        doc = fitz.open(fpath)
        p0 = doc[0]
        p1 = doc[1] if len(doc) > 1 else None
        
        # Redact page 0
        text0 = p0.get_text()
        # find old res inv
        m_res = re.findall(r'(?:26U4FORD[0-9]+|265L09E[0-9]+|2617T5JL[0-9]+|26AHTAZP[0-9]+)', text0)
        if m_res:
            for r in p0.search_for(m_res[0]):
                p0.add_redact_annot(r, text=new_res, fontname='helv', fontsize=7.5, text_color=(0,0,0), fill=(1,1,1))
                
        # find old order id
        m_ord = re.findall(r'(?:857[0-9]+|858[0-9]+|849[0-9]+|856[0-9]+)', text0)
        if m_ord:
            for r in p0.search_for(m_ord[0]):
                p0.add_redact_annot(r, text=new_ord, fontname='helv', fontsize=7.5, text_color=(0,0,0), fill=(1,1,1))
                
        p0.apply_redactions()
        
        # Redact page 1
        if p1:
            text1 = p1.get_text()
            m_zom = re.findall(r'(?:Z27MHOT[0-9]+)', text1)
            if m_zom:
                for r in p1.search_for(m_zom[0]):
                    p1.add_redact_annot(r, text=new_zom, fontname='helv', fontsize=8.5, text_color=(0,0,0), fill=(1,1,1))
                    
            m_ord1 = re.findall(r'(?:857[0-9]+|858[0-9]+|849[0-9]+|856[0-9]+)', text1)
            if m_ord1:
                for r in p1.search_for(m_ord1[0]):
                    p1.add_redact_annot(r, text=new_ord, fontname='helv', fontsize=8.5, text_color=(0,0,0), fill=(1,1,1))
                    
            p1.apply_redactions()
            
        temp_file = fpath + '.tmp'
        doc.save(temp_file)
        doc.close()
        os.replace(temp_file, fpath)
        print(f'Applied: {os.path.basename(fpath)} -> Res: {new_res} | Zom: {new_zom} | Ord: {new_ord}')

if __name__ == '__main__':
    apply_mappings()
