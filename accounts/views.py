from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib import messages
User = get_user_model()
from django.db.models import Q
from django.core.mail import EmailMessage
from shipment_tracking.views import send_delayed_email
def register(request):
    if request.user.is_authenticated==False:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            # print(form)
            if form.is_valid():
                email = form.cleaned_data['email']
                if User.objects.filter(username=email).exists():
                     messages.error(request,"Email already exists") # your error message
                     return redirect(request.path)
                user = form.save()
                # login(request, user)
                group_name = request.POST.get('group_name')
                print(group_name)
                if group_name == 'Admin':
                    admin_group = Group.objects.get(name='Admin')
                    admin_group.user_set.add(user)
                elif group_name == 'Manager':
                    manager_group = Group.objects.get(name='Manager')
                    manager_group.user_set.add(user)
                elif group_name == 'Employee':
                    employee_group = Group.objects.get(name='Employee')
                    employee_group.user_set.add(user)
                elif group_name == 'CNF':
                    employee_group = Group.objects.get(name='CNF')
                    employee_group.user_set.add(user)
                return redirect('login')
        else:
            form = CustomUserCreationForm()
        return render(request, 'accounts/registration.html', {'form': form})
    else:
        return redirect('home')
def user_login(request):
    if request.user.is_authenticated==False:
        if request.method == 'POST':
            # Get the username and password from the POST request
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            # If the user is authenticated, log them in and redirect to a success page
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # If the user is not authenticated, display an error message
                error_message = "Invalid login credentials. Please try again."
                return render(request, 'accounts/login.html', {'error_message': error_message})

        # If the request method is GET, display the login form
        return render(request, 'accounts/login.html')
    else:
        return redirect('home')
def user_logout(request):
    # Logout the user using Django's logout() function
    logout(request)
    return redirect('login')

def send_email(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        text_content = request.POST['message']
        html_content = "<p><strong>"+text_content+"</strong></p>"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [request.POST['to_email']]
        print(subject,text_content,recipient_list)
        send_delayed_email(subject, text_content, html_content, from_email, recipient_list)
        return redirect('home')
    else:
        return render(request, 'accounts/send_email.html')
    

def all_users(request):
    users = User.objects.filter(Q(groups__name='CNF')|Q(groups__name='Manager'))
    return render(request, 'accounts/list_users.html', {'users':users})

def change_password_admin(request, id):
    user=get_object_or_404(User, id=id)
    if request.method=="POST":
        newpass=request.POST.get('newpass', '')
        user.set_password(newpass)
        return redirect('all_users_cnf')
    return render(request, 'accounts/change_password_admin.html')