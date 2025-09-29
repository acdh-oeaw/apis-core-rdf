from apis_core.generic.tables import GenericTable, MoreLessColumn


class PersonTable(GenericTable):
    class Meta(GenericTable.Meta):
        sequence = ["desc", "bio"]

    # example column to show preview and detail
    bio = MoreLessColumn(
        orderable=False,
        preview=lambda x: f"This is {x.surname}",
        fulltext=lambda x: f"This is {x.surname}, {x.forename} {x.surname}.",
    )
