from apis_core.utils.renderers.tei import TeiRenderer


class EntityToTEI(TeiRenderer):
    def render(self, data, media_type=None, renderer_context=None):
        self.template_name = f"apis_entities/tei/{data['entity_type']}.xml"
        return super().render(data, media_type, renderer_context)
