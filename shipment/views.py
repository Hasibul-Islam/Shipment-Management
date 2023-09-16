from django.shortcuts import render, get_object_or_404, redirect
from .models import CNFInfo as CNF
from .forms import ShipmentForm
from django.contrib import messages
from orders.models import Order
from product.models import Product
from shipment_tracking.models import ShipmentTracking
import os
from payment.models import Payment
from company.models import CompanyDetails as Customer
from django.http import FileResponse
import datetime
from django.db.models import Q
from shipment_tracking.pdf_generator import pdf_convertor

def shipment_list(request):
    shipments = CNF.objects.all()
    return render(request, 'shipment/shipment_list.html', {'shipments': shipments})

def shipment_detail(request, shipment_id):
    shipment = get_object_or_404(CNF, id=shipment_id)
    return render(request, 'shipment/shipment_detail.html', {'shipment': shipment})

def shipment_create(request):
    
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            
            cnf_information = form.cleaned_data.get('cnf_information')
            now=datetime.datetime.now()
            try:
                cnf_no = now.strftime("%m%d%Y")+"cnf"+str(Order.objects.order_by('-pk')[0].pk+1)
            except:
                cnf_no = now.strftime("%m%d%Y")+"cnf"+"#99"
            
            contact_person=form.cleaned_data.get('contact_person')
            city=form.cleaned_data.get('city')
            country = form.cleaned_data.get('country')
            state = form.cleaned_data.get('state')
            postal_code=form.cleaned_data.get('postal_code')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            street=form.cleaned_data.get('street')
            best_time_to_call=form.cleaned_data.get('best_time_to_call')
            
            
            CNF.objects.create(
                cnf_information=cnf_information, 
                cnf_no=cnf_no,contact_person=contact_person,
                city=city,
                country=country,
                state=state,
                street=street,
                postal_code=postal_code,
                email=email,
                phone=phone,
                best_time_to_call=best_time_to_call,
                
                )
            
            return redirect('shipment_list')
    else:
        form = ShipmentForm()

    return render(request, 'shipment/shipment_form.html', {'form': form})

def shipment_edit(request, shipment_id):
    shipment = get_object_or_404(CNF, id=shipment_id)
    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()
            return redirect('shipment_list')
    else:
        form = ShipmentForm(instance=shipment)
    return render(request, 'shipment/shipment_edit.html', {'form': form})

def shipment_order_select(request, shipment_id):
    shipment = get_object_or_404(CNF, id=shipment_id)
    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()
            return redirect('shipment_list')
    else:
        form = ShipmentForm(instance=shipment)
    return render(request, 'shipment/shipment_edit.html', {'form': form})
def shipment_delete(request, shipment_id):
    shipment = get_object_or_404(CNF, id=shipment_id)
    if request.method == 'POST':
        shipment.delete()
        return redirect('shipment_list')
    return render(request, 'shipment/shipment_confirm_delete.html', {'shipment': shipment})

def shipment_report(request):
    if request.method=='GET':
        try:
            from_date = request.GET.get('from', '')
            to_date = request.GET.get('to', '')
            
            from_date = datetime.datetime.strptime(request.GET.get('from', ''), '%Y/%m/%d').date()
            to_date = datetime.datetime.strptime(request.GET.get('to', ''), '%Y/%m/%d').date()
            
            shipments= ShipmentTracking.objects.filter(
                Q(order_received_date__gte=from_date) & Q(order_received_date__lte=to_date)
            )
            
            context={
                'shipments':shipments,

            }
            
        except:
            context={
                
            }
    else:
        
        url="http://127.0.0.1:8000"+request.get_full_path()
        
        chrome_path= 'chromedriver.exe'
        os.remove(os.getcwd()+'\\scrape.png')
        printableDiv='printable-div'
        filename=os.getcwd()+"\\order_report.pdf"
        os.remove(filename)
        
        pdf_convertor(chrome_path,url,printableDiv, filename)
        response = FileResponse(open(filename, 'rb'))
        
        return response
        
        context={
            
        }
    
        
    return render(request, 'tracking_order/tracking-report.html', context)

def shipment_report_list(request):
    shipments = ShipmentTracking.objects.all()
    return render(request, 'shipment/shipment_report_list.html', {'shipments': shipments})


def shipment_report_view(request, shipment_id):
    shipment = get_object_or_404(ShipmentTracking, id=shipment_id)
    products = Product.objects.filter(order_no=shipment.order_no)
    
    try:
        payment=get_object_or_404(Payment, order_no=shipment.order_no)
    except:
        payment=None
    customer_no=get_object_or_404(Order, order_no=shipment.order_no).company
    customer = get_object_or_404(Customer, customer_no=customer_no)
    cnf=get_object_or_404(CNF, cnf_no=shipment.cnf_no)
    return render(request, 'shipment/shipment_report_view.html', {'shipment': shipment, 'products':products, 'company': customer, 'cnf':cnf, 'payment':payment} )



def chalan_report_view(request, shipment_id):
    shipment = get_object_or_404(ShipmentTracking, id=shipment_id)
    products = Product.objects.filter(order_no=shipment.order_no)
    try:
        payment=get_object_or_404(Payment, order_no=shipment.order_no)
    except:
        payment=None
    customer_no=get_object_or_404(Order, order_no=shipment.order_no).company
    customer = get_object_or_404(Customer, customer_no=customer_no)
    cnf=get_object_or_404(CNF, cnf_no=shipment.cnf_no)
    return render(request, 'shipment/chalan_report_view.html', {'shipment': shipment, 'products':products, 'company': customer, 'cnf':cnf, 'payment':payment} )