function fetchResults(input_id) {
    input = document.getElementById(input_id);
    fetch("https://nominatim.openstreetmap.org/search?format=geojson&layer=address&q=" + input.value)
        .then(response => response.json())
        .then(data => redrawMap(data))
        .catch(error => console.error('Error:', error));
}

function redrawMap(featurecollection) {
    mapel = document.getElementById("map");
    if (mapel) {
        if (mapel.markers) {
            mapel.markers.clearLayers();
        }
        mapel.markers = L.layerGroup();

        var feature = L.geoJSON(featurecollection.features, {
            onEachFeature: onEachFeature
        }).addTo(mapel.markers);
        mapel.map.fitBounds(feature.getBounds());
        mapel.markers.addTo(mapel.map);
    }
}

function onEachFeature(feature, layer) {
    if (feature.properties.display_name) {
        layer.bindPopup(feature.properties.display_name);
    }
}
document.addEventListener('DOMContentLoaded', function() {
    /* rematch the Enter key for all the placelookup inputs -
     * they should trigger a search and not a form submit */
    document.querySelectorAll('input.placelookup').forEach((input) =>
        input.onkeydown = function(e) {
            if (e.key == 'Enter') {
                fetchResults(input.id);
                return false;
            }
        }
    );
    mapel = document.getElementById("map");
    if (mapel) {
        [lng, lat, zoom, label] = [0, 0, 2, ""];
        lng_input = document.getElementById(mapel.dataset.longitudeId);
        if (lng_input && lng_input.value) {
            lng = parseFloat(lng_input.value);
        }
        lat_input = document.getElementById(mapel.dataset.latitudeId);
        if (lat_input && lat_input.value) {
            lat = parseFloat(lat_input.value);
        }
        label_input = document.getElementById(mapel.dataset.labelId);
        if (label_input && label_input.value) {
            label = label_input.value;
        }
        if (lat && lng) {
            zoom = 11
        };

        mapel.map = L.map('map').setView([lat, lng], zoom);

        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(mapel.map);
        mapel.marker = new L.Marker([lat, lng]);
        if (lat && lng) {
            mapel.marker.addTo(mapel.map)
        }

        mapel.map.on('popupopen', function(e) {
            if (label_input && label == "") {
                label_input.value = e.popup.getContent();
            }

            coordinates = e.popup.getLatLng();
            if (lat_input) {
                lat_input.value = coordinates.lat;
            }
            if (lng_input) {
                lng_input.value = coordinates.lng;
            }
        });

        mapel.map.on('contextmenu', function(e) {
            mapel.marker.closePopup();
            mapel.marker.setLatLng([e.latlng.lat, e.latlng.lng]);
            mapel.marker.addTo(mapel.map);
            display_name = "Unlabelled place: " + e.latlng.lat + ", " + e.latlng.lng;
            fetch("https://nominatim.openstreetmap.org/reverse?format=json&lat=" + e.latlng.lat + "&lon=" + e.latlng.lng)
                .then(response => response.json())
                .then(data => {
                    mapel.marker.bindPopup(data.display_name);
                })
                .catch(error => {
                    mapel.marker.bindPopup(display_name)
                });
        });

    }
});
