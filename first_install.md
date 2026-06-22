# 🚀 GameGlass - Návod k první instalaci a nasazení

Tento dokument je určen převážně učitelům a správcům školních IT sítí, kteří chtějí GameGlass zprovoznit na svém vlastním serveru (typicky na Proxmoxu nebo jiném Linux stroji).

Projekt se skládá ze **dvou hlavních částí**:
1. **Backend (Appwrite):** Databáze a cloudové úložiště pro `.zip` soubory.
2. **Frontend (GameGlass React WebApp):** Samotný webový portál, kam chodí studenti.

---

## ☁️ Krok 1: Příprava Backend Serveru (Appwrite)

Appwrite doporučujeme hostovat lokálně na vašem školním serveru přes Docker, ale můžete využít i jejich oficiální bezplatný Cloud.

### Varianta A: Lokální hostování přes Docker (Doporučeno pro školy)
Nejlepší řešení z hlediska soukromí a rychlosti. Vše běží u vás ve škole.
1. Nainstalujte na svůj Linuxový server (např. Ubuntu VM na Proxmoxu) Docker a Docker Compose.
2. Spusťte instalační skript Appwrite:
   ```bash
   docker run -it --rm \
       --volume /var/run/docker.sock:/var/run/docker.sock \
       --volume "$(pwd)"/appwrite:/usr/src/code/appwrite:rw \
       --entrypoint="install" \
       appwrite/appwrite:1.9.0
   ```
3. Dokončete instalaci, otevřete IP adresu vašeho serveru v prohlížeči a vytvořte si administrátorský účet.

### Varianta B: Cloudové řešení
Pokud nemáte vlastní server, stačí se zdarma zaregistrovat na [cloud.appwrite.io](https://cloud.appwrite.io/).

### Nastavení projektů v Appwrite
Nezávisle na tom, jakou variantu jste vybrali, musíte v Appwrite vytvořit potřebné entity:
1. **Projekt:** Vytvořte projekt (id zkopírujte).
2. **Databáze:** Vytvořte databázi s ID `gameglass_db`.
3. **Kolekce:** Uvnitř databáze vytvořte kolekci `games` a nastavte oprávnění (Permissions) na **Any** (Create, Read, Update, Delete) – pro školní Game Jamy je toto nejjednodušší.
4. **Atributy (Attributes):** V kolekci `games` vytvořte tyto atributy:
   - `title` (String, Required)
   - `author` (String, Required)
   - `type` (String, Required)
   - `zip_file_id` (String, Required)
5. **Úložiště (Storage):** V sekci Storage vytvořte Bucket s ID `games_zips`. Opět nastavte Permissions na **Any** (Read, Create, Update, Delete). *Doporučení: Nastavte maximální velikost souboru na 200 MB a povolte pouze `.zip` extenze.*

---

## 🖥️ Krok 2: Spuštění a nasazení Frontendu (Aplikace)

Složka `webapp/` obsahuje kód pro portál. Je napsaný v React/Vite.

### Konfigurace (Důležité)
Ve složce `webapp/` si vytvořte soubor `.env` a zadejte do něj vaše Appwrite údaje, např.:
```env
VITE_APPWRITE_ENDPOINT=http://ip-vaseho-appwrite-serveru/v1
VITE_APPWRITE_PROJECT_ID=66xxxxxx_vas_projekt_id
```
*(Pokud používáte Cloud, Endpoint je `https://cloud.appwrite.io/v1`)*

### Varianta A: Rychlé spuštění bez Dockeru (přes Node.js)
Tohle se hodí spíš pro vývoj na vašem osobním PC.
```bash
cd webapp
npm install
npm run dev
```

### Varianta B: Produkční nasazení přes Docker Compose (Doporučeno)
Přiložený `docker-compose.yml` automaticky zkompiluje React aplikaci do statických souborů a naservíruje je přes bleskově rychlý NGINX. Ideální pro školní Proxmox.
1. Ujistěte se, že máte ve složce `webapp/` svůj `.env` soubor!
2. Běžte do kořenové složky repozitáře a spusťte:
   ```bash
   docker compose up -d --build
   ```
3. Aplikace nyní běží na portu `80` vašeho serveru!

---

## 👩‍🏫 Co poradit studentům (Game Jam Instrukce)

Až budete vyučovat vývoj her, je potřeba žákům sdělit, že protože hry poběží ve webovém prohlížeči, existují pro Python mírná omezení:

### Obecná pravidla pro zabalení hry
- Celou složku se hrou musíte zazipovat tak, aby po otevření zipu byl rovnou vidět váš spouštěcí soubor (např. `main.py`). Nezipujte nadřazenou složku (nevytvářejte tzv. "folder-in-a-folder").

### Pro Pygame hry
Hry v Pygame pro převod do prohlížeče vyžadují malou, ale **absolutně klíčovou** úpravu ve vaší hlavní smyčce (aby prohlížeč nezamrzl):
1. Importujte knihovnu `asyncio`.
2. Hlavní smyčka hry musí být asynchronní (`async def main():`).
3. Namísto `pygame.time.wait()` používejte `clock.tick(60)`.
4. Uvnitř `while True:` smyčky musí být na konci vždy napsáno: `await asyncio.sleep(0)`.

*Podrobnou ukázku toho, jak vypadá správná asynchronní smyčka, naleznete ve složce `examples/` v tomto repozitáři, kterou můžete studentům rovnou rozdat.*

### Pro Textové hry (Pure Python)
Pro výstupy do naší "Konzole v prohlížeči" používejte klasický `print()`. Pro vstupy můžete normálně psát `input("Tvoje volba: ")`.
Pokud chcete text v konzoli smazat a udělat čistou obrazovku, použijte:
```python
import os
os.system('cls') # nebo 'clear'
```

### Pro Ren'Py (Vizuální novely)
S Ren'Py je to ze všeho nejjednodušší. Studenti nepotřebují exportovat vůbec žádné Web Buildy ze svého PC! Stačí, když otevřou složku svého projektu, označí všechny soubory ve složce `game/` a vytvoří z nich ZIP. Ten nahrají na náš portál, který už si ho zkompiluje za běhu naprosto sám.
