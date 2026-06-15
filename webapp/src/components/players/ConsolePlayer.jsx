import { useEffect, useRef, useState } from 'react';
import { storage, BUCKET_ZIPS_ID } from '../../lib/appwrite';
import JSZip from 'jszip';

export default function ConsolePlayer({ game }) {
  const outputRef = useRef(null);
  const workerRef = useRef(null);
  const [status, setStatus] = useState('Inicializace...');
  const [isWaitingForInput, setIsWaitingForInput] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [showSwTutorial, setShowSwTutorial] = useState(false);
  const pyodideStarted = useRef(false);

  const writeOutput = (text, isError = false) => {
    if (!outputRef.current) return;
    const span = document.createElement('span');
    span.textContent = text;
    if (isError) {
      span.style.color = '#ff6b6b';
      span.style.fontWeight = 'bold';
    }
    outputRef.current.appendChild(span);
    outputRef.current.scrollTop = outputRef.current.scrollHeight;
  };

  const writeln = (text, isError = false) => writeOutput(text + '\n', isError);

  const clearConsole = () => {
    if (outputRef.current) outputRef.current.innerHTML = '';
  };

  useEffect(() => {
    if (pyodideStarted.current) return;
    pyodideStarted.current = true;
    
    writeln('GameGlass Console v4.0 (WebWorker + SW Mode)', false);
    writeln('-------------------------------------------\n', false);
    
    // Registrujeme Service Worker pro zachytávání synchronních XHR požadavků z WebWorkeru
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw-input.js')
        .then(() => navigator.serviceWorker.ready)
        .then(() => {
          console.log('ServiceWorker je připraven.');
          
          if (!navigator.serviceWorker.controller) {
            console.log('Čekám, až ServiceWorker převezme kontrolu nad stránkou...');
            navigator.serviceWorker.addEventListener('controllerchange', () => {
              loadAndExtractGame();
            });
          } else {
            loadAndExtractGame();
          }
        })
        .catch((err) => {
          console.error('Chyba registrace ServiceWorkeru:', err);
          writeln('[CHYBA] Nepodařilo se nastavit Service Worker.', true);
          setShowSwTutorial(true);
        });

      // Posloucháme zprávy od ServiceWorkeru (žádost o vstup)
      navigator.serviceWorker.addEventListener('message', (event) => {
        if (event.data && event.data.type === 'INPUT_REQUEST') {
          setIsWaitingForInput(true);
          // Auto-scroll dolů, když se objeví input box
          setTimeout(() => {
            if (outputRef.current) outputRef.current.scrollTop = outputRef.current.scrollHeight;
          }, 50);
        }
      });
    } else {
      writeln('[CHYBA] Váš prohlížeč nepodporuje Service Workery.', true);
      setShowSwTutorial(true);
      return;
    }

    return () => {
      if (workerRef.current) {
        workerRef.current.terminate();
      }
    };
  }, [game]);

  const loadAndExtractGame = async () => {
    try {
      if (!game.zipFileId) throw new Error('Hra nemá nahraný žádný ZIP zdroják.');

      setStatus('Stahuji herní data...');
      writeln('=> Stahuji soubory ze serveru...');

      const downloadUrl = storage.getFileDownload(BUCKET_ZIPS_ID, game.zipFileId);
      const response = await fetch(downloadUrl);
      if (!response.ok) throw new Error('Nepodařilo se stáhnout ZIP z Appwrite');
      const buffer = await response.arrayBuffer();

      setStatus('Rozbaluji zdrojové kódy...');
      writeln('=> Rozbaluji ZIP archiv...');

      const zip = new JSZip();
      const extracted = await zip.loadAsync(buffer);
      
      let mainPyContent = null;
      let mainPyName = null;
      
      for (const [relativePath, zipEntry] of Object.entries(extracted.files)) {
        if (!zipEntry.dir && relativePath.endsWith('.py')) {
          mainPyName = relativePath;
          mainPyContent = await zipEntry.async('string');
          break;
        }
      }

      if (!mainPyContent) {
        throw new Error('V ZIPu se nenachází žádný .py soubor.');
      }

      writeln(`=> Nalezen hlavní skript: ${mainPyName}`);
      setStatus('Připravuji Worker...');

      // Vytvoříme WebWorker a propojíme jeho komunikaci
      workerRef.current = new Worker('/pyodide-worker.js');
      
      workerRef.current.onmessage = (event) => {
        const data = event.data;
        if (data.type === 'STATUS') {
          setStatus(data.text);
          writeln(`=> ${data.text}`);
        } else if (data.type === 'STDOUT') {
          writeOutput(data.text + '\n');
        } else if (data.type === 'STDERR') {
          writeOutput(data.text + '\n', true);
        } else if (data.type === 'ERROR') {
          writeOutput(data.text, true);
          setStatus('Aplikace skončila s chybou.');
        } else if (data.type === 'DONE') {
          writeOutput(data.text);
          setStatus('Dokončeno.');
        } else if (data.type === 'CLEAR') {
          clearConsole();
        }
      };

      // Pošleme workeru kód k provedení
      workerRef.current.postMessage({
        type: 'RUN_CODE',
        filename: mainPyName,
        code: mainPyContent
      });

    } catch (e) {
      console.error(e);
      writeln(`\n[CHYBA] ${e.message}`, true);
      setStatus('Chyba při načítání hry.');
    }
  };

  const handleInputSubmit = (e) => {
    e.preventDefault();
    const text = inputValue;
    
    // Vypíšeme uživatelův vstup do konzole modře
    const inputSpan = document.createElement('span');
    inputSpan.textContent = text + '\n';
    inputSpan.style.color = '#58a6ff';
    if (outputRef.current) {
      outputRef.current.appendChild(inputSpan);
    }

    setInputValue('');
    setIsWaitingForInput(false);

    // Pošleme vstup zpět přes ServiceWorker
    if (navigator.serviceWorker.controller) {
      navigator.serviceWorker.controller.postMessage({
        type: 'INPUT_RESPONSE',
        text: text
      });
    }
  };

  return (
    <div className="h-full flex flex-col">
      <div className="bg-tickle-card/80 border-b border-tickle-border px-4 py-2 flex items-center justify-between shrink-0">
        <span className="text-tickle-muted font-sans text-sm">
          Status: <span className="text-tickle-text">{status}</span>
        </span>
        <div className="flex gap-2">
          <div className="w-3 h-3 rounded-full bg-[#ff5f56]"></div>
          <div className="w-3 h-3 rounded-full bg-[#ffbd2e]"></div>
          <div className="w-3 h-3 rounded-full bg-[#27c93f]"></div>
        </div>
      </div>
      
      <div className="flex-grow flex flex-col p-4 bg-[#0d1117] overflow-y-auto relative">
        
        {showSwTutorial && (
          <div className="absolute inset-4 bg-[#0d1117]/95 backdrop-blur-md border border-[#ff5f56] rounded-xl p-6 overflow-y-auto flex flex-col z-10 shadow-2xl">
            <h2 className="text-xl font-bold text-[#ff5f56] mb-4">⚠️ Zablokovaný přístup (Bezpečnostní omezení prohlížeče)</h2>
            <p className="text-[#c9d1d9] mb-4 text-sm leading-relaxed">
              Tato konzolová hra vyžaduje pro běh tzv. <strong>Service Workery</strong>. Tyto komponenty jsou prohlížeči blokovány, pokud web neběží na zabezpečeném protokolu (HTTPS) nebo na localhostu. Protože jste pravděpodobně přistoupili k portálu přes nezabezpečenou lokální IP adresu, prohlížeč to zablokoval.
            </p>
            <h3 className="text-white font-bold mb-2 mt-2">Rychlé řešení (přidání výjimky v prohlížeči):</h3>
            <ul className="text-[#c9d1d9] text-sm space-y-3 pl-0 list-none font-sans">
              <li className="bg-white/5 p-3 rounded border border-white/10">
                <strong className="text-white block mb-1">🌍 Google Chrome / Brave:</strong>
                1. Napište do adresního řádku: <code className="bg-black/50 text-[#ffbd2e] px-1 rounded select-all">chrome://flags/#unsafely-treat-insecure-origin-as-secure</code><br/>
                2. Do vyhledávacího pole vložte aktuální IP adresu tohoto portálu (např. <code>http://172.26.x.x</code>).<br/>
                3. Změňte hodnotu z <i>Disabled</i> na <b>Enabled</b> a restartujte prohlížeč.
              </li>
              <li className="bg-white/5 p-3 rounded border border-white/10">
                <strong className="text-white block mb-1">🌊 Microsoft Edge:</strong>
                Stejný postup jako u Chrome, jen do adresního řádku napište: <code className="bg-black/50 text-[#ffbd2e] px-1 rounded select-all">edge://flags/#unsafely-treat-insecure-origin-as-secure</code>
              </li>
              <li className="bg-white/5 p-3 rounded border border-white/10">
                <strong className="text-white block mb-1">🦊 Mozilla Firefox:</strong>
                1. Otevřete: <code className="bg-black/50 text-[#ffbd2e] px-1 rounded select-all">about:config</code> a přijměte riziko.<br/>
                2. Vyhledejte: <code>dom.serviceWorkers.testing.enabled</code><br/>
                3. Dvojklikem změňte na <b>true</b>. Následně zrušte Private mode.
              </li>
              <li className="bg-white/5 p-3 rounded border border-white/10">
                <strong className="text-white block mb-1">🍎 Safari:</strong>
                Safari obecně nepodporuje Service Workery nad HTTP. Pro Safari musí administrátor zprovoznit HTTPS (např. přes interní DNS a Let's Encrypt).
              </li>
            </ul>
            <div className="mt-6 pt-4 border-t border-white/10">
              <p className="text-xs text-tickle-muted">
                <strong>💡 Tip pro administrátory:</strong> Trvalé řešení bez nutnosti tohoto nastavování u žáků je vygenerovat na serveru (např. v NGINX) SSL certifikát a přistupovat na portál vždy přes `https://`.
              </p>
            </div>
          </div>
        )}

        <pre 
          ref={outputRef} 
          className={`font-mono text-sm text-[#c9d1d9] whitespace-pre-wrap break-words ${showSwTutorial ? 'opacity-20 blur-sm' : ''}`}
        ></pre>
        
        {isWaitingForInput && (
          <form onSubmit={handleInputSubmit} className="mt-2 flex">
            <span className="text-[#58a6ff] font-mono text-sm mr-2">&gt;</span>
            <input
              type="text"
              autoFocus
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              className="flex-grow bg-transparent border-none outline-none font-mono text-sm text-[#58a6ff]"
              spellCheck="false"
              autoComplete="off"
            />
          </form>
        )}
      </div>
    </div>
  );
}
