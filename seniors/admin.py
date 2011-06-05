import csv
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from scripts.seniors.models import Senior, Activity

class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1

class SeniorAdmin(admin.ModelAdmin):
    inlines = [ ActivityInline, ]
    search_fields = ('name','kerberos',)

    list_display = ('name', 'kerberos', 'sort_letter',)
    list_filter = ('tnq_year',)

    fieldsets = [
        ('Biographical Information', {'fields':['name', 'name_comments', 'home_town', 'home_state_or_country']}),
        ('MIT Information', {'fields':['kerberos', 'major', 'minor', 'lg']}),
        ('Quote', {'fields':['quote', 'quote_author']}),
      ]
    actions = ['export_as_csv', ]

    def export_as_csv(modeladmin, request, queryset):
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=seniors.csv'
    
        writer = csv.writer(response,)
        writer.writerow(['name', 'firstname', 'lastname', 'comments',
                         'kerberos', 'major', 'minor', 'hometown',
                         'homeState', 'lg', 'quote', 'author', 
                         'activity1', 'years1', 'offices1',
                         'activity2', 'years2', 'offices2',
                         'activity3', 'years3', 'offices3',
                         'activity4', 'years4', 'offices4',
                         'activity5', 'years5', 'offices5', ])

        for senior in queryset:
    	    this_row = [senior.name.encode('utf8'),
                             senior.name.strip().split(" ")[0].encode('utf8'),
                             senior.name.strip().split(" ")[-1].encode('utf8'),
                             senior.name_comments.encode('utf8'),
                             senior.kerberos.encode('utf8'),
                             senior.major.encode('utf8'),
                             senior.minor.encode('utf8'),
                             senior.home_town.encode('utf8'),
                             senior.home_state_or_country.encode('utf8'),
                             senior.lg.encode('utf8'),
                             senior.quote.encode('utf8'),
                             senior.quote_author.encode('utf8')]

            activities = Activity.objects.filter(senior = senior)
            for activity in activities:
                this_row.append(activity.title.encode('utf8'))
                this_row.append(activity.years.encode('utf8'))
                this_row.append(activity.offices.encode('utf8'))
            
            writer.writerow(this_row)
        return response 

    export_as_csv.short_description = "Export selected seniors to CSV"


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'senior')

admin.site.register(Senior, SeniorAdmin)
admin.site.register(Activity, ActivityAdmin)
