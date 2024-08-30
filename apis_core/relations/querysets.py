def RelationListViewQueryset(queryset):
    return queryset.select_subclasses()
