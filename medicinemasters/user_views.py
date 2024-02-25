from urllib import request
from django.shortcuts import render, redirect, HttpResponse
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from medicine_masters import helpers
from medicine_masters.models import Users,DeliveryAddress,Category,Sub_Category,Company,Product,Offer,Order,Order_Detail,Cart,Cart_Detail,Feedback,Prescription,Prescription_Detail
import razorpay
from django.conf import settings
from django.http import JsonResponse

# Users Home Page
def users_home(request):
    if request.user.is_authenticated and request.user.user_type == 1:
            return redirect('admin_home')
    elif request.user.is_authenticated and request.user.user_type == 3:
        return redirect('doctor_home')
    else:
        if request.user.is_authenticated:
            cart_object = Cart.objects.get(user_id = request.user.user_id)
            cart = Cart_Detail.objects.filter(cart_id = cart_object.cart_id)
        else:
            cart = Cart_Detail.objects.all()
        product = Product.objects.all()
        product_count = Product.objects.all().count()
        category = Sub_Category.objects.all()
        category_count = Sub_Category.objects.all().count()

        context = {
            'product' : product,
            'product_count' : product_count,
            'category' : category,
            'category_count' : category_count,
            'cart' : cart
        }
        if request.user.is_authenticated and request.user.user_type == 1:
            return render(request, 'admin/dashboard & profile/admin-home.html')
        else:
            return render(request, 'users/Home.html', context)

# Users Profile
def users_profile(request):
    users = Users.objects.get(user_id=request.user.user_id)
    deliveryaddress = DeliveryAddress.objects.get(user_id=users.user_id)
    offers = Offer.objects.all()
    
    return render(request, 'users/Profile.html',{'address':deliveryaddress, 'offer':offers})

# Profile Update Process
def profile_update(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        user_name = request.POST.get('user_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        bod = request.POST.get('bod')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        prev_img = request.POST.get('prev_img')
        
        users = Users.objects.get(user_id=request.user.user_id)

        if profile_pic == None:
            users.profile_pic = prev_img
        else:
            users.profile_pic = profile_pic
        users.username = user_name
        users.first_name = first_name
        users.last_name = last_name
        users.email = email
        users.phone = phone
        users.gender = gender
        users.bod = bod
        users.address = address
        users.pincode = pincode
        users.save()
    
        return redirect('users_profile')

    return render(request, 'users/Profile.html')

# Edit delivery address
def edit_address(request):
    if request.method == "POST":
        edit_delivery_address = request.POST.get('delivery_address')
        edit_delivery_address_pincode = request.POST.get('delivery_address_pincode')

        users = Users.objects.get(user_id=request.user.user_id)
        deliveryaddress = DeliveryAddress.objects.get(user_id=users.user_id)

        deliveryaddress.delivery_address = edit_delivery_address
        deliveryaddress.delivery_address_pincode = edit_delivery_address_pincode
        deliveryaddress.save()

        return redirect('users_profile')

    return render(request, 'users/Profile.html')

# Users All Product
def all_product(request):
    product = Product.objects.all()
    if request.user.is_authenticated:
        cart_object = Cart.objects.get(user_id = request.user.user_id)
        cart = Cart_Detail.objects.filter(cart_id = cart_object.cart_id)
    product_count = Product.objects.all().count()
    category = Sub_Category.objects.all()
    company = Company.objects.all()
    main_category = Category.objects.all()
    category_count = Sub_Category.objects.all().count()

    context = {
        'product' : product,
        'product_count' : product_count,
        'category' : category,
        'category_count' : category_count,
        'cart' : cart,
        'main_category' : main_category,
        'company' : company,
    }

    return render(request, 'users/All_Product.html', context)

# Users All Category
def all_category(request):
    category = Sub_Category.objects.all()
    context = {
        'category' : category,
    }
    return render(request, 'users/All_Category.html', context)

# Users Product Detail
def product_detail(request, product_id):
    product = Product.objects.get(product_id = product_id)
    if request.user.is_authenticated:
        cart = Cart_Detail.objects.filter(user_id = request.user.user_id)
    else:
        cart = Cart_Detail.objects.all()
    product_detail = product.product_description
    save = int(product.product_price) - int(product.product_discount_price)
    similar_product = Product.objects.filter(subcategory_id = product.subcategory.subcategory_id)

    context = {
        'product' : product,
        'save' : save,
        'product_detail' : product_detail,
        'cart' : cart,
        'similar_product' : similar_product
    }
    return render(request, 'users/Product_Detail.html', context)

# Users Add Cart
def add_to_cart(request):
    if request.method == "POST":
        product_id_cart_item = request.POST.get('product_id_cart_item')

        products = Product.objects.get(product_id = product_id_cart_item)
        product = Product.objects.all()
        product_count = Product.objects.all().count()
        category = Sub_Category.objects.all()
        category_count = Sub_Category.objects.all().count()

        cart_item = Cart.objects.filter(user_id=request.user.user_id).first()
        cart_item_detail = Cart_Detail.objects.filter(cart_id = cart_item.cart_id,product_id = product_id_cart_item).first()
        cart_details = Cart_Detail.objects.filter(product_id = product_id_cart_item)


        context = {
            'product' : product,
            'product_count' : product_count,
            'category' : category,
            'category_count' : category_count,
            'cart_item' : cart_item,
            'cart_item_detail' : cart_item_detail,
            'products' : products,
        }

        if not cart_item:
            cart = Cart(
                user_id = request.user.user_id,
            )
            cart.save()
            cart_detail = Cart_Detail(
                cart_quantity = 1,
                cart_product_price = products.product_discount_price,
                cart_id = cart_item.cart_id,
                product_id = products.product_id,
                prescription_status = products.product_prescription_status,
                user_id = request.user.user_id,
            )
            cart_detail.save()
            cart_detail.cart_total_price = cart_detail.cart_quantity * products.product_discount_price
            cart_detail.save()
            messages.success(request, "Item added to your cart.")
        else:
            if not cart_item_detail:
                cart_detail = Cart_Detail(
                    cart_quantity = 1,
                    cart_product_price = products.product_discount_price,
                    cart_id = cart_item.cart_id,
                    product_id = products.product_id,
                    prescription_status = products.product_prescription_status,
                    user_id = request.user.user_id,
                )
                cart_detail.save()
                cart_detail.cart_total_price = cart_detail.cart_quantity * products.product_discount_price
                cart_detail.save()
                messages.success(request, "Item added to your cart.")
            else:
                for i in cart_details:
                    if i.product_id == products.product_id:
                        i.cart_quantity += 1
                        i.save()
                        i.cart_total_price = int(i.cart_quantity) * int(products.product_discount_price)
                        i.save()
                    else:
                        cart_detail = Cart_Detail(
                            cart_quantity = 1,
                            cart_product_price = products.product_discount_price,
                            cart_id = cart_item.cart_id,
                            product_id = products.product_id,
                            prescription_status = products.product_prescription_status,
                            user_id = request.user.user_id,
                        )
                        cart_detail.save()
                        cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(products.product_discount_price)
                        cart_detail.save()
                        messages.success(request, "Item added to your cart.")

    return render(request, 'users/Home.html', context)

# Users Add Cart
def add_to_cart_all_product(request):
    if request.method == "POST":
        all_product_id_cart_item = request.POST.get('all_product_id_cart_item')

        products = Product.objects.get(product_id = all_product_id_cart_item)
        product = Product.objects.all()
        product_count = Product.objects.all().count()
        category = Sub_Category.objects.all()
        category_count = Sub_Category.objects.all().count()

        cart_item = Cart.objects.filter(user_id=request.user.user_id).first()
        cart_item_detail = Cart_Detail.objects.filter(cart_id = cart_item.cart_id,product_id = all_product_id_cart_item).first()
        cart_details = Cart_Detail.objects.filter(product_id = all_product_id_cart_item)


        context = {
            'product' : product,
            'product_count' : product_count,
            'category' : category,
            'category_count' : category_count,
            'cart_item' : cart_item,
            'cart_item_detail' : cart_item_detail,
            'products' : products,
        }

        if not cart_item:
            cart = Cart(
                user_id = request.user.user_id,
            )
            cart.save()
            cart_detail = Cart_Detail(
                cart_quantity = 1,
                cart_product_price = products.product_discount_price,
                cart_id = cart_item.cart_id,
                product_id = products.product_id,
                prescription_status = products.product_prescription_status,
                user_id = request.user.user_id,
            )
            cart_detail.save()
            cart_detail.cart_total_price = cart_detail.cart_quantity * products.product_discount_price
            cart_detail.save()
            messages.success(request, "Item added to your cart.")
        else:
            if not cart_item_detail:
                cart_detail = Cart_Detail(
                    cart_quantity = 1,
                    cart_product_price = products.product_discount_price,
                    cart_id = cart_item.cart_id,
                    product_id = products.product_id,
                    prescription_status = products.product_prescription_status,
                    user_id = request.user.user_id,
                )
                cart_detail.save()
                cart_detail.cart_total_price = cart_detail.cart_quantity * products.product_discount_price
                cart_detail.save()
                messages.success(request, "Item added to your cart.")
            else:
                for i in cart_details:
                    if i.product_id == products.product_id:
                        i.cart_quantity += 1
                        i.save()
                        i.cart_total_price = int(i.cart_quantity) * int(products.product_discount_price)
                        i.save()
                    else:
                        cart_detail = Cart_Detail(
                            cart_quantity = 1,
                            cart_product_price = products.product_discount_price,
                            cart_id = cart_item.cart_id,
                            product_id = products.product_id,
                            prescription_status = products.product_prescription_status,
                            user_id = request.user.user_id,
                        )
                        cart_detail.save()
                        cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(products.product_discount_price)
                        cart_detail.save()
                        messages.success(request, "Item added to your cart.")

    return render(request, 'users/All_Product.html', context)

# Cart view
def cart_view(request):
    cart = Cart.objects.all()
    cart_item = Cart.objects.get(user_id = request.user.user_id)
    cart_detail = Cart_Detail.objects.filter(cart_id = cart_item.cart_id)
    total_product_in_cart = Cart_Detail.objects.filter(cart_id = cart_item.cart_id).count()
    total = 0
    for i in cart_detail:
        total += int(i.cart_total_price)
    context = {
        'cart_item' : cart_item,
        'cart_detail' : cart_detail,
        'total' : total,
        'total_product_in_cart' : total_product_in_cart
    }
    return render(request, 'users/Cart_View.html', context)

# Add qty
def plus_qty(request, product_id):
    product = Product.objects.all()
    cart = Cart_Detail.objects.all()
    product_count = Product.objects.all().count()
    category = Sub_Category.objects.all()
    category_count = Sub_Category.objects.all().count()
    
    cart_detail = Cart_Detail.objects.get(product_id = product_id, user_id = request.user.user_id)
    
    if cart_detail:
        cart_detail.cart_quantity = cart_detail.cart_quantity+1
        cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(cart_detail.product.product_discount_price)
        cart_detail.save()

    context = {
        'product' : product,
        'product_count' : product_count,
        'category' : category,
        'category_count' : category_count,
        'cart' : cart
    }

    return render(request, 'users/Home.html', context)

# Minus qty
def minus_qty(request, product_id):
    product = Product.objects.all()
    cart = Cart_Detail.objects.all()
    product_count = Product.objects.all().count()
    category = Sub_Category.objects.all()
    category_count = Sub_Category.objects.all().count()
    
    cart_detail = Cart_Detail.objects.get(product_id = product_id, user_id = request.user.user_id)

    if cart_detail:
        if cart_detail.cart_quantity == 1 :
            cart_detail.delete()
        else:
            cart_detail.cart_quantity = cart_detail.cart_quantity-1
            cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(cart_detail.product.product_discount_price)
            cart_detail.save()

    context = {
        'product' : product,
        'product_count' : product_count,
        'category' : category,
        'category_count' : category_count,
        'cart' : cart
    }

    return render(request, 'users/Home.html', context)

# Cart plus qty
def cart_qty_plus(request, product_id):
    cart_detail = Cart_Detail.objects.get(product_id = product_id, user_id = request.user.user_id)
    
    if cart_detail:
        cart_detail.cart_quantity = cart_detail.cart_quantity+1
        cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(cart_detail.product.product_discount_price)
        cart_detail.save()

    cart_item = Cart.objects.get(user_id = request.user.user_id)
    cart_details = Cart_Detail.objects.filter(cart_id = cart_item.cart_id)
    total = 0
    for i in cart_details:
        total += int(i.cart_total_price)

    context = {
        'cart_item' : cart_item,
        'total' : total
    }

    return render(request, 'users/Cart_View.html', context)

# Cart Minus qty
def cart_qty_minus(request, product_id):
    cart_detail = Cart_Detail.objects.get(product_id = product_id, user_id = request.user.user_id)

    if cart_detail:
        if cart_detail.cart_quantity == 1 :
            cart_detail.delete()
        else:
            cart_detail.cart_quantity = cart_detail.cart_quantity-1
            cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(cart_detail.product.product_discount_price)
            cart_detail.save()
        
    cart_item = Cart.objects.get(user_id = request.user.user_id)
    cart_details = Cart_Detail.objects.filter(cart_id = cart_item.cart_id)
    total = 0
    for i in cart_details:
        total += int(i.cart_total_price)

    context = {
        'cart_item' : cart_item,
        'total' : total
    }

    return render(request, 'users/Cart_View.html', context)

#all product qty plus
def all_product_plus_qty(request, product_id):
    if request.method == "POST":
        product = Product.objects.all()
        cart = Cart_Detail.objects.all()
        product_count = Product.objects.all().count()
        category = Sub_Category.objects.all()
        category_count = Sub_Category.objects.all().count()
    
        cart_detail = Cart_Detail.objects.get(product_id = product_id, user_id = request.user.user_id)
        cart_qty = cart_detail.cart_quantity

        if cart_detail:
            cart_detail.cart_quantity = cart_qty+1
            cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(cart_detail.product.product_discount_price)
            cart_detail.save()

        context = {
            'product' : product,
            'product_count' : product_count,
            'category' : category,
            'category_count' : category_count,
            'cart' : cart
        }

    return render(request, 'users/All_Product.html', context)

#all product qty plus
def all_product_by_category_plus_qty(request, product_id):
    if request.method == "POST":
        product = Product.objects.all()
        cart = Cart_Detail.objects.all()
        product_count = Product.objects.all().count()
        category = Sub_Category.objects.all()
        category_count = Sub_Category.objects.all().count()
    
        cart_detail = Cart_Detail.objects.get(product_id = product_id, user_id = request.user.user_id)
        cart_qty = cart_detail.cart_quantity

        if cart_detail:
            cart_detail.cart_quantity = cart_qty+1
            cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(cart_detail.product.product_discount_price)
            cart_detail.save()

        context = {
            'product' : product,
            'product_count' : product_count,
            'category' : category,
            'category_count' : category_count,
            'cart' : cart
        }

    return render(request, 'users/All_Product_By_Category.html', context)

#all product qty minus
def all_product_minus_qty(request, product_id):
    product = Product.objects.all()
    cart = Cart_Detail.objects.all()
    product_count = Product.objects.all().count()
    category = Sub_Category.objects.all()
    category_count = Sub_Category.objects.all().count()
    
    cart_detail = Cart_Detail.objects.get(product_id = product_id, user_id = request.user.user_id)

    if cart_detail:
        if cart_detail.cart_quantity == 1 :
            cart_detail.delete()
        else:
            cart_detail.cart_quantity = cart_detail.cart_quantity-1
            cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(cart_detail.product.product_discount_price)
            cart_detail.save()

    context = {
        'product' : product,
        'product_count' : product_count,
        'category' : category,
        'category_count' : category_count,
        'cart' : cart
    }

    return render(request, 'users/All_Product.html', context)

#all product qty minus
def all_product_by_category_minus_qty(request, product_id):
    product = Product.objects.all()
    cart = Cart_Detail.objects.all()
    product_count = Product.objects.all().count()
    category = Sub_Category.objects.all()
    category_count = Sub_Category.objects.all().count()
    
    cart_detail = Cart_Detail.objects.get(product_id = product_id, user_id = request.user.user_id)

    if cart_detail:
        if cart_detail.cart_quantity == 1 :
            cart_detail.delete()
        else:
            cart_detail.cart_quantity = cart_detail.cart_quantity-1
            cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(cart_detail.product.product_discount_price)
            cart_detail.save()

    context = {
        'product' : product,
        'product_count' : product_count,
        'category' : category,
        'category_count' : category_count,
        'cart' : cart
    }

    return render(request, 'users/All_Product_By_Category.html', context)
    

# Product detail cart qty plus
def product_detail_plus_qty(request, product_id):
    if request.method == "POST":
        product = Product.objects.get(product_id = product_id)
        cart = Cart_Detail.objects.all()
        product_count = Product.objects.all().count()
        category = Sub_Category.objects.all()
        category_count = Sub_Category.objects.all().count()
    
        cart_detail = Cart_Detail.objects.get(product_id = product_id, user_id = request.user.user_id)
        cart_qty = cart_detail.cart_quantity

        if cart_detail:
            cart_detail.cart_quantity = cart_qty+1
            cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(cart_detail.product.product_discount_price)
            cart_detail.save()

        context = {
            'product' : product,
            'product_count' : product_count,
            'category' : category,
            'category_count' : category_count,
            'cart' : cart
        }

    return render(request, 'users/Product_Detail.html', context)

# Product detail cart qty plus
def product_detail_minus_qty(request, product_id):
    if request.method == "POST":
        product = Product.objects.get(product_id = product_id)
        cart = Cart_Detail.objects.all()
        product_count = Product.objects.all().count()
        category = Sub_Category.objects.all()
        category_count = Sub_Category.objects.all().count()
    
        cart_detail = Cart_Detail.objects.get(product_id = product_id, user_id = request.user.user_id)

        if cart_detail:
            if cart_detail.cart_quantity == 1 :
                cart_detail.delete()
            else:
                cart_detail.cart_quantity = cart_detail.cart_quantity-1
                cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(cart_detail.product.product_discount_price)
                cart_detail.save()

        context = {
            'product' : product,
            'product_count' : product_count,
            'category' : category,
            'category_count' : category_count,
            'cart' : cart
        }

    return render(request, 'users/Product_Detail.html', context)

# Users Add Cart
def add_to_cart_product_detail(request , product_id):
    if request.method == "POST":
        product = Product.objects.get(product_id = product_id)
        cart_item = Cart.objects.get(user_id=request.user.user_id)
        cart_item_detail = Cart_Detail.objects.filter(cart_id = cart_item.cart_id,product_id = product_id)
        cart_details = Cart_Detail.objects.filter(product_id = product_id)
        cart = Cart_Detail.objects.all()

        context = {
            'cart_item' : cart_item,
            'cart_item_detail' : cart_item_detail,
            'product' : product,
            'cart' : cart,
        }

        if not cart_item:
            cart = Cart(
                user_id = request.user.user_id,
            )
            cart.save()

            cart_detail = Cart_Detail(
                cart_quantity = 1,
                cart_product_price = product.product_discount_price,
                cart_id = cart_item.cart_id,
                product_id = product.product_id,
                prescription_status = product.product_prescription_status,
                user_id = request.user.user_id,
            )
            cart_detail.save()

            cart_detail.cart_total_price = cart_detail.cart_quantity * product.product_discount_price
            cart_detail.save()

            messages.success(request, "Item added to your cart.")

        else:
            if not cart_item_detail:
                cart_detail = Cart_Detail(
                    cart_quantity = 1,
                    cart_product_price = product.product_discount_price,
                    cart_id = cart_item.cart_id,
                    product_id = product.product_id,
                    prescription_status = product.product_prescription_status,
                    user_id = request.user.user_id,
                )
                cart_detail.save()

                cart_detail.cart_total_price = cart_detail.cart_quantity * product.product_discount_price
                cart_detail.save()

                messages.success(request, "Item added to your cart.")

            else:
                for i in cart_details:
                    if i.product_id == product.product_id:
                        i.cart_quantity += 1
                        i.save()

                        i.cart_total_price = int(i.cart_quantity) * int(product.product_discount_price)
                        i.save()

                    else:
                        cart_detail = Cart_Detail(
                            cart_quantity = 1,
                            cart_product_price = product.product_discount_price,
                            cart_id = cart_item.cart_id,
                            product_id = product.product_id,
                            prescription_status = product.product_prescription_status,
                            user_id = request.user.user_id,
                        )
                        cart_detail.save()

                        cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(product.product_discount_price)
                        cart_detail.save()

                        messages.success(request, "Item added to your cart.")

    return render(request, 'users/Product_Detail.html', context)

# Users Add Cart All Product By Category
def add_to_cart_all_product_by_category(request , product_id):
    if request.method == "POST":
        products = Product.objects.get(product_id = product_id)
        cart_item = Cart.objects.get(user_id=request.user.user_id)
        cart_item_detail = Cart_Detail.objects.filter(cart_id = cart_item.cart_id,product_id = product_id)
        cart_details = Cart_Detail.objects.filter(product_id = product_id)
        cart = Cart_Detail.objects.all()

        if not cart_item:
            cart = Cart(
                user_id = request.user.user_id,
            )
            cart.save()

            cart_detail = Cart_Detail(
                cart_quantity = 1,
                cart_product_price = products.product_discount_price,
                cart_id = cart_item.cart_id,
                product_id = products.product_id,
                prescription_status = products.product_prescription_status,
                user_id = request.user.user_id,
            )
            cart_detail.save()

            cart_detail.cart_total_price = cart_detail.cart_quantity * products.product_discount_price
            cart_detail.save()

            messages.success(request, "Item added to your cart.")

        else:
            if not cart_item_detail:
                cart_detail = Cart_Detail(
                    cart_quantity = 1,
                    cart_product_price = products.product_discount_price,
                    cart_id = cart_item.cart_id,
                    product_id = products.product_id,
                    prescription_status = products.product_prescription_status,
                    user_id = request.user.user_id,
                )
                cart_detail.save()

                cart_detail.cart_total_price = cart_detail.cart_quantity * products.product_discount_price
                cart_detail.save()

                messages.success(request, "Item added to your cart.")

            else:
                for i in cart_details:
                    if i.product_id == products.product_id:
                        i.cart_quantity += 1
                        i.save()

                        i.cart_total_price = int(i.cart_quantity) * int(products.product_discount_price)
                        i.save()

                    else:
                        cart_detail = Cart_Detail(
                            cart_quantity = 1,
                            cart_product_price = products.product_discount_price,
                            cart_id = cart_item.cart_id,
                            product_id = products.product_id,
                            prescription_status = products.product_prescription_status,
                            user_id = request.user.user_id,
                        )
                        cart_detail.save()

                        cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(products.product_discount_price)
                        cart_detail.save()

                        messages.success(request, "Item added to your cart.")

    return render(request, 'users/All_Product_By_Category.html')

# Checkout view
def checkout(request, product_id):
    checkout_product = Product.objects.get(product_id = product_id)
    checkout_price = Product.objects.filter(product_id = product_id)
    address = DeliveryAddress.objects.get(user_id = request.user.user_id)
    prescription_status = Cart_Detail.objects.filter(product_id = product_id ,prescription_status = 0).count()
    discount = 0
    total = 0

    for i in checkout_price:
        discount = int(i.product_discount_price) * 2 / 100

    for i in checkout_price:
        total = i.product_discount_price
    
    after_discount_value = total - discount + 10

    context = {
        'checkout_product':checkout_product,
        'address':address,
        'discount':discount,
        'after_discount_value':after_discount_value,
        'prescription_status':prescription_status
    }
    return render(request, 'users/Checkout.html', context)

# Cart Checkout view
def cart_checkout(request, cart_id):
    cart_items = Cart_Detail.objects.filter(cart_id = cart_id)
    prescription_status = Cart_Detail.objects.filter(cart_id = cart_id, prescription_status = 0).count()
    address = DeliveryAddress.objects.get(user_id = request.user.user_id)
    offer_code = request.POST.get('offer_code')
    offer_detail = Offer.objects.filter(offer_code = offer_code)
    total = 0
    discount = 0
    after_discount_value = 0
    shipping_cost = 10
    
    for i in cart_items:
        total += int(i.cart_total_price)
        
    for i in offer_detail:
        discount = total * i.offer_rate / 100
        
    after_discount_value = total - discount + shipping_cost

    client = razorpay.Client(auth=('rzp_test_SXFY1D0zq29TGB', 'js7DS3s7maZsQXyF11Fx4xK3'))
    payment = client.order.create({'amount':(after_discount_value), 'currency':'INR','payment_capture':1})

    context = {
        'cart_items':cart_items,
        'address':address,
        'total':total,
        'discount' : discount,
        'after_discount_value':after_discount_value,
        'shipping_cost':shipping_cost,
        'payment':payment,
        'prescription_status':prescription_status
    }
    
    return render(request, 'users/Cart_Checkout.html', context)

# Cart Checkout Order view
def cart_checkout_order(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        order_total_amount = request.POST.get('order_total_amount')
        order_amount = request.POST.get('order_amount')
        order_discount = request.POST.get('order_discount')
        shipping_price = request.POST.get('shipping_price')
        prescription_img = request.FILES.get('prescription_img')

        cart_user = Cart.objects.get(user_id=request.user.user_id)
        cart_items = Cart_Detail.objects.filter(cart_id = cart_user.cart_id)
        
        order = Order(
            order_total_amount = order_total_amount,
            order_amount = order_amount,
            order_discount_price = order_discount,
            user_id = request.user.user_id
        )
        order.save()

        prescription = Prescription(
            prescription_img = prescription_img,
            user_id = request.user.user_id,
        )
        prescription.save()

        for i in cart_items:
            order_detail = Order_Detail( 
                product_name = i.product.product_name,
                product_quantity = i.cart_quantity,
                product_price = i.product.product_discount_price,
                product = i.product,
                order_id = order.order_id,
                user_id = request.user.user_id
            )
            order_detail.save()
        
            if i.product.product_prescription_status == 0:
                prescription_detail = Prescription_Detail(
                    order_detail_id = order_detail.order_detail_id,
                    prescription_id = prescription.prescription_id,
                    user_id = request.user.user_id
                )
                prescription_detail.save()
            
    return render(request, 'users/Cart_Checkout.html')

# Checkout Order view
def checkout_order(request, product_id):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        order_total_amount = request.POST.get('order_total_amount')
        order_amount = request.POST.get('order_amount')
        order_discount = request.POST.get('order_discount')
        prescription_img = request.FILES.get('prescription_img')
        cart_user = Cart.objects.get(user_id=request.user.user_id)
        
        product = Product.objects.get(product_id = product_id)
        
        order = Order(
            order_total_amount = order_total_amount,
            order_amount = order_amount,
            order_discount_price = order_discount,
            user_id = request.user.user_id
        )
        order.save()

        order_detail = Order_Detail( 
            product_name = product.product_name,
            product_quantity = 1,
            product_price = product.product_discount_price,
            product = product,
            order_id = order.order_id,
            user_id = request.user.user_id
        )
        order_detail.save()

        prescription = Prescription(
            prescription_img = prescription_img,
            user_id = request.user.user_id,
        )
        prescription.save()

        prescription_detail = Prescription_Detail(
            order_detail_id = order_detail.order_detail_id,
            prescription_id = prescription.prescription_id,
            user_id = request.user.user_id
        )
        prescription_detail.save()

    return render(request, 'users/Checkout.html')

# Order View Page
def track_order(request):
    order = Order.objects.filter(user_id=request.user.user_id)
    order_detail = Order_Detail.objects.filter(user_id=request.user.user_id)
    context = {
        'order':order,
        'order_detail':order_detail
    }
    return render(request, 'users/Track_Order.html', context)
    
def track_order_detail(request, order_tracking_id, order_id):
    order_detail = Order_Detail.objects.filter(order_id = order_id)
    order_tracking_id = order_tracking_id
    order = Order.objects.get(order_tracking_id = order_tracking_id)
    context = {
        'order_detail':order_detail,
        'order_tracking_id':order_tracking_id,
        'order':order
    }
    return render(request, 'users/Track_Order_Detail.html', context)

def all_product_by_category(request, category_id):
    product = Product.objects.filter(subcategory_id = category_id)
    category_name = Sub_Category.objects.get(subcategory_id = category_id)
    if request.user.is_authenticated:
        cart = Cart_Detail.objects.filter(user_id = request.user.user_id)
    else:
        cart = Cart_Detail.objects.all()
    context = {
        'product' : product,
        'category_name' : category_name,
        'cart' : cart,
        'category_id' : category_id,
    }
    return render(request, 'users/All_Product_By_Category.html', context)

# def generate_invoice(request, order_id):
#     pass
    
def delete_cart_item(request, cart_detail_id):
    cart = Cart.objects.all()
    cart_item = Cart.objects.get(user_id = request.user.user_id)
    cart_detail = Cart_Detail.objects.filter(cart_id = cart_item.cart_id)
    total_product_in_cart = Cart_Detail.objects.filter(cart_id = cart_item.cart_id).count()
    
    delete_item = Cart_Detail.objects.get(cart_detail_id = cart_detail_id)
    delete_item.delete()
    
    total = 0
    for i in cart_detail:
        total += int(i.cart_total_price)
    context = {
        'cart_item' : cart_item,
        'cart_detail' : cart_detail,
        'total' : total,
        'total_product_in_cart' : total_product_in_cart
    }
    return render(request, 'users/Cart_View.html', context)

# Delete Company
def cancle_order(request, order_id):
    order = Order.objects.get(order_id = order_id)
    order.delete()
    return redirect('track_order')

def feedback(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback_message = request.POST.get('feedback_message')
        
        if request.user.is_authenticated:
            feedback = Feedback(
                name = name,
                email = email,
                feedback_message = feedback_message,
                user_id = request.user.user_id
            )
            feedback.save()
        else:
            feedback = Feedback(
                name = name,
                email = email,
                feedback_message = feedback_message
            )
            feedback.save()
        return redirect('users_home')

# Get Prescription
def get_prescription(request):
    if request.method == "POST":
        prescription_message = request.POST.get('prescription_message')
        prescription = Prescription(
            user_id = request.user.user_id
        )
        prescription.save()
        prescription_detail = Prescription_Detail(
            prescription_message = prescription_message,
            prescription_status = 'Pending',
            prescription_id = prescription.prescription_id,
            user_id = request.user.user_id
        )
        prescription_detail.save()
        return redirect('users_profile')

#  Serarch
def get_search(request):
    search = request.GET.get('search')
    payload = []

    if search:
        products = Product.objects.filter(product_name__startswith = search)
        categories = Sub_Category.objects.filter(subcategory_name__startswith = search)
        company = Company.objects.filter(company_name__startswith = search)
        if products:
            for product in products:
                payload.append({
                    'name' : product.product_name,
                    'id' : product.product_id,
                    'snippet' : product.product_description,
                    'product' : True
                })

        if categories:
            for category in categories:
                payload.append({
                    'name' : category.subcategory_name,
                    'id' : category.subcategory_id,
                    'snippet' : category.category.category_name,
                    'category' : True
                })

        if company:
            for company in company:
                payload.append({
                    'name' : company.company_name,
                    'id' : company.company_id,
                    'snippet' : company.company_owner_email,
                    'company' : True
                })

    return JsonResponse({
        'status' : True,
        'payload' : payload,
    })

# All product by company
def all_product_by_company(request, company_id):
    product = Product.objects.filter(company_id = company_id)
    company_name = Company.objects.get(company_id = company_id)
    if request.user.is_authenticated:
        cart = Cart_Detail.objects.filter(user_id = request.user.user_id)
    else:
        cart = Cart_Detail.objects.all()
    context = {
        'product' : product,
        'company_name' : company_name,
        'cart' : cart,
        'company_id' : company_id,
    }
    return render(request, 'users/All_Product_By_Company.html', context)

# Add cart in all product by company
def add_to_cart_all_product_by_company(request , product_id):
    if request.method == "POST":
        products = Product.objects.get(product_id = product_id)
        cart_item = Cart.objects.get(user_id=request.user.user_id)
        cart_item_detail = Cart_Detail.objects.filter(cart_id = cart_item.cart_id,product_id = product_id)
        cart_details = Cart_Detail.objects.filter(product_id = product_id)
        cart = Cart_Detail.objects.all()

        if not cart_item:
            cart = Cart(
                user_id = request.user.user_id,
            )
            cart.save()

            cart_detail = Cart_Detail(
                cart_quantity = 1,
                cart_product_price = products.product_discount_price,
                cart_id = cart_item.cart_id,
                product_id = products.product_id,
                prescription_status = products.product_prescription_status,
                user_id = request.user.user_id,
            )
            cart_detail.save()

            cart_detail.cart_total_price = cart_detail.cart_quantity * products.product_discount_price
            cart_detail.save()

            messages.success(request, "Item added to your cart.")

        else:
            if not cart_item_detail:
                cart_detail = Cart_Detail(
                    cart_quantity = 1,
                    cart_product_price = products.product_discount_price,
                    cart_id = cart_item.cart_id,
                    product_id = products.product_id,
                    prescription_status = products.product_prescription_status,
                    user_id = request.user.user_id,
                )
                cart_detail.save()

                cart_detail.cart_total_price = cart_detail.cart_quantity * products.product_discount_price
                cart_detail.save()

                messages.success(request, "Item added to your cart.")

            else:
                for i in cart_details:
                    if i.product_id == products.product_id:
                        i.cart_quantity += 1
                        i.save()

                        i.cart_total_price = int(i.cart_quantity) * int(products.product_discount_price)
                        i.save()

                    else:
                        cart_detail = Cart_Detail(
                            cart_quantity = 1,
                            cart_product_price = products.product_discount_price,
                            cart_id = cart_item.cart_id,
                            product_id = products.product_id,
                            prescription_status = products.product_prescription_status,
                            user_id = request.user.user_id,
                        )
                        cart_detail.save()

                        cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(products.product_discount_price)
                        cart_detail.save()

                        messages.success(request, "Item added to your cart.")

    return render(request, 'users/All_Product_By_Company.html')

#all product qty plus
def all_product_by_company_plus_qty(request, product_id):
    if request.method == "POST":
        product = Product.objects.all()
        cart = Cart_Detail.objects.all()
        product_count = Product.objects.all().count()
        category = Sub_Category.objects.all()
        category_count = Sub_Category.objects.all().count()
    
        cart_detail = Cart_Detail.objects.get(product_id = product_id, user_id = request.user.user_id)
        cart_qty = cart_detail.cart_quantity

        if cart_detail:
            cart_detail.cart_quantity = cart_qty+1
            cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(cart_detail.product.product_discount_price)
            cart_detail.save()

        context = {
            'product' : product,
            'product_count' : product_count,
            'category' : category,
            'category_count' : category_count,
            'cart' : cart
        }

    return render(request, 'users/All_Product_By_Company.html', context)

#all product qty minus
def all_product_by_company_minus_qty(request, product_id):
    product = Product.objects.all()
    cart = Cart_Detail.objects.all()
    product_count = Product.objects.all().count()
    category = Sub_Category.objects.all()
    category_count = Sub_Category.objects.all().count()
    
    cart_detail = Cart_Detail.objects.get(product_id = product_id, user_id = request.user.user_id)

    if cart_detail:
        if cart_detail.cart_quantity == 1 :
            cart_detail.delete()
        else:
            cart_detail.cart_quantity = cart_detail.cart_quantity-1
            cart_detail.cart_total_price = int(cart_detail.cart_quantity) * int(cart_detail.product.product_discount_price)
            cart_detail.save()

    context = {
        'product' : product,
        'product_count' : product_count,
        'category' : category,
        'category_count' : category_count,
        'cart' : cart
    }

    return render(request, 'users/All_Product_By_Company.html', context)
