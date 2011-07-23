from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User as DjangoUser
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save)
def update_nulls(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if field.null and getattr(instance, field.name) == "":
            setattr(instance, field.name, None)

# Create your models here.
class User(DjangoUser):
    user = models.OneToOneField(DjangoUser, primary_key=True, db_column="id", parent_link=True, related_name="checkout_user")
    barcode_id = models.CharField("MIT ID Number", max_length=9, unique=True)
    phone = models.CharField("Phone Number", max_length=20, blank=True, null=True)

    def __unicode__(self):
        if self.user.first_name or self.user.last_name:
            return "%s %s" %(self.user.first_name, self.user.last_name)
        else:
            return str(self.user.username)

class Equipment(models.Model):
    equip_choices = (   ('CAMERA', 'Camera'),
                        ('LENS', 'Lens'),
                        ('MEMORY', 'Memory Card'),
                        ('EXTERNAL_FLASH', 'External Flash'),
                        ('STROBE', 'Strobe'),
                        ('TRIPOD', 'Tripod'),
                        ('MONOPOD', 'Monopod'),
                        ('ACCESSORY', 'Accessory'),
                        ('35MM_CAMERA', '35mm Camera'),
                        ('MEDIUM_FORMAT_CAMERA', 'Medium-Format Camera'),
                        ('LARGE_FORMAT_CAMERA', 'Large-Format Camera'),
                        ('MEDIUM_FORMAT_BACK', 'Medium-Format Film Back'),
                        ('CHARGER', 'Charger'),
                        ('BATTERY', 'Battery'),
                        ('SNAX', 'Snacks'),
                    )


    barcode_id = models.CharField('Barcode ID', max_length=13, unique=True)
    equip_type = models.CharField('Equipment Type', max_length=30, choices=equip_choices)
    pet_name = models.CharField('Pet Name', max_length=30, blank=True, null=True)
    brand = models.CharField('Brand', max_length=30, help_text='Nikon, Mamiya, etc')
    model = models.CharField('Model', max_length=128, blank=True, null=True, help_text='D300, D90, SB900, etc')
    checkout_hours = models.IntegerField('Checkout Length', help_text='Number of hours equipment can be checked out')
    description = models.TextField(max_length=500, blank=True, null=True)
    manual_link = models.URLField('Manual Link', max_length=256, blank=True, null=True, help_text='URL of the equipment manual')
    serial = models.CharField('Serial Number', max_length=128, blank=True, null=True)
    notes = models.TextField(max_length=500, blank=True, null=True)

    def __unicode__(self):
        if self.pet_name:
            return self.pet_name
        else:
            return self.barcode_id

    class Meta:
        verbose_name_plural = "Equipment"

class Checkout(models.Model):
    user = models.ForeignKey(User, related_name="checkouts")
    equipment = models.ForeignKey(Equipment)
    manboard_member = models.ForeignKey(User, related_name="authorized_checkouts")
    date_out = models.DateTimeField()
    date_due = models.DateTimeField()
    date_in = models.DateTimeField(blank=True, null=True)

    def returned(self):
        return self.date_in != None
    returned.boolean = True

    def __unicode__(self):
        return "%s - %s" %(self.user.user.username, self.equipment.__unicode__())

