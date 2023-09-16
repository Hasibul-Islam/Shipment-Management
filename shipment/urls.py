from django.urls import path
from . import views

urlpatterns = [
    path('', views.shipment_list, name='shipment_list'),
    path('report/', views.shipment_report_list, name='shipment_report_list'),
    path('generate-report/', views.shipment_report, name='generate_shipment_report'),
    # path('download/<str:url>', views.download, name='download_shipment'),
    path('create/', views.shipment_create, name='shipment_create'),
    path('details/<int:shipment_id>', views.shipment_detail, name='shipment_detail'),
    path('<int:shipment_id>/edit/', views.shipment_edit, name='shipment_edit'),
    path('<int:shipment_id>/delete/', views.shipment_delete, name='shipment_delete'),
    path('shipment_report_view/<int:shipment_id>/', views.shipment_report_view, name='shipment_report_view'),
    path('chalan_report_view/<int:shipment_id>/', views.chalan_report_view, name='chalan_report_view'),
]
