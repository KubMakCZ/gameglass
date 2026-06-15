import pygame
import asyncio  # PŘIDÁNO PRO WEB: importujeme asyncio pro neblokující smyčku
import random
import sys

async def main():  # PŘIDÁNO PRO WEB: Zabalíme celou hru do asynchronní funkce
    # pygame.init() připraví knihovnu Pygame k použití. Volat to musíme vždy jako první věc!
    pygame.init()

    # --- Nastavení okna a základních konstant ---
    # Konstanty nepíšeme malými písmeny, ale VELKÝMI, abychom zdůraznili, že se jejich hodnota za běhu nemění.
    SIRKA_OKNA = 400
    VYSKA_OKNA = 600
    FPS = 60  # FPS (Frames Per Second) = kolikrát se celá obrazovka překreslí za vteřinu. 60 je hezky plynulé.

    # Barvy zapisujeme jako mix tří kanálů: (Červená, Zelená, Modrá) - každý má hodnotu 0 až 255.
    # (0,0,0) je černá (žádná barva), (255,255,255) je bílá (plné všechny barvy).
    CERNA = (0, 0, 0)
    BILA = (255, 255, 255)
    MODRA_OBLOHA = (135, 206, 235)
    ZELENA = (34, 139, 34)
    ZLUTYP_PTAK = (255, 215, 0)
    CERVENA = (255, 0, 0)

    # Vytvoření okna (plocha, kam se bude vše vykreslovat)
    okno = pygame.display.set_mode((SIRKA_OKNA, VYSKA_OKNA))
    pygame.display.set_caption("Flappy Bird") # Nápis v horní liště programu

    # Herní hodiny pro řízení rychlosti smyčky
    hodiny = pygame.time.Clock()

    # Tvorba písem. font_velky použijeme na herní nápisy (Konec hry apod.), font_maly na menší text.
    font_velky = pygame.font.SysFont("arial", 48, bold=True)
    font_maly = pygame.font.SysFont("arial", 24)

    # Pomocná funkce pro snazší kreslení textu. Abychom nemuseli pokaždé opakovat stejné složité příkazy.
    def zobraz_text(text, font, barva, x, y, zarovnat_stred=False):
        # render() převede text ze znaků do obrázku (tzv. "Surface"), který lze následně nakreslit.
        plocha = font.render(text, True, barva)
        if zarovnat_stred:
            # Vypočítáme obdélník (rect) obrázku textu a řekneme, ať je jeho STŘED (center) na dané X a Y pozici
            rect = plocha.get_rect(center=(x, y))
            okno.blit(plocha, rect) # blit() nalepí obrázek plochy na 'okno'
        else:
            # Jinak ho plácneme normálně za jeho levý horní roh
            okno.blit(plocha, (x, y))

    async def hlavni_smycka():
        # --- PROMĚNNÉ PTÁKA ---
        # Toto jsou proměnné, které se v čase mění, proto nejsou VELKÝMI PÍSMENY
        ptak_x = 50                 # Zleva je pták relativně blízko okraji
        ptak_y = VYSKA_OKNA // 2    # Vertikálně (Y) ho položíme doprostřed okna
        ptak_sirka = 30
        ptak_vyska = 30

        # Fyzika
        rychlost_padu = 0       # Zpočátku stojí pták na místě
        gravitace = 0.5         # Gravitace každým snímkem tuto 'rychlost_padu' zvyšuje směrem DOLŮ (kladné hodnoty Y)
        sila_skoku = -8         # Skok je prostě náhlé nastavení rychlosti do záporných hodnot, tedy NAHORU!

        # --- PROMĚNNÉ PŘEKÁŽEK (ZELENÉ TRUBKY) ---
        trubka_sirka = 60
        mezera_mezi_trubkami = 160  # Jak velikou skulinou bude hráč létat? (v pixelech)
        rychlost_posunu = 3         # Překážky neustále jedou směrem doleva, aby to vypadalo, že pták letí dopředu

        # Seznam do kterého budeme ukládat trubky. Použijeme slovníky {ključ: hodnota}.
        # Např: {"x": 400, "y_stred": 300} ... 'y_stred' určuje, kde přesně je střed oné mezery kudy se letí
        trubky = []

        # Funkce k přidání nové trubky na určené X ose
        def pridej_trubku(x_pozice):
            # Nechceme mezeru úplně na kraji (nemožné projet), omezíme ji od 150px nahoře po 150px dole
            stred_mezery = random.randint(150, VYSKA_OKNA - 150)
            trubky.append({"x": x_pozice, "y_stred": stred_mezery})

        # Přidáme první dvě trubky už před startem hry, nacházejí se zprvu mimo okno vpravo.
        pridej_trubku(SIRKA_OKNA + 100)
        pridej_trubku(SIRKA_OKNA + 400) # Další trubka má odstup 300 pixelů

        skore = 0

        # STAVOVÝ AUTOMAT - skvělý trik v programování. Znalost toho "ve kterém jsme stavu" 
        # nám pomáhá měnit logiku. Hra se chová úplně jinak, když jsme v MENU než když právě HRAJEME.
        stav_hry = "START" # Možnosti: "START", "HRA", "KONEC"

        # --- HERNÍ SMYČKA ---
        while True:

            # 1. ČTENÍ VSTUPŮ (UDÁLOSTI)
            for udalost in pygame.event.get():
                if udalost.type == pygame.QUIT:
                    pygame.quit() # Korektně ukončí knihovnu Pygame
                    sys.exit()    # Ukončí celý Python skript

                # Pokud někdo zmáčkl klávesu na klávesnici (KEYDOWN)
                if udalost.type == pygame.KEYDOWN:
                    if udalost.key == pygame.K_SPACE: # Speciálně zkoumáme MEZERNÍK
                        # Co dělá mezerník záleží na tom, v jakém STAVU je hra:
                        if stav_hry == "START":
                            stav_hry = "HRA"            # Přepneme hru na aktivní
                            rychlost_padu = sila_skoku  # Hned v první sekundě mu dáme skokový impuls
                        elif stav_hry == "HRA":
                            rychlost_padu = sila_skoku  # Hráč skočil! (Pták vzletí nahoru)
                        elif stav_hry == "KONEC":
                            return  # Vyskočíme z této funkce, což vyústí ve spuštění znova (viz úplně dole v kódu)

            # 2. LOGIKA A POHYB 
            # Zpracovává se jen pokud jsme ve stavu HRA
            if stav_hry == "HRA":

                # Aplikace gravitace: Rychlost pádu je stále vyšší kladné číslo
                rychlost_padu += gravitace
                # Přičtením této rychlosti k souřadnici Y pták pomalu (a čím dál rychleji) "padá" na zem okna
                ptak_y += rychlost_padu

                # Pohyb trubek doleva (zmenšujeme jejich osu X)
                for t in trubky:
                    t["x"] -= rychlost_posunu

                # Kontrola první trubky v seznamu: Nevyjela nám náhodou úplně ven z okna doleva?
                if trubky[0]["x"] < -trubka_sirka:
                    trubky.pop(0) # Odstraníme první trubku ze seznamu, už ji nikdy neuvidíme

                    # Zjistíme, kde byla zhruba naposled vygenerovaná trubka, a přidáme novou ZA ni
                    posledni_trubka_x = trubky[-1]["x"]
                    pridej_trubku(posledni_trubka_x + 300)

                    # Pokud trubka odjede ven, znamená to, že ji hráč musel úspěšně přeletět!
                    skore += 1

                # --- Detekce nárazů (KOLIZE) ---
                # Pro kontrolu jestli pták do něčeho vrazil používáme pygame.Rect (neviditelné hranice objektů)
                ptak_rect = pygame.Rect(ptak_x, ptak_y, ptak_sirka, ptak_vyska)

                # 1) Náraz do stropu nebo do podlahy okna
                if ptak_y < 0 or ptak_y + ptak_vyska > VYSKA_OKNA:
                    stav_hry = "KONEC" # Bum! Umřel.

                # 2) Náraz do jakékoliv překážky
                for t in trubky:
                    # Vypočteme, kde končí 'horní' překážka 
                    horni_vyska = t["y_stred"] - (mezera_mezi_trubkami // 2)
                    horni_rect = pygame.Rect(t["x"], 0, trubka_sirka, horni_vyska)

                    # Vypočteme, kde začíná 'spodní' překážka (od středu + polovina mezery)
                    dolni_y = t["y_stred"] + (mezera_mezi_trubkami // 2)
                    # Výška spodní části je VYSKA_OKNA mínus počáteční Y souřadnice spodní trubky
                    dolni_rect = pygame.Rect(t["x"], dolni_y, trubka_sirka, VYSKA_OKNA - dolni_y)

                    # Pokud se "obdélník ptáka" dotýká / prolíná (colliderect) s horní nebo dolní trubkou
                    if ptak_rect.colliderect(horni_rect) or ptak_rect.colliderect(dolni_rect):
                        stav_hry = "KONEC"

            # 3. KRESLENÍ (na 'platno')
            # Smažeme stopu ze starého snímku překrytím čistou oblohou
            okno.fill(MODRA_OBLOHA)

            # Nakreslení obou překážek
            for t in trubky:
                # Horní trubka vykreslena od Y=0 (strop)
                horni_vyska = t["y_stred"] - (mezera_mezi_trubkami // 2)
                pygame.draw.rect(okno, ZELENA, (t["x"], 0, trubka_sirka, horni_vyska))

                # Dolní trubka vykreslena od konce mezery (dolni_y) až dolu k podlaze
                dolni_y = t["y_stred"] + (mezera_mezi_trubkami // 2)
                pygame.draw.rect(okno, ZELENA, (t["x"], dolni_y, trubka_sirka, VYSKA_OKNA - dolni_y))

            # Nakreslení postavy (Ptáka)
            # int() ořezává desetinná čísla z fyziky do celých čísel pixelů, aby to šlo nakreslit
            pygame.draw.rect(okno, ZLUTYP_PTAK, (ptak_x, int(ptak_y), ptak_sirka, ptak_vyska))

            # --- ZOBRAZOVÁNÍ NÁPISŮ (UI) ---
            if stav_hry == "START":
                zobraz_text("Stiskni MEZERNÍK", font_maly, BILA, SIRKA_OKNA//2, VYSKA_OKNA//2 - 50, zarovnat_stred=True)
                zobraz_text("pro začátek létání", font_maly, BILA, SIRKA_OKNA//2, VYSKA_OKNA//2, zarovnat_stred=True)
            elif stav_hry == "HRA":
                # Skóre nahoře
                zobraz_text(str(skore), font_velky, BILA, SIRKA_OKNA//2, 50, zarovnat_stred=True)
            elif stav_hry == "KONEC":
                # GAME OVER statistiky po smrti
                zobraz_text("GAME OVER", font_velky, CERVENA, SIRKA_OKNA//2, VYSKA_OKNA//2 - 50, zarovnat_stred=True)
                zobraz_text(f"Skóre: {skore}", font_maly, BILA, SIRKA_OKNA//2, VYSKA_OKNA//2 + 10, zarovnat_stred=True)
                zobraz_text("Stiskni MEZERNÍK pro restart", font_maly, CERNA, SIRKA_OKNA//2, VYSKA_OKNA//2 + 50, zarovnat_stred=True)

            # "Otoč" buffer z paměti na reálný monitor - tady se stane kouzlo a vše se zobrazí!
            pygame.display.flip()  

            # Pojistka pro správnou rychlost. Počká se milisekundu tak, abychom dodrželi stanovené FPS.
            hodiny.tick(FPS)       
            # PRIDANO PRO WEB
            await asyncio.sleep(0)

# Toto funguje tak, že hru spouštíme donekonečna. Když hráč zemře a dá mezerník,
    # funkce 'hlavni_smycka()' skončí (return), ale díky tomuto cyklu 'while True' 
    # se obratem zavolá od znova z čistého stolu a se skórem nula.
    if __name__ == "__main__":
        while True:
            await hlavni_smycka()


# PŘIDÁNO PRO WEB: Spuštění asynchronní hry
asyncio.run(main())