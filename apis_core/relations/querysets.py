def RelationListViewQueryset(queryset):
    return queryset.select_subclasses()


def RelationViewSetQueryset(queryset):
    return queryset.select_subclasses()
