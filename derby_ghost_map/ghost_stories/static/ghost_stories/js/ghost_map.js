document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    setupLocationCards();
});

function initializeMap() {
    // Get map element and configuration
    const mapElement = document.getElementById('ghost-map');
    if (!mapElement) return;
    
    const centerLat = parseFloat(mapElement.dataset.centerLat) || 52.9225;
    const centerLng = parseFloat(mapElement.dataset.centerLng) || -1.4746;
    const zoomLevel = parseInt(mapElement.dataset.zoom) || 14;
    const apiUrl = mapElement.dataset.apiUrl;
    
    // Create Leaflet map
    const map = L.map('ghost-map').setView([centerLat, centerLng], zoomLevel);
    
    // Add dark-themed map tiles for haunted aesthetic
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19
    }).addTo(map);
    
    // Custom icon for ghost markers
    const ghostIcon = L.icon({
        iconUrl: '/static/ghost_stories/images/ghost-icon.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });
    
    // Fetch location data from API
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // Add GeoJSON features to map
            L.geoJSON(data, {
                pointToLayer: function(feature, latlng) {
                    return L.marker(latlng, {
                        icon: ghostIcon,
                        title: feature.properties.title
                    });
                },
                onEachFeature: function(feature, layer) {
                    // When marker is clicked
                    layer.on('click', function() {
                        showLocationPreview(feature.properties);
                    });
                }
            }).addTo(map);
        })
        .catch(error => {
            console.error('Error loading map data:', error);
        });
    
    // Store map in global variable for later use
    window.ghostMap = map;
}

function showLocationPreview(properties) {
    // Update preview panel with location details
    const previewPanel = document.getElementById('location-preview');
    const previewTitle = document.getElementById('preview-title');
    const previewImage = document.getElementById('preview-image');
    const previewDesc = document.getElementById('preview-description');
    const previewCount = document.getElementById('preview-story-count');
    const viewButton = document.getElementById('view-location-btn');
    
    // Set content
    previewTitle.textContent = properties.title;
    previewDesc.textContent = properties.description;
    previewCount.textContent = properties.story_count;
    
    // Set image if available
    if (properties.image_url) {
        previewImage.innerHTML = `<img src="${properties.image_url}" alt="${properties.title}">`;
    } else {
        previewImage.innerHTML = '<div class="no-image"><i class="fas fa-ghost"></i></div>';
    }
    
    // Set button link
    viewButton.onclick = function() {
        window.location.href = properties.url;
    };
    
    // Show preview panel
    previewPanel.classList.add('active');
    
    // Setup close button
    document.getElementById('close-preview').onclick = function() {
        previewPanel.classList.remove('active');
    };
}

function setupLocationCards() {
    // Allow clicking on location cards to pan map to that location
    const locationCards = document.querySelectorAll('.location-card');
    
    locationCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Don't trigger if clicking on the location link itself
            if (e.target.closest('.location-link')) return;
            
            // Get coordinates from data attributes
            const lat = parseFloat(this.dataset.lat);
            const lng = parseFloat(this.dataset.lng);
            
            // Pan and zoom map if coordinates valid and map exists
            if (!isNaN(lat) && !isNaN(lng) && window.ghostMap) {
                window.ghostMap.setView([lat, lng], 16, {
                    animate: true,
                    duration: 1
                });
                
                // Flash effect on the card
                this.classList.add('highlight');
                setTimeout(() => {
                    this.classList.remove('highlight');
                }, 1500);
            }
        });
    });
}