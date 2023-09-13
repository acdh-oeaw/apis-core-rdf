from django.db.models.signals import post_save
from django.dispatch import receiver
from apis_core.apis_relations.models import TempTriple
from django.apps import apps


def find_relationtype(tt: TempTriple):
    obj_model = type(tt.obj)
    subj_model = type(tt.subj)
    name = tt.prop.name_forward
    reverse = tt.prop.name_reverse
    for model in apps.get_models():
        if (
            getattr(model, "obj_model", None) == obj_model
            and getattr(model, "subj_model", None) == subj_model
            and getattr(model, "temptriple_name", None) == name
            and getattr(model, "temptriple_name_reverse", None) == reverse
        ):
            print(f"TempTriple {tt.pk} matches with {model}")
            return model
    print("Found none.")
    return None


# this function is a helper function that adds a relation for every legacy temptriple that is created or updated
@receiver(post_save, sender=TempTriple)
def addrelation(sender, instance, created, **kwargs):
    model = find_relationtype(instance)
    if model is not None:
        rel, created = model.objects.get_or_create(
            subj=instance.subj, obj=instance.obj, metadata={"temptriple": instance.pk}
        )
        for field in getattr(model, "temptriple_field_list", []):
            setattr(rel, field, getattr(instance, field, None))
        for field, newfield in getattr(model, "temptriple_field_mapping", {}).items():
            setattr(rel, newfield, getattr(instance, field, None))
        rel.save()
