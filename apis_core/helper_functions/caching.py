import inspect


_all_ontology_classes = None
_all_ontology_class_names = None
_all_entity_classes = None
_all_entity_class_names = None
_all_reification_classes = None
_all_reification_class_names = None
_all_vocabulary_classes = None
_all_vocabulary_class_names = None
_cached_property_choices_dict = None
_has_been_initialized = False

def initialize_all():
    from apis_ontology import models as ontology_models
    from apis_core.apis_entities.models import AbstractEntity, TempEntityClass
    from apis_core.apis_relations.models import AbstractReification
    from apis_core.apis_vocabularies.models import AbstractVocabulary
    
    global _all_ontology_classes
    global _all_ontology_class_names
    global _all_entity_classes
    global _all_entity_class_names
    global _all_reification_classes
    global _all_reification_class_names
    global _all_vocabulary_classes
    global _all_vocabulary_class_names
    global _cached_property_choices_dict
    global _has_been_initialized
    if _has_been_initialized:
        raise Exception(
            "The function initialize_all has already been called, but it should only be called "
            "once. Investigate into this second call and avoid it."
        )
    _has_been_initialized = True
    _all_entity_classes = []
    _all_entity_class_names = []
    _all_reification_classes = []
    _all_reification_class_names = []
    _all_vocabulary_classes = []
    _all_vocabulary_class_names = []
    _cached_property_choices_dict = {}
    for ontology_class_name, ontology_class in inspect.getmembers(ontology_models, inspect.isclass):
        if (
            issubclass(ontology_class, AbstractEntity)
            and not ontology_class._meta.abstract
            and ontology_class is not TempEntityClass # TODO RDF: remove this once TempEntityClass is removed
        ):
            _all_entity_classes.append(ontology_class)
            _all_entity_class_names.append(ontology_class_name.lower())
        elif (
            issubclass(ontology_class, AbstractReification)
            and not ontology_class._meta.abstract
        ):
            _all_reification_classes.append(ontology_class)
            _all_reification_class_names.append(ontology_class_name.lower())
        elif (
            issubclass(ontology_class, AbstractVocabulary)
            and not ontology_class._meta.abstract
        ):
            _all_vocabulary_classes.append(ontology_class)
            _all_vocabulary_class_names.append(ontology_class_name.lower())
    _all_ontology_classes = _all_entity_classes + _all_reification_classes + _all_vocabulary_classes
    _all_ontology_class_names = _all_entity_class_names + _all_reification_class_names + _all_vocabulary_class_names

def get_all_ontology_classes():
    """
    Retrieve all ontology classes from apis_ontology.models except for abstract classes, reifications, vocabularys
    
    :return: a list of ontology classes
    """
    if _all_ontology_classes is None:
        initialize_all()
    
    return _all_ontology_classes

def get_ontology_class_of_name(ontology_name):
    """
    Look up an ontology class based on a given name.

    :param ontology_name: a string to compare against classes' __name__
                        values; need not be formatted (letter case does
                        not matter)
    :return: an ontology class – or raise exception
    """
    for ontology_class in get_all_ontology_classes():
        if ontology_class.__name__.lower() == ontology_name.lower():
            return ontology_class
    
    raise Exception("Could not find ontology class of name:", ontology_name)

def get_all_ontology_class_names():
    """
    Retrieve lower-cased names of all ontology classes from apis_ontology.models except for abstract
    classes, reifications, vocabularys

    :return: a list of strings
    """
    
    if _all_ontology_class_names is None:
        initialize_all()
    
    return _all_ontology_class_names

def get_all_entity_classes():
    """
    Retrieve all entity classes from apis_ontology.models except for abstract classes, reifications, vocabularys
    
    :return: a list of entity classes
    """
    global _all_entity_classes
    if _all_entity_classes is None:
        initialize_all()
    
    return _all_entity_classes

def get_entity_class_of_name(entity_name):
    """
    Look up an entity class based on a given name.

    :param entity_name: a string to compare against classes' __name__
                        values; need not be formatted (letter case does
                        not matter)
    :return: an entity class – or raise exception
    """
    for entity_class in get_all_entity_classes():
        if entity_class.__name__.lower() == entity_name.lower():
            return entity_class

    raise Exception("Could not find entity class of name:", entity_name)

def get_all_entity_class_names():
    """
    Retrieve lower-cased names of all entity classes from apis_ontology.models except for abstract
    classes, reifications, vocabularys

    :return: a list of strings
    """
    
    global _all_entity_class_names
    if _all_entity_class_names is None:
        initialize_all()

    return _all_entity_class_names

def get_all_reification_classes():
    """
    Retrieve all reification classes from apis_ontology.models except for abstract classes, reifications, vocabularys
    
    :return: a list of reification classes
    """
    global _all_reification_classes
    if _all_reification_classes is None:
        initialize_all()
    
    return _all_reification_classes

def get_reification_class_of_name(reification_name):
    """
    Look up an reification class based on a given name.

    :param reification_name: a string to compare against classes' __name__
                        values; need not be formatted (letter case does
                        not matter)
    :return: an reification class – or raise exception
    """
    for reification_class in get_all_reification_classes():
        if reification_class.__name__.lower() == reification_name.lower():
            return reification_class
    
    raise Exception("Could not find reification class of name:", reification_name)

def get_all_reification_class_names():
    """
    Retrieve lower-cased names of all reification classes from apis_ontology.models except for abstract
    classes, reifications, vocabularys

    :return: a list of strings
    """
    
    global _all_reification_class_names
    if _all_reification_class_names is None:
        initialize_all()
    
    return _all_reification_class_names

def get_cached_property_choices(entity_self_type_str, entity_other_type_str, search_name_str):
    from apis_core.apis_entities.autocomplete3 import PropertyAutocomplete
    
    res = _cached_property_choices_dict.get((entity_self_type_str, entity_other_type_str, search_name_str))
    if res is not None:
        return res
    else:
        entity_self_contenttype = get_ontology_class_of_name(entity_self_type_str).get_content_type()
        entity_other_contenttype = get_ontology_class_of_name(entity_other_type_str).get_content_type()
        from apis_core.apis_relations.models import Property
        rbc_self_subj_other_obj = Property.objects.filter(
            subj_class=entity_self_contenttype,
            obj_class=entity_other_contenttype,
            name__icontains=search_name_str
        )
        rbc_self_obj_other_subj = Property.objects.filter(
            subj_class=entity_other_contenttype,
            obj_class=entity_self_contenttype,
            name_reverse__icontains=search_name_str
        )
        choices = []
        # The Select2ListView class when finding results for some user input, returns these results in this 'choices' list.
        # This is a list of dictionaries, where each dictionary has an id and a text.
        # In our case however the results can come from two different sets:
        # the one where result hits match on the forward name of a property and the other set where the result hits
        # match on the reverse name. These hits need to re-used later, but additionally the direction of the property
        # is also needed later to persist it correctly (e.g. when creating a triple between two persons, where one is
        # the mother and the other is the daughter, then the property direction is needed).
        # I could not find a way to return in this function a choices list with dictionaries or something else, that
        # would pass additional data. So I am misusing the 'id' item in the dictionary by encoding the id and the direction
        # into a string which will be parsed and split later on.
        for rbc in rbc_self_subj_other_obj:
            choices.append(
                {
                    'id': f"id:{rbc.pk}__direction:{PropertyAutocomplete.SELF_SUBJ_OTHER_OBJ_STR}", # misuse of the id item as explained above
                    'text': rbc.name
                }
            )
        for rbc in rbc_self_obj_other_subj:
            choices.append(
                {
                    'id': f"id:{rbc.pk}__direction:{PropertyAutocomplete.SELF_OBJ_OTHER_SUBJ_STR}", # misuse of the id item as explained above
                    'text': rbc.name_reverse
                }
            )
        _cached_property_choices_dict[(entity_self_type_str, entity_other_type_str, search_name_str)] = choices
        return choices
