import { useState } from 'react';
import { UploadCloud, CheckCircle, AlertCircle, FileCode, Package, Terminal } from 'lucide-react';
import { databases, storage, DB_ID, COLLECTION_ID, BUCKET_ZIPS_ID } from '../lib/appwrite';
import { ID } from 'appwrite';

export default function Submit() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  const [formData, setFormData] = useState({
    name: '',
    author: '',
    type: 'pygame',
    gitUrl: ''
  });
  
  const [file, setFile] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Vyberte prosím ZIP soubor s vaší hrou.');
      return;
    }

    setIsSubmitting(true);
    setError(null);
    setSuccess(false);

    try {
      // 1. Nahrát soubor do Storage
      const uploadedFile = await storage.createFile(
        BUCKET_ZIPS_ID,
        ID.unique(),
        file
      );

      // 2. Vytvořit dokument v databázi
      const doc = await databases.createDocument(
        DB_ID,
        COLLECTION_ID,
        ID.unique(),
        {
          title: formData.name,
          author: formData.author,
          type: formData.type,
          zip_file_id: uploadedFile.$id
        }
      );

      // 3. Uložit ID hry lokálně do prohlížeče (pro možnost pozdějšího smazání)
      const owned = JSON.parse(localStorage.getItem('gameglass_owned') || '[]');
      if (!owned.includes(doc.$id)) {
        owned.push(doc.$id);
        localStorage.setItem('gameglass_owned', JSON.stringify(owned));
      }

      setSuccess(true);
      setFormData({ name: '', author: '', type: 'pygame' });
      setFile(null);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Došlo k chybě při nahrávání hry. Zkuste to prosím znovu.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto animate-fade-in grid md:grid-cols-2 gap-8 items-start">
      
      {/* Formulář pro nahrání */}
      <div>
        <div className="mb-6">
          <h1 className="text-3xl mb-3 text-tickle-text">Nahrát novou hru</h1>
          <p className="text-tickle-muted font-sans">
            Zabal celý svůj projekt a odešli jej na GameGlass.
          </p>
        </div>

        <div className="glass-card p-8 relative">
          {success && (
            <div className="absolute inset-0 bg-tickle-bg/90 backdrop-blur-sm z-10 flex flex-col items-center justify-center p-8 text-center rounded-xl border border-[#27c93f]">
              <CheckCircle size={64} className="text-[#27c93f] mb-4" />
              <h2 className="text-2xl font-bold text-white mb-2">Hra byla úspěšně nahrána!</h2>
              <p className="text-tickle-muted mb-6">Tvá hra je nyní k dispozici v hlavní galerii.</p>
              <button onClick={() => setSuccess(false)} className="btn-primary">Nahrát další hru</button>
            </div>
          )}

          {error && (
            <div className="mb-6 p-4 bg-[#ff5f56]/10 border border-[#ff5f56] rounded-lg flex items-start gap-3">
              <AlertCircle className="text-[#ff5f56] shrink-0" />
              <p className="text-[#ff5f56] text-sm">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="flex flex-col gap-5 font-sans">
            
            <div className="flex flex-col gap-2">
              <label className="text-xs font-bold text-tickle-muted uppercase tracking-wider">Název hry</label>
              <input 
                type="text" 
                required 
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                className="input-field" 
                placeholder="Např. Dungeon Crawler" 
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-xs font-bold text-tickle-muted uppercase tracking-wider">Jméno autora</label>
              <input 
                type="text" 
                required 
                value={formData.author}
                onChange={(e) => setFormData({...formData, author: e.target.value})}
                className="input-field" 
                placeholder="Např. Jan Novák" 
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-xs font-bold text-tickle-muted uppercase tracking-wider">Herní Engine</label>
              <select 
                className="input-field cursor-pointer"
                value={formData.type}
                onChange={(e) => setFormData({...formData, type: e.target.value})}
              >
                <option value="pygame">Pygame (Grafická 2D hra)</option>
                <option value="renpy">Ren'Py (Vizuální novela)</option>
                <option value="python">Čistý Python (Terminálová hra)</option>
              </select>
            </div>

            <div className="flex flex-col gap-2 mt-2">
              <label className="text-xs font-bold text-tickle-muted uppercase tracking-wider">Zdrojové soubory (ZIP)</label>
              <div className="relative">
                <input 
                  type="file" 
                  accept=".zip"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" 
                />
                <div className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${file ? 'border-[#27c93f] bg-[#27c93f]/5' : 'border-tickle-border bg-black/20 hover:border-tickle-accent'}`}>
                  {file ? (
                    <>
                      <CheckCircle size={40} className="mx-auto mb-3 text-[#27c93f]" />
                      <p className="font-bold text-[#27c93f]">{file.name}</p>
                      <p className="text-xs text-tickle-muted mt-1">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                    </>
                  ) : (
                    <>
                      <UploadCloud size={40} className="mx-auto mb-3 text-tickle-muted" />
                      <p className="font-bold text-tickle-text mb-1">Klikni nebo přetáhni ZIP sem</p>
                      <p className="text-xs text-tickle-muted">Max. velikost 50 MB</p>
                    </>
                  )}
                </div>
              </div>
            </div>



            <button 
              type="submit" 
              disabled={isSubmitting}
              className="btn-primary w-full mt-4 py-4 text-lg disabled:opacity-50 flex justify-center items-center gap-2"
            >
              {isSubmitting ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  Nahrávám...
                </>
              ) : 'Odeslat hru do portálu'}
            </button>
          </form>
        </div>
      </div>

      {/* Instrukce a návod */}
      <div className="flex flex-col gap-6 pt-16">
        <div className="glass-card p-6 border-l-4 border-l-[#ffbd2e]">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Package className="text-[#ffbd2e]" /> Jak správně zabalit hru?
          </h2>
          <div className="font-sans text-sm text-tickle-muted space-y-4">
            <p>Hra musí být zabalená do formátu <strong>.ZIP</strong>. Nevybírejte rovnou celou nadřazenou složku, ale <strong>otevřete vaši složku s hrou, označte všechny soubory uvnitř</strong> (Ctrl+A) a teprve z nich vytvořte ZIP soubor. Spouštěcí skript se tak bude nacházet rovnou uvnitř ZIPu a nikoliv uvnitř další podsložky.</p>
          </div>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-[#58a6ff]">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <FileCode className="text-[#58a6ff]" /> Požadavky pro Pygame
          </h2>
          <div className="font-sans text-sm text-tickle-muted space-y-4">
            <ul className="list-disc pl-5 space-y-2">
              <li>Hlavní soubor se musí jmenovat <strong className="text-white">main.py</strong>.</li>
              <li>Hra musí používat asynchronní smyčku pro běh v prohlížeči (použijte <code>asyncio</code>).</li>
              <li>
                Každý průchod hlavní smyčky (`while True:`) musí obsahovat příkaz:<br/>
                <code className="bg-black/50 p-1 rounded text-[#58a6ff] block mt-1">await asyncio.sleep(0)</code>
              </li>
              <li>Zcela se vyhněte `pygame.time.wait()` a `pygame.time.delay()`, použijte hodiny (`clock.tick()`).</li>
            </ul>
          </div>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-[#ff5f56]">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Terminal className="text-[#ff5f56]" /> Požadavky pro Ren'Py & Čistý Python
          </h2>
          <div className="font-sans text-sm text-tickle-muted space-y-4">
            <div>
              <strong className="text-white block mb-1">Vizuální novely (Ren'Py)</strong>
              <p>Zazipujte POUZE obsah zdrojové složky <code>game/</code> vašeho Ren'Py projektu (soubory .rpy a obrázky). Nemusíte exportovat Web Build – náš portál si hru zkompiluje za běhu automaticky sám.</p>
            </div>
            <div className="mt-4">
              <strong className="text-white block mb-1">Terminálové hry (Čistý Python)</strong>
              <p>Hlavní soubor s hrou by měl mít příponu <code>.py</code> (na názvu nezáleží, portál si jej najde automaticky). Pro vstupy klasicky používejte <code>input()</code> a pro výstupy <code>print()</code>. Pokud portál narazí na <code>os.system('cls')</code> nebo <code>clear</code>, obrazovka terminálu se korektně vyčistí.</p>
            </div>
          </div>
        </div>
      </div>

    </div>
  );
}
