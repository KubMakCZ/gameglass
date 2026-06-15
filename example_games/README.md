# 🎮 Python Game Jam - Průvodce, Ukázky a Zdroje

Vítejte v hlavním repozitáři pro **Python Game Jam**! Tento repozitář obsahuje vše, co potřebujete do začátku. Najdete zde ukázky kódu, tipy a triky, jak pracovat s různými herními frameworky v Pythonu. 

*(Poznámka: Samotné zadání a pravidla najdete v souboru `ZADANI_GAME_JAM.md`, který už máte na Moodle.)*

---

## 📂 Co v repozitáři najdete?

*   📁 **`pygame/`** - Obsahuje 7 plně rozkomentovaných ukázkových her (od Pexesa, přes Pong až po Vesmírnou střílečku). Je to ideální základ pro akční a arkádové hry.
*   📁 **`renpy/`** - Obsahuje 3 ukázkové projekty pro tvorbu příběhových her a vizuálních novel. Uvidíte tam, jak se pracuje s postavami, větvením děje i pokročilými animacemi.
*   📁 **`pure_python/`** - Ukázky her vytvořených v čistém Pythonu bez externích knihoven. Najdete zde textovou adventuru a klasického oběšence. Skvělé pro pochopení logiky a smyček.

---

## 🎨 Kde stáhnout grafiku a zvuky (Assety)?

Hra není jen o kódu, ale i o vzhledu a atmosféře. Zde je seznam těch nejlepších stránek, kde si můžete **zdarma a legálně** stáhnout grafiku, zvuky a hudbu do svých her:

### 🖼️ Grafika a 2D Assety
*   [**Kenney.nl**](https://kenney.nl/assets) – Absolutní svatý grál pro začínající vývojáře. Tisíce 2D i 3D modelů, UI prvků a zvuků, které jsou zcela zdarma (tzv. Public Domain - CC0). Nemusíte u nich ani uvádět autora.
*   [**Itch.io (Game Assets)**](https://itch.io/game-assets/free) – Velká platforma pro nezávislé vývojáře. Najdete tam obrovské množství asset packů (pixel art, postavy, pozadí). Stačí filtrovat podle "Free".
*   [**OpenGameArt.org**](https://opengameart.org/) – Jedna z nejstarších a největších komunitních databází herní grafiky. Pozor, čtěte si licence (často je nutné uvést jméno autora do titulků vaší hry).

### 🎵 Zvukové efekty a hudba
*   [**Freesound.org**](https://freesound.org/) – Obrovská databáze uživateli nahraných zvukových efektů (výbuchy, kroky, skákání, vítr). Pro stahování si musíte vytvořit bezplatný účet.
*   [**Incompetech.com**](https://incompetech.com/) – Stránka legendárního skladatele Kevina MacLeoda. Najdete tam stovky skladeb roztříděných podle žánru a nálady. Ideální pro podkresovou hudbu. (Stačí ho uvést v titulcích hry).
*   [**Chiptone**](https://sfbgames.itch.io/chiptone) – Online generátor zvuků, kde si můžete sami vygenerovat vtipné 8-bitové zvuky (skok, zranění, sbírání mincí) pouhým klikáním.

---

## 🛠️ Jaký software k vývoji použít?

I když budete dělat jen jednoduché hry, hodí se vědět, jaké programy vám práci nejvíc usnadní:

### Psaní kódu (IDE)
*   [**Visual Studio Code**](https://code.visualstudio.com/) – Nejpoužívanější editor současnosti. Určitě si do něj stáhněte rozšíření pro Python.
*   [**PyCharm Community**](https://www.jetbrains.com/pycharm/) – Skvělé prostředí od JetBrains, perfektní pro odhalování chyb.
*   [**Thonny**](https://thonny.org/) – Jednoduchý editor dělaný speciálně pro začátečníky. Pokud se vám VS Code zdá moc složitý, Thonny je jasná volba.

### Tvorba grafiky (Pixel Art)
*   [**Piskel**](https://www.piskelapp.com/) – Jednoduchý editor v prohlížeči, perfektní na tvorbu postaviček a jednoduchých animací zdarma.
*   [**Aseprite / LibreSprite**](https://libresprite.github.io/) – Profesionální nástroje na pixel art a animace (LibreSprite je zdarma).
*   *Nebo obyčejné Malování! I s tím se dá udělat zábavná a vtipná hra.*

### Úprava zvuku
*   [**Audacity**](https://www.audacityteam.org/) – Klasický, bezplatný program na stříhání zvuků, úpravu hlasitosti a spojování hudby.

---

## 💡 Rady do začátku a jak postupovat

Pokud nevíte jak začít, zkuste se držet těchto bodů:

1. **Udržujte to jednoduché (KISS):** Váš první cíl není vytvořit MMORPG s obřím světem. Zkuste vytvořit hru, ve které ovládáte čtvereček, co sbírá jiné čtverečky. Teprve až to bude fungovat, nahraďte čtverečky za grafiku a přidejte zvuky.
2. **Kopírujte a upravujte:** Nejlepší způsob, jak se naučit programovat hry, je vzít fungující kód a zkusit ho "rozbít". Vezměte si naši ukázku Pongu nebo Skákačky, změňte barvy, změňte rychlost, přidejte dalšího nepřítele. Postupně tak pochopíte, co který řádek dělá.
3. **Debugujte pomocí `print()`:** Pokud se vaše postava nehýbe nebo se neděje to, co má, vypisujte si do terminálu její souřadnice nebo stav. Mnohdy vám to okamžitě odhalí chybu.
4. **Rozdělte si práci:** Pokud na začátku narazíte na příliš složitý problém, rozdělte si ho na menší části. Nezkoušejte naprogramovat "bojový systém" jako celek. Nejdřív naprogramujte "stisknutí mezerníku ubere nepříteli 1 HP".
5. **Dělejte si zálohy:** Často ukládejte a pokud něco začne fungovat, udělejte si kopii souboru (nebo použijte Git!), než do toho začnete vrtat dál.

Hodně štěstí při vývoji! Nezapomeňte, že primárním cílem Game Jamu je se něco nového naučit a pobavit se u toho.

---

## 🌐 Optimalizace pro Školní Webový Portál (GameGlass)

Aby vaše hry fungovaly nejen u vás na počítači (Desktopu), ale šly bez problémů nahrát a hrát přímo ve webovém prohlížeči v našem školním systému, musíte dodržet několik důležitých technických pravidel:

### 1. Pygame hry (Nutnost použít asynchronní kód)
Webový prohlížeč neumožňuje tzv. "nekonečné blokovací smyčky" (zamrzla by vám celá záložka v prohlížeči). Vaše hlavní herní smyčka proto **musí** být napsána asynchronně pomocí modulu `asyncio`:

*   **Pravidlo 1:** Hlavní smyčka hry musí být definována jako `async def hlavni_smycka():`.
*   **Pravidlo 2:** Uvnitř `while True:` smyčky musíte na konec každého kola (typicky za `pygame.display.flip()`) přidat `await asyncio.sleep(0)`. Tento příkaz "na milisekundu" uvolní prohlížeč, aby stihl vykreslit obraz.
*   **Pravidlo 3:** 🚫 **ZÁKAZ** používání `pygame.time.wait()` nebo `pygame.time.delay()`. Tyto funkce na webu totálně zamrazí celou obrazovku. Pokud potřebujete hru na vteřinu uspat (např. při chybě v Pexesu), použijte `await asyncio.sleep(1)`.
*   **Pravidlo 4:** Spuštění hry na samotném konci souboru musí vypadat takto: `asyncio.run(hlavni_smycka())`

*(Prohlédněte si naše ukázky v adresáři `pygame/`, všechny jsou už pro web plně optimalizované!)*

### 2. Balení her pro odevzdání (ZIP)
Na portál se hry nahrávají ve formátu `.zip`. Je ale velmi důležité, co do ZIPu zabalíte:
*   **Pygame a Čistý Python:** Hlavní spouštěcí soubor vaší hry by měl být umístěn přímo v kořenovém adresáři ZIPu (nezašívejte ho hluboko do složek). Náš portál se ho pokusí najít a pokud se jmenuje `main.py`, je to ideální. Spolu se zdrojovým kódem nezapomeňte do ZIPu přibalit i složku se zvuky a grafikou (např. `/assets`).
*   **Ren'Py (Vizuální novely):** Nemusíte z Ren'Py enginu dělat žádný složitý "Web Export"! Stačí, když vezmete celou složku s vaším projektem (tu, která obsahuje podsložku `game/` se soubory `script.rpy` atd.) a rovnou ji zazipujete. Náš webový portál si tento ZIP automaticky rozbalí a nasadí do něj svůj vlastní webový RenPy motor. Je to naprosto bez starostí!