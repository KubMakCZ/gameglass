# gameglass

GameGlass is a starter project for school and private game jams.
The goal is to make it easy to collect game submissions, present them in one place,
and let players quickly open and test games in a browser.

## Project goals

- Simple game jam website for small communities and classrooms.
- Clear submission flow for teams and students.
- Fast browsing experience for judges and players.
- Easy future extension with backend services and moderation tools.

## Current stack

- Frontend: React + Vite
- UI: Bootstrap 5
- Language: JavaScript
- Package manager: npm

## Repository structure

```text
gameglass/
├── README.md
└── webapp/
    ├── src/
    ├── public/
    └── package.json
```

## Web app

The web application lives in `webapp/`.

### Run locally

```bash
cd webapp
npm install
npm run dev
```

### Build and lint

```bash
cd webapp
npm run lint
npm run build
```

## Suggested product flow

1. Organizers create a jam event.
2. Teams submit game metadata and play link.
3. Visitors open game cards and launch games instantly.
4. Optional judging and feedback are collected.
5. Results are published after the jam closes.

## Notes for backend and game export

- Appwrite is a good fit for users, jam events, and submission metadata.
- Every game should be publishable as a web URL.
- Python/Pygame games can be exported with pygbag or pyodide workflows.
- RenPy games can be exported using web distribution build.

## Progressive checklist (roadmap)

- [ ] **Phase 1 – Core foundation**
  - [ ] Define event model (jam info, timeline, rules).
  - [ ] Define submission model (team, game name, link, description, thumbnail).
  - [ ] Prepare base pages: Home, Active Jam, Submissions.
  - [ ] Add responsive layout for desktop and mobile.
- [ ] **Phase 2 – Submission workflow**
  - [ ] Add login/registration flow for participants.
  - [ ] Add submission form with input validation.
  - [ ] Add edit/update submission functionality before deadline.
  - [ ] Add upload/URL checks for game assets.
- [ ] **Phase 3 – Discovery and judging**
  - [ ] Add filtering and sorting for submitted games.
  - [ ] Add game detail page with embedded play instructions.
  - [ ] Add scoring criteria and judge dashboard.
  - [ ] Add comment/feedback section for each game.
- [ ] **Phase 4 – Operations and quality**
  - [ ] Add admin panel for moderation and event management.
  - [ ] Add analytics (visits, plays, submissions).
  - [ ] Add CI checks and stronger test coverage.
  - [ ] Add deployment docs and release checklist.
- [ ] **Phase 5 – Nice-to-have improvements**
  - [ ] Add themes/branding for different schools or events.
  - [ ] Add localization (Czech/English UI).
  - [ ] Add badges/achievements for participation.
  - [ ] Add archive page for finished jams.
