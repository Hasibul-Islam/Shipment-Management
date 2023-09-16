from django.shortcuts import render, get_object_or_404, redirect
from .models import CompanyDetails
from .forms import CompanyDetailsForm
from datetime import datetime
# Create
def create_company_details(request):
    if request.method == 'POST':
        now = datetime.now()
        try:
            customer_no = now.strftime("%m%d%Y")+str(CompanyDetails.objects.order_by('-pk')[0].pk+1)
        except:
            customer_no = now.strftime("%m%d%Y")+'#1'
        form = CompanyDetailsForm(request.POST, instance=CompanyDetails(customer_no=customer_no))
        if form.is_valid():
            
            form.save()
            return redirect('company_details_list')
    else:
        form = CompanyDetailsForm()
    return render(request, 'company/company_details_form.html', {'form': form})

# Read
def company_details_list(request):
    company_details = CompanyDetails.objects.all()
    
    return render(request, 'company/company_details_list.html', {'company_details': company_details})

def company_details_detail(request, pk):
    company_details = get_object_or_404(CompanyDetails, pk=pk)
    return render(request, 'company/company_details_detail.html', {'company_details': company_details})

# Update

def update_company_details(request, pk):
    company_details = get_object_or_404(CompanyDetails, pk=pk)
    form = CompanyDetailsForm(request.POST or None, instance=company_details)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('company_details_detail', pk=company_details.pk)
    return render(request, 'company/company_details_form.html', {'form': form, 'my_object': company_details})
# Delete

