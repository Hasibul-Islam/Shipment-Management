from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from orders.models import Order
from company.models import CompanyDetails
from payment.models import Payment
from django.contrib import messages
from shipment_tracking.models import ShipmentTracking
def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(request, 'products/product_detail.html', context)
def product_create(request,pk):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        # print(form.errors)
        if form.is_valid():
            
            product_name  = form.cleaned_data.get('product_name')
            gender   = form.cleaned_data.get('gender')
            size_chart     = form.cleaned_data.get('size_chart')
            color_chart  = form.cleaned_data.get('color_chart')
            
            
            fabric_description     = form.cleaned_data.get('fabric_description')
            other_descriptions  = form.cleaned_data.get('other_descriptions')
            quantity   = form.cleaned_data.get('quantity')
            unit_price   = form.cleaned_data.get('unit_price')
            
            
            order_no=Order.objects.get(pk=pk).order_no
            try:
                shipment = get_object_or_404(ShipmentTracking, order_no=order_no)
                if shipment.ready:
                    error_msg = "This order is ready. Can't be added more products."
                    messages.error(request, message=error_msg)
                    return redirect('order_list')
            except:
                None
            try:
                payment=get_object_or_404(Payment, order_no=order_no)
                if payment:
                    error_msg = "Payment already been made for this order. Order no: "+order_no+". No further products can be added. "
                    messages.error(request, message=error_msg)
                    return redirect('order_list')
            except:
                None
            contact_person=CompanyDetails.objects.get(customer_no=Order.objects.get(order_no=order_no).company).contact_person
            # print(contact_person)
            Product.objects.create(
                product_name=product_name,
                gender=gender,
                size_chart=size_chart,
                color_chart=color_chart,
                
                
                fabric_description=fabric_description,
                quantity=quantity,
                other_descriptions=other_descriptions,
                
                unit_price=unit_price,
                contact_person=contact_person,
                order_no=order_no,
            )
            return redirect('product_list')
    else:
        
        form = ProductForm()

    return render(request, 'products/product_create.html', {'form': form})



def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        shipment = get_object_or_404(ShipmentTracking, order_no=product.order_no)
        if shipment.ready:
            error_msg = "This order is ready. Can't be edited."
            messages.error(request, message=error_msg)
            return redirect('product_list')
    except:
        None
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        try:
            payment=get_object_or_404(Payment, order_no=product.order_no)
            products= Product.objects.filter(order_no=payment.order_no)
            total_price=0
            for prod in products:
                total_price+=prod.unit_price*prod.quantity
            payment.total_price=total_price
            payment.save()
        except:
            None
        return redirect('product_list')
    context = {
        'form': form
    }
    return render(request, 'products/product_create.html', context)

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        shipment = get_object_or_404(ShipmentTracking, order_no=product.order_no)
        if shipment.shipped:
            error_msg = "This order is shipped. Can't be deleted"
            messages.error(request, message=error_msg)
            return redirect('product_list')
    except:
        None
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    context = {
        'product': product
    }
    return render(request, 'products/product_delete.html', context)
