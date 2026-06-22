import { useState, useEffect } from 'react';
import { databases, DB_ID, COLLECTION_ID } from '../lib/appwrite';
import GameCard from '../components/GameCard';

import { Query } from 'appwrite';

export default function Home() {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    async function fetchGames() {
      try {
        // Získáme seznam dokumentů (her) z naší Appwrite kolekce, s navýšeným limitem!
        const response = await databases.listDocuments(DB_ID, COLLECTION_ID, [
            Query.limit(100)
        ]);
        
        // Zdokumentujeme data (Appwrite je vrací pod vlastností 'documents')
        const fetchedGames = response.documents.map(doc => ({
          id: doc.$id,
          title: doc.title,
          author: doc.author,
          type: doc.type,
          zipFileId: doc.zip_file_id,
          gitUrl: doc.git_url
        }));
        
        setGames(fetchedGames);
      } catch (error) {
        console.error('Chyba při načítání her z Appwrite:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchGames();
  }, []);

  const filteredGames = games.filter(game => {
    const term = searchTerm.toLowerCase();
    return (
      (game.title && game.title.toLowerCase().includes(term)) ||
      (game.author && game.author.toLowerCase().includes(term))
    );
  });

  return (
    <div className="animate-fade-in">
      <section className="text-center py-16 mb-10">
        <h1 className="text-5xl md:text-6xl mb-6 text-tickle-text">
          Školní <span className="text-tickle-accent">Game Jam</span> Portál
        </h1>
        <p className="text-tickle-muted font-sans text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
          Hrajte, objevujte a sdílejte hry vytvořené studenty v Pythonu. Vše funguje magicky přímo v prohlížeči!
        </p>
      </section>

      <section>
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8">
          <div className="flex items-center gap-3">
            <div className="w-1.5 h-8 bg-tickle-accent rounded-full shadow-[0_0_10px_rgba(255,107,107,0.5)]"></div>
            <h2 className="text-2xl text-tickle-text">Hry v portálu</h2>
          </div>
          
          <div className="relative w-full sm:w-72">
            <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-tickle-muted">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>
            <input 
              type="text" 
              placeholder="Hledat hru nebo autora..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-tickle-card border border-tickle-border text-tickle-text text-sm rounded-lg focus:ring-tickle-accent focus:border-tickle-accent block pl-10 p-2.5 transition-colors placeholder-tickle-muted/50 font-sans outline-none"
            />
          </div>
        </div>
        
        {loading ? (
          <div className="text-center py-12 text-tickle-muted font-sans animate-pulse">
            Načítám hry z databáze...
          </div>
        ) : filteredGames.length === 0 ? (
          <div className="text-center py-12 text-tickle-muted font-sans bg-tickle-card rounded-lg border border-tickle-border">
            Zatím tu nejsou žádné hry nebo žádná hra neodpovídá hledání.
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredGames.map((game) => {
              const ownedIds = JSON.parse(localStorage.getItem('gameglass_owned') || '[]');
              const isOwned = ownedIds.includes(game.id);

              return (
                <GameCard 
                  key={game.id}
                  id={game.id}
                  title={game.title}
                  author={game.author}
                  type={game.type}
                  zipFileId={game.zipFileId}
                  gitUrl={game.gitUrl}
                  isOwned={isOwned}
                  onDelete={() => setGames(games.filter(g => g.id !== game.id))}
                />
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}
