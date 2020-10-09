from django.contrib import admin
from apis_core.apis_relations.models import SubTriple, Triple

admin.site.register(Triple)
admin.site.register(SubTriple)