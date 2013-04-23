import csv
import datetime
from django import forms
from django.contrib import admin
from django.http import HttpResponse
from creditcard.models import Purchaser, LineItem, Patron

class LineItemInline(admin.TabularInline):
    model = LineItem
    extra = 0

class PatronInline(admin.TabularInline):
    model = Patron
    extra = 0

class PurchaserForm(forms.ModelForm):
    class Meta:
        model = Purchaser

    def clean(self):
        cleaned_data = self.cleaned_data
        paymenttype = cleaned_data.get("paymenttype")
        studentid = cleaned_data.get("studentid")
        
        if paymenttype == "t" and not studentid:
            raise forms.ValidationError("You must specify a student id number for purchasers paying with TechCASH.")
        
        return cleaned_data

class PurchaserAdmin(admin.ModelAdmin):
    form = PurchaserForm
    list_display = ('id', 'sort_name', 'amount_paid', 'paymentid', )
    list_filter = ('paymenttype',)
    search_fields = ('firstname', 'lastname', 'paymentid', )
    inlines = [ PatronInline, LineItemInline, ]
    readonly_fields = ('paymentid', )
    fieldsets = [
        ('Contact Information', {'fields':['firstname','lastname','email','phone']}),
        ('Billing Information', {'fields':['purchasedate', ('paymenttype','studentid','paymentid'), 'amount_paid', 'bill_street', 'bill_street2', 'bill_city', 'bill_state', 'bill_zip']}),
    ]

    actions = ['export_techcash_csv']

    def export_techcash_csv(modeladmin, request, queryset):
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=techcash.csv'
    
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Student ID', 'Bill Amount'])
        for purchaser in queryset:
            writer.writerow([purchaser.firstname,
                             purchaser.lastname,
                             purchaser.studentid,
                             purchaser.amount_paid])
        return response 

    export_techcash_csv.short_description = "Export selected TechCASH purchasers to CSV"

class LineItemForm(forms.ModelForm):
    class Meta:
        model = LineItem

    def clean(self):
        cleaned_data = self.cleaned_data
        deliverytype = cleaned_data.get("deliverytype")
        deliverydate = cleaned_data.get("deliverydate")
        purchaser = cleaned_data.get("purchaser")
        
        if deliverytype != "n" and not deliverydate:
            raise forms.ValidationError("You must specify a delivery date.")
        elif deliverydate and deliverytype == "n":
            raise forms.ValidationError("You must specify a delivery type.")
        
        return cleaned_data

class LineItemAdmin(admin.ModelAdmin):
    form = LineItemForm
    list_display = ('year', 'purchaser', 'recipient', 'delivered')
    search_fields = ('purchaser__firstname', 'purchaser__lastname', 'ship_first_name', 'ship_last_name', 'purchaser__email', )
    list_filter = ('shipping_paid', 'deliverytype', 'year')
    readonly_fields = ('purchaser',)
    actions = ['export_as_csv', 'mark_as_shipped']

    def export_as_csv(modeladmin, request, queryset):
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=addresses.csv'
    
        writer = csv.writer(response)
        writer.writerow(['Full Name', 'Company', 'Address 1', 'Address 2', 'City', 'State', 'Zip Code', 'Country', 'E Mail'])
        for lineitem in queryset:
            writer.writerow([lineitem.ship_first_name + " " + lineitem.ship_last_name,
                             'MIT Technique',
                             lineitem.ship_street,
                             lineitem.ship_street2,
                             lineitem.ship_city,
                             lineitem.ship_state,
                             lineitem.ship_zip,
                             'US',
                             lineitem.purchaser.email])
        return response 

    export_as_csv.short_description = "Export selected addresses to CSV"

    def mark_as_shipped(self, request, queryset):
        rows_updated = queryset.update(deliverytype="s", deliverydate=datetime.date.today())
        if rows_updated == 1:
            message_bit = "1 book was"
        else:
            message_bit = "%s books were" % rows_updated
        self.message_user(request, "%s successfully marked as delivered today." % message_bit)

    mark_as_shipped.short_description = "Mark selected line items as shipped today"

class PatronAdmin(admin.ModelAdmin):
    list_display = ('year', 'name', 'purchaser', 'color')

admin.site.register(Purchaser, PurchaserAdmin)
admin.site.register(LineItem, LineItemAdmin)
admin.site.register(Patron, PatronAdmin)
