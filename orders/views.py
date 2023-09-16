from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Order
from .forms import OrderForm
from company.models import CompanyDetails
from datetime import datetime
from shipment_tracking.models import ShipmentTracking
from product.models import Product
from shipment.models import CNFInfo
from django.http import HttpResponse
from .process import html_to_pdf 
import uuid
from payment.models import Payment
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_create(request,pk):
    if request.method == 'POST':
        customer=get_object_or_404(CompanyDetails, pk=pk)
        customer_no= customer.customer_no
        form = OrderForm(request.POST)
        if form.is_valid():
            now = datetime.now()
            try:
                order_no = now.strftime("%m%d%Y")+customer.customer_company+str(Order.objects.order_by('-pk')[0].pk+1)
            except:
                order_no = now.strftime("%m%d%Y")+customer.customer_company+"#99"
            order_date = form.cleaned_data.get('order_date')
            order_delivery_status=form.cleaned_data.get('order_delivery_status')
            delivered_on=form.cleaned_data.get('delivered_on')
            Order.objects.create(
                company=customer_no, order_no=order_no,order_date=order_date,order_delivery_status=order_delivery_status,
                                 delivered_on=delivered_on)
            
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})

def order_edit(request, pk):
    
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_edit.html', {'form': form})
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    products=Product.objects.filter(order_no=order.order_no)
    if request.method=='POST':
        pdf = html_to_pdf('orders/order_detail.html')
        return HttpResponse(pdf, content_type='application/pdf')
    return render(request, 'orders/order_detail.html', {'order':order, 'products':products})
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    try:
        shipment = get_object_or_404(ShipmentTracking, order_no=order.order_no)
        if shipment.ready:
            error_msg = "This order is shipped. Can't be deleted"
            messages.error(request, message=error_msg)
    except:
        None
    if request.method == 'POST':
        order.delete()
        products = Product.objects.filter(order_no=order.order_no)
        for prod in products:
            prod.delete()
        try:
            payment = get_object_or_404(Payment, order_no=order.order_no)
            payment.delete()
        except:
            None
        try:
            tracking = get_object_or_404(ShipmentTracking, order_no=order.order_no)
            tracking.delete()
        except:
            None
        
        return redirect('order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})

def order_shipment_update(request, pk, cnf_pk):
    cnf = get_object_or_404(CNFInfo, pk=cnf_pk)
    order=get_object_or_404(Order, pk=pk)
    shipment_tracking_check=ShipmentTracking.objects.filter(order_no=order.order_no)
    if shipment_tracking_check:
        return redirect('order_list')
    if request.method == 'POST':
        try:
            payment=Payment.objects.get(order_no=order.order_no)
            
        except:
            error_msg = "Please add payment for this order  "+order.order_no
            messages.error(request, message=error_msg)
            return redirect('order_list')
        now=datetime.now()
        
        try:
            shipment_no =  now.strftime("%m%d%Y")+"shipment##"+str(ShipmentTracking.objects.order_by('-pk')[0].pk+1)
        except:
            shipment_no =  now.strftime("%m%d%Y")+"shipment##@99"
        
        ShipmentTracking.objects.create(
            order_no=order.order_no,
            shipment_no=shipment_no,
            cnf_no=cnf.cnf_no,
            order_received_date=order.order_date,
            order_received=True,
            buyer_unique_id=uuid.uuid4(), 
            buyer_payment_unique_id=uuid.uuid4()
            )
        
        Order.objects.filter(pk=pk).update(cnf_no=cnf.cnf_no)
        return redirect('order_list')
    return render(request, 'orders/order_shipment_select_confirm.html', {'order': order})

def order_shipment(request,pk):
    order = get_object_or_404(Order, pk=pk)
    shipments = CNFInfo.objects.all()
    
    return render(request, 'orders/order_shipment.html', {'order': order, 'shipments':shipments})
    

    