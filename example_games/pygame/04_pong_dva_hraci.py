import pygame
import asyncio  # PŘIDÁNO PRO WEB: importujeme asyncio pro neblokující smyčku
import sys

async def main():  # PŘIDÁNO PRO WEB: Zabalíme celou hru do asynchronní funkce
    # pygame.init() spustí vnitřní motory knihovny Pygame. Bez toho nejde ani otevřít okno.
    pygame.init()

    # --- NASTAVENÍ OKNA ---
    SIRKA = 800
    VYSKA = 600
    # Okno upevníme na tyto rozměry
    okno = pygame.display.set_mode((SIRKA, VYSKA))
    pygame.display.set_caption("Pong - Plná Hra pro dva hráče")

    # --- BARVY ---
    BILA = (255, 255, 255)
    CERNA = (0, 0, 0)
    ZELENA = (0, 255, 0)

    # Herní hodiny omezují, aby náš počítač nehrál 1000x za vteřinu, čímž by hra byla nehratelná.
    hodiny = pygame.time.Clock()

    # Tvorba písem (pro vykreslování textu potřebujeme vždy nastavit velikost a typ písma)
    font_velky = pygame.font.SysFont("Arial", 50)
    font_maly = pygame.font.SysFont("Arial", 30)

    # --- STAVOVÝ AUTOMAT (State Machine) ---
    # Trik profesionálů: Hra je vždy v nějakém "Stavu" (Menu, Hra, Konec). 
    # Podle tohoto čísla pak naše hlavní smyčka pozná, jaké má platit rozvržení obrazovky a pravidla.
    STAV_MENU = 0
    STAV_HRA = 1
    STAV_KONEC = 2
    stav = STAV_MENU # Začínáme logicky v hlavním menu

    # --- PROMĚNNÉ HRÁČŮ (Pálky) A MÍČKU ---
    palka_sirka = 15
    palka_vyska = 100
    rychlost_palky = 7
    micek_velikost = 15

    # Funkce, která vrátí všechny proměnné na začátek. Použije se po gólu nebo při startu nové hry.
    def reset_hry():
        # Klíčové slovo 'global' musíme použít vždycky, když uvnitř Funkce chceme MĚNIT proměnnou,
        # která byla vytvořena venku (na nejvyšší úrovni skriptu).
        global hrac1_y, hrac2_y, skore1, skore2, micek_x, micek_y, micek_rychlost_x, micek_rychlost_y

        # Hráče zarovnáme na střed Y osy (Výška okna / 2 - polovina velikosti hráče)
        hrac1_y = VYSKA // 2 - palka_vyska // 2
        hrac2_y = VYSKA // 2 - palka_vyska // 2
        skore1 = 0
        skore2 = 0

        # Míček přesně doprostřed obou os X a Y
        micek_x = SIRKA // 2 - micek_velikost // 2
        micek_y = VYSKA // 2 - micek_velikost // 2

        # Míček poletí rychlostí 5 bodů za snímek šikmo dolů doprava
        micek_rychlost_x = 5
        micek_rychlost_y = 5

    # Okamžitě to zavoláme, abychom proměnným výše vložili výchozí čísla hned při spuštění programu
    reset_hry() 

    bezime = True
    # Hlavní cyklus hry, který točí snímek za snímkem donekonečna, dokud aplikaci neukončíme.
    while bezime:

        # 1. ZPRACOVÁNÍ UDÁLOSTÍ
        # Procházíme např. stisky tlačítek myši, křížek pro zavření okna, jedno-stisky kláves
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                bezime = False # Ukončíme while-cyklus

            # Zjišťujeme, zda se NESTISKNULA klávesa. Tohle se provede jen JEDNOU, i když ji uživatel drží!
            if udalost.type == pygame.KEYDOWN:
                if stav == STAV_MENU and udalost.key == pygame.K_SPACE:
                    # Jsme v menu, hráč stiskl MEZERNÍK. Přepneme hru do režimu STAV_HRA!
                    stav = STAV_HRA 
                elif stav == STAV_KONEC and udalost.key == pygame.K_SPACE:
                    # Jsme na obrazovce s vítězem, hráč chce hrát znovu.
                    reset_hry()     
                    stav = STAV_HRA

        # Oproti tomu toto zjistí AKTUÁLNĚ DRŽENÉ klávesy v tomto zlomku vteřiny
        klavesy = pygame.key.get_pressed()

        # 2. HERNÍ LOGIKA (HÝBÁNÍ SE)
        # Tohle se provede JEN a POUZE, pokud zrovna hrajeme zápas!
        if stav == STAV_HRA:
            # Ovládání Hráče 1 vlevo (Klávesy W a S pro pohyb nahoru/dolů)
            if klavesy[pygame.K_w] and hrac1_y > 0:
                hrac1_y -= rychlost_palky
            # Dolů nemůže víc, než je výška okna zmenšená o jeho vlastní výšku pálky
            if klavesy[pygame.K_s] and hrac1_y < VYSKA - palka_vyska:
                hrac1_y += rychlost_palky

            # Ovládání Hráče 2 vpravo (Šipky Nahoru a Dolů)
            if klavesy[pygame.K_UP] and hrac2_y > 0:
                hrac2_y -= rychlost_palky
            if klavesy[pygame.K_DOWN] and hrac2_y < VYSKA - palka_vyska:
                hrac2_y += rychlost_palky

            # Míček se za každou smyčku kousek posune. Tím vzniká dojem pohybu.
            micek_x += micek_rychlost_x
            micek_y += micek_rychlost_y

            # --- Fyzika: Odraz míčku od stropu a podlahy ---
            # Trik: Vynásobením rychlosti číslem -1 se obrátí znaménko. 
            # Z kladné rychlosti (+5 padá dolů) se stane záporná (-5 letí nahoru). Odrazil se!
            if micek_y <= 0 or micek_y >= VYSKA - micek_velikost:
                micek_rychlost_y *= -1

            # --- Fyzika: Odraz od pálek hráčů ---
            # Abychom to jednoduše spočítali, vyrobíme si takzvané virtuální Obdélníky (Rect)
            rect_micek = pygame.Rect(micek_x, micek_y, micek_velikost, micek_velikost)

            # Pálku Hráče 1 vykreslujeme fixně 30 pixelů od levého okraje
            rect_hrac1 = pygame.Rect(30, hrac1_y, palka_sirka, palka_vyska)
            # Pálku Hráče 2 fixně na pravé straně. (SIRKA - 30 od kraje - velikost pálky)
            rect_hrac2 = pygame.Rect(SIRKA - 30 - palka_sirka, hrac2_y, palka_sirka, palka_vyska)

            # Metoda 'colliderect' doslova zkoumá, jestli se tyto obdélníky v daný moment nepřekrývají
            if rect_micek.colliderect(rect_hrac1) or rect_micek.colliderect(rect_hrac2):
                # Odrazil se od pálky! Obrátíme jeho směr po ose X a ještě ho mírně zrychlíme (* -1.1)
                micek_rychlost_x *= -1.1 

            # --- Vyhodnocení Gólu ---
            if micek_x < 0:
                # Přeletěl za levý okraj (Hráč 1 ho nezachytil). Bod pro Hráče 2!
                skore2 += 1 
                micek_x, micek_y = SIRKA // 2, VYSKA // 2 # Teleportace míčku na prostředek
                micek_rychlost_x = 5 # Reset rychlosti a ať letí k hráči co dostal gól (doprava)
            elif micek_x > SIRKA:
                # Přeletěl vpravo
                skore1 += 1 
                micek_x, micek_y = SIRKA // 2, VYSKA // 2
                micek_rychlost_x = -5 # Směr letu doleva

            # --- Konec Zápasu ---
            # Zápas končí, jakmile někdo dosáhne 5 bodů
            if skore1 >= 5 or skore2 >= 5:
                stav = STAV_KONEC

        # 3. KRESLENÍ GRAFIKY
        # Vždy smažeme starou stopu vyplněním okna čistě černou barvou
        okno.fill(CERNA)

        # Co na obrazovce bude záleží zcela na tom, ve kterém STAVU náš Stavový Automat právě je!
        if stav == STAV_MENU:
            # Vykreslení Menu. .render převede nápis z textu do "razítka"
            nadpis = font_velky.render("PONG", True, BILA)
            navod = font_maly.render("Stiskni MEZERNÍK pro start", True, ZELENA)

            # Tyto razítka .blitnem (otiskneme) na plátno. Výpočet (SIRKA//2 - nadpis.get_width()//2) zarovná nápis čistě doprostřed obrazovky.
            okno.blit(nadpis, (SIRKA//2 - nadpis.get_width()//2, 200))
            okno.blit(navod, (SIRKA//2 - navod.get_width()//2, 300))

        elif stav == STAV_HRA:
            # Jsme ve hře. Vykreslíme půlící čáru (síť v Pongu). 'aaline' je hladká čára.
            pygame.draw.aaline(okno, BILA, (SIRKA // 2, 0), (SIRKA // 2, VYSKA))

            # Nakreslíme pálky na místa, která předtím logika vypočítala
            pygame.draw.rect(okno, BILA, rect_hrac1)
            pygame.draw.rect(okno, BILA, rect_hrac2)

            # Míček vykreslíme jako 'ellipsu' napasovanou na ten neviditelný 'rect_micek' obdélník. Vznikne tak kruh.
            pygame.draw.ellipse(okno, BILA, rect_micek) 

            # Kreslení obou skóre úplně nahoru
            text_skore = font_velky.render(f"{skore1}   {skore2}", True, BILA)
            okno.blit(text_skore, (SIRKA // 2 - text_skore.get_width() // 2, 20))

        elif stav == STAV_KONEC:
            # Zjištění, kdo vyhrál pomocí tzv. ternárního if (vítězem je "Hráč 1" POKUD má skore1>=5, JINAK je to "Hráč 2")
            vitez = "Hráč 1" if skore1 >= 5 else "Hráč 2"

            # Razítka s nápisy
            text_vitez = font_velky.render(f"{vitez} vyhrál!", True, ZELENA)
            text_restart = font_maly.render("Stiskni MEZERNÍK pro novou hru", True, BILA)

            # Obtisknutí doprostřed okna
            okno.blit(text_vitez, (SIRKA//2 - text_vitez.get_width()//2, 200))
            okno.blit(text_restart, (SIRKA//2 - text_restart.get_width()//2, 300))

        # Obraz je složený nanečisto v paměti. .flip() ho teprve natvrdo pošle na monitor!
        pygame.display.flip()

        # Pauza na udržení stabilních 60 FPS
        hodiny.tick(60)
        # PRIDANO PRO WEB
        await asyncio.sleep(0)

# Konec programu
    pygame.quit()
    sys.exit()


# PŘIDÁNO PRO WEB: Spuštění asynchronní hry
asyncio.run(main())