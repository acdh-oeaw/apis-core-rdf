//script that converts the multi select element
$(document).ready(function() {
    $('select.selectmultiple').multiselect({
        includeSelectAllOption: true,
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true,
        templates: {
            filter: '<div class="multiselect-filter"><div class="input-group input-group-sm p-1"><input class="form-control multiselect-search" type="text" /></div></div>'
        }
    });
})

window.addEventListener('load', () => {
    // scroll-to-top button

    //Get the button
    let mybutton = document.getElementById("btn-back-to-top");

    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function() {
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
})
