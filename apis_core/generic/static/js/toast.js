window.addEventListener('load', () => {
    document.querySelectorAll(".mytoast").forEach((element) => {
        element.addEventListener('animationend', function(e) {
            e.animationName == "fadeout" && element.close();
        });
    });
});

function createToast(message) {
    const element = document.querySelector("[data-message-toast]").cloneNode(true)
    delete element.dataset.messagetoast

    document.getElementById("snackbar").appendChild(element);

    element.className += " alert-" + message.tags

    element.innerHTML = message.message

    element.show()
    element.addEventListener('animationend', function(e) {
        e.animationName == "fadeout" && element.close();
    });
}

htmx.on("messages", (event) => {
    event.detail.value.forEach(createToast)
})
