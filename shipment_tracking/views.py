from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.core.mail import EmailMessage
from django.contrib import messages
from django.http import HttpResponseRedirect
from shipment_tracking.models import ShipmentTracking
from company.models import CompanyDetails
from orders.models import Order
import threading
import time
from shipment.models import CNFInfo as CNF
from payment.models import Payment

from django.core.mail import EmailMultiAlternatives
def send_delayed_email(subject, text_content, html_content, from_email, to):
    def send_email():
        time.sleep(5)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    threading.Thread(target=send_email).start()

# def send_delayed_email(subject, message, recipient_list):
#     def send_email():
#         # Wait for 5 seconds
#         time.sleep(5)
#         # Send the email
#         msg = EmailMessage(subject, message,to=recipient_list)
#         msg.send()
#         print('sent')
#     # Start a new thread to send the email
#     threading.Thread(target=send_email).start()
    

# def shipment_tracking_edit(request, shipment_id):
#     shipment_tracking = ShipmentTracking.objects.get(shipment_no=shipment_id)
#     shipment_tracking_timeline = ShipmentTrackingTimeLine.objects.get(shipment_no=shipment_id)
#     if request.method == 'POST':
#         unique_id = request.POST.get('code', '')
        
#         # print(stuff_unique_id, shipment_tracking.stuff_unique_id)
#         if shipment_tracking.ready == True and shipment_tracking.stuff_unique_id==unique_id:
#             # print(shipment_tracking.pk)
#             ShipmentTracking.objects.filter(pk=shipment_tracking.pk).update(shipped=True)
#             ShipmentTrackingTimeLine.objects.filter(pk=shipment_tracking_timeline.pk).update(order_shipped_date=datetime.datetime.now())
#             return redirect('home')
#         elif shipment_tracking.shipped==True and shipment_tracking.overseas_unique_id==unique_id:
#             ShipmentTracking.objects.filter(pk=shipment_tracking.pk).update(reached_overseas=True)
#             ShipmentTrackingTimeLine.objects.filter(pk=shipment_tracking_timeline.pk).update(order_reached_overseas_date=datetime.datetime.now())
#             return redirect('home')
#         elif shipment_tracking.reached_overseas==True and shipment_tracking.buyer_unique_id==unique_id:
#             ShipmentTracking.objects.filter(pk=shipment_tracking.pk).update(product_delivered=True)
#             ShipmentTrackingTimeLine.objects.filter(pk=shipment_tracking_timeline.pk).update(order_delivered_date=datetime.datetime.now())
#             order = Order.objects.get(order_no=shipment_tracking.order_no)
#             Order.objects.filter(pk=order.pk).update(order_delivery_status=True, delivered_on=datetime.datetime.now() )
#             return redirect('home')
#         elif shipment_tracking.product_delivered==True and shipment_tracking.buyer_payment_unique_id==unique_id:
#             try:
#                 payment = Payment.objects.get(order_no=shipment_tracking.order_no)
#             except:
#                 payment=None
#             if payment:
#                 ShipmentTracking.objects.filter(pk=shipment_tracking.pk).update(payment_lc=True)
#                 ShipmentTrackingTimeLine.objects.filter(pk=shipment_tracking_timeline.pk).update(order_payment_lc_date=datetime.datetime.now())
                
#                 Payment.objects.filter(pk=payment.pk).update(payment_status=True, paid_date=datetime.datetime.now())
#             else:
#                 error_msg ="Payment for this order hasn't been created yet. We will inform the origin company. Kindly try again later. You will be given notification once again through your email. "
#                 messages.error(request, message=error_msg)
#                 send_delayed_email('Add the payment. Buyer is waiting to update','New Notification!!!', '<p>You buyer is waiting to update the shipment of <strong>'+shipment_tracking.shipment_no+"</strong> and order no <strong> "+shipment_tracking.order_no+"</strong>. Update the payment form.","nehaa.ahmmed@outlook.com", ['polok.hasibul@gmail.com'])
#                 return redirect('home')
            
#             return redirect('home')
#     return render(request, 'tracking_order/tracking_update.html')
def view_shipment(request, pk):
    shipment_tracking = get_object_or_404(ShipmentTracking, pk=pk)
    if request.method=='POST':
        
        subject="Kindly Update the Tracking with the given Secret Key"
        order=get_object_or_404(Order, order_no=shipment_tracking.order_no)
        
        company=get_object_or_404(CompanyDetails, customer_no=order.company)
        recipient_list = [company.email]
        
        checklist = [
                    shipment_tracking.order_delivered,
                    shipment_tracking.payment_lc
                    ]
        i=0
        while(i<2):
            if checklist[i]==False:
                if i==0:
                    unique_id=shipment_tracking.buyer_unique_id
                elif i==1:
                    unique_id=shipment_tracking.buyer_payment_unique_id
                message="<p> Here is your link http://127.0.0.1:8000/shipment-tracking/update/"+str(pk)+"/ . and your secret code to update the tracking is <strong>"+unique_id+"</strong>. Thank you for helping."    
                
                send_delayed_email(subject,"This is an important message", message,"nehaa.ahmmed@outlook.com",recipient_list)
                
            i+=1
    return render(request, 'shipment_tracking/view_shipment.html', {'shipment_tracking': shipment_tracking})
    


def shipment_confirm_update_buyer(request, pk):
    shipment_tracking = get_object_or_404(ShipmentTracking, id=pk)
    checklist = [shipment_tracking.ready, shipment_tracking.shipped, shipment_tracking.reached_overseas,
                 shipment_tracking.order_delivered, shipment_tracking.payment_lc
                 ]
    if checklist[0]==False:
        status="is Ready"
    elif checklist[1]==False:
        status="is Shipped"
    elif checklist[2]==False:
        status="has Reached Overseas"
    elif checklist[3]==False:
        status="is Delivered"
    elif checklist[4]==False:
        status="has got Payment"
    else:
        status=None
    
    
    
    if request.method == 'POST':
        
        
        if checklist[3]==False:
            unique_code = request.POST.get("code")
            if shipment_tracking.buyer_unique_id==unique_code:
                Order.objects.filter(order_no=shipment_tracking.order_no).update(order_date=datetime.now(),order_delivery_status=True)
                ShipmentTracking.objects.filter(pk=pk).update(order_delivered  =True, order_delivered_date  =datetime.now())
                return redirect('home')
        if checklist[4]==False:
            unique_code = request.POST.get("code")
            if shipment_tracking.buyer_payment_unique_id==unique_code:
                ShipmentTracking.objects.filter(pk=pk).update(payment_lc  =True, order_payment_lc_date  =datetime.now())
                return redirect('home')
    return render(request, 'tracking_order/confirm_update.html', {'shipment_tracking': shipment_tracking, 
                                                                  'status':status, 
                                                                  })

def shipment_confirm_update_cnf(request, pk):
    shipment_tracking = get_object_or_404(ShipmentTracking, id=pk)
    checklist = [shipment_tracking.ready, shipment_tracking.shipped, shipment_tracking.reached_overseas,
                 shipment_tracking.order_delivered, shipment_tracking.payment_lc
                 ]
    if checklist[0]==False:
        status="is Ready"
    elif checklist[1]==False:
        status="is Shipped"
    elif checklist[2]==False:
        status="has Reached Overseas"
    
    else:
        status=None
    
    
    
    if request.method == 'POST':
        
        if checklist[0]==False:
            carton_description=request.POST.get('carton')
            print(carton_description)
            if carton_description==None or carton_description=="":
                return HttpResponseRedirect(request.path_info)
            ShipmentTracking.objects.filter(pk=pk).update(ready=True, order_ready_date=datetime.now(),carton_description=carton_description)
            
            return redirect('home')
        if checklist[1]==False:
            
            container_description = request.POST.get('container')
            if container_description==None or container_description=="":
                return HttpResponseRedirect(request.path_info)
            ShipmentTracking.objects.filter(pk=pk).update(shipped=True, order_shipped_date=datetime.now(),container_description=container_description )
            return redirect('thank_you')
        if checklist[2]==False:
            
            ShipmentTracking.objects.filter(pk=pk).update(reached_overseas =True, order_reached_overseas_date =datetime.now())
            
            return redirect('thank_you')
        
    return render(request, 'tracking_order/confirm_update.html', {'shipment_tracking': shipment_tracking, 
                                                                  'status':status, 
                                                                  })



def tracking_list(request):
    shipment_trackings=ShipmentTracking.objects.all()
    return render(request, 'tracking_order/tracking-list.html', {'shipment_trackings':shipment_trackings})

def tracking_list_cnf(request):
    try:
        cnf = get_object_or_404(CNF, email=request.user.email)
        shipment_trackings=ShipmentTracking.objects.filter(cnf_no=cnf.cnf_no)
    except:
        shipment_trackings=None
    return render(request, 'tracking_order/tracking-list.html', {'shipment_trackings':shipment_trackings})

def thank_you(request):
    return render(request, 'tracking_order/thank_you.html')










