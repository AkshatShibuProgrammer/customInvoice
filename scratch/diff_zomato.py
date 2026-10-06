import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

def compare_docs(path1, path2):
    doc1 = fitz.open(path1)
    doc2 = fitz.open(path2)
    
    print(f"Doc1 ({path1}): {len(doc1)} pages")
    print(f"Doc2 ({path2}): {len(doc2)} pages")
    
    for i in range(min(len(doc1), len(doc2))):
        p1 = doc1[i]
        p2 = doc2[i]
        t1 = p1.get_text()
        t2 = p2.get_text()
        print(f"\n--- Page {i+1} ---")
        print(f"Text length: Doc1={len(t1)}, Doc2={len(t2)}")
        if t1 != t2:
            print("DIFF IN TEXT!")
            lines1 = t1.splitlines()
            lines2 = t2.splitlines()
            import difflib
            diff = list(difflib.unified_diff(lines1[:40], lines2[:40], lineterm=''))
            for d in diff[:30]:
                print("  ", d)
        else:
            print("TEXT IS IDENTICAL.")

compare_docs('scratch/mayank_orig.pdf', 'Mayank_Sikarwar/01_11Aug_Pune_Zomato_GharSe_Lunch_Mayank_388.pdf')
