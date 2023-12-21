from django.db.models import Q
from apis_core.apis_relations.models import TempTriple


class TempTripleHistoryMixin(object):
    def get_triples_for_version(self):
        triples = TempTriple.history.as_of(self.history_date).filter(
            Q(subj=self.instance) | Q(obj=self.instance)
        )
        return triples
