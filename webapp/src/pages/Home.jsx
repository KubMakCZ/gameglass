import { useState, useEffect } from 'react';
import { databases, DB_ID, COLLECTION_ID } from '../lib/appwrite';
import GameCard from '../components/GameCard';

export default function Home() {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchGames() {
      try {
        // Získáme seznam dokumentů (her) z naší Appwrite kolekce
        const response = await databases.listDocuments(DB_ID, COLLECTION_ID);
        
        // Zdokumentujeme data (Appwrite je vrací pod vlastností 'documents')
        const fetchedGames = response.documents.map(doc => ({
          id: doc.$id,
          title: doc.title,
          author: doc.author,
          type: doc.type,
          zipFileId: doc.zip_file_id
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
        <div className="flex items-center gap-3 mb-8">
          <div className="w-1.5 h-8 bg-tickle-accent rounded-full shadow-[0_0_10px_rgba(255,107,107,0.5)]"></div>
          <h2 className="text-2xl text-tickle-text">Nejnovější hry</h2>
        </div>
        
        {loading ? (
          <div className="text-center py-12 text-tickle-muted font-sans animate-pulse">
            Načítám hry z databáze...
          </div>
        ) : games.length === 0 ? (
          <div className="text-center py-12 text-tickle-muted font-sans bg-tickle-card rounded-lg border border-tickle-border">
            Zatím tu nejsou žádné hry. Zkus nějakou nahrát!
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {games.map((game) => {
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
