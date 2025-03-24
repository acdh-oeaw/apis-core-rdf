document.addEventListener('DOMContentLoaded', function() {
    mapel = document.getElementById("map");
    if (mapel) {
        var map = L.map('map').setView([51.505, -0.09], 13);
        var markers = L.markerClusterGroup();

        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        listitems = mapel.querySelectorAll("li");
        var latlngs = [];
        var markers = L.markerClusterGroup();
        for (const element of listitems) {
            var markercontent = element.innerHTML;
            markers.addLayer(L.marker([element.dataset.latitude, element.dataset.longitude]).bindPopup(markercontent).openPopup());
            latlngs.push([element.dataset.latitude, element.dataset.longitude]);
        }
        map.addLayer(markers);
        var bounds = new L.LatLngBounds(latlngs);
        map.fitBounds(bounds);
    }
});
