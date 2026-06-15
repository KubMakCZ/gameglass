importScripts("https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js");

let pyodide = null;
let inputBuffer = null;
let inputView = null;

self.onmessage = async (event) => {
  const msg = event.data;

  if (msg.type === "INIT") {
    inputBuffer = msg.inputBuffer;
    inputView = new Int32Array(inputBuffer);
    
    try {
      pyodide = await loadPyodide({
        stdout: (text) => self.postMessage({ type: 'STDOUT', text }),
        stderr: (text) => self.postMessage({ type: 'STDERR', text }),
        stdin: () => {
          // Send request for input
          self.postMessage({ type: 'REQUEST_INPUT' });
          
          // Wait synchronously on the SharedArrayBuffer until main thread sets index 0 to 1
          Atomics.wait(inputView, 0, 0);
          
          // Read the string length from index 1
          const length = inputView[1];
          let result = "";
          // Read characters from index 2 onwards
          for (let i = 0; i < length; i++) {
            result += String.fromCharCode(inputView[2 + i]);
          }
          
          // Reset status to 0 (waiting)
          inputView[0] = 0;
          return result;
        }
      });
      self.postMessage({ type: 'READY' });
    } catch (e) {
      self.postMessage({ type: 'ERROR', text: e.message });
    }
  }

  if (msg.type === "RUN") {
    try {
      // Mock the os.system calls to prevent exceptions when students use 'clear'
      await pyodide.runPythonAsync(`
import sys
import os
def _mock_system(cmd):
    if cmd in ['clear', 'cls']:
        # Emit a special clear token that the frontend terminal understands
        print(chr(27) + "[2J" + chr(27) + "[3J" + chr(27) + "[H", end="")
        sys.stdout.flush()
    return 0
os.system = _mock_system
      `);
      
      // Write the user code to virtual filesystem and execute
      pyodide.FS.writeFile(msg.filename, msg.code);
      await pyodide.runPythonAsync(msg.code);
      self.postMessage({ type: 'DONE' });
    } catch (e) {
      self.postMessage({ type: 'ERROR', text: e.message });
    }
  }
};
