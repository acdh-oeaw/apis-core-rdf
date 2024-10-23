from collections import defaultdict

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str

from apis_core.apis_entities.utils import get_entity_content_types


class Datamodel:
    entities: [object]
    relations: [object] = []
    graph: dict() = {}

    def __init__(self):
        self.entities = get_entity_content_types()
        if "apis_core.relations" in settings.INSTALLED_APPS:
            from apis_core.relations.utils import relation_content_types

            self.relations = relation_content_types()
        self.make_graph()

    def edges(self):
        edges = defaultdict(list)
        if "apis_core.apis_relations" in settings.INSTALLED_APPS:
            from apis_core.apis_relations.models import Property

            for prop in Property.objects.all():
                for subj_class in prop.subj_class.all():
                    for obj_class in prop.obj_class.all():
                        key = (
                            subj_class.name,
                            obj_class.name,
                        )
                        edges[key].append(prop.name_forward)

        for rel in self.relations:
            for subj_class in rel.model_class().subj_list():
                for obj_class in rel.model_class().obj_list():
                    key = (
                        ContentType.objects.get_for_model(subj_class).name,
                        ContentType.objects.get_for_model(obj_class).name,
                    )
                    edges[key].append(force_str(rel.model_class().name()))
        return edges

    def make_graph(self):
        try:
            from pydot import Dot, Edge, Node

            graph = Dot(graph_type="digraph")
            graph.set_node_defaults(shape="record", rankdir="TB")
            graph.set_graph_defaults(nodesep="1", ranksep="1", TBbalance="max")
            for content_type in self.entities:
                model_class = content_type.model_class()
                node = Node(
                    content_type.name, label=force_str(model_class._meta.verbose_name)
                )
                node.set_URL(model_class.get_listview_url())
                node.set_fillcolor("#3399ff")
                node.set_style("filled")
                graph.add_node(node)
            for (subj, obj), names in self.edges().items():
                e = Edge(subj, obj, label="\n".join(names))
                graph.add_edge(e)
            self.graph = {"svg": graph.create_svg().decode(), "dot": graph.to_string()}
        except ImportError as e:
            self.graph["error"] = str(e)
        except FileNotFoundError as e:
            self.graph["error"] = "Please install graphviz - " + str(e)
