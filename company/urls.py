from django.urls import path
from .views import create_company_details, company_details_list, company_details_detail, update_company_details

urlpatterns = [
    path('', company_details_list, name='company_details_list'),
    path('create/', create_company_details, name='create_company_details'),
    path('<int:pk>/details/', company_details_detail, name='company_details_detail'),
    path('<int:pk>/update/', update_company_details, name='update_company_details'),
    
]
