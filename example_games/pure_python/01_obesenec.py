import random
import os

def vycisti_obrazovku():
    """Vyčistí obrazovku terminálu pro lepší herní zážitek."""
    # Pro Windows použijeme příkaz 'cls', pro systémy typu Linux/Mac 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')

def vykresli_obesence(pocet_chyb):
    """Vykreslí aktuální stav šibenice a oběšence podle počtu chyb."""
    # Seznam různých fází obrázku, index odpovídá počtu chyb
    faze = [
        """
           ------
           |    |
           |
           |
           |
           |
        -------
        """,
        """
           ------
           |    |
           |    O
           |
           |
           |
        -------
        """,
        """
           ------
           |    |
           |    O
           |    |
           |
           |
        -------
        """,
        """
           ------
           |    |
           |    O
           |   /|
           |
           |
        -------
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |
           |
        -------
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   /
           |
        -------
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |
        -------
        """
    ]
    print(faze[pocet_chyb])

def hraj_obesence():
    """Hlavní smyčka a logika hry Oběšenec."""
    # Seznam slov, ze kterých hra náhodně vybírá. Můžete přidat vlastní!
    slova = ["programovani", "python", "skola", "pocitac", "algoritmus", "hra", "promenna"]
    
    # Výběr náhodného slova a převod na velká písmena pro jednotnost
    hledane_slovo = random.choice(slova).upper()
    
    # 'set' (množina) zabraňuje ukládání duplicitních písmen
    uhadnuta_pismena = set()
    chybna_pismena = set()
    max_chyb = 6
    
    vycisti_obrazovku()
    print("Vítejte ve hře OBĚŠENEC!")
    print("------------------------")
    
    # Hra běží, dokud hráč neudělá maximum povolených chyb
    while len(chybna_pismena) < max_chyb:
        vykresli_obesence(len(chybna_pismena))
        
        # Zobrazení hledaného slova s podtržítky pro zatím neuhodnutá písmena
        zobrazene_slovo = ""
        for pismeno in hledane_slovo:
            if pismeno in uhadnuta_pismena:
                zobrazene_slovo += pismeno + " "
            else:
                zobrazene_slovo += "_ "
                
        print(f"Slovo: {zobrazene_slovo}")
        print(f"Chybná písmena: {', '.join(chybna_pismena)}")
        print(f"Zbývající pokusy: {max_chyb - len(chybna_pismena)}")
        
        # Kontrola výhry: Všechna písmena z hledaného slova jsou v množině uhodnutých písmen
        if set(hledane_slovo).issubset(uhadnuta_pismena):
            print("\nGRATULUJEME! Uhodli jste slovo:", hledane_slovo)
            return # Ukončení funkce, tím i hry

        # Získání vstupu od hráče (převedeme na velká písmena)
        tip = input("\nZadej písmeno: ").upper()
        vycisti_obrazovku()
        
        # Kontrola platnosti vstupu: musí to být přesně jeden znak a musí to být písmeno (ne číslo)
        if len(tip) != 1 or not tip.isalpha():
            print("Chyba: Zadej prosím právě jedno písmeno!")
            continue # Skočíme zpět na začátek cyklu while
            
        # Kontrola, zda hráč nehádá písmeno, které už hádal
        if tip in uhadnuta_pismena or tip in chybna_pismena:
            print(f"Pozor: Písmeno '{tip}' už jsi hádal!")
            continue
            
        # Vyhodnocení tipu
        if tip in hledane_slovo:
            print(f"Výborně! Písmeno '{tip}' je ve slově.")
            uhadnuta_pismena.add(tip)
        else:
            print(f"Škoda, písmeno '{tip}' ve slově není.")
            chybna_pismena.add(tip)
            
    # Cyklus skončil - hráč udělal 6 chyb. Hráč prohrál.
    vykresli_obesence(len(chybna_pismena))
    print("\nPROHRÁL JSI! Hledané slovo bylo:", hledane_slovo)

if __name__ == "__main__":
    # Tato část se spustí jen pokud pustíme přímo tento skript
    hraj_obesence()
    input("\nStiskni Enter pro ukončení programu...")
