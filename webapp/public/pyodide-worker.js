importScripts("https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js");

let pyodideReadyPromise;

async function setupPyodide() {
  self.postMessage({ type: 'STATUS', text: 'Načítám Python interpret v izolovaném vlákně...' });
  const pyodide = await loadPyodide();
  
  // Přesměrujeme stdout a stderr jako zprávy hlavnímu vláknu
  pyodide.setStdout({ batched: (msg) => self.postMessage({ type: 'STDOUT', text: msg }) });
  pyodide.setStderr({ batched: (msg) => self.postMessage({ type: 'STDERR', text: msg }) });

  self.postMessage({ type: 'STATUS', text: 'Inicializuji virtuální prostředí...' });
  
  // Nahrajeme vlastní funkci input(), která provede synchronní XHR
  await pyodide.runPythonAsync(`
import builtins
import js
from pyodide.http import pyfetch
import urllib.request

def custom_input(prompt_text=""):
    if prompt_text:
        print(prompt_text, end="")
    
    try:
        import sys
        sys.stdout.flush()
        
        while True:
            xhr = js.XMLHttpRequest.new()
            xhr.open('GET', '/__gameglass_input_wait__', False)
            xhr.send(None)
            
            if xhr.status == 200 and xhr.getResponseHeader('X-GameGlass-Intercepted') == '1':
                return xhr.responseText
            else:
                # Pokud ServiceWorker nebyl aktivní, zkusíme krátký asynchronní sleep přes Python
                # Ale my jsme v synchronní smyčce. Nicméně tento scénář by už díky controllerchange neměl nastat.
                print("Varování: ServiceWorker nezachytil XHR požadavek. Zkouším znovu...")
                import time
                time.sleep(1) # Zpomalí to, aby nám to nevyhodilo stránku, a zkusí to znovu
    except Exception as e:
        print("Input exception:", e)
        return ""

builtins.input = custom_input

import os
def _mock_system(cmd):
    if cmd in ['clear', 'cls']:
        js.postMessage(js.Object.fromEntries([["type", "CLEAR"]]))
    return 0

os.system = _mock_system
  `);

  return pyodide;
}

pyodideReadyPromise = setupPyodide();

self.onmessage = async (event) => {
  if (event.data.type === 'RUN_CODE') {
    const { code, filename } = event.data;
    const pyodide = await pyodideReadyPromise;
    
    try {
      pyodide.FS.writeFile(filename, code);
      self.postMessage({ type: 'STATUS', text: 'Spouštím aplikaci...' });
      await pyodide.runPythonAsync(code);
      self.postMessage({ type: 'DONE', text: '\n[Program úspěšně skončil]' });
    } catch (e) {
      self.postMessage({ type: 'ERROR', text: '\n[CHYBA]\n' + e.message });
    }
  }
};
