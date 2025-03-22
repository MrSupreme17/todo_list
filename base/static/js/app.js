if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/static/js/sw.js')  // Update path to match Django static folder
    .then((reg) => console.log('Service Worker registered', reg))
    .catch((err) => console.log('Service Worker not registered', err));
}