import { useEffect, useState } from 'react';
import { storage, BUCKET_ZIPS_ID } from '../../lib/appwrite';
import JSZip from 'jszip';

export default function PygamePlayer({ game }) {
  const [status, setStatus] = useState('Inicializace...');
  const [iframeSrcDoc, setIframeSrcDoc] = useState(null);

  useEffect(() => {
    let blobUrl = null;

    async function loadAndPreparePygame() {
      try {
        if (!game.zipFileId) throw new Error('Hra nemá nahraný žádný ZIP zdroják.');

        setStatus('Stahuji herní data...');
        const downloadUrl = storage.getFileDownload(BUCKET_ZIPS_ID, game.zipFileId);
        const response = await fetch(downloadUrl);
        if (!response.ok) throw new Error('Nepodařilo se stáhnout ZIP z Appwrite');
        const buffer = await response.arrayBuffer();

        setStatus('Upravuji ZIP pro WebAssembly (Pygbag)...');
        
        const originalZip = new JSZip();
        await originalZip.loadAsync(buffer);
        
        const newZip = new JSZip();
        let mainPyFound = false;

        for (const [relativePath, zipEntry] of Object.entries(originalZip.files)) {
          if (zipEntry.dir) continue;

          const isPythonScript = relativePath.endsWith('.py');
          const isInRoot = !relativePath.includes('/');
          
          if (isPythonScript && isInRoot && !mainPyFound) {
            const content = await zipEntry.async('uint8array');
            newZip.file('main.py', content);
            mainPyFound = true;
          } else {
            const content = await zipEntry.async('uint8array');
            newZip.file(relativePath, content);
          }
        }

        if (!mainPyFound) {
          throw new Error('V ZIPu se nenachází žádný .py soubor v hlavní složce.');
        }

        setStatus('Vytvářím herní balíček...');
        const newZipBlob = await newZip.generateAsync({ type: 'blob', compression: 'STORE' });
        
        blobUrl = URL.createObjectURL(newZipBlob);
        
        setStatus('Spouštím emulátor...');
        
        // Sestavení nativní Pygbag šablony s použitím aktuálního pythons.js (0.9.4)
        const htmlTemplate = `
<!DOCTYPE html>
<html lang="en-us">
<head>
  <meta charset="utf-8">
  <title>Pygame Player</title>
  <style>
    body { background-color: #0d1117; color: white; margin: 0; padding: 0; overflow: hidden; display: flex; justify-content: center; align-items: center; height: 100vh; }
    canvas { 
      outline: none; 
      border: none; 
      box-shadow: 0 0 20px rgba(0,0,0,0.5); 
      /* Klíčová oprava pro Pexeso a myš: 
         Předtím se canvas natáhl na 100% 100% a obraz se jen vizuálně "zdrcl" dovnitř přes object-fit: contain.
         Prohlížeč pak myši posílal souřadnice celého okna, nikoliv samotné hry, takže kliknutí létala mimo karty!
         Teď bude mít canvas přesně takové fyzické rozměry, jaké má mít, se zachováním 4:3 (800x600). */
      aspect-ratio: 4/3;
      max-width: 100vw;
      max-height: 100vh;
      margin: auto;
    }
    #status { display: none !important; }
    #infobox { position: fixed; background: #27c93f; color: white; font-weight: bold; padding: 12px 24px; top: 20px; left: 50%; transform: translateX(-50%); border-radius: 8px; cursor: pointer; display: none; z-index: 1000; }
  </style>
  <script>
    window.apkUrl = "${blobUrl}";
    window.config = {
        xtermjs : "0",
        _sdl2 : "canvas",
        user_canvas : 0,
        user_canvas_managed : 0,
        gui_divider : 2,
        ume_block : 1,
        can_close : 0,
        archive : window.apkUrl,
        gui_debug : 2,
        cdn : "https://pygame-web.github.io/archives/0.9/",
        autorun : 0, 
        PYBUILD : "3.12"
    };

    window.addEventListener("click", () => {
        if (window.MM) {
            window.MM.UME = true;
            if (window.MM.audioContext && window.MM.audioContext.state === "suspended") {
                window.MM.audioContext.resume();
            }
        }
        document.getElementById('infobox').style.display = "none";
    });
  </script>
</head>
<body>
  <div id="status" class="emscripten"></div>
  <div id="infobox">Klikni kamkoliv pro spuštění hry!</div>
  <canvas class="emscripten" id="canvas" oncontextmenu="event.preventDefault()" tabindex="1"></canvas>
  <script src="https://pygame-web.github.io/archives/0.9/pythons.js" type="module" id="site" data-python="python3.12" data-os="vtx,snd,gui" async defer>
#<!--
import sys
import asyncio
import platform
import zipfile
from pathlib import Path

async def custom_site():
    import embed
    
    appdir = Path("/data/data/game")
    appdir.mkdir(parents=True, exist_ok=True)
    
    async with platform.fopen(platform.window.apkUrl, "rb") as archive:
        with zipfile.ZipFile(archive) as zip_ref:
            zip_ref.extractall(appdir.as_posix())
            
    platform.run_main(PyConfig, loaderhome=appdir, loadermain=None)
    
    while embed.counter() < 0:
        await asyncio.sleep(.1)
        
    main = appdir / "main.py"
    
    if not platform.window.MM.UME:
        __import__(__name__).__file__ = main
        platform.window.document.getElementById('infobox').style.display = "block"
        while not platform.window.MM.UME:
            await asyncio.sleep(.1)
            
    platform.window.document.getElementById('infobox').style.display = "none"
    
    await TopLevel_async_handler.start_toplevel(platform.shell, console=False)
    __import__(__name__).__file__ = main
    
    await shell.source(main)
    shell.interactive()

asyncio.run(custom_site())
#--></script>
</body>
</html>
`;
        setIframeSrcDoc(htmlTemplate);

      } catch (e) {
        console.error(e);
        setStatus(`Chyba: ${e.message}`);
      }
    }

    loadAndPreparePygame();

    return () => {
      if (blobUrl) URL.revokeObjectURL(blobUrl);
    };
  }, [game]);

  return (
    <div className="h-full flex flex-col relative bg-[#000]">
      <div className="bg-tickle-card/80 border-b border-tickle-border px-4 py-2 flex items-center justify-between absolute top-0 w-full z-10">
        <span className="text-tickle-muted font-sans text-sm">
          Status: <span className="text-tickle-text">{status}</span>
        </span>
        <div className="flex gap-2">
          <div className="w-3 h-3 rounded-full bg-[#ff5f56]"></div>
          <div className="w-3 h-3 rounded-full bg-[#ffbd2e]"></div>
          <div className="w-3 h-3 rounded-full bg-[#27c93f]"></div>
        </div>
      </div>
      
      <div className="flex-grow w-full h-full pt-10">
        {iframeSrcDoc ? (
          <iframe 
            srcDoc={iframeSrcDoc} 
            className="w-full h-full border-none outline-none"
            title="Pygame Emulator"
            sandbox="allow-scripts allow-same-origin allow-pointer-lock"
          ></iframe>
        ) : (
          <div className="flex items-center justify-center w-full h-full text-tickle-muted">
            Načítám grafické prostředí...
          </div>
        )}
      </div>
    </div>
  );
}
