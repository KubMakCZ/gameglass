import { Link } from 'react-router-dom';
import { Gamepad2, Upload } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 bg-tickle-bg/90 backdrop-blur border-b border-tickle-border py-4">
      <div className="container mx-auto px-6 flex justify-between items-center">
        <Link to="/" className="text-2xl font-display font-bold text-tickle-text flex items-center gap-3 hover:text-tickle-accent transition-colors">
          <Gamepad2 size={32} className="text-tickle-accent" />
          GameGlass
        </Link>
        <div className="flex gap-4">
          <Link to="/submit" className="btn-primary py-2 px-5 text-sm font-sans">
            <Upload size={18} />
            Nahrát hru
          </Link>
        </div>
      </div>
    </nav>
  );
}
