import pygame
import asyncio  # PŘIDÁNO PRO WEB: importujeme asyncio pro neblokující smyčku
import sys
import random

async def main():  # PŘIDÁNO PRO WEB: Zabalíme celou hru do asynchronní funkce
    pygame.init()

    # --- NASTAVENÍ OKNA A PROMĚNNÝCH PROSTŘEDÍ ---
    SIRKA = 800
    VYSKA = 600
    okno = pygame.display.set_mode((SIRKA, VYSKA))
    pygame.display.set_caption("Skákačka přes překážky")

    # --- BARVY ---
    BILA = (255, 255, 255)
    CERNA = (0, 0, 0)
    MODRA = (50, 150, 255) # Na modrou oblohu
    ZELENA = (50, 200, 50) # Zelená pro plošinu trávy
    CERVENA = (255, 0, 0)  # Nebezpečné překážky v cestě

    hodiny = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 40)
    font_maly = pygame.font.SysFont("Arial", 25)

    # --- STAVOVÝ AUTOMAT HRY ---
    STAV_MENU = 0
    STAV_HRA = 1
    STAV_KONEC = 2
    stav = STAV_MENU

    # --- FYZIKA A HERNÍ PROMĚNNÉ ---
    podlaha_y = VYSKA - 50 # V jaké hloubce se nachází hrana země/podlahy? (od shora dolů)
    hrac_sirka = 40
    hrac_vyska = 40

    # Fyzika
    # Gravitace způsobuje trvalé ZRYCHLOVÁNÍ pádu. Ne rychlost, zrychlení!
    gravitace = 0.6
    # Skok není nic jiného, než extrémní rána do záporných hodnot na ose Y (odstřelení do stropu)
    sila_skoku = -12 

    def reset_hry():
        """Funkce pro nahození proměnných do výchozího stavu pro start čisté hry"""
        global hrac_x, hrac_y, rychlost_y, na_zemi, prekazky, skore, rychlost_hry
        hrac_x = 100 # Hráč stojí celkem blízko levému kraji, aby měl čas reagovat

        # Hráče položíme tak, aby jeho nohy (y + výška) přesně seděly na 'podlaha_y'
        hrac_y = podlaha_y - hrac_vyska 
        rychlost_y = 0
        na_zemi = True # Nyní stojí na zemi (a smí tedy zmáčknout Skok)

        # Místo abychom dělali překážku po překážce, uchováme je jako seznam (List)
        prekazky = []  
        skore = 0
        rychlost_hry = 6 # Jak rychle ubíhá terén směrem k hráči doleva?

    reset_hry()

    # --- VLASTNÍ ČASOVAČ (Custom Event) ---
    # Trik z programování: Pygame neustále běží ve smyčce a "naslouchá" událostem (jako stisk myši).
    # Zde si vyrobíme událost NAŠI VLASTNÍ. Pojmenujeme ji libovolně SPAWN_PREKAZKY.
    SPAWN_PREKAZKY = pygame.USEREVENT + 1
    # Nastavíme pygame časovač tak, ať tuto 'neviditelnou klávesu SPAWN_PREKAZKY' pípne
    # do fronty událostí přesně každých 1500 milisekund (1.5 sekundy). Úplně automaticky!
    pygame.time.set_timer(SPAWN_PREKAZKY, 1500)

    bezime = True
    while bezime:

        # 1. ZPRACOVÁNÍ UDÁLOSTÍ
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                bezime = False

            # Zkoumání stisku kláves jako POUHÁ UDÁLOST. To znamená "zmáčklo se to"
            # neboli neřešíme, jestli se to zrovna drží stlačené. Ideální pro Starty a Skoky.
            if udalost.type == pygame.KEYDOWN:
                if stav == STAV_MENU and udalost.key == pygame.K_SPACE:
                    stav = STAV_HRA
                elif stav == STAV_KONEC and udalost.key == pygame.K_SPACE:
                    reset_hry()
                    stav = STAV_HRA

                # Jak hráč skáče? Šipka nahoru! Ale MUSÍ zároveň stát na zemi (na_zemi == True), 
                # jinak bychom mohli skákat ve vzduchu jak pták (tzv. multi-jump)
                elif stav == STAV_HRA and udalost.key == pygame.K_UP and na_zemi:
                    rychlost_y = sila_skoku # Tímto dáváme drtivý impulz rychlosti směrem NAHORU
                    na_zemi = False         # Teď už jsme ve vzduchu!

            # Tady čekáme na PÍPNUTÍ z našeho automatického Custom Časovače!!!
            if udalost.type == SPAWN_PREKAZKY and stav == STAV_HRA:
                # Objevil se signál, že uplynulo 1.5 sekundy.
                # Přidáme novou překážku (čtvereček červený) na konec obrazovky (SIRKA)
                # Tyto překážky ukládáme rovnou jako Rect, protože se to pak hodí u kolizí
                prekazky.append(pygame.Rect(SIRKA, podlaha_y - 40, 30, 40))

                # Aby to nebylo nudné, pokaždé hru o malilinký kousíček zrychlíme.
                rychlost_hry += 0.1 

        # 2. LOGIKA
        if stav == STAV_HRA:
            # --- FYZIKA SKÁKÁNÍ ---
            # Neúprosná gravitace v každém milisekundovém snímku přidává směrem DOLŮ!
            rychlost_y += gravitace  
            # Změníme opravdovou Y pozici hráče o tuto aktuální rychlost.
            # Výsledek? Hráč zpomaluje směrem nahoru... zastaví se... a začne opět zrychlovat dolů k zemi!
            hrac_y += rychlost_y     

            # Musíme ale zabránit tomu, aby hráč propadl podlahou do hlubin!
            if hrac_y + hrac_vyska >= podlaha_y:
                # Opravíme jeho Y, posadíme ho přesně podrážkama na okraj podlahy
                hrac_y = podlaha_y - hrac_vyska 
                rychlost_y = 0   # Rychlost dopadu zrušíme, stál by na místě
                na_zemi = True   # Oznámíme, že zase můžeme skákat, dotýkáme se

            # Vytvoření virtuálního obalu přes našeho hráče kvůli měření kolizí
            hrac_rect = pygame.Rect(hrac_x, hrac_y, hrac_sirka, hrac_vyska)

            # --- LOGIKA VŠECH PŘEKÁŽEK NA TRATI ---
            # For cyklus prekazky[:] zkoumá tzv. KOPII seznamu. 
            # Je to proto, abychom z originálu mohli prvek bezpečně vymazat a nic "nepřeskočili".
            for p in prekazky[:]:
                p.x -= int(rychlost_hry) # Každá jedna překážka jede nezadržitelně doleva směrem na nás

                # Co když se obdélníčky Hráče a Překážky překrývají? -> BOUM!
                if p.colliderect(hrac_rect):
                    stav = STAV_KONEC

                # Pokud na nás nenarazila, zajela na levém okraji pod 0 a zmizela (p.x < -30)
                if p.x < -30:
                    prekazky.remove(p) # Hráč ji s úspěchem přežil a překážka zajela za monitor. Smazat z RAM!
                    skore += 1         # Přičteme za ni bod.

        # 3. KRESLENÍ (na monitor)
        okno.fill(MODRA) # Obloha
        # Nakreslíme zelený pruh od čáry podlahy (podlaha_y) dolů až k zemi, bude dělat vizuál trávy
        pygame.draw.rect(okno, ZELENA, (0, podlaha_y, SIRKA, VYSKA - podlaha_y))

        if stav == STAV_MENU:
            text = font.render("SKÁKAČKA", True, BILA)
            start = font_maly.render("Stiskni MEZERNÍK. Skáče se šipkou NAHORU.", True, CERNA)
            okno.blit(text, (SIRKA//2 - text.get_width()//2, 200))
            okno.blit(start, (SIRKA//2 - start.get_width()//2, 300))

        elif stav == STAV_HRA:
            # Nakreslení postavičky hráče - využijeme ten Rect obal, co už jsme si spočítali
            pygame.draw.rect(okno, CERNA, hrac_rect) 

            # Nakreslíme úplně všechny načítané nepřátelské Rect obdélníky jako červené objekty
            for p in prekazky:
                pygame.draw.rect(okno, CERVENA, p)   

            skore_text = font.render(f"Skóre: {skore}", True, CERNA)
            okno.blit(skore_text, (10, 10))

        elif stav == STAV_KONEC:
            text = font.render("KONEC HRY", True, CERVENA)
            skore_text = font.render(f"Dosažené skóre: {skore}", True, BILA)
            restart = font_maly.render("Stiskni MEZERNÍK pro novou hru", True, CERNA)

            okno.blit(text, (SIRKA//2 - text.get_width()//2, 150))
            okno.blit(skore_text, (SIRKA//2 - skore_text.get_width()//2, 220))
            okno.blit(restart, (SIRKA//2 - restart.get_width()//2, 300))

        # .flip() překlopí to, co jsme nakreslili v paměti na obrazovku k hráči
        pygame.display.flip()
        hodiny.tick(60) # Cílíme na hladkých 60 FPS (Frames Per Second)
        # PRIDANO PRO WEB
        await asyncio.sleep(0)

pygame.quit()
    sys.exit()


# PŘIDÁNO PRO WEB: Spuštění asynchronní hry
asyncio.run(main())