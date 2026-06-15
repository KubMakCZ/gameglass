self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

let inputRequests = {};

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  if (url.pathname === '/__gameglass_input_wait__') {
    event.respondWith(new Promise(resolve => {
      // Uložíme resolve funkci, kterou zavoláme, až přijde zpráva od klienta
      inputRequests['input'] = resolve;
      
      // Pošleme zprávu klientům, že potřebujeme vstup
      self.clients.matchAll().then(clients => {
        clients.forEach(client => client.postMessage({ type: 'INPUT_REQUEST' }));
      });
    }));
  }
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'INPUT_RESPONSE') {
    const resolve = inputRequests['input'];
    if (resolve) {
      resolve(new Response(event.data.text, { 
        status: 200,
        headers: { 'X-GameGlass-Intercepted': '1' }
      }));
      delete inputRequests['input'];
    }
  }
});
