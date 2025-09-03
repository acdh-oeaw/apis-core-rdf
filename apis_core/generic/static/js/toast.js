window.addEventListener('load', () => {
    document.querySelectorAll("[data-timeout-close]").forEach((element) => {
        setTimeout(function() {
            element.close();
        }, element.dataset.timeoutClose);
    });
});

function createToast(message) {
    const element = document.querySelector("[data-message-toast]").cloneNode(true)
    delete element.dataset.messagetoast

    document.body.appendChild(element);

    element.className += " alert-" + message.tags

    element.innerHTML = message.message

    element.show()
    setTimeout(function() {
        element.close();
    }, element.dataset.timeoutClose);
}

htmx.on("messages", (event) => {
    event.detail.value.forEach(createToast)
})
