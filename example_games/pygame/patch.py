import os
import glob
import re

os.chdir(r'C:\gitprojekty_skola\python_gamejam_examples\pygame')
for f in glob.glob('*.py'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()

    # 1. async def
    content = re.sub(r'(\s*)def hlavni_smycka\(\):', r'\1async def hlavni_smycka():', content)

    # 2. Add await to hlavni_smycka() calls
    content = re.sub(r'(\s+)hlavni_smycka\(\)', r'\1await hlavni_smycka()', content)

    # 3. Fix asyncio.sleep(0)
    # Odstranime stary await asyncio.sleep(0) a jeho komentar
    content = re.sub(r'[ \t]*# PØIDÁNO PRO WEB: Dáme prohlížeèi šanci pøekreslit obrazovku\s+await asyncio\.sleep\(0\)\s*', '\n', content)
    
    # Pridame ho tesne za hodiny.tick(...) se stejnym odsazenim
    content = re.sub(r'([ \t]*)(.*hodiny\.tick.*)', r'\1\2\n\1# PØIDÁNO PRO WEB: Dáme prohlížeèi šanci pøekreslit obrazovku\n\1await asyncio.sleep(0)', content)

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f'Opraveno: {f}')
