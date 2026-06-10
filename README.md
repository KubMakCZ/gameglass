# gameglass

GameGlass is a React + Bootstrap webapp starter for hosting school or private game jams.
It focuses on publishing student game submissions and letting classmates quickly open and test each other's games.

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

## Notes for backend and game export

- Use Appwrite for users, jam events and submission metadata.
- Publish each game as a web build URL:
  - Python/Pygame can be exported with tools like pygbag/pyodide workflows.
  - RenPy can be exported with web distribution build.
