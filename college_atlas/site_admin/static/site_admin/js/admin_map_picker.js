document.addEventListener('DOMContentLoaded', function() {
    const latInput = document.getElementById('id_latitude');
    const latInput = document.getElementById('id_latitude');
    const lngInput = document.getElementById('id_longitude');
    
    if (!latInput || !lngInput) {
        return; // Not on a page with lat/long inputs
    }

    // Create a container for the map
    const mapDiv = document.createElement('div');
    mapDiv.id = 'admin-map';
    mapDiv.style.height = '400px';
    mapDiv.style.width = '100%';
    mapDiv.style.marginBottom = '20px';
    mapDiv.style.marginTop = '20px';
    mapDiv.style.borderRadius = '8px';
    mapDiv.style.zIndex = '0';

    const latRow = latInput.closest('.form-row');
    if (latRow) {
        latRow.parentNode.insertBefore(mapDiv, latRow);
    } else {
        latInput.parentNode.insertBefore(mapDiv, latInput);
    }

    let initialLat = parseFloat(latInput.value) || 37.0902;
    let initialLng = parseFloat(lngInput.value) || -95.7129;
    let initialZoom = latInput.value && lngInput.value ? 13 : 4;

    const map = L.map('admin-map').setView([initialLat, initialLng], initialZoom);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    let marker;

    if (latInput.value && lngInput.value) {
        marker = L.marker([initialLat, initialLng], {draggable: true}).addTo(map);
    }

    map.on('click', function(e) {
        const { lat, lng } = e.latlng;
        
        if (marker) {
            marker.setLatLng(e.latlng);
        } else {
            marker = L.marker(e.latlng, {draggable: true}).addTo(map);
        }

        latInput.value = lat.toFixed(6);
        lngInput.value = lng.toFixed(6);
    });

    if (marker) {
         marker.on('dragend', function(e) {
            const { lat, lng } = e.target.getLatLng();
            latInput.value = lat.toFixed(6);
            lngInput.value = lng.toFixed(6);
        });
    }
    
    map.on('click', function(e) {
        if (marker) {
             marker.off('dragend');
             marker.on('dragend', function(event) {
                const { lat, lng } = event.target.getLatLng();
                latInput.value = lat.toFixed(6);
                lngInput.value = lng.toFixed(6);
             });
        }
    });

    function updateMapFromInputs() {
        const lat = parseFloat(latInput.value);
        const lng = parseFloat(lngInput.value);
        
        if (!isNaN(lat) && !isNaN(lng)) {
            const newLatLng = [lat, lng];
            if (marker) {
                marker.setLatLng(newLatLng);
            } else {
                 marker = L.marker(newLatLng, {draggable: true}).addTo(map);
                 marker.on('dragend', function(event) {
                    const { lat, lng } = event.target.getLatLng();
                    latInput.value = lat.toFixed(6);
                    lngInput.value = lng.toFixed(6);
                 });
            }
            map.panTo(newLatLng);
        }
    }

    latInput.addEventListener('change', updateMapFromInputs);
    lngInput.addEventListener('change', updateMapFromInputs);
});
