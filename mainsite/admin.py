from django.contrib import admin
from scripts.mainsite.models import Setting

from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld

class SettingAdmin(admin.ModelAdmin):
    list_display = ('tag', 'value')

class FlatPageAdmin(FlatPageAdminOld):
    class Media:
        js = (
              'codemirror/lib/codemirror.js',
              'codemirror/mode/xml/xml.js',
              'codemirror/mode/javascript/javascript.js',
              'codemirror/mode/css/css.js',
              'codemirror/mode/htmlmixed/htmlmixed.js',
              'js/codemirror_activator.js',
             )

        css = {
                'all' : (
                            'codemirror/lib/codemirror.css',
                            'codemirror/mode/xml/xml.css',
                            'codemirror/mode/javascript/javascript.css',
                            'codemirror/mode/css/css.css',
                            'style/codemirror_extrastyle.css',
                        ),
              }

admin.site.register(Setting, SettingAdmin)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
