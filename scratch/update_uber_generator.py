import re, json

with open(r'F:\Code by Akshat\testgemini\customizable-invoice-generator-webpage (2)\scratch\uber_icons.json', 'r') as f:
    icons = json.load(f)

cash_img = icons['cash']
car_img = icons['car']

html_path = r'F:\Code by Akshat\testgemini\customizable-invoice-generator-webpage (2)\src\utils\official_uber_2_page_receipt_generator.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace car image
content = re.sub(
    r'<img src="https://i\.ibb\.co/[^"]+" alt="Uber Car" class="u-car-icon"[^>]*>',
    f'<img src="{car_img}" alt="Uber Car" class="u-car-icon" />',
    content
)

# Replace svg cash
content = re.sub(
    r'<svg class="u-cash-svg"[^>]*>.*?</svg>',
    f'<img src="{cash_img}" class="u-cash-svg" alt="Cash" />',
    content,
    flags=re.DOTALL
)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated official_uber_2_page_receipt_generator.html successfully!')
