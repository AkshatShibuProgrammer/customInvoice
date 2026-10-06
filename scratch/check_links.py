import re
import os

for filename in ['06_Oct/index.html', '06_Oct/reimbursement_ledger.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    links = set(re.findall(r'href=["\'](.*?)["\']', content))
    print(f"=== Links in {filename} ===")
    missing = []
    checked = 0
    for l in sorted(links):
        if 'Akshat' in l or 'Mayank' in l:
            checked += 1
            full_p = os.path.join('06_Oct', l)
            if not os.path.exists(full_p):
                missing.append(l)
    print(f"  Checked {checked} PDF links. Missing: {len(missing)}")
    if missing:
        for m in missing:
            print("   -> Missing:", m)
    else:
        print("  100% SUCCESS: All links exist on disk!")

