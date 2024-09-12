//script that converts the multi select element
$(document).ready(function() {
    $('select.selectmultiple').multiselect({
        includeSelectAllOption: true,
        enableFiltering: true
    });
})
