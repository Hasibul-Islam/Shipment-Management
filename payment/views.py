from django.shortcuts import render, get_object_or_404, redirect
from .models import Payment
from .forms import PaymentForm
import uuid
import datetime
from django.contrib import messages
from orders.models import Order
from shipment_tracking.models import ShipmentTracking
from product.models import Product
# Create
def create_payment(request, pk):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_status = form.cleaned_data.get('payment_status')
            invoice_no=uuid.uuid4()
            if payment_status:
                paid_date = datetime.datetime.now()
            else:
                paid_date=None
            order_no= Order.objects.get(pk=pk).order_no
            try:
                check_payment_object = get_object_or_404(Payment, order_no=order_no)
                if check_payment_object:
                    error_msg = "Payment for this order is already created. Order No:  "+order_no
                    messages.error(request, message=error_msg)
                    return redirect('order_list')
            except:
                None
            
            payments = Product.objects.filter(order_no=order_no)
            
            if payments:
                total_price = 0
                for payment in payments:
                    total_price+=payment.unit_price*payment.quantity
            else:
                error_msg = "Please add products for this order  "+order_no
                messages.error(request, message=error_msg)
                return redirect('order_list')
            Payment.objects.create(order_no=order_no, total_price=total_price, payment_status=payment_status,paid_date=paid_date,invoice_no=invoice_no)
            
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'payment/create_payment.html', {'form': form})

# Read
def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'payment/payment_list.html', {'payments': payments})

def payment_detail(request, pk):
    payment = get_object_or_404(Payment, id=pk)
    products = Product.objects.filter(order_no=payment.order_no)
    return render(request, 'payment/payment_details.html', {'payment': payment, 'products':products})

# Update
def update_payment(request, pk):
    payment = get_object_or_404(Payment, id=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            payment_staus=form.cleaned_data.get('payment_status')
            print(payment_staus)
            if payment_staus:
                payment = Payment.objects.get(pk=pk)
                payment.payment_status = True
                payment.paid_date = datetime.datetime.now()
                payment.save()
            else:
                payment = Payment.objects.get(pk=pk)
                payment.paid_date=None
                payment.payment_status = False
                payment.save()
            return redirect('payment_list')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'payment/create_payment.html', {'form': form, 'payment': payment})

# Delete
def delete_payment(request, pk):
    payment = get_object_or_404(Payment, id=pk)
    try:
        shipment = get_object_or_404(ShipmentTracking, order_no=payment.order_no)
        if shipment.shipped:
            error_msg = "This order is shipped. Can not be deleted the payment for this order. Order No: "+payment.order_no
            messages.error(request, message=error_msg)
        
            return redirect('order_list')
    except:
        None
    if request.method == 'POST':
        payment.delete()
        return redirect('payment_list')
    return render(request, 'payment/delete_payment.html', {'payment': payment})
