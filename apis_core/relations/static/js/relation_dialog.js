function rel_reinit_select2() {
    document.querySelectorAll("[data-autocomplete-light-function]").forEach(element => {
        var dalFunction = $(element).attr('data-autocomplete-light-function');
        if (yl.functions.hasOwnProperty(dalFunction) && typeof yl.functions[dalFunction] == 'function') {
            yl.functions[dalFunction]($, element);
        }
    });
    $('.select2-selection').addClass("form-control");
}

rel_reinit_select2();

document.body.addEventListener("dismissModal", function(evt) {
    document.getElementById("relationdialog").close();
});
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("relationdialog").addEventListener("mousedown", function(evt) {
        evt.target == this && this.close();
    });
});
