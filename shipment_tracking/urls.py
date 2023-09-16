from django.urls import path
from shipment_tracking.views import view_shipment, shipment_confirm_update_buyer, tracking_list, shipment_confirm_update_cnf, tracking_list_cnf, thank_you

urlpatterns = [
    # path('update/<str:shipment_id>', shipment_tracking_edit, name='shipment_tracking_edit'),
    path('view/<int:pk>/', view_shipment, name='view_shipment'),
    path('update/<int:pk>/', shipment_confirm_update_buyer, name='shipment_confirm_update_buyer'),
    path('update-cnf/<int:pk>/', shipment_confirm_update_cnf, name='shipment_confirm_update_cnf'),
    path('list/', tracking_list, name='tracking_list'),
    path('list-cnf/', tracking_list_cnf, name='tracking_list_cnf'),
    path('thank-you/', thank_you, name='thank_you'),
]