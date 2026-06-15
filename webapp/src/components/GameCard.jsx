import { Play, Gamepad2, Download, Trash, Github } from 'lucide-react';
import { Link } from 'react-router-dom';
import { storage, databases, DB_ID, COLLECTION_ID, BUCKET_ZIPS_ID } from '../lib/appwrite';
import { useState } from 'react';

export default function GameCard({ id, title, author, type, zipFileId, gitUrl, isOwned, onDelete }) {
  const [isDeleting, setIsDeleting] = useState(false);

  const typeLabels = {
    'python': { text: 'Console', color: 'bg-tickle-cool text-tickle-bg' },
    'pygame': { text: 'Pygame', color: 'bg-tickle-secondary text-tickle-bg' },
    'renpy': { text: 'Ren\'Py', color: 'bg-[#ff9ff3] text-tickle-bg' } 
  };

  const currentType = typeLabels[type] || typeLabels['python'];

  const handleDownload = () => {
    if (!zipFileId) return;
    const downloadUrl = storage.getFileDownload(BUCKET_ZIPS_ID, zipFileId);
    
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = `${title}.zip`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const handleDelete = async (e) => {
    e.preventDefault();
    if (!window.confirm(`Opravdu chcete nenávratně smazat hru "${title}"?`)) return;

    setIsDeleting(true);
    try {
      if (zipFileId) {
        try {
          await storage.deleteFile(BUCKET_ZIPS_ID, zipFileId);
        } catch(e) {
          console.warn("Nepodařilo se smazat ZIP soubor, možná už neexistuje", e);
        }
      }
      
      await databases.deleteDocument(DB_ID, COLLECTION_ID, id);
      
      if (onDelete) onDelete();
      
    } catch (err) {
      console.error("Chyba při mazání hry:", err);
      alert("Nepodařilo se smazat hru. Možná k tomu nemáte oprávnění v Appwrite.");
      setIsDeleting(false);
    }
  };

  return (
    <div className={`glass-card flex flex-col overflow-hidden group ${isDeleting ? 'opacity-50 pointer-events-none' : ''}`}>
      <div className="h-40 bg-black/40 flex items-center justify-center relative overflow-hidden">
        <div className="absolute inset-0 bg-tickle-accent/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        
        <Gamepad2 size={64} className="text-tickle-text/10 group-hover:scale-110 transition-transform duration-500" />
        
        <div className="absolute top-3 right-3 flex items-center gap-2">
          {isOwned && (
            <button 
              onClick={handleDelete}
              className="bg-[#ff5f56] text-white p-1.5 rounded shadow-md hover:bg-red-600 transition-colors"
              title="Smazat tuto hru"
            >
              <Trash size={14} />
            </button>
          )}
          <span className={`${currentType.color} text-xs font-bold font-sans px-2.5 py-1 rounded shadow-md`}>
            {currentType.text}
          </span>
        </div>
      </div>
      <div className="p-5 flex flex-col flex-grow gap-4">
        <div>
          <h3 className="text-xl mb-1 text-tickle-text group-hover:text-tickle-accent transition-colors truncate">{title}</h3>
          <p className="text-tickle-muted text-sm font-sans truncate">od <span className="text-tickle-text/80">{author}</span></p>
        </div>
        <div className="mt-auto flex justify-between items-center gap-2">
          <div className="flex gap-2">
            <button 
              onClick={handleDownload}
              disabled={!zipFileId}
              className="btn-secondary py-2 px-3 text-xs disabled:opacity-50"
              title="Stáhnout ZIP"
            >
              <Download size={14} />
            </button>
            {gitUrl && (
              <a 
                href={gitUrl} 
                target="_blank" 
                rel="noopener noreferrer"
                className="btn-secondary py-2 px-3 text-xs flex items-center justify-center"
                title="Zdrojový kód na GitHubu/GitLabu"
              >
                <Github size={14} />
              </a>
            )}
          </div>
          <Link to={`/play/${id}`} className="btn-primary py-2 px-4 text-xs flex items-center gap-1">
            <Play size={14} /> Hrát
          </Link>
        </div>
      </div>
    </div>
  );
}
