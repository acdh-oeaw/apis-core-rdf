document.body.addEventListener("reinit_select2", function(evt) {
    form = document.getElementById(evt.detail.value);
    form.querySelectorAll(".listselect2").forEach(element => {
        $(element).select2({
            ajax: {
                url: $(element).data("autocomplete-light-url"),
            },
            dropdownParent: $(form),
        });
    });
    $('.select2-selection').addClass("form-control");
});
document.body.addEventListener("dismissModal", function(evt) {
    document.getElementById("relationdialog").close();
});
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("relationdialog").addEventListener("mousedown", function(evt) {
        evt.target == this && this.close();
    });
});
