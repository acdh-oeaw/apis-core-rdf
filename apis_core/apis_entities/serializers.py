import re

from django.urls import reverse_lazy
from rest_framework import serializers


class BaseEntitySerializer(serializers.HyperlinkedModelSerializer):
    uri_set = serializers.HyperlinkedRelatedField(
        view_name="apis:apis_api:uri-detail",
        lookup_field="pk",
        many=True,
        read_only=True,
    )
    collection = serializers.HyperlinkedRelatedField(
        view_name="apis:apis_api:collection-detail",
        lookup_field="pk",
        many=True,
        read_only=True,
    )
    text = serializers.HyperlinkedRelatedField(
        view_name="apis:apis_api:text-detail",
        lookup_field="pk",
        many=True,
        read_only=True,
    )


class GeoJsonSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        p_pk = self.context.get("p_pk")
        short = False
        url_r = reverse_lazy(
            "apis:apis_entities:resolve_ambigue_place",
            kwargs={"pk": str(p_pk), "uri": obj["id"][7:]},
        )
        long = False
        if "http://www.w3.org/2003/01/geo/wgs84_pos#long" in obj.keys():
            long = float(
                obj["http://www.w3.org/2003/01/geo/wgs84_pos#long"][0]["value"]
            )
            lat = float(obj["http://www.w3.org/2003/01/geo/wgs84_pos#lat"][0]["value"])
        elif "long" in obj.keys():
            long = float(obj["long"][0]["value"])
            lat = float(obj["lat"][0]["value"])
            short = True
        if long:
            popup = ""
            for k in obj.keys():
                if k == "id" or k == "long" or k == "lat":
                    continue
                if not short or k.startswith("http"):
                    title = k.split("#")[-1]
                else:
                    title = k
                popup += "<b>{}:</b> {}<br/>".format(title, obj[k][0]["value"])
            r = {
                "geometry": {"type": "Point", "coordinates": [long, lat]},
                "type": "Feature",
                "properties": {
                    "popupContent": """{}
                    <b>Geonames:</b> <a href='{}'>Select this URI</a>""".format(
                        popup, url_r
                    )
                },
                "id": url_r,
            }
            return r
        else:
            return ""


class GeoJsonSerializerTheme(serializers.BaseSerializer):
    def to_representation(self, obj):
        if obj[0] is None:
            return ""
        url_r = reverse_lazy(
            "apis:apis_core:place-detail", kwargs={"pk": str(obj[0].pk)}
        )
        if obj[0].lng:
            relations = []
            for rel2 in obj[1]:
                if rel2[1] is not None:
                    res_str = f"{rel2[1].name} / {rel2[0].name}"
                else:
                    res_str = f"{rel2[0].name}"
                if rel2[2] is not None:
                    res_str += f" ({rel2[2]}-"
                if rel2[3] is not None:
                    if res_str.endswith("-"):
                        res_str += f"{rel2[3]})"
                    else:
                        res_str += f" (-{rel2[3]})"
                if "(" in res_str and not res_str.endswith(")"):
                    res_str += ")"
                # relations.append((res_str, rel2[2], rel2[3]))
                relations.append(
                    {
                        "id": rel2[-1].pk,
                        "relation": res_str,
                        "start_date": rel2[2],
                        "end_date": rel2[3],
                    }
                )
            r = {
                "geometry": {"type": "Point", "coordinates": [obj[0].lng, obj[0].lat]},
                "type": "Feature",
                "properties": {
                    "name": obj[0].name,
                    "uris": [x.uri for x in obj[0].uri_set.all()],
                    "kind": obj[0].kind.name
                    if obj[0].kind is not None
                    else "undefined",
                    "url": url_r,
                    # "relation_kind": ", ".join([x[0].name for x in obj[1]])
                    "relations": relations,
                },
                "id": url_r,
            }
            return r
        else:
            return ""


class NetJsonEdgeSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        ent_obj = obj.__class__.__name__
        ob_match = re.match(r"([A-Z][a-z]+)([A-Z][a-z]+)$", ent_obj)
        rel_a = "related_" + ob_match.group(1).lower()
        rel_b = "related_" + ob_match.group(2).lower()
        if rel_a == rel_b:
            rel_a += "A"
            rel_b += "B"
        r = {
            "source": getattr(obj, rel_a).pk,
            "target": getattr(obj, rel_b).pk,
            "id": obj.pk,
            "type": "arrow",
            "data": dict(),
        }
        r["data"]["start_date"] = obj.start_date_written
        r["data"]["end_date"] = obj.end_date_written
        r["data"]["relation_type"] = obj.relation_type.name

        return r


class NetJsonNodeSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        ent_obj = obj.__class__.__name__
        ent_url = reverse_lazy(
            "apis:apis_entities:generic_entities_edit_view",
            kwargs={"pk": str(obj.pk), "entity": ent_obj.lower()},
        )
        tt = """<div class='arrow'></div>
            <div class='sigma-tooltip-header'>{}</div>
            <div class='sigma-tooltip-body'>
            <table>
                <tr><th>Type</th> <td>{}</td></tr>
                <tr><th>Entity</th> <td><a href='{}'>Link</a></td></tr>
            </table>
            <button class='small-button' onclick='expand_node("{}", {})'>expand</button>
            </div>""".format(str(obj), ent_obj, ent_url, ent_obj, obj.pk)
        r = {
            "type": ent_obj.lower(),
            "label": str(obj),
            "id": obj.pk,
            "tooltip": tt,
            "data": dict(),
        }
        r["data"]["uri"] = [x.uri for x in obj.uri_set.all()]
        r["data"]["notes"] = obj.notes
        r["data"]["references"] = obj.references
        r["data"]["start_date"] = obj.start_date_written
        r["data"]["end_date"] = obj.end_date_written
        if ent_obj.lower() != "person":
            if obj.kind:
                r["data"]["kind"] = obj.kind.name
        if ent_obj.lower() == "place":
            r["data"]["lat"] = obj.lat
            r["data"]["lon"] = obj.lng
        if ent_obj.lower() == "person":
            r["data"]["profession"] = [x.name for x in obj.profession.all()]
            if obj.gender:
                r["data"]["gender"] = obj.gender
        return r
