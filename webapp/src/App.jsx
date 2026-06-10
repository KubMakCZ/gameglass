import { useState } from 'react'
import './App.css'

const starterGames = [
  {
    id: 1,
    title: 'Dungeon Quiz',
    author: 'Team Alpha',
    engine: 'Python + Pygame',
    playUrl: 'https://example.com/dungeon-quiz',
    notes: 'Keyboard controls, puzzle and math rounds.',
  },
  {
    id: 2,
    title: 'Rainy Story',
    author: 'Team Delta',
    engine: 'RenPy',
    playUrl: 'https://example.com/rainy-story',
    notes: 'Visual novel with choices and multiple endings.',
  },
]

function App() {
  const [games, setGames] = useState(starterGames)
  const [formData, setFormData] = useState({
    title: '',
    author: '',
    engine: 'Python text game',
    playUrl: '',
  })

  const handleChange = (event) => {
    const { name, value } = event.target
    setFormData((current) => ({ ...current, [name]: value }))
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    setGames((current) => [
      {
        ...formData,
        id: Date.now(),
        notes: 'New student submission',
      },
      ...current,
    ])
    setFormData({
      title: '',
      author: '',
      engine: 'Python text game',
      playUrl: '',
    })
  }

  return (
    <div className="bg-body-tertiary min-vh-100 py-4">
      <main className="container">
        <div className="p-4 p-md-5 mb-4 rounded-4 shadow-sm bg-white text-start">
          <p className="text-uppercase fw-semibold text-secondary mb-2">
            GameGlass · School & Private Game Jam Hub
          </p>
          <h1 className="display-6 fw-bold mb-3">Publish, test and play student games</h1>
          <p className="mb-0 text-secondary">
            This React + Bootstrap webapp is ready for class game jams. Students can share
            Python, Pygame or RenPy projects and everyone can open playable builds in one
            place.
          </p>
        </div>

        <section className="row g-4">
          <div className="col-lg-7">
            <div className="card shadow-sm h-100">
              <div className="card-body text-start">
                <h2 className="h4 mb-3">Playable submissions</h2>
                <p className="text-secondary mb-4">
                  Add links to exported HTML builds so students can test each other&apos;s games.
                </p>
                <div className="d-grid gap-3">
                  {games.map((game) => (
                    <article key={game.id} className="border rounded-3 p-3">
                      <div className="d-flex justify-content-between flex-wrap gap-2 align-items-center">
                        <h3 className="h5 m-0">{game.title}</h3>
                        <span className="badge text-bg-light border">{game.engine}</span>
                      </div>
                      <p className="mb-2 text-secondary small">By {game.author}</p>
                      <p className="mb-3 small">{game.notes}</p>
                      <a
                        className="btn btn-sm btn-primary"
                        href={game.playUrl}
                        target="_blank"
                        rel="noreferrer"
                      >
                        Play game
                      </a>
                    </article>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="col-lg-5">
            <div className="card shadow-sm mb-4">
              <div className="card-body text-start">
                <h2 className="h4 mb-3">Publish a game</h2>
                <form className="row g-3" onSubmit={handleSubmit}>
                  <div className="col-12">
                    <label className="form-label" htmlFor="title">
                      Game title
                    </label>
                    <input
                      id="title"
                      className="form-control"
                      name="title"
                      value={formData.title}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div className="col-12">
                    <label className="form-label" htmlFor="author">
                      Author / team
                    </label>
                    <input
                      id="author"
                      className="form-control"
                      name="author"
                      value={formData.author}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div className="col-12">
                    <label className="form-label" htmlFor="engine">
                      Engine
                    </label>
                    <select
                      id="engine"
                      className="form-select"
                      name="engine"
                      value={formData.engine}
                      onChange={handleChange}
                    >
                      <option>Python text game</option>
                      <option>Python + Pygame</option>
                      <option>RenPy</option>
                    </select>
                  </div>
                  <div className="col-12">
                    <label className="form-label" htmlFor="playUrl">
                      Play URL
                    </label>
                    <input
                      id="playUrl"
                      className="form-control"
                      name="playUrl"
                      type="url"
                      placeholder="https://..."
                      value={formData.playUrl}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div className="col-12">
                    <button type="submit" className="btn btn-success w-100">
                      Publish submission
                    </button>
                  </div>
                </form>
              </div>
            </div>

            <div className="card shadow-sm">
              <div className="card-body text-start">
                <h2 className="h5 mb-3">Backend and export notes</h2>
                <ul className="small m-0 ps-3">
                  <li>Use Appwrite for jam events, submissions and user accounts.</li>
                  <li>Store game metadata in an Appwrite collection.</li>
                  <li>
                    Compile student games to web output (Pyodide/Pygbag for Python, web export
                    build for RenPy) and host each build with a public URL.
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
