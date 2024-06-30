from django.contrib import admin

from explorer import models

class LegislativeTextAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'legislation_title', 'school')

class LegislationBookAdmin(admin.ModelAdmin):
    exclude = ("has_performed_export",)

to_register = [
    [models.LegislativeText, LegislativeTextAdmin],
    [models.LegislationBook, LegislationBookAdmin],
    [models.LegislationClassification],
    [models.School],
    [models.Country],
]
for i in to_register:
    admin.site.register(*i)