How to test:

create a model that inherits from `apis_core.relations.models.Relation`.
The model will have to have the attribute `subj_model` and `obj_model` which point
to some Django model (can also be a list of Django models).
You can define the class methods `name` and `reverse_name` to provide human readable
strings for your relation model. They defaulto to the `verbose_name` and the
`verbose_name` with the string ` reverse` appended.

Now you can create instances of that relation on your entity pages.
