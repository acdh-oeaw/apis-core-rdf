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
        mapel.map = L.map('map').setView([0, 0], 2);

        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(mapel.map);

        mapel.map.on('popupopen', function(e) {
            feature = e.popup._source.feature;
            [longitude, latitude] = feature.geometry.coordinates;
            label_input = document.getElementById("id_label");
            label_input.value = feature.properties.display_name;
            latitude_input = document.getElementById("id_latitude");
            latitude_input.value = latitude;
            longitude_input = document.getElementById("id_longitude");
            longitude_input.value = longitude;
        });

    }
});
