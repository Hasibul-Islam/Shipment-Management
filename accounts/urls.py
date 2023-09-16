from django.urls import include, path
from . import views
urlpatterns = [
    
    path('registration/', views.register, name='registration'),
    path('login/', views.user_login, name='login'),
    path('user_logout/', views.user_logout, name='logout'),
    path('send_email/', views.send_email, name='send_email'),
    path('cnf_user_list/', views.all_users, name='all_users_cnf'),
    path('change_password_admin/<int:id>/', views.change_password_admin, name='change_password_admin'),
]