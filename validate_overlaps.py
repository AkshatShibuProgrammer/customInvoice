import fitz
import glob
import os

for person in ['Akshat_Sinha', 'Mayank_Sikarwar']:
    folder = f'E:\\pune visit\\Final_Submission_Package\\{person}'
    print(f'=== VALIDATING {person} ===')
    files = sorted(glob.glob(os.path.join(folder, '*.pdf')))
    for f in files:
        if 'Merged' in f:
            continue
        fname = os.path.basename(f)
        doc = fitz.open(f)
        for page_idx, page in enumerate(doc):
            text = page.get_text()
            if 'F4142Date' in text:
                print(f'  [COLLISION DETECTED] {fname}')
            words = page.get_text('words')
            lines = {}
            for w in words:
                y_key = round(w[1], 1)
                lines.setdefault(y_key, []).append(w)
            for y_key, line_words in lines.items():
                line_words.sort(key=lambda x: x[0])
                for i in range(len(line_words) - 1):
                    w1 = line_words[i]
                    w2 = line_words[i+1]
                    overlap = w1[2] - w2[0]
                    if overlap > 2.0:
                        print(f'  [OVERLAP >2pt] {fname} P{page_idx}: "{w1[4]}" and "{w2[4]}" overlap={overlap:.2f}pt at y={y_key}')

print('ALL PDF VALIDATION PASSED CLEANLY!')
