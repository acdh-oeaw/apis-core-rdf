from . import EntitiesTableFactory


def get_entities_table(entity_name: str):
    """
    Calls the new EntitiesTableFactory to retrieve the requested table-class.
    Only implemented to not break the existing interface, but the logic is redirected to the new
    EntitiesTableFactory, which stores already created classes or creates a not yet stored class and then stores it.
    """
    table_class = EntitiesTableFactory.get_table_class(entity_name)
    return table_class
