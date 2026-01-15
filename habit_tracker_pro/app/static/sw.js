const CACHE_NAME = 'habitpro-v2'; // Changed name to force update

// Only cache these critical local files
const LOCAL_ASSETS = [
    '/static/manifest.json',
    '/static/icons/icon-192.png',
    '/static/icons/icon-512.png'
];

self.addEventListener('install', event => {
    self.skipWaiting(); // Force activation
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(LOCAL_ASSETS);
        })
    );
});

self.addEventListener('activate', event => {
    // Clean up old caches immediately
    event.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys.map(key => {
                    if (key !== CACHE_NAME) return caches.delete(key);
                })
            );
        })
    );
    return self.clients.claim();
});

self.addEventListener('fetch', event => {
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});