from django.db import models

from apis_core.generic.forms.widgets import NewlineSeparatedListWidget


class NewlineSeparatedListField(models.TextField):
    """
    This field is basically a textfield with a custom widget.
    It uses the NewlineSeparatedListWidget to provide a simply way
    for users to enter multiple values without having to think about
    the separator.
    """

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        kwargs["widget"] = NewlineSeparatedListWidget(attrs={"class": "mb-1"})
        return super().formfield(
            form_class=form_class, choices_form_class=choices_form_class, **kwargs
        )
