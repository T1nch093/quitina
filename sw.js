/* Quitina: guarda el juego en el teléfono. Primero intenta la red (para recibir actualizaciones) y si no hay conexión usa lo guardado. */
const CACHE = 'quitina-v26';
const CORE = ['./', 'index.html', 'manifest.webmanifest', 'assets/mantis-arte.jpg', 'assets/mantis-sprites.webp', 'assets/mantis-sprites.json', 'icons/icon-192.png', 'icons/icon-512.png', 'assets/iconos.webp'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(fetch(e.request).then(r => {
    if (r.ok && (new URL(e.request.url).origin === location.origin || e.request.url.includes('fonts.g'))) { const cp = r.clone(); caches.open(CACHE).then(c => c.put(e.request, cp)); }
    return r;
  }).catch(() => caches.match(e.request, {ignoreSearch: true})));
});
