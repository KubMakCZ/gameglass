# GameGlass - Roadmap & TODO

Tento dokument slouží k evidenci postupu vývoje a dlouhodobých cílů.

## 📝 Fáze 1: Základy a Design (DOKONČENO)
- [x] Návrh architektury (React + Appwrite) a řešení Python her v prohlížeči.
- [x] Inicializace Vite / React projektu.
- [x] Moderní UI/UX stylizace s ohledem na edukaci webdesignu (Tailwind CSS, "Tickle" estetika).
- [x] Založení navigační struktury (Home, Submit form).

## 🗄️ Fáze 2: Appwrite Backend (DOKONČENO)
- [x] Instalace a nastavení self-hosted Appwrite pro školy.
- [x] Propojení React aplikace s Appwrite Client SDK.
- [x] Zprovoznění nahrávání reálného ZIP souboru do Appwrite Storage.
- [x] Ukládání detailů her do databáze (Kolekce `games`).

## ⚙️ Fáze 3: Kompilace her a Hraní (DOKONČENO)
- [x] `PygamePlayer`: Spouštění grafických 2D her v prohlížeči. Vytvořeno pomocí JSZip na úpravu struktury a emulátoru `pygbag` s nativním WebAssembly zásahem do audia.
- [x] `ConsolePlayer`: Plnohodnotný terminál v prohlížeči vytvořený přes `pyodide` (WebWorkers + ServiceWorkers), podporuje plně synchronní `input()`.
- [x] `RenpyPlayer`: Spouštění vizuálních novel kompilací přes `Ren'Py Web`.

## 🚀 Fáze 4: Beta, Vydání a Proxmox Deployment (DOKONČENO)
- [x] Otestování kompletního "Flow" na reálných projektech.
- [x] Zabezpečení proti smazání (Lokální `LocalStorage` vlastnictví se skrytým košem).
- [x] Tvorba `Dockerfile`, `docker-compose.yml` pro spuštění na Proxmox LXC kontejneru přes NGINX.
- [x] Napsání profi `README.md` a `first_install.md`.
- [x] Zahrnutí ukázkových projektů pro učitele do složky `examples/`.

---

## 🔮 Fáze 5: Velké budoucí plány (PLÁNOVÁNO / ROADMAPA)

### Systém uživatelů a rolí
- [ ] Integrace Appwrite Auth (registrace, přihlášení pomocí e-mailu / Google).
- [ ] Tvorba rolí: **Admin** (plná správa), **Porotce/Učitel** (hodnocení), **Student** (zpráva vlastních her).
- [ ] Hodnotící panel, bodování soutěžních projektů.

### Rozšířená podpora Enginů
- [ ] Běh her z **GB Studio** (pomocí GameBoy webového emulátoru).
- [ ] Podpora pro **AGS** (Adventure Game Studio).
- [ ] Vytvoření speciální kategorie s tlačítkem *"Stáhnout"* pro obrovské 3D hry (Unity, Godot, Unreal Engine), které nelze spolehlivě hrát v prohlížeči.

### Bohaté profily a rozdělení soutěží
- [ ] Náhledové obrázky a plnohodnotné textové profily pro každou hru.
- [ ] Možnost přidávat k hrám instrukce pro ovládání.
- [ ] Zakládání izolovaných **Game Jamů** (soutěžních ročníků). Hry nebudou v jednom velkém seznamu, ale rozřazené pod konkrétní soutěž (např. *Zimní Game Jam 2026*).

### Vícejazyčnost (i18n)
- [ ] Příprava lokalizačních souborů a přepínač jazyků (CZ, SK, EN, DE).
