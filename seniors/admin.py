# -*- coding: utf-8 -*-
import codecs
import csv
from collections import defaultdict
from StringIO import StringIO
from zipfile import ZipFile
from django.contrib import admin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from seniors.models import Senior, Activity
import re

class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1

majors = {
    "Mechanical Engineering": "2",
    "Physics": "8",
    "Electrical Engineering": "6-1",
    "Computer Science": "6-3",
    "Chemical Engineering": "10",
    "Management": "15",
    "Political Science": "17",
    "Brain  Cognitive Sciences": "9",
    "Civil Engineering": "1",
    "Chemistry": "5",
    "Biology": "7",
    "Music": "21M",
    "Aerospace Engineering": "16",
    "History": "21H",
    "Writing": "21W",
    "Nuclear Engineering": "22",
    "Philosophy": "24"
}

## {{{ http://code.activestate.com/recipes/577305/ (r1)
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}
## end of http://code.activestate.com/recipes/577305/ }}}

state_abbrs = {}
for abbr in states.keys():
    state_abbrs[states[abbr]] = abbr

lg_expansions = [x.split("\t", 2) for x in
"""ADPhi	Alpha Delta Phi
AEP	Alpha Epsilon Pi
AXO	Alpha Chi Omega
B-Entry	MacGregor B-Entry
Annex, McCormick	McCormick Annex
Baker House	Baker
Beast	East Campus 2E
""".splitlines()]

greek_letters = {
        "ALPHA"     : "\u0391",
        "BETA"      : "\U0392",
        "GAMMA"     : "\U0393",
        "DELTA"     : "\U0394",
        "EPSILON"   : "\U0395",
        "ZETA"      : "\U0396",
        "ETA"       : "\U0397",
        "THETA"     : "\U0398",
        "IOTA"      : "\U0399",
        "KAPPA"     : "\U039A",
        "LAMBDA"    : "\U039B",
        "MU"        : "\U039C",
        "NU"        : "\U039D",
        "XI"        : "\U039E",
        "OMICRON"   : "\U039F",
        "PI"        : "\U03A0",
        "RHO"       : "\U03A1",
        "SIGMA"     : "\U0393",
        "TAU"       : "\U03A4",
        "UPSILON"   : "\U03A5",
        "PHI"       : "\U03A6",
        "CHI"       : "\U03A7",
        "PSI"       : "\U03A8",
        "OMEGA"     : "\U03A9",
}

def format_lg(lg):
    fragments = lg.split()
    for i, word in enumerate(fragments):
        if word.upper() in greek_letters.keys():
            fragments[i] = greek_letters[word.upper()]
        else:
            fragments[i] = word + " "
    return "".join(fragments).strip()

def format_major(major):
    major = major.upper().strip()
    major = major.replace("AND", "")
    major = major.replace("COURSE", "")
    major = major.replace(" - ", " / ")
    for one, two in majors.iteritems():
        major = major.replace(one.upper(), two)
    major = re.sub(ur'^([0-9A-Z–-]+)[^0-9A-Z–-]+([0-9A-Z–-]+)$', r'\1 / \2', major)
    major = re.sub(r'([0-9]+)-([A-Z]+)', r'\1\2', major)
    major = major.replace("-", u"\u2013")
    major = major.strip()
    return major

def format_state(state):
    state = state.strip()

    if state.upper() in states.keys():
        state = states[state.upper()]

    if state.upper() in state_abbrs.keys():
        state = state_abbrs[state.upper()]
    return state

def format_name(name):
    name = re.sub(r' ([A-Z]) ', r' \1. ', name)
    return name.strip()

def format_years(years):
    years = re.sub(r',\s*', r' ', years)
    return years.strip()

def format_author(author):
    author = re.sub(r'^"(.*)"$', r'\1', author)
    author = re.sub(r"^'(.*)'$", r"\1", author)
    author = re.sub(r'^-', r'', author)
    author = re.sub(r'^([^,]*?),\s*([^0-9,][^,]*?)$', r'\1 (\2)', author)
    author = re.sub(r'\("(.+)"\)', r'(\1)', author)
    return author.strip()

def fix_seniors(tnq_year, func, attr=None, get=None, set=None):
    if not get:
        get = lambda senior: getattr(senior, attr)
    if not set:
        set = lambda senior, value: setattr(senior, attr, value)
    queryset = Senior.objects.filter(tnq_year=2012).order_by("sort_letter")
    pages = Paginator(queryset, 30)

    def do_senior(senior):
        try:
            val = get(senior)
            if val:
                new_val = func(val)
                if new_val != val:
                    print "%s\t%s\t%s" % (val, new_val, senior.name)
                    return [(senior, new_val)]
        except IndexError:
            pass
        return []

    for i in range(pages.num_pages):
        seniors = list(pages.page(i+1).object_list)
        todo = []
        for senior in seniors:
            todo.extend(do_senior(senior))
        if not todo:
            continue
        if raw_input("Okay [yN]? ").lower() == "y":
            for senior, new_val in todo:
                set(senior, new_val)
                senior.save()
        else:
            for senior in seniors:
                change = do_senior(senior)
                if change:
                    new_val = change[0][1]
                    if raw_input("Okay [yN]? ").lower() == "y":
                        set(senior, new_val)
                        senior.save()

def _sort_seniors(queryset):
    import PyICU
    collator = PyICU.Collator.createInstance(PyICU.Locale("es_ES"))
    queryset = queryset.exclude(image_path=None)
    sorted_seniors = list(queryset)
    sort_first_name = lambda _: _.name.split()[0].strip()
    sort_last_name = lambda _: [w for w in _.name.split() if w[0].lower() == _.sort_letter.lower()][-1].lower().strip()
    sorted_seniors.sort(key=lambda _: sort_last_name(_)+" "+sort_first_name(_), cmp=collator.compare)
    return sorted_seniors

class SeniorAdmin(admin.ModelAdmin):
    inlines = [ ActivityInline, ]
    search_fields = ('name', 'kerberos',)

    list_display = ('name', 'kerberos', 'sort_letter',)
    list_filter = ('tnq_year',)

    fieldsets = [
        ('Biographical Information', {'fields':['name', 'sort_letter', 'name_comments', 'home_town', 'home_state_or_country', 'image_path',]}),
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

        SPECIAL_PAGES = defaultdict(lambda: SENIORS_PER_PAGE)
        SPECIAL_PAGES.update({11:4,
                             28:4,
                             49:4,
                             68:4})

        sorted_seniors = _sort_seniors(queryset)

        pages = []
        unpaginated_seniors = list(sorted_seniors)

        count = 0

        page = 0
        while unpaginated_seniors:
            on_page = SPECIAL_PAGES[page]
            this_page, unpaginated_seniors = unpaginated_seniors[:on_page], unpaginated_seniors[on_page:]
            pages.append(this_page)
            page += 1

        def sanitize(str):
            return str.replace(r"<", r"\<").replace(r">", r"\>")

        def format_senior(senior):
            if not senior:
                return "<ParaStyle:Senior Info Text>"
            else:
                senior_string = u"<ParaStyle:Senior Info Text>"
                senior_string += senior.kerberos
                senior_string += BULLET
                senior_string += senior.major
                if senior.minor:
                    senior_string += ", "+senior.minor
                senior_string += SLASHES
                senior_string += senior.home_town + ", " + format_state(senior.home_state_or_country)
                if senior.lg:
                    senior_string += BULLET
                    senior_string += format_lg(senior.lg)
                activities = Activity.objects.filter(senior = senior)
                if activities:
                    senior_string += SLASHES
                    for i, activity in enumerate(activities):
                        if i:
                            senior_string += BULLET
                        senior_string += activity.title
                        senior_string += " <cPosition:Superscript>"
                        senior_string += activity.years
                        senior_string += "<cPosition:>"
                        if activity.offices:
                            senior_string += " (" + activity.offices + ")"
                if senior.quote:
                    senior_string += SLASHES
                    senior_string += sanitize(senior.quote)
                    if senior.quote_author:
                        senior_string += DASH
                        senior_string += sanitize(senior.quote_author)
                return senior_string

        for i in range(len(pages)):
            seniors = pages[i]
            if len(seniors) < SENIORS_PER_PAGE:
                half_num = int(len(seniors)/2.0 + 0.5)
                if i % 2 == 0: #On a left-hand page
                    seniors = [None]*(SENIORS_PER_ROW-half_num) \
                        + seniors[:half_num]\
                        +[None]*(SENIORS_PER_PAGE-len(seniors)-(SENIORS_PER_ROW-half_num))\
                        + seniors[half_num:]
                else:
                    seniors = seniors[:half_num]\
                        +[None]*(SENIORS_PER_ROW-half_num)\
                        +seniors[half_num:]\
                        +[None]*(SENIORS_PER_PAGE-len(seniors)-(SENIORS_PER_ROW-half_num))

            images = ""
            page_string = u"""<UNICODE-MAC>
<Version:7><FeatureSet:InDesign-Roman>"""
            for senior in seniors:
                if senior:
                    page_string += "<ParaStyle:Senior Name>%s<cNextXChars:Box>\n" % format_name(senior.name)
                    images += senior.image_path+"\n"
                else:
                    page_string += "<ParaStyle:Senior Name><cNextXChars:Box>\n"
                    images += "\n"
            for j in range(SENIORS_PER_ROW):
                page_string += format_senior(seniors[j])
                page_string += "\n"
                page_string += format_senior(seniors[j+SENIORS_PER_ROW])
                page_string += "<cNextXChars:Column>\n"

            zip.writestr("page%02d.txt" % i, codecs.BOM_UTF16_LE + page_string.encode("utf_16_le"))
            zip.writestr("images%02d.txt" % i, images)
        zip.close()
        return response

    export_as_tagged_text.short_description = "Export selected seniors to Adobe Tagged Text"

    def export_as_csv(modeladmin, request, queryset):
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=seniors.csv'

        sorted_seniors = _sort_seniors(queryset)

        writer = csv.writer(response,)
        writer.writerow(['name', 'firstname', 'lastname', 'comments',
                         'kerberos', 'major', 'minor', 'hometown',
                         'homeState', 'lg', 'quote', 'author',
                         'activity1', 'years1', 'offices1',
                         'activity2', 'years2', 'offices2',
                         'activity3', 'years3', 'offices3',
                         'activity4', 'years4', 'offices4',
                         'activity5', 'years5', 'offices5', ])

        for senior in sorted_seniors:
            this_row = [format_name(senior.name).encode('utf8'),
                             senior.name.strip().split(" ")[0].encode('utf8'),
                             senior.name.strip().split(" ")[-1].encode('utf8'),
                             senior.name_comments.encode('utf8'),
                             senior.kerberos.encode('utf8'),
                             format_major(senior.major).encode('utf8'),
                             senior.minor.encode('utf8'),
                             senior.home_town.encode('utf8'),
                             senior.home_state_or_country.encode('utf8'),
                             senior.lg.encode('utf8'),
                             senior.quote.encode('utf8'),
                             senior.quote_author.encode('utf8')]

            activities = Activity.objects.filter(senior = senior)
            for activity in activities:
                this_row.append(activity.title.encode('utf8'))
                this_row.append(format_years(activity.years).encode('utf8'))
                this_row.append(activity.offices.encode('utf8'))

            writer.writerow(this_row)
        return response

    export_as_csv.short_description = "Export selected seniors to CSV"


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'senior')

admin.site.register(Senior, SeniorAdmin)
admin.site.register(Activity, ActivityAdmin)
