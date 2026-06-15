import { Link } from 'react-router-dom';
import { Upload } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 bg-tickle-bg/90 backdrop-blur border-b border-tickle-border py-4">
      <div className="container mx-auto px-6 flex justify-between items-center">
        <Link to="/" className="text-2xl font-display font-bold text-tickle-text flex items-center gap-3 hover:text-tickle-accent transition-colors">
          <img 
            src="/logo.jpg" 
            alt="GameGlass Logo" 
            className="w-10 h-10 object-cover rounded-xl shadow-[0_0_15px_rgba(255,107,107,0.4)] border border-tickle-border/50"
          />
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
