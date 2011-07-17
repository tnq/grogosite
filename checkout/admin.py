from checkout.models import User, Equipment, Checkout
from django.contrib import admin

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('pet_name','equip_type','brand','model', 'barcode_id',)
    list_filter = ('equip_type',)

class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'equipment', 'date_out', 'date_in', 'returned',)
    list_filter = ('user','equipment', )

admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(User)
