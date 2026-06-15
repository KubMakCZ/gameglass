import pygame
import asyncio  # PŘIDÁNO PRO WEB: importujeme asyncio pro neblokující smyčku
import sys
import random

# Inicializace knihovny Pygame - povinný krok. Nastaví všechny podmoduly zvuků, kreslení atd.
async def main():  # PŘIDÁNO PRO WEB: Zabalíme celou hru do asynchronní funkce
    pygame.init()

    # --- Nastavení herního okna ---
    SIRKA = 800
    VYSKA = 600
    # Vytvoření hlavního okna hry o dané velikosti v pixelech (obrazových bodech)
    okno = pygame.display.set_mode((SIRKA, VYSKA))
    # Přidáme název hry do horní lišty softwarového okna
    pygame.display.set_caption("Chytání jablek")

    # --- Paleta barev ---
    # Barvy zadáváme přes číselné hodnoty Červené, Zelené a Modré - RGB (Red, Green, Blue)
    CERNA = (0, 0, 0)      # Černá je absence všech barev
    ZELENA = (0, 255, 0)   # Barva hráče (košíku)
    CERVENA = (255, 0, 0)  # Barva padajícího jablka
    BILA = (255, 255, 255) # Použijeme pro texty

    # Vytvoření objektu 'Clock', který řídí rychlost, aby hra nejela super rychle na výkonných PC
    hodiny = pygame.time.Clock()

    # Tvorba "fontu" neboli stylu písma pro vypisování skóre atd.
    font = pygame.font.SysFont("Arial", 36)

    # --- Proměnné Hráče (Zelený Košík dole) ---
    hrac_sirka = 100
    hrac_vyska = 20
    # Kde bude stát na začátku? X=vodorovně (uprostřed mínus půlka hráče), Y=svisle (úplně dole)
    hrac_x = SIRKA // 2 - hrac_sirka // 2
    hrac_y = VYSKA - 40
    # Rychlost hráče říká, o kolik pixelů se posune, když drží šipku
    rychlost_hrace = 8

    # --- Proměnné Jablka (Červený čtvereček shora) ---
    jablko_velikost = 30
    # Vybereme mu náhodnou souřadnici X kdekoliv od okraje do okraje
    jablko_x = random.randint(0, SIRKA - jablko_velikost)
    # Y mu dáme do ZÁPORNÝCH HODNOT! To znamená, že začíná nahoře schovaný mimo obrazovku!
    jablko_y = -jablko_velikost
    rychlost_jablka = 5 # Jak rychle jablko letí dolů?

    # Herní statistiky
    skore = 0
    zivoty = 3

    # Pravdivostní proměnná (boolean) udávající, že aplikace běží.
    bezime = True

    # ==========================================
    # HLAVNÍ HERNÍ SMYČKA (GAME LOOP)
    # Vše, co se děje ve hře se opakuje zde, zhruba 60x za vteřinu
    # ==========================================
    while bezime:

        # 1. ČTENÍ UDÁLOSTÍ
        # Kontrolujeme, co uživatel dělá - například zda nechce program zavřít
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                bezime = False # Když klikne na křížek, ukončíme smyčku tím, že z 'bezime' uděláme False

        # Hra se fyzicky hraje jenom dokud máme nějaké životy
        if zivoty > 0:

            # 2. LOGIKA HRÁČE: Čteme stisknutí kláves v reálném čase
            # pygame.key.get_pressed() vrací obrovský seznam s hodnotami True nebo False u VŠECH tlačítek na klávesnici
            klavesy = pygame.key.get_pressed()

            # Pokud drží levou šipku a navíc ještě nenarazil do levé zdi (x > 0)
            if klavesy[pygame.K_LEFT] and hrac_x > 0:
                hrac_x -= rychlost_hrace # Posuneme ho doleva (odečteme x)

            # Pokud drží pravou šipku a nenarazil do pravé zdi (Zde musíme odečíst šířku postavy, abychom měřili od kraje)
            if klavesy[pygame.K_RIGHT] and hrac_x < SIRKA - hrac_sirka:
                hrac_x += rychlost_hrace # Posuneme ho doprava (přičteme x)

            # 3. LOGIKA PADÁNÍ JABLKA
            # Osa Y jde v počítačové grafice "shora dolů", takže se zvyšující se Y jablko padá níže
            jablko_y += rychlost_jablka

            # --- KOLIZE (Dotyk hráče s jablkem) ---
            # Abychom snadno zjistili, jestli se dotýkají, "obalíme" je virtuálními obdélníky (Rect)
            hrac_rect = pygame.Rect(hrac_x, hrac_y, hrac_sirka, hrac_vyska)
            jablko_rect = pygame.Rect(jablko_x, jablko_y, jablko_velikost, jablko_velikost)

            # Pokud se tyto dva obdélníky protnou/srazí... Hráč ho chytil!
            if hrac_rect.colliderect(jablko_rect):
                skore += 1            # Dáme mu bod
                rychlost_jablka += 0.2 # Mírně hru zrychlíme, ať je to těžší!

                # Vygenerujeme znovu to stejné jablko úplně nahoře na nové X pozici
                jablko_y = -jablko_velikost
                jablko_x = random.randint(0, SIRKA - jablko_velikost)

            # 4. LOGIKA PŘEHLÉDNUTÍ JABLKA
            # Co se stane, když jablko propadne až za spodní hranu obrazovky?
            elif jablko_y > VYSKA:
                zivoty -= 1 # Hráč přišel o život

                # Musíme jablko i přesto respawnovat zpět nahoru, aby hra mohla pokračovat
                jablko_y = -jablko_velikost
                jablko_x = random.randint(0, SIRKA - jablko_velikost)

        # 5. KRESLENÍ VŠEHO NA OBRAZOVKU
        # Každý snímek musíme celé okno zalít černou barvou, jinak by postavička dělala šmouhy, jak se hýbe
        okno.fill(CERNA) 

        # Kreslíme jenom to, co je zrovna relevantní
        if zivoty > 0:
            # Vykreslení obdélníku hráče
            pygame.draw.rect(okno, ZELENA, (hrac_x, hrac_y, hrac_sirka, hrac_vyska))
            # Vykreslení obdélníku jablka
            pygame.draw.rect(okno, CERVENA, (jablko_x, jablko_y, jablko_velikost, jablko_velikost))

            # Převedeme textovou proměnnou (string) do obrázku (surface)
            text_skore = font.render(f"Skóre: {skore}", True, BILA)
            text_zivoty = font.render(f"Životy: {zivoty}", True, BILA)

            # 'Nalepíme' (blit) tyto obrázky textů na plátno (obrazovku)
            okno.blit(text_skore, (10, 10))
            okno.blit(text_zivoty, (SIRKA - 150, 10))

        else:
            # Hráč nemá životy, je KONEC HRY! Kreslíme varovný text doprostřed.
            text_konec = font.render(f"KONEC HRY! Tvé skóre: {skore}", True, CERVENA)
            okno.blit(text_konec, (SIRKA//2 - 180, VYSKA//2))

        # --- FINALIZACE SNÍMKU ---
        # Toto pošle všechny ty připravené obdélníčky a texty z paměti počítače rovnou do monitoru!
        pygame.display.flip()

        # A tohle vynutí pauzu natolik dlouhou, abychom za vteřinu nepřekročili 60 smyček (60 FPS)
        hodiny.tick(60)       
        # PRIDANO PRO WEB
        await asyncio.sleep(0)

# Pokud 'bezime' skočí na False a vyskočíme ze smyčky 'while', musíme bezpečně zhasnout!
    pygame.quit()
    sys.exit()


# PŘIDÁNO PRO WEB: Spuštění asynchronní hry
asyncio.run(main())