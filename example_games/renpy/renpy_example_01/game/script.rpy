# Definice postav (jméno a barva textu)
define k = Character("Karel", color="#3498db")
define p = Character("Petra", color="#e74c3c")
define v = Character("Vypravěč", color="#95a5a6")
define b = Character("Boss", color="#ff0000")

# Zástupné obrázky pro pozadí (hrad nahradíme skutečnou mapou ze složky 'images')
image bg les = Solid("#228B22") # Zelená barva jako les
image bg jeskyně = Solid("#696969") # Šedá barva jako jeskyně

# Hra začíná zde
label start:

    # Zobrazí pozadí lesa
    scene bg les
    with fade

    v "Byl krásný slunečný den a Karel se rozhodl jít na procházku do lesa."
    
    k "Dnes je opravdu nádherně. Možná najdu nějaké houby."
    
    v "Najednou uslyšel zapraskání větviček."
    
    p "Ahoj Karle! Co tady děláš?"
    
    k "Petro! Ty jsi mě vyděsila. Jen se tu procházím."
    
    p "Slyšela jsem, že v nedaleké jeskyni je ukrytý poklad. Půjdeme se podívat?"
    
    k "Zní to nebezpečně, ale proč ne."

    # Přesun do jeskyně
    scene bg jeskyně
    with dissolve

    v "Karel a Petra dorazili k temné jeskyni."
    
    k "Tady je hrozná tma. Nevidím na krok."
    
    p "Neboj se, mám baterku. Podívej, tamhle něco svítí!"
    
    v "V rohu jeskyně našli starou kouzelnou mapu."
    
    k "To je nádherná mapa celého kraje! A je na ní vyznačený poklad!"

    # Zobrazíme naši novou mapu ze složky images
    scene bg_mapa
    with fade

    v "Mapa se před nimi rozvinula v celé své kráse. V tu chvíli se ale zničehonic objevil mocný strážce!"
    
    # Pomocí bloku můžeme obrázek zmenšit a vycentrovat
    show boss:
        zoom 0.25
        xalign 0.5
        yalign 0.5
    with dissolve

    b "MUAHAHA! Já jsem Boss! A tahle mapa patří mně!"
    
    p "Páni, to je ale hrozivý nepřítel. Vypadá jako... nějaký temný stín!"
    
    k "Neboj se Petro! Utíkámeee!"
    
    hide boss
    with fade
    
    v "Karel a Petra sice nenašli poklad, ale odnesli si zážitek na celý život. A přízrak dál stráží svou mapu."

    # Konec hry
    return
