from apis_core.apis_entities.tables import AbstractEntityTable
from apis_core.generic.tables import MoreLessColumn


class PersonTable(AbstractEntityTable):
    class Meta(AbstractEntityTable.Meta):
        sequence = ["desc", "bio"]

    # example column to show preview and detail
    bio = MoreLessColumn(
        orderable=False,
        preview=lambda x: f"This is {x.surname}",
        fulltext=lambda x: f"This is {x.surname}, {x.forename} {x.surname}.",
    )
