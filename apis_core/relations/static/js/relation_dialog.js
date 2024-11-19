function tohtml(item) {
    const span = document.createElement('span');
    span.innerHTML = item.text;
    return span;
}
document.body.addEventListener("reinit_select2", function(evt) {
    form = document.getElementById(evt.detail.value);
    form.querySelectorAll(".listselect2, .modelselect2multiple, .modelselect2").forEach(element => {
        $(element).select2({
            ajax: {
                url: $(element).data("autocomplete-light-url"),
            },
            dropdownParent: $(form),
            templateResult: tohtml,
            templateSelection: tohtml,
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
