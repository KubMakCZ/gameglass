import pygame
import asyncio  # PŘIDÁNO PRO WEB: importujeme asyncio pro neblokující smyčku
import random
import sys

# Povinná příprava knihovny Pygame
async def main():  # PŘIDÁNO PRO WEB: Zabalíme celou hru do asynchronní funkce
    pygame.init()

    # --- NASTAVENÍ OKNA A MŘÍŽKY ---
    # Hra SNAKE (Had) většinou nefunguje na pixely jako ostatní hry, ale funguje na jakési neviditelné "Mřížce".
    SIRKA_OKNA = 800
    VYSKA_OKNA = 600
    VELIKOST_DILKU = 20  # Velikost jednoho čtverečku na mřížce (dílku hada i jídla)
    FPS = 15             # Rychlost hada. Zde je nižší 15, protože pohyb po skocích na mřížce nevyžaduje 60 FPS.

    # Definice Palety Barev (Red, Green, Blue)
    CERNA = (0, 0, 0)
    BILA = (255, 255, 255)
    ZELENA = (0, 255, 0)
    CERVENA = (255, 0, 0)

    okno = pygame.display.set_mode((SIRKA_OKNA, VYSKA_OKNA))
    pygame.display.set_caption("Klasický Had (Snake)")

    hodiny = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 36)

    # Pomocná funkce pro rychlé vykreslení textu na daných x, y. 
    # Zkracuje to kód, abychom pořád neopakovali metody render() a blit().
    def zobraz_text(text, barva, x, y):
        text_plocha = font.render(text, True, barva)
        okno.blit(text_plocha, (x, y))

    # Veškerou logiku hry teď poprvé schováme do tzv. Hlavní Funkce.
    # Proč? Jakmile funkce skončí (kvůli výhře/prohře), velmi jednoduše se tímto trikem dá celá hra resetovat, 
    # jelikož stačí funkci zavolat odznova.
    async def hlavni_smycka():

        # --- POČÁTEČNÍ STAV HRY ---
        # Nejdůležitější princip této hry! Tělo hada není jeden objekt, je to SEZNAM SOUŘADNIC (pole v poli).
        # Každý článek jeho těla má své [x, y]. Ten ÚPLNĚ PRVNÍ prvek na pozici 0 je HLAVA HADA.
        had_telo = [
            [SIRKA_OKNA // 2, VYSKA_OKNA // 2],                         # Hlava
            [SIRKA_OKNA // 2 - VELIKOST_DILKU, VYSKA_OKNA // 2],        # Druhý článek břicha
            [SIRKA_OKNA // 2 - 2 * VELIKOST_DILKU, VYSKA_OKNA // 2]     # Ocas
        ]

        # Směr pohybu! Tohle číslo přidáme při každém snímku k souřadnicím HLAVY. 
        # Tím ji virtuálně posuneme vpřed. 
        smer_x = VELIKOST_DILKU # Z počátku letí had doprava, protože z osy X roste pozitivně
        smer_y = 0              # Do vertikály Y mu zpočátku nepřidáváme nic, letí rovně

        # --- POZICE JÍDLA (ČERVENÝ ČTVEREČEK) ---
        # Jídlo musíme nasměrovat přesně do nějaké buňky mřížky!
        # Trik: random.randrange(od, do, krok) ... Jídlo padne například na X=20, 40, 60... ale NIKDY na 17, 33 atd.
        # Kdyby nebylo zarovnané na mřížku, tak ho had miné!
        jidlo_x = random.randrange(0, SIRKA_OKNA, VELIKOST_DILKU)
        jidlo_y = random.randrange(0, VYSKA_OKNA, VELIKOST_DILKU)

        skore = 0
        konec_hry = False # Boolean kontrolka pro Game Over

        # Nekonečná smyčka tohoto jednoho konkrétního zápasu
        while True:

            # 1. ZPRACOVÁNÍ UDÁLOSTÍ
            for udalost in pygame.event.get():
                if udalost.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Detekce šipek pro změnu SMĚRU pohybu HADA
                if udalost.type == pygame.KEYDOWN:

                    # OCHRANA: Had nemůže provést fyzicky nemožný obrat o 180 stupňů a zajet si rovnou do těla!
                    # Tzn. pokud zmáčknul šipku DOLEVA, a had letí rovně/doprava (smer_x == 0),
                    # teprve pak si smí dovolit nastavit změnu směru.
                    if udalost.key == pygame.K_LEFT and smer_x == 0:
                        smer_x = -VELIKOST_DILKU # Záporná hodnota pro směr vlevo
                        smer_y = 0               # Vertikální se ruší
                    elif udalost.key == pygame.K_RIGHT and smer_x == 0:
                        smer_x = VELIKOST_DILKU  # Kladná hodnota pro směr vpravo
                        smer_y = 0
                    elif udalost.key == pygame.K_UP and smer_y == 0:
                        smer_x = 0
                        smer_y = -VELIKOST_DILKU # Záporná hodnota směrem vzhůru k Y=0
                    elif udalost.key == pygame.K_DOWN and smer_y == 0:
                        smer_x = 0
                        smer_y = VELIKOST_DILKU

                    # Pokud zemřel a bliká varování, čekáme na Mezerník
                    if udalost.key == pygame.K_SPACE and konec_hry:
                        # Pokud nastane RETURN, znamená to, že se celá tato 'hlavni_smycka()' okamžitě ukončí,
                        # její paměť (proměnné had_telo atd) se nenávratně vymaže.
                        # Následně ji však náš spouštěč úplně dole v souboru spustí naprosto na čisto znova. (RESTART)
                        return  

            # LOGIKA HRY: Provede se jenom pokud žijeme
            if not konec_hry:

                # --- ZÁKLADNÍ PRINCIP POHYBU HADA ---
                # Jak hada posunout?
                # 1. Spočítáme, kde se bude nacházet hadova hlava v PŘÍŠTÍM Snímku
                # Vezmeme si pozici staré hlavy, neboli had_telo na nultém indexu
                nova_hlava_x = had_telo[0][0] + smer_x
                nova_hlava_y = had_telo[0][1] + smer_y

                # 2. Tuto ZCELA NOVOU POZICI vsuneme pomocí "insert" na ÚPLNÝ ZAČÁTEK (index 0) našeho Seznamu
                # Náš had je najednou o kousek delší! (Natáhl hlavu tam, kam letí)
                had_telo.insert(0, [nova_hlava_x, nova_hlava_y])

                # --- SEŽRÁNÍ JÍDLA (Růst hada) ---
                # Zjišťujeme, zda se souřadnice nové hlavy náhodou rovnou nerovnají pozici Jídla na mřížce.
                # Nepoužíváme obdélníkové kolize, protože pracujeme s přesnou mřížkou!
                if nova_hlava_x == jidlo_x and nova_hlava_y == jidlo_y:
                    skore += 1 # Bod do tabulky!

                    # Zrušíme staré jídlo a najdeme mu na hracím plánu nové náhodné místo (zarovnané na mřížku)
                    jidlo_x = random.randrange(0, SIRKA_OKNA, VELIKOST_DILKU)
                    jidlo_y = random.randrange(0, VYSKA_OKNA, VELIKOST_DILKU)

                    # TOHLE JE DŮLEŽITÉ: Náš hadí Seznam byl momentálně obohacen o přední novou "hlavu", tzn vyrostl, a 
                    # a my mu ten starý OCAS NEZKRÁTÍME. Takže je opravdu objektivně o jedno políčko natrvalo větší!
                else:
                    # Pokud jídlo na této pozici NEBYLO, my musíme zachovat hada stále stejně dlouhého.
                    # Nahoře jsme mu před chvílí přidali hlavičku. Tady dole mu z konce seznamu (ocásku) 
                    # jeden prvek odebereme (pomocí .pop()), takže vlastně provedl POHYB A JE STÁLE STEJNĚ DLOUHÝ.
                    had_telo.pop()

                # --- SMRTELNÉ NÁRAZY (Stěna a Sebevražda) ---

                # Pokud vylétla nová hlava mimo rozměry Okna...
                if (nova_hlava_x < 0 or nova_hlava_x >= SIRKA_OKNA or
                    nova_hlava_y < 0 or nova_hlava_y >= VYSKA_OKNA):
                    konec_hry = True # GAME OVER

                # Nebo pokud had sežral vlastního ocas!
                # for-cyklus "for dilek in had_telo[1:]" prohlédne VŠE kromě samotné hlavy (začíná od indexu 1, čili tělo)
                # A pokud se na jedné jediné z těchto pozic těla nachází nově nakreslená hlava, tak had do sebe kousl.
                for dilek in had_telo[1:]:
                    if nova_hlava_x == dilek[0] and nova_hlava_y == dilek[1]:
                        konec_hry = True

            # --- VYKRESLOVÁNÍ (Obarvování monitoru) ---
            okno.fill(CERNA)  # Umytí tabule na černo

            # 1. Jídlo (Čtverec o rozměrech jedné buňky na mřížce)
            pygame.draw.rect(okno, CERVENA, (jidlo_x, jidlo_y, VELIKOST_DILKU, VELIKOST_DILKU))

            # 2. Celý samotný dlouhý had
            # Projdeme seznam všech buněk a pro každičkou z nich na daném [X, Y] nakreslíme jeden zelený kvádr
            for dilek in had_telo:
                pygame.draw.rect(okno, ZELENA, (dilek[0], dilek[1], VELIKOST_DILKU, VELIKOST_DILKU))

            zobraz_text(f"Skóre: {skore}", BILA, 10, 10)

            if konec_hry:
                # Zásadní hláška uprostřed pole o tom, ať to zkusí hráč znovu.
                zobraz_text("Konec hry! Stiskni MEZERNÍK pro novou hru.", CERVENA, 100, VYSKA_OKNA // 2)

            # Hotový frame se prohazuje s tím na monitoru
            pygame.display.flip()  

            # Omezení rychlosti
            hodiny.tick(FPS)
            # PRIDANO PRO WEB
            await asyncio.sleep(0)

# Úplný spodek skriptu Pythonu
    # Tento 'if' ověřuje, jestli Python zapnul tento soubor napřímo jako první.
    if __name__ == "__main__":

        # NEKONEČNÁ SLUČKA ŽIVOTA. 
        # Jakmile uvnitř `hlavni_smycka` zavoláme 'return' kvůli Game Over + stisku Mezerníku, 
        # funkce se zničí, a tento while True ji opět vzkřísí z prachu k novému životu s čistým listem skóre.
        while True:
            await hlavni_smycka()


# PŘIDÁNO PRO WEB: Spuštění asynchronní hry
asyncio.run(main())