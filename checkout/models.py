from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User as DjangoUser

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
                        ('SNAX', 'Snacks'),
                    )


    barcode_id = models.CharField(max_length=7, unique=True)
    equip_type = models.CharField(max_length=30, choices=equip_choices)
    pet_name = models.CharField(max_length=30, blank=True, null=True)
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    manual_link = models.URLField(max_length=256, blank=True, null=True)
    serial = models.CharField(max_length=128, blank=True, null=True)
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
    date_in = models.DateTimeField(blank=True, null=True)

    def returned(self):
        return self.date_in != None
    returned.boolean = True

    def __unicode__(self):
        return "%s - %s" %(self.user.user.username, self.equipment.__unicode__())

