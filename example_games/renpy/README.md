# Ren'Py: Tvorba Vizuálních Novel

Vítejte u příkladů pro Ren'Py! Ren'Py je oblíbený nástroj (engine) pro tvorbu vizuálních novel (VN) a her založených na příběhu. Používá jednoduchý skriptovací jazyk založený na Pythonu.

Tato složka obsahuje tři příklady, které vás provedou od úplných základů až po pokročilejší funkce.

## Jak začít
1. Stáhněte si Ren'Py z [oficiálních stránek](https://www.renpy.org/).
2. Otevřete Ren'Py Launcher.
3. V nastavení (Preferences) nastavte "Projects Directory" na složku, ve které se nacházíte (`C:\gitprojekty_skola\python_gamejam_examples\renpy`).
4. V levém menu uvidíte projekty `renpy_example_01`, `renpy_example_02` a `renpy_example_03`.
5. Klikněte na projekt a zvolte "Launch Project" (Spustit projekt) pro hraní. Pro úpravu kódu zvolte "script.rpy" v sekci "Edit File".

---

## 📖 Příklad 1: Základy (renpy_example_01)
Tento příklad ukazuje naprosté základy tvorby příběhu.
- **Definice postav:** Jak vytvořit postavu, která mluví určitou barvou.
- **Změna pozadí:** Jak přepínat scény pomocí příkazu `scene`.
- **Dialogy:** Jak nechat postavy mluvit.
- **Přechody (Transitions):** Použití `with fade` (zatmívání) a `with dissolve` (prolínání).

## 🔀 Příklad 2: Volby a proměnné (renpy_example_02)
Ve hrách je klíčové, aby hráč mohl ovlivňovat děj!
- **Menu:** Tvorba interaktivních voleb (tlačítek).
- **Proměnné:** Jak si hra pamatuje, co hráč udělal (např. `$ ma_mec = True`).
- **Podmínky (if/else):** Jak se příběh větví na základě předchozích rozhodnutí.
- **Skákání (jump):** Přesun mezi různými částmi kódu (labely).

## 🚀 Příklad 3: Pokročilé funkce (renpy_example_03)
Pro ty, kteří chtějí jít dál a přidat do hry složitější prvky.
- **Obrazovky (Screens):** Vytvoření vlastního uživatelského rozhraní (např. trvalý ukazatel skóre).
- **Animace (ATL):** Pohybování s obrázky, změna jejich velikosti, rotace nebo průhlednosti.
- **Python bloky (`python:`):** Vložení klasického Python kódu pro složitější matematiku, náhodná čísla nebo logiku miniher.

---

### Užitečné tipy pro GameJam
- **Média:** Ren'Py umí přehrávat hudbu (`play music "hudba.ogg"`) i zvuky (`play sound "klik.ogg"`). Média ukládejte do složek `audio/` a `images/` uvnitř složky `game/`.
- **Obrázky:** Stačí vložit obrázek (např. `les.jpg`) do složky `images/` a Ren'Py ho automaticky rozpozná a umožní vám napsat `scene les`.
- **Chyby:** Pokud uděláte v kódu chybu, Ren'Py vám ukáže šedou obrazovku s informacemi o tom, na kterém řádku chyba nastala. Často jde jen o chybějící dvojtečku nebo špatné odsazení!
