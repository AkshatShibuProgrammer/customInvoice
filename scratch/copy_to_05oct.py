import os

with open('portal-reimbursement.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make links relative for inside 05_Oct
adjusted = content.replace('href="05_Oct/Akshat/', 'href="Akshat/')
adjusted = adjusted.replace('href="05_Oct/Mayank/', 'href="Mayank/')
adjusted = adjusted.replace('href="05_Oct/Akshat/"', 'href="Akshat/"')
adjusted = adjusted.replace('href="05_Oct/Mayank/"', 'href="Mayank/"')

# Write inside 05_Oct
with open('05_Oct/index.html', 'w', encoding='utf-8') as f:
    f.write(adjusted)

with open('05_Oct/reimbursement_consolidated.html', 'w', encoding='utf-8') as f:
    f.write(adjusted)

print("Created 05_Oct/index.html and 05_Oct/reimbursement_consolidated.html successfully!")
