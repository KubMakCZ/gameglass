# Pygame: Herní Engine v Pythonu

Vítejte v sekci ukázek pro Pygame! Tato knihovna tvoří absolutní standard pro tvorbu jednoduchých, výkonných 2D her v Pythonu. Oproti klasickým konzolovým skriptům je v Pygame výjimečná jedna věc: používá se zde **Herní Smyčka (Game Loop)**.

Cílem této série příkladů je poskytnout vám ucelené komentované vzory od úplných základů až po složitější arkády. Všechny příklady byly bohatě okomentovány, aby si začínající tvůrci z řad středoškoláků a začátečníků dokázali propojit teorii s praxí.

## Kostra Pygame programu
Každý, i ten nejsložitější program v Pygame, stojí na nepsaných 4 pilířích, které se odehrávají ve nekonečném cyklu zvaném _Herní smyčka_:

```python
import pygame
pygame.init() # Zapnutí modulů (NUTNOST)

# 0. PŘÍPRAVA (Jednou před hrou)
okno = pygame.display.set_mode((800, 600))
hodiny = pygame.time.Clock()

bezime = True
while bezime: # TOTO JE HERNÍ SMYČKA, TOČÍ SE 60x ZA VTEŘINU
    
    # 1. ZPRACOVÁNÍ UDÁLOSTÍ (Event Handling)
    # Tady čteme, jestli hráč nestiskl klávesu, myš, nebo nezavírá okno
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            bezime = False
            
    # 2. HERNÍ LOGIKA (Game Logic)
    # Zde počítáme fyziku. Pokud loď letí, přičítáme XY. Pokud narazila do zdi, končíme hru atd.
    # Tady se dělají všechny ty super výpočty a matematika v pozadí.
    
    # 3. KRESLENÍ GRAFIKY (Render)
    # Nejdříve smažeme to, co bylo v předchozím milisekundovém kroku namalované
    okno.fill((0, 0, 0)) # Černá
    # Teď z vypočítaných čísel namalujeme obdélníčky, kolečka nebo obrázky postav.
    
    # 4. AKTUALIZACE OBRAZOVKY (Flip)
    # Naší monitor o ničem z kroku 3 neví, dokud nezavoláme tuto finální klíčovou metodu, 
    # která vezme obraz z mezipaměti procesoru a mrskne jím do vaší obrazovky.
    pygame.display.flip()
    
    # Kontrola na 60 FPS (snímků za vteřinu)
    hodiny.tick(60)

pygame.quit() # Korektní vypnutí
```

## Co se zde nachází
Všechny zdrojové kódy v této složce jsou plně hratelné, připravené k tomu, abyste v nich upravovali gravitaci, rychlost, nebo tvary!

1. **`01_pexeso.py`** – Hra testující vaši paměť na barvy. Ideální příklad použití myši, "polí v polích" a takzvaného Objektově Orientovaného Programování. Každá karta si žije vlastním životem!
2. **`02_flappy_bird.py`** – Prototyp populární hry. Ukazuje jak naprogramovat "Stavový automat" (hra ví, jestli je v Menu nebo už se bojuje o život), kolize, generování nekonečných překážek a simulaci gravitace.
3. **`03_chytani_jablek.py`** – Zlatý standard. Chytání padajících předmětů pomocí pohybu zleva doprava a počítání skóre. Krásně ukazuje detekce kolizí (`.colliderect()`).
4. **`04_pong_dva_hraci.py`** – Klasika pro dva lidi u jedné klávesnice s míčkem. Je to čistá ukázka odrazové fyziky, měnění směru střely podle úhlů nárazu.
5. **`05_skakacka_gravitace.py`** – Modelová hra se skoky typu Dinosaur z Google Chrome při nefungujícím internetu.
6. **`06_vesmirna_strilecka.py`** – Znič nepřátele, co ti padají na hlavu, a nesmíš se s nimi srazit. Skvělý příklad pro správu seznamů desítek nezávislých střel a meteorů v RAM paměti!
7. **`07_had.py`** – Klasický had z mobilních telefonů. Geniální příklad, kde se neuvažuje v pixelech, ale v jakési teoretické matematické mřížce. Had tu roste díky posunům celých seznamů!

Přejeme vám ohromnou zábavu s Pygame! S těmito dovednostmi je už opravdu jen krůček k vašemu vlastnímu obřímu RPG!
