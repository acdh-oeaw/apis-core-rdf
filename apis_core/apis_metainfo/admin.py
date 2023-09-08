from django.contrib import admin

from .models import Source, Collection, Uri

admin.site.register(Source)
admin.site.register(Collection)
admin.site.register(Uri)
