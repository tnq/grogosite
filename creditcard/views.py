# Create your views here.
from django.shortcuts import render_to_response
from creditcard.models import Purchaser, LineItem, Patron
from mainsite.models import Setting
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django import forms
import collections
import json

class UploadFileForm(forms.Form):
    orders_file = forms.FileField()
    
@login_required
def upload(request):
    """Upload the Cybersource CSV file of orders for processing."""

    purchased_items = []
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            orders_file = request.FILES['orders_file']
            reader = csv.DictReader(orders_file)
            purchased_items = create_orders_from_file(reader)
    else:
        form = UploadFileForm()

    context = {'form':form, 'purchased_items':purchased_items}
    context.update(csrf(request))

    return render_to_response('admin/creditcard/upload.html', context )

import csv, time
def create_orders_from_file(reader):
    """Process the Cybersource CSV orders file into Purchasers and LineItems."""

    returnlist = []
    for order in reader:
        paymentid = order['Merchant Reference Number'].strip("'")
        comment = order['Comment'] or order['MerDatafield1']
        line_items = [item.strip() for item in comment.split(',')]
        
        only_shipping = len(line_items) == 1 and line_items[0] == 'Shipping'
        already_loaded = Purchaser.objects.filter(paymentid = paymentid).count() != 0
        order_okay = order['ReplyRFlag'] in ["SOK", "SOK,SOK"]
        is_reimbursement = order['Source'] == "UBC"

        if not already_loaded and order_okay and not is_reimbursement:
            purchasedate = time.strftime("%Y-%m-%d",  time.strptime(order['Request Date'], "%b %d %Y %H:%M:%S %p"))

            purchaser = Purchaser(firstname = order['BillToFirstName'],
                lastname = order['BillToLastName'],
                purchasedate = purchasedate,
                paymentid = paymentid,
                paymenttype = 'c',
                amount_paid = int(float( order['PaymentAmount'] )),
                bill_street = order['BillToAddress1'],
                bill_street2 = order['BillToAddress2'],
                bill_city = order['BillToCity'],
                bill_state = order['BillToState'],
                bill_zip = order['BillToZip'],
                email = order['BillToEmail'],
                phone = order['BillToPhone'])

            purchaserlist = [purchaser.firstname + " " + purchaser.lastname + " ($" + str(purchaser.amount_paid) + ")"]
            itemlist = []
            
            if only_shipping:
                itemlist.append("ONLY SHIPPING - NOT ADDED INTO DATABASE")
            else:
                purchaser.save()

                for item in line_items:
                    if len(item) == 0:
                        itemlist.append("PROBLEMS WITH THIS PURCHASER")

                    elif item == "Shipping":
                        itemlist.append("Shipping")

                    else:
                        #2012-Book, 2012-FreshmanBundle, 2012-Bronze
                        year = int(item[0:4])
                        item = item[5:] # 2012-Book --> Book

                        if item == "Book":
                            create_lineitem(year = year,
                                            purchaser = purchaser,
                                            order = order,
                                            shipping_paid = 'Shipping' in line_items)
                            itemlist.append(year)

                        elif item == "FreshmanBundle":
                            for tempyear in range(year, year+4):
                                create_lineitem(year = tempyear,
                                                purchaser = purchaser,
                                                order = order,
                                                shipping_paid = 'Shipping' in line_items)
                                itemlist.append(tempyear)

                        elif item == "SeniorBundle":
                            for tempyear in range(year-3, year+1):
                                create_lineitem(year = tempyear,
                                                purchaser = purchaser,
                                                order = order,
                                                shipping_paid = 'Shipping' in line_items)
                                itemlist.append(tempyear)

                        elif item in Patron.reverse_patron_dict.keys():
                            patron = Patron(purchaser = purchaser,
                                            color = Patron.reverse_patron_dict[item],
                                            year = int(year),
                                            name = order['MerDatafield2'] )
                            patron.save()
                            create_lineitem(year, purchaser, order, True)
                            itemlist.append(item)

                purchaserlist.append(itemlist)
                returnlist.append(purchaserlist)

    return returnlist

def create_lineitem(year, purchaser, order, shipping_paid):
    """Create a LineItem in the database."""

    lineitem = LineItem(purchaser= purchaser,
                        year = str(year),
                        deliverydate = None,
                        deliverytype = 'n',
                        ship_first_name = order['ShipToFirstName'],
                        ship_last_name = order['ShipToLastName'],
                        shipping_paid = shipping_paid,
                        ship_street = order['ShipToAddress1'],
                        ship_street2 = order['ShipToAddress2'],
                        ship_city = order['ShipToCity'],
                        ship_state = order['ShipToState'],
                        ship_zip = order['ShipToZip'])
    lineitem.save()

from itertools import groupby
import datetime
@login_required
def graph_dates(request):
    """Create graphs of total and per day book sales for each edition."""

    deliveries = []
    total_deliveries = []
    total = 0
    midnight = datetime.time(0, 0)
    toutc = datetime.timedelta(hours=-5)
    plusday = datetime.timedelta(days=1)

    try:
        current_year = int(Setting.objects.get(tag='tnq_year').value)
    except ObjectDoesNotExist:
        current_year = 2013

    # Exclude undelivered books
    delivered_books = LineItem.objects.exclude(deliverydate=None)
    # Exclude voided books
    delivered_books = delivered_books.exclude(deliverytype="v")
    # Only include 2013 books
    delivered_books = delivered_books.filter(year=current_year)

    delivered_books = delivered_books.order_by("deliverydate")
    ddate = lambda x: x.deliverydate
    for deliverydate, group in groupby(delivered_books, key=ddate):
        epoch_time = 1000*time.mktime((datetime.datetime.combine(deliverydate, midnight)+toutc).utctimetuple())
        num = len(list(group))
        deliveries += [[epoch_time, num]]
        total += num
        total_deliveries += [[epoch_time, total]]

    tomorrow = 1000*time.mktime((datetime.datetime.combine(datetime.date.today(), midnight)+plusday+toutc).utctimetuple())
    deliveries += [[tomorrow, 0]]

    sales = collections.defaultdict(list)
    cum_sales = collections.defaultdict(list)
    total = collections.defaultdict(lambda: 0)

    # Exclude voided books
    sold_books = LineItem.objects.exclude(deliverytype="v")
    # Exclude free books
    sold_books = sold_books.exclude(purchaser__paymenttype="f")
    # Only include years past 2009
    sold_books = sold_books.filter(year__gt=2009)

    sold_books = sold_books.order_by("year", "purchaser__purchasedate")

    for (year, purchasedate), group in groupby(sold_books, key=lambda x: (x.year, x.purchaser.purchasedate)):
        epoch_time = datetime.datetime.combine(purchasedate, midnight)
        try:
            epoch_time = epoch_time.replace(year=current_year+int(epoch_time.year)-int(year))
        except ValueError:
            # Leap years, bah
            epoch_time = epoch_time.replace(year=current_year+int(epoch_time.year)-int(year),
                                            day=28)
        epoch_time = 1000*time.mktime((epoch_time+toutc).utctimetuple())
        num = len(list(group))
        sales[year] += [[epoch_time, num]]
        total[year] += num
        cum_sales[year] += [[epoch_time, total[year]]]

    return render_to_response("creditcard/graph.html", {
        "deliveries":deliveries,
        "sales":json.dumps(dict(sales)),
        "total_deliveries":total_deliveries,
        "cum_sales":json.dumps(dict(cum_sales))})
