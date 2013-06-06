from django.db import models
from django.forms import ModelForm

# Create your models here.
class Purchaser(models.Model):
    payment_choices = (  ('c', 'Credit Card'),
                         ('s', 'Cash'),
                         ('t', 'TechCash'),
                         ('x', 'Check'),
                         ('f', 'Free'),
                         ('r', 'Replacement')
                      )
    payment_dict = {}
    for choice in payment_choices:
        payment_dict[choice[0]] = choice[1]

    firstname = models.CharField('First Name', max_length = 30)
    lastname = models.CharField('Last Name', max_length = 30)
    paymentid = models.CharField('Payment ID', max_length = 32, unique = True, null = True)
    studentid = models.IntegerField('Student ID', blank = True, null = True)
    paymenttype = models.CharField('Payment Type', max_length = 1, choices=payment_choices)
    amount_paid = models.IntegerField('Amount Paid')
    purchasedate = models.DateField('Purchase Date', help_text="YYYY-MM-DD.")
    bill_street = models.CharField('Address', max_length = 50, blank = True)
    bill_street2 = models.CharField('Address 2', max_length = 50, blank = True)
    bill_city = models.CharField('City', max_length = 50, blank = True)
    bill_state = models.CharField('State', max_length = 2, blank = True)
    bill_zip = models.CharField('ZIP Code', max_length = 5, blank = True)
    email = models.EmailField()
    phone = models.CharField(max_length = 15, blank = True)


    def get_full_payment_type(self):
        return self.payment_dict[self.paymenttype]

    def get_full_name(self):
        return self.firstname + " " + self.lastname

    def sort_name(self):
        return self.lastname.capitalize() + ", " + self.firstname.capitalize()
    sort_name.admin_order_field = 'lastname'

    def __unicode__(self):
        return self.sort_name()

class PurchaserForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Purchaser

class LineItem(models.Model):
    delivery_choices = (
                            ('n', 'Not delivered'),
                            ('p', 'Picked Up'),
                            ('s', 'Shipped'),
                            ('i', 'In-Person Delivery'),
                            ('v', 'Voided'),
                       )

    delivery_dict = {}
    for choice in delivery_choices:
        delivery_dict[choice[0]] = choice[1]

    purchaser = models.ForeignKey(Purchaser)
    year = models.IntegerField('Book Year')
    deliverytype = models.CharField('Delivery Type', max_length=1, choices=delivery_choices )
    deliverydate = models.DateField('Delivery Date', blank = True, null=True)
    ship_first_name = models.CharField('Recipient First Name', max_length = 50)
    ship_last_name = models.CharField('Recipient Last Name', max_length = 50)
    shipping_paid = models.BooleanField('Shipping Paid?')
    ship_street = models.CharField('Ship Street', max_length = 50, blank = True)
    ship_street2 = models.CharField('Ship Street 2', max_length = 50, blank = True)
    ship_city = models.CharField('Ship City', max_length = 50, blank = True)
    ship_state = models.CharField('Ship State', max_length = 2, blank = True)
    ship_zip = models.CharField('Ship Zip', max_length = 7, blank = True)

    def __unicode__(self):
        return str(self.year) + " " + self.ship_first_name + " " + self.ship_last_name

    def delivered(self):
        return self.deliverytype != 'n'
    delivered.boolean = True

    def deliverytype_plain(self):
        return self.delivery_dict[self.deliverytype]

    def recipient(self):
        return self.ship_last_name.capitalize() + ", " + self.ship_first_name.capitalize()

    def get_ship_full_name(self):
        return self.ship_first_name + " " + self.ship_last_name
    recipient.admin_order_field = 'ship_last_name'

class LineItemForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = LineItem

class Patron(models.Model):
    patron_choices = (  ('b', 'Bronze'),
                        ('s', 'Silver'),
                        ('g', 'Gold'),
                        ('p', 'Platinum'),
                     )

    patron_dict = {}
    reverse_patron_dict = {}
    for choice in patron_choices:
        patron_dict[choice[0]] = choice[1]
        reverse_patron_dict[choice[1]] = choice[0]

    purchaser = models.ForeignKey(Purchaser)
    name = models.CharField('Patron Name', max_length = 100)
    year = models.IntegerField('Patron Year')
    color = models.CharField(max_length = 1, choices=patron_choices)

    def get_patron_title(self):
        return self.patron_dict[self.color]

    def __unicode__(self):
        return self.name

class PatronForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Patron
