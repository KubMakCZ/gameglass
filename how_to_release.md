# 🚀 Jak tvořit "Releases" a Vydávat nové verze na GitHubu

Až v budoucnu naprogramuješ nové funkce (např. účty, podpora Godot enginu, atd.), je dobrým zvykem tyto verze oficiálně oštítkovat a vydat na GitHubu jako tzv. **Release**. Díky tomu si budou moci ostatní učitelé jednoduše stáhnout konkrétní stabilní verzi.

Tento návod ti krok za krokem vysvětlí, jak na to.

---

## 1. Aktualizace čísla verze v kódu
Předtím, než vydáš novou verzi, měl bys nejprve upravit verzi přímo v kódu projektu:
1. Otevři soubor `webapp/package.json`.
2. Změň řádek `"version": "0.1.0"` na novou verzi (např. `"0.2.0"`).
3. Tyto úpravy normálně ulož a pošli na GitHub (`git commit` a `git push`).

*(Verzování se většinou řídí pravidlem: **1.0.0** -> První číslo je masivní překopání projektu, prostřední číslo jsou nové fuknce, a to poslední jsou opravy drobných chyb, tzv. bugfixy).*

---

## 2. Vytvoření "Release" přes webové rozhraní GitHubu
Tohle je ten nejsnazší a nejhezčí způsob, jak aplikaci vydat pro ostatní.

1. Běž na stránku svého repozitáře na webu [GitHub.com](https://github.com/).
2. Na hlavní stránce projektu najdi vpravo na panelu sekci nazvanou **Releases** (bývá pod sekcí About) a klikni na **Create a new release** (případně "Draft a new release").
3. **Choose a tag:** Klikni na tlačítko, napiš název verze např. `v0.1.0` a z nabídky zvol *Create new tag: v0.1.0 on publish*.
4. **Target:** Zkontroluj, že je tam vybraná větev `main`.
5. **Release title:** Napiš něco chytlavého, např. *GameGlass v0.1.0 - První stabilní vydání!* nebo *Aktualizace: Podpora Godot Enginu*.
6. **Popis (Describe this release):** Sem vypiš formou odrážek, co je v této verzi nového. Lidé to rádi čtou!
   - *Příklad:*
     - *Přidána podpora pro Unity.*
     - *Opraven bug s mizejícím košem.*
7. Nakonec úplně dole klikni na velké zelené tlačítko **Publish release**.

Hotovo! 🎊 GitHub nyní tvůj repozitář vezme v přesně aktuálním stavu, zabalí ho do ZIP archivu, nalepí na něj štítek a nabídne ho jako oficiální vydání komukoliv, kdo si projekt najde.

---

## 3. Aktualizace nasazeného projektu (na Proxmoxu)
Jakmile vydáš na GitHubu novou verzi a budeš ji chtít dostat na svůj běžící Proxmox server ve škole, proces je neuvěřitelně lehký díky skriptu, který pro tebe vznikl:

1. Připoj se na svůj školní server, kde ti GameGlass běží.
2. Vstup do složky s projektem (`cd /cesta/ke/gameglass`).
3. Spusť aktualizační skript:
   ```bash
   bash update.sh
   ```
4. Tento skript si naprosto sám "šáhne" na GitHub pro tvoje nové úpravy, zastaví starou verzi webu, nahradí jí tou novou a všechno znovu bezpečně spustí.
