$(document).ready(function() {
    $(document).on('submit', 'form.form.ajax_form', unbind_ajax_forms);
});

function unbind_ajax_forms(event) {
    $(this).find('button').attr('disabled', true);
    event.preventDefault();
    event.stopPropagation();
    var formData = $(this).serialize();
    //var button_text = $(this).find(':button').text();
    $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            beforeSend: function(request) {
                var csrftoken = getCookie('csrftoken');
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            //data:formData,
        })
        .done(function(response) {
            window[response.call_function](response)
        })
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
