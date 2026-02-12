from django.contrib import admin

from .models import SearchEntry


@admin.register(SearchEntry)
class SearchEntryAdmin(admin.ModelAdmin):
    pass
