from django.contrib import admin

from .models import LegislativeText, LegislationBook

class LegislativeTextAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'legislation_title', 'school')

class LegislationBookAdmin(admin.ModelAdmin):
    exclude = ("has_performed_export",)

admin.site.register(LegislativeText, LegislativeTextAdmin)
admin.site.register(LegislationBook, LegislationBookAdmin)
