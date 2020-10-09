import inspect
import sys

# from reversion import revisions as reversion
import reversion
from crum import get_current_request
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from model_utils.managers import InheritanceManager

# from apis_core.apis_entities.models import Person
from apis_core.apis_metainfo.models import TempEntityClass



#######################################################################
#
# Custom Managers
#
#######################################################################
from apis_core.apis_vocabularies.models import RelationBaseClass


def find_if_user_accepted():
    request = get_current_request()
    if request is not None:
        print('running through request')
        if request.user.is_authenticated:
            print('authenticated')
            return {}
        else:
            return {'published': True}
    else:
        return {}


class RelationPublishedQueryset(models.QuerySet):
    def filter_for_user(self, *args, **kwargs):
        if getattr(settings, "APIS_SHOW_ONLY_PUBLISHED", False):
            request = get_current_request()
            if request is not None:
                if request.user.is_authenticated:
                    return self
                else:
                    return self.filter(published=True)
            else:
                return self.filter(published=True)
        else:
            return self

    def filter_ann_proj(self, request=None, ann_proj=1, include_all=True):
        """The filter function provided by the manager class.

        :param request: `django.request` object
        :return: queryset that contains only objects that are shown in the highlighted text or those not connected
            to an annotation at all.
        """
        qs = self
        users_show = None
        if request:
            ann_proj = request.session.get('annotation_project', False)
            if not ann_proj:
                return qs
            users_show = request.session.get('users_show_highlighter', None)
        query = Q(annotation__annotation_project_id=ann_proj)
        if users_show is not None:
            query.add(Q(annotation__user_added_id__in=users_show), Q.AND)
        if include_all:
            query.add(Q(annotation__annotation_project__isnull=True), Q.OR)
        return qs.filter(query)


class BaseRelationManager(models.Manager):
    def get_queryset(self):
        return RelationPublishedQueryset(self.model, using=self._db)

    def filter_ann_proj(self, request=None, ann_proj=1, include_all=True):
        return self.get_queryset().filter_ann_proj(request=request, ann_proj=ann_proj, include_all=include_all)

    def filter_for_user(self):
        if hasattr(settings, "APIS_SHOW_ONLY_PUBLISHED") or "apis_highlighter" in getattr(settings, "INSTALLED_APPS"):
            return self.get_queryset().filter_for_user()
        else:
            return self.get_queryset()







from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor

class InheritanceForwardManyToOneDescriptor(ForwardManyToOneDescriptor):
    def get_queryset(self, **hints):
        return self.field.remote_field.model.objects_inheritance.db_manager(hints=hints).select_subclasses()


class InheritanceForeignKey(models.ForeignKey):
    forward_related_accessor_class = InheritanceForwardManyToOneDescriptor



class Triple(models.Model):

    # TODO __sresch__ : add ent filter shortcut so that e.g. this can be shortened: Triple.objects.filter(Q(subj__pk=113) | Q(obj__pk=113))

    subj = InheritanceForeignKey(TempEntityClass, on_delete=models.CASCADE, related_name="triple_subj")
    obj = InheritanceForeignKey(TempEntityClass, on_delete=models.CASCADE, related_name="triple_obj")
    prop = models.ForeignKey(RelationBaseClass, on_delete=models.CASCADE, related_name="triple_prop")

    objects = models.Manager()
    objects_inheritance = InheritanceManager()

    def __repr__(self):

        return f"<Triple: subj: {self.subj}, prop: {self.prop}, obj: {self.obj}>"


    def __str__(self):

        return self.__repr__()


    def save(self, *args, **kwargs):

        # TODO __sresch__ : Integrate proper check if subj and obj instances are of valid class as defined in prop.subj_class and prop.obj_class

        allowed_contenttypes = self.prop.subj_class.all()
        ct_subj = ContentType.objects.get(model=self.subj.__class__.__name__)
        if ct_subj not in allowed_contenttypes:
            raise Exception()

        allowed_contenttypes = self.prop.obj_class.all()
        ct_obj = ContentType.objects.get(model=self.obj.__class__.__name__)
        if ct_obj not in allowed_contenttypes:
            raise Exception()

        super().save(*args, **kwargs)


class TempTriple(Triple):


    review = models.BooleanField(
        default=False,
        help_text="Should be set to True, if the data record holds up quality standards.",
    )
    start_date = models.DateField(blank=True, null=True)
    start_start_date = models.DateField(blank=True, null=True)
    start_end_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_start_date = models.DateField(blank=True, null=True)
    end_end_date = models.DateField(blank=True, null=True)
    start_date_written = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Start",
    )
    end_date_written = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="End",
    )
    # text = models.ManyToManyField("Text", blank=True)
    # collection = models.ManyToManyField("Collection")
    status = models.CharField(max_length=100)
    # source = models.ForeignKey(
    #     "Source", blank=True, null=True, on_delete=models.SET_NULL
    # )
    references = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)


class SubTriple(Triple):

    comment = models.CharField(max_length=100)









#######################################################################
#
# AbstractRelation
#
#######################################################################


# class AbstractRelation(TempEntityClass):
#     """
#     Abstract super class which encapsulates common logic between the different relations and provides various methods
#     relating to either all or specific relations.
#     """
#     objects = BaseRelationManager()
#
#     #annotation_links = AnnotationRelationLinkManager()
#
#     class Meta:
#         abstract = True
#         default_manager_name = 'objects'
#
#
#
#     # Methods dealing with individual data retrievals of instances
#     ####################################################################################################################
#
#     def __str__(self):
#         return "{} ({}) {}".format(self.get_related_entity_instanceA(), self.relation_type, self.get_related_entity_instanceB())
#
#
#     def get_web_object(self):
#
#         nameA = self.get_related_entity_instanceA().name
#         nameB = self.get_related_entity_instanceB().name
#
#         if self.get_related_entity_classA() == Person:
#             nameA += ", "
#             if self.get_related_entity_instanceA().first_name is None:
#                 nameA += "-"
#             else:
#                 nameA += self.get_related_entity_instanceA().first_name
#
#         if self.get_related_entity_classB() == Person:
#             nameB += ", "
#             if self.get_related_entity_instanceB().first_name is None:
#                 nameB += "-"
#             else:
#                 nameB += self.get_related_entity_instanceB().first_name
#
#         result = {
#             'relation_pk': self.pk,
#             'relation_type': self.relation_type.name,
#             self.get_related_entity_field_nameA(): nameA,
#             self.get_related_entity_field_nameB(): nameB,
#             'start_date': self.start_date_written,
#             'end_date': self.end_date_written}
#         return result
#
#
#     def get_table_dict(self, entity):
#         """Dict for the tabels in the html view
#
#         :param entity: Object of type :class:`entities.models.Place`; Used to determine which Place is the main antity
#             and which one the related.
#         :return:
#         """
#         if self.get_related_entity_instanceA() == entity:
#             rel_other_key = self.get_related_entity_field_nameB()[:-1]
#             rel_other_value = self.get_related_entity_instanceB()
#             rel_type = self.relation_type.label
#         elif self.get_related_entity_instanceB() == entity:
#             rel_other_key = self.get_related_entity_field_nameA()[:-1]
#             rel_other_value = self.get_related_entity_instanceA()
#             rel_type = self.relation_type.label_reverse
#         else:
#             raise Exception("Did not find corresponding entity. Wiring of current relation to current entity is faulty.")
#
#         result = {
#             'relation_pk': self.pk,
#             'relation_type': rel_type,
#             rel_other_key: rel_other_value,
#             'start_date_written': self.start_date_written,
#             'end_date_written': self.end_date_written,
#             'start_date': self.start_date,
#             'end_date': self.end_date}
#         return result
#
#
#
#     # Various Methods enabling convenient shortcuts between entities, relations, fields, etc
#     ####################################################################################################################
#
#
#     # Methods dealing with all relations
#     ####################################################################################################################
#
#
#     _all_relation_classes = None
#     _all_relation_names = None
#
#
#     @classmethod
#     def get_all_relation_classes(cls):
#         """
#         Instantiates both lists: '_all_relation_classes' and '_all_relation_names'
#
#         :return: list of all python classes of the relations defined within this models' module
#         """
#
#         # check if not yet instantiated
#         if cls._all_relation_classes == None:
#             # if not, then instantiate the private lists
#
#             relation_classes = []
#             relation_names = []
#
#             # using python's reflective logic, the following loop iterates over all classes of this current module.
#             for relation_name, relation_class in inspect.getmembers(
#                     sys.modules[__name__], inspect.isclass):
#                 print('inspecting classes')
#                 # check for python classes not to be used.
#                 if \
#                         relation_class.__module__ == "apis_core.apis_relations.models" and \
#                         relation_class.__name__ != "AnnotationRelationLinkManager" and \
#                         relation_class.__name__ != "BaseRelationManager" and \
#                         relation_class.__name__ != "RelationPublishedQueryset" and \
#                         relation_class.__name__ != "AbstractRelation":
#
#                     relation_classes.append(relation_class)
#                     relation_names.append(relation_name.lower())
#
#             cls._all_relation_classes = relation_classes
#             cls._all_relation_names = relation_names
#
#         return cls._all_relation_classes
#
#
#     @classmethod
#     def get_relation_class_of_name(cls, relation_name):
#         """
#         :param entity_name: str : The name of an relation
#         :return: The model class of the relation respective to the given name
#         """
#
#         for relation_class in cls.get_all_relation_classes():
#             if relation_class.__name__.lower() == relation_name.lower():
#                 return relation_class
#
#         raise Exception("Could not find relation class of name:", relation_name)
#
#
#     @classmethod
#     def get_all_relation_names(cls):
#         """
#         :return: list of all class names in lower case of the relations defined within this models' module
#         """
#
#         if cls._all_relation_classes == None:
#
#             # The instantion logic of relation_names list is coupled to the instantiation logic of the relation_classes
#             # list done in the method 'get_all_relation_classes'; hence just calling that is sufficient.
#             cls.get_all_relation_classes()
#
#         return cls._all_relation_names
#
#
#
#     # Methods dealing with related relations and entities
#     ####################################################################################################################
#
#
#     _relation_classes_of_entity_class = {}
#     _relation_classes_of_entity_name = {}
#     _relation_field_names_of_entity_class = {}
#
#
#     @classmethod
#     def get_relation_classes_of_entity_class(cls, entity_class):
#         """
#         :param entity_class : class of an entity for which the related relations should be returned
#         :return: a list of relation classes that are related to the entity class
#
#         E.g. AbstractRelation.get_relation_classes_of_entity_class( Person )
#         -> [ PersonEvent, PersonInstitution, PersonPerson, PersonPlace, PersonWork ]
#         """
#
#         return cls._relation_classes_of_entity_class[entity_class]
#
#
#     @classmethod
#     def get_relation_classes_of_entity_name(cls, entity_name):
#         """
#         :param entity_name : class name of an entity for which the related relations should be returned
#         :return: a list of relation classes that are related to the entity class
#
#         E.g. AbstractRelation.get_relation_classes_of_entity_class( 'person' )
#         -> [ PersonEvent, PersonInstitution, PersonPerson, PersonPlace, PersonWork ]
#         """
#
#         return cls._relation_classes_of_entity_name[entity_name.lower()]
#
#
#     @classmethod
#     def add_relation_class_of_entity_class(cls, entity_class):
#         """
#         Adds the given entity class to a list which is later retrieved via a dictionary, where the entity class and entity class name
#         define the key and the list of related relation classes as their values.
#
#         :param entity_class: the class for which the related relation (the current cls) will be saved into a respective list.
#         :return: None
#         """
#
#         # get the list of the class dictionary, create if not yet exists.
#         relation_class_list = cls._relation_classes_of_entity_class.get(entity_class, [])
#
#         # append the current relation class to the list.
#         relation_class_list.append(cls)
#
#         # save into the dictionary, which uses the entity class as key and the extended list above as value.
#         cls._relation_classes_of_entity_class[entity_class] = relation_class_list
#         cls._relation_classes_of_entity_name[entity_class.__name__.lower()] = relation_class_list
#
#
#     @classmethod
#     def get_relation_field_names_of_entity_class(cls, entity_class):
#         """
#         :param entity_class : class of an entity for which the related relation class field names should be returned
#         :return: a list of relation class field names that are related to the entity class
#
#         E.g. AbstractRelation.get_relation_names_of_entity_class( Person )
#         -> [ personevent_set, personinstitution_set, related_personA, related_personB, personplace_set, personwork_set ]
#         """
#
#         return cls._relation_field_names_of_entity_class[entity_class]
#
#
#     @classmethod
#     def add_relation_field_name_of_entity_class(cls, relation_name, entity_class):
#         """
#         Adds the given entity class to a list which is later retrieved via a dictionary, where the entity class
#         defines the key and the list of related relation classes as its values.
#
#         :param entity_class: the class for which the related relation (the current cls) will be saved into a respective list.
#         :return: None
#         """
#
#         # get the list of the class dictionary, create if not yet exists.
#         relation_names_list = cls._relation_field_names_of_entity_class.get(entity_class, [])
#         # append the current relation field name to the list.
#         relation_names_list.append(relation_name)
#         # save into the dictionary, which uses the entity class as key and the extended list above as value.
#         cls._relation_field_names_of_entity_class[entity_class] = relation_names_list
#
#
#     def get_related_entity_instanceA(self):
#         """
#         This method only works on the relation instance of a given relation class.
#         There it returns the instance of an entity on the 'A' side of the given relation instance.
#
#         Note that if your IDE complains about expecting a 'str' instead of 'None' this happens because
#         the method 'get_related_entity_field_nameA()' is only implemented and overridden at runtime in the
#         function 'generate_all_fields' in the class 'EntityRelationFieldGenerator'.
#
#         :return: An entity instance related to the current relation instance
#         """
#         return getattr( self, self.get_related_entity_field_nameA() )
#
#
#     def get_related_entity_instanceB(self):
#         """
#         This method only works on the relation instance of a given relation class.
#         There it returns the instance of an entity on the 'B' side of the given relation instance.
#
#         Note that if your IDE complains about expecting a 'str' instead of 'None' this happens because
#         the method 'get_related_entity_field_nameB()' is only implemented and overridden at runtime in the
#         function 'generate_all_fields' in the class 'EntityRelationFieldGenerator'.
#
#         :return: An entity instance related to the current relation instance
#         """
#         return getattr( self, self.get_related_entity_field_nameB() )
#
#
#
#     # method stumps
#     ####################################################################################################################
#     # These stumps merely serve as placeholders so that both IDE and developers know that these methods exist.
#     # They are implemented programmatically in the function 'generate_all_fields' in the class 'EntityRelationFieldGenerator'.
#
#
#     @classmethod
#     def get_related_entity_classA(cls):
#         """
#         :return: the python class of the A side of the current relation class or instance
#         E.g. PersonWork -> Person
#         """
#         return None
#
#     @classmethod
#     def get_related_entity_classB(cls):
#         """
#         :return: the python class of the B side of the current relation class or instance
#         E.g. PersonWork -> Work
#         """
#         return None
#
#     @classmethod
#     def get_related_entity_field_nameA(cls):
#         """
#         :return: the name of the field of the A side of the current relation class or instance
#         E.g. PersonWork -> "related_person"
#         """
#         return None
#
#     @classmethod
#     def get_related_entity_field_nameB(cls):
#         """
#         :return: the name of the field of the B side of the current relation class or instance
#         E.g. PersonWork -> "related_work"
#         """
#         return None
#
#
#
#
# #######################################################################
# #
# # Person - ... - Relation
# #
# #######################################################################
#
#
# @reversion.register(follow=['tempentityclass_ptr'])
# class PersonPerson(AbstractRelation):
#
#     pass
#
#
# @reversion.register(follow=['tempentityclass_ptr'])
# class PersonPlace(AbstractRelation):
#
#     pass
#
#
# @reversion.register(follow=['tempentityclass_ptr'])
# class PersonInstitution(AbstractRelation):
#
#     pass
#
#
# @reversion.register(follow=['tempentityclass_ptr'])
# class PersonEvent(AbstractRelation):
#
#     pass
#
#
# @reversion.register(follow=['tempentityclass_ptr'])
# class PersonWork(AbstractRelation):
#
#     pass
#
#
# #######################################################################
# #
# #   Institution - ... - Relation
# #
# #######################################################################
#
#
# @reversion.register(follow=['tempentityclass_ptr'])
# class InstitutionInstitution(AbstractRelation):
#
#     pass
#
#
# @reversion.register(follow=['tempentityclass_ptr'])
# class InstitutionPlace(AbstractRelation):
#
#     pass
#
#
# @reversion.register(follow=['tempentityclass_ptr'])
# class InstitutionEvent(AbstractRelation):
#
#     pass
#
#
# @reversion.register(follow=['tempentityclass_ptr'])
# class InstitutionWork(AbstractRelation):
#
#     pass
#
#
# #######################################################################
# #
# #   Place - ... - Relation
# #
# #######################################################################
#
#
# @reversion.register(follow=['tempentityclass_ptr'])
# class PlacePlace(AbstractRelation):
#
#     pass
#
#
# @reversion.register(follow=['tempentityclass_ptr'])
# class PlaceEvent(AbstractRelation):
#
#     pass
#
#
# @reversion.register(follow=['tempentityclass_ptr'])
# class PlaceWork(AbstractRelation):
#
#     pass
#
#
# #######################################################################
# #
# #   Event - ... - Relation
# #
# #######################################################################
#
#
# @reversion.register(follow=['tempentityclass_ptr'])
# class EventEvent(AbstractRelation):
#
#     pass
#
#
# @reversion.register(follow=['tempentityclass_ptr'])
# class EventWork(AbstractRelation):
#
#     pass
#
#
# #######################################################################
# #
# #   Work - ... - Relation
# #
# #######################################################################
#
#
# @reversion.register(follow=['tempentityclass_ptr'])
# class WorkWork(AbstractRelation):
#
#     pass

