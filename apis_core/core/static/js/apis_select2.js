/*!
 * Django Autocomplete Light APIS Override - Select2 function
 * This JS File is based on `dal_select2/static/autocomplete_light/select2.js` from Django Autocomplete Light.
 * We use it to register our own dal function `apis_select2` which changes 2 things from the one from upstream:
 * * it modifies the ajax.processResults function to not overwrite the value.id
 * * it passes the dropdownParent argument to select2 to make the select2 dropdown part of the same form as
 *   the original select input instead of putting it at the end of the page
 *   (See: https://select2.org/dropdown#dropdown-placement)
 */

document.addEventListener('dal-init-function', function() {

    yl.registerFunction('apis_select2', function($, element) {

        var $element = $(element);

        // Templating helper
        function template(text, is_html) {
            if (is_html) {
                var $result = $('<span>');
                $result.html(text);
                return $result;
            } else {
                return text;
            }
        }

        function result_template(item) {
            var is_data_html = ($element.attr('data-html') !== undefined || $element.attr('data-result-html') !== undefined)

            if (item.create_id) {
                var $result = $('<span>').addClass('dal-create');
                if (is_data_html) {
                    return $result.html(item.text);
                } else {
                    return $result.text(item.text);
                }
            } else {
                return template(item.text, is_data_html);
            }
        }

        function selected_template(item) {
            if (item.selected_text !== undefined) {
                return template(item.selected_text,
                    $element.attr('data-html') !== undefined || $element.attr('data-selected-html') !== undefined
                );
            } else {
                return result_template(item);
            }
            return
        }

        var ajax = null;
        if ($element.attr('data-autocomplete-light-url')) {
            ajax = {
                url: $element.attr('data-autocomplete-light-url'),
                dataType: 'json',
                delay: 250,

                data: function(params) {
                    var data = {
                        q: params.term, // search term
                        page: params.page,
                        create: $element.attr('data-autocomplete-light-create') && !$element.attr('data-tags'),
                        forward: yl.getForwards($element)
                    };

                    return data;
                },
                processResults: function(data, page) {
                    if ($element.attr('data-tags')) {
                        $.each(data.results, function(index, value) {
                            value.id = value.id;
                        });
                    }

                    return data;
                },
                cache: true
            };
        }
        use_tags = false;
        tokenSeparators = null;
        // Option 1: 'data-tags'
        if ($element.attr('data-tags')) {
            tokenSeparators = [','];
            use_tags = true;
        }
        // Option 2: 'data-token-separators'
        if ($element.attr('data-token-separators')) {
            use_tags = true
            tokenSeparators = $element.attr('data-token-separators')
            if (tokenSeparators == 'null') {
                tokenSeparators = null;
            }
        }
        $element.select2({
            tokenSeparators: tokenSeparators,
            debug: true,
            containerCssClass: ':all:',
            placeholder: $element.attr('data-placeholder') || '',
            language: $element.attr('data-autocomplete-light-language'),
            minimumInputLength: $element.attr('data-minimum-input-length') || 0,
            allowClear: !$element.is('[required]'),
            templateResult: result_template,
            templateSelection: selected_template,
            ajax: ajax,
            with: null,
            tags: use_tags,
            dropdownParent: $(element.form),
        });

        $element.on('select2:selecting', function(e) {
            var data = e.params.args.data;

            if (data.create_id !== true)
                return;

            e.preventDefault();
            e.stopImmediatePropagation();

            var select = $element;

            $.ajax({
                url: $element.attr('data-autocomplete-light-url'),
                type: 'POST',
                dataType: 'json',
                data: {
                    text: data.id,
                    forward: yl.getForwards($element)
                },
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", document.csrftoken);
                },
                success: function(data, textStatus, jqXHR) {
                    if ('error' in data) {
                        error = data['error']
                        document.querySelectorAll(".invalid-feedback").forEach(el => el.remove());
                        now = new Date();
                        date = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds()
                        $('.dal-create').append(
                            `<p class="invalid-feedback d-block">${date}: <strong>${error}</strong>`
                        );

                    } else {
                        select.append(
                            $('<option>', {
                                value: data.id,
                                text: data.text,
                                selected: true
                            })
                        );
                        select.trigger('change');
                        select.select2('close');
                    }
                }
            });
        });
    });
})
