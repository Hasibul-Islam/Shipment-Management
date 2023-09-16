from django.urls import path
from . import views



urlpatterns = [
    # List view - /payments/
    path('', views.payment_list, name='payment_list'),

    # Create view - /payments/create/
    path('create/<int:pk>/', views.create_payment, name='payment_create'),
    path('view/<int:pk>/', views.payment_detail, name='view_payment'),
    # Update view - /payments/1/update/
    path('update/<int:pk>/', views.update_payment, name='payment_update'),

    # Delete view - /payments/1/delete/
    path('delete/<int:pk>/', views.delete_payment, name='payment_delete'),
]
