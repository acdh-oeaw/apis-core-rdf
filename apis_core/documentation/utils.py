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
        for rel in self.relations:
            for subj_class in rel.model_class().subj_list():
                subj_name = ContentType.objects.get_for_model(subj_class).name
                for obj_class in rel.model_class().obj_list():
                    obj_name = ContentType.objects.get_for_model(obj_class).name

                    original_pair = (subj_name, obj_name)
                    key = tuple(sorted(original_pair))

                    rel_model = rel.model_class()
                    rel_label = ""
                    if key == original_pair:
                        rel_label = (
                            f"{force_str(rel_model.name())}/{force_str(rel_model.reverse_name())}"
                            if rel_model.name() != rel_model.reverse_name()
                            else rel_model.name()
                        )
                    else:
                        rel_label = (
                            f"{force_str(rel_model.reverse_name())}/{force_str(rel_model.name())}"
                            if rel_model.name() != rel_model.reverse_name()
                            else rel_model.name()
                        )

                    edges[key].append(rel_label)
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
                e = Edge(subj, obj, label="\n".join(names), fontsize="11")
                graph.add_edge(e)
            self.graph = {"svg": graph.create_svg().decode(), "dot": graph.to_string()}
        except ImportError as e:
            self.graph["error"] = str(e)
        except FileNotFoundError as e:
            self.graph["error"] = "Please install graphviz - " + str(e)
