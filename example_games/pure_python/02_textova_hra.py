import time
import os

def vycisti_obrazovku():
    """Vyčistí obrazovku terminálu, aby text nebyl nepřehledný."""
    os.system('cls' if os.name == 'nt' else 'clear')

def vypis_pomalu(text, zpozdeni=0.03):
    """
    Vypíše text znak po znaku pro lepší herní (RPG) atmosféru.
    Parametr 'zpozdeni' určuje, jak rychle se text vypíše.
    """
    for znak in text:
        # parametr end='' způsobí, že 'print' automaticky neodřádkuje
        # flush=True vynutí okamžité vypsání znaku na obrazovku
        print(znak, end='', flush=True)
        time.sleep(zpozdeni)
    print() # Odřádkování na samotném konci

# Definice místností (mapa hry)
# Každá místnost je slovník (dictionary) obsahující popis a cesty do dalších místností.
# Umožňuje to jednoduše tvořit i velmi složitou mapu.
mistnosti = {
    'jeskyne': {
        'popis': 'Stojíš v temné vlhké jeskyni. Slyšíš kapání vody a cítíš chlad.',
        'vychody': {'sever': 'chodba'}, # Klíč je směr, hodnota je ID další místnosti
        'predmety': ['klic'] # Seznam předmětů ležících v místnosti
    },
    'chodba': {
        'popis': 'Jsi v dlouhé kamenné chodbě. Na stěnách jsou podivné prastaré malby.',
        'vychody': {'jih': 'jeskyne', 'vychod': 'pokladnice'},
        'predmety': []
    },
    'pokladnice': {
        'popis': 'Ocitl ses v obrovské místnosti se zlatými dveřmi na konci a podstavcem uprostřed.',
        'vychody': {'zapad': 'chodba'},
        'predmety': ['mec']
    }
}

# Počáteční stav hry (proměnné pro sledování stavu hráče)
aktualni_mistnost = 'jeskyne'
inventar = [] # Prázdný seznam pro předměty

def hraj_hru():
    """Hlavní smyčka hry, která zpracovává příkazy od hráče."""
    global aktualni_mistnost # Potřebujeme měnit globální proměnnou
    
    vycisti_obrazovku()
    vypis_pomalu("Vítej v textovém dobrodružství!")
    vypis_pomalu("K dispozici máš příkazy: 'jdi [smer]', 'vezmi [predmet]', 'inventar', 'pomoc', 'konec'")
    print("-" * 50)
    time.sleep(1)
    
    # Hlavní herní smyčka (běží do nekonečna, dokud ji neukončíme)
    while True:
        # Získání dat o aktuální lokaci
        mistnost_data = mistnosti[aktualni_mistnost]
        print("\n" + "=" * 50)
        vypis_pomalu(mistnost_data['popis'])
        
        # Zobrazení dostupných východů
        vychody = list(mistnost_data['vychody'].keys())
        print(f"Vidíš cesty na: {', '.join(vychody)}")
        
        # Zobrazení předmětů v místnosti
        if mistnost_data['predmety']:
            print(f"Na zemi leží: {', '.join(mistnost_data['predmety'])}")
            
        # Neustálý výpis inventáře, pokud v něm něco je
        if inventar:
            print(f"[ Tvůj inventář: {', '.join(inventar)} ]")
            
        # Vstup od hráče, vše převedeme na malá písmena a rozdělíme podle mezer do seznamu
        prikaz = input("\nCo chceš udělat? > ").lower().strip().split()
        
        if not prikaz:
            continue # Hráč nic nezadal a zmáčkl Enter
            
        akce = prikaz[0] # První slovo je samotná akce
        
        # ==========================================
        # Zpracování jednotlivých příkazů
        # ==========================================
        if akce == 'konec':
            print("Díky za hru!")
            break # Přeruší smyčku while a ukončí hru
            
        elif akce == 'pomoc':
            print("\n--- NÁPOVĚDA ---")
            print("Můžeš psát následující příkazy:")
            print("  jdi [sever/jih/zapad/vychod] - přesun do jiné místnosti")
            print("  vezmi [predmet] - sebereš předmět ze země")
            print("  inventar - vypíše, co máš u sebe")
            print("  konec - ukončí hru")
            print("----------------\n")
            
        elif akce == 'inventar':
            # Kontrola, zda seznam inventar není prázdný
            if inventar:
                print(f"Máš u sebe: {', '.join(inventar)}")
            else:
                print("Tvůj inventář je prázdný.")
                
        elif akce == 'jdi':
            if len(prikaz) < 2:
                print("Chyba: Musíš zadat směr (např. 'jdi sever').")
                continue
                
            smer = prikaz[1] # Druhé slovo je směr
            if smer in mistnost_data['vychody']:
                aktualni_mistnost = mistnost_data['vychody'][smer]
                vycisti_obrazovku()
                vypis_pomalu(f"Jdeš na {smer}...")
            else:
                print("Tímto směrem nemůžeš jít!")
                
        elif akce == 'vezmi':
            if len(prikaz) < 2:
                print("Chyba: Musíš zadat, co chceš vzít (např. 'vezmi klic').")
                continue
                
            predmet = prikaz[1]
            if predmet in mistnost_data['predmety']:
                mistnost_data['predmety'].remove(predmet) # Odebere ze země
                inventar.append(predmet) # Přidá hráči
                print(f"Vzal jsi předmět: {predmet}.")
            else:
                print(f"Předmět '{predmet}' tady nikde nevidíš.")
                
        else:
            print("Neznámý příkaz. Zkus např. 'jdi sever', 'vezmi klic', 'pomoc' nebo 'konec'.")

if __name__ == "__main__":
    hraj_hru()
