from django.contrib import admin
from lg.models import LivingGroup

class LGAdmin(admin.ModelAdmin):
    list_display = ('year', 'lg_name','location', 'rep_email', 'rep_phone')

admin.site.register(LivingGroup, LGAdmin)