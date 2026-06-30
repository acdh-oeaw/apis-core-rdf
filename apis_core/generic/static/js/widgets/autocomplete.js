function activateClickedSuggestion(element) {
  wrapper = element.parentElement.parentElement;
  wrapper.querySelector("input[type='hidden']").value = element.dataset.url;
  wrapper.querySelector("input:not([type='hidden'])").value = element.dataset.title;
}
document.addEventListener('click', function(event) {
  if (!event.target.matches("#autocomplete")) {
    suggestions = document.getElementsByClassName('suggestions-dropdown');
    for (let i = 0; i < suggestions.length; i++) {
      suggestions[i].innerHTML = '';
    }
  }
});
