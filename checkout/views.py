# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from checkout.models import Equipment, Checkout, User

@login_required
def view_equipment(request):
    digital_cameras = Equipment.objects.filter(equip_type="CAMERA").order_by("brand","-model")
    film_cameras = Equipment.objects.filter(equip_type="35MM_CAMERA").order_by("brand","-model")
    medium_cameras = Equipment.objects.filter(equip_type="MEDIUM_FORMAT_CAMERA").order_by("brand","-model")
    large_cameras = Equipment.objects.filter(equip_type="LARGE_FORMAT_CAMERA").order_by("brand","-model")

    lenses = Equipment.objects.filter(equip_type="LENS").order_by("brand","-model")

    return render_to_response('checkout/view_equipment.html', { 'digital_cameras'   : digital_cameras,
                                                                'film_cameras'      : film_cameras,
                                                                'medium_cameras'    : medium_cameras,
                                                                'large_cameras'     : large_cameras,
                                                                'lenses'            : lenses,
                                                              })

