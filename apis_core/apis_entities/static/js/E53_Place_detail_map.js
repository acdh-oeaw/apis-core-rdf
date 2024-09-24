document.addEventListener('DOMContentLoaded', function() {
    mapel = document.getElementById("map");
    if (mapel) {
        var markercontent = mapel.innerHTML;
        var map = L.map('map').setView([mapel.dataset.latitude, mapel.dataset.longitude], 13);

        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        L.marker([mapel.dataset.latitude, mapel.dataset.longitude]).addTo(map).bindPopup(markercontent).openPopup();
    }
});
