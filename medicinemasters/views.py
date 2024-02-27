from django.shortcuts import render, redirect, HttpResponse
from medicine_masters.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from medicine_masters.models import Users,DeliveryAddress,Category,Sub_Category,Company,Product,Offer,Order,Order_Detail,Cart,Cart_Detail
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

# login and signup screen send
def login_page(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')
# Login Process
def dologin(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'),)

        if user != None: 
            login(request, user)
            user_type = user.user_type
            if user_type == 1:
                return redirect('admin_home')
            elif user_type == 2:
                return redirect('users_home')
            elif user_type == 3:
                return redirect('doctor_home')
            else:
                # Message For Not Match User Type...
                message = 'User are Invalid !!'
                return render(request, 'login.html',{'error':message})
        else:
            # Message For User Is Not Exist...
            message = 'Email and password are Invalid !'
            # Message For User Is Not Exist...
            return render(request, 'login.html',{'error':message})

# Logout Process
def dologout(request):
    logout(request)
    return redirect('users_home')

# Check username at live time to write user
def check_username(request):
    username = request.POST.get('username')
    if username != "":
        if get_user_model().objects.filter(username=username).exists():
            return HttpResponse('<div style="color: red;"><i class="fa-regular fa-circle-xmark"></i> This username already exists </div>')
        else:
            return HttpResponse('<div style="color: green;"><i class="fa-regular fa-circle-check"></i> This username is available for you </div>')
    else:
        return HttpResponse('<div></div>')

# Check email at live time to write user
def check_email(request):
    email = request.POST.get('email')
    if email != "":
        if get_user_model().objects.filter(email=email).exists():
            return HttpResponse('<div style="color: red;"><i class="fa-regular fa-circle-xmark"></i> This email already exists </div>')
        else:
            return HttpResponse('<div style="color: green;"><i class="fa-regular fa-circle-check"></i> This email is available for you </div>')
    else:
        return HttpResponse('<div></div>')
    
# Registration Process
def dosignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        passw = request.POST.get('password')
        password = make_password(passw)

        if Users.username == username:
            message = 'User are Invalid !!'
            return render(request, 'login.html',{'error':message})
        else:
            signup = Users(
                username = username,
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = password,
            )
            signup.save()
            
            address = DeliveryAddress(
                user_id = signup.user_id,
                delivery_address = '',
            )
            address.save()

            send_mail(
                'Message To Medicine Masters',
                'Congratulations '+first_name+' '+last_name+' To join Medicine Masters,after login you setup your profile like address etc.',
                'medicinemasters23@gmail.com',
                [email],
                fail_silently=False,
            )

            cart = Cart(
                user_id = signup.user_id,
            )
            cart.save()
                
            return redirect(login_page)        

