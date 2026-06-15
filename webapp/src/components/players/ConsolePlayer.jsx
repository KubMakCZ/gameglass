import { useEffect, useRef, useState } from 'react';
import { storage, BUCKET_ZIPS_ID } from '../../lib/appwrite';
import JSZip from 'jszip';

export default function ConsolePlayer({ game }) {
  const outputRef = useRef(null);
  const workerRef = useRef(null);
  const [status, setStatus] = useState('Inicializace...');
  const [isWaitingForInput, setIsWaitingForInput] = useState(false);
  const [inputValue, setInputValue] = useState('');
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
      
      <div className="flex-grow flex flex-col p-4 bg-[#0d1117] overflow-y-auto">
        <pre 
          ref={outputRef} 
          className="font-mono text-sm text-[#c9d1d9] whitespace-pre-wrap break-words"
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
