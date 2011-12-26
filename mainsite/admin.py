from django.contrib import admin
from mainsite.models import Setting

class SettingAdmin(admin.ModelAdmin):
    list_display = ('tag', 'value')

admin.site.register(Setting, SettingAdmin)
