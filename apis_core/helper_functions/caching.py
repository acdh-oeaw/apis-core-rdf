import importlib
import inspect
from django.contrib.contenttypes.models import ContentType


# global variables used in this module which acts as a singleton
_ontology_classes = None
_ontology_class_names = None
_entity_classes = None
_entity_class_names = None
_reification_classes = None
_reification_class_names = None
_vocabulary_classes = None
_vocabulary_class_names = None
_contenttype_classes = None
_contenttype_class_names = None
_property_autocomplete_choices = None
_class_contenttype_dict = None

def _init_all_ontology_classes():
    """
    internal function that initiales the lists containing all ontology classes (entities,
    reifications, vocabularies)
    
    :return: None
    """
    
    # the imports are done here as this module here might be called before full Django
    # initialization. Otherwise, it would break.
    from apis_ontology import models as ontology_models
    from apis_core.apis_entities.models import AbstractEntity, TempEntityClass
    from apis_core.apis_relations.models import AbstractReification
    from apis_core.apis_vocabularies.models import AbstractVocabulary
    
    global _ontology_classes
    global _ontology_class_names
    global _entity_classes
    global _entity_class_names
    global _reification_classes
    global _reification_class_names
    global _vocabulary_classes
    global _vocabulary_class_names
    if (
        _ontology_classes is not None
        or _ontology_class_names is not None
        or _entity_classes is not None
        or _entity_class_names is not None
        or _reification_classes is not None
        or _reification_class_names is not None
        or _vocabulary_classes is not None
        or _vocabulary_class_names is not None
    ):
        raise Exception("initialization is called but some variables are already initialized.")
    _ontology_classes = []
    _ontology_class_names = []
    _entity_classes = []
    _entity_class_names = []
    _reification_classes = []
    _reification_class_names = []
    _vocabulary_classes = []
    _vocabulary_class_names = []

    try:
        from apis_ontology import models as ontology_models
    except ImportError:
        pass
    else:
        # iterate over classes in apis_ontology.models, and differentiate them by their parents
        for ontology_class_name, ontology_class in inspect.getmembers(ontology_models, inspect.isclass):
            if (
                issubclass(ontology_class, AbstractEntity)
                and not ontology_class._meta.abstract
                and ontology_class is not TempEntityClass # TODO RDF: remove this once TempEntityClass is removed
            ):
                _entity_classes.append(ontology_class)
                _entity_class_names.append(ontology_class_name.lower())
            elif (
                issubclass(ontology_class, AbstractReification)
                and not ontology_class._meta.abstract
            ):
                _reification_classes.append(ontology_class)
                _reification_class_names.append(ontology_class_name.lower())
            elif (
                issubclass(ontology_class, AbstractVocabulary)
                and not ontology_class._meta.abstract
            ):
                _vocabulary_classes.append(ontology_class)
                _vocabulary_class_names.append(ontology_class_name.lower())
        _ontology_classes = _entity_classes + _reification_classes + _vocabulary_classes
        _ontology_class_names = _entity_class_names + _reification_class_names + _vocabulary_class_names

def get_all_ontology_classes():
    if _ontology_classes is None:
        _init_all_ontology_classes()
    
    return _ontology_classes


def get_all_ontology_class_names():
    if _ontology_class_names is None:
        _init_all_ontology_classes()
    
    return _ontology_class_names


def get_ontology_class_of_name(ontology_name_str):
    """
    Look up an ontology class based on a given name.

    :param ontology_name_str: a string to compare against classes' __name__
                        values; need not be formatted (letter case does
                        not matter)
    :return: an ontology class – or raise exception
    """
    for ontology_class in get_all_ontology_classes():
        if ontology_class.__name__.lower() == ontology_name_str.lower():
            return ontology_class
    
    raise Exception("Could not find ontology class of name:", ontology_name_str)


def get_all_entity_classes():
    if _entity_classes is None:
        _init_all_ontology_classes()
    
    return _entity_classes


def get_all_entity_class_names():
    if _entity_class_names is None:
        _init_all_ontology_classes()
    
    return _entity_class_names


def get_entity_class_of_name(entity_name_str):
    """
    Look up an entity class based on a given name.

    :param entity_name_str: a string to compare against classes' __name__
                        values; need not be formatted (letter case does
                        not matter)
    :return: an entity class – or raise exception
    """
    for entity_class in get_all_entity_classes():
        if entity_class.__name__.lower() == entity_name_str.lower():
            return entity_class

    raise Exception("Could not find entity class of name:", entity_name_str)


def get_all_reification_classes():
    if _reification_classes is None:
        _init_all_ontology_classes()
    
    return _reification_classes


def get_all_reification_class_names():
    if _reification_class_names is None:
        _init_all_ontology_classes()
    
    return _reification_class_names


def get_reification_class_of_name(reification_name_str):
    """
    Look up a reification class based on a given name.

    :param reification_name_str: a string to compare against classes' __name__
                        values; need not be formatted (letter case does
                        not matter)
    :return: an reification class – or raise exception
    """
    for reification_class in get_all_reification_classes():
        if reification_class.__name__.lower() == reification_name_str.lower():
            return reification_class
    
    raise Exception("Could not find reification class of name:", reification_name_str)


def get_autocomplete_property_choices(model_self_class_str, model_other_class_str, search_name_str):
    """
    A function to cache for user search string in property autocomplete fields.
    WARNING: This will not work when properties are edited during runtime!
    But since properties are part of the ontology they should not be changed during runtime anyway.
    
    :param model_self_class_str: entity class from which side we are looking for
    :param model_other_class_str: related entity class for which suitable properties are searched
    :param search_name_str: search string provided by user
    :return: a list of choices in the format which is used by the django-autocomplete field
    """
    from apis_core.apis_entities.autocomplete3 import PropertyAutocomplete

    global _property_autocomplete_choices
    if _property_autocomplete_choices is None:
        _property_autocomplete_choices = {}
    res = _property_autocomplete_choices.get(
        (model_self_class_str, model_other_class_str, search_name_str)
    )
    if res is not None:
        return res
    else:
        model_self_contenttype = get_contenttype_of_class(get_ontology_class_of_name(
            model_self_class_str
        ))
        model_other_contenttype = get_contenttype_of_class(get_ontology_class_of_name(
            model_other_class_str
        ))
        from apis_core.apis_relations.models import Property
        rbc_self_subj_other_obj = Property.objects.filter(
            subj_class=model_self_contenttype,
            obj_class=model_other_contenttype,
            name__icontains=search_name_str
        )
        rbc_self_obj_other_subj = Property.objects.filter(
            subj_class=model_other_contenttype,
            obj_class=model_self_contenttype,
            name_reverse__icontains=search_name_str
        )
        choices = []
        # The Select2ListView class when finding results for some user input, returns these
        # results in this 'choices' list. This is a list of dictionaries, where each dictionary
        # has an id and a text. In our case however the results can come from two different sets:
        # the one where result hits match on the forward name of a property and the other set
        # where the result hits match on the reverse name. These hits need to re-used later,
        # but additionally the direction of the property is also needed later to persist it
        # correctly (e.g. when creating a triple between two persons, where one is the mother and
        # the other is the daughter, then the property direction is needed). I could not find a
        # way to return in this function a choices list with dictionaries or something else,
        # that would pass additional data. So I am misusing the 'id' item in the dictionary by
        # encoding the id and the direction into a string which will be parsed and split later on.
        for rbc in rbc_self_subj_other_obj:
            choices.append(
                {
                    # misuse of the id item as explained above
                    'id': f"id:{rbc.pk}__direction:{PropertyAutocomplete.SELF_SUBJ_OTHER_OBJ_STR}",
                    'text': rbc.name
                }
            )
        for rbc in rbc_self_obj_other_subj:
            choices.append(
                {
                    # misuse of the id item as explained above
                    'id': f"id:{rbc.pk}__direction:{PropertyAutocomplete.SELF_OBJ_OTHER_SUBJ_STR}",
                    'text': rbc.name_reverse
                }
            )
        _property_autocomplete_choices[
            (model_self_class_str, model_other_class_str, search_name_str)
        ] = choices
        
        return choices


def get_all_contenttype_classes():
    """
    Return a list of all Django Contenttype classes.
    """
    
    def init_contenttype_classes():
        """
        Iterate through a list of modules and filter for
        - classes
        - which are not abstract
        - except for those explicitly ignored (via models_exclude list).
        """
        global _contenttype_classes
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
        if _contenttype_classes is not None:
            r2 = []
            for c in _contenttype_classes:
                for c2 in apis_modules:
                    if c in c2:
                        r2.append(c2)
            apis_modules = r2
        # this is a hack, because the `apis_modules` are hardcoded, up there
        # but there is no guarantee that all of them are available
        lst_cont_pre = []
        for module in apis_modules:
            try:
                lst_cont_pre.append(importlib.import_module(module))
            except ImportError:
                pass
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
        _contenttype_classes = lst_cont
        
    if _contenttype_classes is None:
        init_contenttype_classes()

    return _contenttype_classes


def get_all_class_modules_and_names():
    """
    :return: a list of tuples where each contains a str for the app label and a str for the class
    """
    
    global _contenttype_class_names
    if _contenttype_class_names is None:
        _contenttype_class_names = []
        for cls in get_all_contenttype_classes():
            _contenttype_class_names.append((cls.__module__.split(".")[-2], cls.__name__))
            
    return _contenttype_class_names


def get_contenttype_of_class(model_class):
    """
    Helper method which caches ContentType of a given model class. When first called on a model, it
    fetches its respective ContentType from the DB and caches it in a class dictionary. Later, this
    dictionary is called.

    :param model_class: django model class
    :return: ContentType class representing the model class
    """

    global _class_contenttype_dict
    if _class_contenttype_dict is None:
        _class_contenttype_dict = {}
    if model_class not in _class_contenttype_dict:
        _class_contenttype_dict[model_class] = ContentType.objects.get(model=model_class.__name__)
    
    return _class_contenttype_dict[model_class]
