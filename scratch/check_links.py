import re

for filename in ['05_Oct/index.html', '05_Oct/reimbursement_consolidated.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    links = set(re.findall(r'href=["\'](.*?)["\']', content))
    print(f"=== Links in {filename} ===")
    for l in sorted(links):
        if 'Akshat' in l or 'Mayank' in l:
            print(" ", l)
