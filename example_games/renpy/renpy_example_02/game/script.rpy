# Definice postav
define h = Character("Hrdina", color="#f1c40f")
define s = Character("Stařec", color="#bdc3c7")

# Proměnné pro sledování stavu hry
default ma_mec = False
default zivoty = 3

image bg vesnice = Solid("#8FBC8F")
image bg les = Solid("#228B22")
image bg zamek = Solid("#4B0082")

label start:
    scene bg vesnice
    
    h "Dnes je den, kdy vyrazím na dobrodružství!"
    
    s "Počkej, mladíku! Je nebezpečné jít sám."
    
    # Ukázka menu (volby)
    menu:
        s "Vezmi si s sebou jednu z těchto věcí."
        
        "Vzít si starý meč.":
            $ ma_mec = True
            h "Vezmu si ten meč, bude se hodit."
            s "Dobrá volba. Opatruj se!"
            
        "Odmítnout s díky.":
            h "Ne, děkuji. Zvládnu to sám."
            s "Jak myslíš. Ale buď opatrný."
            
    # Skok na další část příběhu
    jump cesta_lesem

label cesta_lesem:
    scene bg les
    with dissolve
    
    "Cestuješ hlubokým lesem. Najednou na tebe vyskočí zlý vlk!"
    
    # Podmínka (if/else) podle toho, co hráč zvolil
    if ma_mec:
        h "Ha! Mám meč! Těch se nebojím."
        "Použil jsi meč a vlka jsi odehnal."
    else:
        h "Ouha, nemám zbraň! Musím utéct!"
        $ zivoty -= 1
        "Při útěku ses zranil. Zbývají ti [zivoty] životy."
        
        if zivoty <= 0:
            jump konec_hry
            
    "Pokračuješ dál v cestě."
    jump hrad

label hrad:
    scene bg zamek
    with fade
    
    "Konečně jsi dorazil k temnému hradu."
    "Našel jsi spoustu zlata a stal ses hrdinou!"
    
    "Gratulujeme k vítězství!"
    return

label konec_hry:
    "Přišel jsi o všechny životy."
    "GAME OVER"
    return
