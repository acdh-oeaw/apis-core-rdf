//script that converts the multi select element
$(document).ready(function() {
    $('select.selectmultiple').multiselect({
        includeSelectAllOption: true,
        enableFiltering: true
    });
})

document.addEventListener("readystatechange", (event) => {
  if (event.target.readyState === "interactive") {
    // equivalent to DOMContentLoaded; document has loaded, defered scripts
    // have downloaded and executed, sub-resources may not be ready yet
  } else if (event.target.readyState === "complete") {
    // fired when fully loaded, incl. sub-resources and async scripts
  }
});
