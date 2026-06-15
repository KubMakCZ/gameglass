import os
import glob

os.chdir(r'C:\gitprojekty_skola\python_gamejam_examples\pygame')
for f in glob.glob('*.py'):
    if f.startswith('patch'): continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('async def hlavni_smycka():', 'async def hlavni_smycka():')
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
