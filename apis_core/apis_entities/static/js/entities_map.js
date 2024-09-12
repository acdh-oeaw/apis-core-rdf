// we center on vienna first
var map = L.map('map').setView([47.26, 11.3933], 8);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
var markers = document.getElementById("markers");
for (option of markers.options) {
    var longitude = option.dataset.longitude;
    var latitude = option.dataset.latitude;
    if ((latitude > -180 && latitude < 180) && (longitude > -90 && longitude < 90)) {
        var marker = L.marker([latitude, longitude]).addTo(map).bindPopup(option.innerHtml);
    }
}