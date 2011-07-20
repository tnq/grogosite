from checkout.models import User, Equipment, Checkout
from django.contrib import admin
import datetime

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('pet_name','equip_type','brand','model', 'barcode_id',)
    list_filter = ('equip_type',)
    fieldsets = (
        ('Technique Information', { 
            'fields':('barcode_id', 'pet_name', 'checkout_hours'),
        }),
        ('Hardware', {
            'fields':('equip_type', 'brand', 'model', 'serial'),
        }),
        ('Extra Information', {
            'fields':('description', 'manual_link', 'notes'),
            'classes':('collapse',),
        }),
    )

class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'equipment', 'date_out', 'date_due', 'date_in', 'returned',)
    list_filter = ('user','equipment', )
    actions = ['return_equipment',]

    def return_equipment(self, request, queryset):
        rows_updated = queryset.update(date_in = datetime.datetime.now())
        names = [c.equipment.__unicode__() for c in queryset]
        if rows_updated == 1:
            message_bit = names[0] + " was"
        else:
            message_bit = ", ".join(names) + " were"
        self.message_user(request, "%s marked as checked in right now." % message_bit)

    return_equipment.short_description = "Mark items as returned right now"

class UserAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'email', 'is_staff', ) 


admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(User, UserAdmin)
