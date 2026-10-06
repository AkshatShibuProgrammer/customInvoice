import subprocess
import os

res = subprocess.run(
    ['git', 'show', 'e715020:Mayank_Sikarwar/01_11Aug_Pune_Zomato_GharSe_Lunch_Mayank_388.pdf'],
    capture_output=True
)

with open('scratch/mayank_orig.pdf', 'wb') as f:
    f.write(res.stdout)

print("Saved scratch/mayank_orig.pdf size:", os.path.getsize('scratch/mayank_orig.pdf'))
