import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Submit from './pages/Submit';
import Play from './pages/Play';

function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="container mx-auto px-6 pt-10 pb-20 flex-grow">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/submit" element={<Submit />} />
          <Route path="/play/:id" element={<Play />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
