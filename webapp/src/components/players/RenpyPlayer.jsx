import { useEffect, useState } from 'react';
import { storage, BUCKET_ZIPS_ID } from '../../lib/appwrite';
import JSZip from 'jszip';

export default function RenpyPlayer({ game }) {
  const [status, setStatus] = useState('Inicializace...');
  const [iframeSrcDoc, setIframeSrcDoc] = useState(null);

  useEffect(() => {
    let blobUrl = null;

    async function loadAndPrepareRenpy() {
      try {
        if (!game.zipFileId) throw new Error('Hra nemá nahraný žádný ZIP zdroják.');

        setStatus('Stahuji herní data...');
        const downloadUrl = storage.getFileDownload(BUCKET_ZIPS_ID, game.zipFileId);
        
        const response = await fetch(downloadUrl);
        if (!response.ok) throw new Error('Nepodařilo se stáhnout ZIP z Appwrite');
        const buffer = await response.arrayBuffer();
        
        setStatus('Upravuji ZIP pro RenPy...');
        const originalZip = new JSZip();
        await originalZip.loadAsync(buffer);
        
        
        const handleZip = async (zipBlob) => {
          try {
            // 1. Stáhneme oficiální base_game.zip (obsahuje Python SDK RenPy a main.py)
            const baseResponse = await fetch('/renpy-engine/base_game.zip');
            const baseBlob = await baseResponse.blob();
            
            const jszip = new JSZip();
            const baseZip = await jszip.loadAsync(baseBlob);
            
            // Odstraníme starou hru z baseZipu (pokud tam nějaká je)
            const filesToRemove = [];
            baseZip.forEach((relativePath) => {
              if (relativePath.startsWith('game/')) {
                filesToRemove.push(relativePath);
              }
              if (relativePath.endsWith('.py') && relativePath !== 'main.py' && !relativePath.startsWith('renpy/')) {
                filesToRemove.push(relativePath); // Smažeme např. renpy_example_01.py
              }
            });
            filesToRemove.forEach(f => baseZip.remove(f));

            // 2. Načteme uživatelův ZIP
            const userZip = await (new JSZip()).loadAsync(zipBlob);
            
            // Najdeme cestu k podsložce 'game/' v uživatelově zipu
            let gameFolderPath = '';
            userZip.forEach((relativePath) => {
              if (relativePath.endsWith('game/') || relativePath === 'game' || relativePath.match(/(^|\/)game\//)) {
                const match = relativePath.match(/(.*(?:^|\/))game\//);
                if (match) gameFolderPath = match[0];
              }
            });

            if (!gameFolderPath) {
              setStatus('Chyba: V nahraném ZIPu nebyla nalezena složka "game".');
              return;
            }

            // 3. Zkopírujeme soubory z uživatelské game/ složky do baseZipu
            const promises = [];
            userZip.forEach((relativePath, file) => {
              if (relativePath.startsWith(gameFolderPath) && !file.dir) {
                const newPath = 'game/' + relativePath.substring(gameFolderPath.length);
                promises.push(
                  file.async('blob').then(blob => {
                    baseZip.file(newPath, blob);
                  })
                );
              }
            });
            await Promise.all(promises);

            // 4. Vygenerujeme výsledný ZIP
            const newZipBlob = await baseZip.generateAsync({ type: 'blob' });
            blobUrl = URL.createObjectURL(newZipBlob);
            
          } catch (e) {
            console.error(e);
            setStatus('Nastala chyba při zpracování ZIP archivu.');
          }
        };

        await handleZip(buffer);
        if (!blobUrl) return;

        setStatus('Spouštím RenPy WebAssembly Emulátor...');
        
        const htmlTemplate = `
<!doctype html>
<html lang="en-us">
<head>
  <meta charset="utf-8">
  <title>RenPy Player</title>
  <style>
    html {
      background: #000;
      font-family: sans-serif;
    }
    body, html {
      overscroll-behavior: none;
      margin: 0;
      padding: 0;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      overflow: hidden;
    }
    #canvas, #overlayDiv {
      position: absolute;
      top: 0px;
      left: 0px;
      width: 100%;
      height: 100%;
      border: 0 none;
      object-fit: contain;
    }
    #canvas {
      background: #000;
    }
    .visible {
      visibility: visible;
      opacity: 1.0;
      transition: opacity .1s linear;
    }
    .hidden {
      visibility: hidden;
      opacity: 0;
      transition: visibility 0s .25s, opacity .25s linear;
    }
    #statusDiv {
      background: rgba(0, 0, 0, 0.75);
      width: 50%;
      margin: auto;
      min-width: 340px;
      padding: 10px;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      border-radius: 8px;
      color: #ccc;
      text-align: center;
      z-index: 10;
    }
    #statusProgress {
      width: 100%;
      margin-top: 10px;
    }
    /* Skryjeme původní menu RenPy, protože máme vlastní GameGlass UI */
    #ContextContainer { display: none !important; }
  </style>
</head>
<body>
  <canvas id="canvas" oncontextmenu="event.preventDefault()" tabindex="-1"></canvas>
  <div id="overlayDiv"></div>

  <div id="statusDiv">
    <div id="statusTextDiv">Načítám RenPy Engine...</div>
    <progress id="statusProgress" value="0" max="100"></progress>
  </div>

  <div id="inputDiv" class="hidden">
    <form id="inputForm">
      <div id="inputPrompt"></div>
      <input id="inputText" type="text">
    </form>
  </div>

  <div id="presplash" style="display: none;"></div>

  <div id="ContextContainer" style="display: none;">
    <a id="ContextButton">&#8801;</a><br />
    <div id="ContextMenu" style="display: none;">
      <input id="ID_SavegamesImport" type="file" accept="application/zip" style="display:none"></input>
    </div>
  </div>

  <script>
      // Připojíme Blob URL staženýho ZIPu přímo do enginu
      window.gameZipURL = '${blobUrl}';

      // Konfigurace pro Emscripten, aby věděl, kde najít .wasm a .data
      window.Module = {
          locateFile: function(path, prefix) {
              if (path.endsWith('.data') || path.endsWith('.wasm')) {
                  return '/renpy-engine/' + path;
              }
              return prefix + path;
          }
      };
  </script>
  <!-- Odkazy na lokální engine soubory. Cesta musí odpovídat public složce Vite -->
  <script src="/renpy-engine/renpy-pre.js"></script>
  <script async type="text/javascript" src="/renpy-engine/renpy.js"></script>
</body>
</html>
`;
        setIframeSrcDoc(htmlTemplate);

      } catch (e) {
        console.error(e);
        setStatus(`Chyba: ${e.message}`);
      }
    }

    loadAndPrepareRenpy();

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
            title="RenPy Emulator"
            sandbox="allow-scripts allow-same-origin allow-pointer-lock"
          ></iframe>
        ) : (
          <div className="flex items-center justify-center w-full h-full text-tickle-muted">
            Načítám RenPy Engine prostředí...
          </div>
        )}
      </div>
    </div>
  );
}
