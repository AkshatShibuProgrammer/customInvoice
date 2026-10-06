with open('src/utils/official_uber_2_page_receipt_generator.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'u-map-container', text)]
print("Found matches:", len(matches))
for idx in matches[:3]:
    print("--------------------")
    print(text[max(0, idx-50):min(len(text), idx+350)])
