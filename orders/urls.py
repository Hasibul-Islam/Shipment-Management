from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('create/<int:pk>/', views.order_create, name='order_create'),
    path('update/<int:pk>/', views.order_edit, name='order_update'),
    path('delete/<int:pk>/', views.order_delete, name='order_delete'),
    path('update_shipment/<int:pk>/', views.order_shipment, name='select_cnf'),
    
    path('update_shipment/<int:pk>/<int:cnf_pk>/', views.order_shipment_update, name='select_cnf_confirm'),
]
