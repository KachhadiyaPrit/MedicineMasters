from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from medicine_masters.models import Users,DeliveryAddress,Category,Sub_Category,Company,Product,Offer,Order,Order_Detail,Notification,Cart_Detail,Prescription,Prescription_Detail,Payment
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Sum
from django.db.models import ExpressionWrapper, F
from django.db import models
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse

# Admin
# Admin Home Page
@login_required(login_url='login_page')
def admin_home(request):
    user = Users.objects.filter(user_type = 2).count()
    products = Product.objects.all().count()
    categories = Category.objects.all().count()

    context = {
        'user' : user,
        'products' : products,
        'categories' : categories
    }

    return render(request, 'admin/dashboard & profile/admin-home.html',context)

# Admin Profile Page
@login_required(login_url='login_page')
def admin_profile(request):
    return render(request, 'admin/dashboard & profile/admin-profile.html')

# Admin Profile Update Process
@login_required(login_url='login_page')
def admin_profile_update(request):
    if request.method == "POST":
        username = request.POST.get('user_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        users = Users.objects.get(user_id=request.user.user_id)

        users.username = username
        users.first_name = first_name
        users.last_name = last_name
        users.email = email
        users.save()
    
        return redirect('admin_profile')

    return render(request, 'admin/admin-profile.html')

# Category
# Add Category Page
@login_required(login_url='login_page')
def add_category_page(request):
    return render(request, 'admin/category/add_category.html')

# Category add into database
@login_required(login_url='login_page')
def add_category(request):
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        category_image = request.FILES.get('category_image')
        
        category = Category(
            category_name = category_name,
            category_img = category_image,
        )
        category.save()
    
        return redirect('add_category_page')
    return render(request, 'admin/category/add_category.html')

# View category page
@login_required(login_url='login_page')
def view_category(request):
    category = Category.objects.all()
    context = {
        'category':category,
    }
    return render(request, 'admin/category/view_category.html',context)

# Edit Category
@login_required(login_url='login_page')
def edit_category(request, category_id):
    category = Category.objects.get(category_id = category_id)
    context = {
        'category':category,
    }
    return render(request, 'admin/category/edit_category.html', context)

# Update Category
@login_required(login_url='login_page')
def update_category(request):
    if request.method == "POST":
        prev_img = request.POST.get('prev_img')
        category_id = request.POST.get('category_id')
        category_name = request.POST.get('category_name')
        category_image = request.FILES.get('category_image')
        
        category = Category.objects.get(category_id = category_id)
        
        category.category_id = category_id
        category.category_name = category_name
        if category_image == None:
            category.category_img = prev_img
        else:
            category.category_img = category_image
        category.save()
    
        return redirect('view_category')
    return render(request, 'admin/category/edit_category.html')

# Delete Category
@login_required(login_url='login_page')
def delete_category(request, category_id):
    category = Category.objects.get(category_id = category_id)
    category.delete()
    return redirect('view_category')

# Sub Category
# Add Sub Category Page
@login_required(login_url='login_page')
def add_subcategory_page(request):
    category = Category.objects.all()
    context = {
        'category':category,
    }
    return render(request, 'admin/sub category/add_subcategory.html',context)

# Sub Category add into database
@login_required(login_url='login_page')
def add_subcategory(request):
    if request.method == "POST":
        subcategory_name = request.POST.get('subcategory_name')
        subcategory_image = request.FILES.get('subcategory_image')
        category_id = request.POST.get('category_id')
        print('category_id = ',category_id)
        sub_category = Sub_Category(
            subcategory_name = subcategory_name,
            subcategory_img = subcategory_image,
            category_id = category_id,
        )
        sub_category.save()
    
        return redirect('add_subcategory_page')
    return render(request, 'admin/sub category/add_subcategory.html')

# View sub category page
@login_required(login_url='login_page')
def view_subcategory(request):
    subcategory = Sub_Category.objects.all()
    context = {
        'subcategory':subcategory,
    }
    return render(request, 'admin/sub category/view_subcategory.html',context)

# Edit Sub Category
@login_required(login_url='login_page')
def edit_subcategory(request, subcategory_id):
    subcategory = Sub_Category.objects.get(subcategory_id = subcategory_id)
    category = Category.objects.all()
    context = {
        'subcategory':subcategory,
        'category':category,
    }
    return render(request, 'admin/sub category/edit_subcategory.html', context)

# Updaye sub category
@login_required(login_url='login_page')
def update_subcategory(request):
    if request.method == "POST":
        prev_img = request.POST.get('prev_img')
        subcategory_id = request.POST.get('subcategory_id')
        subcategory_name = request.POST.get('subcategory_name')
        subcategory_image = request.FILES.get('subcategory_image')
        category_id = request.POST.get('category_id')
        
        subcategory = Sub_Category.objects.get(subcategory_id = subcategory_id)
        
        subcategory.subcategory_id = subcategory_id
        subcategory.subcategory_name = subcategory_name
        if subcategory_image == None:
            subcategory.subcategory_img = prev_img
        else:
            subcategory.subcategory_img = subcategory_image
        subcategory.category_id = category_id
        subcategory.save()
    
        return redirect('view_subcategory')
    return render(request, 'admin/sub category/edit_subcategory.html')

# Delete Sub Category
@login_required(login_url='login_page')
def delete_subcategory(request, subcategory_id):
    subcategory = Sub_Category.objects.get(subcategory_id = subcategory_id)
    subcategory.delete()
    messages.success(request, 'Sub Category Are Successfully Deleted...')
    return redirect('view_subcategory')

# Company
# Add company page
@login_required(login_url='login_page')
def add_company_page(request):
    return render(request, 'admin/company/add_company.html')

# Add company
@login_required(login_url='login_page')
def add_company(request):
    if request.method == "POST":
        company_name = request.POST.get('company_name')
        company_owner_name = request.POST.get('company_owner_name')
        company_owner_email = request.POST.get('company_owner_email')
        company_owner_phone = request.POST.get('company_owner_phone')
        company_address = request.POST.get('company_address')
        
        company = Company(
            company_name = company_name,
            company_owner_name = company_owner_name,
            company_owner_email = company_owner_email,
            company_owner_phone = company_owner_phone,
            company_address = company_address,
        )
        company.save()
    
        return redirect('add_company_page')
    return render(request, 'admin/company/add_company.html')

# View company page
@login_required(login_url='login_page')
def view_company(request):
    company = Company.objects.all()
    context = {
        'company':company,
    }
    return render(request, 'admin/company/view_company.html',context)

# Edit Company
@login_required(login_url='login_page')
def edit_company(request, company_id):
    company = Company.objects.get(company_id = company_id)
    context = {
        'company':company,
    }
    return render(request, 'admin/company/edit_company.html', context)

# Update Company
@login_required(login_url='login_page')
def update_company(request):
    if request.method == "POST":
        company_id = request.POST.get('company_id')
        company_name = request.POST.get('company_name')
        company_owner_name = request.POST.get('company_owner_name')
        company_owner_email = request.POST.get('company_owner_email')
        company_owner_phone = request.POST.get('company_owner_phone')
        company_address = request.POST.get('company_address')
        
        company = Company.objects.get(company_id = company_id)
        
        company.company_id = company_id
        company.company_name = company_name
        company.company_owner_name = company_owner_name
        company.company_owner_email = company_owner_email
        company.company_owner_phone = company_owner_phone
        company.company_address = company_address
        company.save()
    
        return redirect('view_company')
    return render(request, 'admin/company/edit_company.html')

# Delete Company
@login_required(login_url='login_page')
def delete_company(request, company_id):
    company = Company.objects.get(company_id = company_id)
    print('company',company)
    company.delete()
    messages.success(request, 'Company Are Successfully Deleted...')
    return redirect('view_company')

# Product
# Add Product Page
@login_required(login_url='login_page')
def add_product_page(request):
    company = Company.objects.all()
    subcategory = Sub_Category.objects.all()
    context = {
        'company':company,
        'subcategory':subcategory,
    }
    return render(request, 'admin/product/add_product.html',context)

# Product add into database
@login_required(login_url='login_page')
def add_product(request):
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_price = request.POST.get('product_price')
        product_discount_price = request.POST.get('product_discount_price')
        product_quantity = request.POST.get('product_quantity')
        product_expirydate = request.POST.get('product_expirydate')
        product_prescription_status = request.POST.get('product_prescription_status')
        company_id = request.POST.get('company_id')
        subcategory_id = request.POST.get('subcategory_id')
        product_weight = request.POST.get('product_weight')
        product_madein = request.POST.get('product_madein')
        product_advantage = request.POST.get('product_advantage')
        product_disadvantage = request.POST.get('product_disadvantage')
        product_image = request.FILES.get('product_image')
        
        product = Product(
            product_name = product_name,
            product_description = product_description,
            product_price = product_price,
            product_discount_price = product_discount_price,
            product_quantity = product_quantity,
            product_expirydate = product_expirydate,
            product_prescription_status = product_prescription_status,
            company_id = company_id,
            subcategory_id = subcategory_id,
            product_weight = product_weight,
            product_madein = product_madein,
            product_advantage = product_advantage,
            product_disadvantage = product_disadvantage,
            product_img = product_image,
        )
        product.save()
    
        return redirect('add_product_page')
    return render(request, 'admin/product/add_product.html')

# View Product
@login_required(login_url='login_page')
def view_product(request):
    product = Product.objects.all()
    context = {
        'product':product,
    }
    return render(request, 'admin/product/view_product.html',context)

# Edit product
@login_required(login_url='login_page')
def edit_product(request, product_id):
    product = Product.objects.get(product_id = product_id)
    subcategory = Sub_Category.objects.all()
    company = Company.objects.all()
    context = {
        'product':product,
        'subcategory':subcategory,
        'company':company,
    }
    return render(request, 'admin/product/edit_product.html', context)

# Update product
@login_required(login_url='login_page')
def update_product(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_price = request.POST.get('product_price')
        product_discount_price = request.POST.get('product_discount_price')
        product_quantity = request.POST.get('product_quantity')
        product_expirydate = request.POST.get('product_expirydate')
        product_prescription_status = request.POST.get('product_prescription_status')
        company_id = request.POST.get('company_id')
        subcategory_id = request.POST.get('subcategory_id')
        product_weight = request.POST.get('product_weight')
        product_madein = request.POST.get('product_madein')
        product_advantage = request.POST.get('product_advantage')
        product_disadvantage = request.POST.get('product_disadvantage')
        product_image = request.FILES.get('product_image')
        prev_img = request.POST.get('prev_img')
        
        product = Product.objects.get(product_id = product_id)

        product.product_name = product_name
        product.product_description = product_description
        product.product_price = product_price
        product.product_discount_price = product_discount_price
        product.product_quantity = product_quantity
        product.product_expirydate = product_expirydate
        product.product_prescription_status = product_prescription_status
        product.company_id = company_id
        product.product_weight = product_weight
        product.product_madein = product_madein
        product.product_advantage = product_advantage
        product.product_disadvantage = product_disadvantage
        product.subcategory_id = subcategory_id
        if product_image == None:
            product.product_img = prev_img
        else:
            product.product_img = product_image
        product.save()

        cart_detail = Cart_Detail.objects.filter(product_id = product_id)
        for i in cart_detail:
            i.prescription_status = product_prescription_status
            i.save()
    
        return redirect('view_product')
    return render(request, 'admin/product/view_product.html')

# Delete Company
@login_required(login_url='login_page')
def delete_product(request, product_id):
    product = Product.objects.get(product_id = product_id)
    product.delete()
    messages.success(request, 'Company Are Successfully Deleted...')
    return redirect('view_product')

# Offer
# Add offer Page
@login_required(login_url='login_page')
def add_offer_page(request):
    return render(request, 'admin/offer/add_offer.html')

# Offer add into database
@login_required(login_url='login_page')
def add_offer(request):
    if request.method == "POST":
        offer_code = request.POST.get('offer_code')
        offer_rate = request.POST.get('offer_rate')
        offer_required_amount = request.POST.get('offer_required_amount')
        offer_description = request.POST.get('offer_description')
        offer_image = request.FILES.get('offer_image')
        
        offer = Offer(
            offer_code = offer_code,
            offer_rate = offer_rate,
            offer_required_amount = offer_required_amount,
            offer_description = offer_description,
            offer_img = offer_image,
        )
        offer.save()
    
        return redirect('add_offer_page')
    return render(request, 'admin/offer/add_offer.html')

# View Offer
@login_required(login_url='login_page')
def view_offer(request):
    offer = Offer.objects.all()
    context = {
        'offer':offer,
    }
    return render(request, 'admin/offer/view_offer.html',context)

# Edit Offer
@login_required(login_url='login_page')
def edit_offer(request, offer_id):
    offer = Offer.objects.get(offer_id = offer_id)
    context = {
        'offer':offer,
    }
    return render(request, 'admin/offer/edit_offer.html', context)

# Update offer
@login_required(login_url='login_page')
def update_offer(request):
    if request.method == "POST":
        offer_id = request.POST.get('offer_id')
        offer_code = request.POST.get('offer_code')
        offer_rate = request.POST.get('offer_rate')
        offer_required_amount = request.POST.get('offer_required_amount')
        offer_description = request.POST.get('offer_description')
        offer_image = request.FILES.get('offer_image')
        prev_img = request.POST.get('prev_img')
        
        offer = Offer.objects.get(offer_id = offer_id)

        offer.offer_code = offer_code
        offer.offer_rate = offer_rate
        offer.offer_required_amount = offer_required_amount
        offer.offer_description = offer_description
        if offer_image == None:
            offer.offer_img = prev_img
        else:
            offer.offer_img = offer_image
        offer.save()
    
        return redirect('view_offer')
    return render(request, 'admin/offer/view_offer.html')

# Delete Offer
@login_required(login_url='login_page')
def delete_offer(request, offer_id):
    offer = Offer.objects.get(offer_id = offer_id)
    offer.delete()
    messages.success(request, 'Company Are Successfully Deleted...')
    return redirect('view_offer')

# User
# View Users
@login_required(login_url='login_page')
def view_user(request):
    users = Users.objects.filter(user_type = 2)
    context = {
        'users':users,
    }
    return render(request, 'admin/user/view_user.html',context)

# View User Detail
@login_required(login_url='login_page')
def view_user_detail(request, user_id):
    user = Users.objects.get(user_id = user_id)
    order = Order.objects.filter(user_id = user_id)
    order_count = Order.objects.filter(user_id = user_id).count()
    
    total_payments = 0
    for i in order:
        total_payments += i.order_total_amount
    
    context = {
        'user':user,
        'order_count':order_count,
        'total_payment':total_payments
    }
    return render(request, 'admin/user/view_user_detail.html',context)

# User delete
@login_required(login_url='login_page')
def delete_user(request, user_id):
    user = Users.objects.get(user_id = user_id)
    user.delete()
    messages.success(request, 'User Are Successfully Deleted...')
    return redirect('view_user')

# Change user order status
@login_required(login_url='login_page')
def change_status(request, user_id):
    user = Users.objects.get(user_id = user_id)
    if user.is_active == 1:
        user.is_active = 0
        user.save()
    else:
        user.is_active = 1
        user.save()
    return redirect('view_user_detail', user_id)

# Send mail to all
@login_required(login_url='login_page')
def send_mail_to_all(request):
    if request.method == "POST":
        email_msg = request.POST.get('email_msg')
        users = Users.objects.filter(user_type = 2)

        for i in users:
            send_mail(
                'Message To Medicine Masters',
                'Hello '+i.username+' '+email_msg,
                'medicinemasters23@gmail.com',
                [i.email],
                fail_silently=False,
            )
    return render(request, 'admin/user/view_user.html')

# Order
# Order History
@login_required(login_url='login_page')
def order_history(request):
    order = Order.objects.all()
    context = {
        'order' : order,
    }
    return render(request, 'admin/order history/view_order_history.html',context)

# Order History Detail
@login_required(login_url='login_page')
def order_history_detail(request, order_id):
    order = Order.objects.get(order_id = order_id)
    order_detail = Order_Detail.objects.filter(order_id = order_id)
    for i in order_detail:
        prescription_status = Prescription_Detail.objects.all()
    order_tracking_id = Order_Detail.objects.filter(order_id = order_id).first()
    
    context = {
        'order_detail' : order_detail,
        'order_tracking_id' : order_tracking_id,
        'prescription_status' : prescription_status,
        'order':order
    }
    return render(request, 'admin/order history/view_order_detail.html',context)
    
# Update Order status
@login_required(login_url='login_page')
def update_order_status(request):
    if request.method == "POST":
        order_tracking_id = request.POST.get('order_tracking_id')
        order_status = request.POST.get('order_status')
        
        order = Order.objects.get(order_tracking_id = order_tracking_id)
        order.order_status = order_status
        order.save()

    return render(request, 'admin/order history/view_order_detail.html')

# Order delete
@login_required(login_url='login_page')
def delete_order(request, order_id):
    order = Order.objects.get(order_id = order_id)
    order.delete()
    messages.success(request, 'User Are Successfully Deleted...')
    return redirect('order_history')

# Send user order releted mail
@login_required(login_url='login_page')
def order_mail(request, user_email):
    order_releted_mail = request.POST.get('order_releted_mail')

    send_mail(
        'Message To Medicine Masters',
        order_releted_mail,
        'medicinemasters23@gmail.com',
        [user_email],
        fail_silently=False,
        )
    return render(request, 'admin/order history/view_order_detail.html')

# Offer
# Add offer Page
@login_required(login_url='login_page')
def add_notification_page(request):
    user = Users.objects.all()
    context = {
        'user': user,
    }
    return render(request, 'admin/notification/add_notification.html', context)

# Notification add into database
@login_required(login_url='login_page')
def add_notification(request):
    if request.method == "POST":
        notification_message = request.POST.get('notification_message')
        
        notification = Notification(
            notification_message = notification_message,
            user_id = request.user.user_id
        )
        notification.save()
        return redirect('add_notification_page')
    return render(request, 'admin/notification/add_notification.html')

# Doctor
# Add Doctor Page
@login_required(login_url='login_page')
def add_doctor_page(request):
    return render(request, 'admin/doctor/add_doctor.html')

# Add Doctor
@login_required(login_url='login_page')
def add_doctor(request):
    if request.method == "POST":
        username = request.POST.get('username')
        doctor_first_name = request.POST.get('doctor_first_name')
        doctor_last_name = request.POST.get('doctor_last_name')
        doctor_email = request.POST.get('doctor_email')
        doctor_gender = request.POST.get('doctor_gender')
        doctor_password = request.POST.get('doctor_password')

        user = Users(
            username = username,
            first_name = doctor_first_name,
            last_name = doctor_last_name,
            email = doctor_email,
            gender = doctor_gender,
            password=make_password(doctor_password),
            user_type = 3
        )
        user.save()
        
        send_mail(
            'Message To Medicine Masters',
            'Hello '+doctor_first_name+' '+doctor_last_name + ' This is notify mail to login this email and password, Email : ' + doctor_email + ' Password : ' + doctor_password + '.',
            'medicinemasters23@gmail.com',
            [doctor_email],
            fail_silently=False,
        )

        return redirect('add_doctor_page')
    return render(request, 'admin/doctor/add_doctor.html')

# View Doctor
@login_required(login_url='login_page')
def view_doctor(request):
    doctor = Users.objects.filter(user_type = 3)
    context = {
        'doctor':doctor,
    }
    return render(request, 'admin/doctor/view_doctor.html',context)

# Delete doctor
@login_required(login_url='login_page')
def delete_doctor(request, doctor_id):
    doctor = Users.objects.get(user_id = doctor_id)
    doctor.delete()
    messages.success(request, 'User Are Successfully Deleted...')
    return redirect('view_doctor')


# Payment
# Payment History
@login_required(login_url='login_page')
def payment_history(request):
    payment = Payment.objects.all()
    context = {
        'payment' : payment,
    }
    return render(request, 'admin/payment history/payment_history.html',context)

def most_selling_report(request):
    most_selling_products = Order_Detail.objects.values('product_id','product_name','product__product_discount_price') \
        .annotate(total_quantity=Sum('product_quantity')) \
        .annotate(product_total=Sum(ExpressionWrapper(F('product_quantity') * F('product__product_discount_price'), output_field=models.IntegerField()))) \
        .order_by('-total_quantity')[:10]

    total = most_selling_products.aggregate(Sum('product_total'))['product_total__sum']

    context = {'most_selling_products': most_selling_products,'total':total}

    template_path = 'reports/most_selling_report.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ProductSellReport.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    return response