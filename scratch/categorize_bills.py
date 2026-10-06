import os
import sys
import fitz
import re

sys.stdout.reconfigure(encoding='utf-8')

# Collect all PDFs from 05_Oct/Akshat and 05_Oct/Mayank
all_bills = []

for emp in ['Akshat', 'Mayank']:
    folder = os.path.join('05_Oct', emp)
    for fname in sorted(os.listdir(folder)):
        if fname.endswith('.pdf') and not fname.endswith('_Merged.pdf'):
            fpath = os.path.join(folder, fname)
            all_bills.append({
                'emp': emp,
                'fname': fname,
                'fpath': fpath
            })

def categorize(fname):
    fl = fname.lower()
    if 'zomato' in fl:
        return 'Zomato'
    elif 'uber' in fl:
        return 'Uber'
    elif 'pizzahut' in fl or 'pizza' in fl:
        return 'Pizza Hut (Non-Zomato Food)'
    elif 'royalmint' in fl or 'nagpur' in fl:
        return 'Nagpur Royal Mint (Non-Zomato Food)'
    elif 'gingerhotel' in fl or 'nivant' in fl or 'hotel' in fl:
        return 'Ginger Hotel / Nivant (Non-Zomato Food)'
    elif 'ola' in fl:
        return 'Ola (Non-Uber Transport)'
    else:
        return 'Other'

categorized = {}
for b in all_bills:
    cat = categorize(b['fname'])
    categorized.setdefault(cat, []).append(b)

print(f"Total individual bills collected: {len(all_bills)}")
for cat, bills in categorized.items():
    print(f"  {cat}: {len(bills)} bills")
