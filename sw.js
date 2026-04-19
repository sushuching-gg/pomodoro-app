const CACHE_NAME = 'pomodoro-v1';
const ASSETS = [
  './pomodoro.html',
  './manifest.json',
  './resized_transparent.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((res) => res || fetch(e.request))
  );
});
