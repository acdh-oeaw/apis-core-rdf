/*
 * show a map in a popover
 */
function showMap(element) {
    document.querySelectorAll(".popovermap").forEach(el => el.remove());

    let map;

    let rect = element.getBoundingClientRect();
    let pTop = rect.top + window.scrollY - 250;
    let pLeft = rect.left + window.scrollX - 550;

    let mapDiv = document.createElement("div");
    mapDiv.classList.add("popovermap");
    mapDiv.setAttribute("id", "popovermap");

    mapDiv.style.position = "absolute";
    mapDiv.style.top = pTop + "px";
    mapDiv.style.left = pLeft + "px";

    document.body.appendChild(mapDiv);

    if (typeof map !== "undefined") {
        map.off();
        map.remove();
    }

    map = L.map('popovermap', {
        center: [parseInt(element.dataset.latitude), parseInt(element.dataset.longitude)],
        zoom: 5
    });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    L.marker([parseInt(element.dataset.latitude), parseInt(element.dataset.longitude)]).addTo(map);
}

function delMap(element) {
    document.querySelectorAll(".popovermap").forEach(el => el.remove());
}
