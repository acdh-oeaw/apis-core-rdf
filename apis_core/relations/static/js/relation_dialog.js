function successFunction(data, textStatus, jqXHR) {
	if ('error' in data) {
		error = data['error']
                        $('.dal-create').append(
                            `<p class="invalid-feedback d-block""><strong>${error}</strong>`
                        );

                    } else {
                        select.append(
                            $('<option>', {value: data.id, text: data.text, selected: true})
                        );
                        select.trigger('change');
                        select.select2('close');
                    }
}
function tohtml(item) {
    const span = document.createElement('span');
    span.innerHTML = item.text;
    return span;
}

function rel_reinit_select2() {
    document.querySelectorAll(".listselect2, .modelselect2multiple, .modelselect2").forEach(element => {
        $(element).select2({
            ajax: {
                url: $(element).data("autocomplete-light-url"),
            },
            dropdownParent: $(element.form),
            templateResult: tohtml,
            templateSelection: tohtml,
	    success: successFunction,
        });
    });
    $('.select2-selection').addClass("form-control");
}

rel_reinit_select2();

document.body.addEventListener("reinit_select2", function(evt) {
    rel_reinit_select2();
});
document.body.addEventListener("dismissModal", function(evt) {
    document.getElementById("relationdialog").close();
});
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("relationdialog").addEventListener("mousedown", function(evt) {
        evt.target == this && this.close();
    });
});
