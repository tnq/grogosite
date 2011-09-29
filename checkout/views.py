# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from checkout.models import *

from datetime import datetime, timedelta
import time

@login_required
def graph_checkouts(request):
    equipment = Equipment.objects.all()
    all_checkouts = []
    toutc = timedelta(hours=-5)
    plusday = timedelta(days=1)

    for e in equipment:
        checkouts = Checkout.objects.filter(equipment=e).order_by(date_out)
        checkout_list = []
        for c in checkouts:
            checkout_list.append((1000*time.mktime(c.date_out.utctimetuple()), 1))
            checkout_list.append((1000*time.mktime(c.date_in.utctimetuple()), 0))
        all_checkouts.append(checkout_list)

    return render_to_response('checkout/graph.html', {'checkouts':all_checkouts})

def graph_user_checkouts(request):
    checkouts = request.user.checkouts.order
    equipment = [c.equipment for c in checkouts]
    all_checkouts = []
    toutc = timedelta(hours=-5)
    plusday = timedelta(days=1)

    for e in equipment:
        checkouts = Checkout.objects.filter(equipment=e).order_by(date_out)
        checkout_list = []
        for c in checkouts:
            checkout_list.append((1000*time.mktime(c.date_out.utctimetuple()), 1))
            checkout_list.append((1000*time.mktime(c.date_in.utctimetuple()), 0))
        all_checkouts.append(checkout_list)

    return render_to_response('checkout/graph.html', {'checkouts':all_checkouts})

#Use URL (i.e. checkout/equipment/TNQ1234)
@login_required
def graph_equipment_checkouts(request, equipment):
    checkouts = Checkout.objects.filter(equipment=equipment)
    equipment = [c.equipment for c in checkouts]
    all_checkouts = []
    toutc = timedelta(hours=-5)
    plusday = timedelta(days=1)

    for e in equipment:
        checkouts = Checkout.objects.filter(equipment=e).order_by(date_out)
        checkout_list = []
        for c in checkouts:
            checkout_list.append((1000*time.mktime(c.date_out.utctimetuple()), 1))
            checkout_list.append((1000*time.mktime(c.date_in.utctimetuple()), 0))
        all_checkouts.append(checkout_list)

    return render_to_response('checkout/graph.html', {'checkouts':all_checkouts})

@login_required
def view_equipment(request):
    digital_cameras = Equipment.objects.filter(equip_type="CAMERA").order_by("brand","-model")
    film_cameras = Equipment.objects.filter(equip_type="35MM_CAMERA").order_by("brand","-model")
    medium_cameras = Equipment.objects.filter(equip_type="MEDIUM_FORMAT_CAMERA").order_by("brand","-model")
    large_cameras = Equipment.objects.filter(equip_type="LARGE_FORMAT_CAMERA").order_by("brand","-model")
    lenses = Equipment.objects.filter(equip_type="LENS").order_by("brand","-model")

#key_func = lambda r: r.date_due() if r.date_due() else datetime(1990,01,01,00,00,00,00)

#digital_cameras = sorted(digital_cameras, key=key_func)
#film_cameras = sorted(film_cameras, key=key_func)
#medium_cameras = sorted(medium_cameras, key=key_func)
#large_cameras = sorted(large_cameras, key=key_func)
#lenses = sorted(lenses, key=key_func)

    return render_to_response('checkout/view_equipment.html', { 'digital_cameras'   : digital_cameras,
                                                                'film_cameras'      : film_cameras,
                                                                'medium_cameras'    : medium_cameras,
                                                                'large_cameras'     : large_cameras,
                                                                'lenses'            : lenses,
                                                              })

