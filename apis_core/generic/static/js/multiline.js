function more(element) {
    input = element.previousElementSibling.cloneNode(true);
    input.value = "";
    element.before(input);
}
