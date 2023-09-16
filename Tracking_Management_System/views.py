from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from accounts.decorators import check_user_able_to_see_page
from shipment_tracking.models import ShipmentTracking
from datetime import datetime
from django.db.models import Q
# @check_user_able_to_see_page(Group.objects.get(name='Admin'),Group.objects.get(name='Manager'))

def home(request):
    if request.user.is_authenticated:
        to_date= datetime.today()
        from_date= datetime.today().replace(day=1)
        shipments= ShipmentTracking.objects.filter(
                    Q(order_received_date__gte=from_date) & Q(order_received_date__lte=to_date)
                )
    else:
        return redirect('login')
    return render(request, 'home.html', {'shipments': shipments})