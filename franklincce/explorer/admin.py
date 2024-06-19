from django.contrib import admin

from .models import LegislativeText, LegislationBook

admin.site.register(LegislativeText)
admin.site.register(LegislationBook)
