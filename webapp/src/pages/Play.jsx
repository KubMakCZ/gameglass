import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ChevronLeft } from 'lucide-react';
import { databases, DB_ID, COLLECTION_ID, storage, BUCKET_ZIPS_ID } from '../lib/appwrite';
import ConsolePlayer from '../components/players/ConsolePlayer';
import PygamePlayer from '../components/players/PygamePlayer';
import RenpyPlayer from '../components/players/RenpyPlayer';

export default function Play() {
  const { id } = useParams();
  const [game, setGame] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadGame() {
      try {
        const doc = await databases.getDocument(DB_ID, COLLECTION_ID, id);
        setGame({
          id: doc.$id,
          title: doc.title,
          author: doc.author,
          type: doc.type,
          zipFileId: doc.zip_file_id
        });
      } catch (e) {
        console.error('Nepodařilo se načíst hru:', e);
      } finally {
        setLoading(false);
      }
    }
    loadGame();
  }, [id]);

  if (loading) {
    return <div className="text-center py-20 text-tickle-muted animate-pulse">Načítám prostředí pro hraní...</div>;
  }

  if (!game) {
    return (
      <div className="text-center py-20">
        <h2 className="text-2xl text-tickle-accent mb-4">Hra nenalezena</h2>
        <Link to="/" className="btn-secondary py-2 px-4">Zpět na domovskou stránku</Link>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[80vh] animate-fade-in">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <Link to="/" className="p-2 bg-tickle-card/50 hover:bg-tickle-card rounded border border-tickle-border transition-colors">
            <ChevronLeft size={20} className="text-tickle-text" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-tickle-text">{game.title}</h1>
            <p className="text-sm text-tickle-muted font-sans">od {game.author}</p>
          </div>
        </div>
        <div className="bg-tickle-card border border-tickle-border px-3 py-1 rounded font-sans text-sm text-tickle-accent shadow-[0_0_10px_rgba(255,107,107,0.2)]">
          Prostředí: {game.type}
        </div>
      </div>

      <div className="flex-grow bg-black/60 rounded-xl border border-tickle-border overflow-hidden relative shadow-2xl">
        {game.type === 'python' ? (
          <ConsolePlayer game={game} />
        ) : game.type === 'pygame' ? (
          <PygamePlayer game={game} />
        ) : game.type === 'renpy' ? (
          <RenpyPlayer game={game} />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center text-tickle-muted text-center p-8 font-sans">
            <div>
              <h3 className="text-xl mb-2 text-tickle-text">Grafický mód ({game.type})</h3>
              <p>Zatím není připojen přehrávač pro tento engine.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
