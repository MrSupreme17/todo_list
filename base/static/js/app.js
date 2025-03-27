// Check if the browser supports Service Workers
if ('serviceWorker' in navigator) {
  
  // Register the Service Worker for offline functionality
  navigator.serviceWorker.register('/static/js/sw.js')  // Update path to match Django static folder
    .then((reg) => console.log('Service Worker registered', reg))  // Log success message if registration works
    .catch((err) => console.log('Service Worker not registered', err));  // Log error if registration fails
}
