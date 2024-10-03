/* config for bootstrap-multiselect widget,
see also https://davidstutz.github.io/bootstrap-multiselect/#configuration-options
*/
function configMultiSelect() {
  $('select.selectmultiple').multiselect({
    includeSelectAllOption: true,
    enableFiltering: true
  });
}

/* config HTMX events,
* see also https://htmx.org/events/
*/
function configHtmx() {
  document.body.addEventListener('htmx:beforeSwap', function(event) {
    if (event.detail.xhr.status === 204) {
      // Swap content even when the response is empty.
      event.detail.shouldSwap = true;
    }
  });
}

document.addEventListener("readystatechange", (event) => {
  if (event.target.readyState === "interactive") {
    // equivalent to DOMContentLoaded; document has loaded, defered scripts
    // have downloaded and executed, sub-resources may not be ready yet
  } else if (event.target.readyState === "complete") {
    // fired when fully loaded, incl. sub-resources and async scripts

    configMultiSelect();
    configHtmx();
  }
});
