import importlib
import inspect

from django.contrib.contenttypes.models import ContentType
from django.db.models.base import ModelBase


class GetContentTypes:

    # class member dict for caching ContentType objects in
    # get_content_type_of_class_or_instance method
    class_content_type_dict = {}

    def get_names(self):
        """
        Create tuples from a list of model classes to store their module names
        and class names (as strings).

        :return: a list of tuples
        """
        res = []
        for cls in self._lst_cont:
            res.append((cls.__module__.split(".")[-2], cls.__name__))
        return res

    def get_model_classes(self):
        """
        Return a list of Django model classes.
        """
        return self._lst_cont

    @classmethod
    def get_content_type_of_class_or_instance(cls, model_class_or_instance):
        """
        Helper method which caches ContentType of a given model class or instance.
        When first called on a model, it fetches its respective ContentType from the DB
        and caches it in a class dictionary. Later, this dictionary is called.

        :param model_class_or_instance: model class or instance of a model class
        :return: dictionary holding Django ContentType object
        """

        if type(model_class_or_instance) is ModelBase:
            # true if model_class_or_instance is model class
            model_class = model_class_or_instance
        elif type(type(model_class_or_instance)) is ModelBase:
            # true if model_class_or_instance is model instance
            model_class = type(model_class_or_instance)
        else:
            raise Exception(
                f"Passed argument is neither model class nor model instance: {type(model_class_or_instance)}"
            )

        if model_class not in cls.class_content_type_dict:
            cls.class_content_type_dict[model_class] = ContentType.objects.get(
                model=model_class.__name__
            )
        return cls.class_content_type_dict[model_class]

    def __init__(self, lst_conts: list = None):
        """
        Iterate through a list of modules and filter for
        - classes
        - which are not abstract
        - except for those explicitly ignored (via models_exclude list).

        :param lst_conts: (optional) list of paths to app models, in form of strings,
                          e.g. "apis_core.apis_entities.models".
                          By default, apis_core models are iterated over.
        """
        models_exclude = [
            "texttype_collections",
            "relationbaseclass",
            "baserelationmanager",
            "relationpublishedqueryset",
            "inheritanceforwardmanytoonedescriptor",
            "inheritanceforeignkey",
        ]
        apis_modules = [
            "apis_core.apis_metainfo.models",
            "apis_core.apis_vocabularies.models",
            "apis_core.apis_entities.models",
            "apis_core.apis_relations.models",
            "apis_ontology.models",
        ]
        if lst_conts is not None:
            r2 = []
            for c in lst_conts:
                for c2 in apis_modules:
                    if c in c2:
                        r2.append(c2)
            apis_modules = r2
        lst_cont_pre = [importlib.import_module(x) for x in apis_modules]
        lst_cont = []
        for m in lst_cont_pre:
            for cls_n in dir(m):
                if not cls_n.startswith("__") and "__module__" in list(
                    dir(getattr(m, cls_n))
                ):
                    if (
                        getattr(m, cls_n).__module__ in apis_modules
                        and getattr(m, cls_n) not in lst_cont
                        and cls_n.lower() not in models_exclude
                        and inspect.isclass(getattr(m, cls_n))
                        and getattr(m, cls_n)._meta.abstract is False
                    ):
                        lst_cont.append(getattr(m, cls_n))
        lst_cont.append(ContentType)
        self._lst_cont = lst_cont
