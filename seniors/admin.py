# -*- coding: utf-8 -*-
import csv
from StringIO import StringIO
from zipfile import ZipFile
from django.contrib import admin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from seniors.models import Senior, Activity

class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1

class SeniorAdmin(admin.ModelAdmin):
    inlines = [ ActivityInline, ]
    search_fields = ('name', 'kerberos',)

    list_display = ('name', 'kerberos', 'sort_letter',)
    list_filter = ('tnq_year',)

    fieldsets = [
        ('Biographical Information', {'fields':['name', 'sort_letter', 'name_comments', 'home_town', 'home_state_or_country']}),
        ('MIT Information', {'fields':['tnq_year', 'kerberos', 'major', 'minor', 'lg']}),
        ('Quote', {'fields':['quote', 'quote_author']}),
      ]
    actions = ['export_as_csv', 'export_as_tagged_text', ]

    def export_as_tagged_text(modeladmin, request, queryset):
        response = HttpResponse(mimetype='application/zip')
        response['Content-Disposition'] = 'attachment; filename=seniors.zip'

        zip = ZipFile(response, 'w')

        SENIORS_PER_PAGE = 8
        SENIORS_PER_ROW = 4
        BULLET = u" · "
        SLASHES = u" // "
        DASH = u" – "

        pages = Paginator(queryset, SENIORS_PER_PAGE)

        def format_senior(senior):
            if not senior:
                return ""
            else:
                senior_string = u"<ParaStyle:Senior Info Text Second Try>"
                senior_string += senior.kerberos
                senior_string += BULLET
                senior_string += senior.major
                if senior.minor:
                    senior_string += ", "+senior.minor
                senior_string += SLASHES
                senior_string += senior.home_town + ", " + senior.home_state_or_country
                senior_string += BULLET
                senior_string += senior.lg
                activities = Activity.objects.filter(senior = senior)
                if activities:
                    senior_string += SLASHES
                    for i, activity in enumerate(activities):
                        if i:
                            senior_string += BULLET
                        senior_string += activity.title
                        senior_string += " <cPosition:Superscript>"
                        senior_string += activity.years
                        senior_string += "<cPosition:> "
                        if activity.offices:
                            senior_string += " (" + activity.offices + ")"
                if senior.quote:
                    senior_string += SLASHES
                    senior_string += senior.quote
                    senior_string += DASH
                    senior_string += senior.quote_author
                return senior_string

        for i in range(pages.num_pages):
            seniors = list(pages.page(i+1).object_list)
            seniors.extend([None]*(SENIORS_PER_PAGE-len(seniors)))
            page_string = u"""<UNICODE-MAC>
<Version:7><FeatureSet:InDesign-Roman>
"""
            for senior in seniors:
                if senior:
                    page_string += "<ParaStyle:Senior Name>%s<cNextXChars:Box>\n" % senior.name
                else:
                    page_string += "<cNextXChars:Box>\n"
            for j in range(SENIORS_PER_ROW):
                page_string += format_senior(seniors[j])
                page_string += "\n"
                page_string += format_senior(seniors[j+SENIORS_PER_ROW])
                page_string += "<cNextXChars:Column>\n"

            zip.writestr("page%d.txt" % i, page_string.encode("utf_16_le"))
        zip.close()
        return response

    export_as_tagged_text.short_description = "Export selected seniors to Adobe Tagged Text"

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
