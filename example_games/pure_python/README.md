# Pure Python Hry v Terminálu 🐍🎮

Tato složka obsahuje ukázky jednoduchých her, které běží přímo v příkazovém řádku (terminálu) a k jejichž vytvoření není potřeba žádná externí knihovna typu Pygame. Jsou ideální pro seznámení se se základy programovací logiky (cykly, podmínky, slovníky, seznamy).

## Užitečné tipy a triky pro terminálové hry

Zde je několik zajímavých technik, které můžete ve svých hrách využít:

### 1. Čištění obrazovky
Pro iluzi animace nebo zobrazení nové "scény" je užitečné vymazat obsah terminálu, aby se starý text nehromadil nahoře.

```python
import os

def vycisti_obrazovku():
    # 'cls' funguje na Windows, 'clear' na Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')

# Příklad použití:
print("Stará scéna")
vycisti_obrazovku()
print("Nová scéna (to předchozí zmizelo)")
```

### 2. Pomalé vypisování textu (RPG efekt)
V adventurách vypadá skvěle, když se text nevypíše najednou v jedné milisekundě, ale znak po znaku (jako na psacím stroji). Hra má hned lepší atmosféru.

```python
import time
import sys

def vypis_pomalu(text, zpozdeni=0.05):
    for znak in text:
        print(znak, end='', flush=True) # flush=True je nutné, aby se znak ihned zobrazil
        time.sleep(zpozdeni) # Uspí program na zadaný počet sekund
    print() # Na konci odřádkujeme pro další text

vypis_pomalu("Probouzíš se v temném lese a nic si nepamatuješ...")
```

### 3. Barevný text v terminálu (ANSI escape kódy)
Do terminálu můžete psát barevně pomocí speciálních znakových sekvencí.
*(Poznámka: Ve starších Windows cmd to nemusí fungovat bez zapnutí podpory, ale v moderních terminálech to funguje spolehlivě.)*

```python
# Definice barev pomocí ANSI kódů
CERVENA = '\033[91m'
ZELENA = '\033[92m'
ZLUTA = '\033[93m'
MODRA = '\033[94m'
RESET = '\033[0m' # Resetuje barvu zpět na normální (VELMI DŮLEŽITÉ)

print(f"Tohle je normální text.")
print(f"{CERVENA}Pozor, nepřítel útočí!{RESET}")
print(f"{ZELENA}Úspěšně jsi otevřel truhlu a našel jsi {ZLUTA}zlato{ZELENA}.{RESET}")
```

### 4. Náhodnost
Bez náhody by hry byly předvídatelné a nudné. Modul `random` je váš nejlepší přítel!

```python
import random

# Hod kostkou (náhodné celé číslo od 1 do 6)
kostka = random.randint(1, 6)
print(f"Hodil jsi: {kostka}")

# Náhodný výběr položky ze seznamu
nepratele = ["Skřet", "Kostlivec", "Drak", "Sliz"]
nahodny_nepritel = random.choice(nepratele)
print(f"Objevil se divoký {nahodny_nepritel}!")
```

### 5. Slovníky pro tvorbu herního světa (Mapy)
Jak je ukázáno ve skriptu `02_textova_hra.py`, nejlepší způsob jak uchovávat data o místnostech a předmětech v nich, je použití struktury dat zvané `dictionary` (slovník). 
Můžete tak jednoduše propojovat místnosti pomocí směrů a ukládat do nich seznamy věcí.

Nebojte se experimentovat a zkusit si ukázkový kód upravit! Co takhle přidat do textové hry zdraví postavy, bojový systém, nebo zamčené dveře, které vyžadují klíč z jiné místnosti?
