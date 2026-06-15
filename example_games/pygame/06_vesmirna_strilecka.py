import pygame
import asyncio  # PŘIDÁNO PRO WEB: importujeme asyncio pro neblokující smyčku
import sys
import random

async def main():  # PŘIDÁNO PRO WEB: Zabalíme celou hru do asynchronní funkce
    pygame.init()

    # --- NASTAVENÍ OKNA ---
    SIRKA = 800
    VYSKA = 600
    okno = pygame.display.set_mode((SIRKA, VYSKA))
    pygame.display.set_caption("Vesmírná střílečka (Space Invaders)")

    # --- BARVY ---
    CERNA = (0, 0, 0)
    ZELENA = (0, 255, 0)   # Hráč (Vesmírná loď)
    CERVENA = (255, 0, 0)  # Nepřátelé (Mimozemšťani, Meteority)
    ZLUCA = (255, 255, 0)  # Projektily (Lasery)
    BILA = (255, 255, 255) # Text a UI

    hodiny = pygame.time.Clock()
    font_velky = pygame.font.SysFont("Arial", 50)
    font_maly = pygame.font.SysFont("Arial", 30)

    # Herní stav 0,1,2 - stejná logika oddělení úvodního menu od zápasu
    STAV_MENU = 0
    STAV_HRA = 1
    STAV_KONEC = 2
    stav = STAV_MENU

    # Rozměry vesmírné lodi hráče
    hrac_sirka = 40
    hrac_vyska = 40
    rychlost_hrace = 6
    rychlost_projektilu = 10 # Lasery létají celkem svižně nahoru

    # Vytvoření vlastního časovače pro přidávání nepřátel, viz skákačka
    SPAWN_NEPRITELE = pygame.USEREVENT + 1

    def reset_hry():
        """Tato funkce srovná hru zpátky do prvního dne, když spustíme reset"""
        global hrac_x, hrac_y, projektily, nepratele, skore, rychlost_nepritele, spawn_cas

        # Hráč je dole nad hranou obrazovky
        hrac_x = SIRKA // 2 - hrac_sirka // 2
        hrac_y = VYSKA - 60

        # Budou zde létat nezávisle na sobě desítky kulek i nepřátel.
        # Abychom se v nich vyznali, naženeme je všechny do SEZNAMŮ.
        projektily = [] 
        nepratele = []  

        skore = 0
        rychlost_nepritele = 2.0
        spawn_cas = 1000 # Počáteční čas (v milisekundách) k objevování padajících mimozemšťanů 

        # Nastartování naší události (eventu), začne tikat...
        pygame.time.set_timer(SPAWN_NEPRITELE, spawn_cas)

    reset_hry()

    bezime = True
    while bezime:
        # 1. ZPRACOVÁNÍ UDÁLOSTÍ
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                bezime = False

            # Zjišťujeme JEDNORÁZOVÉ stisknutí tlačítek. Například výstřel nebo posun v menu.
            if udalost.type == pygame.KEYDOWN:
                if stav == STAV_MENU and udalost.key == pygame.K_SPACE:
                    stav = STAV_HRA
                elif stav == STAV_KONEC and udalost.key == pygame.K_SPACE:
                    reset_hry()
                    stav = STAV_HRA
                elif stav == STAV_HRA and udalost.key == pygame.K_SPACE:
                    # --- VÝSTŘEL ---
                    # Hráč právě odpálil! Vypočítáme, kde zhruba leží střed jeho lodi (špička křídel)
                    projektil_x = hrac_x + hrac_sirka // 2 - 5
                    # A přímo na těchto souřadnicích se narodí nová "KULKA" v podobě Rect. Přidáme do listu.
                    projektily.append(pygame.Rect(projektil_x, hrac_y, 10, 20))

            # Zde časovač zakřičel (třeba každou sekundu), že na nás padá další nepřítel
            if udalost.type == SPAWN_NEPRITELE and stav == STAV_HRA:
                # Narodil se nový nepřítel nahoře mimo obraz (proto je osa y záporná: -40) na náhodném místě osy X.
                n_x = random.randint(0, SIRKA - 40)
                nepratele.append(pygame.Rect(n_x, -40, 40, 40))

                # STUPŇOVÁNÍ OBTÍŽNOSTI (Nepřátelé padají čím dál rychleji)
                rychlost_nepritele += 0.05

                # Čím déle hrajeme, tím se také zkracuje ten časovač a nepřátel je hustší roj.
                # Omezíme to na min 300ms, aby ta hra byla alespoň fyzicky dohratelná a nepřátelé nespadli z jednolité zdi.
                if spawn_cas > 300: 
                    spawn_cas -= 20 
                    # Musíme časovač s tímto novým o 20ms kratším časem znovu "nastartovat"
                    pygame.time.set_timer(SPAWN_NEPRITELE, spawn_cas)

        if stav == STAV_HRA:
            # 2. LOGIKA

            # Ovládání vesmírné lodi doprava a doleva držením tlačítek
            klavesy = pygame.key.get_pressed()
            if klavesy[pygame.K_LEFT] and hrac_x > 0:
                hrac_x -= rychlost_hrace
            if klavesy[pygame.K_RIGHT] and hrac_x < SIRKA - hrac_sirka:
                hrac_x += rychlost_hrace

            # --- POHYB VŠECH LASERŮ (KULEK) ---
            # Projektily[:] dělá kopii listu, to se musí dělat vždy, když chci za běhu for-cyklu z toho pole
            # věci rovnou odstraňovat! Kdybychom neodstraňovali kulky, list by narostl a hra spadla na paměť.
            for p in projektily[:]: 
                p.y -= rychlost_projektilu # Y se ZMENŠUJE, protože kulka cestuje odspodu (např. Y=500) nahoru (Y=0)

                # Když kulka odcestuje nad okraj obrazovky do hlubin kosmu, smažeme ji
                if p.y < 0: projektily.remove(p)

            # Hráč samotný obalený do neviditelného Rect rámečku pro vyhodnocování havárií
            hrac_rect = pygame.Rect(hrac_x, hrac_y, hrac_sirka, hrac_vyska)

            # --- POHYB VŠECH NEPŘÁTEL & KOLIZE ---
            for n in nepratele[:]:
                n.y += int(rychlost_nepritele) # Zvyšujeme Y -> Meteorit letí strmě dolů z nebes k podlaze

                # 1. Havárie! Pokud meteorit doletí až úplně dolů přes obrazovku, NEBO narazí do Hráče
                if n.y > VYSKA or n.colliderect(hrac_rect):
                    stav = STAV_KONEC

                # 2. Křížová kontrola, zda SE STŘETLA KULKA S NEPŘÍTELEM (Laser do Meteoritu)
                # Každého meteorita porovnáme znovu se všemi létajícími lasery na scéně! 
                for p in projektily[:]:
                    # .colliderect znamená "prolnuly se tyhle dva čtverce?"
                    if p.colliderect(n):
                        # BUM! Nastal obrovský výbuch. 
                        # Zmizí Laser i Meteorit, tak je oba bezpečně (jen pokud už nebyli smazáni) vymažeme
                        if p in projektily: projektily.remove(p)
                        if n in nepratele: nepratele.remove(n)
                        skore += 10 # +10 bodů do kasičky!

                        # SLOVO 'break' ZMRAZÍ TENTO VNITŘNÍ FOR CYKLUS!
                        # Má to logiku - Pokud tento Nepřítel 'n' byl teď vteřinu zničen, už nedává smysl dál
                        # v tomto mikrosnímku procházet zbylé kulky a ptát se, jestli ho střelily taky. Přerušíme to.
                        break 

        # 3. KRESLENÍ GRAFIKY
        okno.fill(CERNA)

        if stav == STAV_MENU:
            text = font_velky.render("VESMÍRNÁ STŘÍLEČKA", True, ZLUCA)
            start = font_maly.render("Stiskni MEZERNÍK. Střílíš mezerníkem, pohyb šipkami.", True, BILA)
            okno.blit(text, (SIRKA//2 - text.get_width()//2, 200))
            okno.blit(start, (SIRKA//2 - start.get_width()//2, 300))

        elif stav == STAV_HRA:
            # Jsme ve hře! Nyní se z paměti převedou čísla Rect rámečků do reálných obrazců na monitoru.

            # Naše loď
            pygame.draw.rect(okno, ZELENA, hrac_rect) 

            # Smyčka vykreslí všechny Lasery co jsou aktuálně ve vzduchu
            for p in projektily: 
                pygame.draw.rect(okno, ZLUCA, p) 

            # Ta samá smyčka vykreslí pluky všech padajících Nepřátel
            for n in nepratele: 
                pygame.draw.rect(okno, CERVENA, n) 

            # Zobrazení skóre
            skore_text = font_maly.render(f"Skóre: {skore}", True, BILA)
            okno.blit(skore_text, (10, 10))

        elif stav == STAV_KONEC:
            text = font_velky.render("ZEMŘEL JSI!", True, CERVENA)
            skore_text = font_velky.render(f"Tvé skóre: {skore}", True, BILA)
            restart = font_maly.render("Stiskni MEZERNÍK pro novou hru", True, ZLUCA)

            okno.blit(text, (SIRKA//2 - text.get_width()//2, 150))
            okno.blit(skore_text, (SIRKA//2 - skore_text.get_width()//2, 250))
            okno.blit(restart, (SIRKA//2 - restart.get_width()//2, 350))

        # Obraz je spočítán. Posíláme do HDMI portu na monitor! (.flip)
        pygame.display.flip()
        hodiny.tick(60)
        # PRIDANO PRO WEB
        await asyncio.sleep(0)

pygame.quit()
    sys.exit()


# PŘIDÁNO PRO WEB: Spuštění asynchronní hry
asyncio.run(main())