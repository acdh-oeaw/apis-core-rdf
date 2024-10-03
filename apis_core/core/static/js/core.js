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
  // DOM content swapping behaviour
  document.body.addEventListener('htmx:beforeSwap', function(event) {
    if (event.detail.xhr.status === 204) {
      // swap even when the response is empty
      event.detail.shouldSwap = true;
    }
  });
}

/* scroll-to-top button */
function scrollButton() {

  //Get the button
  let mybutton = document.getElementById("btn-back-to-top");

  // When the user scrolls down 20px from the top of the document, show the button
  window.onscroll = function () {
    scrollFunction();
  };

  function scrollFunction() {
    if (
      document.body.scrollTop > 20 ||
      document.documentElement.scrollTop > 20
    ) {
      mybutton.style.display = "block";
    } else {
      mybutton.style.display = "none";
    }
  }
  // When the user clicks on the button, scroll to the top of the document
  mybutton.addEventListener("click", backToTop);

  function backToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  }
}

document.addEventListener("readystatechange", (event) => {
  if (event.target.readyState === "interactive") {
    // equivalent to DOMContentLoaded; document has loaded, defered scripts
    // have downloaded and executed, sub-resources may not be ready yet
  } else if (event.target.readyState === "complete") {
    // fired when fully loaded, incl. sub-resources and async scripts

    configMultiSelect();
    configHtmx();
    scrollButton();
  }
});
