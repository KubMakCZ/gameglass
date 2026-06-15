# Definice postav
define p = Character("Průvodce", color="#9b59b6")

# Ukázka ATL (Animation and Transformation Language)
# Tato transformace s objektem hýbe a mění jeho průhlednost
transform pohyb_a_zmizeni:
    xalign 0.1 yalign 0.5
    linear 2.0 xalign 0.9 # Přesun zleva doprava za 2 sekundy
    pause 0.5
    linear 1.0 alpha 0.0 # Zmizení za 1 sekundu

transform skakani:
    alpha 1.0
    xalign 0.5
    yalign 0.5
    easein 0.2 yalign 0.4
    easeout 0.2 yalign 0.5
    repeat

# Ukázka vlastní obrazovky (Screen)
screen ukazatel_skore():
    frame:
        xalign 0.95 yalign 0.05
        vbox:
            text "Skóre: [hrac_skore]" size 30 color "#fff"

image bg vesmir = Solid("#000022")
image hvezda = Solid("#FFFF00", xysize=(50, 50)) # Zástupný obrázek hvězdy

# Proměnná pro Python blok
default hrac_skore = 0

label start:
    scene bg vesmir
    
    # Zobrazení vlastní obrazovky
    show screen ukazatel_skore
    
    p "Vítej v pokročilém tutoriálu!"
    
    # Ukázka Python bloku pro složitější logiku
    python:
        # Můžeme psát čistý Python kód
        import random
        nahodne_cislo = random.randint(10, 50)
        hrac_skore += nahodne_cislo
        
    p "Díky Pythonu jsme ti právě náhodně přidali [nahodne_cislo] bodů!"
    
    p "Nyní si ukážeme animace pomocí ATL."
    
    # Zobrazení obrázku s aplikací transformace
    show hvezda at pohyb_a_zmizeni
    
    p "Tato hvězda se přesune přes obrazovku a pak zmizí."
    
    # Počkáme na dokončení animace (3.5s)
    pause 3.5
    
    p "A teď něco skákavého!"
    
    show hvezda at skakani
    
    p "Tohle je transformace, která se neustále opakuje."
    
    p "To je z pokročilých funkcí vše. Můžeš vytvářet minihry, inventáře a mnohem víc!"
    
    # Skrytí obrazovky
    hide screen ukazatel_skore
    
    return
