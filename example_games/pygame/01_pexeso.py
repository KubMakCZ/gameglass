import pygame
import asyncio  # PŘIDÁNO PRO WEB: importujeme asyncio pro neblokující smyčku
import random
import sys

async def main():  # PŘIDÁNO PRO WEB: Zabalíme celou hru do asynchronní funkce
    # pygame.init() nastartuje všechny vnitřní moduly Pygame.
    # Je to naprosto povinný první krok před tím, než můžeme v Pygame cokoliv udělat.
    pygame.init()

    # --- Konstanty okna a rozvržení mřížky ---
    # Konstanty (velkými písmeny) se během hry nemění. Určují základní vlastnosti naší hry.
    SIRKA_OKNA = 600
    VYSKA_OKNA = 600
    FPS = 30 # Počet snímků za sekundu (jak rychle se hra překresluje). 30 bohatě stačí pro Pexeso.

    # Kolik karet chceme mít na šířku a na výšku?
    RADKY = 4
    SLOUPCE = 4
    # Velikost jedné karty v pixelech (obrazových bodech)
    KARTICKA_VELIKOST = 100
    # Mezera mezi kartičkami
    MEZERA = 20

    # Výpočet celkové šířky a výšky celé mřížky karet, abychom ji pak mohli na obrazovce vycentrovat
    Mrizka_sirka = (SLOUPCE * KARTICKA_VELIKOST) + ((SLOUPCE - 1) * MEZERA)
    Mrizka_vyska = (RADKY * KARTICKA_VELIKOST) + ((RADKY - 1) * MEZERA)

    # Vypočítáme, kde mřížka začíná na osách X (vodorovně) a Y (svisle), aby byla přesně uprostřed okna
    Odsazeni_x = (SIRKA_OKNA - Mrizka_sirka) // 2
    Odsazeni_y = (VYSKA_OKNA - Mrizka_vyska) // 2

    # Barvy v Pygame se zadávají ve formátu (R, G, B) = Red, Green, Blue.
    # Každá hodnota je od 0 (nic) do 255 (maximum dané barvy).
    BILA = (255, 255, 255)
    SEDA = (150, 150, 150)
    TMAVE_MODRA = (20, 20, 80)
    ZELENA_TEXT = (50, 255, 50)

    # Budeme mít celkem 16 karet (4x4), což znamená 8 různých párů (8 unikátních barev).
    BARVY_PARU = [
        (255, 0, 0),    # Červená
        (0, 255, 0),    # Světle Zelená
        (0, 0, 255),    # Modrá
        (255, 255, 0),  # Žlutá
        (255, 0, 255),  # Fialová
        (0, 255, 255),  # Azurová
        (255, 165, 0),  # Oranžová
        (139, 69, 19)   # Hnědá
    ]

    # Vytvoříme samotné okno (obrazovku), kam se bude vše vykreslovat
    okno = pygame.display.set_mode((SIRKA_OKNA, VYSKA_OKNA))
    # Nastavíme text, který uvidíme nahoře v liště okna
    pygame.display.set_caption("Pexeso (Hledání barevných párů)")

    # Založíme si herní "hodiny" - pomohou nám udržovat hru v rychlosti stanovené přes FPS
    hodiny = pygame.time.Clock()

    # Fonty slouží pro vykreslování textu. Načteme si dva různé.
    font = pygame.font.SysFont("arial", 40, bold=True)
    font_maly = pygame.font.SysFont("arial", 20)

    # --- Třída objektu - objektově orientované programování (OOP) ---
    # Třída je jako "plánek" na vytvoření konkrétních věcí. Zde je to plánek na vytvoření "Kartičky".
    # Každá kartička si bude sama pamatovat, jakou má barvu a jestli je už otočená.
    class Karticka:
        def __init__(self, radek, sloupec, barva_vnitrku):
            self.barva = barva_vnitrku # Tato barva bude vidět, když se karta otočí

            # Stavové proměnné (True = ano, False = ne)
            self.odkryta = False  # Zda ji hráč v tomto tahu právě teď otočil
            self.nalezena = False # Zda už hráč našel její pár a karta je tak z kola venku

            # Matematika! Vypočítáme přesnou pozici X a Y (v pixelech), kam se tato karta nakreslí.
            self.x = Odsazeni_x + sloupec * (KARTICKA_VELIKOST + MEZERA)
            self.y = Odsazeni_y + radek * (KARTICKA_VELIKOST + MEZERA)

            # pygame.Rect vytvoří "neviditelný obdélník" kolem naší kartičky.
            # Díky němu se mnohem snadněji zjišťuje, jestli na kartičku hráč kliknul myší.
            self.rect = pygame.Rect(self.x, self.y, KARTICKA_VELIKOST, KARTICKA_VELIKOST)

        def vykresli(self):
            # Funkce (metoda), která zajistí, že se karta správně namaluje na obrazovku

            if self.odkryta or self.nalezena:
                # Pokud je karta odkrytá (otočená), namalujeme její tajnou barvu
                pygame.draw.rect(okno, self.barva, self.rect)
            else:
                # Pokud karta leží rubem nahoru, namalujeme ji šedou (nebo jakýkoliv jiný vzor chceme)
                pygame.draw.rect(okno, SEDA, self.rect)

            # Kromě výplně nakreslíme ještě bílý obrys (rámeček) o tloušťce 3 pixely, ať to lépe vypadá
            pygame.draw.rect(okno, BILA, self.rect, 3)

    async def hlavni_smycka():
        # --- PŘÍPRAVA HRY ---
        # 1. Připravíme si seznam barev. Chceme 8 párů, takže každou barvu z BARVY_PARU potřebujeme dvakrát.
        barvy_do_hry = BARVY_PARU * 2 
        # Modul random má funkci shuffle, která pořadí položek v seznamu krásně zamíchá.
        random.shuffle(barvy_do_hry) 

        # 2. Vytvoření "mřížky" kartiček (2D pole, tedy seznam v seznamu)
        karticky = []
        index_barvy = 0 # Slouží k tomu, abychom z listu barvy_do_hry postupně brali barvy

        for radek in range(RADKY):
            rada = [] # Vytvoříme prázdný seznam pro jeden konkrétní řádek
            for sloupec in range(SLOUPCE):
                # Pro každé políčko vytvoříme nový objekt podle našeho "plánku" Karticka
                karta = Karticka(radek, sloupec, barvy_do_hry[index_barvy])
                rada.append(karta) # Kartu přidáme do řádku
                index_barvy += 1
            karticky.append(rada) # Celý naplněný řádek přidáme do hlavní mřížky

        # Proměnné pro systém hry - pamatujeme si, co hráč naklikal v aktuálním tahu
        prvni_vybrana = None
        druha_vybrana = None

        pocet_pokusu = 0
        nalezeno_paru = 0

        # --- HLAVNÍ HERNÍ SMYČKA ---
        # Tento cyklus 'while True' běží pořád dokola, stokrát za sekundu a tvoří samotnou hru
        while True:

            # 1. ZPRACOVÁNÍ UDÁLOSTÍ (Event handling)
            # Události jsou vstupy od hráče: stisknutí klávesy, kliknutí myší, zavření okna křížkem...
            for udalost in pygame.event.get():
                # Pokud hráč klikl na červený křížek okna, ukončíme Pygame a celou aplikaci
                if udalost.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Kontrola kliknutí myší (MOUSEBUTTONDOWN = tlačítko zmáčknuto dolů, button 1 = levé tlačítko)
                if udalost.type == pygame.MOUSEBUTTONDOWN and udalost.button == 1:

                    # Pokud už hráč v tomto tahu otočil dvě karty a čekáme, zabráníme mu klikat dál!
                    if prvni_vybrana is not None and druha_vybrana is not None:
                        continue # "continue" přeskočí zbytek kódu v této smyčce a nedovolí mu kartu otočit

                    # Kde přesně se myš nachází? Souřadnice X,Y na obrazovce.
                    mys_x, mys_y = pygame.mouse.get_pos()

                    # Projdeme všechny naše karty jednu po druhé a zkontrolujeme, zda hráč neklikl na některou z nich
                    for radek in range(RADKY):
                        for sloupec in range(SLOUPCE):
                            karta = karticky[radek][sloupec]

                            # Metoda collidepoint zjistí, zda se bod (myš) nachází uvnitř obdélníku (karty)
                            if karta.rect.collidepoint(mys_x, mys_y):
                                # Otočit můžeme jen kartu, která ještě NENÍ otočená
                                if not karta.odkryta and not karta.nalezena:
                                    karta.odkryta = True # Hráč ji otočil!

                                    # Systém logiky: Byla tohle první karta v tahu?
                                    if prvni_vybrana is None:
                                        prvni_vybrana = karta
                                    else:
                                        # Nebyla, takže to už musí být druhá karta v tahu.
                                        druha_vybrana = karta
                                        pocet_pokusu += 1 # Tah končí, započítáme pokus

            # 2. VYKRESLOVÁNÍ (Kreslíme nový "snímek" - frame)
            # Nejdřív vždy smažeme starý obraz tím, že celé okno přebarvíme jednolitou barvou
            okno.fill(TMAVE_MODRA)

            # Projdeme mřížku a řekneme každé kartičce, aby se nakreslila na okno
            for radek in range(RADKY):
                for sloupec in range(SLOUPCE):
                    karticky[radek][sloupec].vykresli()

            # Vykreslíme text s počtem pokusů. Funkce render vytvoří z textu "obrázek", který pak můžeme vykreslit
            text_tahy = font_maly.render(f"Počet pokusů: {pocet_pokusu}", True, BILA)
            # blit je příkaz pro "nalep tento obrázek na dané souřadnice"
            okno.blit(text_tahy, (10, 10))

            # Zkontrolujeme vítězství
            if nalezeno_paru == 8: # Maximum možných párů je 8
                text_konec = font.render("Vítězství! Skvělá paměť.", True, ZELENA_TEXT)
                # Center zarovná text hezky doprostřed požadované X pozice
                rect = text_konec.get_rect(center=(SIRKA_OKNA // 2, VYSKA_OKNA - 30))
                okno.blit(text_konec, rect)

            # ZÁSADNÍ VĚC: Po tom co jsme do paměti Pygame naskládali příkazy kreslení, 
            # musíme to všechno najednou zviditelnit na obrazovce pomocí příkazu flip() nebo update()!
            # Děláme to už teď, abychom (pokud budeme dole hru pauzovat), viděli otočenou druhou kartu.
            pygame.display.flip()

            # 3. HERNÍ LOGIKA: Vyhodnocení tahu
            # Pokud už hráč vybral dvě karty, musíme zjistit, jestli udělal pár
            if prvni_vybrana is not None and druha_vybrana is not None:
                if prvni_vybrana.barva == druha_vybrana.barva:
                    # SUPER! Barvy se shodují, je to PÁR!
                    prvni_vybrana.nalezena = True
                    druha_vybrana.nalezena = True
                    nalezeno_paru += 1
                else:
                    # ŠPATNĚ! Barvy se liší.
                    # Aby hráč vůbec stihl zaregistrovat barvu druhé karty, musíme na chvíli zmrazit hru
                    # PŘIDÁNO PRO WEB: Ve webovém prostředí nesmíme použít pygame.time.wait(), protože by zmrazil prohlížeč. 
                    # Místo toho asynchronně uspíme smyčku, což umožní prohlížeči vykreslit druhou kartu.
                    await asyncio.sleep(1) 

                    # A pak obě karty otočíme zase lícem dolů (šedá strana nahoru)
                    prvni_vybrana.odkryta = False
                    druha_vybrana.odkryta = False

                # Tah je u konce, ať už to byl pár nebo ne. Vyčistíme výběr pro další tah!
                prvni_vybrana = None
                druha_vybrana = None

            # Rychlost smyčky: Řekneme hodinám, že chceme, aby smyčka běžela maximálně tolikrát za vteřinu, jak určuje FPS
            hodiny.tick(FPS)
            # PRIDANO PRO WEB
            await asyncio.sleep(0)

# Tohle říká Pythonu: Pokud tento soubor spouštíš jako hlavní program (ne jen importuješ),
    # tak teprve tehdy spusť hlani_smycka()
    if __name__ == "__main__":
        await hlavni_smycka()


# PŘIDÁNO PRO WEB: Spuštění asynchronní hry
asyncio.run(main())