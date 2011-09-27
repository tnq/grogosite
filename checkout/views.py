# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from checkout.models import *

import datetime
import time

@login_required
def graph_checkouts(request):
    equipment = Equipment.objects.all()
    all_checkouts = []
    toutc = datetime.timedelta(hours=-5)
    plusday = datetime.timedelta(days=1)

    for e in equipment:
        checkouts = Checkout.objects.filter(equipment=e).order_by(date_out)
        checkout_list = []
        for c in checkouts:
            checkout_list.append((1000*time.mktime(c.date_out.utctimetuple()), 1))
            checkout_list.append((1000*time.mktime(c.date_in.utctimetuple()), 0))
        all_checkouts.append(checkout_list)

    return render_to_response('checkout/graph.html', {'checkouts':all_checkouts})

@login_required
def equipment_status(request):
    digital = Equipment.objects.filter(equip_type="CAMERA")
    lenses =          Equipment.objects.filter(equip_type="LENS")
    cards =           Equipment.objects.filter(equip_type="MEMORY")
    
    return render_to_response('checkout/equipment.html', {'digital':digital, 'lenses':lenses, 'cards':cards})
