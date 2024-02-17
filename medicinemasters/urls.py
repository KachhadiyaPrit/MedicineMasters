"""
URL configuration for medicinemasters project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views, user_views, admin_views, doctor_view

urlpatterns = [ 
    # Login Or Registration Page Url
    path('login_signup', views.login_signup, name='login_signup'),
    
    # Login Or Signup Process Page Url
    path('dologin', views.dologin, name='dologin'),
    path('dosignup', views.dosignup, name='dosignup'),
    path('check_username', views.check_username, name='check_username'),
    path('dologout', views.dologout, name='dologout'),
    
    # Admin Home Page Url
    path('admin', admin_views.admin_home, name='admin_home'),

    # Admin Profile Url
    path('admin/profile', admin_views.admin_profile, name='admin_profile'),
    path('admin/profile_update', admin_views.admin_profile_update, name='admin_profile_update'),

    # Admin To Category Url 
    path('admin/add_category_page', admin_views.add_category_page, name='add_category_page'),
    path('admin/add_category', admin_views.add_category, name='add_category'),
    path('admin/view_category', admin_views.view_category, name='view_category'),
    path('admin/edit_category/<str:category_id>', admin_views.edit_category, name='edit_category'),
    path('admin/update_category', admin_views.update_category, name='update_category'),
    path('admin/delete_category/<str:category_id>', admin_views.delete_category, name='delete_category'),

    # Admin To Sub Category
    path('admin/add_subcategory_page', admin_views.add_subcategory_page, name='add_subcategory_page'),
    path('admin/add_subcategory', admin_views.add_subcategory, name='add_subcategory'),
    path('admin/view_subcategory', admin_views.view_subcategory, name='view_subcategory'),
    path('admin/edit_subcategory/<str:subcategory_id>', admin_views.edit_subcategory, name='edit_subcategory'),
    path('admin/update_subcategory', admin_views.update_subcategory, name='update_subcategory'),
    path('admin/delete_subcategory/<str:subcategory_id>', admin_views.delete_subcategory, name='delete_subcategory'),

    # Admin To Company
    path('admin/add_company_page', admin_views.add_company_page, name='add_company_page'),
    path('admin/add_company', admin_views.add_company, name='add_company'),
    path('admin/view_company', admin_views.view_company, name='view_company'),
    path('admin/edit_company/<str:company_id>', admin_views.edit_company, name='edit_company'),
    path('admin/update_company', admin_views.update_company, name='update_company'),
    path('admin/delete_company/<str:company_id>', admin_views.delete_company, name='delete_company'),

    # Admin To Product
    path('admin/add_product_page', admin_views.add_product_page, name='add_product_page'),
    path('admin/add_product', admin_views.add_product, name='add_product'),
    path('admin/view_product', admin_views.view_product, name='view_product'),
    path('admin/edit_product/<str:product_id>', admin_views.edit_product, name='edit_product'),
    path('admin/update_product', admin_views.update_product, name='update_product'),
    path('admin/delete_product/<str:product_id>', admin_views.delete_product, name='delete_product'),

    # Admin To Offer
    path('admin/add_offer_page', admin_views.add_offer_page, name='add_offer_page'),
    path('admin/add_offer', admin_views.add_offer, name='add_offer'),
    path('admin/view_offer', admin_views.view_offer, name='view_offer'),
    path('admin/edit_offer/<str:offer_id>', admin_views.edit_offer, name='edit_offer'),
    path('admin/update_offer', admin_views.update_offer, name='update_offer'),
    path('admin/delete_offer/<str:offer_id>', admin_views.delete_offer, name='delete_offer'),

    # Admin To User
    path('admin/view_user', admin_views.view_user, name='view_user'),
    path('admin/view_user_detail/<int:user_id>', admin_views.view_user_detail, name='view_user_detail'),
    path('admin/delete_user/<str:user_id>', admin_views.delete_user, name='delete_user'),
    path('admin/view_user_detail/change_status/<str:user_id>', admin_views.change_status, name='change_status'),
    path('admin/send_mail_to_all', admin_views.send_mail_to_all, name='send_mail_to_all'),

    # Admin To Order History
    path('admin/order_history', admin_views.order_history, name="order_history"),
    path('admin/order_history_detail/<str:order_id>', admin_views.order_history_detail, name="order_history_detail"),
    path('admin/update_order_status', admin_views.update_order_status, name="update_order_status"),
    
    # Admin To Notification
    path('admin/add_notification_page', admin_views.add_notification_page, name='add_notification_page'),
    path('admin/add_notification', admin_views.add_notification, name='add_notification'),

    # Admin To Doctor
    path('admin/add_doctor_page', admin_views.add_doctor_page, name='add_doctor_page'),
    path('admin/add_doctor', admin_views.add_doctor, name='add_doctor'),

    # Doctor
    # Doctor Home Page Url
    path('doctor', doctor_view.doctor_home, name='doctor_home'),
    path('doctor/view_all_prescription', doctor_view.view_all_prescription, name='view_all_prescription'),
    path('doctor/view_prescription_details/<int:prescription_id>', doctor_view.view_prescription_details, name='view_prescription_details'),
    path('doctor/view_got_prescriptions', doctor_view.view_got_prescriptions, name='view_got_prescriptions'),
    path('doctor/view_got_prescriptions/generate_prescription_page/<int:prescription_id>', doctor_view.generate_prescription_page, name='generate_prescription_page'),
    path('doctor/view_got_prescriptions/generate_prescription_page/send_prescription', doctor_view.send_prescription, name='send_prescription'),

    # User Home Page Url, Profile / Profile Update Url, Add / Edit Address Url
    path('', user_views.users_home, name='users_home'),    
    path('user/profile', user_views.users_profile, name='users_profile'),
    path('user/profile_update', user_views.profile_update, name='profile_update'),
    path('edit_address', user_views.edit_address, name='edit_address'),
    path('user/all_products', user_views.all_product, name='all_product'),
    path('user/all_category', user_views.all_category, name='all_category'),
    path('user/add_to_cart', user_views.add_to_cart, name='add_to_cart'),
    path('user/delete_cart_item/<int:cart_detail_id>', user_views.delete_cart_item, name='selete_cart_item'),
    path('user/all_product/add_to_cart_all_product', user_views.add_to_cart_all_product, name='add_to_cart_all_product'),
    path('user/cart_view', user_views.cart_view, name='cart_view'),
    path('user/plus_qty/<int:product_id>', user_views.plus_qty, name='plus_qty'),
    path('user/minus_qty/<int:product_id>', user_views.minus_qty, name='minus_qty'),
    path('user/product_detail/<str:product_id>', user_views.product_detail, name='product_detail'),
    path('user/all_product_plus_qty/<int:product_id>', user_views.all_product_plus_qty, name='all_product_plus_qty'),
    path('user/all_product_minus_qty/<int:product_id>', user_views.all_product_minus_qty, name='all_product_minus_qty'),
    path('user/all_product_by_category/all_product_by_category_plus_qty/<int:product_id>', user_views.all_product_by_category_plus_qty, name='all_product_by_category_plus_qty'),
    path('user/all_product_by_company/all_product_by_company_plus_qty/<int:product_id>', user_views.all_product_by_company_plus_qty, name='all_product_by_company_plus_qty'),
    path('user/all_product_by_category/all_product_by_category_minus_qty/<int:product_id>', user_views.all_product_by_category_minus_qty, name='all_product_by_category_minus_qty'),
    path('user/all_product_by_company/all_product_by_company_minus_qty/<int:product_id>', user_views.all_product_by_company_minus_qty, name='all_product_by_company_minus_qty'),
    path('user/cart_qty_plus/<int:product_id>', user_views.cart_qty_plus, name='cart_qty_plus'),
    path('user/cart_qty_minus/<int:product_id>', user_views.cart_qty_minus, name='cart_qty_minus'),
    path('user/add_to_cart_product_detail/<str:product_id>', user_views.add_to_cart_product_detail, name='add_to_cart_product_detail'),
    path('user/all_product_by_category/add_to_cart_all_product_by_category/<int:product_id>', user_views.add_to_cart_all_product_by_category, name='add_to_cart_all_product_by_category'),
    path('user/all_product_by_company/add_to_cart_all_product_by_company/<int:product_id>', user_views.add_to_cart_all_product_by_company, name='add_to_cart_all_product_by_company'),
    path('user/product_detail_plus_qty/<str:product_id>', user_views.product_detail_plus_qty, name='product_detail_plus_qty'),
    path('user/product_detail_minus_qty/<str:product_id>', user_views.product_detail_minus_qty, name='product_detail_minus_qty'),
    path('user/checkout/<str:product_id>', user_views.checkout, name='checkout'),
    path('user/cart_checkout/<int:cart_id>', user_views.cart_checkout, name='cart_checkout'),
    path('user/cart_checkout_order', user_views.cart_checkout_order, name='cart_checkout_order'),
    path('user/checkout/checkout_order/<int:product_id>', user_views.checkout_order, name='checkout_order'),
    path('user/profile/track_order', user_views.track_order, name='track_order'),
    path('user/profile/track_order/track_order_detail/<str:order_tracking_id>/<int:order_id>', user_views.track_order_detail, name='track_order_detail'),
    path('user/profile/track_order/cancle_order/<int:order_id>', user_views.cancle_order, name='cancle_order'),
    path('user/all_product_by_category/<int:category_id>', user_views.all_product_by_category, name='all_product_by_category'),
    path('user/all_product_by_company/<int:company_id>', user_views.all_product_by_company, name='all_product_by_company'),
    path('generateinvoice/<int:order_id>/', user_views.GenerateInvoice.as_view(), name = 'generateinvoice'),
    path('user/profile/get_prescription', user_views.get_prescription, name = 'get_prescription'),
    path('feedback', user_views.feedback, name = 'feedback'),
    path('get-search/', user_views.get_search, name = 'get-search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
