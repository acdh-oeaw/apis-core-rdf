import functools
from pathlib import Path

from django.apps import apps
from django.contrib.contenttypes.models import ContentType

from apis_core.apis_entities.models import AbstractEntity


def get_entity_classes():
    return list(filter(lambda x: issubclass(x, AbstractEntity), apps.get_models()))


def get_entity_content_types():
    return [ContentType.objects.get_for_model(model) for model in get_entity_classes()]


@functools.lru_cache
def get_feature_codes():
    try:
        featurecode_list = [(None, "---")]
        self = Path(__file__)
        featurecodefile = self.parent / "featureCodes_en.txt"
        featurecodes = featurecodefile.read_text()
        featurecodes = [
            line.split("\t")
            for line in featurecodes.split("\n")
            if len(line.split("\t")) == 3
        ]
        featurecode_list.extend([(el[0], el[0] + ": " + el[1]) for el in featurecodes])
    except Exception:
        featurecode_list = [(None, "None: could not read list of feature codes")]
    return featurecode_list
